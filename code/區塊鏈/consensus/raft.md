# Raft 共識演算法

## 歷史背景

Raft 由 Diego Ongaro 和 John Ousterhout 於 2014 年在論文《In Search of an Understandable Consensus Algorithm》中提出。相較於複雜的 Paxos，Raft 設計更易理解的共識演算法，現已被 etcd、Consul 等分散式系統廣泛採用。

## 核心原理

### 領導者選舉
Raft 透過任期（Term）和心跳機制選舉領導者：
1. 追隨者（Follower）在超時後成為候選者（Candidate）
2. 候選者請求其他節點投票，獲得多數票則成為領導者（Leader）
3. 領導者定期發送心跳維持權威

### 日誌複製
所有變更都透過領導者：
1. 客戶端請求發送給領導者
2. 領導者將命令附加到日誌，複製到多數節點
3. 一旦多數節點確認，則提交並執行命令

### 安全性
Raft 保證選出的領導者擁有所有已提交的日誌條目，確保系統一致性。

## 使用範例

```python
from raft import Raft

# 建立 Raft 系統
raft = Raft(node_count=5)
print(f"節點數: {raft.node_count}")

# 執行選舉
leader = raft.run_election()
if leader:
    print(f"領導者: Node {leader.node_id}")

# 複製命令
command = "SET x = 100"
success, count = raft.replicate_command(leader, command)
print(f"複製結果: {success}, 成功節點: {count}")
```

## 參考資料

- [Raft Paper](https://raft.github.io/raft.pdf) - Ongaro & Ousterhout
- [Raft 視覺化](https://raft.github.io/)
- [In Search of an Understandable Consensus Algorithm](https://www.usenix.org/conference/atc14/technical-sessions/presentation/ongaro)
