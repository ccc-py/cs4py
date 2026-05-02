# BLEU 分數

## 歷史背景

BLEU（Bilingual Evaluation Understudy）由 IBM 研究員 Kishore Papineni 等人於 2002 年提出，用於自動評估機器翻譯的品質。BLEU 是目前最廣泛使用的機器翻譯自動評估指標，其核心思想是：機器翻譯的候選譯文與多個參考譯文的 n-gram 重疊度越高，翻譯品質越好。

## 核心原理

### BLEU 公式

BLEU = BP × exp(Σ w_n × log p_n)

其中：
- **p_n**：n-gram 修正精確率（n=1 到 4）
- **w_n**：各 n-gram 的權重（通常均權）
- **BP**：簡潔度懲罰（Brevity Penalty）

### 修正精確率（Modified Precision）

不同於一般精確率，BLEU 使用「修正」計數：
- 候選譯文中某 n-gram 的計數，不超過所有參考譯文中該 n-gram 的最大出現次數
- 避免候選譯文重複高頻詞來作弊

### 簡潔度懲罰（Brevity Penalty）

當候選譯文比參考譯文短時給予懲罰：

BP = 1 (若候選長度 > 最佳參考長度)
BP = e^(1 - ref_len / cand_len) (否則)

這防止候選譯文過短而獲得高分。

## 使用範例

```python
from bleu import bleu_score, bleu_detail

candidate = "the cat is on the mat"
references = [
    "the cat is on the mat",
    "there is a cat on the mat",
]

score = bleu_score(candidate, references)
print(f"BLEU-4 分數: {score:.2f}")

# 詳細資訊
detail = bleu_detail(candidate, references)
print(f"1-gram 精確率: {detail['ngram_precisions']['1-gram']:.4f}")
print(f"簡潔度懲罰: {detail['brevity_penalty']:.4f}")
```

## 參考資料

- Papineni, K., et al. (2002). "BLEU: a Method for Automatic Evaluation of Machine Translation". ACL.
- [BLEU 介紹](https://en.wikipedia.org/wiki/BLEU)
- "Neural Machine Translation" - Stanford CS224n Lecture Notes
