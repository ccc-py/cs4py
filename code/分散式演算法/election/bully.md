# 分散式演算法 — Bully 演算法 (Bully Algorithm)

## 歷史背景

Bully 演算法由 Hector Garcia-Molina 於 1982 年提出，是一種在同步分散式系統中選舉領導者（leader election）的經典演算法。演算法名稱源於「霸道」的特性：優先權最高的節點會「霸凌」其他節點成為領導者。

## 核心原理

### 前提假設
- 每個節點有唯一的 ID（數值越大，優先權越高）
- 系統是同步的（訊息傳遞有時間上限）
- 節點可以知道哪些其他節點存在

### 演算法步驟
1. **發起選舉**：節點 P 向所有 ID 比自己大的節點發送 ELECTION 訊息
2. **回覆 OK**：收到 ELECTION 的節點回覆 OK，然後自己也發起選舉
3. **宣布勝利**：若 P 沒有收到任何 OK（沒有更大 ID 的節點），則宣布自己為 leader，發送 COORDINATOR 訊息
4. **接受 leader**：其他節點收到 COORDINATOR 後接受該 leader

### 複雜度
- 訊息複雜度：O(n²)（最壞情況）
- 時間複雜度：O(n)（最壞情況）

### 優缺點
**優點**：簡單易懂，保證選出 ID 最大的節點
**缺點**：訊息開銷大，需要同步假設

## 使用範例

```python
from bully import EventDrivenBully

# 創建 5 個節點
bully = EventDrivenBully([0, 1, 2, 3, 4])

# 從節點 2 發起選舉
bully.start_election(2)
bully.process_messages()

print(f"領導者: {bully.get_leader()}")  # 應該是 4
```

## 參考資料

- Garcia-Molina, H. (1982). Elections in a Distributed Computing System. IEEE Transactions on Computers.
- Tanenbaum, A. S., & Van Steen, M. (2007). Distributed Systems: Principles and Paradigms.
