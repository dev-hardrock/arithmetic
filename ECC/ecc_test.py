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


def gcd(a, b):
    if a < b:
        return gcd(b, a)
    while a % b != 0:
        temp = b
        b = a % b
        a = temp
    return b


# 根据费马小定理求解分式的逆元
def inverse_mod(n, p):
    """
    p为素数，且 n 和 p 互质， 则  n**(p -1) = 1 (mod p), 即 n * n **（p-2） = 1 (mod p)
    a/b (mod p) = a/b * 1 (mod p) = a/b * b * b ** ( p - 2) (mod p) = a*b**(p-2) mod p
    这里传的是b和p的值，return b**(p-2) mod p

    此方法对大数计算，精准度不够，需要改用扩展欧几里得法求解。

    :param n:
    :param p:
    :return:
    """
    assert gcd(abs(n), abs(p)) == 1
    return n ** (p - 2) % p


if __name__ == "__main__":
    g = 3, 6
    curve = EllipticCurve(97, 2, 3, g, 5)
    result = curve.mult(1, g)
    print(result)
    result = curve.mult(2, g)
    print(result)
    result = curve.mult(3, g)
    print(result)
    result = curve.mult(4, g)
    print(result)
    result = curve.mult(5, g)
    print(result)

