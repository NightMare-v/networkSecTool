import random
import re

class RSA:
    def is_prime(self, n):
        '''primality test'''
        if n <= 3:
            return n > 1
        elif (n % 2 == 0) or (n % 3 == 0):
            return False
        i = 5
        while i * i <= n:
            if (n % i == 0) or (n % (i + 2) == 0):
                return False
            i += 6
        return True

    def gcd(self, a, b):
        '''返回a、b的最大公约数'''
        return a if b == 0 else self.gcd(b, a % b)

    def lcm(self, a, b):
        '''返回a、b的最小公倍数'''
        return a // self.gcd(a, b) * b

    def ex_gcd(self, a, b, d, x, y):
        '''
        函数结束时，（x + b) % b为 (a % b)的乘法逆元
        '''
        if b == 0:
            d[0], x[0], y[0] = a, 1, 0
        else:
            self.ex_gcd(b, a % b, d, y, x)
            y[0] -= a // b * x[0]

    def quick_power(self, a, b, mod):
        res = 1
        while b != 0:
            if (b & 1) == 1:
                res = (res * a) % mod
            a = a * a % mod
            b >>= 1
        return res

    def generate(self):
        '''
        Generates a k-bit RSA public/private pair
        @param 
        @returns 返回密钥对
        '''
        p, q = 6007, 360089
        # p、q互质，他来决定了模数n的大小，消息可被转化为不大于n的数加密
        # 其实可以给函数加一个参数，来约束p、q的大小
        lambdan = self.lcm(p - 1, q - 1)
        e = 795479
        while not self.is_prime(e):
            e = random.randint(2, lambdan - 1)
        d = [0]
        self.ex_gcd(e, lambdan, [0], d, [0])
        d = d[0] % lambdan
        print('e:', end='')
        print(e)
        print('d:', end='')
        print(d)
        return {
            'n': p * q,  # public key (part I)
            'e': e,  # public key (part II)
            'd': d,  # private key
        }

    def encrypt(self, m, e, n):
        '''
        明文m，指数e，模数n 
        '''
        c = self.quick_power(m, e, n)
        return c

    def dencypt(self, c, d, n):
        m = self.quick_power(c, d, n)
        return m


if __name__ == "__main__":
    alice = RSA()
    bob = RSA()
    keys = alice.generate()

    # 对于字符的转化
    msg = map(ord,"25f9e")
    # print(list(map(lambda x:str(x),list(msg))))
    msg = list(map(lambda x:str(x-30),list(msg)))
    # print(msg)
    msg = ''.join(msg)
    # print(msg)
    msg = int(msg)

    '''bob使用alice的公钥加秘明文，alice收到密文后使用私钥解密'''
    c = bob.encrypt(m=msg, e=keys['e'], n=keys['n'])
    m = alice.dencypt(c, d=keys['d'], n=keys['n'])
    assert msg == m

    # 对于msg的转化回
    m = re.findall(r'.{2}', str(m))
    m = map(int,m)
    m = map(lambda x:x+30,m)
    m = "".join(map(chr,m))

    print('msg:', end='')
    print(m)
    print('c:', end='')
    print(c)