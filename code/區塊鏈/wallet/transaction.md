# 區塊鏈交易結構（UTXO 模型）

## 歷史背景

比特幣採用 UTXO（Unspent Transaction Output，未花費交易輸出）模型來追蹤代幣的所有權。不同於帳戶餘額模型，UTXO 模型類似實體現金：每筆交易消耗先前的輸出，並產生新的輸出。以太坊則採用帳戶模型。

## 核心原理

### UTXO 模型
- **交易輸入**：引用先前交易的輸出（txid + output_index）
- **交易輸出**：指定接收者地址與金額
- **未花費輸出**：尚未被後續交易引用的輸出

### 交易驗證
1. 檢查輸入的 UTXO 是否存在且未被花費
2. 驗證每個輸入的簽章（證明擁有權）
3. 檢查輸入總額 ≥ 輸出總額（差值為手續費）

### Coinbase 交易
每個區塊的第一筆交易是 Coinbase 交易，沒有輸入，用於創造新幣（區塊獎勵）給礦工。

## 使用範例

```python
from transaction import Transaction, TransactionInput, TransactionOutput, UTXOSet

# 建立 UTXO 集合
utxo_set = UTXOSet()

# Coinbase 交易（挖礦獎勵）
coinbase = Transaction(inputs=[], outputs=[TransactionOutput("Alice", 50.0)])
utxo_set.process_transaction(coinbase)

# Alice 發送 30 給 Bob
tx_input = TransactionInput(coinbase.txid, 0)
tx = Transaction(
    inputs=[tx_input],
    outputs=[
        TransactionOutput("Bob", 30.0),
        TransactionOutput("Alice", 20.0)  # 找零
    ]
)

# 簽署並驗證
tx.sign_input(0, "alice_private_key")
print(f"驗證: {tx.verify_input(0, 'alice_public_key')}")
```

## 參考資料

- [Bitcoin Transactions](https://bitcoin.org/en/developer-guide#transactions)
- [UTXO Model](https://en.bitcoin.it/wiki/Transaction)
- [Mastering Bitcoin - Transactions](https://github.com/bitcoinbook/bitcoinbook)
