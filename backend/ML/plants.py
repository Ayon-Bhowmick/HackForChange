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
import sklearn.metrics
import matplotlib.pyplot as plt

BUILD_DATA = False
TRAIN = True

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
        self.log = logging.getLogger("info")
        self.conv1 = nn.Conv2d(1, 32, 5)
        self.conv2 = nn.Conv2d(32, 64, 5)
        self.conv3 = nn.Conv2d(64, 128, 5)
        self.conv4 = nn.Conv2d(128, 256, 5)
        self.conv5 = nn.Conv2d(256, 512, 5)
        self.fc1 = nn.Linear(512 * 5 * 5, 1024)
        self.dropout = nn.Dropout(0.5)
        self.fc2 = nn.Linear(1024, 1024)
        # self.fc3 = nn.Linear(1024, 1024)
        self.fc4 = nn.Linear(1024, 512)
        self.fc5 = nn.Linear(512, 62)

    def convs(self, x):
        x = F.relu(self.conv1(x))
        x = F.max_pool2d(F.relu(self.conv2(x)), (3, 3))
        x = F.max_pool2d(F.relu(self.conv3(x)), (3, 3))
        x = F.max_pool2d(F.relu(self.conv4(x)), (3, 3))
        x = F.max_pool2d(F.relu(self.conv5(x)), (3, 3))
        x = x.view(-1, 512 * 5 * 5)
        return x

    def forward(self, x):
        x = self.convs(x)
        x = F.relu(self.fc1(x))
        x = self.dropout(x)
        x = F.relu(self.fc2(x))
        # x = F.relu(self.fc3(x))
        x = F.relu(self.fc4(x))
        x = self.fc5(x)
        return x

def run(img) -> "set[bool, str]":
    img = cv2.resize(img, (604, 604))
    img = cv2.copyMakeBorder(img, 2, 2, 2, 2, cv2.BORDER_CONSTANT, value=0)
    img = torch.Tensor(img).view(-1, 1, 604, 604)
    img /= 255.0
    model = AyonNet()
    model.load_state_dict(torch.load("plant.pt"))
    model.eval()
    with torch.no_grad():
        output = model(img)
        pred = F.softmax(output, dim=1)
        confidence, classes = torch.max(pred, 1)
        plant = class_map[classes.item()]
        return (confidence.item() > 0.9, plant)


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
    model = AyonNet().cuda()
    if TRAIN:
        log.info("Training model")
        optimizer = optim.Adam(model.parameters(), lr=0.001)
        train_X = torch.Tensor(np.array([i[0] for i in training_data])).view(-1, 1, 604, 604)
        train_X /= 255.0
        train_y = torch.Tensor(np.array([i[1] for i in training_data]))
        BATCH_SIZE = 10
        EPOCHS = 3
        for epoch in range(EPOCHS):
            for i in tqdm(range(0, len(train_X), BATCH_SIZE)):
                batch_X = train_X[i:i + BATCH_SIZE].view(-1, 1, 604, 604).cuda()
                batch_y = train_y[i:i + BATCH_SIZE].cuda()
                model.zero_grad()
                outputs = model(batch_X)
                outputs = F.softmax(outputs, dim=1)
                loss = nn.NLLLoss()
                l = loss(outputs, torch.argmax(batch_y, 1))
                l.backward()
                optimizer.step()
            log.info(f"Epoch: {epoch}. Loss: {l}")
        torch.save(model.state_dict(), "plant.pt")
    else:
        model.load_state_dict(torch.load("plant.pt"))


    log.info("testing")
    test_X = torch.Tensor(np.array([i[0] for i in testing_data])).view(-1, 1, 604, 604)
    test_y = torch.Tensor(np.array([i[1] for i in testing_data]))
    true = []
    pred = []
    model.eval()
    with torch.no_grad():
        for i in tqdm(range(len(test_X))):
            real = torch.argmax(test_y[i])
            net_out = model(test_X[i].view(-1, 1, 604, 604).cuda())[0]
            print(test_X[i])
            print("net_out", net_out)
            predict = torch.softmax(net_out, dim=0)
            print(real, torch.argmax(predict))
            true.append(real)
            pred.append(predict)
        log.info(sklearn.metrics.classification_report(true, pred, target_names=list(class_map.values())))
        # save confusion matrix
        cm = sklearn.metrics.confusion_matrix(true, pred)
        fig = plt.figure()
        ax = fig.add_subplot(111)
        cax = ax.matshow(cm)
        plt.title("Confusion matrix of the classifier")
        fig.colorbar(cax)
        ax.set_xticklabels([""] + list(class_map.values()))
        ax.set_yticklabels([""] + list(class_map.values()))
        plt.xlabel("Predicted")
        plt.ylabel("True")
        plt.savefig("confusion_matrix.png")
    # log.info(f"Accuracy: {round(correct/total, 3)}")
    model.train()
