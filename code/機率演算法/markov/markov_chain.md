# 馬可夫鏈 (Markov Chain)

## 歷史背景

馬可夫鏈以俄羅斯數學家安德雷·馬可夫（Andrey Markov）命名，他在 1906 年研究詩歌語言的依賴性時提出了這個概念。他的動機是證明大數法則可以推廣到相依隨機變數序列。

馬可夫鏈現在廣泛應用於：
- 自然語言處理（n-gram 模型）
- 物理系統建模（布朗運動）
- 排隊理論
- Google 的 PageRank 演算法

## 核心原理

### 馬可夫性質

對於狀態序列 $X_0, X_1, \ldots$，滿足：

$$
P(X_{n+1} = j | X_n = i, X_{n-1}, \ldots, X_0) = P(X_{n+1} = j | X_n = i)
$$

即「未來只依賴於現在，不依賴於過去」。

### 轉移矩陣

對於有限狀態空間 $\{s_1, \ldots, s_n\}$，轉移矩陣 $P$ 定義為：

$$
P_{ij} = P(X_{n+1} = s_j | X_n = s_i)
$$

每行和為 1：$\sum_j P_{ij} = 1$。

### 平穩分佈 (Stationary Distribution)

平穩分佈 $\pi$ 滿足：

$$
\pi = \pi P
$$

即 $\pi$ 是 $P$ 的特徵值 1 對應的左特徵向量。

### 存在性條件

若馬可夫鏈是：
- **不可約** (irreducible): 任意狀態可到達任意其他狀態
- **非週期** (aperiodic): 不存在狀態會週期性返回

則平穩分佈存在且唯一，且無論初始分佈如何，長期分佈都會收斂到 $\pi$。

## 使用範例

```python
import numpy as np
from markov.markov_chain import MarkovChain, TextGenerator

# 簡單氣象模型
states = ["晴", "雨"]
P = np.array([[0.9, 0.1], [0.5, 0.5]])
mc = MarkovChain(states, P)

# 模擬
seq = mc.simulate("晴", 10)
print(" -> ".join(seq))

# 平穩分佈
pi = mc.get_stationary_distribution()
print(f"平穩分佈: {pi}")

# 文字生成
tg = TextGenerator(order=1)
tg.train("我 喜歡 吃 蘋果 我 喜歡 吃 香蕉")
print(tg.generate(20))
```

## 與其他模型比較

| 模型 | 記憶性 | 複雜度 | 應用場景 |
|------|--------|--------|----------|
| 獨立同分佈 | 無 | O(1) | 簡單隨機抽樣 |
| 馬可夫鏈 | 1 階 | O(n²) | 序列建模 |
| 隱馬可夫模型 | 潛在狀態 | O(n²) | 語音識別 |
| RNN/LSTM | 長期記憶 | O(n) | 深度學習 NLP |

## 參考資料

1. Markov, A. A. (1906). Rasprostranenie zakona bol'shih chisel na velichiny, zavisyaschie drug ot druga. *Izvestiya Fiziko-matematicheskogo obschestva pri Kazanskom universitete*, 15(9), 135-156.
2. Norris, J. R. (1998). *Markov Chains*. Cambridge University Press.
3. Grimmett, G., & Stirzaker, D. (2001). *Probability and Random Processes*. Oxford University Press.
