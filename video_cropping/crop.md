#视频裁剪区域映射
![img_2.png](img_2.png)


主要是依据造影对应的Pascal_VOC数据集标注格式的xml标注文件对视频进行裁剪，xml标注文件格式如下：

![xml_pic](img.png) 

而后读取对应标注框位置，并映射至超声造影区域进行视频裁剪，视频和xml存放格式如下：

![img_1.png](img_1.png)

