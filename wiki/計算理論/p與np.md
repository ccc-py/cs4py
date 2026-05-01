# P vs NP 問題

## 歷史背景

P vs NP 是理論計算機科學中最重要的未解問題之一。

### 重要里程碑

- **1971 年**：Stephen Cook 提出 P vs NP 問題
- **1972 年**：Richard Karp 證明了 21 個問題是 NP-完備的
- **至今未解**：目前大多數研究者相信 P ≠ NP

## 核心概念

### 定義

- **P**: 可以在多項式時間內「解決」的問題類別
- **NP**: 可以在多項式時間內「驗證解」的問題類別
- 顯然 P ⊆ NP
- **問題**：P = NP 還是 P ≠ NP？

### 類比

- **P**: 「我可以輕鬆解決這個問題」
- **NP**: 「我可以輕鬆檢查答案是否正確」

如果 P = NP：
- 「輕鬆檢查答案」→「輕鬆解決問題」
- 這會革命化計算機科學！
- 密碼學崩潰、優化問題易解、AI 飛躍...

如果 P ≠ NP（大多數人相信）：
- 「輕鬆檢查答案」≠「輕鬆解決問題」
- 許多問題本質上困難
- 密碼學基本安全

## 百萬美元難題

Clay Mathematics Institute 將 P vs NP 列為七大千禧年難題之一，解決者可獲得一百萬美元獎金。

## 複雜度類別階層

```
L ⊆ NL ⊆ P ⊆ NP ⊆ PSPACE ⊆ EXPTIME
```

- 已知嚴格包含關係：L ⊊ NL ⊊ PSPACE ⊊ EXPTIME
- 未解問題：P vs NP、NP vs PSPACE、P vs PSPACE

## 參考資料

- Cook, S. A. (1971). [The complexity of theorem proving procedures](https://doi.org/10.1145/800157.805047). *Proceedings of the 3rd Annual ACM Symposium on Theory of Computing*, 151-158.
- Fortnow, L. J. (2013). *The Golden Ticket: P, NP, and the Search for the Impossible*. Princeton University Press.
- Aaronson, S. (2017). P ?= NP. *Communications of the ACM*, 60(2), 50-59.
