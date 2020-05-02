from PIL import Image
import pytesseract
import numpy as np
import argparse
import cv2, os


parser = argparse.ArgumentParser()
parser.add_argument("-i", "--image", required=True)
parser.add_argument("-p", "--preprocess", type=str, default="thresh")
args = vars(parser.parse_args())


image = cv2.imread(args["image"])
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


if args["preprocess"] == "thresh":
    gray = cv2.threshold(gray, 0, 255,
                         cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

elif args["preprocess"] == "blur":
    gray = cv2.medianBlur(gray, 3)


filename = "{}.png".format(os.getpid())
cv2.imwrite(filename, gray)


text = pytesseract.image_to_string(Image.open(filename))
os.remove(filename)


print(text)

# show the output images
cv2.imshow("Image", image)
cv2.imshow("Output", gray)
cv2.waitKey(0)
cv2.destroyAllWindows()