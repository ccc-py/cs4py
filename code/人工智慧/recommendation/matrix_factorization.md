# 矩陣分解推薦 (Matrix Factorization)

## 歷史背景

矩陣分解技術在推薦系統中的應用可以追溯到 2000 年代初期。2006 年，Netflix 發起了著名的 Netflix Prize 競賽，提供 100 萬美元獎金給能夠將推薦準確度提升 10% 的團隊。這場競賽極大地推動了矩陣分解技術的發展。

最終獲勝的 BellKor's Pragmatic Chaos 團隊使用了多種矩陣分解方法的集成，包括 SVD（奇異值分解）、PMF（概率矩陣分解）等。自此，矩陣分解成為推薦系統的核心技術之一。

## 核心原理

### 1. 低秩矩陣分解

將用戶-物品評分矩陣 $R$ 分解為兩個低維矩陣的乘積：
$$R \approx U \times V^T$$

其中：
- $U \in \mathbb{R}^{m \times k}$ 是用戶潛在因子矩陣
- $V \in \mathbb{R}^{n \times k}$ 是物品潛在因子矩陣
- $k$ 是潛在因子維度（通常遠小於 $m$ 和 $n$）

### 2. 優化目標

最小化平方誤差加上正則化項：
$$\min_{U,V} \sum_{(u,i) \in \mathcal{K}} (r_{ui} - \mathbf{u}_u^T \mathbf{v}_i)^2 + \lambda(\|\mathbf{u}_u\|^2 + \|\mathbf{v}_i\|^2)$$

其中 $\mathcal{K}$ 是已知評分的集合，$\lambda$ 是正則化參數。

### 3. 隨機梯度下降

對於每個已知評分 $(u, i, r_{ui})$：
$$\mathbf{u}_u \leftarrow \mathbf{u}_u + \gamma (e_{ui} \cdot \mathbf{v}_i - \lambda \mathbf{u}_u)$$
$$\mathbf{v}_i \leftarrow \mathbf{v}_i + \gamma (e_{ui} \cdot \mathbf{u}_u - \lambda \mathbf{v}_i)$$

其中 $e_{ui} = r_{ui} - \mathbf{u}_u^T \mathbf{v}_i$ 是預測誤差，$\gamma$ 是學習率。

### 4. 預測

用戶 $u$ 對物品 $i$ 的預測評分為：
$$\hat{r}_{ui} = \mathbf{u}_u^T \mathbf{v}_i = \sum_{f=1}^k u_{uf} \cdot v_{if}$$

## 使用範例

```python
from matrix_factorization import train_sgd, predict_rating_mf, top_n_recommendations_mf

# 評分數據
ratings = {
    1: {101: 5, 102: 3, 103: 4, 104: 2},
    2: {101: 4, 102: 5, 103: 3, 105: 4},
    3: {101: 2, 102: 4, 104: 5, 105: 3},
    4: {102: 2, 103: 5, 104: 4, 105: 5}
}

# 訓練模型
users = sorted(ratings.keys())
items = sorted(set(i for r in ratings.values() for i in r))
user_index = {u: i for i, u in enumerate(users)}
item_index = {i: idx for idx, i in enumerate(items)}
user_factors, item_factors = train_sgd(ratings, num_factors=5, num_epochs=20)

# 預測評分
pred = predict_rating_mf(1, 105, user_factors, item_factors, user_index, item_index)
print(f"預測用戶1對物品105的評分: {pred:.2f}")

# Top-N推薦
recs = top_n_recommendations_mf(1, ratings, user_factors, item_factors, user_index, item_index, n=3)
print(f"用戶1的Top-3推薦: {recs}")
```

## 參考資料

1. Koren, Y., Bell, R., & Volinsky, C. (2009). Matrix factorization techniques for recommender systems. *Computer*, 42(8), 30-37.
2. Salakhutdinov, R., & Mnih, A. (2008). Probabilistic matrix factorization. *NIPS*, 20, 1257-1264.
3. Funk, S. (2006). Netflix Update: Try This at Home. *sifter.org*.
