import csv

wfile=r'E:\hongxing1\result0808_1.txt'
vfile=r'E:\hongxing1\result0808.csv'

with open(vfile, 'w', newline='') as csvfile:
    spamwriter = csv.writer(csvfile, dialect='excel')
    # 读要转换的txt文件，文件每行各词间以\t字符分隔
    with open(wfile, 'r') as filein:
        for line in filein:
            line_list = line.strip('\n').split('\t')
            # line_list = line.split('\t')
            spamwriter.writerow(line_list)

print("Write to CSV successfully")