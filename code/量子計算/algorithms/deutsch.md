# Deutsch 演算法

## 歷史背景

Deutsch 演算法由 David Deutsch 在 1985 年提出，是第一個展現量子計算優勢的演算法。該演算法解決了「Deutsch 問題」：判斷一個二元函數是常數函數（對所有輸入輸出相同）還是平衡函數（對一半輸入輸出 0，另一半輸出 1）。

古典演算法需要評估函數兩次才能確定，而 Deutsch 演算法只需要一次評估，展現了量子計算的優勢。

## 核心原理

### Deutsch 問題
給定函數 $f: \{0,1\} \rightarrow \{0,1\}$，判斷：
- **常數函數**： $f(0) = f(1)$
- **平衡函數**： $f(0) \neq f(1)$

### 量子電路
1. 初始化：$|0\rangle|1\rangle$
2. 應用 Hadamard：$|+\rangle|-\rangle = \frac{1}{2}(|00\rangle - |01\rangle + |10\rangle - |11\rangle)$
3. 應用 Oracle $U_f$：$|x\rangle|y\rangle \rightarrow |x\rangle|y \oplus f(x)\rangle$
4. 由於目標是 $|-\rangle$，產生相位 kickback：$(-1)^{f(x)}|x\rangle|-\rangle$
5. 對第一個量子位元應用 Hadamard
6. 測量第一個量子位元

### 數學推導
經過 Oracle 後：
$$|\psi\rangle = \frac{1}{2}[(-1)^{f(0)}|0\rangle + (-1)^{f(1)}|1\rangle]|-\rangle$$

再應用 Hadamard：
- 若 $f(0) = f(1)$（常數）：$|\psi\rangle = \pm |0\rangle|-\rangle$
- 若 $f(0) \neq f(1)$（平衡）：$|\psi\rangle = \pm |1\rangle|-\rangle$

## 使用範例

```python
from deutsch import deutsch_with_oracle, constant_function, balanced_function_x

# 測試常數函數
result = deutsch_with_oracle(constant_function)
print(result)  # "constant"

# 測試平衡函數
result = deutsch_with_oracle(balanced_function_x)
print(result)  # "balanced"
```

## 量子優勢

| 方法 | 查詢次數 |
|---|---|
| 古典最優 | 2 |
| Deutsch 量子演算法 | 1 |

## 參考資料

1. Deutsch, D. (1985). "Quantum Theory, the Church-Turing Principle and the Universal Quantum Computer". *Proceedings of the Royal Society A*, 400(1818), 97-117.
2. Nielsen, M. A., & Chuang, I. L. (2010). *Quantum Computation and Quantum Information*. Cambridge University Press.
3. Cleve, R., et al. (1998). "Quantum Algorithms Revisited". *Proceedings of the Royal Society A*, 454(1969), 339-354.
