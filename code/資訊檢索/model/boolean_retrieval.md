# 布林檢索模型 (Boolean Retrieval Model)

## 歷史背景

布林檢索模型是最早的資訊檢索模型之一，基於布林邏輯（Boolean Logic）。1950-1960 年代，隨著電子計算機的發展，圖書館開始使用機電設備進行檔案檢索，布林檢索成為標準方法。

雖然現代搜尋引擎主要使用排名模型（如向量空間、BM25），布林檢索仍然在以下場景中使用：
- 專業資料庫檢索（PubMed、IEEE Xplore）
- 法律文件搜尋
- 精確匹配的應用場景

## 核心原理

### 布林運算

將查詢表示為布林運算式：
- **AND**：兩個詞彙都出現
- **OR**：任一詞彙出現
- **NOT**：不包含該詞彙

### 查詢解析

將中序表示法（Infix）轉換為後序表示法（Postfix），使用 Shunting-yard 演算法：
```
中序: A AND B OR C
後序: A B AND C OR
```

### 評估過程

使用堆疊評估後序運算式：
1. 遇到詞彙：查詢索引，將文件集合推入堆疊
2. 遇到運算子：從堆疊彈出操作數，執行集合運算，結果推回堆疊

### 範式轉換

- **合取範式（CNF）**：多個 AND 子句的 OR 組合
- **析取範式（DNF）**：多個 OR 子句的 AND 組合

## 使用範例

```python
from model.boolean_retrieval import BooleanRetrievalModel

model = BooleanRetrievalModel()
model.add_document("the cat sat")
model.add_document("the dog ran")

results = model.search("cat OR dog")
print(results)  # {0, 1}

results = model.search("cat AND NOT dog")
print(results)  # {0}
```

## 參考資料

- Van Rijsbergen, C. J. (1979). *Information Retrieval*. Butterworths.
- Manning, C. D., Raghavan, P., & Schütze, H. (2008). *Introduction to Information Retrieval*. Cambridge University Press.
- Witten, I. H., Moffat, A., & Bell, T. C. (1999). *Managing Gigabytes: Compressing and Indexing Documents and Images*. Morgan Kaufmann.
