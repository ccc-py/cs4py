# 分散式演算法 — 環狀選舉演算法 (Ring Election Algorithm)

## 歷史背景

環狀選舉演算法（也稱為 Chang-Roberts 演算法）由 Er-Chang Chang 和 Roseelia Roberts 於 1979 年提出。該演算法假設系統中的節點邏輯上排列成一個環，訊息沿著環單向傳遞。

## 核心原理

### 演算法設定
- 節點按 ID 排序形成邏輯環
- 每個節點只知道下一個節點是誰
- 訊息沿環順時針傳遞

### 選舉過程
1. **發起選舉**：節點 P 向鄰居發送 ELECTION(id(P)) 訊息
2. **轉發規則**：
   - 收到 ELECTION(x) 時，若 x > id(P)，轉發該訊息
   - 若 x < id(P)，用 id(P) 替換後轉發
   - 若 x == id(P)，P 當選 leader
3. **通知**：leader 發送 COORDINATOR 訊息繞環通知

### 複雜度
- 訊息複雜度：O(n²)（最壞情況），O(n log n)（平均）
- 時間複雜度：O(n)（訊息傳播時間）

### 改進版本
- 使用逾時機制避免重複訊息
- 只在收到比自己大的 ID 時才轉發

## 使用範例

```python
from ring import RingElection

# 創建環狀拓撲
ring = RingElection([0, 1, 2, 3, 4])

# 發起選舉
leader = ring.simulate_full_election(2)
print(f"領導者: {leader}")  # 應該是 4
```

## 參考資料

- Chang, E., & Roberts, R. (1979). An Improved Algorithm for Decentralized Extrema-Finding in Circular Configurations. Communications of the ACM.
- Tanenbaum, A. S., & Van Steen, M. (2007). Distributed Systems: Principles and Paradigms.
