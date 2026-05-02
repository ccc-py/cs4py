# Shor 因數分解演算法

## 歷史背景

Shor 演算法由 Peter Shor 在 1994 年提出，是量子計算發展史上最重要的突破之一。該演算法能在多項式時間內分解大整數，對現代密碼學（特別是 RSA 加密）構成潛在威脅。

Shor 演算法的核心是將因數分解問題轉化為週期尋找問題，並利用量子傅立葉變換在指數級加速週期尋找。

## 核心原理

### 問題定義
給定合數 $N$，找到 $N = p \times q$ 的非平凡因數。

### 演算法步驟
1. **選擇隨機數** $a$，滿足 $1 < a < N$ 且 $\gcd(a, N) = 1$
2. **量子週期尋找**：找到函數 $f(x) = a^x \bmod N$ 的週期 $r$
3. **古典後處理**：
   - 若 $r$ 為偶數且 $a^{r/2} \not\equiv -1 \pmod{N}$
   - 則 $\gcd(a^{r/2} \pm 1, N)$ 給出 $N$ 的因數

### 量子傅立葉變換 (QFT)
$$QFT|x\rangle = \frac{1}{\sqrt{N}}\sum_{y=0}^{N-1} e^{2\pi i xy/N}|y\rangle$$

QFT 可以在 $O(n^2)$ 量子閘內實作，是 Shor 演算法的核心。

### 連分數
用於從 QFT 的測量結果中推導出有理數 $r/N$ 的近似值。

## 使用範例

```python
from shor import shor_algorithm

# 分解 15
result = shor_algorithm(15)
print(result)  # (3, 5) 或 (5, 3)

# 分解 21
result = shor_algorithm(21)
print(result)  # (3, 7) 或 (7, 3)
```

## 時間複雜度比較

| 方法 | 時間複雜度 | 分解 2048-bit RSA |
|---|---|---|
| 古典試除法 | $O(\sqrt{N})$ | ~10¹⁰ 年 |
| 廣義數域篩法 | $O(e^{(\log N)^{1/3}})$ | ~10⁹ 年 |
| **Shor 演算法** | **$O((\log N)³)$** | **數小時** |

## 參考資料

1. Shor, P. W. (1994). "Algorithms for Quantum Computation: Discrete Logarithms and Factoring". *Proceedings of the 35th Annual Symposium on Foundations of Computer Science*.
2. Shor, P. W. (1997). "Polynomial-Time Algorithms for Prime Factorization and Discrete Logarithms on a Quantum Computer". *SIAM Journal on Computing*, 26(5), 1484-1509.
3. Nielsen, M. A., & Chuang, I. L. (2010). *Quantum Computation and Quantum Information*. Cambridge University Press.
4. Ekert, A., & Jozsa, R. (1996). "Quantum Computation and Shor's Factoring Algorithm". *Reviews of Modern Physics*, 68(3), 733-753.
