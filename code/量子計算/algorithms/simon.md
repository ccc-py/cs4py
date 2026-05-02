# Simon 演算法

## 歷史背景

Simon 演算法由 Daniel Simon 在 1994 年提出，是量子計算史上的重要里程碑。它解決了「Simon 問題」：找出隱藏的週期 $s$，使得函數 $f$ 滿足 $f(x) = f(y)$ 若且唯若 $y = x$ 或 $y = x \oplus s$。

Simon 演算法是第一個展現**指數級量子加速**的算法，其技術（週期尋找 over GF(2)）直接啟發了 Shor 演算法的發展。

## 核心原理

### Simon 問題
給定 Oracle 函數 $f: \{0,1\}^n \rightarrow \{0,1\}^n$，滿足：
$$f(x) = f(y) \iff y = x \text{ 或 } y = x \oplus s$$

找出隱藏的 $n$-bit 字串 $s \neq 0^n$。

### 量子演算法步驟
1. 初始化：$|0\rangle^{\otimes n}|0\rangle^{\otimes n}$
2. Hadamard：$|+\rangle^{\otimes n}|0\rangle^{\otimes n}$
3. Oracle：$|x\rangle|f(x)\rangle$ 對所有 $x$ 的疊加
4. 測量第二組量子位元，坍縮到某個 $f(x)$
5. 對第一組應用 Hadamard 並測量，得到 $y$ 滿足 $y \cdot s = 0 \pmod{2}$
6. 重複 $n-1$ 次，得到足夠的線性方程
7. 解線性方程組求得 $s$

### 數學關鍵
經過 Oracle 並測量第二組後，第一組處於：
$$\frac{1}{\sqrt{2}}(|x\rangle + |x \oplus s\rangle)$$

應用 $H^{\otimes n}$ 後測量，得到 $y$ 滿足 $y \cdot s = 0 \pmod{2}$。

## 使用範例

```python
from simon import simon_algorithm, simon_oracle_function

# 隱藏週期
s = "101"
n = len(s)
f = simon_oracle_function(s)

# 執行 Simon 演算法
result = simon_algorithm(n, f)
print(f"隱藏週期: {s}")
print(f"結果: {result}")
```

## 時間複雜度比較

| 方法 | 查詢次數 | n=100 時 |
|---|---|---|
| 古典（最優） | $O(2^{n/2})$ | ~$10^{15}$ |
| **Simon 演算法** | **$O(n)$** | **100** |

## 參考資料

1. Simon, D. R. (1994). "On the Power of Quantum Computation". *Proceedings of the 35th Annual Symposium on Foundations of Computer Science*.
2. Simon, D. R. (1997). "On the Power of Quantum Computation". *SIAM Journal on Computing*, 26(5), 1474-1483.
3. Nielsen, M. A., & Chuang, I. L. (2010). *Quantum Computation and Quantum Information*. Cambridge University Press.
4. Brassard, G., & Høyer, P. (1997). "An Exact Quantum Polynomial-Time Algorithm for Simon's Problem". *Proceedings of the Israel Symposium on Theory of Computing and Systems*.
