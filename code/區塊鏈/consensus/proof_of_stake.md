# 權益證明（Proof of Stake, PoS）

## 歷史背景

權益證明最早由 Sunny King 和 Scott Nadal 於 2012 年在 Peercoin 中實作。不同於 PoW 靠算力競爭，PoS 根據參與者持有的加密貨幣數量（權益）來選擇區塊生產者。以太坊於 2022 年完成合併（The Merge），從 PoW 轉為 PoS 共識機制。

## 核心原理

### 驗證者選擇
驗證者（Validator）質押代幣成為候選人，系統根據權益大小給予相應的被選中機率。權益越高，被選為下一個區塊生產者的機率越大。

### 優勢
- 能源消耗遠低於 PoW
- 攻擊成本更高（需要持有 51% 的代幣）
- 區塊生產更穩定

### 懲罰機制
若驗證者作惡或離線，其質押的代幣會被部分沒收（Slashing），以確保誠實行為。

## 使用範例

```python
from proof_of_stake import ProofOfStake

# 建立 PoS 系統
pos = ProofOfStake()

# 新增驗證者
pos.add_validator("Alice", 100.0)
pos.add_validator("Bob", 200.0)
pos.add_validator("Charlie", 700.0)

# 查看選中機率
for v in pos.validators:
    prob = pos.get_validator_probability(v.address)
    print(f"{v.address}: 機率={prob:.2%}")

# 選擇驗證者
selected = pos.select_validator()
print(f"選中的驗證者: {selected.address}")
```

## 參考資料

- [Peercoin Whitepaper](https://peercoin.net/whitepaper)
- [Ethereum Proof of Stake](https://ethereum.org/en/developers/docs/consensus-mechanisms/pos/)
- [Proof of Stake - Wikipedia](https://en.wikipedia.org/wiki/Proof_of_stake)
