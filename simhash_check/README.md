# npl_text_tools

text_simhash_check.py 

这个程序是用于在一个目录下查找所有的txt文件，并计算它们的Simhash值。Simhash是一种用于文本相似性比较的算法，能够对文本内容进行哈希运算，得到一个数字表示文本内容的特征。

程序运行时需要输入一个目录路径作为参数。它会递归地遍历该目录及其子目录中的所有txt文件，读取文件内容并计算Simhash值。同时，在读取文件时会检测文件的编码，并将其转换为UTF-8编码。

计算完所有文件的Simhash值后，程序会构建一个SimhashIndex对象，用于存储文件路径和对应的Simhash值。SimhashIndex是一个类似于字典的对象，可以通过Simhash值来查找对应的文件路径。

程序最后会输出所有相似的文件路径。具体地，程序会遍历SimhashIndex中所有的文件路径，对于每个文件，它会查找与其相似的所有文件，并将它们的路径输出到控制台。输出的顺序是按照相似文件数量从多到少排序的。

这个程序使用了第三方库cchardet来检测文件编码，并使用了进度条库progress.bar来显示处理进度。


安装依赖库
```
pip install cchardet simhash progress 
```
运行
```
python text_simhash_check.py ./ 
```
