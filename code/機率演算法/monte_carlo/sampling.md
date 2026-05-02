# 蒙地卡羅抽樣方法 (Sampling Methods)

## 歷史背景

### 拒絕抽樣 (Rejection Sampling)

由 John von Neumann 在 1951 年提出，是最早的通用抽樣方法之一。這個方法允許從任意複雜的分佈抽樣，只要有一個簡單的提議分佈。

### 重要性抽樣 (Importance Sampling)

由 Herman Kahn 在 1950 年代於核武器模擬中發展，用於解決稀有事件模擬中的高變異數問題。

### 拉丁超立方抽樣 (Latin Hypercube Sampling)

由 McKay、Beckman 和 Conover 於 1979 年提出，用於電腦實驗的設計，確保樣本在每個維度上均勻分佈。

## 核心原理

### 拒絕抽樣

給定目標分佈 $p(x)$ 和提議分佈 $q(x)$，滿足 $p(x) \leq M \cdot q(x)$：

1. 從 $q(x)$ 抽樣得到 $x$
2. 從 $\text{Uniform}(0, 1)$ 抽樣得到 $u$
3. 如果 $u \leq \frac{p(x)}{M \cdot q(x)}$，接受 $x$；否則拒絕

**接受率**: $1/M$，因此 $M$ 應盡可能小。

### 重要性抽樣

估計 $\mathbb{E}_p[f(X)] = \int f(x) p(x) dx$，但從 $q(x)$ 抽樣：

$$
\mathbb{E}_p[f(X)] = \mathbb{E}_q\left[f(X) \frac{p(X)}{q(X)}\right] \approx \frac{1}{N} \sum_{i=1}^N f(X_i) w_i
$$

其中 $w_i = \frac{p(X_i)}{q(X_i)}$ 是重要性權重。

### 拉丁超立方抽樣

將每個維度的範圍分成 $N$ 個等寬區間，確保每個區間恰好有一個樣本。這比簡單隨機抽樣更有效地覆蓋整個空間。

## 使用範例

```python
from monte_carlo.sampling import rejection_sampling, importance_sampling_estimate

# 拒絕抽樣：從自定義分佈抽樣
def target_pdf(x):
    return 2 * x if 0 <= x <= 1 else 0  # 三角形分佈

def proposal_sampler():
    return random.uniform(0, 1)

def proposal_pdf(x):
    return 1.0

samples = rejection_sampling(target_pdf, proposal_sampler, proposal_pdf, M=2.0, n_samples=1000)

# 重要性抽樣
result = importance_sampling_estimate(
    lambda x: x**2,  # 被積函數
    lambda x: 1.0,  # 目標分佈 (均勻)
    lambda: random.uniform(0, 1),  # 抽樣器
    lambda x: 1.0,  # 提議分佈
    n_samples=10000
)
```

## 變異數縮減技術比較

| 技術 | 原理 | 適用場景 |
|------|------|----------|
| 拒絕抽樣 | 接受/拒絕機制 | 從複雜分佈抽樣 |
| 重要性抽樣 | 加權樣本 | 稀有事件模擬 |
| 分層抽樣 | 分層獨立抽樣 | 減少估計變異數 |
| 控制變量 | 利用相關變量 | 已知輔助資訊 |
| 拉丁超立方 | 確保空間覆蓋 | 電腦實驗設計 |

## 參考資料

1. Von Neumann, J. (1951). Various techniques used in connection with random digits. *National Bureau of Standards Applied Mathematics Series*, 12, 36-38.
2. Kahn, H. (1956). *Applications of Monte Carlo*. RAND Corporation.
3. McKay, M. D., Beckman, R. J., & Conover, W. J. (1979). A comparison of three methods for selecting values of input variables in the analysis of output from a computer code. *Technometrics*, 21(2), 239-245.
4. Owen, A. B. (2013). *Monte Carlo theory, methods and examples*. Stanford University.
