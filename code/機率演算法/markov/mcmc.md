# 馬可夫鏈蒙地卡羅 (MCMC)

## 歷史背景

MCMC 方法由 Nicholas Metropolis 等人在 1953 年的論文《Equation of State Calculations by Fast Computing Machines》中首次提出（即 Metropolis 演算法）。後來 W. K. Hastings 在 1970 年將其推廣為 Metropolis-Hastings 演算法。

Gibbs 抽樣由 Geman 兄弟在 1984 年提出，名稱來自物理學中的 Gibbs 分佈。

MCMC 是貝氏統計推論的核心工具，廣泛應用於：
- 貝氏統計推論
- 物理系統模擬（統計力學）
- 機器學習（貝氏神經網路、主題模型）

## 核心原理

### 目標

從複雜的目標分佈 $\pi(x)$ 抽樣，其中 $\pi(x)$ 可能只知道未正規化的形式 $\tilde{\pi}(x)$。

### Metropolis-Hastings 演算法

1. **初始化**: 選擇初始值 $x^{(0)}$
2. **迭代**: 對 $t = 0, 1, 2, \ldots$
   - 從提議分佈 $q(x'|x^{(t)})$ 產生候選 $x'$
   - 計算接受機率:
     $$
     \alpha = \min\left(1, \frac{\tilde{\pi}(x') q(x^{(t)}|x')}{\tilde{\pi}(x^{(t)}) q(x'|x^{(t)})}\right)
$$
   - 以機率 $\alpha$ 接受: $x^{(t+1)} = x'$，否則 $x^{(t+1)} = x^{(t)}$

### Gibbs 抽樣

當可以從每個變數的條件分佈抽樣時：

對 $t = 0, 1, 2, \ldots$，依序更新：
$$x_i^{(t+1)} \sim p(x_i | x_1^{(t+1)}, \ldots, x_{i-1}^{(t+1)}, x_{i+1}^{(t)}, \ldots, x_n^{(t)})$$

### 收斂性

- **Burn-in**: 前 $B$ 個樣本通常被捨棄，因為它們依賴於初始值
- **混合時間** (Mixing time): 鏈需要多長時間才能忘記初始值

## 使用範例

```python
from markov.mcmc import metropolis_hastings_symmetric, sample_normal_mixture
import math

# 定義目標分佈: 標準常態 N(0,1)
def target_log_pdf(x):
    return -0.5 * x**2  # log π(x) ∝ -x²/2

# Metropolis-Hastings 抽樣
samples = metropolis_hastings_symmetric(
    target_log_pdf,
    proposal_std=1.0,
    initial=0.0,
    n_samples=10000,
    burn_in=1000
)

print(f"平均: {sum(samples)/len(samples):.4f}")  # 接近 0
print(f"變異數: {np.var(samples):.4f}")        # 接近 1
```

## 與其他抽樣方法比較

| 方法 | 適用場景 | 複雜度 | 收斂保證 |
|------|---------|--------|---------|
| 逆轉換法 | 簡單分佈 | O(1) | 精確 |
| 拒絕抽樣 | 中等複雜度 | O(1/M) | 精確 |
| Importance Sampling | 積分估計 | O(n) | 精確 |
| Metropolis-Hastings | 複雜分佈 | O(混合時間) | 漸近 |
| Gibbs 抽樣 | 條件可抽樣 | O(混合時間) | 漸近 |

## 參考資料

1. Metropolis, N., Rosenbluth, A. W., Rosenbluth, M. N., Teller, A. H., & Teller, E. (1953). Equation of state calculations by fast computing machines. *The Journal of Chemical Physics*, 21(6), 1087-1092.
2. Hastings, W. K. (1970). Monte Carlo sampling methods using Markov chains and their applications. *Biometrika*, 57(1), 97-109.
3. Geman, S., & Geman, D. (1984). Stochastic relaxation, Gibbs distributions, and the Bayesian restoration of images. *IEEE Transactions on Pattern Analysis and Machine Intelligence*, 6, 721-741.
4. Robert, C. P., & Casella, G. (2004). *Monte Carlo Statistical Methods*. Springer.
