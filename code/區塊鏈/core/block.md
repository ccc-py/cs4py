# 區塊與區塊鏈結構

## 歷史背景

區塊鏈技術由中本聰於 2008 年在《Bitcoin: A Peer-to-Peer Electronic Cash System》論文中首次提出。區塊鏈是一種去中心化的分散式帳本技術，透過密碼學方法將資料區塊按時間順序連接，形成不可竄改的鏈式結構。

## 核心原理

### 區塊結構
每個區塊包含以下核心欄位：
- **index**: 區塊序號
- **timestamp**: 時間戳記
- **data**: 區塊儲存的資料（交易資訊）
- **prev_hash**: 前一個區塊的雜湊值
- **nonce**: 隨機數（用於工作量證明）
- **hash**: 本區塊的雜湊值

### 鏈式結構
每個區塊透過 `prev_hash` 指向前一個區塊，形成不可中斷的鏈。任何對歷史區塊的竄改都會導致後續所有區塊的雜湊值失效，從而被檢測出來。

### 驗證機制
區塊鏈的有效性透過以下方式驗證：
1. 檢查每個區塊的雜湊值是否正確計算
2. 檢查每個區塊的 `prev_hash` 是否與前一區塊的 `hash` 相符

## 使用範例

```python
from block import Blockchain

# 創建區塊鏈
my_blockchain = Blockchain()
print("創建創世區塊:", my_blockchain.get_latest_block())

# 新增區塊
my_blockchain.add_block({"amount": 10, "sender": "Alice", "receiver": "Bob"})
my_blockchain.add_block({"amount": 20, "sender": "Bob", "receiver": "Charlie"})

# 驗證區塊鏈
print("區塊鏈長度:", len(my_blockchain.chain))
print("區塊鏈是否有效:", my_blockchain.is_chain_valid())

# 竄改測試
my_blockchain.chain[1].data = {"amount": 100, "sender": "Alice", "receiver": "Bob"}
print("竄改後區塊鏈是否有效:", my_blockchain.is_chain_valid())
```

## 參考資料

- [Bitcoin Whitepaper](https://bitcoin.org/bitcoin.pdf) - Satoshi Nakamoto
- [區塊鏈技術指南](https://github.com/yeasy/blockchain_guide)
- [Mastering Bitcoin](https://github.com/bitcoinbook/bitcoinbook) - Andreas M. Antonopoulos
