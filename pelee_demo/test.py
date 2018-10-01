#coding:utf-8
import numpy as np

import os
import caffe

#from google.protobuf import text_format
#from caffe.proto import caffe_pb2

# load PASCAL VOC labels


model_def = 'model/people_detection/deploy.prototxt'
model_weights = 'model/people_detection/pelee_SSD_304x304_iter_82000.caffemodel'

net = caffe.Net(model_def,  # defines the structure of the model
                model_weights,  # contains the trained weights
                caffe.TEST)  # use test mode (e.g., don't perform dropout)

# input preprocessing: 'data' is the name of the input blob == net.inputs[0]
transformer = caffe.io.Transformer({'data': net.blobs['data'].data.shape})
transformer.set_transpose('data', (2, 0, 1))
transformer.set_input_scale('data', 0.017)
transformer.set_mean('data', np.array([103.94, 116.78, 123.68]))  # mean pixel
transformer.set_raw_scale('data', 255)  # the reference model operates on images in [0,255] range instead of [0,1]
transformer.set_channel_swap('data', (2, 1, 0))  # the reference model has channels in BGR order instead of RGB


def do_detect(image):
    transformed_image = transformer.preprocess('data', image)
    net.blobs['data'].data[...] = transformed_image

    # Forward pass.
    detections = net.forward()['detection_out']
    # Parse the outputs.
    #det_label = detections[0, 0, :, 1]
    det_conf = detections[0, 0, :, 2]
    det_xmin = detections[0, 0, :, 3]
    det_ymin = detections[0, 0, :, 4]
    det_xmax = detections[0, 0, :, 5]
    det_ymax = detections[0, 0, :, 6]

    # Get detections with confidence higher than 0.4.
    top_indices = [i for i, conf in enumerate(det_conf) if conf >= 0.4]

    top_conf = det_conf[top_indices]

    top_xmin = det_xmin[top_indices]
    top_ymin = det_ymin[top_indices]
    top_xmax = det_xmax[top_indices]
    top_ymax = det_ymax[top_indices]

    #plt.imshow(image)
    #plt.savefig("samples/202017000300_R_2018_05_17_11_37_26_left_005337_1.png")

    result_str = ""
    for i in xrange(top_conf.shape[0]):
        xmin = int(round(top_xmin[i] * image.shape[1]))
        ymin = int(round(top_ymin[i] * image.shape[0]))
        xmax = int(round(top_xmax[i] * image.shape[1]))
        ymax = int(round(top_ymax[i] * image.shape[0]))
        result_str += str(xmin)+" "+str(ymin) +" "+str(ymax - ymin)+" "+str(xmax - xmin)+" "+top_conf[i]+"\n"
    return result_str
# set net to batch size of 1
batch_size = 1
image_resize = 304
net.blobs['data'].reshape(batch_size, 3, image_resize, image_resize)
#test_dir = "F:\\竞赛\\PRCV\\mission\\detection\\test\\images"
test_dir = "/home/lavi/gttolmdb/mydataset/people_detection/JPEGImages/test"
result_dir = "result"

result_list = []
name_list=[]
for img_name in os.listdir(test_dir):
    name_list.append(img_name[0:-4]+".txt")
    image = caffe.io.load_image(os.path.join(test_dir, img_name))
    result_list.append(do_detect(image))
i = 0
for name in name_list:
    with open(os.path.join(result_dir,name),'w') as f:
        f.write(result_list[i])
        i += 1

