# 內容基推薦 (Content-based Recommendation)

## 歷史背景

內容基推薦是推薦系統最早的方法之一，其思想源於信息檢索領域。早在 1990 年代，研究人員就開始利用物品的文本內容、屬性等特徵來進行推薦。

與協同過濾不同，內容基推薦不依賴其他用戶的行為數據，而是基於物品本身的特徵和用戶的歷史偏好來構建推薦。這種方法特別適合冷啟動場景（新用戶或新物品）。

著名的應用包括新聞推薦系統（如 Google News）、音樂推薦（基於歌曲特徵）等。

## 核心原理

### 1. 物品特徵提取

將物品轉換為特徵向量，常用方法包括：

- **TF-IDF**：衡量詞語在文檔中的重要性
  $$\text{TF-IDF}(t, d) = \text{TF}(t, d) \times \text{IDF}(t)$$
  其中 $\text{IDF}(t) = \log \frac{N}{df_t}$，$N$ 是文檔總數，$df_t$ 是包含詞語 $t$ 的文檔數。

### 2. 用戶畫像構建

基於用戶過去喜歡的物品，構建用戶的興趣畫像：
$$\mathbf{p}_u = \frac{1}{|L_u|} \sum_{i \in L_u} \mathbf{x}_i$$

其中 $L_u$ 是用戶 $u$ 喜歡的物品集合，$\mathbf{x}_i$ 是物品 $i$ 的特徵向量。

### 3. 相似度匹配

計算用戶畫像與候選物品的相似度，常用餘弦相似度：
$$\text{sim}(\mathbf{p}_u, \mathbf{x}_i) = \frac{\mathbf{p}_u \cdot \mathbf{x}_i}{\|\mathbf{p}_u\| \|\mathbf{x}_i\|}$$

### 4. 推薦生成

選取相似度最高的 N 個物品推薦給用戶。

## 使用範例

```python
from content_based import compute_tfidf, build_user_profile, recommend_items

# 物品描述
items = [
    "action adventure hero save world",
    "romance love story couple happy ending",
    "action combat fight battle warrior",
    "comedy funny joke laugh entertainment",
    "romance drama emotional relationship",
    "adventure exploration discover treasure map"
]
item_ids = [101, 102, 103, 104, 105, 106]

# 計算TF-IDF特徵
features, vocab = compute_tfidf(items)
print(f"詞彙表大小: {len(vocab)}")

# 用戶喜歡的物品索引
liked_indices = [0, 2]  # 喜歡動作冒險類
profile = build_user_profile(liked_indices, features)

# 生成推薦
recommendations = recommend_items(profile, features, item_ids, liked_indices, n=3)
print(f"推薦物品ID: {recommendations}")
```

## 參考資料

1. Pazzani, M. J., & Billsus, D. (2007). Content-based recommendation systems. *The adaptive web*, 325-341.
2. Lops, P., de Gemmis, M., & Semeraro, G. (2011). Content-based recommender systems: State of the art and trends. *Recommender systems handbook*, 73-105.
3. Salton, G., & Buckley, C. (1988). Term-weighting approaches in automatic text retrieval. *Information processing & management*, 24(5), 513-523.
