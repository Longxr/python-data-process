import os
import re
import string

import pefile


def check_certificate(pefile_path):
    pe = pefile.PE(pefile_path)
    # PE文件头第5个结构体保存证书信息，没有证书的exe结构体中VirtualAddress、Size字段值都为0
    # https://docs.microsoft.com/en-us/windows/win32/debug/pe-format#optional-header-data-directories-image-only
    IMAGE_DIRECTORY_ENTRY_SECURITY = str(pe.OPTIONAL_HEADER.DATA_DIRECTORY[4])
    pattern1 = r'VirtualAddress:\s+0x0\b'
    pattern2 = r'Size:\s+0x0\b'
    if (re.search(pattern1, IMAGE_DIRECTORY_ENTRY_SECURITY) is None and re.search(pattern2, IMAGE_DIRECTORY_ENTRY_SECURITY) is None):
        return True
    else:
        return False


if __name__ == '__main__':
    file_path = "C:\\Program Files\\OpenSSL-Win64\\libcrypto-1_1-x64.dll"
    status = check_certificate(file_path)
    print('{0} {1} certificate!'.format(file_path, "have" if status else "no"))
