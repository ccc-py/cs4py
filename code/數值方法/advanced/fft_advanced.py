"""
進階快速傅立葉變換 (FFT) 應用

實作 FFT-based 摺積和快速多項式乘法，純 Python 從頭實現，
不使用 numpy 等外部函式庫。

歷史背景：
Cooley 和 Tukey 在 1965 年發表的論文開啟了 FFT 的現代時代。
事實上，Gauss 在 1805 年就已經發明了類似的方法，但未受注意。
FFT 是 20 世紀最重要的數值演算法之一，將 O(n²) 的 DFT 降至 O(n log n)。

本模組展示如何利用自訂的 FFT 實現：
1. 快速摺積：O(n log n) 而非 O(n²)
2. 快速多項式乘法：領先方法

author: cs4py
"""

import cmath
import math


def fft(x: list[complex]) -> list[complex]:
    """
    快速傅立葉變換 (Cooley-Tukey 遞迴版本)

    將時域信號轉換為頻域表示

    Args:
        x: 輸入序列（長度應為 2 的冪次）

    Returns:
        FFT 結果序列
    """
    n = len(x)
    if n == 1:
        return x

    if n % 2 != 0:
        raise ValueError("輸入長度必須是 2 的冪次")

    even = fft(x[0::2])
    odd = fft(x[1::2])

    result = [0j] * n
    for k in range(n // 2):
        t = cmath.exp(2j * math.pi * k / n) * odd[k]
        result[k] = even[k] + t
        result[k + n // 2] = even[k] - t

    return result


def ifft(x: list[complex]) -> list[complex]:
    """
    快速傅立葉反變換

    Args:
        x: 頻域序列

    Returns:
        時域序列
    """
    n = len(x)
    conjugate = [v.conjugate() for v in x]
    forward = fft(conjugate)
    return [v / n for v in forward]


def next_power_of_two(n: int) -> int:
    """
    找出大於等於 n 的最小 2 的冪次

    Args:
        n: 目標數字

    Returns:
        2 的冪次
    """
    if n <= 0:
        return 1
    if n & (n - 1) == 0:
        return n
    n |= n >> 1
    n |= n >> 2
    n |= n >> 4
    n |= n >> 8
    n |= n >> 16
    return n + 1


def zero_pad(x: list[float], n: int) -> list[complex]:
    """
    將序列補零至長度 n

    Args:
        x: 輸入序列
        n: 目標長度

    Returns:
        補零後的複數序列
    """
    result = [complex(v, 0) for v in x]
    while len(result) < n:
        result.append(0j)
    return result[:n]


def convolve_naive(a: list[float], b: list[float]) -> list[float]:
    """
    暴力摺積：O(n²) 複雜度

    (a * b)[n] = Σ a[k] * b[n-k]

    Args:
        a: 第一個序列
        b: 第二個序列

    Returns:
        摺積結果
    """
    n = len(a)
    m = len(b)
    result = [0.0] * (n + m - 1)
    for i in range(n):
        for j in range(m):
            result[i + j] += a[i] * b[j]
    return result


def convolve_fft(a: list[float], b: list[float]) -> list[float]:
    """
    FFT-based 摺積：O(n log n) 複雜度

    原理：時域摺積 = 頻域乘法

    1. 將 a, b 補零至相同長度（≥ len(a) + len(b) - 1）
    2. 對兩序列做 FFT
    3. 逐點相乘
    4. 做反 FFT 取得結果

    Args:
        a: 第一個序列
        b: 第二個序列

    Returns:
        摺積結果
    """
    output_len = len(a) + len(b) - 1
    n = next_power_of_two(output_len)

    a_padded = zero_pad(a, n)
    b_padded = zero_pad(b, n)

    A = fft(a_padded)
    B = fft(b_padded)

    C = [A[i] * B[i] for i in range(n)]

    c = ifft(C)

    result = [c[i].real for i in range(output_len)]
    return result


def multiply_polynomials(p: list[float], q: list[float]) -> list[float]:
    """
    快速多項式乘法

    將多項式係數視為序列，使用 FFT 進行乘法

    Args:
        p: 第一個多項式係數（遞減次方）
        q: 第二個多項式係數（遞減次方）

    Returns:
        乘積多項式係數
    """
    return convolve_fft(p, q)


def naive_polynomial_multiply(p: list[float], q: list[float]) -> list[float]:
    """
    暴力多項式乘法

    Args:
        p: 第一個多項式係數
        q: 第二個多項式係數

    Returns:
        乘積多項式係數
    """
    return convolve_naive(p, q)


if __name__ == "__main__":
    import time

    print("=" * 50)
    print("FFT 應用：摺積與多項式乘法")
    print("=" * 50)

    print("\n--- 簡單摺積示範 ---")
    a = [1.0, 2.0, 3.0, 4.0]
    b = [0.5, 1.0, 0.5]

    result_naive = convolve_naive(a, b)
    result_fft = convolve_fft(a, b)

    print(f"a = {a}")
    print(f"b = {b}")
    print(f"摺積結果（暴力法）: {[round(x, 4) for x in result_naive]}")
    print(f"摺積結果（FFT）:    {[round(x, 4) for x in result_fft]}")

    max_diff = max(abs(result_naive[i] - result_fft[i]) for i in range(len(result_naive)))
    print(f"兩者最大差異: {max_diff:.10f}")

    print("\n--- 多項式乘法示範 ---")
    p = [1.0, 2.0, 3.0]
    q = [4.0, 5.0]

    result_poly_naive = naive_polynomial_multiply(p, q)
    result_poly_fft = multiply_polynomials(p, q)

    print(f"p(x) = 1 + 2x + 3x²")
    print(f"q(x) = 4 + 5x")
    print(f"p*q = 4 + 13x + 22x² + 15x³")
    print(f"暴力乘法結果: {result_poly_naive}")
    print(f"FFT乘法結果:   {result_poly_fft}")

    print("\n--- 效能比較 ---")
    sizes = [64, 128, 256, 512, 1024]

    print(f"{'大小':>6} {'暴力法(ms)':>12} {'FFT法(ms)':>12} {'加速比':>8}")
    print("-" * 42)

    for size in sizes:
        a_large = [float(i % 10) for i in range(size)]
        b_large = [float(i % 10) for i in range(size // 2)]

        start = time.time()
        result_naive_large = convolve_naive(a_large, b_large)
        time_naive = (time.time() - start) * 1000

        start = time.time()
        result_fft_large = convolve_fft(a_large, b_large)
        time_fft = (time.time() - start) * 1000

        speedup = time_naive / time_fft if time_fft > 0 else float('inf')
        print(f"{size:6d} {time_naive:12.2f} {time_fft:12.2f} {speedup:8.2f}x")

    print("\n--- 大小為 2 的冪次的 FFT 效率 ---")
    n = 512
    x = [complex(float(i), 0) for i in range(n)]

    start = time.time()
    X = fft(x)
    time_fft_single = (time.time() - start) * 1000

    print(f"n = {n} 的 FFT 耗時: {time_fft_single:.3f} ms")

    print("\n" + "=" * 50)
    print("FFT 應用示範完成")
    print("=" * 50)