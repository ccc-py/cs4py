# FORTH 解譯器 (FORTH Stack-Based Language Interpreter)

## 歷史背景

FORTH 由 Charles H. Moore 於 1970 年代初期發明，最初用於控制射電望遠鏡的儀器。Moore 在開車時想到這個設計，將其命名為「Fourth-generation language」，但由於當時的系統只支援 5 個字母的檔名，因此變成了「FORTH」。

FORTH 因其極小的體量（某些實作僅需幾 KB）和高效的執行速度，被廣泛應用於嵌入式系統、天文觀測、太空任務（如 NASA 的太空梭）等資源受限的環境。ISO 於 1994 年發布了 FORTH-94 標準。

## 核心原理

### 堆疊架構

FORTH 使用後進先出（LIFO）堆疊作為主要數據結構。所有操作都透過推入（push）和彈出（pop）完成：

```
3 4 + .     →  推入 3，推入 4，彈出兩個相加，推入結果，輸出
```

### 逆向波蘭表示法（RPN）

FORTH 使用後綴表示法，運算子在運算元之後：

| 中綴 | RPN |
|------|-----|
| 3 + 4 | 3 4 + |
| (3 + 4) × 2 | 3 4 + 2 × |
| 2³ | 2 3 ^ |

### 字典

所有詞彙（單詞/函數）儲存在字典中，分為：
- **內建詞**：由系統提供（如 +, -, *, /, dup, swap）
- **使用者定義詞**：用 `: name ... ;` 定義

### 控制結構

FORTH 的控制結構基於編譯時詞編碼：

```forth
\ 條件分支
5 3 > if 10 else 20 then .    → 輸出 10

\ 循環
0 5 0 do i + loop .           → 0+1+2+3+4 = 10
```

### 編譯與直譯

FORTH 是雙狀態語言：
- **直譯模式**：立即執行輸入的詞
- **編譯模式**：將詞編碼到字典中（`: name ... ;`）

## 堆疊操作詞

| 詞 | 效果 | 說明 |
|----|------|------|
| dup | ( a -- a a ) | 複製棧頂 |
| drop | ( a -- ) | 丟棄棧頂 |
| swap | ( a b -- b a ) | 交換棧頂兩個元素 |
| over | ( a b -- a b a ) | 複製第二個元素到棧頂 |
| rot | ( a b c -- b c a ) | 旋轉前三個元素 |

## 使用範例

```python
from forth.interpreter import ForthInterpreter

forth = ForthInterpreter()

# 基本運算
forth.run("3 4 + .")        # 輸出: 7
forth.run("10 2 - .")       # 輸出: 8

# 定義詞彙
forth.evaluate(": sq dup * ;")
forth.run("7 sq .")         # 輸出: 49

# 階乘
forth.evaluate(": fact 1 swap 1 + 1 do i * loop ;")
forth.run("5 fact .")       # 輸出: 120
```

## 參考資料

- Moore, C. H. (1970). FORTH: A New Way to Program a Minicomputer.
- ISO/IEC 15145:1997 - Information technology — Programming languages — Forth.
- Brodie, L. (1984). Starting FORTH.
