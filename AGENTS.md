# AGENTS.md - cs4py 開發規劃

## 專案概述

本專案使用 Python 實作資訊科學的各種經典方法與程式，從歷史角度選取具有代表性的演算法與系統。

## 目錄結構

```
cs4py/
├── AGENTS.md
├── _doc/                  # 計畫文件（v1.0.md, v2.0.md）
├── code/                  # 程式碼
│   ├── 人工智慧/
│   │   ├── search/       # 搜尋演算法
│   │   ├── game/         # 遊戲 AI
│   │   ├── ml/           # 機器學習
│   │   ├── nn/           # 深度學習
│   │   ├── evolution/    # 演化計算
│   │   ├── agent/        # AI Agent
│   │   ├── recommendation/ # 推薦系統
│   │   └── nlp/          # 自然語言處理
│   ├── 演算法/
│   │   ├── graph/        # 圖論演算法
│   │   ├── sort/         # 排序演算法
│   │   ├── dp/           # 動態規劃
│   │   ├── method/       # 演算法設計方法論
│   │   ├── string/       # 字串演算法
│   │   └── math/         # 數論演算法
│   ├── 計算理論/
│   │   ├── automata/     # 自動機理論
│   │   ├── regex/        # 正規語言
│   │   ├── lambda_calculus/ # Lambda 演算
│   │   ├── cellular/     # 細胞自動機
│   │   ├── computability/ # 可計算性理論
│   │   ├── grammar/      # 形式語言
│   │   └── complexity/   # 計算複雜度
│   ├── 密碼學/
│   │   ├── classical/    # 古典密碼
│   │   ├── modern/       # 現代密碼
│   │   ├── hash/         # 雜湊函數
│   │   └── signature/    # 數位簽章
│   ├── 資料結構/
│   │   ├── linked_list/  # 鏈結串列
│   │   ├── tree/         # 樹結構
│   │   ├── hash_table/   # 雜湊表
│   │   ├── heap/         # 堆積
│   │   └── union_find/   # 並查集
│   └── 程式語言/
│       ├── lisp/         # Lisp 解譯器
│       ├── forth/        # FORTH 解譯器
│       ├── calc/         # 計算機語言
│       └── vm/           # 簡單虛擬機器
├── 資料壓縮/
│   ├── entropy/      # 熵編碼
│   ├── dictionary/   # 字典式壓縮
│   ├── transform/    # 轉換編碼
│   └── image/        # 圖片壓縮
├── 數值方法/
│   ├── root_finding/    # 求根方法
│   ├── linear/         # 線性代數方法
│   ├── integration/    # 數值積分
│   ├── interpolation/  # 插值方法
│   └── ode/           # 常微分方程
├── 計算幾何/
│   ├── basic/         # 基礎點線運算
│   ├── convex_hull/   # 凸包算法
│   ├── closest_pair/  # 最近點對
│   ├── polygon/       # 多邊形操作
│   ├── sweep_line/    # 掃描線算法
│   └── triangulation/ # 三角化
└── wiki/                  # Wiki 文章
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

### 計算理論 - 程式碼 (code/計算理論/) — 已完成

#### automata/
- [x] dfa.py + dfa.md
- [x] nfa.py + nfa.md
- [x] nfa_to_dfa.py + nfa_to_dfa.md
- [x] pda.py + pda.md
- [x] turing.py + turing.md

#### regex/
- [x] engine.py + engine.md
- [x] nfa_builder.py + nfa_builder.md

#### lambda_calculus/
- [x] parser.py + parser.md
- [x] reducer.py + reducer.md
- [x] encoder.py + encoder.md

#### cellular/
- [x] game_of_life.py + game_of_life.md
- [x] rule30.py + rule30.md

#### computability/
- [x] halting.py + halting.md
- [x] busy_beaver.py + busy_beaver.md
- [x] godel_number.py + godel_number.md

#### grammar/
- [x] cfg.py + cfg.md
- [x] cyk.py + cyk.md

#### complexity/
- [x] sat.py + sat.md
- [x] tsp.py + tsp.md
- [x] knapsack_nphard.py + knapsack_nphard.md
- [x] clique.py + clique.md
- [x] vertex_cover.py + vertex_cover.md
- [x] p_vs_np.py + p_vs_np.md
- [x] np_complete.py + np_complete.md
- [x] reduction.py + reduction.md

### 演算法 - 程式碼 (code/演算法/) — 已完成

#### graph/
- [x] bfs_dfs.py + bfs_dfs.md
- [x] dijkstra.py + dijkstra.md
- [x] shortest_path.py + shortest_path.md
- [x] mst.py + mst.md
- [x] articulation.py + articulation.md
- [x] bipartite_matching.py + bipartite_matching.md
- [x] topological_sort.py + topological_sort.md
- [x] strongly_connected.py + strongly_connected.md
- [x] max_flow.py + max_flow.md
- [x] eulerian.py + eulerian.md
- [x] min_cost_flow.py + min_cost_flow.md
- [x] matching.py + matching.md
- [x] planar.py + planar.md
- [x] graph_coloring.py + graph_coloring.md

#### sort/
- [x] merge_sort.py + merge_sort.md
- [x] heap_sort.py + heap_sort.md
- [x] quick_sort.py + quick_sort.md
- [x] radix_sort.py + radix_sort.md
- [x] selection_sort.py + selection_sort.md
- [x] bucket_sort.py + bucket_sort.md
- [x] shell_sort.py + shell_sort.md
- [x] insertion_sort.py + insertion_sort.md
- [x] counting_sort.py + counting_sort.md

#### dp/
- [x] knapsack
- [x] lcs
- [x] fibonacci
- [x] matrix_chain
- [x] subset_sum
- [x] optimal_bst
- [x] edit_distance
- [x] lis
- [x] coin_change

#### method/
- [x] greedy
- [x] divide_conquer
- [x] backtracking
- [x] branch_and_bound

#### string/
- [x] kmp
- [x] trie
- [x] rabin_karp

#### math/
- [x] gcd_lcm
- [x] prime_sieve
- [x] fft
- [x] discrete_log
- [x] modular_exponentiation
- [x] miller_rabin
- [x] chinese_remainder

#### approximation/
- [x] vertex_cover.py + vertex_cover.md
- [x] tsp.py + tsp.md
- [x] set_cover.py + set_cover.md
- [x] knapsack.py + knapsack.md
- [x] max_cut.py + max_cut.md

#### advanced/
- [x] treap.py + treap.md
- [x] splay_tree.py + splay_tree.md
- [x] suffix_tree.py + suffix_tree.md

### 人工智慧 - 程式碼 (code/人工智慧/) — 已完成

#### search/
- [x] a_star.py + a_star.md
- [x] bfs_dfs_ai.py + bfs_dfs_ai.md
- [x] simulated_annealing.py + simulated_annealing.md
- [x] genetic_search.py + genetic_search.md

#### game/
- [x] minimax.py + minimax.md
- [x] monte_carlo_tree_search.py + monte_carlo_tree_search.md
- [x] expectimax.py + expectimax.md

#### ml/
- [x] perceptron.py + perceptron.md
- [x] kmeans.py + kmeans.md
- [x] decision_tree.py + decision_tree.md
- [x] knn.py + knn.md
- [x] mlp.py + mlp.md
- [x] naive_bayes.py + naive_bayes.md
- [x] linear_regression.py + linear_regression.md
- [x] pca.py + pca.md

#### nn/
- [x] cnn.py + cnn.md
- [x] rnn.py + rnn.md

#### evolution/
- [x] genetic_algorithm.py + genetic_algorithm.md
- [x] particle_swarm.py + particle_swarm.md

#### agent/
- [x] reactive_agent.py + reactive_agent.md
- [x] q_learning.py + q_learning.md
- [x] sarsa.py + sarsa.md
- [x] bdi_agent.py + bdi_agent.md

#### recommendation/
- [x] collaborative_filtering.py + collaborative_filtering.md
- [x] matrix_factorization.py + matrix_factorization.md
- [x] content_based.py + content_based.md
- [x] association_rules.py + association_rules.md
- [x] evaluation.py + evaluation.md

#### nlp/
- [x] attention.py + attention.md
- [x] bleu.py + bleu.md
- [x] rnn_nlp.py + rnn_nlp.md
- [x] word2vec.py + word2vec.md
- [x] naive_bayes_text.py + naive_bayes_text.md
- [x] ngram.py + ngram.md
- [x] viterbi.py + viterbi.md

### 密碼學 - 程式碼 (code/密碼學/) — 已完成

#### classical/
- [x] caesar.py + caesar.md
- [x] vigenere.py + vigenere.md
- [x] frequency.py + frequency.md
- [x] enigma.py + enigma.md

#### modern/
- [x] rsa.py + rsa.md
- [x] diffie_hellman.py + diffie_hellman.md
- [x] elgamal.py + elgamal.md

#### hash/
- [x] sha256.py + sha256.md
- [x] md5.py + md5.md

#### signature/
- [x] digital_signature.py + digital_signature.md

### 資料結構 - 程式碼 (code/資料結構/) — 已完成

#### linked_list/
- [x] singly.py + singly.md
- [x] doubly.py + doubly.md

#### tree/
- [x] binary_tree.py + binary_tree.md
- [x] bst.py + binary_search_tree.md
- [x] avl.py + avl.md
- [x] red_black.py + red_black.md

#### hash_table/
- [x] chaining.py + chaining.md
- [x] open_addressing.py + open_addressing.md

#### heap/
- [x] binary_heap.py + binary_heap.md

#### union_find/
- [x] uf.py + uf.md

### 程式語言 - 程式碼 (code/程式語言/) — 已完成

#### lisp/
- [x] interpreter.py + interpreter.md

#### forth/
- [x] interpreter.py + interpreter.md

#### calc/
- [x] calculator.py + calculator.md

#### vm/
- [x] simple_vm.py + simple_vm.md

### 數值方法 - 程式碼 (code/數值方法/) — 已完成 (v3.0)

#### root_finding/
- [x] bisection.py + bisection.md
- [x] newton.py + newton.md
- [x] secant.py + secant.md

#### linear/
- [x] gaussian_elimination.py + gaussian_elimination.md
- [x] lu_decomposition.py + lu_decomposition.md
- [x] jacobi_iteration.py + jacobi_iteration.md

#### integration/
- [x] trapezoidal.py + trapezoidal.md
- [x] simpson.py + simpson.md
- [x] monte_carlo.py + monte_carlo.md

#### interpolation/
- [x] lagrange.py + lagrange.md
- [x] spline.py + spline.md

#### ode/
- [x] euler.py + euler.md
- [x] runge_kutta.py + runge_kutta.md

### 計算幾何 - 程式碼 (code/計算幾何/) — 已完成 (v3.0)

#### basic/
- [x] point.py + point.md
- [x] line.py + line.md

#### convex_hull/
- [x] graham_scan.py + graham_scan.md
- [x] jarvis_march.py + jarvis_march.md
- [x] quickhull.py + quickhull.md

#### closest_pair/
- [x] closest_pair.py + closest_pair.md

#### polygon/
- [x] point_in_polygon.py + point_in_polygon.md
- [x] polygon_area.py + polygon_area.md
- [x] triangulation.py + triangulation.md

#### sweep_line/
- [x] line_sweep.py + line_sweep.md

#### triangulation/
- [x] delaunay.py + delaunay.md

### 資訊檢索 - 程式碼 (code/資訊檢索/) — 已完成 (v3.0)

#### indexing/
- [x] inverted_index.py + inverted_index.md
- [x] suffix_array.py + suffix_array.md

#### ranking/
- [x] tfidf.py + tfidf.md
- [x] pagerank.py + pagerank.md
- [x] bm25.py + bm25.md

#### model/
- [x] vector_space.py + vector_space.md
- [x] boolean_retrieval.py + boolean_retrieval.md
- [x] lsi.py + lsi.md

#### evaluation/
- [x] metrics.py + metrics.md

#### text/
- [x] tokenizer.py + tokenizer.md

### 計算理論 - Wiki 文章 (wiki/計算理論/)

- [x] 哥德爾不完備定理.md
- [x] 歸約.md
- [x] np完全.md
- [x] p與np.md

## 開發順序

### 第一階段：計算理論 (已完成) ✓

### 第二階段：演算法 (已完成) ✓
- graph/、sort/、dp/、method/、string/、math/
- 擴充：graph/ (min_cost_flow, matching, planar, graph_coloring)、approximation/、advanced/

### 第三階段：人工智慧 (已完成) ✓
- search/、game/、ml/、nn/、evolution/、agent/
- 擴充：recommendation/、nlp/

### 第四階段：程式語言 (已完成) ✓

### 第五階段：密碼學 (v2.0) (已完成) ✓
- classical/ → modern/ → hash/ → signature/

### 第六階段：資料結構 (v2.0) (已完成) ✓
- linked_list/ → tree/ → hash_table/ → heap/ → union_find/

### 第七階段：資料壓縮 (v3.0) (已完成) ✓
- entropy/ → dictionary/ → transform/ → image/

### 第八階段：數值方法 (v3.0) (已完成) ✓
- root_finding/ → linear/ → integration/ → interpolation/ → ode/

### 第九階段：計算幾何 (v3.0) (已完成) ✓
- basic/ → convex_hull/ → closest_pair/ → polygon/ → sweep_line/ → triangulation/

### 第十階段：資訊檢索 (v3.0) (已完成) ✓
- indexing/ → ranking/ → model/ → evaluation/ → text/

### 第十一階段：機率演算法 (v3.0) (已完成) ✓
- monte_carlo/ → randomized/ → probabilistic_ds/ → markov/

## 資料壓縮 - 程式碼 (code/資料壓縮/) — 已完成 (v3.0)

### entropy/
- [x] huffman.py + huffman.md
- [x] shannon_fano.py + shannon_fano.md
- [x] arithmetic_coding.py + arithmetic_coding.md

### dictionary/
- [x] lz77.py + lz77.md
- [x] lzw.py + lzw.md
- [x] lz78.py + lz78.md

### transform/
- [x] run_length.py + run_length.md
- [x] burrows_wheeler.py + burrows_wheeler.md
- [x] move_to_front.py + move_to_front.md

### image/
- [x] dct.py + dct.md

### 機率演算法 - 程式碼 (code/機率演算法/) — 已完成 (v3.0)

#### monte_carlo/
- [x] integration.py + integration.md
- [x] pi_estimation.py + pi_estimation.md
- [x] sampling.py + sampling.md

#### randomized/
- [x] quickselect.py + quickselect.md
- [x] skip_list.py + skip_list.md

#### probabilistic_ds/
- [x] bloom_filter.py + bloom_filter.md
- [x] hyperloglog.py + hyperloglog.md
- [x] count_min_sketch.py + count_min_sketch.md
- [x] min_hash.py + min_hash.md

#### markov/
- [x] markov_chain.py + markov_chain.md
- [x] mcmc.py + mcmc.md

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

## v3.0 完成總結

### 新增領域（5 個）
| 領域 | 子目錄數 | .py/.md 對數 |
|---|---|---|
| 數值方法 | 5 | 13 |
| 資料壓縮 | 4 | 10 |
| 計算幾何 | 6 | 11 |
| 資訊檢索 | 5 | 10 |
| 機率演算法 | 4 | 11 |

### 擴充項目
| 領域 | 項目 |
|---|---|
| 演算法/graph/ | min_cost_flow, matching, planar, graph_coloring |
| 演算法/ | approximation/ (5), advanced/ (3) |
| 人工智慧/ | recommendation/ (5), nlp/ (7) |

### 總計
- v3.0 新增 .py 檔案：79 個
- v3.0 新增 .md 檔案：79 個
- 所有 .py 與 .md 均一一對應，無遺漏
