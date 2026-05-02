# 分散式演算法 — 兩階段提交 (Two-Phase Commit, 2PC)

## 歷史背景

兩階段提交協定（2PC）是分散式資料庫和交易中保證原子性的經典協定。由 Jim Gray 於 1978 年在論文 "Notes on Database Operating Systems" 中形式化描述。

## 核心原理

### 參與角色
- **協調者 (Coordinator)**：負責決策的中心節點
- **參與者 (Participants)**：執行交易的節點

### 第一階段：準備 (PREPARE)
1. 協調者向所有參與者發送 PREPARE
2. 參與者執行交易但不提交，回覆 YES 或 NO

### 第二階段：決策 (DECIDE)
1. 若所有參與者回覆 YES → 發送 COMMIT
2. 若有任何 NO → 發送 ABORT
3. 參與者執行決策並回覆 ACK

### 狀態轉換
```
INIT → VOTING → COMMITTED / ABORTED
```

### 缺點（阻塞問題）
- 協調者失效會導致參與者無限期等待
- 無逾時機制，是**阻塞式**協定
- 需要日誌記錄以處理崩潰恢復

## 使用範例

```python
from two_phase_commit import TwoPhaseCommit

# 建立 2PC
tpc = TwoPhaseCommit(coordinator_id=0, participant_ids=[1, 2, 3])

# 執行交易
success, msg = tpc.execute_transaction()
print(f"結果: {msg}")
```

## 參考資料

- Gray, J. (1978). Notes on Database Operating Systems. Springer.
- Bernstein, P. A., Hadzilacos, V., & Goodman, N. (1987). Concurrency Control and Recovery in Database Systems.
