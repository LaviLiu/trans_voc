import numpy as np
import matplotlib.pyplot as plt


import os
import caffe

from google.protobuf import text_format
from caffe.proto import caffe_pb2

# load PASCAL VOC labels
labelmap_file = 'model/people_detection/labelmap_people_detection.prototxt'
file = open(labelmap_file, 'r')
labelmap = caffe_pb2.LabelMap()
text_format.Merge(str(file.read()), labelmap)

def get_labelname(labelmap, labels):
    num_labels = len(labelmap.item)
    labelnames = []
    if type(labels) is not list:
        labels = [labels]
    for label in labels:
        found = False
        for i in xrange(0, num_labels):
            if label == labelmap.item[i].label:
                found = True
                labelnames.append(labelmap.item[i].display_name)
                break
        assert found == True
    return labelnames

model_def = 'model/people_detection/deploy.prototxt'
model_weights = 'model/people_detection/pelee_SSD_304x304_iter_82000.caffemodel'

net = caffe.Net(model_def,      # defines the structure of the model
                model_weights,  # contains the trained weights
                caffe.TEST)     # use test mode (e.g., don't perform dropout)

# input preprocessing: 'data' is the name of the input blob == net.inputs[0]
transformer = caffe.io.Transformer({'data': net.blobs['data'].data.shape})
transformer.set_transpose('data', (2, 0, 1))
transformer.set_input_scale('data', 0.017)
transformer.set_mean('data', np.array([103.94,116.78,123.68])) # mean pixel
transformer.set_raw_scale('data', 255)  # the reference model operates on images in [0,255] range instead of [0,1]
transformer.set_channel_swap('data', (2,1,0))  # the reference model has channels in BGR order instead of RGB

def do_detect(image,colors):
    transformed_image = transformer.preprocess('data', image)
    net.blobs['data'].data[...] = transformed_image

    # Forward pass.
    detections = net.forward()['detection_out']

    # Parse the outputs.
    det_label = detections[0,0,:,1]
    det_conf = detections[0,0,:,2]
    det_xmin = detections[0,0,:,3]
    det_ymin = detections[0,0,:,4]
    det_xmax = detections[0,0,:,5]
    det_ymax = detections[0,0,:,6]

    # Get detections with confidence higher than 0.4.
    top_indices = [i for i, conf in enumerate(det_conf) if conf >= 0.4]

    top_conf = det_conf[top_indices]
    top_label_indices = det_label[top_indices].tolist()
    top_labels = get_labelname(labelmap, top_label_indices)
    top_xmin = det_xmin[top_indices]
    top_ymin = det_ymin[top_indices]
    top_xmax = det_xmax[top_indices]
    top_ymax = det_ymax[top_indices]

    plt.imshow(image)
    plt.savefig("samples/202017000300_R_2018_05_17_11_37_26_left_005337_1.png")

    currentAxis = plt.gca()
    currentAxis.axes.xaxis.set_visible(False)
    currentAxis.axes.yaxis.set_visible(False)
    font = {'weight' : 'bold',
        'size'   : 12}

    plt.rc('font', **font)

    for i in xrange(top_conf.shape[0]):
        xmin = int(round(top_xmin[i] * image.shape[1]))
        ymin = int(round(top_ymin[i] * image.shape[0]))
        xmax = int(round(top_xmax[i] * image.shape[1]))
        ymax = int(round(top_ymax[i] * image.shape[0]))
        score = top_conf[i]
        label = int(top_label_indices[i])
        label_name = top_labels[i]
        display_txt = '%s: %.2f'%(label_name, score)
        coords = (xmin, ymin), xmax-xmin+1, ymax-ymin+1
        color = colors[label]
        currentAxis.add_patch(plt.Rectangle(*coords, fill=False, edgecolor=color, linewidth=2))
        currentAxis.text(xmin, ymin, display_txt, bbox={'facecolor':color, 'alpha':0.8})
    
    plt.savefig("samples/202017000300_R_2018_05_17_11_37_26_left_005337_2.png")

# set net to batch size of 1
image_resize = 304
net.blobs['data'].reshape(1,3,image_resize,image_resize)

colors=[]
for r in [0.2,0.4,0.8,0.6,1.0]:
    for g in [0.3,0.7]:
        for b in [0.4,0.8]:
            colors.append([r,g,b,1.0])

plt.rcParams['figure.figsize'] = (10, 10)
plt.rcParams['image.interpolation'] = 'nearest'
plt.rcParams['image.cmap'] = 'gray'

image = caffe.io.load_image('samples/202017000300_R_2018_05_17_11_37_26_left_005337.jpg')
do_detect(image, colors)
