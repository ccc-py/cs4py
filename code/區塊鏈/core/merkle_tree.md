# Merkle Tree（默克爾樹）

## 歷史背景

默克爾樹由 Ralph Merkle 於 1979 年提出，首次出現在《A Digital Signature Based on a Conventional Encryption Function》論文中。比特幣區塊頭中包含默克爾根，用於高效驗證區塊內交易的存在性，無需下載完整區塊資料。

## 核心原理

### 樹狀結構
默克爾樹是一種二元雜湊樹：
1. 葉節點是資料的雜湊值
2. 內部節點是其兩個子節點組合後的雜湊值
3. 根節點（默克爾根）代表所有資料的摘要

### 包含證明
透過提供從目標葉節點到根節點路徑上的所有兄弟節點雜湊值，可以在 O(log n) 時間內驗證某筆交易是否存在於樹中，而無需擁有完整的交易列表。

### 應用場景
- 比特幣區塊中的交易驗證
- IPFS 等分散式系統的資料完整性驗證
- 輕量級客戶端（SPV 客戶端）

## 使用範例

```python
from merkle_tree import MerkleTree

# 建立交易資料的默克爾樹
transactions = ["tx1", "tx2", "tx3", "tx4"]
merkle_tree = MerkleTree(transactions)

print("默克爾根:", merkle_tree.get_root())

# 取得包含證明
proof = merkle_tree.get_proof("tx2")
print("tx2 的證明:", proof)
print("驗證 tx2:", merkle_tree.verify_proof("tx2", proof, merkle_tree.get_root()))
```

## 參考資料

- [Merkle Tree - Wikipedia](https://en.wikipedia.org/wiki/Merkle_tree)
- [Bitcoin Developer Guide - Merkle Trees](https://developer.bitcoin.org/devguide/block_chain.html)
- [Ralph Merkle's Original Paper](https://www.merkle.com/papers/CSUR1989.pdf)
