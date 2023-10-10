import hashlib

def get_file_md5(f):
    m = hashlib.md5()
    while True:
        #如果不用二进制打开文件，则需要先编码
        #data = f.read(1024).encode('utf-8')
        data = f.read(1024)  #将文件分块读取
        if not data:
            break
        m.update(data)
    return m.hexdigest()

#将file2文件写入改动了一个位数的数据
txt1 = '123456789'
txt2 = '123456789'
with open('1.txt', 'w', encoding='utf-8') as f1, open('2.txt', 'w', encoding='utf-8') as f2:
    f1.write(txt1)
    f2.write(txt2)

with open('1.txt', 'rb') as f1, open('2.txt', 'rb') as f2:
    print('file1:' + txt1)
    print('file2:' + txt2)
    file1_md5 = get_file_md5(f1)
    file2_md5 = get_file_md5(f2)
    print('file1_md5:',file1_md5)
    print('file2_md5:',file2_md5)
    if file1_md5 != file2_md5:
        print('file has changed')
    else:
        print('file not changed')
