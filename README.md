# WIDER FACE PASCAL VOC ANNOTATIONS

This repository contains the [WIDER FACE](http://mmlab.ie.cuhk.edu.hk/projects/WIDERFace/) annotations converted to the [Pascal VOC](http://host.robots.ox.ac.uk/pascal/VOC/) XML format.

It also contains the script used to do this conversion.

```
usage: convert.py [-h] [-ap ANNOTATIONS_PATH] [-tp TARGET_PATH]
                  [-ip IMAGES_PATH]

optional arguments:
  -h, --help            show this help message and exit
  -ap ANNOTATIONS_PATH, --annotations-path ANNOTATIONS_PATH
                        the annotations file path.
                        ie:"./wider_face_split/wider_face_train_bbx_gt.txt".
  -tp TARGET_PATH, --target-path TARGET_PATH
                        the target directory path where XML files will be
                        copied.
  -ip IMAGES_PATH, --images-path IMAGES_PATH
                        the images directory path. ie:"./WIDER_train/images"
```

It has been used as following:

```
$ ./convert.py -ap ./wider_face_split/wider_face_train_bbx_gt.txt -tp ./WIDER_train_annotations/ -ip ./WIDER_train/images/
$ ./convert.py -ap ./wider_face_split/wider_face_val_bbx_gt.txt -tp ./WIDER_val_annotations/ -ip ./WIDER_val/images/
```

# License

MIT Licensed. Copyright (c) Alexis Kofman 2018.