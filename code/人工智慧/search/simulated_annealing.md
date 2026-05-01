# 模擬退火演算法 (Simulated Annealing)

## 歷史背景

1953 年 Nicholas Metropolis 等人提出 Metropolis 演算法，模擬熱力學系統的粒子行為。1983 年 Scott Kirkpatrick、C. Daniel Gelatt 和 Mario P. Vecchi 在 IBM 將其首次應用於組合最佳化問題，發表於《Science》期刊。演算法名稱源自金屬加工中的退火工藝：加熱金屬使原子自由移動，然後緩慢冷卻使它們排列到最低能量狀態。

## 核心原理

### Metropolis 準則

接受新解的概率：
```
P(接受) = 1                        如果 ΔE < 0（改善）
P(接受) = exp(-ΔE / T)            如果 ΔE ≥ 0（惡化）
```

其中 ΔE 為成本變化，T 為當前溫度。

### 退火計畫

| 策略 | 公式 | 特性 |
|------|------|------|
| 指數冷卻 | T = T₀ · α^k | 最常用，簡單有效 |
| 線性冷卻 | T = T₀ - k · α | 理論保證但實務少用 |
| 對數冷卻 | T = c / log(1 + k) | 理論上保證全域最佳 |

### 搜尋階段

1. **高溫期**：大量接受惡化解，廣泛探索搜尋空間
2. **降溫期**：接受率逐漸降低，開始集中在有希望的區域
3. **低溫期**：幾乎只接受改善解，精細微調當前最佳解

## 使用範例

```python
from search.simulated_annealing import simulated_annealing

def cost(x):
    return (x[0] - 3) ** 2 + 5  # 最小值在 x=3

best_sol, best_cost, history = simulated_annealing(
    current_solution=[0.0],
    cost_func=cost,
    neighbor_func=lambda x: [x[0] + random.uniform(-1, 1)],
    initial_temp=100.0,
    cooling_rate=0.99,
    seed=42,
)
```

## 複雜度

- **時間**：O(max_iterations × 鄰居生成 + 成本評估)
- **空間**：O(n × i)，n 為解的維度，i 為迭代次數（儲存歷史）

## 參數調優建議

| 參數 | 建議範圍 | 說明 |
|------|---------|------|
| initial_temp | 100-1000 | 足夠高以接受 ~80% 惡化解 |
| cooling_rate | 0.95-0.999 | 越接近 1 收斂越好但越慢 |
| max_iterations | 5000-50000 | 依問題複雜度調整 |

## 參考資料

- Kirkpatrick, S., Gelatt, C. D., & Vecchi, M. P. (1983). Optimization by Simulated Annealing. Science.
- Metropolis, N., et al. (1953). Equation of State Calculations by Fast Computing Machines.
