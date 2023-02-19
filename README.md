# npl_text_tools

text_similarity_check.py 

是一个文本相似度比较工具，能够对指定目录下的所有文本文件进行相似度计算，并将相似度高于指定阈值的文件路径和相似度保存成 CSV 文件。
程序接受两个命令行参数：目录路径和相似度阈值。其中，目录路径指定了待处理的文本文件所在的目录，相似度阈值用于筛选相似度高于该阈值的文件对。

安装依赖库
```
pip install chardet sklearn pandas argparse
```
运行
```
python text_similarity_check.py ./ 0.6
```

程序使用了以下 Python 库：
```
os：用于遍历目录和文件。
chardet：用于自动检测文本文件编码。
sklearn：用于计算文本相似度。
pandas：用于将结果保存成 CSV 文件。
argparse：用于解析命令行参数。
```

程序的运行流程如下：
```
解析命令行参数，获取目录路径和相似度阈值。
遍历目录及其子目录，获取所有文本文件路径。
对每个文本文件，读取前2000个字符，并使用 chardet 检测文件编码，忽略解码错误。
使用 TfidfVectorizer 处理所有文本文件，得到文档-词条矩阵。
使用 cosine_similarity 计算文本相似度矩阵。
遍历相似度矩阵，将相似度高于指定阈值的文件路径和相似度值存储到字典中。
将字典转换成 DataFrame，并将 DataFrame 保存成 CSV 文件。
最终，程序输出一个 CSV 文件，包含所有相似度高于指定阈值的文件对和相似度值。可以使用 Excel 或其他工具打开该文件，查看结果。
```
