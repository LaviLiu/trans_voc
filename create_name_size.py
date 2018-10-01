import os
from PIL import Image
dataset_prefix="F:/竞赛/PRCV/mission"
datasetName = "people_detection"
type="test"
name_size = os.path.join(dataset_prefix,datasetName,"listfile")+'/'+type+'_name_size.txt'
img_dir = os.path.join(dataset_prefix,datasetName,"JPEGImages",type)
name_size_file = open(name_size, 'w')

for img_name in os.listdir(img_dir):
    img = Image.open(os.path.join(img_dir,img_name))
    width,height = img.size
    name_size_file.write(img_name[0:-4]+" "+str(width)+" "+str(height)+"\n")
name_size_file.close()
