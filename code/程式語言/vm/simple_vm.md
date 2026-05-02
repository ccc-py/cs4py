# 簡單堆疊式虛擬機器 (Simple Stack-based Virtual Machine)

## 歷史背景

虛擬機器（Virtual Machine, VM）的概念可以追溯到 1960 年代。IBM 在 1960 年代開發的 CP-CMS 系統中首次實現了虛擬化的概念。而堆疊式虛擬機器的設計則深受 Forth 語言（1970 年代）和後來的 Java 虛擬機器（JVM, 1995）影響。

堆疊式架構的優點在於指令簡潔，不需要指定運算元，因為運算元隱含在堆疊中。這種設計被許多解譯器和虛擬機器採用，包括：

- **Java Virtual Machine (JVM)**：使用堆疊式架構，指令集豐富
- **Python 虛擬機器**：CPython 使用基於堆疊的評估模型
- **Forth**：一種串接式語言，核心就是一個堆疊機
- **PostScript**：頁面描述語言，也是堆疊式設計

## 核心概念與原理

### 堆疊式虛擬機器架構

一個基本的堆疊式虛擬機器包含以下元件：

1. **運算堆疊（Stack）**：用於儲存中間運算結果
2. **指令指標（Instruction Pointer, IP）**：指向下一條要執行的指令
3. **位元組碼（Bytecode）**：編碼後的指令序列
4. **變數記憶體（Variables）**：儲存變數值
5. **呼叫堆疊（Call Stack）**：用於函式呼叫與返回

### 指令集設計

本實作的指令集包含：

| 指令 | 操作碼 | 說明 |
|------|--------|------|
| PUSH val | 0x01 | 將數值壓入堆疊 |
| POP | 0x02 | 彈出堆疊頂端 |
| ADD | 0x03 | 彈出兩個值相加，結果壓棧 |
| SUB | 0x04 | 彈出兩個值相減，結果壓棧 |
| MUL | 0x05 | 彈出兩個值相乘，結果壓棧 |
| DIV | 0x06 | 彈出兩個值相除，結果壓棧 |
| JMP addr | 0x07 | 無條件跳轉到指定位址 |
| JZ addr | 0x08 | 堆疊頂端為 0 時跳轉 |
| JNZ addr | 0x09 | 堆疊頂端不為 0 時跳轉 |
| CALL addr | 0x0A | 呼叫函式，儲存返回位址 |
| RET | 0x0B | 從函式返回 |
| PRINT | 0x0C | 印出堆疊頂端值 |
| HALT | 0x0D | 停止虛擬機器 |
| LOAD var | 0x0E | 載入變數值到堆疊 |
| STORE var | 0x0F | 將堆疊頂端儲存到變數 |

### 組譯器（Assembler）

組譯器負責將人類可讀的文字指令轉換為虛擬機器可執行的位元組碼。包含兩個階段：

1. **第一遍掃描**：收集標籤（label）並建立標籤到位址的對應表
2. **第二遍掃描**：將指令轉換為位元組碼，解析標籤參考

## 使用範例

### 計算階乘

```python
from simple_vm import VM, factorial_program

vm = VM()
bytecode = factorial_program()  # 計算 5!
vm.load_bytecode(bytecode)
vm.run()  # 輸出: 120
```

### 計算費波那契數列

```python
from simple_vm import VM, fibonacci_program

vm = VM()
bytecode = fibonacci_program()  # 計算第 10 項
vm.load_bytecode(bytecode)
vm.run()  # 輸出: 55
```

### 手動建立位元組碼

```python
from simple_vm import VM, OpCode

vm = VM()
bytecode = [
    (OpCode.PUSH, 10),
    (OpCode.PUSH, 20),
    (OpCode.ADD),
    (OpCode.PRINT),
    (OpCode.HALT),
]
vm.load_bytecode(bytecode)
vm.run()  # 輸出: 30
```

## 參考資料

1. **Java Virtual Machine Specification** - https://docs.oracle.com/javase/specs/jvms/se17/html/
2. **Stack-based Virtual Machines** - https://en.wikipedia.org/wiki/Stack_machine
3. **Forth Programming Language** - https://en.wikipedia.org/wiki/Forth_(programming_language)
4. **Python Virtual Machine** - https://realpython.com/python-virtual-machine/
5. **A Brief History of Virtualization** - https://www.ibm.com/history/virtualization
