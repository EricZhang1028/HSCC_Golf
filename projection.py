import argparse
import numpy as np
import cv2
import os

def make_parser():
    parser = argparse.ArgumentParser("Projection")
    parser.add_argument("-p", "--image_path", required=True, type=str, help="image path")
    parser.add_argument("-n", "--npz_path", required=True, type=str, help="npz path")
    parser.add_argument("-s", "--show", default=False, type=str, help="show image")
    
    return parser

def main(args):
    if not os.path.exists(args.image_path): 
        print(f"image {args.image_path} not exists")
        return

    if not os.path.exists(args.npz_path):
        print(f"npz file {args.npz_path} not exists")
        return

    img_name = args.image_path.split("/")[-1]
    cali_info = np.load(args.npz_path)
    print(dict(cali_info["img_dict"]))
    print(img_name)
    img_index = int(dict(cali_info["img_dict"])[img_name])
    rvecs, tvecs, mtx, dist = cali_info["rvecs"], cali_info["tvecs"], cali_info["mtx"], cali_info["dist"]    

    while True:
        inp = input().strip()
        if inp == "q": break
        
        coordinates = [float(i) for i in inp.split()]
        imgPoint, _ = cv2.projectPoints(np.array(coordinates), rvecs[img_index], tvecs[img_index], mtx, dist)
        center_coordinates = (round(imgPoint[0][0][0]), round(imgPoint[0][0][1]))
        print(center_coordinates)
        
        img = cv2.imread(args.image_path)
        radius, color, thickness = 20, (255, 0, 0), 2
        img = cv2.circle(img, center_coordinates, radius, color, thickness)

        if args.show:
            cv2.imshow("imgPoint", img)
            cv2.waitKey(5000)
        else:
            cv2.imwrite("output.jpg", img)

if __name__ == '__main__':
    args = make_parser().parse_args()
    main(args)