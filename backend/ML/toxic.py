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
                        self.data.append([img, np.eye(2)[self.LABELS[label]]])
                        if label == self.TOXIC:
                            self.toxic_count += 1
                        else:
                            self.nontoxic_count += 1
                    except Exception as e:
                        self.log.error(e)
        np.random.shuffle(self.data)
        np.save("toxic_data.npy", self.data)
        self.log.info(f"Toxic: {self.toxic_count}   Non-Toxic: {self.nontoxic_count}")

class Net(nn.Module):
    def __init__(self):
        super.__init__()
        super.conv1 = nn.Conv2d(1, 32, 5)
        super.conv2 = nn.Conv2d(32, 64, 5)
        super.conv3 = nn.Conv2d(64, 128, 5)
        super.conv4 = nn.Conv2d(128, 256, 5)
        super.conv5 = nn.Conv2d(256, 512, 5)
        super.fc1 = nn.Linear(512*5*5, 1024)
        super.fc2 = nn.Linear(1024, 512)
        super.fc3 = nn.Linear(512, 2)

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
    data = np.load("toxic_data.npy", allow_pickle=True)
    net = Net()
    optimizer = optim.Adam(net.parameters(), lr=0.001)
    
