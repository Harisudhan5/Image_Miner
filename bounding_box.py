import pytesseract
import cv2

image = cv2.imread("Test Images//3.png")
img_RGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
#print(pytesseract.image_to_string(img_RGB))

results = pytesseract.image_to_boxes(img_RGB)
ih, iw, ic = image.shape
for box in results.splitlines():
    box = box.split(' ')
    print(box)
    x, y, w, h = int(box[1]), int(box[2]), int(box[3]), int(box[4])
    cv2.rectangle(image, (x, ih-y), (w, ih-h), (0, 255, 0), 2)
results = pytesseract.image_to_data(img_RGB)

desired_width = 800
desired_height = 600
resized_image = cv2.resize(image, (desired_width, desired_height))
cv2.imshow("Input", resized_image)
cv2.waitKey(0)

