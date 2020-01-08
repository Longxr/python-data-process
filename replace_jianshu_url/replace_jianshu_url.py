import imghdr
import os
import re
import shutil

import requests

## 用户名
user_name = 'Longxr';
## 仓库名
github_repository = 'PicStored';
## 存放图片的git文件夹路径
git_images_folder = 'F:/workspace/GithubCode/PicStored/blog'

# 设置用户代理头
headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36'
}

# 获取当前目录下所有md文件
def get_md_files(md_dir):
    md_files = [];
    for root, dirs, files in sorted(os.walk(md_dir)):
        for file in files:
            # 获取.md结尾的文件
            if(file.endswith('.md')):
                file_path = os.path.join(root, file)
                print(file_path)
                #忽略排除目录
                need_append = 0
                for ignore_dir in ignore_dir_list:
                    if(ignore_dir in file_path.split('/') == True):
                        need_append = 1
                if(need_append == 0):
                    md_files.append(file_path)
    return md_files

# 获取网络图片
def get_http_image(image_url, file_new_name):
    image_info = {'image_url': '', 'new_image_url': ''}
    image_data = requests.get(image_url.split('?')[0], headers=headers).content
    # 创建临时文件
    tmp_new_image_path_and_name = os.path.join(git_images_folder, file_new_name)
    with open(tmp_new_image_path_and_name, 'wb+') as f:
        f.write(image_data)
    img_type = imghdr.what(tmp_new_image_path_and_name)
    if(img_type == None):
        img_type = ''
    else:
        img_type = '.'+img_type
    # 生成新的名字加后缀
    new_image_path_and_name = tmp_new_image_path_and_name+img_type
    # 重命名图片
    os.rename(tmp_new_image_path_and_name, new_image_path_and_name)
    new_image_url = 'https://cdn.jsdelivr.net/gh/'+ user_name + '/' +github_repository+'/blog/'+ file_new_name + img_type
    image_info = {
        'image_url': image_url,
        'new_image_url': new_image_url
    }
    print('image_info', image_info)

    return image_info


# 获取本地图片
def get_local_image(image_url, file_new_name):
    image_info = {'image_url': '', 'new_image_url': ''}
    try:
        # 获取图片类型
        img_type = image_url.split('.')[-1]
        # 新的图片名和文件后缀
        image_name = file_new_name +'.'+ img_type
        # 新的图片路径和名字
        new_image_path_and_name = os.path.join(git_images_folder, image_name);
        shutil.copy(image_url, new_image_path_and_name)
        # 生成url
        new_image_url = 'https://cdn.jsdelivr.net/gh/'+ user_name + '/' +github_repository+'/blog/'+ file_new_name + img_type
        # 图片信息
        image_info = {
            'image_url': image_url,
            'new_image_url': new_image_url
        }
        print(image_info)
        return image_info
    except Exception as e:
        print(e)

    return image_info
    
# 爬取单个md文件内的图片
def get_images_from_md_file(md_file):
    md_content = ''
    image_info_list = []
    md_file_name = os.path.splitext(os.path.basename(md_file))[0]
    url_index = 0

    with open(md_file, 'r', encoding='UTF-8') as f:
        md_content = f.read()
        image_urls = re.findall(r'!\[.*?\]\((.*?)\)', md_content)
        for image_url in image_urls:
            url_index += 1
            image_new_name_without_type = md_file_name + '_%02d'%url_index

            # 处理本地图片
            if(image_url.startswith('http') == False):
                image_info = get_local_image(image_url, image_new_name_without_type)
                image_info_list.append(image_info)
            # 处理网络图片
            else:
                # 只爬取简书的
                if(image_url.startswith('https://upload-images.jianshu.io')):
                    try:
                        image_info = get_http_image(image_url, image_new_name_without_type)
                        image_info_list.append(image_info)
                    except Exception as e:
                        print(image_url, 'Unable to crawl, skip!')
                        pass
        for image_info in image_info_list:
            md_content = md_content.replace(image_info['image_url'], image_info['new_image_url'])

    with open(md_file, 'w+', encoding='UTF-8') as f:
        f.write(str(md_content.encode('utf-8').decode('utf-8')))

if __name__ == '__main__':
    if(os.path.exists(git_images_folder)):
        pass
    else:
        os.mkdir(git_images_folder)
    # 获取本目录下所有md文件
    md_files = get_md_files(os.path.dirname(os.path.abspath(__file__)))

    # 将md文件依次爬取
    for md_file in md_files:
      # 爬取单个md文件内的图片
      get_images_from_md_file(md_file)
