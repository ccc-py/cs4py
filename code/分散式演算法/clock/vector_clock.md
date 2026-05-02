# 分散式演算法 — 向量時鐘 (Vector Clock)

## 歷史背景

向量時鐘由 Colin Fidge 和 Friedemann Mattern 於 1988 年左右獨立提出，是對 Lamport 邏輯時鐘的改進。向量時鐘可以捕捉分散式系統中的因果關係，區分因果相關事件和並發事件。

## 核心原理

### 向量時鐘結構
每個節點維護一個向量 V[n]（n = 節點數）：
- V[i]：節點 i 已知的最高事件計數

### 更新規則
1. **本地事件**：V[node] += 1
2. **發送訊息**：V[node] += 1，附帶 V 到訊息
3. **接收訊息**：對所有 i，V[i] = max(V[i], msg_V[i])，然後 V[node] += 1

### 比較關係
對於向量 V1, V2：
- **V1 < V2**：∀i, V1[i] ≤ V2[i]，且 ∃i, V1[i] < V2[i]
- **V1 = V2**：∀i, V1[i] = V2[i]
- **並發 (V1 | V2)**：¬(V1 < V2) ∧ ¬(V2 < V1)

### 因果關係
- 若 V1 < V2，則事件 1 因果先於事件 2
- 若 V1 | V2，則兩事件**並發**（concurrent）

### 應用
- 分散式資料庫（Amazon Dynamo）
- 版本向量（Version Vectors）
- 衝突解決

## 使用範例

```python
from vector_clock import VectorClockSystem, compare_vectors

# 建立系統
system = VectorClockSystem([0, 1, 2])

# 模擬事件
system.nodes[0].local_event("任務開始")
system.send_message(0, 1, "資料")
system.deliver_messages()

# 比較向量
v1 = system.nodes[0].get_vector()
v2 = system.nodes[1].get_vector()
print(compare_vectors(v1, v2))  # '<' 或 '|'
```

## 參考資料

- Fidge, C. J. (1988). Timestamps in Message-Passing Systems That Preserve the Partial Ordering.
- Mattern, F. (1989). Virtual Time and Global States of Distributed Systems.
