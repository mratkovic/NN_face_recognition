import sys
import time
import image_preprocess
import glob
import os
from os.path import join, relpath, dirname


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



origin_folder = sys.argv[1]
destination_folder = sys.argv[2]


files = sorted(glob.glob(origin_folder+"/**/*.jpg", recursive=True))
size = len(files)
print('Total: ', size)


batch_start_time = start_time = time.time()
for i, f in enumerate(files):

	if i%250 == 0: 
		current = time.time()
		batch_time = current - batch_start_time
		elapsed = current - start_time

		print('\n\nProgress: {}/{}; batch_time: {}; total_time: {}\n'.format(i, size, batch_time, elapsed))
		batch_start_time = time.time()


	output_folder = join(destination_folder, dirname(relpath(f, origin_folder))) 
	if not os.path.exists(output_folder):
	    	os.makedirs(output_folder)
	print("{}/{}\t{}".format(i, size, f))
	result = image_preprocess.save_faces(f, output_folder)
	


print("Completed...")
print("Total time: {}".format(time.time() - start_time))