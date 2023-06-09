def inv_mod(n, p):
    if n == 0:
        raise ZeroDivisionError('division by zero')
    if n < 0:
        return p - inv_mod(-n, p)

    s, old_s = 0, 1
    t, old_t = 1, 0
    r, old_r = p, n

    while r != 0:
        quotient = old_r // r
        old_r, r = r, old_r - quotient * r
        old_s, s = s, old_s - quotient * s
        old_t, t = t, old_s - quotient * t
        print(old_r, r)
        print(old_s, s)
        print(old_t, t)

    gcd, x, y = old_r, old_s, old_t
    print(gcd, x, y)



def inv_mod_test():
    """
    对n,p,  存在 mn = kp + 1 ；
    通过辗转相除法求解最大公约数。
    :return:
    """
    n = 11
    p = 26
    inv_mod(n, p)


if __name__ == '__main__':
    inv_mod_test()
