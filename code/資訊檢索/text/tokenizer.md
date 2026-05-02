# 文字預處理與分詞器 (Text Preprocessing & Tokenizer)

## 歷史背景

文字預處理是資訊檢索和文字探勘的基礎步驟。1950-1960 年代的早期系統就開始使用停用詞列表（stop word list），而詞幹提取（stemming）則由 Julie Beth Lovins 在 1968 年首次提出系統化方法。

Martin Porter 在 1980 年提出的 Porter Stemmer 成為英文詞幹提取的標準演算法，至今仍被廣泛使用。現代自然語言處理（NLP）使用更複雜的方法（如 lemmatization），但詞幹提取因其簡單高效仍佔有一席之地。

## 核心原理

### 文字預處理步驟

1. **斷詞（Tokenization）**：將文字分割為詞彙單位
2. **小寫化（Lowercasing）**：統一詞彙大小寫
3. **停用詞移除（Stop Word Removal）**：移除高頻無意義詞（the, a, is）
4. **詞幹提取（Stemming）**：將詞彙還原為詞幹（running -> run）

### Porter Stemmer 核心規則

- **步驟 1a**: sses -> ss, ies -> i, ss -> ss, s -> 
- **步驟 1b**: ed, ing 結尾處理
- **步驟 1c**: y -> i（當前面是輔音）
- **步驟 2-5**: 更複雜的後綴替換（如 ization -> ize）

### 停用詞

停用詞是那些在文件中出現極頻繁但無特定意義的詞彙，移除它們可以：
- 減少索引大小
- 提升檢索效率
- 降低雜訊

## 使用範例

```python
from text.tokenizer import SimpleTokenizer

tokenizer = SimpleTokenizer(
    lowercase=True, 
    remove_stopwords=True, 
    stemming=True
)

text = "The running foxes are jumping quickly"
tokens = tokenizer.tokenize(text)
print(tokens)  # ['run', 'fox', 'jump', 'quickli']
```

## 參考資料

- Lovins, J. B. (1968). Development of a stemming algorithm. *Mechanical Translation and Computational Linguistics*, 11(1-2), 22-31.
- Porter, M. F. (1980). An algorithm for suffix stripping. *Program*, 14(3), 130-137.
- Manning, C. D., Raghavan, P., & Schütze, H. (2008). *Introduction to Information Retrieval*. Cambridge University Press.
- Salton, G., & McGill, M. J. (1983). *Introduction to Modern Information Retrieval*. McGraw-Hill.
