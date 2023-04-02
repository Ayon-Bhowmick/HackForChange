import os
import cv2
import numpy as np
from tqdm import tqdm
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import logging
import sys
import pickle

BUILD_DATA = True
LOAD_MODEL = False

class PlantDataMaker():
    log = logging.getLogger("info")
    TRAIN_PATH = "./plants/dataset"
    TEST_PATH = "./plants/dataset-test"
    training_data = []
    testing_data = []
    class_map = {}

    def makeTrainingData(self):
        self.log.info("Making training data")
        for i, dir in enumerate(tqdm(os.listdir(self.TRAIN_PATH))):
            self.class_map[i] = dir
            for file in os.listdir(os.path.join(self.TRAIN_PATH, dir)):
                try:
                    path = os.path.join(self.TRAIN_PATH, dir, file)
                    img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
                    # 1920x1080
                    img = cv2.resize(img, (600, 600))
                    img = cv2.copyMakeBorder(img, 2, 2, 2, 2, cv2.BORDER_CONSTANT, value=0)
                    self.training_data.append([np.array(img), np.eye(62)[i]])
                except Exception as e:
                    self.log.error(e)
        np.random.shuffle(self.training_data)
        np.save("plant_training_data.npy", self.training_data)
        with open("plant_class_map.pkl", "wb") as f:
            pickle.dump(self.class_map, f)

    def makeTestingData(self):
        self.log.info("Making testing data")
        for i, dir in enumerate(tqdm(os.listdir(self.TEST_PATH))):
            for file in os.listdir(os.path.join(self.TRAIN_PATH, dir)):
                try:
                    path = os.path.join(self.TRAIN_PATH, dir, file)
                    img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
                    # 1920x1080
                    img = cv2.resize(img, (600, 600))
                    img = cv2.copyMakeBorder(img, 2, 2, 2, 2, cv2.BORDER_CONSTANT, value=0)
                    self.training_data.append([np.array(img), np.eye(62)[i]])
                except Exception as e:
                    self.log.error(e)
        np.random.shuffle(self.training_data)
        np.save("plant_testing_data.npy", self.training_data)

class AyonNet(nn.Module):
    def __init__(self):
        super().__init__()
        self.conv1 = nn.Conv2d(1, 32, 5)
        self.conv2 = nn.Conv2d(32, 64, 5)
        self.conv3 = nn.Conv2d(64, 128, 5)
        self.conv4 = nn.Conv2d(128, 256, 5)
        self.conv5 = nn.Conv2d(256, 512, 5)
        self.fc1 = nn.Linear(512 * 5 * 5, 1024)
        self.fc2 = nn.Linear(1024, 1024)
        self.fc3 = nn.Linear(1024, 1024)
        self.fc4 = nn.Linear(1024, 512)
        self.fc5 = nn.Linear(512, 62)

    def convs(self, x):
        x = F.max_pool2d(F.relu(self.conv1(x)), (2, 2))
        x = F.max_pool2d(F.relu(self.conv2(x)), (2, 2))
        x = F.max_pool2d(F.relu(self.conv3(x)), (2, 2))
        x = F.max_pool2d(F.relu(self.conv4(x)), (3, 3))
        x = F.max_pool2d(F.relu(self.conv5(x)), (3, 3))
        x = x.view(-1, 512 * 5 * 5)

    def forward(self):
        x = self.convs(x)
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = F.relu(self.fc3(x))
        x = F.relu(self.fc4(x))
        x = self.fc5(x)
        return x


if __name__ == "__main__":
    logging.basicConfig(stream=sys.stdout)
    logging.getLogger("info").setLevel(logging.INFO)
    log = logging.getLogger("info")
    plant = PlantDataMaker()
    if BUILD_DATA:
        plant.makeTrainingData()
        plant.makeTestingData()
        training_data = plant.training_data
        testing_data = plant.testing_data
        class_map = plant.class_map
    else:
        training_data = np.load("plant_training_data.npy", allow_pickle=True)
        testing_data = np.load("plant_testing_data.npy", allow_pickle=True)
        with open("plant_class_map.pkl", "rb") as f:
            class_map = pickle.load(f)
    net = AyonNet()
    optimizer = optim.Adam(net.parameters(), lr=0.001)
    train_X = torch.Tensor(np.array([i[0] for i in training_data])).view(-1, 1, 604, 604)
    train_X /= 255.0
    train_y = torch.Tensor(np.array([i[1] for i in training_data]))
    BATCH_SIZE = 25
    EPOCHS = 3
    for epoch in range(EPOCHS):
        for i in tqdm(range(0, len(train_X), BATCH_SIZE)):
            batch_X = train_X[i:i + BATCH_SIZE].view(-1, 1, 604, 604)
            batch_y = train_y[i:i + BATCH_SIZE]
            net.zero_grad()
            outputs = net(batch_X)
            outputs = F.softmax(outputs, dim=1)
            loss = F.binary_cross_entropy(outputs, batch_y)
            loss.backward()
            optimizer.step()
        log.info(f"Epoch: {epoch}. Loss: {loss}")

    correct = 0
    total = 0
    log.info("Testing")
