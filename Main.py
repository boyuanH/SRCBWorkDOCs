from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import os

def __is_point_in_exist_rect__(point, rects):
    # 判断该点是否是在一个已知的矩形list里 矩形为一个turple,前两个为坐标点，后两个为width height
    for rect in rects:
        x1 = rect[1]
        x2 = x1 + rect[2] - 1
        y1 = rect[0]
        y2 = y1 + rect[3] - 1
        if x1 <= point[3][1] <= x2 and y1 <= point[3][0] <= y2:
            return True
    return False


def __find_rect_by_point__(curr_point, img_array):
    i = curr_point[3][0]
    j = curr_point[3][1]
    # 当确定了i,j是左上角点后，求出该矩形的长宽各占多少像素点
    rect_width = 1
    rect_height = 1
    rows, cols, div = img_array.shape
    last_point = [img_array[i, j][0], img_array[i, j][1], img_array[i, j][2]]
    for row in range(i+1, rows):
        current_point = img_array[row, j]
        if __is_green_point__(last_point) is False and __is_green_point__(current_point) is True:
            break
        else:
            rect_height = rect_height + 1
    last_point = [img_array[i, j][0], img_array[i, j][1], img_array[i, j][2]]
    for col in range(j+1, cols):
        current_point = img_array[i, col]
        if __is_green_point__(last_point) is False and __is_green_point__(current_point) is True:
            break
        else:
            rect_width = rect_width + 1
    rect = (i, j, rect_width, rect_height)
    return rect


def __is_new_img_point(last_point, next_point):
    if __is_green_point__(last_point) is True and __is_green_point__(next_point) is False:
        return True
    else:
        return False


def __is_green_point__(point):
    if point[0] == 0 and point[1] == 255 and point[2] == 0:
        return True
    else:
        return False


def __output_rect__(rect, image_name, img):
    img_out_array = []
    for y in range(rect[0], rect[3] + rect[0]):
        row_array = []
        for x in range(rect[1], rect[1] + rect[2]):
            row_array.append(img[y, x])
        img_out_array.append(row_array)
    plt.imsave(image_name, img_out_array)


def main():
    current_file_name = 'testImg.bmp'
    directory_info = "D:\\Work\\RICOH\\tmpImg\\"
    target_directory = 'D:\\Work\\RICOH\\imgs\\'
    files = os.listdir(directory_info)
    for file_index in range(0, len(files)):
        current_file_name = os.path.join(directory_info, files[file_index])
        if os.path.isfile(current_file_name):
            img = np.array(Image.open(current_file_name))  # 打开图像并转化为数字矩阵
            rects = []
            rows, cols, div = img.shape
            for i in range(rows):
                lst_point = [0, 255, 0, [i, -1]]
                for j in range(cols):
                    current_point = [img[i, j][0], img[i, j][1], img[i, j][2], [i, j]]
                    if __is_new_img_point(lst_point, current_point) is True:
                        if __is_point_in_exist_rect__(current_point, rects) is False:
                            rects.append(__find_rect_by_point__(current_point, img))
                    lst_point = current_point
            index = 0
            (short_name, extension) = os.path.splitext(files[file_index])
            for rect in rects:
                img_name = target_directory + short_name + '_' + str(index) + extension
                __output_rect__(rect, img_name, img)
                index = index + 1
                print(short_name + 'Saved')


if __name__ == "__main__":
    main()


