# 編輯距離 (Edit Distance / Levenshtein Distance)

## 歷史背景

編輯距離（Edit Distance），又稱 Levenshtein 距離，由俄羅斯數學家 Vladimir Levenshtein 於 1965 年提出。

### 應用領域

- **拼字檢查**：找出最可能的正確拼寫
- **DNA 序列比對**：測量基因序列的相似度
- **自然語言處理**：計算字串相似度
- **語音識別**：評估識別結果
- **資訊檢索**：模糊搜尋

## 演算法原理

### 定義

將字串 s1 轉換為 s2 所需的最少操作次數，允許的操作：
- **插入**（Insert）：在 s1 中插入一個字元
- **刪除**（Delete）：從 s1 中刪除一個字元
- **替換**（Substitute/Replace）：將 s1 中的一個字元替換為另一個

每個操作的成本為 1。

### 動態規劃

```
定義 dp[i][j] = s1[0:i] 轉換為 s2[0:j] 的最小操作次數

基底情況：
- dp[0][j] = j（插入 j 個字元）
- dp[i][0] = i（刪除 i 個字元）

遞推式：
若 s1[i-1] == s2[j-1]：
    dp[i][j] = dp[i-1][j-1]  // 字元相同，無需操作
否則：
    dp[i][j] = 1 + min(
        dp[i-1][j],    // 刪除 s1[i-1]
        dp[i][j-1],    // 插入 s2[j-1]
        dp[i-1][j-1]   // 替換 s1[i-1] 為 s2[j-1]
    )
```

**時間複雜度**：O(m * n)
**空間複雜度**：O(m * n)（可優化到 O(min(m, n))）

## DP 表示例

```
計算 "kitten" -> "sitting"：

    ""  s  i  t  t  i  n  g
""   0  1  2  3  4  5  6  7
k    1  1  2  3  4  5  6  7
i    2  2  1  2  3  4  5  6
t    3  3  2  1  2  3  4  5
t    4  4  3  2  1  2  3  4
e    5  5  4  3  2  2  3  4
n    6  6  5  4  3  3  2  3

結果：dp[6][7] = 3
操作：kitten -> sitten -> sittin -> sitting
```

## 空間優化

觀察 DP 表，計算 dp[i][j] 時只需要：
- 當前行：dp[i][*]
- 前一行：dp[i-1][*]

因此只需保留兩行，空間複雜度降到 O(n)。

## 編輯操作重建

通過回溯 DP 表，可以重建出具體的編輯操作序列：

```
從 dp[m][n] 開始，反向追蹤：
1. 如果 s1[i-1] == s2[j-1]，對齊，i--, j--
2. 否則，檢查三個方向：
   - 來自 dp[i-1][j]：刪除 s1[i-1]
   - 來自 dp[i][j-1]：插入 s2[j-1]
   - 來自 dp[i-1][j-1]：替換 s1[i-1] 為 s2[j-1]
```

## 程式碼說明

### 核心 DP

```python
def edit_distance(str1, str2):
    m, n = len(str1), len(str2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if str1[i-1] == str2[j-1]:
                dp[i][j] = dp[i-1][j-1]
            else:
                dp[i][j] = 1 + min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1])

    return dp[m][n]
```

## 應用場景

### 1. 拼字檢查器

```
輸入： "acress"
建議： "actress" (距離 1), "actresses" (距離 2)
```

### 2. DNA 序列比對

```
序列1： AGTACG
序列2： AGTCG
距離： 1（刪除 A）
```

### 3. 模糊搜尋

在搜尋引擎中，允許使用者輸入略有不同的關鍵字。

## 變體

| 變體 | 說明 |
|------|------|
| Damerau-Levenshtein | 增加相鄰交換操作 |
| Hamming Distance | 只允許替換，字串長度必須相同 |
| Jaro-Winkler | 適合短字串，考慮前綴 |

## 參考資料

- Levenshtein, V. I. (1966). *Binary codes capable of correcting deletions, insertions, and reversals*. Soviet Physics Doklady, 10(8), 707-710.
- Wagner, R. A., & Fischer, M. J. (1974). *The string-to-string correction problem*. Journal of the ACM, 21(1), 168-173.
- Cormen, T. H., et al. (2009). *Introduction to Algorithms* (3rd ed.). MIT Press. (Chapter 15.4)
