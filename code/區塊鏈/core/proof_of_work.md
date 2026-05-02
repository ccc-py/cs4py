# 工作量證明（Proof of Work, PoW）

## 歷史背景

工作量證明概念最早由 Cynthia Dwork 和 Moni Naor 於 1993 年提出，用於防止垃圾郵件。1997 年 Adam Back 發明了 Hashcash，將 PoW 應用於郵件過濾。2008 年，中本聰在比特幣白皮書中採用 PoW 作為共識機制，讓節點透過算力競爭來產生新區塊。

## 核心原理

### Hashcash 式謎題
工作量證明要求礦工找到一個 nonce（隨機數），使得區塊雜湊值滿足特定的條件（如前 N 位為 0）。這是一個暴力搜尋的過程，沒有其他捷徑，必須嘗試大量的 nonce 值。

### 難度調整
區塊鏈系統會根據全網算力的變化，定期調整挖礦難度，目標是保持區塊產生時間的穩定性（比特幣約 10 分鐘一個區塊）。

### 安全性
由於修改區塊需要重新計算該區塊及其後所有區塊的 PoW，攻擊者需要掌握全網 51% 以上的算力才能成功竄改區塊鏈。

## 使用範例

```python
from proof_of_work import ProofOfWork
from datetime import datetime
import time

# 建立 PoW 實例
pow_algorithm = ProofOfWork(difficulty=4)
print("當前難度:", pow_algorithm.difficulty)

# 模擬挖礦
index = 1
timestamp = str(datetime.now())
data = "Alice sends 10 BTC to Bob"
prev_hash = "0" * 64

print("\n開始挖礦...")
start_time = time.time()
hash_result, nonce = pow_algorithm.mine(index, timestamp, data, prev_hash)
end_time = time.time()

print(f"挖礦成功！Nonce: {nonce}, Hash: {hash_result}")
print(f"耗時: {end_time - start_time:.2f} 秒")
```

## 參考資料

- [Bitcoin Whitepaper](https://bitcoin.org/bitcoin.pdf) - Satoshi Nakamoto
- [Hashcash](http://www.hashcash.org/) - Adam Back
- [Proof of Work - Bitcoin Wiki](https://en.bitcoin.it/wiki/Proof_of_work)
