import os
import argparse
import glob

def main(args):
    imgs_dir = args.path

    index = 1
    for filepath in glob.glob(os.path.join(imgs_dir, "*.bmp")):
        # filename = os.path.basename(filepath)
        dirname = os.path.dirname(filepath)
        os.rename(filepath, os.path.join(dirname, f"cb_{index}.bmp"))
        index += 1
    
        

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--path", required=True, help="frame_path")
    args = parser.parse_args()
    main(args)