#将普通的图片，txt标注框数据集，转换成VOC格式的

#! /usr/bin/python

import os, sys
import glob
from PIL import Image
import shutil

#src_img_dir = "/media/chenxp/Datadisk/ocr_dataset/ICDAR2011/train-textloc"
#src_txt_dir = "/media/chenxp/Datadisk/ocr_dataset/ICDAR2011/train-textloc"
src_img_dir = "F:/竞赛/PRCV/mission/detection/train/images"
src_txt_dir = "F:/竞赛/PRCV/mission/detection/train/predicted"
#src_img_dir = "F:/竞赛/PRCV/mission/detection/test/images"
#src_txt_dir = "F:/竞赛/PRCV/mission/detection/test/predicted"
#txt的标记文件的前缀
anno_prefix = ""
dataset_prefix="F:/竞赛/PRCV/mission/detection"
anno_sub_dir = "Annotations"
imge_sub_dir = "JPEGImages"
dataset="people_detection"
train_test = "train"
anno_dir = os.path.join(dataset_prefix,dataset,anno_sub_dir)
image_dir = os.path.join(dataset_prefix,dataset,imge_sub_dir)
if(os.path.exists(os.path.join(dataset_prefix,dataset)) is False):
    os.mkdir(os.path.join(dataset_prefix,dataset))
if(os.path.exists(anno_dir) is False):
    os.mkdir(anno_dir)
if(os.path.exists(image_dir) is False):
    os.mkdir(image_dir)
dst_anno_dir = os.path.join(anno_dir,train_test)
dst_img_dir = os.path.join(image_dir,train_test)
if(os.path.exists(os.path.join(anno_dir,train_test)) is False):
    os.mkdir(os.path.join(anno_dir,train_test))
if(os.path.exists(os.path.join(image_dir,train_test)) is False):
    os.mkdir(os.path.join(image_dir,train_test))

img_Lists = glob.glob(src_img_dir + '/*.jpg')

img_basenames = [] # e.g. 100.jpg
for item in img_Lists:
    img_basenames.append(os.path.basename(item))

img_names = [] # e.g. 100
for item in img_basenames:
    shutil.copy(os.path.join(src_img_dir, item),os.path.join(dst_img_dir,item))
    temp1, temp2 = os.path.splitext(item)
    img_names.append(temp1)

for img in img_names:
    im = Image.open((src_img_dir + '/' + img + '.jpg'))
    width, height = im.size

    # open the crospronding txt file
    gt = open(os.path.join(src_txt_dir, anno_prefix ,img + '.txt')).read().splitlines()

    # write in xml file
    #os.mknod(anno_dir + '/' + img + '.xml')
    xml_file = open((dst_anno_dir + '/' + img + '.xml'), 'w')
    xml_file.write('<annotation>\n')
    xml_file.write('    <folder>VOC2007</folder>\n')
    xml_file.write('    <filename>' + str(img) + '.jpg' + '</filename>\n')
    xml_file.write('    <size>\n')
    xml_file.write('        <width>' + str(width) + '</width>\n')
    xml_file.write('        <height>' + str(height) + '</height>\n')
    xml_file.write('        <depth>3</depth>\n')
    xml_file.write('    </size>\n')

    # write the region of text on xml file
    for img_each_label in gt:
        spt = img_each_label.split(' ')
        xml_file.write('    <object>\n')
        xml_file.write('        <name>text</name>\n')
        xml_file.write('        <pose>Unspecified</pose>\n')
        xml_file.write('        <truncated>0</truncated>\n')
        xml_file.write('        <difficult>0</difficult>\n')
        xml_file.write('        <bndbox>\n')
        xml_file.write('            <xmin>' + str(spt[0]) + '</xmin>\n')
        xml_file.write('            <ymin>' + str(spt[1]) + '</ymin>\n')
        xml_file.write('            <xmax>' + str(int(spt[0])+int(spt[3])) + '</xmax>\n')
        xml_file.write('            <ymax>' + str(int(spt[1])+int(spt[2])) + '</ymax>\n')
        xml_file.write('        </bndbox>\n')
        xml_file.write('    </object>\n')

    xml_file.write('</annotation>')
    xml_file.close()

