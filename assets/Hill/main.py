import numpy as np
import sys


# 判断矩阵是否存在逆矩阵
def judge_inverse_matrix(matrix):
    try:
        np.linalg.inv(matrix)
    except:
        return False
    return True


# 输入列表并转换为矩阵
def inputmatrix():
    row_num = int(input("请输入矩阵的行数："))
    all_list = []
    for i in range(1, row_num + 1):
        row = input(f"请输入加密矩阵第{i}行(以空格为分隔)：")
        if row[0] == ' ':
            print("输入有误，第一位不该为空格")
            sys.exit()
        else:
            row_list = row.split(' ')
        # 将列表中str转换为int
        if len(row_list) == row_num:
            for n in row_list:
                row_list[row_list.index(n)] = int(row_list[row_list.index(n)])
            all_list.append(row_list)
        else:
            print("前后输入的行数不一致,请重修输入")
            break
    encrypt_matrix = np.array(all_list)
    if not judge_inverse_matrix(encrypt_matrix):
        print("该矩阵不存在逆矩阵，请重修输入")
    return encrypt_matrix


# 生成矩阵的逆矩阵。如果逆矩阵含有小数，就四舍五入
def generate_inverse_matrix(matrix):
    inverse_matrix = np.linalg.inv(matrix)
    for row in inverse_matrix:
        for num in row:
            num = round(num)
    print("加密矩阵的逆矩阵为：")
    for array in inverse_matrix:
        print(array)
    return inverse_matrix


# 生成字母-数字对应的字典
def alphabet_number():
    alphabet_number_dict = {}
    for i in range(97, 123):
        alphabet_number_dict[chr(i)] = i % 97
    return alphabet_number_dict


def encrypt():
    # 明文字母转换成对应数字
    input_plaintext = input("请输入明文：")
    num_list = []
    dic = alphabet_number()
    for i in input_plaintext:
        num_list.append(dic[i])

    # 如果矩阵行数不能整除明文，则用'z'的数字25补全
    matrix = inputmatrix()
    row_num = len(matrix)
    supple_num = row_num - (len(num_list) % row_num)
    if len(num_list) % row_num != 0:
        for n in range(1, supple_num + 1):
            num_list.append(25)
    print(f"\n添加了{supple_num}个z补全明文")

    # 分组加密
    group_num = int(len(num_list) / row_num)
    whole_encrypt_num_list = []
    for g in range(0, group_num):
        plaintext_matrix = np.array(num_list[0 + g * row_num: (g + 1) * row_num])
        encrypt_num_list = np.matmul(plaintext_matrix, matrix)
        for num in encrypt_num_list:
            whole_encrypt_num_list.append(num)

    # 将加密后的数字转换为字母
    ciphertext = ""
    for ennum in whole_encrypt_num_list:
        # 对超出范围的数字取模
        if ennum > 25:
            ennum = ennum % 26
        for k in dic:
            if dic[k] == ennum:
                ciphertext = ciphertext + k
    print("加密后密文为：", ciphertext[:-supple_num], '\n')


def decrypt():
    # 输入密文并转换为对应数字
    input_ciphertext = input("请输入密文：")
    num_list2 = []
    dic2 = alphabet_number()
    for i in input_ciphertext:
        num_list2.append(dic2[i])

    # 解密就不添加'z'来补全密文了
    matrix = inputmatrix()
    row_num2 = len(matrix)
    supple_num2 = row_num2 - (len(num_list2) % row_num2)

    # 用逆矩阵分组解密
    inserve_matrix = generate_inverse_matrix(matrix)
    group_num2 = int(len(num_list2) / row_num2)
    whole_decrypt_num_list = []
    for g in range(0, group_num2):
        plaintext_matrix = np.array(num_list2[0 + g * row_num2: (g + 1) * row_num2])
        decrypt_num_list = np.matmul(plaintext_matrix, inserve_matrix)
        for num in decrypt_num_list:
            whole_decrypt_num_list.append(num)

    # 将解密后的数字转换为对应字母
    plaintext = ""
    for denum in whole_decrypt_num_list:
        if denum > 25 or denum < -26:
            denum = denum % 26

        # 防止取模后是负数，字典中找不到对应的字母
        if denum < 0:
            denum = denum + 26
        # 字典中寻找与数字对应的字母
        for k in dic2:
            if dic2[k] == denum:
                plaintext = plaintext + k
    print("解密后明文为：", plaintext, '\n')


if __name__ == '__main__':
    while True:
        print("========Hill密码========\n")
        print("1.加密\n2.解密\n")
        print("注意：如果输入矩阵的逆矩阵中含有小数，采用四舍五入的方法\n")
        pattern = input("请选择模式：")
        if pattern == '1':
            encrypt()
        elif pattern == '2':
            decrypt()
        else:
            print("输入有误，请重修输入")
