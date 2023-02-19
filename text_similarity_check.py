import os
import chardet
import argparse
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
"""
这个程序是一个文本相似度比较工具，能够对指定目录下的所有文本文件进行相似度计算，并将相似度高于指定阈值的文件路径和相似度保存成 CSV 文件。

程序接受两个命令行参数：目录路径和相似度阈值。其中，目录路径指定了待处理的文本文件所在的目录，相似度阈值用于筛选相似度高于该阈值的文件对。

pip install chardet sklearn pandas argparse


程序使用了以下 Python 库：

os：用于遍历目录和文件。
chardet：用于自动检测文本文件编码。
sklearn：用于计算文本相似度。
pandas：用于将结果保存成 CSV 文件。
argparse：用于解析命令行参数。
程序的运行流程如下：

解析命令行参数，获取目录路径和相似度阈值。
遍历目录及其子目录，获取所有文本文件路径。
对每个文本文件，读取前2000个字符，并使用 chardet 检测文件编码，忽略解码错误。
使用 TfidfVectorizer 处理所有文本文件，得到文档-词条矩阵。
使用 cosine_similarity 计算文本相似度矩阵。
遍历相似度矩阵，将相似度高于指定阈值的文件路径和相似度值存储到字典中。
将字典转换成 DataFrame，并将 DataFrame 保存成 CSV 文件。
最终，程序输出一个 CSV 文件，包含所有相似度高于指定阈值的文件对和相似度值。可以使用 Excel 或其他工具打开该文件，查看结果。

"""


# 解析命令行参数
parser = argparse.ArgumentParser(description='Find similar text files in a directory.')
parser.add_argument('directory', type=str, help='Directory path')
parser.add_argument('--similarity', type=float, default=0.8, help='Minimum similarity threshold')
args = parser.parse_args()

directory = args.directory  # 目录路径
similarity_threshold = args.similarity  # 相似度阈值
files = []  # 保存所有txt文件的列表

# 遍历目录及其子目录，获取所有txt文件
for root, _, filenames in os.walk(directory):
    for filename in filenames:
        if filename.endswith('.txt'):
            files.append(os.path.join(root, filename))

# 创建一个TfidfVectorizer对象
vectorizer = TfidfVectorizer()

# 使用TfidfVectorizer对象处理所有文本文件
corpus = []
for file in files:
    with open(file, 'rb') as f:
        try:
            raw_data = f.read(2000)
            encoding = chardet.detect(raw_data)['encoding']  # 使用chardet自动检测编码
            text = raw_data.decode(encoding, errors='ignore')[:2000]  # 读取前2000个字符，忽略解码错误
            print(file)
            corpus.append(text)
        except Exception as e:
            print(f"Error reading file {file}: {e}")

# 使用向量化器处理文本，得到文档-词条矩阵
X = vectorizer.fit_transform(corpus)

# 计算文本相似度
similarity_matrix = cosine_similarity(X)

# 遍历相似度矩阵，将相似度高于阈值的文件路径和相似度值存储到字典中
results = {'file1': [], 'file2': [], 'similarity': []}
for i in range(len(files)):
    for j in range(i+1, len(files)):
        if similarity_matrix[i,j] > similarity_threshold:
            results['file1'].append(files[i])
            results['file2'].append(files[j])
            results['similarity'].append(similarity_matrix[i,j])

# 将字典转换成 DataFrame，并将 DataFrame 保存成文件
df = pd.DataFrame(results)
df.to_csv('similar_files.csv', index=False)
