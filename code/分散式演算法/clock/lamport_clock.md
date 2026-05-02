# 分散式演算法 — Lamport 邏輯時鐘 (Lamport Clock)

## 歷史背景

Lamport 邏輯時鐘由 Leslie Lamport 於 1978 年在論文 "Time, Clocks, and the Ordering of Events in a Distributed System" 中提出。這是分散式系統中事件排序的奠基性工作，引入了「happens-before」關係的概念。

## 核心原理

### Happens-Before 關係 (→)
對於事件 a, b：
1. 若 a, b 在同一節點且 a 先發生，則 a → b
2. 若 a 是發送訊息事件，b 是接收該訊息事件，則 a → b
3. 若 a → b 且 b → c，則 a → c

### Lamport 時鐘規則
每個節點維護一個計數器 C：
1. **本地事件**：C = C + 1
2. **發送訊息**：C = C + 1，附帶 C 到訊息中
3. **接收訊息**：C = max(C, msg_timestamp) + 1

### 特性
- 若 a → b，則 time(a) < time(b)
- 反之不成立（time(a) < time(b) 不代表 a → b）
- 提供**全序**（total order），但無法分辨並發事件

### 應用
- 分散式系統事件日誌
- 狀態機複製（決定順序）
- 全域快照的基礎

## 使用範例

```python
from lamport_clock import DistributedSystem

# 建立系統
system = DistributedSystem([0, 1, 2])

# 模擬事件
system.nodes[0].local_event("任務開始")
system.send_message(0, 1, "資料")
system.deliver_messages()

# 查看全域事件順序
events = system.get_all_events()
for nid, desc, time, _ in events:
    print(f"[{time}] 節點 {nid}: {desc}")
```

## 參考資料

- Lamport, L. (1978). Time, Clocks, and the Ordering of Events in a Distributed System. Communications of the ACM.
- Tanenbaum, A. S., & Van Steen, M. (2007). Distributed Systems: Principles and Paradigms.
