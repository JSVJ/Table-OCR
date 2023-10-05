# Essentials
from PIL import Image
import cv2
import pytesseract
from matplotlib import pyplot as plt
import numpy as np

# Initializing the variables
IMAGE_ADDRESS = 'samples//sample.png'

# Get the image
# im_file = IMAGE_ADDRESS
# im = Image.open(im_file)
# im.show()
image = cv2.imread(IMAGE_ADDRESS)

# Get the coordinates of the image
'''
For now we can select manually, later we can replace it
'''

ROIS = cv2.selectROI(windowName = "Please select the 3rd and 4th rows", img = image)
# print(ROIS)
top_x, top_y, width, height = int(ROIS[0]), int(ROIS[1]), int(ROIS[2]), int(ROIS[3])
bottom_x = width + top_x
bottom_y = height + top_y
top_left = (top_x, top_y)
bottom_right = (bottom_x, bottom_y)

# Crop the image
# for reference and to check whether the ROIs are properly aligned or not.
# bounding_box_image = cv2.rectangle(img = image, pt1 = top_left, pt2 = bottom_right, color = (0, 0, 255), thickness = 2)
# cv2.imshow(winname = 'selected ROI image',mat = bounding_box_image)
cropped_image = image[top_y : bottom_y, top_x : bottom_x]
# cv2.imshow(winname = 'cropped image', mat = cropped_image)

# Preprocess the image
'''
1. making the image to white background with black text.
2. using a kernel and erosion facility, thining the text thickness (for this case, we use the minimum thickness possible)
'''
inverted_image = cv2.bitwise_not(cropped_image)
_, im_bw = cv2.threshold(inverted_image, 120, 255, cv2.THRESH_BINARY)
kernel = np.ones((1, 1), np.uint8)
# dilated_image = cv2.dilate(im_bw, kernel, iterations = 1)
# kernel = np.ones((1, 1), np.uint8)
# eroded_image = cv2.erode(dilated_image, kernel, iterations = 1)
# morphed_image = cv2.morphologyEx(eroded_image, cv2.MORPH_CLOSE, kernel)

preprocessed_image = im_bw

cv2.imshow(winname = "preprocessed image", mat = preprocessed_image)

# Detect the characters from the image
config = '--oem 1 --psm 6'
ocr_result = pytesseract.image_to_string(preprocessed_image, config = config)
print(ocr_result)
print('OCR Detection is DONE')

# Save the detected data in a csv
print(type(ocr_result))
file = open('temp/test.txt', 'w')
n = file.write(ocr_result)
file.close()




cv2.waitKey(0) 
cv2.destroyAllWindows()