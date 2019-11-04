#coding=utf-8
import logging
import os
import shutil
import sys

from ffmpy import FFmpeg
from natsort import natsorted

logger = logging.getLogger(__name__)

def video_convert(in_path, out_path):
    FFmpeg(inputs={in_path: None}, outputs={out_path: '-c copy -bsf:v h264_mp4toannexb -f mpegts'}).run()


def execCmd(cmd):
    """
    执行计算命令时间
    """
    r = os.popen(cmd)
    text = r.read().strip()
    r.close()
    return text

def del_path(path):
    if not os.path.exists(path):
        return

    if os.path.isdir(path):
        shutil.rmtree(path)
    elif os.path.isfile(path):
        os.remove(path)


def flv_dir_to_mp4(in_path_dir, out_path_file):
    """
    将flv文件转换为mp4
    法一:(只显示第一段，有问题)
    ffmpeg -safe 0 -f concat -i filelist.txt -c copy out.mp4
    法二:
    ffmpeg -i input1.mp4 -c copy -bsf:v h264_mp4toannexb -f mpegts intermediate1.ts
    ffmpeg -i "concat:1.ts|2.ts|...n.ts" -c copy -absf aac_adtstoasc out.mp4
    """

    tsfile_dir = os.path.join(in_path_dir, 'tsfile')
    del_path(out_path_file)
    del_path(tsfile_dir)

    os.mkdir(tsfile_dir)

    out_files = []

    # 生成中间文件ts
    for root, dirs, files in os.walk(in_path_dir):
            files = natsorted(files)
            for file in files:
                if os.path.splitext(file)[1] == '.flv':
                    file_path = os.path.join(root, file)
                    video_convert(os.path.join(root, file), os.path.join(tsfile_dir, os.path.splitext(file)[0] + '.ts'))

    # 获取列表参数
    for root, dirs, files in os.walk(tsfile_dir):
            files = natsorted(files)
            for file in files:
                if os.path.splitext(file)[1] == '.ts':
                    file_path = os.path.join(root, file)
                    out_files.append(file_path)

    cmd = '|'.join(out_files)
    print(out_files)
    cmd = 'concat:' + "\"" + cmd + "\""
    cmd = 'ffmpeg -i ' + cmd + ' -c copy -absf aac_adtstoasc -movflags faststart ' + out_path_file
    # cmd = 'ffmpeg -i ' + cmd + ' -safe 0 -segment_time_metadata 1 -vf select=concatdec_select -af aselect=concatdec_select,aresample=async=1 ' + out_path_file
    # print(cmd)
    print(execCmd(cmd))


if __name__ == '__main__':
    print('sys argv', sys.argv)
    if len(sys.argv) == 3:
        flv_dir_to_mp4(sys.argv[1], sys.argv[2])
    elif len(sys.argv) == 2:
        flv_dir_to_mp4(sys.argv[1], os.path.join(sys.argv[1], 'out.mp4'))
    else:
        root_dir = os.path.dirname(os.path.abspath(__file__))
        flv_dir_to_mp4(root_dir, os.path.join(root_dir, 'out.mp4'))
