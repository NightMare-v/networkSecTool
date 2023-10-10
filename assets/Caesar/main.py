def caesar(message):
    message1 = message.upper()  # 把明文字母变成大写
    message1 = list(message1)  # 将明文字符串转换成列表
    list1 = []
    for i in range(len(message1)):
        if message1[i] == ' ':
            list1.append(message1[i])  # 若为空格不用移动
        elif ord(message1[i]) <= 90 - 3 + 1:  # A-X右移三位
            list1.append(chr(ord(message1[i]) + 3))
            result = ''.join(list1)  # 列表转换成字符串
        else:
            list1.append(chr(ord(message1[i]) - (26 - 3)))  # Y和Z回到A、B
            result = ''.join(list1)
    return result

def decaesar(message):
    message1 = message.upper()  # 把明文字母变成大写
    message1 = list(message1)  # 将明文字符串转换成列表
    list1 = []
    for i in range(len(message1)):
        if message1[i] == ' ':
            list1.append(message1[i])  # 若为空格不用移动
        elif ord(message1[i]) <= 90 - 3 + 1:  # A-X右移三位
            list1.append(chr(ord(message1[i]) - 3))
            result = ''.join(list1)  # 列表转换成字符串
        else:
            list1.append(chr(ord(message1[i]) - (26 - 3)))  # Y和Z回到A、B
            result = ''.join(list1)
    return result
def main():
    print('input code:')
    message = input()
    encode_caesar = caesar(message)
    print('encode:',encode_caesar)
    decaesar_ = decaesar(encode_caesar)
    print('decode:',decaesar_)

if __name__ == '__main__':
    main()