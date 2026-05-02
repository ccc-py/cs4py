# 簡化版 EVM（以太坊虛擬機）

## 歷史背景

以太坊虛擬機（EVM）由 Vitalik Buterin 等人於 2013-2014 年設計，是以太坊區塊鏈的核心執行環境。EVM 是一個堆疊式虛擬機，負責執行智能合約的字節碼。本實作為教學用簡化版本，展示核心概念。

## 核心原理

### 堆疊式架構
EVM 使用後進先出（LIFO）堆疊來儲存操作數：
- **PUSH**: 將數值推入堆疊
- **POP**: 從堆疊彈出數值
- 算術運算從堆疊取操作數，結果壓回堆疊

### 燃料機制（Gas）
每個指令執行消耗燃料，防止無限循環攻擊，並為計算資源付費。

### 指令集
- **算術**: ADD, MUL, SUB, DIV
- **邏輯**: AND, OR, XOR, NOT
- **控制流**: JUMP, JUMPI（條件跳轉）
- **合約交互**: CALL, DELEGATECALL

## 使用範例

```python
from evm_simple import EVM

# 建立 EVM
evm = EVM()

# 編寫合約：(5 + 3) * 2
code = [
    {"op": "PUSH", "value": 5},
    {"op": "PUSH", "value": 3},
    {"op": "ADD"},
    {"op": "PUSH", "value": 2},
    {"op": "MUL"},
    {"op": "STOP"}
]

evm.load_code(code)
evm.run()

result = evm.stack.pop()
print(f"結果: {result}")  # 輸出 16
```

## 參考資料

- [Ethereum Yellow Paper](https://ethereum.github.io/yellowpaper/paper.pdf)
- [EVM Opcode Reference](https://www.evm.codes/)
- [Ethereum Virtual Machine](https://ethereum.org/en/developers/docs/evm/)
