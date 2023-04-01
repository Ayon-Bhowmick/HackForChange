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

BUILD_DATA = False
LOAD_MODEL = False
USE_MODEL = True

class ToxicDataMaker():
    log = logging.getLogger("info")
    TOXIC = "./tpc-imgs/toxic_images"
    NONTOXIC = "./tpc-imgs/nontoxic_images"
    LABELS = {TOXIC: 1, NONTOXIC: 0}
    data = []
    toxic_count = 0
    nontoxic_count = 0

    def make_training_data(self):
        pad = nn.ZeroPad2d(2)
        for label in self.LABELS:
            self.log.info(label)
            for dir in os.listdir(label):
                for file in tqdm(os.listdir(os.path.join(label, dir))):
                    try:
                        path = os.path.join(label, dir, file)
                        img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
                        img = cv2.resize(img, (300, 300))
                        img = torch.from_numpy(np.array(img))
                        img = pad(img)
                        self.data.append([np.array(img), np.eye(2)[self.LABELS[label]]])
                        if label == self.TOXIC:
                            self.toxic_count += 1
                        else:
                            self.nontoxic_count += 1
                    except Exception as e:
                        self.log.error(e)
        np.random.shuffle(self.data)
        np.save("toxic_data.npy", self.data)
        self.log.info(f"Toxic: {self.toxic_count}   Non-Toxic: {self.nontoxic_count}")

class AyonNet(nn.Module):
    def __init__(self):
        super().__init__()
        self.conv1 = nn.Conv2d(1, 32, 5)
        self.conv2 = nn.Conv2d(32, 64, 5)
        self.conv3 = nn.Conv2d(64, 128, 5)
        self.conv4 = nn.Conv2d(128, 256, 5)
        self.conv5 = nn.Conv2d(256, 512, 5)
        self.fc1 = nn.Linear(512*5*5, 1024)
        self.fc2 = nn.Linear(1024, 512)
        self.fc3 = nn.Linear(512, 2)

    def forward(self, x):
        x = F.max_pool2d(F.relu(self.conv1(x)), (2, 2))
        x = F.max_pool2d(F.relu(self.conv2(x)), (2, 2))
        x = F.max_pool2d(F.relu(self.conv3(x)), (2, 2))
        x = F.max_pool2d(F.relu(self.conv4(x)), (2, 2))
        x = F.max_pool2d(F.relu(self.conv5(x)), (2, 2))
        x = x.view(-1, 512*5*5)
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = self.fc3(x)
        return F.softmax(x, dim=1)


if __name__ == "__main__":
    logging.basicConfig(stream=sys.stdout)
    logging.getLogger("info").setLevel(logging.INFO)
    toxic = ToxicDataMaker()
    if BUILD_DATA:
        toxic.make_training_data()
    log = logging.getLogger("info")
    data = np.load("toxic_data.npy", allow_pickle=True)
    net = AyonNet()
    optimizer = optim.Adam(net.parameters(), lr=0.001)
    X = torch.Tensor(np.array([i[0] for i in data])).view(-1, 304, 304)
    X = X/255.0
    y = torch.Tensor(np.array([i[1] for i in data]))
    val_size = int(len(X) * 0.1)
    train_X = X[:-val_size]
    train_y = y[:-val_size]
    test_X = X[-val_size:]
    test_y = y[-val_size:]
    # logging.info(train_X.shape, train_y.shape, test_X.shape, test_y.shape)
    BATCH_SIZE = 50
    EPOCHS = 3
    log.info("Starting training")
    for epoch in range(EPOCHS):
        for i in tqdm(range(0, len(train_X), BATCH_SIZE)):
            batch_X = train_X[i:i+BATCH_SIZE].view(-1, 1, 304, 304)
            batch_y = train_y[i:i+BATCH_SIZE]
            net.zero_grad()
            outputs = net(batch_X)
            loss = nn.MSELoss()
            l = loss(outputs, batch_y)
            l.backward()
            optimizer.step()
        logging.info(f"Epoch: {epoch}. Loss: {loss}")

    correct = 0
    total = 0
    log.info("testing")
    with torch.no_grad():
        for i in tqdm(range(len(test_X))):
            real = torch.argmax(test_y[i])
            net_out = net(test_X[i].view(-1, 1, 304, 304))[0]
            predict = torch.argmax(net_out)
            if predict == real:
                correct += 1
            total += 1
    log.info("Accuracy:", round(correct/total, 3))

    if round(correct/total, 3) > 0:
        torch.save(net.state_dict(), "toxic.pt")
