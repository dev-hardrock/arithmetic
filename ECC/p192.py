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


# 私钥通过取随机数得到
def P192_public_key_test():
    """
    Private key: 07915f86918ddc27005df1d6cf0c142b625ed2eff4a518ff
    Public key (X): 15207009984421a6586f9fc3fe7e4329d2809ea51125f8ed
    Public key (Y): b09d42b81bc5bd009f79e4b59dbbaa857fca856fb9f7ea25
    """
    curve = ECC_P192
    private_key = 0x07915f86918ddc27005df1d6cf0c142b625ed2eff4a518ff
    public_key = curve.mult(private_key, curve.g)
    public_key_x = public_key[0]
    public_key_y = public_key[1]
    print(hex(public_key_x))
    print(hex(public_key_y))


# 私钥通过取随机数得到
def P192_data_set_1():
    """
    P-192 data set 1
    Private A: 07915f86 918ddc27 005df1d6 cf0c142b 625ed2ef f4a518ff
    Private B: 1e636ca790b50f68f15d8dbe86244e309211d635de00e16d
    Public A(x): 15207009984421a6586f9fc3fe7e4329d2809ea51125f8ed
    Public A(y): b09d42b81bc5bd009f79e4b59dbbaa857fca856fb9f7ea25
    DHKey: fb3ba2012c7e62466e486e229290175b4afebc13fdccee46
    :return:
    """
    curve = ECC_P192
    Private_A = 0x07915f86918ddc27005df1d6cf0c142b625ed2eff4a518ff
    Private_B = 0x1e636ca790b50f68f15d8dbe86244e309211d635de00e16d
    Public_Ax = 0x15207009984421a6586f9fc3fe7e4329d2809ea51125f8ed
    Public_Ay = 0xb09d42b81bc5bd009f79e4b59dbbaa857fca856fb9f7ea25

    dhkey_x, dhkey_y = curve.mult(Private_B, (Public_Ax, Public_Ay))
    print(sys._getframe().f_code.co_name, ":", hex(dhkey_x))


def P192_data_set_2():
    """
    P-192 data set 2
    Private A: 52ec1ca6e0ec973c29065c3ca10be80057243002f09bb43e
    Private B: 57231203533e9efe18cc622fd0e34c6a29c6e0fa3ab3bc53
    Public A(x): 45571f027e0d690795d61560804da5de789a48f94ab4b07e
    Public A(y): 0220016e8a6bce74b45ffec1e664aaa0273b7cbd907a8e2b
    DHKey: a20a34b5497332aa7a76ab135cc0c168333be309d463c0c0
    :return:
    """
    curve = ECC_P192
    Private_A = 0x52ec1ca6e0ec973c29065c3ca10be80057243002f09bb43e
    Private_B = 0x57231203533e9efe18cc622fd0e34c6a29c6e0fa3ab3bc53
    Public_Ax = 0x45571f027e0d690795d61560804da5de789a48f94ab4b07e
    Public_Ay = 0x0220016e8a6bce74b45ffec1e664aaa0273b7cbd907a8e2b

    dhkey_x, dhkey_y = curve.mult(Private_B, (Public_Ax, Public_Ay))
    print(sys._getframe().f_code.co_name, ":", hex(dhkey_x))


def P192_data_set_3():
    """
    P-192 data set 3
    Private A: 00a0df08eaf51e6e7be519d67c6749ea3f4517cdd2e9e821
    Private B: 2bf5e0d1699d50ca5025e8e2d9b13244b4d322a328be1821
    Public A(x): 2ed35b430fa45f9d329186d754eeeb0495f0f653127f613d
    Public A(y): 27e08db74e424395052ddae7e3d5a8fecb52a8039b735b73
    DHKey: 3b3986ba70790762f282a12a6d3bcae7a2ca01e25b87724e
    :return:
    """
    curve = ECC_P192
    Private_A = 0x00a0df08eaf51e6e7be519d67c6749ea3f4517cdd2e9e821
    Private_B = 0x2bf5e0d1699d50ca5025e8e2d9b13244b4d322a328be1821
    Public_Ax = 0x2ed35b430fa45f9d329186d754eeeb0495f0f653127f613d
    Public_Ay = 0x27e08db74e424395052ddae7e3d5a8fecb52a8039b735b73

    dhkey_x, dhkey_y = curve.mult(Private_B, (Public_Ax, Public_Ay))
    print(sys._getframe().f_code.co_name, ":", hex(dhkey_x))


def P192_data_set_4():
    """
    P-192 data set 4
    Private A: 030a4af66e1a4d590a83e0284fca5cdf83292b84f4c71168
    Private B: 12448b5c69ecd10c0471060f2bf86345c5e83c03d16bae2c
    Public A(x): f24a6899218fa912e7e4a8ba9357cb8182958f9fa42c968c
    Public A(y): 7c0b8a9ebe6ea92e968c3a65f9f1a9716fe826ad88c97032
    DHKey: 4a78f83fba757c35f94abea43e92effdd2bc700723c61939
    :return:
    """
    curve = ECC_P192
    Private_A = 0x030a4af66e1a4d590a83e0284fca5cdf83292b84f4c71168
    Private_B = 0x12448b5c69ecd10c0471060f2bf86345c5e83c03d16bae2c
    Public_Ax = 0xf24a6899218fa912e7e4a8ba9357cb8182958f9fa42c968c
    Public_Ay = 0x7c0b8a9ebe6ea92e968c3a65f9f1a9716fe826ad88c97032

    dhkey_x, dhkey_y = curve.mult(Private_B, (Public_Ax, Public_Ay))
    print(sys._getframe().f_code.co_name, ":", hex(dhkey_x))


def P192_data_set_5():
    """
    P-192 data set 5
    Private A: 604df406c649cb460be16244589a40895c0db7367dc11a2f
    Private B: 526c2327303cd505b9cf0c012471902bb9e842ce32b0addc
    Public A(x): cbe3c629aceb41b73d475a79fbfe8c08cdc80ceec00ee7c9
    Public A(y): f9f70f7ae42abda4f33af56f7f6aa383354e453fa1a2bd18
    DHKey: 64d4fe35567e6ea0ca31f947e1533a635436d4870ce88c45
    :return:
    """
    curve = ECC_P192
    Private_A = 0x604df406c649cb460be16244589a40895c0db7367dc11a2f
    Private_B = 0x526c2327303cd505b9cf0c012471902bb9e842ce32b0addc
    Public_Ax = 0xcbe3c629aceb41b73d475a79fbfe8c08cdc80ceec00ee7c9
    Public_Ay = 0xf9f70f7ae42abda4f33af56f7f6aa383354e453fa1a2bd18

    dhkey_x, dhkey_y = curve.mult(Private_B, (Public_Ax, Public_Ay))
    print(sys._getframe().f_code.co_name, ":", hex(dhkey_x))


def P192_data_set_6():
    """
    P-192 data set 6
    Private A: 1a2c582a09852979eb2cee18fb0befb9a55a6d06f6a8fad3
    Private B: 243778916920d68df535955bc1a3cccd5811133a8205ae41
    Public A(x): eca2d8d30bbef3ba8b7d591fdb98064a6c7b870cdcebe67c
    Public A(y): 2e4163a44f3ae26e70dae86f1bf786e1a5db5562a8ed9fee
    DHKey: 6433b36a7e9341940e78a63e31b3cf023282f7f1e3bf83bd
    :return:
    """
    curve = ECC_P192
    Private_A = 0x1a2c582a09852979eb2cee18fb0befb9a55a6d06f6a8fad3
    Private_B = 0x243778916920d68df535955bc1a3cccd5811133a8205ae41
    Public_Ax = 0xeca2d8d30bbef3ba8b7d591fdb98064a6c7b870cdcebe67c
    Public_Ay = 0x2e4163a44f3ae26e70dae86f1bf786e1a5db5562a8ed9fee

    dhkey_x, dhkey_y = curve.mult(Private_B, (Public_Ax, Public_Ay))
    print(sys._getframe().f_code.co_name, ":", hex(dhkey_x))


def P192_data_set_7():
    """
    P-192 data set 7
    Private A: 0f494dd08b493edb07228058a9f30797ff147a5a2adef9b3
    Private B: 2da4cd46d9e06e81b1542503f2da89372e927877becec1be
    Public A(x): 9f56a8aa27346d66652a546abacc7d69c17fd66e0853989f
    Public A(y): d7234c1464882250df7bbe67e0fa22aae475dc58af0c4210
    DHKey: c67beda9baf3c96a30616bf87a7d0ae704bc969e5cad354b
    :return:
    """
    curve = ECC_P192
    Private_A = 0x0f494dd08b493edb07228058a9f30797ff147a5a2adef9b3
    Private_B = 0x2da4cd46d9e06e81b1542503f2da89372e927877becec1be
    Public_Ax = 0x9f56a8aa27346d66652a546abacc7d69c17fd66e0853989f
    Public_Ay = 0xd7234c1464882250df7bbe67e0fa22aae475dc58af0c4210

    dhkey_x, dhkey_y = curve.mult(Private_B, (Public_Ax, Public_Ay))
    print(sys._getframe().f_code.co_name, ":", hex(dhkey_x))


def P192_data_set_8():
    """
    P-192 data set 8
    Private A: 7381d2bc6ddecb65126564cb1af6ca1985d19fb57f0fff16
    Private B: 18e276beff75adc3d520badb3806822e1c820f1064447848
    Public A(x): 61c7f3c6f9e09f41423dce889de1973d346f2505a5a3b19b
    Public A(y): 919972ff4cd6aed8a4821e3adc358b41f7be07ede20137df
    DHKey: 6931496eef2fcfb03e0b1eef515dd4e1b0115b8b241b0b84
    :return:
    """
    curve = ECC_P192
    Private_A = 0x7381d2bc6ddecb65126564cb1af6ca1985d19fb57f0fff16
    Private_B = 0x18e276beff75adc3d520badb3806822e1c820f1064447848
    Public_Ax = 0x61c7f3c6f9e09f41423dce889de1973d346f2505a5a3b19b
    Public_Ay = 0x919972ff4cd6aed8a4821e3adc358b41f7be07ede20137df

    dhkey_x, dhkey_y = curve.mult(Private_B, (Public_Ax, Public_Ay))
    print(sys._getframe().f_code.co_name, ":", hex(dhkey_x))


def P192_data_set_9():
    """
    P-192 data set 9
    Private A: 41c7b484ddc37ef6b7952c379f87593789dac6e4f3d8d8e6
    Private B: 33e4eaa77f78216e0e99a9b200f81d2ca20dc74ad62d9b78
    Public A(x): 9f09c773adb8e7b66b5d986cd15b143341a66d824113c15f
    Public A(y): d2000a91738217ab8070a76c5f96c03de317dfab774f4837
    DHKey: a518f3826bb5fa3d5bc37da4217296d5b6af51e5445c6625
    :return:
    """
    curve = ECC_P192
    Private_A = 0x41c7b484ddc37ef6b7952c379f87593789dac6e4f3d8d8e6
    Private_B = 0x33e4eaa77f78216e0e99a9b200f81d2ca20dc74ad62d9b78
    Public_Ax = 0x9f09c773adb8e7b66b5d986cd15b143341a66d824113c15f
    Public_Ay = 0xd2000a91738217ab8070a76c5f96c03de317dfab774f4837

    dhkey_x, dhkey_y = curve.mult(Private_B, (Public_Ax, Public_Ay))
    print(sys._getframe().f_code.co_name, ":", hex(dhkey_x))


def P192_data_set_10():
    """
    P-192 data set 10
    Private A: 703cf5ee9c075f7726d0bb36d131c664f5534a6e6305d631
    Private B: 757291c620a0e7e9dd13ce09ceb729c0ce1980e64d569b5f
    Public A(x): fa2b96d382cf894aeeb0bd985f3891e655a6315cd5060d03
    Public A(y): f7e8206d05c7255300cc56c88448158c497f2df596add7a2
    DHKey: 12a3343bb453bb5408da42d20c2d0fcc18ff078f56d9c68c
    :return:
    """
    curve = ECC_P192
    Private_A = 0x703cf5ee9c075f7726d0bb36d131c664f5534a6e6305d631
    Private_B = 0x757291c620a0e7e9dd13ce09ceb729c0ce1980e64d569b5f
    Public_Ax = 0xfa2b96d382cf894aeeb0bd985f3891e655a6315cd5060d03
    Public_Ay = 0xf7e8206d05c7255300cc56c88448158c497f2df596add7a2

    dhkey_x, dhkey_y = curve.mult(Private_B, (Public_Ax, Public_Ay))
    print(sys._getframe().f_code.co_name, ":", hex(dhkey_x))












ECC_P192 = EllipticCurve(
    p=6277101735386680763835789423207666416083908700390324961279,
    a=-3,
    b=0x64210519e59c80e70fa7e9ab72243049feb8deecc146b9b1,
    g=(0x188da80eb03090f67cbf20eb43a18800f4ff0afd82ff1012,
        0x07192b95ffc8da78631011ed6b24cdd573f977a11e794811),
    n=6277101735386680763835789423176059013767194773182842284081,
)

if __name__ == '__main__':
    # P192_public_key_test()
    P192_data_set_1()
    P192_data_set_2()
    P192_data_set_3()
    P192_data_set_4()
    P192_data_set_5()
    P192_data_set_6()
    P192_data_set_7()
    P192_data_set_8()
    P192_data_set_9()
    P192_data_set_10()
