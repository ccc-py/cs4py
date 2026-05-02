# 分散式演算法 — Gossip 協定 (Gossip Protocol)

## 歷史背景

Gossip 協定（又稱流行病協定，Epidemic Protocol）起源於 1980 年代分散式資料庫的研究。名稱源於其類似流行病傳播的方式。現代應用包括 Amazon Dynamo、Cassandra、Redis Cluster 等分散式系統。

## 核心原理

### 基本模式
每個節點週期性地：
1. 隨機選擇 k 個鄰居（fanout）
2. 將自己的狀態/資訊傳給它們
3. 鄰居收到後也做同樣的事

### 傳播過程
- **Round 1**：初始節點傳給 k 個鄰居（共 k+1 個知道）
- **Round 2**：這 k+1 個節點各傳給 k 個（約 k²+k+1 個知道）
- **Round r**：覆蓋約 kʳ 個節點

### 收斂速度
- O(log n) 輪可覆蓋所有 n 個節點
- 實際系統中通常 3-7 輪即可

### 變體
- **Push**：只推播（如上所述）
- **Pull**：只拉取
- **Push-Pull**：兩者結合（更快收斂）

## 使用範例

```python
from gossip_protocol import GossipProtocol

# 建立 gossip 系統
gossip = GossipProtocol(list(range(20)), fanout=3)

# 加入初始資訊
gossip.add_initial_data(0, "新聞A")

# 執行傳播
gossip.run_until_converged(target_coverage=0.9)
```

## 參考資料

- Demers, A., et al. (1987). Epidemic Algorithms for Replicated Database Maintenance. PODC.
- van Renesse, R., et al. (1998). Gossip-Based Peer Sampling. ACM TOCS.
