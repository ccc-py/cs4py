# 實用拜占庭容錯（PBFT）

## 歷史背景

PBFT 由 Miguel Castro 和 Barbara Liskov 於 1999 年在論文《Practical Byzantine Fault Tolerance》中提出。它是第一個能在異步網路環境下實用化的拜占庭容錯演算法，被廣泛應用於聯盟鏈（如 Hyperledger Fabric）中。

## 核心原理

### 拜占庭將軍問題
系統中可能存在惡意節點（拜占庭節點），它們會發送錯誤訊息或合謀攻擊。PBFT 能在總節點數 n ≥ 3f+1 的情況下，容忍 f 個拜占庭節點。

### 三階段協議
1. **Pre-prepare**：主節點（Primary）將客戶端請求分配序號，發送 pre-prepare 訊息給所有備份節點
2. **Prepare**：備份節點驗證後發送 prepare 訊息，收集 2f 個 prepare 後進入 prepared 狀態
3. **Commit**：節點發送 commit 訊息，收集 2f+1 個 commit 後執行請求並回覆客戶端

### 視圖變更
若主節點失效或作惡，系統會觸發視圖變更（View Change），選舉新的主節點。

## 使用範例

```python
from pbft import PBFT

# 建立 PBFT 系統：4 個節點，容忍 1 個拜占庭節點
pbft = PBFT(node_count=4, byzantine_nodes=[3])

# 執行共識
request = "Transfer 10 BTC from Alice to Bob"
success, result = pbft.run_consensus(request)

print(f"共識結果: {'成功' if success else '失敗'}")
print(f"Prepare 數: {result['prepare_count']}")
print(f"Commit 數: {result['commit_count']}")
```

## 參考資料

- [PBFT Paper](http://pmg.csail.mit.edu/papers/osdi99.pdf) - Castro & Liskov
- [Byzantine Fault Tolerance](https://en.wikipedia.org/wiki/Byzantine_fault)
- [Hyperledger Fabric Consensus](https://hyperledger-fabric.readthedocs.io/)
