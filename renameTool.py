#coding:utf-8
'''
@author: Lenovo
'''

import os,shutil
from astropy.time.utils import split

def rename(dir,prefix,sparator='_',saveDir=None,suffix=None,renameAnno=False,annoDir=None,annoSaveDir=None,oldAnnoSuffix='.xml',newAnnoSuffix=None):
    '''
    function: 修改某个文件夹下的文件的名称和扩展名，如果文件有同名的注释/标注文件，
    可以同时修改对应标注文件的名称和扩展名同时保留原文件
    Args：
        dir:文件原始路径，最后不需要加斜杠
        saveDir:文件修改名称后存储的路径，最后不需要加斜杠
        suffix:新的扩展名
        renameAnno：是否需要修改同名的注释文件的名称
        annoDir：注释文件的原始路径，，最后不足要加斜杠
        annoSaveDir：注释文件修改名称后存储的路径，最后不足要加斜杠
        oldAnnoSuffix：注释文件的原始后缀名
        newAnnoSuffix：注释文件修改后的后缀名
    '''
    # 检查参数
    if saveDir is None:
        saveDir = dir
    #检查保存文件夹是否存在，不存在创建
    if os.path.exists(saveDir)is False:
        os.makedirs(saveDir)
        
    if renameAnno:
        if annoSaveDir is None:
            annoSaveDir = annoDir
        if newAnnoSuffix is None:
            newAnnoSuffix = oldAnnoSuffix
        if annoDir is None:
            print("please input annoDir")
            exit(-1)
            if os.path.exists(annoSaveDir)is False:
                os.makedirs(annoSaveDir)
        if os.path.exists(annoSaveDir)is False:
            os.makedirs(annoSaveDir)
    
        
    i=0
    filelist = os.listdir(dir)#该文件夹下所有的文件（包括文件夹）
    #xmllist = os.listdir(xmlDir)#该文件夹下所有的文件（包括文件夹）
    for files in filelist:#遍历所有文件
        
        oldPath = os.path.join(dir,files);#原来的文件路径
        if os.path.isdir(oldPath):#如果是文件夹则跳过
            continue;
        # splitext 函数用来分离文件名和扩展名
        filename=os.path.splitext(files)[0];#文件名
        filetype=os.path.splitext(files)[1];#文件扩展名 ,前面带有点
        if suffix is None:
            suffix = filetype
        newName = prefix + sparator + str(i)
        newPath=os.path.join(saveDir,newName+suffix);#新的文件路径
        #如果文件已经存在则删除，再复制
        if os.path.exists(newPath):
            os.remove(newPath)
        #os.rename(oldPath,newPath)#重命名:可以将原来的文件移动到新的路径下
        shutil.copyfile(oldPath,newPath)#复制
        if renameAnno:
            #默认一个文件对应一个同名的标注文件
            oldAnnoPath = os.path.join(annoDir,filename+oldAnnoSuffix)
            newAnnoPath=os.path.join(annoSaveDir,newName + newAnnoSuffix);#新的文件路径
            if os.path.exists(newAnnoPath):
                os.remove(newAnnoPath)
            shutil.copyfile(oldAnnoPath,newAnnoPath)#复制
        i=i+1
           
    print("rename done.................")