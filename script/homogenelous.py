import functools as ft


def permutation(n, k):
    if k > n:
        return 0
    elif 0 < k <= n:
        return ft.reduce(lambda x, y: x * y, [n - v for v in range(k)])
    else:
        return 1


def factorial(n):
    return permutation(n, n - 1)


def combination(n, k):
    return int(permutation(n, k) / factorial(k))


def homogeneous(n, k):
    return combination(n + k - 1, k)


def homogeneous_with_limit(m, n, t):
    return sum([(-1) ** k * combination(n, k) * homogeneous(n, t - n - m * k) \
                for k in range(0, int((t - n) / m) + 1)])


if __name__ == '__main__':
    print("上限付き重複組み合わせを計算します")
    print("同名カードの最大枚数: ", end="")
    m = int(input())
    print("カードの種類: ", end="")
    n = int(input())
    print("デッキの最大枚数: ", end="")
    t = int(input())
    print("homogeneous_with_limit: ", end="")
    print(sum([homogeneous_with_limit(m, n, k) for k in range(40, t + 1)]))
