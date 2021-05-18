# System stuff
import os
import sys
import argparse
sys.path.append(os.path.join(".."))
from pathlib import Path

# Image processing
import cv2

def main():
    # initialize argument parser
    ap = argparse.ArgumentParser(description="Calculate distance from target image to flower images")
    ap.add_argument('-p', '--path', default= Path('../visual_data/A2_images'), type = Path, help="Path to the data")
    args = ap.parse_args()

    # Path that points to location of the flower images
    flowers_dir = args.path
    # Path that points to the target image
    target_image = cv2.imread(os.path.join("..", "visual_data", "A2_target_image", "image_0001.jpg"))

    # Create an outpath csv file
    outpath_flowers = os.path.join("..", "visual_data", "A2_output", "distances.csv")


    # Create a histogram for the target image. This object is a numpy.ndarray type
    hist_target = cv2.calcHist([target_image], [0, 1, 2], None, [8, 8, 8], [0,256, 0,256, 0,256])
    # Normalize the target image
    norm_target = cv2.normalize(hist_target, hist_target, 0,255, cv2.NORM_MINMAX)

    # Create titles for the output file
    titles = " ".join(["filename", "distance"])

    with open(outpath_flowers, "w", encoding="utf-8") as file:
        file.write(titles + "\n")

    # Loop over all the images in the flower directory
    for flower in Path(flowers_dir).glob("*.jpg"):
        # Get to each image
        flower_path = Path(str(flower))
        # Load image
        load_flower = cv2.imread(str(flower_path))              
        # Create histogram of each image
        flowers_hist = cv2.calcHist([load_flower], [0,1,2], None, [8,8,8], [0,256, 0,256, 0,256])
        # Normalize each histogram
        norm_flowers = cv2.normalize(flowers_hist, flowers_hist , 0,255, cv2.NORM_MINMAX)
        # Compare histogram of target image, to the histograms of all other images
        # and round the number of decimals to 2.
        hist_comparison = round(cv2.compareHist(norm_target, norm_flowers, cv2.HISTCMP_CHISQR), 2)
        # Append compared histogram to outpath
        image_info = " ".join([str(flower_path), str(hist_comparison)])
        # Save
        with open(outpath_flowers, "a", encoding="utf-8") as file:
            file.write(image_info + "\n")
    print("Done, the distances.csv file is now located in '../visual_data/A2_output'")        
        
if __name__ == '__main__':
    main()