# coding=utf-8

import os
import re


def findStr(string, subStr, findCnt):
    """ 查找子串第n次出现的位置 """
    listStr = string.split(subStr, findCnt)
    if len(listStr) <= findCnt:
        return -1
    return len(string) - len(listStr[-1]) - len(subStr)


def text_interception(inpath, outpath):
    """ 删除日志文件前面的时间等多余文本 """
    with open(outpath, "w", encoding="utf-8") as fout:
        with open(inpath, "r", encoding="utf-8") as fin:
            sub = ":"
            for line in fin:
                index = findStr(line, sub, 3) + 1
                ret = line[index:]
                fout.write(ret.strip() + '\n')


def is_valid(string):
    """ 判断是否包含需要排除的字段 """
    exclude_list = ["Heart", "Login"]
    for item in exclude_list:
        if item in string:
            return False

    return True


def receive_extract(inpath, outpath):
    """ 提取 receive data """
    with open(outpath, "w", encoding="utf-8") as fout:
        with open(inpath, "r", encoding="utf-8") as fin:
            start = "receive data"
            end = "}"
            flag = False
            jsonstr = ""
            for line in fin:
                if start in line:
                    flag = True
                    jsonstr = ("{\n")
                    continue

                if end == line.strip():
                    flag = False
                    jsonstr += "}\n\n"
                    if is_valid(jsonstr):
                        fout.write(jsonstr)
                    continue

                if "Caller" in line:
                    continue

                if True == flag:
                    jsonstr = jsonstr + "    " + line


if __name__ == '__main__':
    root_dir = os.path.dirname(os.path.abspath(__file__))
    inpath = os.path.join(root_dir, "200716-093708logcat.txt")
    outpath = os.path.join(root_dir, "out.log")
    text_interception(inpath, outpath)

    inpath = outpath
    outpath = os.path.join(root_dir, "result.json")
    receive_extract(inpath, outpath)
