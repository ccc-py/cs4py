# Bernstein-Vazirani 演算法

## 歷史背景

Bernstein-Vazirani 演算法由 Ethan Bernstein 和 Umesh Vazirani 在 1993 年提出，是 Deutsch 演算法的推廣。該演算法解決的問題是：給定一個 Oracle 函數 $f(x) = s \cdot x \pmod{2}$（其中 $s$ 是隱藏的 $n$-bit 字串），找出 $s$。

古典演算法需要 $n$ 次查詢，而 Bernstein-Vazirani 演算法只需要 **1 次查詢**，展現了指數級的量子優勢。

## 核心原理

### 問題定義
給定 Oracle 存取函數 $f: \{0,1\}^n \rightarrow \{0,1\}$，其中 $f(x) = s \cdot x \pmod{2}$（點積模 2），$s$ 是隱藏的 $n$-bit 字串。找出 $s$。

### 量子電路
1. 初始化：$|0\rangle^{\otimes n}|1\rangle$
2. 應用 Hadamard：$|+\rangle^{\otimes n}|-\rangle$
3. Oracle：$U_f$ 產生相位 kickback $(-1)^{s\cdot x}|x\rangle|-\rangle$
4. 對資料位元應用 $H^{\otimes n}$
5. 測量資料位元，結果即為 $s$

### 數學推導
經過 Oracle 後：
$$|\psi\rangle = \frac{1}{\sqrt{2^n}}\sum_{x=0}^{2^n-1} (-1)^{s\cdot x}|x\rangle|-\rangle$$

應用 $H^{\otimes n}$：
$$H^{\otimes n}|x\rangle = \frac{1}{\sqrt{2^n}}\sum_{z=0}^{2^n-1} (-1)^{x\cdot z}|z\rangle$$

當 $z = s$ 時，干涉相長；其他情況干涉相消。因此測量結果為 $s$。

## 使用範例

```python
from bernstein_vazirani import bernstein_vazirani_with_measurement

# 隱藏字串
s = "101"
result = bernstein_vazirani_with_measurement(s)
print(f"隱藏字串: {s}")
print(f"結果: {result}")  # 應該等於 "101"
```

## 量子優勢

| 方法 | 查詢次數 | n=100 時 |
|---|---|---|
| 古典（最優） | n | 100 |
| **Bernstein-Vazirani** | **1** | **1** |

## 參考資料

1. Bernstein, E., & Vazirani, U. (1993). "Quantum Complexity Theory". *Proceedings of the 25th Annual ACM Symposium on Theory of Computing*.
2. Bernstein, E., & Vazirani, U. (1997). "Quantum Complexity Theory". *SIAM Journal on Computing*, 26(5), 1411-1473.
3. Nielsen, M. A., & Chuang, I. L. (2010). *Quantum Computation and Quantum Information*. Cambridge University Press.
4. Cleve, R., et al. (1998). "Quantum Algorithms Revisited". *Proceedings of the Royal Society A*, 454(1969), 339-354.
