# Grover 演算法

## 歷史背景

Grover 演算法由 Lov Grover 在 1996 年提出，是量子計算中最著名的演算法之一。它提供了一種在無結構資料庫中進行搜尋的量子方法，時間複雜度為 $O(\sqrt{N})$，相比古典演算法的 $O(N)$ 有二次加速。

Grover 演算法的應用範圍很廣，包括搜尋問題、優化問題、以及作為其他量子演算法的子程序。

## 核心原理

### 問題定義
在 $N = 2^n$ 個項目的無結構資料庫中，找到滿足特定條件的目標項目。

### 演算法步驟
1. **初始化**：創建均勻疊加態 $|s\rangle = \frac{1}{\sqrt{N}}\sum_{x=0}^{N-1}|x\rangle$
2. **Grover 迭代**（重複約 $\frac{\pi}{4}\sqrt{N}$ 次）：
   - **Oracle**：對目標狀態 $|ω\rangle$ 添加負號
   - **擴散算子**：關於均值反轉（inversion about average）
3. **測量**：以高機率得到目標狀態

### 幾何解釋
Grover 迭代可以看作是狀態向量在 $|ω\rangle$ 和 $|s'\rangle$（均勻態中除去 $|ω\rangle$ 的部分）構成的二維平面上的旋轉。

每次迭代旋轉角度 $θ ≈ \frac{2\sqrt{N-1}}{N}$，經過約 $\frac{\pi}{4}\sqrt{N}$ 次旋轉後，狀態接近 $|ω\rangle$。

### 數學表示
擴散算子：$U_s = 2|s\rangle\langle s| - I$

Grover 迭代：$G = U_s U_ω$

其中 $U_ω = I - 2|ω\rangle\langleω|$ 是 Oracle。

## 使用範例

```python
from grover import grover_search

# 搜尋 2-qubit 系統中的目標 3 (|11⟩)
target = 3
result, final_state = grover_search(target, 2)
print(f"搜尋結果: {result:02b}")  # 應該是 11
```

## 時間複雜度比較

| 方法 | 查詢次數 | N=1024 時 |
|---|---|---|
| 古典線性搜尋 | O(N) | 1024 |
| 古典二分搜尋 | O(log N) | 10 (需排序) |
| Grover 演算法 | O(√N) | 32 |

## 參考資料

1. Grover, L. K. (1996). "A Fast Quantum Mechanical Algorithm for Database Search". *Proceedings of the 28th Annual ACM Symposium on Theory of Computing*.
2. Grover, L. K. (1997). "Quantum Mechanics Helps in Searching for a Needle in a Haystack". *Physical Review Letters*, 79(2), 325-328.
3. Nielsen, M. A., & Chuang, I. L. (2010). *Quantum Computation and Quantum Information*. Cambridge University Press.
4. Boyer, M., et al. (1998). "Tight Bounds on Quantum Searching". *Fortschritte der Physik*, 46(4-5), 493-505.
