# 分散式演算法 — 三階段提交 (Three-Phase Commit, 3PC)

## 歷史背景

三階段提交（3PC）是對兩階段提交（2PC）的改進，由 Dale Skeen 和 Michael Stonebraker 於 1983 年在論文 "A Formal Model of Crash Recovery in a Distributed System" 中提出。主要解決 2PC 的阻塞問題。

## 核心原理

### 三個階段
1. **CAN COMMIT**（類似 2PC 的 PREPARE）
   - 協調者詢問所有參與者是否可以提交
   - 參與者回覆 YES 或 NO
   
2. **PRE-COMMIT**
   - 若所有 YES，協調者發送 PRE-COMMIT
   - 參與者確認並進入 PRE-COMMITTED 狀態
   
3. **DO-COMMIT**
   - 協調者發送 COMMIT
   - 參與者提交並回覆 ACK

### 狀態轉換
```
INIT → VOTING → PRE_COMMITTED → COMMITTED
                 ↓
              ABORTED
```

### 非阻塞特性
- 若協調者在第一階段失效：參與者逾時後中止
- 若協調者在第二階段失效：參與者已有 PRE-COMMIT 狀態，可詢問其他節點決定
- 若協調者在第三階段失效：參與者直接提交

### 限制
- 假設網路可靠（無網路分區）
- 需要準確的逾時機制

## 使用範例

```python
from three_phase_commit import ThreePhaseCommit

# 建立 3PC
tpc = ThreePhaseCommit(coordinator_id=0, participant_ids=[1, 2, 3])

# 執行交易
success, msg = tpc.execute_transaction()
print(f"結果: {msg}")
```

## 參考資料

- Skeen, D., & Stonebraker, M. (1983). A Formal Model of Crash Recovery in a Distributed System. IEEE Transactions on Software Engineering.
- Lamport, L. (1998). The Part-Time Parliament. ACM Transactions on Computer Systems.
