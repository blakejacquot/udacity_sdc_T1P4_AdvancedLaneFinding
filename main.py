"""
    Docstring
"""

# Import standard libraries
import glob
import os
import numpy as np
#import matplotlib.pyplot as plt
#import matplotlib.image as mpimg
#import math
import pickle
#from scipy.signal import find_peaks_cwt

#Import non-standard libraries
import cv2


def compute_camera_cal(dir_cal_images):
    """Compute distortion parameters for chessboard jpg's in a directory

    Args:
        dir_cal_images: Directory of calibration chessboard images

    Returns:
        objpoints: List of 3d points in real world space.
        imgpoints: List of 2d points in image plane.

    """
    print('Computing camera calibration matrices')
    # prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
    num_x = 9 # Number of inside corners in x-direction
    num_y = 6 # Number of inside corners in y-direction
    objp = np.zeros((num_y*num_x, 3), np.float32)
    objp[:, :2] = np.mgrid[0:num_x, 0:num_y].T.reshape(-1, 2)

    # Arrays to store object points and image points from all the images.
    objpoints = [] # 3d points in real world space
    imgpoints = [] # 2d points in image plane.

    # Make a list of calibration images
    search_phrase = os.path.join('.', dir_cal_images, 'calibration*.jpg')
    images = glob.glob(search_phrase)

    # Step through the list and search for chessboard corners
    for fname in images:
        print('Processing ', fname)
        img = cv2.imread(fname)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Find the chessboard corners
        ret, corners = cv2.findChessboardCorners(gray, (num_x, num_y), None)

        # If found, add object points, image points
        if ret:
            objpoints.append(objp)
            imgpoints.append(corners)

            # Draw and display the corners
            img = cv2.drawChessboardCorners(img, (num_x, num_y), corners, ret)
            cv2.imshow('img', img)
            cv2.waitKey(500)
    cv2.destroyAllWindows()
    return objpoints, imgpoints

def undistort_image(objpoints, imgpoints, img):
    """Undistort an image with calibration parameters

    Args:
        objpoints: List of 3d points in real world space.
        imgpoints: List of 2d points in image plane.
        img: 2D image.

    Returns:
        undistorted_img:
    """
    print(img.shape)
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints,
        gray.shape[::-1], None, None)
    undistorted_img = cv2.undistort(img, mtx, dist, None, mtx)
    return undistorted_img

def make_binary_image():
    """
    Docstring
    """
    pass

def mark_lane_pixels():
    """
    Docstring
    """
    pass

def calc_lane_curvature():
    """
    Docstring
    """
    pass

def warp_lanes_to_origimage():
    """
    Docstring
    """
    pass

def write_annotated_image():
    """
    Docstring
    """
    pass

def proc_pipeline(objpoints, imgpoints, img):
    """ Process an image pipline on an image

    Args:
        objpoints:
        imgpoints:
        images:

    Returns:



    Compute the camera calibration matrix and distortion coefficients given a set of
    chessboard images.

    Apply a distortion correction to raw images.

    Use color transforms, gradients, etc., to create a thresholded binary image.

    Apply a perspective transform to rectify binary image ("birds-eye view").

    Detect lane pixels and fit to find the lane boundary.

    Determine the curvature of the lane and vehicle position with respect to center.

    Warp the detected lane boundaries back onto the original image.

    Output visual display of the lane boundaries and numerical estimation of lane
    curvature and vehicle position.
    """
    #print(objpoints, imgpoints)
    #print(type(objpoints), type(imgpoints))

    undistorted_img = undistort_image(objpoints, imgpoints, img)

    make_binary_image()
    mark_lane_pixels()
    calc_lane_curvature()
    warp_lanes_to_origimage()
    write_annotated_image()
    return undistorted_img



def main():
    """
    Docstring
    """
    dir_cal_images = os.path.join('.', 'camera_cal')
    dir_test_images = os.path.join('test_images')
    dir_output_images = os.path.join('output_images')

    proc_distortion_data = 0
    proc_pipeline_cal_images = 1
    proc_pipeline_test_images = 0
    proc_pipeline_target_images = 0

    if proc_distortion_data == 1:
        objpoints, imgpoints = compute_camera_cal(dir_cal_images)
        pickle_data = {}
        pickle_data["objpoints"] = objpoints
        pickle_data["imgpoints"] = imgpoints
        pickle.dump( pickle_data, open("calibration_data.p", "wb" ))


    pickle_data = pickle.load(open("calibration_data.p","rb"))
    objpoints = pickle_data["objpoints"]
    imgpoints = pickle_data["imgpoints"]



    if proc_pipeline_cal_images == 1:
        search_phrase = os.path.join(dir_cal_images, '*.jpg')
        images = glob.glob(search_phrase)
        for fname in images:
            print('Processing ', fname)
            img = cv2.imread(fname)
            ret_img = proc_pipeline(objpoints, imgpoints, img)
            curr_name = fname[-10:-4]
            out_path = os.path.join(dir_output_images, curr_name + '.jpg')
            cv2.imwrite(out_path, ret_img)




    if proc_pipeline_test_images == 1:
        search_phrase = os.path.join(dir_test_images, '*.jpg')
        images_test = glob.glob(search_phrase)
        proc_pipeline(objpoints, imgpoints, images_test)


    if proc_pipeline_target_images == 0:
        print(dir_output_images)


if __name__ == "__main__":
    main()