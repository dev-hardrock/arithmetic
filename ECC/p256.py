import sys


class EllipticCurve:
    """
    ECC 加密算法测试代码
    """

    def __init__(self, p, a, b, g, n):
        """
        初始化椭圆曲线函数
        :param p: 素模P
        :param a:
        :param b:
        :param g: 椭圆曲线上的基点
        :param n: g的阶数
        """
        self.p = p
        self.a = a
        self.b = b
        self.g = g
        self.n = n

        assert pow(2, p - 1, p) == 1   # 判断 2**(p-1) % p == 1
        assert (4 * a ** 3 + 27 * b ** 2) % p != 0  # 排除奇异曲线
        assert self.is_on_curve(g)      # 判断g点是否在曲线上
        assert self.mult(n, g) is None   # 判断 np == 0

    def is_on_curve(self, dot):
        """
        检查 点dot是否在曲线E上
        :param dot: 点的坐标（x，y）
        :return:
        """
        if dot is None:
            return True     # 单位元 0
        x, y = dot
        return (y ** 2 - x ** 3 - self.a * x - self.b) % self.p == 0

    def add(self, dot1, dot2):
        """
        根据公式：
            P != Q  时
                m = （(Y1 - Y2）/(X1 - X2)) mod p
            P == Q 时
                m = (( 3 * X1^2 + a ) / (2 * Y1)) mod p
            X = (m^2 - X1 - X2) mod p
            Y = (Y1 + m * (X - X1)) mod p
        :param dot1:
        :param dot2:
        :return:
        """
        if dot1 is None:
            return dot2
        if dot2 is None:
            return dot1

        x1, y1 = dot1
        x2, y2 = dot2

        if x1 == x2 and y1 != y2:
            return None

        if x1 == x2:
            m = (3 * x1 ** 2 + self.a) * inverse_mod(2 * y1, self.p)
        else:
            m = (y1 - y2) * inverse_mod(x1 - x2, self.p)

        # P + Q + R = 0, -P = Q + R , P 和 -P 关于x轴对称。
        x3 = (m ** 2 - x1 - x2)
        y3 = (y1 + m * (x3 - x1))
        return x3 % self.p, -y3 % self.p

    def double(self, dot):
        return self.add(dot, dot)

    def neg(self, dot):
        """Returns -point."""
        if dot is None:
            return None

        x, y = dot
        result = x, -y % self.p

        assert self.is_on_curve(result)

        return result

    def mult(self, n, dot):
        """
        计算点dot的n倍点，使用椭圆曲线的加法定义计算。
        :param n:
        :param dot:
        :return:
        """
        # if n = k * self.n，  则 n * p = k * self.n * p  = K * 0 = 0
        if n % self.n == 0 or dot is None:
            return None
        if n < 0:
            return self.neg(self.mult(-n, dot))

        result = None
        addend = dot

        while n:
            if n & 1:
                result = self.add(result, addend)
            addend = self.double(addend)
            n >>= 1

        return result


def inverse_mod(n, p):
    """Returns the inverse of n modulo p.

    This function returns the only integer x such that (x * n) % p == 1.

    n must be non-zero and p must be a prime.
    """
    if n == 0:
        raise ZeroDivisionError('division by zero')
    if n < 0:
        return p - inverse_mod(-n, p)

    s, old_s = 0, 1
    t, old_t = 1, 0
    r, old_r = p, n

    while r != 0:
        quotient = old_r // r
        old_r, r = r, old_r - quotient * r
        old_s, s = s, old_s - quotient * s
        old_t, t = t, old_s - quotient * t

    gcd, x, y = old_r, old_s, old_t

    assert gcd == 1
    assert (n * x) % p == 1

    return x % p


def P256_public_key_generate():
    """
    Private A: 3f49f6d4 a3c55f38 74c9b3e3 d2103f50 4aff607b eb40b799 5899b8a6 cd3c1abd
    Private B: 55188b3d 32f6bb9a 900afcfb eed4e72a 59cb9ac2 f19d7cfb 6b4fdd49 f47fc5fd
    Public A(x): 20b003d2 f297be2c 5e2c83a7 e9f9a5b9 eff49111 acf4fddb cc030148 0e359de6
    Public A(y): dc809c49 652aeb6d 63329abf 5a52155c 766345c2 8fed3024 741c8ed0 1589d28b
    Public B(x): 1ea1f0f0 1faf1d96 09592284 f19e4c00 47b58afd 8615a69f 559077b2 2faaa190
    Public B(y): 4c55f33e 429dad37 7356703a 9ab85160 472d1130 e28e3676 5f89aff9 15b1214a
    DHKey: ec0234a3 57c8ad05 341010a6 0a397d9b 99796b13 b4f866f1 868d34f3 73bfa698
    :return:
    """
    curve = ECC_P256
    Private_A = 0x3f49f6d4a3c55f3874c9b3e3d2103f504aff607beb40b7995899b8a6cd3c1abd
    Private_B = 0x55188b3d32f6bb9a900afcfbeed4e72a59cb9ac2f19d7cfb6b4fdd49f47fc5fd
    Public_Ax = 0x20b003d2f297be2c5e2c83a7e9f9a5b9eff49111acf4fddbcc0301480e359de6
    Public_Ay = 0xdc809c49652aeb6d63329abf5a52155c766345c28fed3024741c8ed01589d28b

    Public_Ax, Public_Ay = curve.mult(Private_A, curve.g)
    Public_Bx, Public_By = curve.mult(Private_B, curve.g)
    print(sys._getframe().f_code.co_name, ":", hex(Public_Ax), hex(Public_Ay))
    print(sys._getframe().f_code.co_name, ":", hex(Public_Bx), hex(Public_By))


def P256_data_set_1():
    """
    Private A: 3f49f6d4 a3c55f38 74c9b3e3 d2103f50 4aff607b eb40b799 5899b8a6 cd3c1abd
    Private B: 55188b3d 32f6bb9a 900afcfb eed4e72a 59cb9ac2 f19d7cfb 6b4fdd49 f47fc5fd
    Public A(x): 20b003d2 f297be2c 5e2c83a7 e9f9a5b9 eff49111 acf4fddb cc030148 0e359de6
    Public A(y): dc809c49 652aeb6d 63329abf 5a52155c 766345c2 8fed3024 741c8ed0 1589d28b
    Public B(x): 1ea1f0f0 1faf1d96 09592284 f19e4c00 47b58afd 8615a69f 559077b2 2faaa190
    Public B(y): 4c55f33e 429dad37 7356703a 9ab85160 472d1130 e28e3676 5f89aff9 15b1214a
    DHKey: ec0234a3 57c8ad05 341010a6 0a397d9b 99796b13 b4f866f1 868d34f3 73bfa698
    :return:
    """
    curve = ECC_P256
    Private_A = 0x3f49f6d4a3c55f3874c9b3e3d2103f504aff607beb40b7995899b8a6cd3c1abd
    Private_B = 0x55188b3d32f6bb9a900afcfbeed4e72a59cb9ac2f19d7cfb6b4fdd49f47fc5fd
    Public_Ax = 0x20b003d2f297be2c5e2c83a7e9f9a5b9eff49111acf4fddbcc0301480e359de6
    Public_Ay = 0xdc809c49652aeb6d63329abf5a52155c766345c28fed3024741c8ed01589d28b

    Public_Bx = 0x1ea1f0f01faf1d9609592284f19e4c0047b58afd8615a69f559077b22faaa190
    Public_By = 0x4c55f33e429dad377356703a9ab85160472d1130e28e36765f89aff915b1214a
    DHKey_Ax, DHKey_Ay = curve.mult(Private_A, (Public_Bx, Public_By))
    DHKey_Bx, DHKey_By = curve.mult(Private_B, (Public_Ax, Public_Ay))
    print(sys._getframe().f_code.co_name, ":", hex(DHKey_Ax), hex(DHKey_Ay))
    print(sys._getframe().f_code.co_name, ":", hex(DHKey_Bx), hex(DHKey_By))


def P256_data_set_2():
    """
    Private A: 06a51669 3c9aa31a 6084545d 0c5db641 b48572b9 7203ddff b7ac73f7 d0457663
    Private B: 529aa067 0d72cd64 97502ed4 73502b03 7e8803b5 c60829a5 a3caa219 505530ba
    Public A(x): 2c31a47b 5779809e f44cb5ea af5c3e43 d5f8faad 4a8794cb 987e9b03 745c78dd
    Public A(y): 91951218 3898dfbe cd52e240 8e43871f d0211091 17bd3ed4 eaf84377 43715d4f
    Public B(x): f465e43f f23d3f1b 9dc7dfc0 4da87581 84dbc966 204796ec cf0d6cf5 e16500cc
    Public B(y): 0201d048 bcbbd899 eeefc424 164e33c2 01c2b010 ca6b4d43 a8a155ca d8ecb279
    DHKey: ab85843a 2f6d883f 62e5684b 38e30733 5fe6e194 5ecd1960 4105c6f2 3221eb69
    :return:
    """
    curve = ECC_P256
    Private_A = 0x06a516693c9aa31a6084545d0c5db641b48572b97203ddffb7ac73f7d0457663
    Private_B = 0x529aa0670d72cd6497502ed473502b037e8803b5c60829a5a3caa219505530ba

    Public_Ax, Public_Ay = curve.mult(Private_A, curve.g)
    Public_Bx, Public_By = curve.mult(Private_B, curve.g)

    DHKey_Ax, DHKey_Ay = curve.mult(Private_A, (Public_Bx, Public_By))
    DHKey_Bx, DHKey_By = curve.mult(Private_B, (Public_Ax, Public_Ay))
    print(sys._getframe().f_code.co_name, ":", hex(DHKey_Ax), hex(DHKey_Ay))
    print(sys._getframe().f_code.co_name, ":", hex(DHKey_Bx), hex(DHKey_By))




# P-256, Spec5.3-Page 992
ECC_P256 = EllipticCurve(
    p=115792089210356248762697446949407573530086143415290314195533631308867097853951,
    a=-3,
    b=0x5ac635d8aa3a93e7b3ebbd55769886bc651d06b0cc53b0f63bce3c3e27d2604b,
    g=(0x6b17d1f2e12c4247f8bce6e563a440f277037d812deb33a0f4a13945d898c296,
        0x4fe342e2fe1a7f9b8ee7eb4a7c0f9e162bce33576b315ececbb6406837bf51f5),
    n=115792089210356248762697446949407573529996955224135760342422259061068512044369,
)


if __name__ == '__main__':
    # P256_public_key_generate()
    P256_data_set_1()
    P256_data_set_2()
