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

BUILD_DATA = True

class ToxicClassifier():
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




if __name__ == "__main__":
    logging.basicConfig(stream=sys.stdout)
    logging.getLogger("info").setLevel(logging.INFO)
    toxic = ToxicClassifier()
    if BUILD_DATA:
        toxic.make_training_data()
