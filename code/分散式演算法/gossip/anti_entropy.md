# 分散式演算法 — 反熵同步 (Anti-Entropy)

## 歷史背景

反熵（Anti-Entropy）同步由 Amazon 的 Dynamo 論文（2007）推廣，用於分散式資料庫的副本同步。名稱源於資訊論中的「熵」概念：系統透過同步來降低資料不一致的「熵」。

## 核心原理

### 基本想法
節點定期隨機選擇其他節點進行同步，交換資料差異並修復不一致。

### 三種策略
1. **Push**：節點 A 主動將自己的資料推送給 B
2. **Pull**：節點 A 向 B 請求資料，然後更新自己
3. **Push-Pull**（推薦）：兩者結合，收斂最快

### 同步過程
1. 節點選擇隨機鄰居
2. 交換摘要（digest）：鍵到版本的映射
3. 比較摘要，找出差異
4. 傳輸缺失/過期的資料

### 應用場景
- **Dynamo/Cassandra**：副本同步
- **網路分區恢復**：分區後修復資料
- **最終一致性**：保證系統最終達到一致

### 收斂速度
- Push 或 Pull 單獨：O(log n) 輪
- Push-Pull：O(log n) 輪，但常數更小

## 使用範例

```python
from anti_entropy import AntiEntropy

# 建立系統
ae = AntiEntropy(list(range(5)))

# 寫入資料
ae.write_data(0, "key1", "value1")

# 執行反熵同步
ae.run_round('push-pull')
```

## 參考資料

- DeCandia, G., et al. (2007). Dynamo: Amazon's Highly Available Key-value Store. SOSP.
- Lakshman, A., & Malik, P. (2010). Cassandra: A Decentralized Structured Storage System. ACM SIGOPS.
