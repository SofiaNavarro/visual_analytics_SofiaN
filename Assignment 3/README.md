## Instructions

First you need to build the virtual environment ass3 by running create_visual_venv.sh. You do this by opening a terminal and making sure you have ```cd'ed``` into the 'Assignment 3' folder, then write:
```
./create_visual_venv.sh
```

If this does not work, or you get "permission denied" try:
```
chmod +x create_visual_venv.sh
```
This bash script should now have upgraded to the latest version of pip as well as installed the packages from the requirements.txt. Furhtermore, the bash script also creates a folder in the visual_data folder called A3_output.

Make sure you are still in the 'Assignment 1' folder, and activate the virtual environment by typing:
```
source ass3/bin/activate
```

After activating the virtual environment, run the main script by typing:
```
python 3A_edge_detection.py
```
The script should only take a few seconds to run, and the output can be found in the folder A3_output.
