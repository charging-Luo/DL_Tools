import cv2
import os
from tqdm import tqdm

import xml.etree.ElementTree as ET
from xml.etree.ElementTree import Element

# for PASCAL_VOC_dataset xml labels
def video_cropping(root_path,output_path=None):

    if output_path == None:
        output_path = root_path

    for root,dirs,files in os.walk(root_path):
        for file in tqdm(files):
            if (".avi" in file): #对avi文件进行遍历
                filename,extension = file.split(".") #获取文件名及后缀
                path = os.path.join(root, file)
                List_boundary = []
                xmlname = os.path.join(root, filename + ".xml")
                tree = ET.parse(xmlname) #读取xml注释文件
                xml_root = tree.getroot() #获取根节点
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
                    if time == 300:
                        break




if __name__ == '__main__':
    video_path = 'D:/subject/Datasets/视频裁剪label'
    output_path = 'D:/subject/Datasets/视频裁剪label/epoch1'
    video_cropping(video_path,output_path)