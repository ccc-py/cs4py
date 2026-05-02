"""
質數篩選演算法

包含埃拉托斯特尼篩法（Sieve of Eratosthenes）和分段篩法（Segmented Sieve），
以及使用篩法進行質因數分解。
"""

from typing import List, Dict
import math


def sieve_of_eratosthenes(n: int) -> List[int]:
    """
    埃拉托斯特尼篩法

    找出所有小於等於 n 的質數。
    原理：從 2 開始，將每個質數的倍數標記為合數，
    未被標記的即為質數。

    時間複雜度：O(n log log n)
    空間複雜度：O(n)

    參數:
        n: 上限（包含）

    回傳:
        小於等於 n 的所有質數列表
    """
    if n < 2:
        return []

    is_prime: List[bool] = [True] * (n + 1)
    is_prime[0] = is_prime[1] = False

    # 只需檢查到 sqrt(n)
    limit: int = int(math.isqrt(n))
    for i in range(2, limit + 1):
        if is_prime[i]:
            # 標記 i 的所有倍數（從 i*i 開始）
            for j in range(i * i, n + 1, i):
                is_prime[j] = False

    # 收集所有質數
    primes: List[int] = [i for i in range(2, n + 1) if is_prime[i]]
    return primes


def segmented_sieve(n: int, segment_size: int = 10000) -> List[int]:
    """
    分段篩法（Segmented Sieve）

    將範圍 [2, n] 分成多個小段，逐段篩選質數。
    適合處理非常大的 n，因為只需要 O(sqrt(n)) 的空間。

    參數:
        n: 上限（包含）
        segment_size: 每段的大小

    回傳:
        小於等於 n 的所有質數列表
    """
    if n < 2:
        return []

    # 先找出 sqrt(n) 內的所有質數
    sqrt_n: int = int(math.isqrt(n))
    base_primes: List[int] = sieve_of_eratosthenes(sqrt_n)

    primes: List[int] = []

    # 分段處理
    low: int = 2
    high: int = min(low + segment_size, n + 1)

    while low < n + 1:
        # 當前段的標記陣列
        is_prime: List[bool] = [True] * (high - low)

        # 用基礎質數篩選當前段
        for p in base_primes:
            # 找出第一個 >= low 的 p 的倍數
            start: int = max(p * p, ((low + p - 1) // p) * p)
            for j in range(start, high, p):
                is_prime[j - low] = False

        # 收集當前段的質數
        for i in range(low, high):
            if is_prime[i - low]:
                primes.append(i)

        # 移動到下一個段
        low = high
        high = min(low + segment_size, n + 1)

    return primes


def prime_factorization_sieve(n: int) -> Dict[int, int]:
    """
    使用篩法進行質因數分解

    預先計算每個數的最小質因數（spf - smallest prime factor），
    然後可以用 O(log n) 的時間分解任意數。

    參數:
        n: 要分解的數

    回傳:
        質因數字典，鍵為質數，值為指數
    """
    if n < 2:
        return {}

    # 計算每個數的最小質因數
    spf: List[int] = list(range(n + 1))  # spf[i] = i 的最小質因數

    limit: int = int(math.isqrt(n))
    for i in range(2, limit + 1):
        if spf[i] == i:  # i 是質數
            for j in range(i * i, n + 1, i):
                if spf[j] == j:
                    spf[j] = i

    # 使用 spf 進行分解
    factors: Dict[int, int] = {}
    temp: int = n
    while temp > 1:
        p: int = spf[temp]
        factors[p] = factors.get(p, 0) + 1
        temp //= p

    return factors


def prime_factorization(n: int) -> Dict[int, int]:
    """
    對單個數進行質因數分解（使用試除法，基於預計算的質數表）

    參數:
        n: 要分解的數

    回傳:
        質因數字典
    """
    if n < 2:
        return {}

    # 先取得 sqrt(n) 內的質數
    sqrt_n: int = int(math.isqrt(n))
    primes: List[int] = sieve_of_eratosthenes(sqrt_n)

    factors: Dict[int, int] = {}
    temp: int = n

    for p in primes:
        if p * p > temp:
            break
        while temp % p == 0:
            factors[p] = factors.get(p, 0) + 1
            temp //= p

    if temp > 1:
        factors[temp] = factors.get(temp, 0) + 1

    return factors


def is_prime(n: int) -> bool:
    """
    檢查一個數是否為質數

    參數:
        n: 要檢查的數

    回傳:
        如果是質數則回傳 True
    """
    if n < 2:
        return False
    if n < 4:
        return True
    if n % 2 == 0:
        return False

    limit: int = int(math.isqrt(n))
    for i in range(3, limit + 1, 2):
        if n % i == 0:
            return False
    return True


if __name__ == "__main__":
    # 示範質數篩選演算法
    print("質數篩選演算法示範")
    print("=" * 40)

    # 埃拉托斯特尼篩法
    n: int = 50
    print(f"\n埃拉托斯特尼篩法 (n={n}):")
    primes: List[int] = sieve_of_eratosthenes(n)
    print(f"  <= {n} 的質數: {primes}")
    print(f"  共 {len(primes)} 個質數")

    # 分段篩法
    n_large: int = 100
    print(f"\n分段篩法 (n={n_large}):")
    primes_seg: List[int] = segmented_sieve(n_large, segment_size=20)
    print(f"  <= {n_large} 的質數: {primes_seg}")
    print(f"  共 {len(primes_seg)} 個質數")

    # 驗證兩種方法結果相同
    print(f"\n驗證兩種篩法結果相同: {primes == primes_seg}")

    # 質因數分解
    print("\n質因數分解:")
    test_numbers: List[int] = [12, 36, 100, 97, 360]
    for num in test_numbers:
        factors: Dict[int, int] = prime_factorization(num)
        factor_str: str = " * ".join(f"{p}^{e}" if e > 1 else str(p)
                                     for p, e in sorted(factors.items()))
        print(f"  {num} = {factor_str}")

    # 使用篩法預計算的分解
    print("\n使用篩法預計算的質因數分解 (n=360):")
    factors_sieve: Dict[int, int] = prime_factorization_sieve(360)
    print(f"  spf 方法: {factors_sieve}")

    # 質數檢查
    print("\n質數檢查:")
    test_primes: List[int] = [2, 3, 17, 25, 97, 100, 7919]
    for num in test_primes:
        print(f"  {num} 是質數: {is_prime(num)}")
