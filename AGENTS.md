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
│   │   ├── nlp/          # 自然語言處理
│   │   ├── reinforcement/ # 強化學習
│   │   └── generative/   # 生成模型
│   ├── 演算法/
│   │   ├── graph/        # 圖論演算法
│   │   ├── sort/         # 排序演算法
│   │   ├── dp/           # 動態規劃
│   │   ├── method/       # 演算法設計方法論
│   │   ├── string/       # 字串演算法
│   │   ├── math/         # 數論演算法
│   │   ├── approximation/ # 近似演算法
│   │   ├── advanced/     # 進階資料結構
│   │   └── flow/         # 網路流演算法
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
│   ├── 程式語言/
│   │   ├── lisp/         # Lisp 解譯器
│   │   ├── forth/        # FORTH 解譯器
│   │   ├── calc/         # 計算機語言
│   │   └── vm/           # 簡單虛擬機器
│   ├── 資料壓縮/
│   │   ├── entropy/      # 熵編碼
│   │   ├── dictionary/   # 字典式壓縮
│   │   ├── transform/    # 轉換編碼
│   │   └── image/        # 圖片壓縮
│   ├── 數值方法/
│   │   ├── root_finding/    # 求根方法
│   │   ├── linear/         # 線性代數方法
│   │   ├── integration/    # 數值積分
│   │   ├── interpolation/  # 插值方法
│   │   ├── ode/           # 常微分方程
│   │   └── advanced/      # 進階數值方法
│   ├── 計算幾何/
│   │   ├── basic/         # 基礎點線運算
│   │   ├── convex_hull/   # 凸包算法
│   │   ├── closest_pair/  # 最近點對
│   │   ├── polygon/       # 多邊形操作
│   │   ├── sweep_line/    # 掃描線算法
│   │   └── triangulation/ # 三角化
│   ├── 資訊檢索/
│   │   ├── indexing/     # 索引結構
│   │   ├── ranking/      # 排序演算法
│   │   ├── model/        # 檢索模型
│   │   ├── evaluation/   # 評估指標
│   │   └── text/         # 文字處理
│   ├── 機率演算法/
│   │   ├── monte_carlo/   # 蒙特卡羅方法
│   │   ├── randomized/    # 隨機化演算法
│   │   ├── probabilistic_ds/ # 機率資料結構
│   │   └── markov/        # 馬可夫鏈
│   ├── 電腦圖學/
│   │   ├── raster/        # 光柵化演算法
│   │   ├── transform/    # 幾何變換
│   │   ├── render/        # 渲染演算法
│   │   ├── clip/          # 裁剪演算法
│   │   └── color/         # 色彩空間
│   ├── 區塊鏈/
│   │   ├── core/          # 核心結構
│   │   ├── consensus/     # 共識演算法
│   │   ├── smart_contract/ # 智能合約
│   │   └── wallet/        # 錢包
│   ├── 量子計算/
│   │   ├── gates/         # 量子閘與電路
│   │   ├── algorithms/    # 量子演算法
│   │   └── concepts/      # 量子概念
│   ├── 資訊理論/
│   │   ├── entropy/       # 熵計算
│   │   ├── channel/       # 通道模型
│   │   ├── coding/        # 通道編碼
│   │   └── source/        # 信源編碼理論
│   ├── 分散式演算法/
│   │   ├── election/      # 領導者選舉
│   │   ├── consensus/     # 共識協定
│   │   ├── clock/         # 邏輯時鐘
│   │   ├── snapshot/      # 快照演算法
│   │   └── gossip/        # 流行病協定
│   └── 形式方法/
│       ├── model_checking/ # 模型檢查
│       ├── theorem/        # 定理證明
│       ├── symbolic/       # 符號執行
│       ├── abstract/       # 抽象解釋
│       └── contract/       # 契約式設計
├── wiki/                  # Wiki 文章
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

#### flow/ (v4.0)
- [x] push_relabel.py + push_relabel.md — 前置推送-重標號最大流演算法
- [x] hungarian.py + hungarian.md — 匈牙利演算法（指派問題）
- [x] min_mean_cycle.py + min_mean_cycle.md — 最小均值環演算法

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

#### reinforcement/ (v4.0)
- [x] policy_gradient.py + policy_gradient.md — 策略梯度法（REINFORCE）
- [x] actor_critic.py + actor_critic.md — Actor-Critic 演算法
- [x] dqn.py + dqn.md — 深度 Q 網路
- [x] ddpg.py + ddpg.md — 深度確定性策略梯度

#### generative/ (v4.0)
- [x] autoencoder.py + autoencoder.md — 自編碼器
- [x] vae.py + vae.md — 變分自編碼器
- [x] gan.py + gan.md — 生成對抗網路
- [x] diffusion.py + diffusion.md — 擴散模型

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

### 數值方法 - 程式碼 (code/數值方法/) — 已完成

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

#### advanced/ (v4.0)
- [x] finite_difference.py + finite_difference.md — 有限差分法（前向/後向/中央差分、熱傳導方程）
- [x] finite_element.py + finite_element.md — 有限元素法（一維 Galerkin 方法、Poisson 方程）
- [x] fft_advanced.py + fft_advanced.md — FFT 進階應用（摺積、多項式乘法）

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

### 計算理論 - Wiki 文章 (wiki/計算理論/)

- [x] 哥德爾不完備定理.md
- [x] 歸約.md
- [x] np完全.md
- [x] p與np.md

### 電腦圖學 - 程式碼 (code/電腦圖學/) — 已完成 (v4.0)

#### raster/ — 光柵化演算法
- [x] bresenham.py + bresenham.md — 布雷森漢姆直線演算法
- [x] midpoint_circle.py + midpoint_circle.md — 中點畫圓演算法
- [x] polygon_fill.py + polygon_fill.md — 掃描線多邊形填充
- [x] line_aa.py + line_aa.md — Xiaolin Wu 反鋸齒直線

#### transform/ — 幾何變換
- [x] transform2d.py + transform2d.md — 2D 幾何變換（平移、旋轉、縮放）
- [x] transform3d.py + transform3d.md — 3D 變換與投影（正交/透視）

#### render/ — 渲染演算法
- [x] ray_tracing.py + ray_tracing.md — 基礎光線追蹤（光線-球體相交、反射、漫射）
- [x] z_buffer.py + z_buffer.md — Z-Buffer 隱面消除

#### clip/ — 裁剪演算法
- [x] cohen_sutherland.py + cohen_sutherland.md — Cohen-Sutherland 直線裁剪
- [x] sutherland_hodgman.py + sutherland_hodgman.md — Sutherland-Hodgman 多邊形裁剪

#### color/ — 色彩空間
- [x] color_space.py + color_space.md — RGB/HSL/HSV 轉換與色彩操作

### 區塊鏈 - 程式碼 (code/區塊鏈/) — 已完成 (v4.0)

#### core/ — 核心結構
- [x] block.py + block.md — 區塊與區塊鏈結構
- [x] merkle_tree.py + merkle_tree.md — Merkle Tree 默克爾樹
- [x] proof_of_work.py + proof_of_work.md — 工作量證明 PoW

#### consensus/ — 共識演算法
- [x] proof_of_stake.py + proof_of_stake.md — 權益證明 PoS
- [x] pbft.py + pbft.md — 實用拜占庭容錯
- [x] raft.py + raft.md — Raft 共識演算法
- [x] paxos.py + paxos.md — Paxos 共識演算法

#### smart_contract/ — 智能合約
- [x] evm_simple.py + evm_simple.md — 簡化版 EVM 虛擬機

#### wallet/ — 錢包
- [x] address.py + address.md — 錢包地址生成
- [x] transaction.py + transaction.md — 交易結構（UTXO 模型）
- [x] signature_verify.py + signature_verify.md — ECDSA 簽章驗證

### 量子計算 - 程式碼 (code/量子計算/) — 已完成 (v4.0)

#### gates/ — 量子閘與電路
- [x] quantum_gates.py + quantum_gates.md — 基本量子閘 (H, X, Y, Z, CNOT, T, S) 與矩陣表示
- [x] circuit.py + circuit.md — 量子電路模擬器（閘序列組合、狀態演化、測量）

#### algorithms/ — 量子演算法
- [x] deutsch.py + deutsch.md — Deutsch 演算法（首個展現量子優勢的演算法）
- [x] grover.py + grover.md — Grover 搜尋演算法（O(√n) 非結構化搜尋）
- [x] shor.py + shor.md — Shor 因數分解演算法（量子傅立葉變換、指數加速）
- [x] quantum_teleportation.py + quantum_teleportation.md — 量子隱形傳態協定
- [x] bernstein_vazirani.py + bernstein_vazirani.md — Bernstein-Vazirani 演算法（單次查詢找隱藏字串）
- [x] simon.py + simon.md — Simon 演算法（指數加速前驅、週期尋找）

#### concepts/ — 量子概念
- [x] bell_state.py + bell_state.md — Bell 態（最大糾纏對、CHSH 不等式）
- [x] density_matrix.py + density_matrix.md — 密度矩陣（純態 vs 混合態、部分跡）

### 資訊理論 - 程式碼 (code/資訊理論/) — 已完成 (v4.0)

#### entropy/ — 熵計算
- [x] entropy.py + entropy.md — 香農熵、聯合熵、條件熵
- [x] mutual_info.py + mutual_info.md — 互資訊、KL 散度、交叉熵

#### channel/ — 通道模型
- [x] channel_capacity.py + channel_capacity.md — 通道容量、香農第二定理、DMC 容量
- [x] binary_channel.py + binary_channel.md — BSC、BEC 模擬與錯誤分析

#### coding/ — 通道編碼
- [x] hamming_code.py + hamming_code.md — 海明碼 (7,4)、錯誤修正
- [x] reed_solomon.py + reed_solomon.md — 里德-所羅門碼、GF(256) 算術
- [x] crc.py + crc.md — CRC-8、CRC-16、CRC-32 多項式檢查

#### source/ — 信源編碼理論
- [x] channel_coding_theorem.py + channel_coding_theorem.md — 通道編碼定理示範、Shannon 極限
- [x] rate_distortion.py + rate_distortion.md — 率失真函數、Blahut-Arimoto 演算法

### 分散式演算法 - 程式碼 (code/分散式演算法/) — 已完成 (v4.0)

#### election/ — 領導者選舉
- [x] bully.py + bully.md — Bully 演算法（霸道演算法）、優先權選舉
- [x] ring.py + ring.md — 環狀選舉演算法、令牌傳遞

#### consensus/ — 共識協定
- [x] two_phase_commit.py + two_phase_commit.md — 兩階段提交 (2PC)
- [x] three_phase_commit.py + three_phase_commit.md — 三階段提交 (3PC)

#### clock/ — 邏輯時鐘
- [x] lamport_clock.py + lamport_clock.md — Lamport 邏輯時鐘、happens-before 關係
- [x] vector_clock.py + vector_clock.md — 向量時鐘、因果順序、衝突檢測

#### snapshot/ — 快照演算法
- [x] chandy_lamport.py + chandy_lamport.md — Chandy-Lamport 快照演算法

#### gossip/ — 流行病協定
- [x] gossip_protocol.py + gossip_protocol.md — Gossip 協定、資訊傳播
- [x] anti_entropy.py + anti_entropy.md — 反熵同步、Push-Pull 策略

### 形式方法 - 程式碼 (code/形式方法/) — 已完成 (v4.0)

#### model_checking/ — 模型檢查
- [x] kripke.py + kripke.md — Kripke 結構（時序邏輯模型）
- [x] ctl.py + ctl.md — CTL 計算樹邏輯（分支時序邏輯）
- [x] ltl.py + ltl.md — LTL 線性時序邏輯

#### theorem/ — 定理證明
- [x] resolution.py + resolution.md — 一階邏輯歸結原理
- [x] tableau.py + tableau.md — 語意表決演算法

#### symbolic/ — 符號執行
- [x] symbolic_execution.py + symbolic_execution.md — 符號執行引擎（路徑爆炸、約束求解）

#### abstract/ — 抽象解釋
- [x] abstract_interp.py + abstract_interp.md — 抽象解釋框架（抽象域、轉遞函數）

#### contract/ — 契約式設計
- [x] design_by_contract.py + design_by_contract.md — 契約式設計（前置條件、後置條件、不變量）

## 開發順序

### 第一至六階段 (v1.0-v2.0): 已完成 ✓

| 階段 | 領域 | 完成狀態 |
|---|---|---|
| 第一階段 | 計算理論 | ✓ 已完成 |
| 第二階段 | 演算法 | ✓ 已完成 |
| 第三階段 | 人工智慧 | ✓ 已完成 |
| 第四階段 | 程式語言 | ✓ 已完成 |
| 第五階段 | 密碼學 | ✓ 已完成 |
| 第六階段 | 資料結構 | ✓ 已完成 |

### 第七至十一階段 (v3.0): 已完成 ✓

| 階段 | 領域 | 完成狀態 |
|---|---|---|
| 第七階段 | 資料壓縮 | ✓ 已完成 |
| 第八階段 | 數值方法 | ✓ 已完成 |
| 第九階段 | 計算幾何 | ✓ 已完成 |
| 第十階段 | 資訊檢索 | ✓ 已完成 |
| 第十一階段 | 機率演算法 | ✓ 已完成 |

### 第十二至十七階段 (v4.0): 已完成 ✓

| 階段 | 領域 | 完成狀態 |
|---|---|---|
| 第十二階段 | 電腦圖學 | ✓ 已完成 |
| 第十三階段 | 區塊鏈 | ✓ 已完成 |
| 第十四階段 | 量子計算 | ✓ 已完成 |
| 第十五階段 | 資訊理論 | ✓ 已完成 |
| 第十六階段 | 分散式演算法 | ✓ 已完成 |
| 第十七階段 | 形式方法 | ✓ 已完成 |

### 擴充項目 (v4.0): 已完成 ✓

| 領域 | 擴充項目 |
|---|---|
| 人工智慧/ | reinforcement/ (4), generative/ (4) |
| 演算法/ | flow/ (3) |
| 數值方法/ | advanced/ (3) |

---

## v4.0 完成總結

### 新增領域（6 個）
| 領域 | 子目錄數 | .py/.md 對數 |
|---|---|---|
| 電腦圖學 | 5 | 11 |
| 區塊鏈 | 4 | 11 |
| 量子計算 | 3 | 10 |
| 資訊理論 | 4 | 9 |
| 分散式演算法 | 5 | 9 |
| 形式方法 | 5 | 11 |

### 擴充項目（v4.0）
| 領域 | 項目 |
|---|---|
| 人工智慧/reinforcement/ | policy_gradient, actor_critic, dqn, ddpg (4) |
| 人工智慧/generative/ | autoencoder, vae, gan, diffusion (4) |
| 演算法/flow/ | push_relabel, hungarian, min_mean_cycle (3) |
| 數值方法/advanced/ | finite_difference, finite_element, fft_advanced (3) |

### v4.0 統計
| 項目 | 數量 |
|---|---|
| 新增 .py 檔案 | 71 個 |
| 新增 .md 檔案 | 71 個 |
| 新增領域數 | 6 個 |
| 新增子目錄數 | 26 個 |

### 總計（v1.0 + v2.0 + v3.0 + v4.0）

| 領域 | .py/.md 對數 |
|---|---|
| 計算理論 | 17 |
| 演算法 | 40 |
| 人工智慧 | 33 |
| 密碼學 | 9 |
| 資料結構 | 7 |
| 程式語言 | 4 |
| 資料壓縮 | 10 |
| 數值方法 | 16 |
| 計算幾何 | 11 |
| 資訊檢索 | 10 |
| 機率演算法 | 11 |
| 電腦圖學 | 11 |
| 區塊鏈 | 11 |
| 量子計算 | 10 |
| 資訊理論 | 9 |
| 分散式演算法 | 9 |
| 形式方法 | 11 |
| **總計** | **229 個** |

### 頂層領域（17 個）
計算理論、演算法、人工智慧、密碼學、資料結構、程式語言、資料壓縮、數值方法、計算幾何、資訊檢索、機率演算法、電腦圖學、區塊鏈、量子計算、資訊理論、分散式演算法、形式方法

---

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