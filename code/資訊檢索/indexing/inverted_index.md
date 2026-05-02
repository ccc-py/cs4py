# 反向索引 (Inverted Index)

## 歷史背景

反向索引是資訊檢索系統中最核心的資料結構，起源於 1950 年代的早期檔案檢索系統。Gerard Salton 在 1960 年代發展的 SMART 系統中廣泛應用了此概念。與傳統的「文件→詞彙」正向索引相反，反向索引建立「詞彙→文件」的對應關係，使得搜尋引擎能夠在毫秒內找到包含特定詞彙的所有文件。

現代搜尋引擎（如 Google、Bing）都依賴高度優化的反向索引來支援數十億網頁的即時檢索。

## 核心原理

### 反向索引結構

反向索引由兩部分組成：
1. **詞彙表（Vocabulary）**：所有不重複詞彙的列表
2. **投寄列表（Posting List）**：每個詞彙對應的文件 ID 列表，通常包含：
   - 文件 ID
   - 詞彙在文件中的位置（position）
   - 詞彙頻率（term frequency）

### 建立過程

```
文件集合 → 分詞 → 建立詞彙到文件的映射 → 排序優化
```

### 布林查詢

使用集合運算實作布林邏輯：
- **AND**：交集運算，兩個詞彙都出現的文件
- **OR**：聯集運算，任一詞彙出現的文件
- **NOT**：差集運算，不包含該詞彙的文件

### 片語查詢

檢查多個詞彙是否在文件中連續出現，需要利用位置資訊。

## 使用範例

```python
from indexing.inverted_index import InvertedIndex

# 建立索引
idx = InvertedIndex()
idx.add_document(1, "The quick brown fox")
idx.add_document(2, "A quick dog")

# 查詢
print(idx.boolean_and('quick', 'fox'))  # {1}
print(idx.boolean_or('dog', 'fox'))    # {1, 2}
print(idx.phrase_query('quick brown')) # {1}
```

## 參考資料

- Manning, C. D., Raghavan, P., & Schütze, H. (2008). *Introduction to Information Retrieval*. Cambridge University Press.
- Salton, G. (1971). The SMART Retrieval System—Experiments in Automatic Document Processing. Prentice Hall.
- Zobel, J., & Moffat, A. (2006). Inverted files for text search engines. *ACM Computing Surveys*, 38(2), 6.
