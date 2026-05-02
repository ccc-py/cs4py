# Paxos 共識演算法

## 歷史背景

Paxos 由 Leslie Lamport 於 1998 年在論文《The Part-Time Parliament》中提出。這是第一個被證明正確的共識演算法，廣泛應用於分散式系統（如 Google Chubby）。由於論文以希臘議會故事形式撰寫，初期難以理解，後來才有更清晰的說明版本。

## 核心原理

### 三種角色
1. **Proposer（提議者）**：提出議案，推動共識達成
2. **Acceptor（接受者）**：決定是否接受議案，可投票
3. **Learner（學習者）**：學習已達成共識的值

### 兩階段協議
1. **Prepare/Promise 階段**：
   - 提議者發送 prepare(n) 給多數接受者
   - 接受者若 n 大於已承諾的編號，則回傳 promise，並承諾不再接受編號小於 n 的議案

2. **Accept/Accepted 階段**：
   - 提議者收到多數 promise 後，發送 accept(n, value)
   - 接受者若 n ≥ 已承諾編號，則接受該議案
   - 一旦多數接受者接受，共識達成

### 安全性
Paxos 保證：如果一個值被選定，後續所有選定的值都必須是同一個值。

## 使用範例

```python
from paxos import Paxos

# 建立 Paxos 系統
paxos = Paxos(proposer_count=1, acceptor_count=3, learner_count=1)

# 執行共識
proposer = paxos.proposers[0]
value = "SET x = 100"
success, result = paxos.run_paxos(proposer, value, round_num=1)

print(f"共識結果: {success}")
print(f"選定值: {result}")
```

## 參考資料

- [The Part-Time Parliament](https://lamport.azurewebsites.net/pubs/lamport-paxos.pdf) - Leslie Lamport
- [Paxos Made Simple](https://lamport.azurewebsites.net/pubs/paxos-simple.pdf) - Leslie Lamport
- [Paxos - Wikipedia](https://en.wikipedia.org/wiki/Paxos_(computer_science))
