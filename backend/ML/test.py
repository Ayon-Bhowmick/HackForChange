from plants import run
import os
import cv2

PATH = "./plants/dataset-user_images"

if __name__ == "__main__":
    for f in os.listdir(PATH):
        try:
            img = cv2.imread(os.path.join(PATH, f), cv2.IMREAD_GRAYSCALE)
        except Exception as e:
            print(e)
        print(run(img))
