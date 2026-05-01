# 遺傳演算法 (Genetic Algorithm)

## 歷史背景

遺傳演算法由 John Holland 於 1975 年在《Adaptation in Natural and Artificial Systems》一書中正式提出。Holland 受到生物進化過程的啟發，將自然選擇和遺傳學的機制應用到最佳化問題。1989 年 David Goldberg 的《Genetic Algorithms in Search, Optimization, and Machine Learning》使 GA 成為廣泛使用的最佳化方法。

## 核心原理

### 基本流程

1. **初始化**：隨機產生初始族群
2. **評估**：計算每個個體的適應度
3. **選擇**：依適應度挑選優良個體作為父母
4. **交叉**：交換父母基因產生後代
5. **突變**：隨機改變部分基因維持多樣性
6. **替換**：新一代取代舊一代
7. **重複** 步驟 2-6 直到收斂

### 選擇策略

| 策略 | 描述 | 特性 |
|------|------|------|
| 輪盤賭 | 機率正比於適應度 | 容易早熟 |
| 競賽選擇 | 隨機選 k 個取最佳 | 可控制選擇壓力 |
| 菁英保留 | 保留最佳 n 個個體 | 防止最佳解流失 |

### UCT 公式（探索與開發平衡）

```
UCT = Q(s,a) + C × √(ln N(s) / N(s,a))
```

C 控制探索程度，通常設為 √2。

## 使用範例

```python
from evolution.genetic_algorithm import genetic_algorithm

def fitness(genes):
    return -sum(x ** 2 for x in genes)  # 最小化 Sphere 函數

best, history = genetic_algorithm(
    n_genes=5,
    fitness_func=fitness,
    population_size=50,
    n_generations=100,
    gene_range=(-5.0, 5.0),
    seed=42,
)
```

## 複雜度

- **時間**：O(G × P × (n + f))，G 為代數，P 為族群大小，n 為基因數，f 為適應度計算成本
- **空間**：O(P × n)

## 參數建議

| 參數 | 建議 | 說明 |
|------|------|------|
| 族群大小 | 20-200 | 越大越好但越慢 |
| 交叉率 | 0.6-0.9 | 太高破壞好解，太低收斂慢 |
| 突變率 | 0.01-0.2 | 保持多樣性的關鍵 |

## 參考資料

- Holland, J. H. (1975). Adaptation in Natural and Artificial Systems.
- Goldberg, D. E. (1989). Genetic Algorithms in Search, Optimization, and Machine Learning.
