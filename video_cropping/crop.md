# 视频裁剪区域映射

### 依赖包：
`pip install tqdm` \
`pip install opencv-python` 

----
# 简介
⭐ 1.主要是依据造影对应的Pascal_VOC数据集标注格式的xml读取视频对应标注框位置，并映射至超声造影区域进行视频裁剪。 \
⭐ 2.循环利用cv2打开造影文件逐帧裁剪并按指定编码器 “XVID” 生成avi格式可自定时间（取0-30s）的视频数据。
<div align="center">
  <img src="../readme_raw_pic/cropping/img_2.png" width="300"/>
</div>

---
# 使用示例

##数据准备
将所需裁剪的造影视频数据及对应的**同名**xml标注文件置于同一文件夹，xml文件标注格式及文件夹内存储格式如下:

| xml文件标注格式                                | xml文件与视频文件存储格式                            |
|------------------------------------------|-------------------------------------------|
| ![](../readme_raw_pic/cropping/img.png)  | ![](../readme_raw_pic/cropping/img_1.png) |

##设置文件路径

```python
    video_path = 'D:/subject/Datasets/视频裁剪label' # video_path对应存放原始视频和对应标注文件的位置
    output_path = 'D:/subject/Datasets/视频裁剪label/epoch1' # output_path对应输出位置
    video_cropping(video_path,output_path) # 程序入口
```

## 设置终止时间


```python
    if time == 300:
        break  #设置终止时间
```


-----
# 代码实现
### 读取原影像bounding boxes标注坐标转化为列表


````python
  for root,dirs,files in os.walk(root_path):
        for file in tqdm(files):
            if (".avi" in file):    #对avi文件进行遍历
                # 获取文件名及后缀
                filename,extension = file.split(".")
                path = os.path.join(root, file)
                List_boundary = []
                xmlname = os.path.join(root, filename + ".xml")
                # 读取xml注释文件
                tree = ET.parse(xmlname)
                # 获取根节点
                xml_root = tree.getroot()
                for ob in xml_root.iter('object'):
                    for bndbox in ob.iter('bndbox'):
                        for xmin in bndbox.iter('xmin'):
                            x1 = xmin.text
                            List_boundary.append(x1)
                        for ymin in bndbox.iter('ymin'):
                            y1 = ymin.text
                            List_boundary.append(y1)
                        for xmax in bndbox.iter('xmax'):
                            x2 = xmax.text
                            List_boundary.append(x2)
                        for ymax in bndbox.iter('ymax'):
                            y2 = ymax.text
                            List_boundary.append(y2)

                for i in range(len(List_boundary)):
                    List_boundary[i] = int(List_boundary[i])
                a,b,c,d = List_boundary
````


### 利用opencv包裁剪视频
```python

                cap = cv2.VideoCapture(path)
                outputname = output_path + '/' + filename + 'cut.' + extension
                fps = cap.get(5)
                cut_size = (c-a, d-b)
                fourcc = cv2.VideoWriter_fourcc(*'XVID')

                #VideoWriter参数设定：输出路径；编码器；帧率；大小尺寸
                output = cv2.VideoWriter(outputname,fourcc,fps,cut_size)
                time = 0
                while cap.isOpened():
                    time = time + 1
                    ret, frame = cap.read()
                    target = frame[b:d, a-400:c-400]
                    output.write(target)
                    # 设定时间到达30s时停止
                    if time == 300:
                        break
```