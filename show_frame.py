import argparse
from ast import parse
import cv2


def main(args):
    video_path, skip_frame = args.path, int(args.skip)
    cap = cv2.VideoCapture(video_path)

    frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT)
    width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    fps = cap.get(cv2.CAP_PROP_FPS)

    print(f"Frame count: {frame_count}")
    print(f"Resolution: {width} x {height}")
    print(f"FPS: {fps}")

    font = cv2.FONT_HERSHEY_SIMPLEX
    color = (255, 0, 0)
    fontScale = 1
    thickness = 2

    cnt = 0
    if skip_frame != 0:
        while cap.isOpened():
            cnt += 1
            ret, frame = cap.read()
            if not ret:
                print("Can't receive frame (stream end?). Exiting...")
                break
            if cnt == skip_frame: break

    frame_no = cnt + 1
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print("Can't receive frame (stream end?). Exiting...")
            break
        img = cv2.resize(frame, (int(width * 0.6), int(height * 0.6)))
        img = cv2.putText(img, f"{width} x {height}", (10, 30), font, fontScale, color, thickness, cv2.LINE_AA)
        img = cv2.putText(img, "FPS:" + str(fps), (10, 70), font, fontScale, color, thickness, cv2.LINE_AA)
        img = cv2.putText(img, "Frame no.: " + str(frame_no), (10, 105), font, fontScale, color, thickness, cv2.LINE_AA)
        cv2.imshow("frame", img)
        key = cv2.waitKey(0)

        # if frame_no == 503:
        #     cv2.imwrite("brightness.jpg", frame)
        if key == ord('q'):
            break
        frame_no += 1

    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--path", required=True, help="video path")
    parser.add_argument("-s", "--skip", required=False, type=int ,help="#skip frame", default=0)
    args = parser.parse_args()
    main(args)