import os
import cv2


# 视频切片

def slice_video(root_path, cut_frame, out_path):
    for root, dirs, files in os.walk(root_path):
        for file in files:

            filename, extension = file.split('')
            if '.avi' in file:
                path = os.path.join(root, file)
                video = cv2.VideoCapture(path)
                video_fps = int(video.get(cv2.CAP_PROP_FPS))

                outPutDirName = out_path + '/' + filename + '/'
                if not os.path.exists(outPutDirName):
                    os.makedirs(outPutDirName)

                print(video_fps)
                current_frame = 0
                while (True):
                    ret, image = video.read()
                    current_frame = current_frame + 1
                    if ret is False:
                        video.release()
                        break
                    if current_frame % cut_frame == 0:
                        # cv2.imwrite(save_path + '/' + file[:-4] + str(current_frame) + '.jpg',
                        #             image)  # file[:-4]是去掉了".mp4"后缀名，这里我的命名格式是，视频文件名+当前帧数+.jpg，使用imwrite就不能有中文路径和中文文件名
                        cv2.imwrite(outPutDirName + str(current_frame) + '.jpg', image)
                        # cv2.imencode('.jpg', image)[1].tofile(outPutDirName + file[:-4] + str(current_frame) + '.jpg')
                        # #使用imencode就可以整个路径中可以包括中文，文件名也可以是中文
                        print('正在保存' + file + outPutDirName + '/' + file[:-4] + str(current_frame))
                    if current_frame == 300:
                        break


if __name__ == '__main__':
    cut_frame = 5  # 间隔多少帧切一片
    root_path = ''
    out_path = ''
    slice_video(root_path,cut_frame,out_path)
