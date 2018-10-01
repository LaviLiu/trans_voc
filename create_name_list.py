import os
dataset_prefix="F:/竞赛/PRCV/mission/detection"
datasetName = "people_detection"
img="JPEGImages"
type="train"
name_list = os.path.join(dataset_prefix,datasetName,"ImageSets/Main")+"/"+type+".txt"
with open(name_list,'w') as f:
    for name in os.listdir(os.path.join(dataset_prefix,datasetName,img,type)):
        f.write(name[0:-4]+"\n")
