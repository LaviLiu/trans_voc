# trans_voc
将自己的目标检测的数据集的标注方式转换成VOC数据集格式
# 文件准备
1. 运行bbox_to_xml.py将标注形式转换成xml格式。
常见的目标检测数据集的标注方式是txt格式的,如202017000300_R_2018_05_17_11_37_26_left_000262.txt，做目标检测需要把数据的的标注改成xml 形式的，如202017000300_R_2018_05_17_11_37_26_left_000262.xml所示，对训练集合测试集分别生成。
2. create_list.py 创建图片和标注的xml文件的对应列表。
如train.txt和test.txt所示，格式如 下所示，对训练集合测试集分别生成。
```
people_detection/JPEGImages/train/202017000300_R_2018_05_17_11_37_26_left_000262.jpg people_detection/Annotations/train/202017000300_R_2018_05_17_11_37_26_left_000262.xml
people_detection/JPEGImages/train/202017000300_R_2018_05_17_11_37_26_left_000467.jpg people_detection/Annotations/train/202017000300_R_2018_05_17_11_37_26_left_000467.xml
...
```
3. create_name_list.py 创建图片的名称列表，不带有后缀名。对训练集合测试集分别生成。如下所示:
```
202017000300_R_2018_05_17_11_37_26_left_000262
202017000300_R_2018_05_17_11_37_26_left_000467
...
```
4. create_name_size.py 创建图片大小列表，格式如下所示：
```
202017000300_R_2018_05_17_11_37_26_left_005337 320 240
202017000300_R_2018_05_17_11_37_26_left_005787 320 240
...
```
# 生成lmdb
我有一个专门将数据集装换成lmdb 的文件夹，gttolmdb，目录结构如下所示。
- gttolmbd
  - mydataset #原始数据集和一些前面生成的只做lmdb数据集需要的文件
    - people_detection #数据集的名字
      - Annotation # xml形式的标注文件，如果没有使用bbox_to_xml.py生成。
        - train # 训练集的标注文件
        - test # 测试集的标注文件
      - ImageSets
        - Main # 图片的名称列表，不需要后缀名，如果没有使用create_name_list.py生成
      - JPEGImages # 原始的图片文件
        - train #训练集的图片文件
        - test #测试集图片文件
      - listfile #其他一些列表文件
        - train.txt # 训练集图片与标注的xml文件列表，是上面使用create_list.py生成的
        - test.txt # 测试集图片与标注的xml文件列表，是上面使用create_list.py生成的
        - train_name_size.txt # 训练集图片大小列表文件，使用 create_name_size.py生成
        - test_name_size.txt # 测试集图片大小列表文件，使用 create_name_size.py生成
  - result #生成的结果
    - people_detection #数据集名称
      - people_detection_train_lmdb # 生成的训练集lmdb文件位置
      - people_detection_test_lmdb #生成的测试集lmdb文件位置
      - labelmap_people_detection.prototxt # 列表标签映射文件
      
      #下面的四个文件是从上面的listfile文件夹中复制来的，之所以复制到result是以为，训练网络的时候会用到这四个文件，把训练用到到的文件都放在result文件夹下，比较清晰容易找到
      - train.txt # 训练集图片与标注的xml文件列表，是上面使用create_list.py生成的
      - test.txt # 测试集图片与标注的xml文件列表，是上面使用create_list.py生成的
      - train_name_size.txt # 训练集图片大小列表文件，使用 create_name_size.py生成
      - test_name_size.txt # 测试集图片大小列表文件，使用 create_name_size.py生成
  - create_annoset.py #生成lmdb需要调用的python脚本
  - create_data.sh #生成lmdb需要的shell文件
  
只需要准备好相应的文件，修改create_data.sh中的数据库的名字，路径等，create_annoset.py中caffe的根目录，然后运行 create_data.sh 就可以在result下生成lmdb数据集。
# 工具脚本
1. visual_boxes.py 使用opencv-python 可视化txt文件中的标注框
2. drawbox.py 使用PIL.ImageDraw 可视化txt文件的标注框
3. renameTool.py 对图片文件重命名，同时可以对对应的标注文件重命名


