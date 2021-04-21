#!/usr/bin/env python3

import xml.etree.ElementTree as ET
from xml.dom import minidom
from PIL import Image
import os

def createAnnotationPascalVocTree(folder, basename, path, width, height):
    annotation = ET.Element('annotation')
    ET.SubElement(annotation, 'folder').text = folder
    ET.SubElement(annotation, 'filename').text = basename
    ET.SubElement(annotation, 'path').text = path

    source = ET.SubElement(annotation, 'source')
    ET.SubElement(source, 'database').text = 'Unknown'

    size = ET.SubElement(annotation, 'size')
    ET.SubElement(size, 'width').text = width
    ET.SubElement(size, 'height').text = height
    ET.SubElement(size, 'depth').text = '3'

    ET.SubElement(annotation, 'segmented').text = '0'

    return ET.ElementTree(annotation)

def createObjectPascalVocTree(xmin, ymin, xmax, ymax):
    obj = ET.Element('object')
    ET.SubElement(obj, 'name').text = 'face'
    ET.SubElement(obj, 'pose').text = 'Unspecified'
    ET.SubElement(obj, 'truncated').text = '0'
    ET.SubElement(obj, 'difficult').text = '0'

    bndbox = ET.SubElement(obj, 'bndbox')
    ET.SubElement(bndbox, 'xmin').text = xmin
    ET.SubElement(bndbox, 'ymin').text = ymin
    ET.SubElement(bndbox, 'xmax').text = xmax
    ET.SubElement(bndbox, 'ymax').text = ymax

    return ET.ElementTree(obj)

def parseImFilename(imFilename, imPath):
    im = Image.open(os.path.join(imPath, imFilename))

    folder, basename = imFilename.split('/')
    width, height = im.size

    return folder, basename, imFilename, str(width), str(height)

def convertWFAnnotations(annotationsPath, targetPath, imPath, fixPath):
    ann = None
    basename = ''
    with open(annotationsPath) as f:
        while True:
            imFilename = f.readline().strip()

            '''
            discard err in name example:
                dataset/train/0 0 0 0 0 0 0 0 0 0

            in file:

                0--Parade/0_Parade_Parade_0_1040.jpg
                1
                494 251 75 110 0 0 0 0 2 0
                0--Parade/0_Parade_Parade_0_452.jpg
                0
                0 0 0 0 0 0 0 0 0 0                      <-- Fix Error
                0--Parade/0_Parade_Parade_0_630.jpg
                17
                20 186 14 20 1 0 0 0 0 0
                94 162 31 49 0 0 0 0 0 0
                119 181 14 17 2 0 0 0 2 0
                190 142 25 38 1 0 1 0 0 0
                375 129 46 62 0 0 0 0 0 0
                150 163 19 25 0 0 0 0 1 0
                349 122 26 38 0 0 0 0 0 0
                458 150 31 42 0 0 0 0 0 0
                527 174 10 16 1 0 0 0 0 0
                560 131 25 39 0 0 0 0 0 0
                695 143 49 64 0 0 0 0 0 0
                742 164 10 14 2 0 0 0 2 0
                822 138 29 38 0 0 0 0 2 0
                890 140 23 48 0 0 0 0 0 1
                954 156 12 18 1 0 0 0 0 0
                988 209 16 17 1 0 0 0 0 0
                615 143 22 24 1 0 0 0 2 0
            '''
            if len(imFilename.split(' ')) > 1:
                continue

            if imFilename:
                folder, basename, path, width, height = parseImFilename(imFilename, imPath)
                ann = createAnnotationPascalVocTree(folder, basename, os.path.join(fixPath, path), width, height)
                nbBndboxes = f.readline()

                i = 0
                while i < int(nbBndboxes):
                    i = i + 1
                    x1, y1, w, h, _, _, _, _, _, _ = [int(i) for i in f.readline().split()]

                    ann.getroot().append(createObjectPascalVocTree(str(x1), str(y1), str(x1 + w), str(y1 + h)).getroot())

                if not os.path.exists(targetPath):
                     os.makedirs(targetPath)
                annFilename = os.path.join(targetPath, basename.replace('.jpg','.xml'))

                # pretty annotation
                o = open(annFilename, 'wb')
                o.write(bytes(
                        minidom.parseString(
                            ET.tostring(ann.getroot())) \
                                    .toprettyxml(indent="   ").encode('utf-8')))
                o.close()
                print('{} => {}'.format(basename, annFilename))
            else:
                break
    f.close()


if __name__ == '__main__':
    import argparse

    PARSER = argparse.ArgumentParser()
    PARSER.add_argument('-ap', '--annotations-path', help='the annotations file path. ie:"./wider_face_split/wider_face_train_bbx_gt.txt".')
    PARSER.add_argument('-tp', '--target-path', help='the target directory path where XML files will be copied.')
    PARSER.add_argument('-ip', '--images-path', help='the images directory path. ie:"./WIDER_train/images"')
    PARSER.add_argument('-fp', '--fix-images-path', help='annotation base path replace')

    ARGS = vars(PARSER.parse_args())

    if not ARGS['fix_images_path']:
        ARGS['fix_images_path'] = ARGS['images_path']

    convertWFAnnotations(ARGS['annotations_path'],
                            ARGS['target_path'],
                            ARGS['images_path'],
                            ARGS['fix_images_path'])

