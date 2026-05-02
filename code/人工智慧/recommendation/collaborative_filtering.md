# 用戶基協同過濾 (User-based Collaborative Filtering)

## 歷史背景

協同過濾 (Collaborative Filtering) 是推薦系統中最經典且廣泛使用的技術之一。該概念最早由 Goldberg 等人在 1992 年提出，應用於 Tapestry 系統中。隨後在 1990 年代末期，隨著 Amazon、Netflix 等電子商務平台的興起，協同過濾技術得到了廣泛的應用與發展。

用戶基協同過濾的核心思想是「物以類聚，人以群分」：相似用戶對同一物品會有相似的評分。Amazon 的「購買此商品的用戶也購買了...」就是協同過濾的典型應用。

## 核心原理

### 1. 相似度計算

協同過濾依賴於用戶之間的相似度計算，常用方法有：

**餘弦相似度 (Cosine Similarity)**
$$\text{sim}(u,v) = \frac{\mathbf{u} \cdot \mathbf{v}}{\|\mathbf{u}\| \|\mathbf{v}\|} = \frac{\sum_i r_{ui} \cdot r_{vi}}{\sqrt{\sum_i r_{ui}^2} \cdot \sqrt{\sum_i r_{vi}^2}}$$

**皮爾森相關係數 (Pearson Correlation)**
$$\text{sim}(u,v) = \frac{\sum_i (r_{ui} - \bar{r}_u)(r_{vi} - \bar{r}_v)}{\sqrt{\sum_i (r_{ui} - \bar{r}_u)^2} \cdot \sqrt{\sum_i (r_{vi} - \bar{r}_v)^2}}$$

### 2. 評分預測

對於用戶 $u$ 對物品 $i$ 的評分預測：
$$\hat{r}_{ui} = \frac{\sum_{v \in N(u)} \text{sim}(u,v) \cdot r_{vi}}{\sum_{v \in N(u)} |\text{sim}(u,v)|}$$

其中 $N(u)$ 為與用戶 $u$ 最相似且對物品 $i$ 有評分的用戶集合。

### 3. Top-N 推薦

對所有未評分物品進行預測，選取預測評分最高的 N 個物品推薦給用戶。

## 使用範例

```python
from collaborative_filtering import cosine_similarity, predict_rating, top_n_recommendations

# 定義用戶-物品評分矩陣
ratings = {
    1: {101: 5, 102: 3, 103: 4, 104: 2},
    2: {101: 4, 102: 5, 103: 3, 105: 4},
    3: {101: 2, 102: 4, 104: 5, 105: 3},
    4: {102: 2, 103: 5, 104: 4, 105: 5}
}

# 計算用戶1和用戶2的相似度
sim = cosine_similarity(ratings[1], ratings[2])
print(f"用戶1和用戶2的餘弦相似度: {sim:.3f}")

# 預測用戶1對物品105的評分
pred = predict_rating(1, 105, ratings)
print(f"預測用戶1對物品105的評分: {pred:.2f}")

# 生成Top-3推薦
recommendations = top_n_recommendations(1, ratings, n=3)
print(f"用戶1的Top-3推薦: {recommendations}")
```

## 參考資料

1. Goldberg, D., Nichols, D., Oki, B. M., & Terry, D. (1992). Using collaborative filtering to weave an information tapestry. *Communications of the ACM*, 35(12), 61-70.
2. Resnick, P., Iacovou, N., Suchak, M., Bergstrom, P., & Riedl, J. (1994). GroupLens: an open architecture for collaborative filtering of netnews. *CSCW*, 175-186.
3. Sarwar, B., Karypis, G., Konstan, J., & Riedl, J. (2001). Item-based collaborative filtering recommendation algorithms. *WWW*, 285-295.
