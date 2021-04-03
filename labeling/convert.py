import os
import shutil
from bs4 import BeautifulSoup

def run_convert(all_classes, train_img, train_annotation, yolo_path, write_txt):
    now_path = os.getcwd()
    data_counter = 0

    for data_file in os.listdir(train_annotation):
        try:
            with open(os.path.join(train_annotation, data_file), 'r', encoding='utf-8') as f:
                print("read file...")
                soup = BeautifulSoup(f.read(), 'xml')
                img_name = soup.select_one('filename').text

                for size in soup.select('size'):
                    img_w = int(size.select_one('width').text)
                    img_h = int(size.select_one('height').text)
                    
                img_info = []
                for obj in soup.select('object'):
                    xmin = int(obj.select_one('xmin').text)
                    xmax = int(obj.select_one('xmax').text)
                    ymin = int(obj.select_one('ymin').text)
                    ymax = int(obj.select_one('ymax').text)
                    objclass = all_classes.get(obj.select_one('name').text)

                    x = (xmin + (xmax-xmin)/2) * 1.0 / img_w
                    y = (ymin + (ymax-ymin)/2) * 1.0 / img_h
                    w = (xmax-xmin) * 1.0 / img_w
                    h = (ymax-ymin) * 1.0 / img_h
                    img_info.append(' '.join([str(objclass), str(x),str(y),str(w),str(h)]))

                # copy image to yolo path and rename
                img_path = os.path.join(train_img, img_name)
                img_format = img_name.split('.')[1]  # jpg or png
                shutil.copyfile(img_path, yolo_path + str(data_counter) + '.' + img_format)
                
                # create yolo bndbox txt
                with open(yolo_path + str(data_counter) + '.txt', 'a+', encoding='utf-8') as f:
                    f.write('\n'.join(img_info))

                # create train or val txt
                with open(write_txt, 'a', encoding='utf-8') as f:
                    # path = os.path.join(now_path, yolo_path)
                    path = yolo_path
                    line_txt = [path + str(data_counter) + '.' + img_format, '\n']
                    f.writelines(line_txt)

                data_counter += 1
                    
        except Exception as e:
            print(e)
           
    print('the file is processed')


all_classes = {'ear': 0}

train_img = "train/images/"
train_annotation = "train/annotations/"
yolo_path = "yolo_train/"
write_txt = 'train.txt'

# train_img = "val/images/"
# train_annotation = "val/annotations/"
# yolo_path = "yolo_val/"
# write_txt = 'val.txt'

cfg_file = write_txt.split('/')[0]
if not os.path.exists(cfg_file):
    os.mkdir(cfg_file)

file=open(write_txt, 'w', encoding='utf-8')

run_convert(all_classes, train_img, train_annotation, yolo_path, write_txt)