import pytesseract
import cv2

image = cv2.imread("Test Images//3.png")
img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
hImg, wImg, c = img.shape
boxes = pytesseract.image_to_data(img)
bounding_boxes = []
for x,b in enumerate(boxes.splitlines()):
    if x!=0:
        b = b.split()
        if len(b) == 12 and b[-1] != "-1":
            print(b)
            x,y,w,h = int(b[6]),int(b[7]),int(b[8]),int(b[9])
            cv2.rectangle(img,(x,y),(w+x,h+y),(0,0,255),2)
            bounding_boxes.append([x,y,w,h])

cv2.imshow("Result",img)
cv2.waitKey(0)





