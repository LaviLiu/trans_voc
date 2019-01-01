import xml.dom.minidom as xmldom
import cv2

def parser_xml(name):
    boxes_list = []
    DomTree = xmldom.parse(name)
    annotation = DomTree.documentElement
    filenamelist = annotation.getElementsByTagName('filename')  # [<DOM Element: filename at 0x381f788>]
    filename = filenamelist[0].childNodes[0].data
    objectlist = annotation.getElementsByTagName('object')
    for object in objectlist:
        bndbox = object.getElementsByTagName('bndbox')
        box = bndbox[0]
        #box = bndbox[0].childNodes[0]
        xmin = box.getElementsByTagName('xmin')
        x1 = int(xmin[0].childNodes[0].data)
        ymin = box.getElementsByTagName('ymin')
        y1 = int(ymin[0].childNodes[0].data)
        xmax = box.getElementsByTagName('xmax')
        x2 = int(xmax[0].childNodes[0].data)
        ymax = box.getElementsByTagName('ymax')
        y2 = int(ymax[0].childNodes[0].data)
        w = x2 - x1
        h = y2 - y1
        boxes_list.append((x1,y1,w,h))
    #print (filename,boxes_list)
    #print(type(filename))
    #print(type(filename.encode('utf-8')))
    return filename.encode('utf-8'), boxes_list

def visual(imgName, xml):
    image = cv2.imread(imgName)
    height, width = image.shape[0:2]
    print(width, height)
    filename, boxes_list = parser_xml(xml)
    #boxes = boxes_list[0]
    #cv2.rectangle(image, (int(boxes[0]), int(boxes[1])), (int(boxes[0]) + int(boxes[3]), int(boxes[1]) + int(boxes[2])),(255, 0, 0), 1)
    for boxes in boxes_list:
        cv2.rectangle(image, (int(boxes[0]), int(boxes[1])),(int(boxes[0]) + int(boxes[3]), int(boxes[1]) + int(boxes[2])), (255, 0, 0), 1)
    cv2.imshow("image", image)
    cv2.waitKey(0)


if __name__ == '__main__':
    imgName = 'IMG_1.jpg'
    xml = 'IMG_1.xml'
    visual(imgName, xml)
