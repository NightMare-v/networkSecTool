import json
from pathlib import Path
from secrets import token_bytes
from typing import Tuple

# 随机生成密钥
def random_key(length:int) -> int:
    key:bytes = token_bytes(nbytes=length)
    key_int:int = int.from_bytes(key, 'big')
    return key_int

# 编码密文
def encrypt(raw:str) -> Tuple[int, int]:
    print('数据为:',raw)   # 测试用打印
    raw_bytes:bytes = raw.encode()
    raw_int:int = int.from_bytes(raw_bytes, 'big')
    key_int:int = random_key(len(raw_bytes))
    # print(raw_int ^ key_int)
    return raw_int ^ key_int, key_int

# 解码密文
def decrypt(encrypted:int, key_int:int) -> str:
    decrypted:int = encrypted ^ key_int
    length = (decrypted.bit_length() + 7) // 8
    decrypted_bytes:bytes = int.to_bytes(decrypted, length, 'big')
    # decrypted_file=decrypted_bytes.decode()
    # print(decrypted_file)
    return decrypted_bytes.decode()

# 文件中读取并调用编码密文
def encrypt_file(path:str, key_path=None, *, encoding='utf-8'):
    path = Path(path)
    cwd = path.cwd() / path.name.split('.')[0]
    path_encrypted = cwd / path.name
    if key_path is None:
        key_path = cwd / 'key'
    if not cwd.exists():
        cwd.mkdir()
        path_encrypted.touch()
        key_path.touch()
    with path.open('rt', encoding=encoding) as f1, \
        path_encrypted.open('wt', encoding=encoding) as f2, \
            key_path.open('wt', encoding=encoding) as f3:
        encrypted, key = encrypt(f1.read())
        print('密文为:',encrypted) # 测试用打印
        print('密钥为:',key)   # 测试用打印
        json.dump(encrypted, f2)
        json.dump(key, f3)

# 文件中得出并存储解码密文（明文）
def decrypt_file(path_encrypted:str, key_path=None, *, encoding='utf-8'):
    path_encrypted = Path(path_encrypted)
    cwd = path_encrypted.cwd()
    path_decrypted = cwd / 'decrypted'
    if not path_decrypted.exists():
        path_decrypted.mkdir()
        path_decrypted /= path_encrypted.name
        path_decrypted.touch()
    if key_path is None:
        key_path = cwd / 'key'
    key_path = cwd.cwd() / path_encrypted.name.split('.')[0] / 'key'
    path_decrypted = cwd / 'decrypted' / path_encrypted.name
    with path_encrypted.open('rt', encoding=encoding) as f1, \
            key_path.open('rt', encoding=encoding) as f2, \
            path_decrypted.open('wt', encoding=encoding) as f3:
        decrypted = decrypt(json.load(f1), json.load(f2))
        print('明文为:',decrypted) # 测试用打印
        f3.write(decrypted)

if __name__ == '__main__':
    encrypt_file('_testText.txt')
    decrypt_file('_testText\_testText.txt','_testText\key')
