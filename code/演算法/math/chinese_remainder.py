"""
中國剩餘定理 (Chinese Remainder Theorem, CRT)

歷史背景：
- 中國剩餘定理最早出現在南北朝時期（公元 5 世紀）的《孫子算經》
- 問題：「今有物不知其數，三三數之剩二，五五數之剩三，七七數之剩二，問物幾何？」
- 答案：23（滿足 x ≡ 2 (mod 3), x ≡ 3 (mod 5), x ≡ 2 (mod 7)）
- 在數論、密碼學（如 RSA-CRT）中有重要應用

定理內容：
- 給定一組同餘方程組：
  x ≡ a₁ (mod n₁)
  x ≡ a₂ (mod n₂)
  ...
  x ≡ aₖ (mod nₖ)
- 若所有 nᵢ 兩兩互質，則存在唯一解 x mod N（其中 N = n₁ * n₂ * ... * nₖ）
"""

from typing import List, Tuple, Optional


def extended_gcd(a: int, b: int) -> Tuple[int, int, int]:
    """
    擴展歐幾里得演算法

    原理：
    找到整數 x, y 使得 ax + by = gcd(a, b)

    時間複雜度：O(log min(a, b))
    空間複雜度：O(1)

    Args:
        a: 第一個整數
        b: 第二個整數

    Returns:
        (gcd, x, y) 其中 gcd 是最大公因數，ax + by = gcd
    """
    if b == 0:
        return a, 1, 0
    else:
        gcd, x1, y1 = extended_gcd(b, a % b)
        x = y1
        y = x1 - (a // b) * y1
        return gcd, x, y


def mod_inverse(a: int, m: int) -> Optional[int]:
    """
    計算 a 在模 m 下的乘法反元素

    原理：
    找 x 使得 a * x ≡ 1 (mod m)
    使用擴展歐幾里得演算法，若 gcd(a, m) = 1，則反元素存在

    Args:
        a: 要找反元素的數
        m: 模數

    Returns:
        a 在模 m 下的反元素，若不存在則返回 None
    """
    gcd, x, _ = extended_gcd(a, m)
    if gcd != 1:
        return None  # 反元素不存在
    return x % m


def chinese_remainder_theorem(remainders: List[int], moduli: List[int]) -> Optional[int]:
    """
    中國剩餘定理：解同餘方程組

    原理：
    1. 檢查所有模數是否兩兩互質
    2. 計算 N = n₁ * n₂ * ... * nₖ
    3. 對於每個 i，計算：
       - Ni = N / ni
       - Mi = Ni 在模 ni 下的反元素
       - term_i = ai * Ni * Mi
    4. 解 x = Σ term_i mod N

    時間複雜度：O(k² log M)，k 是方程數量，M 是模數的最大值
    空間複雜度：O(k)

    Args:
        remainders: 餘數列表 [a₁, a₂, ..., aₖ]
        moduli: 模數列表 [n₁, n₂, ..., nₖ]，需兩兩互質

    Returns:
        滿足所有同餘方程的最小正整數解，若無解則返回 None
    """
    if len(remainders) != len(moduli):
        return None

    k = len(remainders)

    # 檢查模數是否兩兩互質
    for i in range(k):
        for j in range(i + 1, k):
            if extended_gcd(moduli[i], moduli[j])[0] != 1:
                return None  # 模數不互質

    # 計算 N = 所有模數的乘積
    N = 1
    for n in moduli:
        N *= n

    result = 0

    for i in range(k):
        Ni = N // moduli[i]
        Mi = mod_inverse(Ni, moduli[i])
        if Mi is None:
            return None
        result += remainders[i] * Ni * Mi

    return result % N


def chinese_remainder_theorem_stepwise(remainders: List[int], moduli: List[int]) -> Optional[int]:
    """
    逐步合併的中國剩餘定理（不需所有模數互質）

    原理：
    兩個方程合併：
    x ≡ a₁ (mod n₁)
    x ≡ a₂ (mod n₂)

    令 g = gcd(n₁, n₂)
    若 a₁ ≢ a₂ (mod g)，無解
    否則，合併為一個方程：x ≡ a (mod lcm(n₁, n₂))

    時間複雜度：O(k² log M)
    空間複雜度：O(1)

    Args:
        remainders: 餘數列表
        moduli: 模數列表

    Returns:
        解，若無解則返回 None
    """
    if len(remainders) != len(moduli) or not remainders:
        return None

    def merge(a1: int, n1: int, a2: int, n2: int) -> Optional[Tuple[int, int]]:
        """合併兩個方程 x ≡ a1 (mod n1) 和 x ≡ a2 (mod n2)"""
        gcd, m1, m2 = extended_gcd(n1, n2)
        if (a1 - a2) % gcd != 0:
            return None  # 無解

        lcm = n1 // gcd * n2  # 避免溢位
        # 新解：x ≡ a1 + n1 * ((a2 - a1) // gcd * m1) (mod lcm)
        x = (a1 + n1 * (((a2 - a1) // gcd * m1) % (lcm // n1))) % lcm
        return (x, lcm)

    a, n = remainders[0], moduli[0]
    for i in range(1, len(remainders)):
        result = merge(a, n, remainders[i], moduli[i])
        if result is None:
            return None
        a, n = result

    return a


def demo_sunzi_problem() -> None:
    """孫子算經問題演示"""
    print("  孫子算經問題：")
    print("  今有物不知其數，")
    print("  三三數之剩二，五五數之剩三，七七數之剩二，")
    print("  問物幾何？")
    print()
    print("  同餘方程組：")
    print("    x ≡ 2 (mod 3)")
    print("    x ≡ 3 (mod 5)")
    print("    x ≡ 2 (mod 7)")
    print()

    remainders = [2, 3, 2]
    moduli = [3, 5, 7]
    result = chinese_remainder_theorem(remainders, moduli)
    print(f"  解：x = {result}")
    print(f"  驗證：")
    for a, n in zip(remainders, moduli):
        print(f"    {result} mod {n} = {result % n} {'✓' if result % n == a else '✗'}")


if __name__ == "__main__":
    print("=== 中國剩餘定理 (Chinese Remainder Theorem) 測試 ===\n")

    # 測試 1：孫子算經問題
    print("1. 孫子算經問題：")
    demo_sunzi_problem()
    print()

    # 測試 2：簡單範例
    print("2. 簡單範例：")
    test_cases = [
        ([1, 2, 3], [2, 3, 5]),   # x ≡ 1 mod 2, ≡ 2 mod 3, ≡ 3 mod 5
        ([2, 3, 2], [3, 5, 7]),   # 孫子問題
        ([1, 1], [3, 5]),          # x ≡ 1 mod 3, ≡ 1 mod 5
    ]

    for remainders, moduli in test_cases:
        result = chinese_remainder_theorem(remainders, moduli)
        print(f"  同餘方程：{list(zip(remainders, moduli))}")
        print(f"  解：x = {result}")
        if result is not None:
            verify = all(result % n == a for a, n in zip(remainders, moduli))
            print(f"  驗證：{'通過' if verify else '失敗'}")
        print()

    # 測試 3：擴展歐幾里得演算法
    print("3. 擴展歐幾里得演算法：")
    test_pairs = [(48, 18), (35, 15), (17, 31)]
    for a, b in test_pairs:
        gcd, x, y = extended_gcd(a, b)
        print(f"  gcd({a}, {b}) = {gcd}, {a}*{x} + {b}*{y} = {a*x + b*y}")
    print()

    # 測試 4：模反元素
    print("4. 模反元素：")
    pairs = [(3, 11), (7, 13), (4, 8)]  # 最後一個不存在反元素
    for a, m in pairs:
        inv = mod_inverse(a, m)
        if inv is not None:
            print(f"  {a}^(-1) mod {m} = {inv}")
            print(f"  驗證：{a} * {inv} mod {m} = {(a * inv) % m}")
        else:
            print(f"  {a} 在模 {m} 下沒有反元素")
    print()

    # 測試 5：逐步合併版本
    print("5. 逐步合併版本（不必互質）：")
    remainders = [2, 3]
    moduli = [4, 6]  # 不互質
    result = chinese_remainder_theorem_stepwise(remainders, moduli)
    print(f"  同餘方程：x ≡ 2 (mod 4), x ≡ 3 (mod 6)")
    print(f"  解：x = {result}")
    if result is not None:
        print(f"  驗證：{result} mod 4 = {result % 4}, {result} mod 6 = {result % 6}")
