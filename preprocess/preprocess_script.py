import sys

if "help" in sys.argv or len(sys.argv) < 3:
	print("<======================>USAGE<=========================================>")
	print("\n"+'\033[93m'+"USAGE"+'\033[0m'+": 'python3 {} origin_folder destination_folder'".format(sys.argv[0]))
	print("origin_folder: path to folder where are all images that need to be preprocessed")
	print("destination_folder: path to folder where will preprocess results be stored")
	
	print("\n"+'\033[96m'+"Note"+'\033[0m'+": preprocess results are scaled images of faces in image.")
	print("New images are saved as '{original_name}_{index}.jpg'")
	print("where {original_name} stands for original name of the image and")
	print("{index} stands for face index.")
	print("<=====================================================================>")
	exit()


import image_preprocess

import glob
import os
from os.path import join, relpath, dirname

origin_folder = sys.argv[1]
destination_folder = sys.argv[2]


files = glob.glob(origin_folder+"/**/*.jpg", recursive=True)
#print(files)

for f in files:
	#output_folder = destination_folder + "/" + f[len(origin_folder)+1:f.rfind("/")+1]
	output_folder = join(destination_folder, dirname(relpath(f, origin_folder))) 
	
	#print("folder:", output_folder)
	if not os.path.exists(output_folder):
	    	os.makedirs(output_folder)
	
	result = image_preprocess.save_faces(f, output_folder)
	#print("result:", result)
	
