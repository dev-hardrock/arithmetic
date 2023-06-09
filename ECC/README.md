# 简单理解ECC加密算法的加解密过程

最近在一些项目中，频繁用到ECC加密算法，但是一直没看懂其中的加解密原理。最近专门花了一些时间，查了很多资料，终于把其中的沟沟道道弄懂了。

网上很多资料都讲述的很全，本文不做过多描述，给大家推荐些资料：

英文原版：[Elliptic Curve Cryptography: a gentle introduction - Andrea Corbellini](https://andrea.corbellini.name/2015/05/17/elliptic-curve-cryptography-a-gentle-introduction/)

翻译的中文版：[椭圆曲线介绍（一）：实数上面的椭圆曲线_AdijeShen的博客-CSDN博客_实数和椭圆曲线转换](https://blog.csdn.net/AdijeShen/article/details/122132389)

但是作为一个软件开发工程师，只需要简单理解这个加密怎么用代码去写，中间的计算逻辑是怎么样的，至于原理是什么，为什么能够保证安全之类的，都不需要理解。只需要记住一下几个概念：

## 椭圆曲线定义

椭圆曲线就是满足下面条件的，曲线上面的所有点构成的一个集合，这种方程形式被叫做维尔斯特拉斯标准形式（Weierstrass normal form）。
$$
\{(x,y)\ \in \ R^2 \ | \ E_p: y^2 = x^3 + ax + b \ (mod \ p) , 4a^3 + 27b^2 \neq 0 \} \ \bigcup \ \{0\}
$$
- p为素数，定义了有限域的大小
- a和b是椭圆曲线等式的参数



**对于椭圆曲线，有如下定义：**

- 椭圆曲线的单位元是 <font color=#dd0000>`0`</font>（定义的无穷远点）；
- 一个点<font color=#dd0000>`P`</font>的逆元<font color=#dd0000>`-P`</font>就是<font color=#dd0000>`P`</font>关于<font color=#dd0000>`X`</font>轴对称的那个点；
- 椭圆曲线加法定义如下：令<font color=#dd0000>`P`</font>，<font color=#dd0000>`Q`</font>，<font color=#dd0000>`R`</font>是一条直线与椭圆曲线的三个交点，则 

$$
P + Q + R = 0 \Rightarrow Q + R = -P
$$

**代数上的加法**

知道了椭圆曲线的计算规则，那么要如何计算呢？ 令：
$$
P = (x_P,y_P), Q = (x_Q,y_Q)
$$
如果<font color=#dd0000>`P`</font>，<font color=#dd0000>`Q`</font>是两个不同点，那么经过他们的直线的斜率为：
$$
m = \frac{(y_P-y_Q)}{(x_P-x_Q)}
$$
他们与椭圆曲线的交点的坐标为<font color=#dd0000>`R`</font>:
$$
\begin{aligned}  
& x_R = m^2 - x_P - x_Q \\
& y_R = y_p + m(x_R - x_P) \\
& or \\
& y_R = y_Q + m(x_R - x_Q)
\end{aligned}
$$
如果 <font color=#dd0000>`P`</font>=<font color=#dd0000>`Q`</font>，则计算方法为：
$$
\begin{aligned}
& m  = \frac{3x_P^2+a}{2y_P} \\
& x_R = m^2 - 2x_P \\
& y_R = y_P + m(x_R - x_P)
\end{aligned}
$$
**标量乘法**

椭圆曲线上没有定义点和点之间的乘法，只有标量乘法，而标量乘法是通过加法来实现的：
$$
nP = \underbrace{P + P + ··· + P}_{n \ \ timers}
$$
例如计算 2P的值：

做P点的切线F，设F与椭圆曲线相交与点Z,则存在
$$
\begin{cases}
& P + P + Z = 0 \\
& y_z^2 = x_Z^3 + ax_Z + b \ (mod  \ p) \\
\end{cases}	
\Rightarrow
\begin{cases}
& 2P = -Z \\
& (y_z^2 - (x_Z^3 + ax_Z + b)) \ (mod  \ p) = 0 
\end{cases}
$$
所以，2P的值为点Z关于X轴的对称点，我们只需要求出点Z的坐标，即可算出2P的值。

**计算优化**

假设add和double的复杂度是`O(1)`的，那么单纯这样的一个标量乘法的复杂度是`O(n)`的，然而却可以通过一些方法来变成`O(log n)` 的。比如`n = 151`的时候，可以把它拆解为`10010111b`，即：
$$
\begin{aligned}
& 151 = 1* 2^7 + 0 * 2^6 +0 * 2^5 + 4 * 2^4 + 0 * 2^3 + 1 * 2^2 + 1 * 2^1 + 1 * 2^0 \\ 
& \ \ \ \ \ \ = 2^7 + 2^4 + 2^2+2^1+2^0
\end{aligned}
$$
则计算可以简化为:
$$
151*P = 2^7P + 2^4P + 2^2P + 2^1P + 2^0P
$$
计算结果如下，这样只需要调用7次double方法和4次add方法。而直接算的话要调用150次add方法。

- 计算 0 + P 得到 P。
- double P , 得到 2P.
-  add 2P 和 P, 得到 $ 2^1P + 2^0P $.
-  double 2P,得到$2^2P$
-  add $2^2P$,得到 $2^2P+ 2^1P + 2^0P $.
-  double $2^2P$，得到 $2^3P$
-  double $2^3P$,得到$2^4P$
-  add $2^4P$, 得到  $2^4P + 2^2P + 2^1P + 2^0P $.

 ...



###### 模p的整数域

即要求x,y都为整数，切公式都需要 mod p ，以确保y的取值范围在 0 - p内。即：
$$
\begin{aligned}  
& m = \frac{(y_P-y_Q)}{(x_P-x_Q)} \ \ \ (mod \ p) \\
& x_R = m^2 - x_P - x_Q \ \ \ (mod \ p)\\
& y_R = y_p + m(x_R - x_P) \ \ (mod \ p) \\
& or \\
& y_R = y_Q + m(x_R - x_Q) \ \ \ ( mod \ p)
\end{aligned}
$$
***注意：***

这里涉及到分式的求模运算，需要转换成乘法的求模运算。

- 根据费马小定理求模：

  费马小定理： 对于正整数n和p, p为素数， 存在 $n^{p-1} = 1 \ mod \ p$ ,将公式变形下：
  $$
  \begin{aligned}  
  n^{p-1} = 1 \ mod \ p \\
  \Rightarrow n*n^{p-2} = 1 \ mod \ p \\
  \end{aligned}
  $$
  即n^{p-2}为n的逆元。则：
  $$
  \begin{aligned}  
  & m = \frac{(y_P-y_Q)}{(x_P-x_Q)} \ \ \ (mod \ p) \\ 
  & \ \ \ \ = \frac{(y_P-y_Q)}{(x_P-x_Q)} * 1\ \ \ (mod \ p)	\\
  & \ \ \ \ = \frac{(y_P-y_Q)}{(x_P-x_Q)} *(x_P-x_Q)* (x_P-x_Q)^{p-2}\ \ \ (mod \ p) \\
  & \ \ \ \ = (y_P-y_Q)(x_P-x_Q)^{p-2}\ \ (mod \ p) \\
  
  \end{aligned}
  $$
  

- 根据扩展欧几里得算法求模：

  **对于整数a,b，存在有整数x, y使得 ax + by = gcd(a,b)**

  - 算法原理

    给定整数a、b，对它们进行辗转相除法，可得他们的最大公约数。收集辗转相除法中产生的式子，倒回去，可以得到ax + by = gcd(a,b)的整数解。

    利用扩展的欧几里得算法求得满足条件的c：先做辗转相除，当a、b互素时，最后一步得到的余数为1，再从1出发，对前面得到的所有除法算式进行变形，将余数用除数和被除数表示，最终便可将1表示为a与b的一种线性组合，即
    $$
     ax +by =1
    $$
    从而 x 就是 a 模 b 的乘法逆元。 因此寻找乘法逆元的过程就是求x和y的过程。
    $$
    \begin{aligned}
    & gcd(a, b) = ax + by  	\\
    &  \ = (kb+r)x+by	\\
    & \ = (kx+y)b + rx	\\
    & \ = (kx+y)b (mod \ b) +  rx \ (mod \ b)	\\
    & \ = rx \ (mod \ b)
    \end{aligned}
    $$
    

    所以， gcd(a,b) = gcd(b, a%b) = 1;

    观察一下gcd算法的递归代码，可以发现算法的终止条件是a=gcd，b=0。对于这样的a和b来说，我们已经找到了一组解使得ax+by=gcd，比如很明显，x=1，y=0。实际上y可以为任何值，因为b=0。

    如果已知gcd(b, a%b)的解为 $x_0$ 和 $y_0$， 则 gcd(a,b)可求：
    $$
    \begin{aligned}
    & gcd(a,b) = gcd(b,a\%b)	\\
    & \ \ \ \ \  \  \  \  \  \  \ \ \ \  =  bx_0 + (a\%b)y_0		\\
    & \ \ \ \ \  \  \  \  \  \  \ \ \ \  =  bx_0 + (a - (a/b)b)y_0 \\
    & \ \ \ \ \  \  \  \  \  \  \ \ \ \  =  bx_0 + ay_0 - b(a/b)y_0 \\
    & \ \ \ \ \  \  \  \  \  \  \ \ \ \  =  y_0 * a + b*(x_0 - (a/b)y_0) 
    \end{aligned}
    $$
    显然， 对于a和 b 来说， 它的一组解为 $y_0$ 和 $x_0 - (a/b)y_0$ .

    若 gcd(a, a%b) 为终止， 即 a = gcd, a%b =0.  则  解为 $x_0 =1, y_0 = 0 $
    $$
    \begin{aligned}
    & x = y0 = 0	\\
    & y = x_0 - (a/b)y_0 = 1 - (a/b)* 0 = 1
    \end{aligned}
    $$
     

    以此类推。



**椭圆曲线的阶**

有限域上面的椭圆曲线是由有限个点所构成的，那么具体有几个点呢？

首先，定义概念**椭圆曲线群的阶**为当前椭圆曲线群上面的点的数量。

可以直接将x从0到p − 1计数有多少点，但这样的复杂度是`O ( p )`的，在p比较大的时候会很慢，也有比较高效的算法来计算椭圆曲线的阶，比如[Schoof算法](https://en.wikipedia.org/wiki/Schoof's_algorithm)，这里不具体展开。

##### 标量乘法以及循环群

标量乘法的计算方法即为计算多次的加法：

![image20230222093428572](https://markdown-1306347444.cos.ap-shanghai.myqcloud.com/img/image-20230222093428572.png)

同样的，可以用之前提出的**二进制分解**的方法来加快运算。

但有限域上面的乘法有一个有趣的性质，就是他会构成一个乘法循环子群。

![cyclicsubgroup](https://markdown-1306347444.cos.ap-shanghai.myqcloud.com/img/cyclic-subgroup.png)

会发现`nP`会在 `(0,P,2P,3P,4P)`这些值中不断循环。可以在[这个链接](https://andrea.corbellini.name/ecc/interactive/modk-mul.html)里面试一下。

![image20230222093936277](https://markdown-1306347444.cos.ap-shanghai.myqcloud.com/img/image-20230222093936277.png)

![image20230222094045749](https://markdown-1306347444.cos.ap-shanghai.myqcloud.com/img/image-20230222094045749.png)

这样的`P`被称作这个循环子群的**生成元**(generator)或者**基本点**(base point)。

###### 子群的阶

有一个问题就是**由`P`生成的循环子群的阶是多少呢？**。或者换一种说法，`P`的阶是多少？。

- `P`的阶就是令`nP = 0`的最小的n，（0本身除外），在上面的例子里面就是5。
- `P`的阶和整个椭圆曲线的阶是满足[拉格朗日定理](https://en.wikipedia.org/wiki/Lagrange's_theorem_(group_theory))的，也就是说子群的阶可以整除父群的阶。

因此就可以用下面的方法找出某个点P的阶了：

1. 使用[Schoof算法](https://en.wikipedia.org/wiki/Schoof's_algorithm)计算得出整个椭圆曲线的阶N。
2. 找到阶N的所有因子。
3. 对于N的每个因子n，按照从小到大的方式，计算nP。
4. 如果`nP = 0`，那么n是子群的阶。









## Sample 

在蓝牙Core Spec中，对ECC P-192和P-256的算法定义如下：

对 **P-192**和**P-256**加密算法， **a = -3**:

素模 **p** ,阶 **r** ,基点 **G**的坐标（G<sub>x</sub>, G<sub>y</sub>）的值由下面给出：

**For P-192:**

>p =  6277101735386680763835789423207666416083908700390324961279
>
>r =  6277101735386680763835789423176059013767194773182842284081
>
>b =  0x 64210519 e59c80e7 0fa7e9ab 72243049 feb8deec c146b9b1
>
>Gx =  0x 188da80e b03090f6 7cbf20eb 43a18800 f4ff0afd 82ff1012
>
>Gy =  0x 07192b95 ffc8da78 631011ed 6b24cdd5 73f977a1 1e794811

### 定义：

**给定一个整数u, 0 < u < r， 以及曲线E上的一个点V,计算值P<sub>192</sub>(u, V)作为点V的第u倍的uV的x坐标。**

私钥应为 1 到 r/2之间， 其中 r 为椭圆曲线上阿贝尔群的阶数（即在 1到 2<sup>192</sup>/2）。



**For P-256**

>p =   11579208921035624876269744694940757353008614341529031419553363 1308867097853951
>
>r =  11579208921035624876269744694940757352999695522413576034242225 9061068512044369
>
>b =  0x5ac635d8 aa3a93e7 b3ebbd55 769886bc 651d06b0 cc53b0f6 3bce3c3e  27d2604b
>
>Gx =  0x6b17d1f2 e12c4247 f8bce6e5 63a440f2 77037d81 2deb33a0 f4a13945  d898c296
>
>Gy =  0x 4fe342e2 fe1a7f9b 8ee7eb4a 7c0f9e16 2bce3357 6b315ece cbb64068  37bf51f5

### 定义：

****

**给定一个整数u, 0 < u < r， 以及曲线E上的一个点V,计算值P<sub>256</sub>(u, V)作为点V的第u倍的uV的x坐标。**

私钥应为 1 到 r/2之间， 其中 r 为椭圆曲线上阿贝尔群的阶数（即在 1到 2<sup>256</sup>/2）。



## 私钥的产生

**取一个随机整数 u, ，满足 0 < u < r,  u 即为私钥 **

###  公钥的产生

**公钥Q为曲线E上的点G的第u倍的uG点的坐标，且满足Y<sub>Q</sub><sup>2</sup> = X<sub>Q</sub><sup>3</sup> + aX<sub>Q</sub>+b(mod p)**

### DHKey的产生

假设A的私钥为Private_A, 公钥为Public_A(Public_Ax, Public_Ay);B的私钥为Private_B,公钥为Public_B(Public_Bx, Public_By),则
$$
DHkey = Private\_A *(Public\_Bx, Public\_By) \\
DHkey = Private\_B *(Public\_Ax, Public\_Ay)
$$
这两个公式算出来的dhkey是一样的。

