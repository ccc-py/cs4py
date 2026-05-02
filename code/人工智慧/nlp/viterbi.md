# Viterbi 演算法

## 歷史背景

Viterbi 演算法由 Andrew Viterbi 於 1967 年提出，最初用於解碼卷積碼（convolutional codes）等通訊領域的錯誤更正。隨後發現其可應用於隱藏式馬可夫模型（Hidden Markov Model, HMM）的解碼問題，成為自然語言處理中詞性標註（POS tagging）、命名實體識別等任務的核心演算法。

## 核心原理

Viterbi 演算法是一種動態規劃演算法，用於在給定觀測序列的情況下，尋找 HMM 中最可能的隱藏狀態序列（即 Viterbi 路徑）。

### HMM 的三大要素

1. **狀態集合**：系統可能的隱藏狀態（如詞性：名詞、動詞、形容詞）
2. **觀測集合**：可觀測到的符號（如單詞）
3. **模型參數**：
   - 初始狀態機率 π
   - 狀態轉移機率 A
   - 發射機率 B

### 演算法步驟

1. **初始化**：計算第一步各狀態的機率
2. **遞推**：對每個時間步，計算到達各狀態的最大機率，並記錄路徑
3. **終止**：找到最後時間步機率最大的狀態
4. **回溯**：根據 backpointer 重建完整路徑

時間複雜度：O(T × N²)，其中 T 為序列長度，N 為狀態數。

## 使用範例

```python
from viterbi import viterbi

# 定義 HMM 參數
states = ["NOUN", "VERB", "ADJ"]
observations = ["I", "love", "Python", "programming"]

start_prob = {"NOUN": 0.3, "VERB": 0.5, "ADJ": 0.2}

trans_prob = {
    ("NOUN", "VERB"): 0.4, ("NOUN", "NOUN"): 0.3, ("NOUN", "ADJ"): 0.3,
    ("VERB", "NOUN"): 0.6, ("VERB", "VERB"): 0.2, ("VERB", "ADJ"): 0.2,
    ("ADJ", "NOUN"): 0.7, ("ADJ", "VERB"): 0.2, ("ADJ", "ADJ"): 0.1,
}

emit_prob = {
    ("NOUN", "I"): 0.1, ("NOUN", "love"): 0.1, ("NOUN", "Python"): 0.6, ("NOUN", "programming"): 0.2,
    ("VERB", "I"): 0.1, ("VERB", "love"): 0.7, ("VERB", "Python"): 0.1, ("VERB", "programming"): 0.1,
    ("ADJ", "I"): 0.1, ("ADJ", "love"): 0.2, ("ADJ", "Python"): 0.3, ("ADJ", "programming"): 0.4,
}

best_path = viterbi(observations, states, start_prob, trans_prob, emit_prob)
print("最可能的詞性序列:", best_path)
# 輸出: ['VERB', 'VERB', 'NOUN', 'NOUN'] 或類似結果
```

## 參考資料

- Viterbi, A. J. (1967). "Error bounds for convolutional codes and an asymptotically optimum decoding algorithm". IEEE Transactions on Information Theory.
- Rabiner, L. R. (1989). "A tutorial on hidden Markov models and selected applications in speech recognition". Proceedings of the IEEE.
- [Wikipedia: Viterbi algorithm](https://en.wikipedia.org/wiki/Viterbi_algorithm)
