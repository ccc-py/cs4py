"""
離散對數問題 (Discrete Logarithm Problem)

包含：
1. 離散對數問題定義
2. Baby-step Giant-step 演算法
3. Pohlig-Hellman 演算法（針對合數階群）
4. 示範程式
"""

from typing import Optional, Tuple, Dict
import math


def baby_step_giant_step(g: int, h: int, p: int) -> Optional[int]:
    """
    Baby-step Giant-step 演算法求解離散對數
    
    求解 g^x ≡ h (mod p) 中的 x。
    
    這個演算法由 Daniel Shanks 提出，時間複雜度 O(√n)，
    其中 n 是群的階（對於質數 p，階為 p-1）。
    
    時間複雜度：O(√p)
    空間複雜度：O(√p)
    
    Args:
        g: 生成元（或底數）
        h: 目標值
        p: 質數模數
        
    Returns:
        x 滿足 g^x ≡ h (mod p)，如果不存在則返回 None
    """
    # 計算 m = ceil(√p)
    m = int(math.ceil(math.sqrt(p)))
    
    # Baby steps: 計算 g^j mod p 對於 j = 0, 1, ..., m-1
    baby_steps = {}
    current = 1
    for j in range(m):
        if current not in baby_steps:
            baby_steps[current] = j
        current = (current * g) % p
    
    # 計算 g^(-m) mod p
    # 使用費馬小定理：g^(p-1) ≡ 1 (mod p)，所以 g^(-m) ≡ g^(p-1-m) (mod p)
    g_m_inv = pow(g, p - 1 - m, p)
    
    # Giant steps: 計算 h * (g^(-m))^i 對於 i = 0, 1, ..., m
    giant = h % p
    for i in range(m):
        if giant in baby_steps:
            # 找到解：x = baby_steps[giant] + i * m
            return baby_steps[giant] + i * m
        giant = (giant * g_m_inv) % p
    
    return None  # 沒有找到解


def pohlig_hellman(g: int, h: int, p: int, factors: Dict[int, int]) -> Optional[int]:
    """
    Pohlig-Hellman 演算法
    
    當群的階（p-1）是合數時，可以將離散對數問題分解為
    各個質因子冪次下的子問題，然後用中國餘式定理組合結果。
    
    如果 p-1 有小的質因子，這個演算法非常有效。
    
    Args:
        g: 生成元
        h: 目標值
        p: 質數模數
        factors: p-1 的質因子分解，格式為 {質因子: 冪次}
        
    Returns:
        x 滿足 g^x ≡ h (mod p)，如果不存在則返回 None
    """
    # 群的階
    n = p - 1
    
    # 存儲每個質因子冪次下的結果
    congruences = []  # (x_mod, modulus)
    
    for q, e in factors.items():
        # 處理質因子 q^e
        mod = q ** e
        
        # 計算 g' = g^(n/q^e) 和 h' = h^(n/q^e)
        # 這樣在子群中的階是 q^e
        g_prime = pow(g, n // mod, p)
        h_prime = pow(h, n // mod, p)
        
        # 現在求解 (g')^x ≡ h' (mod p) 其中 x < q^e
        # 使用 BSGS 或窮舉（因為 q^e 通常不大）
        x_q = None
        
        if mod <= 2**20:  # 如果 mod 不太大，使用 BSGS
            x_q = baby_step_giant_step_prime_power(g_prime, h_prime, p, q, e)
        
        if x_q is None:
            # 降級到普通 BSGS
            x_q = baby_step_giant_step(g_prime, h_prime, p)
            if x_q is not None:
                x_q = x_q % mod
        
        if x_q is None:
            return None
        
        congruences.append((x_q, mod))
    
    # 使用中國餘式定理組合結果
    return chinese_remainder(congruences, n)


def baby_step_giant_step_prime_power(
    g: int, h: int, p: int, q: int, e: int
) -> Optional[int]:
    """
    針對質因子冪次 q^e 的 Baby-step Giant-step
    
    利用 Pohlig-Hellman 的思想，在質因子冪次的子群中求解。
    
    Args:
        g, h, p: 同上
        q: 質因子
        e: 冪次
        
    Returns:
        在 mod q^e 下的離散對數值
    """
    mod = q ** e
    x = 0
    
    # 逐位求解（基於 q 進制）
    current_g = pow(g, 1, p)
    current_h = pow(h, 1, p)
    factor = 1  # q^i
    
    for i in range(e):
        # 求解 (g^(factor))^(x_i) ≡ h' (mod p) 其中 x_i ∈ {0, 1, ..., q-1}
        g_i = pow(current_g, factor, p)
        h_i = current_h
        
        # 窮舉 x_i（因為 q 通常很小）
        x_i = None
        for candidate in range(q):
            if pow(g_i, candidate, p) == h_i % p:
                x_i = candidate
                break
        
        if x_i is None:
            return None
        
        x += x_i * factor
        
        # 更新 current_h: h = h / (g^x_i * factor)
        current_h = (current_h * pow(pow(g, -1, p), x_i * factor, p)) % p
        factor *= q
    
    return x % mod


def chinese_remainder(congruences: list, full_mod: int) -> int:
    """
    中國餘式定理
    
    求解同餘方程組：
    x ≡ a_i (mod n_i)
    
    Args:
        congruences: [(a_i, n_i), ...] 列表
        full_mod: 所有 n_i 的乘積（或者 lcm）
        
    Returns:
        滿足所有同餘方程的解
    """
    result = 0
    for a, n in congruences:
        # 計算 N/n 對於當前模數的逆元
        other_mods = [nj for _, nj in congruences if nj != n]
        N_over_n = 1
        for m in other_mods:
            N_over_n *= m
        
        # 求逆元
        inv = pow(N_over_n, -1, n)
        result = (result + a * N_over_n * inv) % full_mod
    
    return result


def factor(n: int) -> Dict[int, int]:
    """
    簡單的質因子分解（用於 Pohlig-Hellman）
    
    Args:
        n: 待分解的數
        
    Returns:
        質因子分解字典
    """
    factors = {}
    d = 2
    temp = n
    while d * d <= temp:
        while temp % d == 0:
            factors[d] = factors.get(d, 0) + 1
            temp //= d
        d += 1 if d == 2 else 2  # 2 之後只檢查奇數
    if temp > 1:
        factors[temp] = factors.get(temp, 0) + 1
    return factors


def demo_basic():
    """基本 Baby-step Giant-step 示範"""
    print("=" * 60)
    print("離散對數問題 - Baby-step Giant-step 演算法")
    print("=" * 60)
    
    # 範例：求解 2^x ≡ 9 (mod 11)
    g, h, p = 2, 9, 11
    print(f"\n求解: {g}^x ≡ {h} (mod {p})")
    x = baby_step_giant_step(g, h, p)
    print(f"解: x = {x}")
    if x is not None:
        print(f"驗證: {g}^{x} mod {p} = {pow(g, x, p)}")
    
    # 另一個範例
    print("\n" + "-" * 40)
    g, h, p = 3, 7, 17
    print(f"求解: {g}^x ≡ {h} (mod {p})")
    x = baby_step_giant_step(g, h, p)
    print(f"解: x = {x}")
    if x is not None:
        print(f"驗證: {g}^{x} mod {p} = {pow(g, x, p)}")
    
    # 顯示演算法步驟
    print("\n" + "-" * 40)
    print("演算法步驟示範（小例子）:")
    g, h, p = 2, 9, 11
    m = int(math.ceil(math.sqrt(p)))
    print(f"m = ceil(√{p}) = {m}")
    
    print("\nBaby steps (g^j mod p):")
    baby = {}
    current = 1
    for j in range(m):
        baby[current] = j
        print(f"  g^{j} = {current}")
        current = (current * g) % p
    
    print(f"\nGiant steps (h * (g^(-m))^i):")
    g_m_inv = pow(g, p - 1 - m, p)
    giant = h % p
    for i in range(m):
        print(f"  i={i}: {giant}", end="")
        if giant in baby:
            print(f" -> 找到匹配! x = {baby[giant]} + {i}*{m} = {baby[giant] + i * m}")
            break
        print()
        giant = (giant * g_m_inv) % p


def demo_pohlig_hellman():
    """Pohlig-Hellman 演算法示範"""
    print("\n" + "=" * 60)
    print("Pohlig-Hellman 演算法")
    print("=" * 60)
    
    # 選擇一個 p 使得 p-1 有小的質因子
    # p = 101, p-1 = 100 = 2^2 * 5^2
    p = 101
    g = 2  # 生成元
    h = 57  # 目標值
    
    print(f"\n模數 p = {p}")
    print(f"p-1 = {p-1} = {factor(p-1)}")
    print(f"求解: {g}^x ≡ {h} (mod {p})")
    
    factors = factor(p - 1)
    x = pohlig_hellman(g, h, p, factors)
    print(f"解: x = {x}")
    if x is not None:
        print(f"驗證: {g}^{x} mod {p} = {pow(g, x, p)}")


def demo_comparison():
    """比較窮舉法和 BSGS 的效能"""
    print("\n" + "=" * 60)
    print("效能比較：窮舉法 vs Baby-step Giant-step")
    print("=" * 60)
    
    import time
    
    # 小模數
    p = 101
    g = 2
    
    for x_true in [10, 50, 90]:
        h = pow(g, x_true, p)
        print(f"\n求解 {g}^x ≡ {h} (mod {p}), 真實 x = {x_true}")
        
        # BSGS
        start = time.perf_counter()
        x = baby_step_giant_step(g, h, p)
        bsgs_time = time.perf_counter() - start
        print(f"  BSGS: x = {x}, 時間 = {bsgs_time * 1000:.3f} ms")
        
        # 窮舉法
        start = time.perf_counter()
        found = None
        for x_try in range(p):
            if pow(g, x_try, p) == h:
                found = x_try
                break
        brute_time = time.perf_counter() - start
        print(f"  窮舉: x = {found}, 時間 = {brute_time * 1000:.3f} ms")
        if brute_time > 0:
            print(f"  加速比: {brute_time/bsgs_time:.2f}x")


if __name__ == "__main__":
    demo_basic()
    demo_pohlig_hellman()
    demo_comparison()
