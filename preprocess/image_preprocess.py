import numpy as np
import sys
import dlib
import cv2
from os.path import join, basename, splitext

import constants 

__face_detector = dlib.get_frontal_face_detector()
__face_pose_predictor = dlib.shape_predictor(constants.PREDICTOR_MODEL)


def __get_landmarks(image, face_rect):
	pose_landmarks = __face_pose_predictor(image, face_rect)
	return list(map(lambda p: (p.x, p.y), pose_landmarks.parts()))	
	

def __align(image, landmarks, landmarkIndices, output_dimension):
	npLandmarks = np.float32(landmarks)
	npLandmarkIndices = np.array(landmarkIndices)

	H = cv2.getAffineTransform(npLandmarks[npLandmarkIndices], output_dimension * constants.MINMAX_TEMPLATE[npLandmarkIndices])
	alignedImage = cv2.warpAffine(image, H, (output_dimension, output_dimension))

	return alignedImage


def get_faces(image_path, output_dimension=128, landmarkIndices=constants.OUTER_EYES_AND_NOSE):
	image = cv2.imread(image_path)

	detected_faces = __face_detector(image, 1)
	#print("detected faces", len(detected_faces))
	
	images = []
	for i, face_rect in enumerate(detected_faces):
		landmarks = __get_landmarks(image, face_rect)
		alignedFace = __align(image, landmarks, landmarkIndices, output_dimension)
				
		images.append(alignedFace)

	return images


def save_faces(image_path, output_folder, output_dimension=128, landmarkIndices=constants.OUTER_EYES_AND_NOSE):
	images = get_faces(image_path, output_dimension, landmarkIndices)
	
	image_paths = []
	for i, image in enumerate(images):
		base, extension = splitext(basename(image_path))
		new_image_name = "{}_{}{}".format(base, i, extension)
		new_image_path = join(output_folder, new_image_name)
		cv2.imwrite(new_image_path, image) 
		
		image_paths.append(new_image_path)

	return image_paths
