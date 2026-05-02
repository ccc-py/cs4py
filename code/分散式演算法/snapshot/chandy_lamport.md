# 分散式演算法 — Chandy-Lamport 快照演算法

## 歷史背景

Chandy-Lamport 演算法由 K. Mani Chandy 和 Leslie Lamport 於 1985 年在論文 "Distributed Snapshots: Determining Global States of Distributed Systems" 中提出。這是分散式系統中取得全域一致快照的經典演算法。

## 核心原理

### 問題定義
在分散式系統中，每個行程有自己的狀態，通道中有在途訊息。目標是取得一個**全域一致的快照**（consistent global state）。

### 演算法步驟
1. **發起者**：記錄本地狀態，向所有輸出通道發送 MARKER 訊息
2. **接收者收到 MARKER**：
   - 若是第一次收到 MARKER：記錄本地狀態，轉發 MARKER 到其餘通道
   - 否則：記錄該通道的訊息狀態
3. **終止**：當所有行程都收到來自所有輸入通道的 MARKER

### 一致性保證
- 快照包含的訊息：在 marker 之前發送、且在 marker 之後到達的訊息
- 確保**沒有 orphan 訊息**（發送者狀態在快照中，但接收者不在）

### 通道狀態
通道狀態 = 在 marker 發送後、接收前，通過該通道的訊息集合

## 使用範例

```python
from chandy_lamport import ChandyLamportSnapshot

# 建立系統
snapshot = ChandyLamportSnapshot([0, 1, 2])

# 設定狀態
snapshot.processes[0].set_state(100)

# 發起快照
snapshot.initiate(initiator_id=0)
snapshot.deliver_all_markers()

# 取得結果
state, channels = snapshot.processes[0].get_snapshot()
```

## 參考資料

- Chandy, K. M., & Lamport, L. (1985). Distributed Snapshots: Determining Global States of Distributed Systems. ACM Transactions on Computer Systems.
- Tanenbaum, A. S., & Van Steen, M. (2007). Distributed Systems: Principles and Paradigms.
