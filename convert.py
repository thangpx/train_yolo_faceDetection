
from __future__ import print_function

import os
from shutil import copyfile
from PIL import Image

def convert():
    filePath = 'E:/STUDY/DIP/DL/Data/Faces/'
    train_txt = filePath + 'wider_face_split/wider_face_train_bbx_gt.txt'
    src_dir = filePath + 'WIDER_train/images/'
    dst_dir = './data/train_img/'
    yolo_trainFile = open('yolo_train.txt','w+')

    numberOfFile = 0
    with open(train_txt,'r') as fp:
        line = fp.readline()
        nObject = 0
        while line:
            if nObject == 0:
                oStr = fp.readline()
                nObject = int(oStr)
                # Create dependence files
                # -- Remove the new line characters from the string
                line = line.strip('\r\n')
                # -- split the path information
                fname, fextension = os.path.splitext(line)
                # -- remove the '/' character
                fname = fname.split('/').pop()
                # -- read the image information
                width, height = Image.open(src_dir + line).size
                # -- write to the training file
                yolo_trainFile.write('%s\n' % (dst_dir + fname + fextension))
                # -- create text file (annotations file)
                annotations_file = open(dst_dir + fname + '.txt', 'w+')
                # -- copy image file
                copyfile(src_dir + line, dst_dir + fname + fextension)

                numberOfFile += 1
                print('Total file: %d' % numberOfFile, end='\r')

                if nObject == 0:
                    line = fp.readline()
            else:
                # Read the parameters
                line = fp.readline()
                params = line.strip('\r\n').split(' ')
                # Convert the parameters to the range from 0 to 1
                xCenter = (float(params[0]) + float(params[2]) / 2) / width
                yCenter = (float(params[1]) + float(params[3]) / 2) / height
                w = float(params[2]) / width
                h = float(params[3]) / height
                # Write to file
                annotations_file.write('0 %.4f %.4f %.4f %.4f' % (xCenter, yCenter, w, h))
                nObject -= 1
                if nObject != 0:
                    annotations_file.write('\n')
            
            if nObject == 0:
                annotations_file.close()
                line = fp.readline()
    
    fp.close()
    print('Total file: %d' % numberOfFile)


if __name__ == '__main__':
    convert()