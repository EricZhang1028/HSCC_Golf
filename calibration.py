import argparse
import cv2
import glob
import os

import numpy as np

OUTPUT_DIR = "data/cali_out"
# 11 x 7 ->　70mm
def make_parser():
    parser = argparse.ArgumentParser("Calibration")
    parser.add_argument("-r", "--rows", default=12, type=int, help="#rows of chessboard")
    parser.add_argument("-c", "--cols", default=8, type=int, help="#cols of chessboard")
    parser.add_argument("-m", "--mm", default=90, type=int, help="width per block using mm")
    parser.add_argument("-p", "--path", default="data/sample", help="images path")
    parser.add_argument("-s", "--show", default=False, type=bool, help="show camlibarte image")
    parser.add_argument("-w", default=False, type=bool, help="Is windows?")

    return parser

def main(args):
    rows, cols, mm = args.rows, args.cols, args.mm
    criteria = (cv2.TERM_CRITERIA_MAX_ITER + cv2.TERM_CRITERIA_EPS, 30, 0.001)
    objectPoints = np.zeros((rows * cols, 3), np.float32)
    objectPoints[:, :2] = np.mgrid[0:rows*mm:mm, 0:cols*mm:mm].T.reshape(-1, 2)

    objectPointsArray = []
    imgPointsArray = []

    files_path = sorted(glob.glob(os.path.join(args.path, "*")))
    img_dict = {}

    for path in files_path:
        img = cv2.imread(path)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Find the chess board corners
        ret, corners = cv2.findChessboardCorners(gray, (rows, cols), None)    

        if ret:
            # Refine the corner position
            corners = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)

            objectPointsArray.append(objectPoints)
            imgPointsArray.append(corners)
            img_dict[path.split('/')[-1]] = len(objectPointsArray)-1

            cv2.drawChessboardCorners(img, (rows, cols), corners, ret)
        else:
            print(f"image {path} can't be calibrated.")
        
        if args.show:
            cv2.imshow("chess board", img)
            cv2.waitKey(10000)

    # Calibrate the camera and save the results
    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objectPointsArray, imgPointsArray, gray.shape[::-1], None, None)

    # Print the camera calibration error
    error = 0
    for i in range(len(objectPointsArray)):
        imgPoints, _ = cv2.projectPoints(objectPointsArray[i], rvecs[i], tvecs[i], mtx, dist)
        error += cv2.norm(imgPointsArray[i], imgPoints, cv2.NORM_L2) / len(imgPoints)
    print("Re-projection error: ", error / len(objectPointsArray))

    # save calibration result
    # output_file = args.path.split('/')[-1] + ".npz"
    head_tail = os.path.split(args.path)
    output_dir = "/".join(head_tail[0].split("/")[:-1])
    output_path = os.path.join(output_dir, "cali_out.npz")
    np.savez(output_path, mtx=mtx, dist=dist, rvecs=rvecs, tvecs=tvecs, error=(error / len(objectPointsArray)), img_dict=np.array(list(img_dict.items())))
    print(f"Calibration result saved in {output_path}")

    if args.show:
        # Load one of the test images
        last_file = files_path[-1]
        img = cv2.imread(last_file)
        h, w = img.shape[:2]

        # Obtain the new camera matrix and undistort the image
        newCameraMtx, roi = cv2.getOptimalNewCameraMatrix(mtx, dist, (w, h), 1, (w, h))
        undistortedImg = cv2.undistort(img, mtx, dist, None, newCameraMtx)

        # Crop the undistorted image
        # x, y, w, h = roi
        # undistortedImg = undistortedImg[y:y + h, x:x + w]

        # Display the final result
        cv2.imshow("undistorted chess board", np.hstack((img, undistortedImg)))
        cv2.waitKey(0)
        cv2.destroyAllWindows()

if __name__ == '__main__':
    args = make_parser().parse_args()
    main(args)