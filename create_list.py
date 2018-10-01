import os
#创建name_list和img_xml_list
def create_list(dataName,img_list_txt,img_path,img_name_list_txt,type):
    f=open(img_name_list_txt,'w')
    fAll=open(img_list_txt,'w')
    for name in os.listdir(img_path):
        f.write(name[0:-4]+'\n')
        fAll.write(dataName+'/'+'JPEGImages'+'/'+type+'/'+name[0:-4]+img_suffix+' ')
        fAll.write(dataName+'/'+'Annotations'+'/'+type+'/'+name[0:-4]+'.xml'+'\n')
    f.close()

dataset_prefix="F:/竞赛/PRCV/mission"
img_suffix = '.jpg'
dataName = 'people_detection'  # dataset name
type = 'test'  # type
bb_split=','
img_path = dataset_prefix+"/"+ dataName + '/JPEGImages/' + type + '/'  # img path
img_name_list_txt = dataset_prefix+"/"+ dataName + '/ImageSets/Main/'+type+'.txt'
img_xml_list_txt = dataset_prefix+"/"+ dataName + '/listfile/' + type +'.txt'
create_list(dataName,img_xml_list_txt,img_path,img_name_list_txt,type)