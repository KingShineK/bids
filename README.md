# bids
招标数据提取
主要对千里马招标网进行爬取的数据，已经测试了10000个文件的数据提取，字段提取准确率达到80%
read.py：遍历文件夹下的所有文件，进行数据的预提取，将数据保存在一个txt文件中
bid6.py：对read.py生成的数据进行精提取
to_csv.py：将最后结果csv格式转换为excel格式