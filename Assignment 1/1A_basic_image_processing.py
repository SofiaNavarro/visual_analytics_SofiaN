# Load necessary libraries
import os
import argparse
import numpy as np
import sys
import cv2
from utils import jimshow
from pathlib import Path
sys.path.append(os.path.join(".."))

def main():
    # initialize argument parser
    ap = argparse.ArgumentParser(description="Slice images into 4 equal pieces")
    ap.add_argument('-p', '--path', default= Path('../visual_data/A1_images'), type = Path, help="Path to the data")
    args = ap.parse_args()

    dir_image = args.path
    #os.path.join("..", "visual_data", "assOne_images") # point to the directory where the original images reside
    info_images = os.path.join("..", "visual_data", "A1_output", "image_shape.csv") # make a csv file for the metadata info on images
    outpath = os.path.join("..", "visual_data", "A1_output") # Outpath where the sliced images are stored

    # Write titles for the csv files
    titles =  " ".join(["filename", "heigth", "width", "channels"])

    # Save titles in the info_images file
    with open(info_images, "w", encoding="utf-8") as file:
            file.write(titles + "\n")


    for image in Path(dir_image).glob("*.JPG"): # Run through every image in the image_path directory
        image_open = cv2.imread(str(image)) # Read all images in the folder
        height, width, _ = image_open.shape # Define height, width and channels as a dummy variable, since I won't be needing it.
        top_left = image_open[0:height//2, 0:width//2] # Slice images
        top_right = image_open[0:height//2, width//2:width] # Slice images
        bottom_left = image_open[height//2:height, 0:width//2] # Slice images
        bottom_right = image_open[height//2:height, width//2:width] # Slice images


        path, filename = os.path.split(image) # Split path into path and filename
        basename, extension = os.path.splitext(filename) # Further split the filename into a basename and .JPG
        outpath_tl = os.path.join(outpath, basename + "_Top_left" + extension) # Make filename for split image
        outpath_tr = os.path.join(outpath, basename + "_Top_right" + extension) # Make filename for split image
        outpath_bl = os.path.join(outpath, basename + "_Bottom_left" + extension) # Make filename for split image
        outpath_br = os.path.join(outpath, basename + "_Bottom_right" + extension) # Make filename for split image

        # Save the four equal sized slices of the images
        cv2.imwrite(outpath_tl, top_left)
        cv2.imwrite(outpath_tr, top_right)
        cv2.imwrite(outpath_bl, bottom_left)
        cv2.imwrite(outpath_br, bottom_right)

        # Make a list of all the filenames 
        # with the height, width and number of channels included
        # and save it in the csv file made earlier:
        info = [(basename + "_Top_left" + extension + " " + str(height//2) + " " + str(width//2) + " " + str(_) + "\n"),
                (basename + "_Top_right" + extension + " " + str(height//2) + " " + str(width//2) + " " + str(_) + "\n"),
                (basename + "_Bottom_left" + extension + " " + str(height//2) + " " + str(width//2) + " " + str(_) + "\n"),
                (basename + "_Bottom_right" + extension + " " + str(height//2) + " " + str(width//2) + " " + str(_) + "\n")]
        save_info = "".join(info)

        with open(info_images, "a", encoding= "utf-8") as file:
            file.write(save_info + "\n")
    
    print("Done, all the sliced images as well as the csv file containing the image shapes are saved in '../visual_data/A1_output'")

if __name__ == '__main__':
    main()