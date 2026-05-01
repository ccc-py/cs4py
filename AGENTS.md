# AGENTS.md - cs4py 開發規劃

## 專案概述

本專案使用 Python 實作資訊科學的各種經典方法與程式，從歷史角度選取具有代表性的演算法與系統。

## 目錄結構

```
cs4py/
├── AGENTS.md
├── _doc/                  # 計畫文件
├── code/                  # 程式碼
│   ├── 人工智慧/
│   │   ├── search/       # 搜尋演算法（A*, Simulated Annealing）
│   │   ├── game/         # 遊戲 AI（Minimax, MCTS）
│   │   ├── ml/           # 機器學習（Perceptron, K-Means, Decision Tree, KNN）
│   │   └── evolution/    # 演化計算（Genetic Algorithm）
│   ├── 演算法/
│   │   ├── graph/        # 圖論（BFS/DFS/Dijkstra）
│   │   └── sort/         # 排序（Merge Sort/Heap Sort）
│   ├── 計算理論/
│   │   ├── automata/     # 自動機理論
│   │   ├── regex/        # 正規語言
│   │   ├── lambda_calculus/ # Lambda 演算
│   │   ├── cellular/     # 細胞自動機
│   │   ├── computability/ # 可計算性理論
│   │   ├── grammar/      # 形式語言
│   │   └── complexity/   # 計算複雜度
│   └── 程式語言/
│       ├── lisp/         # Lisp 解譯器
│       ├── forth/        # FORTH 解譯器
│       └── calc/         # 計算機語言
└── wiki/                  # Wiki 文章
    ├── 人工智慧/
    ├── 演算法/
    ├── 程式語言/
    └── 計算理論/
```

## 實作原則

1. **歷史價值**：優先選取對資訊科學發展有重要影響的演算法與系統
2. **可讀性**：程式碼清晰易懂，包含適當註釋
3. **教學性**：適合作為學習教材，展現核心概念
4. **純 Python**：盡量使用純 Python 實作，減少外部依賴
5. **測試**：每個實作都包含測試程式或範例使用方式
6. **文件搭配**：每個 .py 檔案都要搭配一個 .md 說明文件

## 檔案規範

### .py 檔案
- 實作真正的演算法，不是文章或概念講解
- 包含 docstring 說明
- 包含測試範例 (`if __name__ == "__main__":`)

### code/ 下的 .md 檔案
- 說明該程式的歷史背景
- 解釋核心概念與原理
- 提供使用範例
- 附上參考資料連結

### wiki/ 下的文章
- 無程式的文章式內容
- 放在 `wiki/<領域名稱>/` 目錄下
    - 領域名稱： 人工智慧 / 計算理論 / 演算法 / 程式語言
- 由 LLM 維護更新

## 實作進度追蹤

### 計算理論 - 程式碼 (code/計算理論/)

#### automata/ (已完成)
- [x] dfa.py + dfa.md
- [x] nfa.py + nfa.md
- [x] nfa_to_dfa.py + nfa_to_dfa.md
- [x] pda.py + pda.md
- [x] turing.py + turing.md

#### regex/ (已完成)
- [x] engine.py + engine.md
- [x] nfa_builder.py + nfa_builder.md

#### lambda_calculus/ (已完成)
- [x] parser.py + parser.md
- [x] reducer.py + reducer.md
- [x] encoder.py + encoder.md

#### cellular/ (已完成)
- [x] game_of_life.py + game_of_life.md
- [x] rule30.py + rule30.md

#### computability/ (已完成)
- [x] halting.py + halting.md
- [x] busy_beaver.py + busy_beaver.md
- [x] godel_number.py + godel_number.md

#### grammar/ (已完成)
- [x] cfg.py + cfg.md
- [x] cyk.py + cyk.md

#### complexity/ (已完成)
- [x] sat.py + sat.md
- [x] tsp.py + tsp.md
- [x] knapsack_nphard.py + knapsack_nphard.md
- [x] clique.py + clique.md
- [x] vertex_cover.py + vertex_cover.md
- [x] p_vs_np.py + p_vs_np.md
- [x] np_complete.py + np_complete.md
- [x] reduction.py + reduction.md

### 演算法 - 程式碼 (code/演算法/)

#### graph/ (部分完成)
- [x] bfs_dfs.py + bfs_dfs.md
- [x] dijkstra.py + dijkstra.md
- [ ] shortest_path (Bellman-Ford, Floyd-Warshall)
- [ ] mst (Prim, Kruskal)

#### sort/ (部分完成)
- [x] merge_sort.py + merge_sort.md
- [x] heap_sort.py + heap_sort.md
- [ ] quick_sort
- [ ] radix_sort

#### dp/ (待實作)
- [ ] knapsack
- [ ] lcs
- [ ] fibonacci
- [ ] matrix_chain

#### method/ (待實作)
- [ ] greedy
- [ ] divide_conquer
- [ ] backtracking
- [ ] branch_and_bound

#### string/ (待實作)
- [ ] kmp
- [ ] trie
- [ ] rabin_karp

#### math/ (待實作)
- [ ] gcd_lcm
- [ ] prime_sieve
- [ ] fft

### 人工智慧 - 程式碼 (code/人工智慧/)

#### search/ (部分完成)
- [x] a_star.py + a_star.md
- [ ] bfs_dfs_ai
- [x] simulated_annealing.py + simulated_annealing.md
- [ ] genetic_search

#### game/ (部分完成)
- [x] minimax.py + minimax.md
- [x] monte_carlo_tree_search.py + monte_carlo_tree_search.md
- [ ] expectimax

#### ml/ (部分完成)
- [x] perceptron.py + perceptron.md
- [x] kmeans.py + kmeans.md
- [x] decision_tree.py + decision_tree.md
- [x] knn.py + knn.md

#### nn/ (待實作)
- [ ] mlp
- [ ] cnn
- [ ] rnn

#### evolution/ (部分完成)
- [x] genetic_algorithm.py + genetic_algorithm.md
- [ ] particle_swarm

#### agent/ (待實作)
- [ ] reactive_agent
- [ ] bdi_agent

### 計算理論 - Wiki 文章 (wiki/計算理論/)

- [x] 哥德爾不完備定理.md
- [x] 歸約.md
- [x] np完全.md
- [x] p與np.md

## 開發順序

### 第一階段：計算理論 (已完成)
1. automata/ - 自動機理論 ✓
2. regex/ - 正規語言 ✓
3. lambda_calculus/ - Lambda 演算 ✓
4. cellular/ - 細胞自動機 ✓
5. computability/ - 可計算性理論 ✓
6. grammar/ - 形式語言 ✓
7. complexity/ - 計算複雜度 ✓

### 第二階段：演算法 (進行中)
- graph/ - 圖論演算法（部分完成）
- sort/ - 排序演算法（部分完成）
- dp/ - 動態規劃
- method/ - 演算法設計方法論
- string/ - 字串演算法
- math/ - 數論演算法

### 第三階段：人工智慧 (進行中)
- search/ - 搜尋演算法（A*, Simulated Annealing 已完成）
- game/ - 遊戲 AI（Minimax, MCTS 已完成）
- ml/ - 機器學習（Perceptron, K-Means, Decision Tree, KNN 已完成）
- nn/ - 深度學習 / 神經網路
- evolution/ - 演化計算（Genetic Algorithm 已完成）
- agent/ - AI Agent

### 第四階段：程式語言（進行中）

#### lisp/ (已完成)
- [x] interpreter.py + interpreter.md

#### forth/ (已完成)
- [x] interpreter.py + interpreter.md

#### calc/ (已完成)
- [x] calculator.py + calculator.md

#### vm/ (待實作)
- [ ] simple_vm

## 開發指引

### 新增演算法時
1. 確認所屬領域目錄已存在，若無則建立
2. 每個 .py 搭配同名的 .md 說明文件
3. .py 必須包含：docstring、type hints、`if __name__ == "__main__":` 測試區塊
4. .md 必須包含：歷史背景、核心原理、使用範例、參考資料
5. 更新此檔案的實作進度

### 程式碼風格
- 使用中文註解和 docstring
- 函數/變數命名使用 snake_case 英文
- 盡量使用純 Python，避免外部依賴
- 強調教學性和可讀性
