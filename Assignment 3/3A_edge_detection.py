# Import all the necessary packages
import os
import sys
import argparse
import cv2
import numpy as np
from pathlib import Path
sys.path.append(os.path.join(".."))
from utils import jimshow
from utils import jimshow_channel


def main():
    # initialize argument parser
    ap = argparse.ArgumentParser(description="Outline every letter in the image by performing edge detection")
    ap.add_argument('-p', '--path', default= Path('../visual_data/A3_target_image.jpg'), type = Path, help="Path to the data")
    args = ap.parse_args()
    
    # define the path to the image
    text_image = os.path.join("..", "visual_data", "A3_target_image.jpg")
    truths = cv2.imread(text_image)

    # See what the dimensions of the image are
    truths.shape

    # Draw a rectangle around the text of the image 
    truths_ROI = cv2.rectangle(truths, (1300, 830), (2930, 2850), (0, 255, 0), 3)

    # Crop the image to include only the area marked by the rectangle using slicing 
    crop_ROI = truths_ROI[830:2850, 1300:2930]

    # Make an outpath to where I save the image to
    outpath = os.path.join("..", "visual_data", "A3_output", "image_cropped.jpg")

    # Save the image to this path
    save_cropped = cv2.imwrite(outpath, crop_ROI)

    # Define the path to the cropped image
    crop_path = os.path.join("..", "visual_data", "A3_output", "image_cropped.jpg")

    # Load image
    cropped_truths = cv2.imread(crop_path)

    # First the image is blurred using Gaussian blur
    blurred = cv2.GaussianBlur(cropped_truths, (5,5), 0)

    # Create the canny object to perform canny edge detection on the image
    canny = cv2.Canny(blurred, 30, 150)

    # Let's see what the image looks like after the canny edge detection has been performed
    jimshow_channel(canny)

    # Now, we're interested in the external contour of the objects in the image
    # So we filter out any inner structures from the outer edge of the whole object
    # the function findContours() is used on a copy of the cropped image, so we don't modify it in place
    (contours, _) = cv2.findContours(canny.copy(),
                     cv2.RETR_EXTERNAL,
                     cv2.CHAIN_APPROX_SIMPLE)

    # Lastly, after defining the external contours we want to draw green contour lines
    letters_image = cv2.drawContours(cropped_truths, # draw contours on copy of original image
                             contours, # our list of contours
                             -1, # which contours to draw (on all the letters)
                             (0,255,0), # contour color green
                             1) # contour pixel width

    # How many letters are in the image?
    print(f"The text in the image consists of {len(contours)} letters!")

    # Make outpath to the image
    outpath2 = os.path.join("..", "visual_data", "A3_output", "A3_final_image.jpg")

    # Save this image
    cv2.imwrite(outpath2, letters_image)
    
    print("Done, the cropped image with the edges can be found in '../visual_data/A3_output'")

if __name__ == '__main__':
    main()