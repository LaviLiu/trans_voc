import cv2
from PIL import Image
imgName = "202017000300_R_2018_05_17_11_37_26_left_000262.jpg"
txtName = "202017000300_R_2018_05_17_11_37_26_left_000262.txt" #txt的ground truth形式：x,y,h,w

image = cv2.imread(imgName)
im = Image.open(imgName)
width, height = im.size
print(width,height)
print(image.shape)
with open(txtName,'r') as f:
    gt = f.read().splitlines()
    for boxes in gt:
        boxes = boxes.split(" ")
        #cv2.rectangle(image,(int(boxes[0]),int(boxes[1])),(int(boxes[0])+int(boxes[3]),int(boxes[1])+int(boxes[2])),(255,0,0),1)
        cv2.rectangle(image, (int(boxes[0]), int(boxes[1])),(int(boxes[0]) + int(boxes[3]), int(boxes[1]) + int(boxes[2])), (255, 0, 0), 1)
cv2.imshow("image",image)
cv2.waitKey(0)