# 粒子群優化演算法 (Particle Swarm Optimization)

## 歷史背景

1995 年 James Kennedy（社會心理學家）和 Russell Eberhart（電機工程師）在普渡大學共同提出 PSO。靈感來自對鳥群覓食行為的模擬：鳥群不知道食物在哪裡，但知道離食物有多遠，透過追蹤離食物最近的鳥來尋找食物。

PSO 屬於群體智能（Swarm Intelligence）的範疇，與遺傳演算法同為演化計算的重要分支，但 PSO 沒有交叉和突變操作，而是透過速度更新實現搜尋。

## 核心原理

### 速度更新公式

```
v(t+1) = w·v(t) + c1·r1·(pbest - x) + c2·r2·(gbest - x)
x(t+1) = x(t) + v(t+1)
```

### 參數意義

| 參數 | 名稱 | 作用 |
|------|------|------|
| w | 慣性權重 | 保持原有運動趨勢，全局探索 |
| c1 | 個體學習因子 | 向自身歷史最佳位置移動 |
| c2 | 群體學習因子 | 向群體歷史最佳位置移動 |
| r1, r2 | 隨機數 | 引入隨機性，避免早熟 |

### 演算法流程

1. 初始化粒子群（隨機位置和速度）
2. 評估每個粒子的適應度
3. 更新個體最佳 (pbest) 和群體最佳 (gbest)
4. 更新每個粒子的速度和位置
5. 重複步驟 2-4 直到收斂

### 參數調優建議

| 參數 | 建議值 | 說明 |
|------|--------|------|
| w | 0.4-0.9 | 可線性遞減：w = w_max - (w_max-w_min)·t/T |
| c1, c2 | 1.5-2.0 | 通常設為相等 |
| 粒子數 | 20-50 | 依問題維度調整 |

## 使用範例

```python
from evolution.particle_swarm import particle_swarm_optimization

def fitness(x):
    return x[0]**2 + x[1]**2  # Sphere 函數

best_pos, best_fit, history = particle_swarm_optimization(
    n_dims=2,
    fitness_func=fitness,
    n_particles=30,
    n_iterations=100,
    bounds=(-5.0, 5.0),
    seed=42,
)
```

## 與遺傳演算法比較

| 特性 | PSO | 遺傳演算法 |
|------|-----|-----------|
| 操作 | 速度更新 | 交叉、突變 |
| 記憶 | 保留 pbest/gbest | 無記憶 |
| 編碼 | 實數 | 二進制/實數 |
| 收斂速度 | 較快 | 較慢 |
| 跳脫局部最佳 | 較弱 | 較強（突變） |

## 參考資料

- Kennedy, J., & Eberhart, R. (1995). Particle swarm optimization. IEEE International Conference on Neural Networks.
- Poli, R., Kennedy, J., & Blackwell, T. (2007). Particle swarm optimization. Swarm Intelligence.
