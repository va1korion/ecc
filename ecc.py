from mod import Mod


# this is lab 4 implementation of elliptic curve encryption
# E 751(-1, 1)
# G (0, 1)


class Point:
    x = int()
    y = int()

    def __init__(self, x, y):
        self.x = Mod(x, module)
        self.y = Mod(y, module)

    def __str__(self):
        return "("+str(int(self.x))+", "+str(int(self.y))+")"

    def equals(self, other):
        if other.x == self.x and self.y == other.y:
            return True
        return False


module = 751
a = -1
G = Point(0, 1)


def add(p1, p2):
    lam = Mod(0, module)
    if p1.y + p2.y == 0 and p1.x == p2.x:
        return Point(0, 0)

    if p1.equals(p2):
        lam = lam + (3 * (p1.x ** 2) + a) // (2 * p1.y)
    else:
        try:
            lam = (p2.y - p1.y) // (p2.x - p1.x)
        except ZeroDivisionError:
            print("Zero division")
            print(p1)
            print(p2)
            exit()
    x = Mod((lam * lam - p1.x - p2.x), module)
    y = Mod((lam * (p1.x - x) - p1.y), module)

    point = Point(x, y)
    return point


def multiply(point, mult):
    tmp = point
    f = False
    if mult < 0:
        mult = -mult
        f = True
    for i in range(mult - 1):
        tmp = add(tmp, point)
        if tmp.equals(point) or add(tmp, point).equals(Point(0, 0)):
            print("Loop: "+str(i))
            print(tmp)
    if f:
        tmp.y = 751 - tmp.y
    return tmp


def encrypt(point, k, B):
    C = (multiply(G, k), add(point, multiply(B, k)))
    return C


def decrypt(C, n):
    m = multiply(C[0], -1*n)
    ans = add(C[1], m)
    return ans


if __name__ == '__main__':
    alphabet = {
        'а': Point(228, 271),
        'р': Point(243, 87),
        'е': Point(234, 587),
        'н': Point(238, 576),
        'с': Point(243, 664)
    }
    ks = [2, 19, 4, 8, 2, 2, 16, 10, 2]

    b = Point(406, 397)

    print('Encryption: ')
    msg = 'ренессанс'
    print('MSG: ' + msg)
    for i in range(len(msg)):
        p = alphabet[msg[i]]
        k = ks[i]
        ans = encrypt(p, k, b)
        print("C(" + msg[i] + ", " + str(k) + ") = {(" + str(int(ans[0].x)) + ", " + str(int(ans[0].y)) + "), (" + str(
            int(ans[1].x)) + ", " + str(int(ans[1].y)) + "))")

    print('Decryption: ')
    msg = [(Point(188, 93), Point(623, 166)),  # ихтиология
           (Point(725, 195), Point(513, 414)),
           (Point(346, 242), Point(461, 4)),
           (Point(489, 468), Point(739, 574)),
           (Point(725, 195), Point(663, 476)),
           (Point(745, 210), Point(724, 522)),
           (Point(725, 195), Point(663, 476)),
           (Point(618, 206), Point(438, 40)),
           (Point(286, 136), Point(546, 670)),
           (Point(179, 275), Point(73, 72)),
           ]
    n = 32
    # ans = multiply(msg[-1][0], n)
    # print(str(ans.x)+" "+ str(ans.y))
    for i in range(len(msg)):

        ans = decrypt(msg[i], n)
        print("P = (" + str(int(ans.x)) + ", " + str(int(ans.y)) + ")")

    P = Point(59, 386)
    Q = Point(61, 129)
    R = Point(100, 364)
    print()
    print("P: "+str(P))
    print("Q: "+str(Q))
    print("R: "+str(R))
    P = multiply(P, 2)
    Q = multiply(P, 3)
    R = multiply(P, -1)
    ans = add(P, Q)
    ans = add(ans, R)
    print("2P + 3Q - R: "+str(ans))

    print()
    P = Point(45, 720)
    print("P: "+str(P))
    n = 111
    print("n: " + str(n))
    print("nP: " + str(multiply(P, n)))

    print("\n \nSignature:")
    G = Point(416, 55)
    e = 11
    d = 5
    k = 6
    kG = multiply(G, k)
    print("kG: " + str(kG))
    r = int(kG.x) % 13
    z = 11
    s = (z * (e + d * r)) % 13
    signature = Point(r, s)
    print("Signature: "+str(signature))
    Q = multiply(G, d)

    v = 6 % 13 # s**-1 mod n
    u1 = e * v % 13
    u2 = int(signature.x) * v % 13
    X = add(multiply(G, u1), multiply(Q, u2))
    print("X="+str(X))
