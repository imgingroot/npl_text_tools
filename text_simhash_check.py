import os
import sys
import cchardet
from simhash import Simhash, SimhashIndex
from progress.bar import Bar

"""" 
这个程序是用于在一个目录下查找所有的txt文件，并计算它们的Simhash值。Simhash是一种用于文本相似性比较的算法，能够对文本内容进行哈希运算，得到一个数字表示文本内容的特征。

程序运行时需要输入一个目录路径作为参数。它会递归地遍历该目录及其子目录中的所有txt文件，读取文件内容并计算Simhash值。同时，在读取文件时会检测文件的编码，并将其转换为UTF-8编码。

计算完所有文件的Simhash值后，程序会构建一个SimhashIndex对象，用于存储文件路径和对应的Simhash值。SimhashIndex是一个类似于字典的对象，可以通过Simhash值来查找对应的文件路径。

程序最后会输出所有相似的文件路径。具体地，程序会遍历SimhashIndex中所有的文件路径，对于每个文件，它会查找与其相似的所有文件，并将它们的路径输出到控制台。输出的顺序是按照相似文件数量从多到少排序的。

这个程序使用了第三方库cchardet来检测文件编码，并使用了进度条库progress.bar来显示处理进度。
"""" 

progressbar = Bar('')


# 获取目录下的所有文件路径
def get_file_paths(dir_path):
    file_paths = []
    for root, dirs, files in os.walk(dir_path):
        for file in files:
            if file.lower().endswith('.txt'):
                file_path = os.path.join(root, file)
                file_paths.append(file_path)
    return file_paths


# 读取文件内容并返回Simhash值
def get_simhash(file_path):
    try:
        progressbar.next()
        progressbar.suffix= f'{file_path[-30:]}' 
        with open(file_path, 'rb') as f:
            content = f.read(8192)
            # 检测文件编码并转换为UTF-8编码
            encoding = cchardet.detect(content)['encoding']
            content = content.decode(encoding, errors='ignore')
            # 计算Simhash值
            simhash = Simhash(content)

            return simhash
    except Exception as e:
        print(f'Error reading file {file_path}: {e}')
        return None


# 计算所有文件的Simhash值并构建SimhashIndex
def build_simhash_index(file_paths):
    objs = [(file_path, get_simhash(file_path)) for file_path in file_paths]
    objs = [(file_path, simhash) for file_path, simhash in objs if simhash is not None]
    index = SimhashIndex(objs, k=3)
    return index, objs



if __name__ == '__main__':

    if len(sys.argv) != 2:
        print('Usage: python script.py <dir_path>')
        sys.exit(1)
    dir_path = sys.argv[1]
    file_paths = get_file_paths(dir_path)
    progressbar = Bar('Processing', max=len(file_paths))
    index, objs = build_simhash_index(file_paths)
    progressbar.finish()
    similar_files = {}
    for file_path, simhash in objs:
        similar = index.get_near_dups(simhash)
        if len(similar) > 1:
            similar_files[file_path] = similar

    # 按照相似文件数量从多到少排序输出
    sorted_files = sorted(similar_files.items(), key=lambda x: len(x[1]), reverse=True)
    for file_path, similar in sorted_files:
        print(f"{file_path} has {len(similar)} similar files:")
        for s in similar:
            print(f"\t{s}")

