# cs4py 專案內容規劃

本專案使用 Python 實作資訊科學的各種經典方法與程式，從歷史角度選取具有代表性的演算法與系統。

## ai/ 人工智慧

### 搜尋演算法
- `search/bfs.py` - 廣度優先搜尋 (BFS)
- `search/dfs.py` - 深度優先搜尋 (DFS)
- `search/astar.py` - A* 搜尋演算法
- `search/ucs.py` - 統一成本搜尋 (Uniform Cost Search)

### 經典問題
- `puzzle/eight_queens.py` - 八皇后問題
- `puzzle/knights_tour.py` - 騎士巡禮問題
- `puzzle/maze.py` - 迷宮生成與求解
- `puzzle/sudoku.py` - 數獨求解器

### 機器學習 (Machine Learning)
- `ml/perceptron.py` - 感知器 (Perceptron, 1958)
- `ml/adaline.py` - ADALINE (1960)
- `ml/knn.py` - K-近鄰演算法 (KNN)
- `ml/decision_tree.py` - 決策樹 (ID3/C4.5)
- `ml/random_forest.py` - 隨機森林
- `ml/naive_bayes.py` - 朴素貝葉斯分類器
- `ml/logistic_regression.py` - 羅吉斯回歸
- `ml/svm.py` - 支援向量機 (SVM, 1963)
- `ml/pca.py` - 主成分分析 (PCA)
- `ml/kmeans.py` - K-means 聚類
- `ml/hierarchical_clustering.py` - 階層式聚類
- `ml/em.py` - 期望最大化演算法 (EM)
- `ml/hmm.py` - 隱馬爾可夫模型 (HMM)
- `ml/linear_regression.py` - 線性回歸
- `ml/ridge_lasso.py` - Ridge & Lasso 回歸

### 演化計算 (Evolutionary Computation)
- `evolution/genetic_algorithm.py` - 遺傳演算法 (Holland, 1975)
- `evolution/genetic_programming.py` - 遺傳程式設計 (Koza, 1992)
- `evolution/evolution_strategies.py` - 演化策略 (ES)
- `evolution/pso.py` - 粒子群最佳化 (PSO, 1995)
- `evolution/ant_colony.py` - 蟻群演算法 (1992)

### 遊戲 AI
- `game/minimax.py` - Minimax 演算法
- `game/alpha_beta.py` - Alpha-Beta 剪枝
- `game/tictactoe.py` - 井字遊戲 AI
- `game/alphago.py` - AlphaGo 簡化版 (MCTS + 神經網路)

### 深度學習 / 神經網路 (Deep Learning)
- `nn/engine.py` - 神經網路引擎 (從頭實作，不含框架)
- `nn/layer.py` - 層實作 (Dense, Conv2D, RNN, LSTM)
- `nn/activation.py` - 激活函數 (ReLU, Sigmoid, Tanh, Softmax, GELU)
- `nn/optimizer.py` - 優化器 (SGD, Momentum, Adam, AdamW)
- `nn/loss.py` - 損失函數 (MSE, Cross-Entropy, BCE)
- `nn/train.py` - 訓練循環示範
- `nn/mlp.py` - 多層感知機 (MLP)
- `nn/cnn.py` - 卷積神經網路 (LeNet, AlexNet, VGG)
- `nn/rnn.py` - 循環神經網路 (RNN, 1980s)
- `nn/lstm.py` - 長短期記憶網路 (LSTM, 1997)
- `nn/gru.py` - 門控循環單元 (GRU, 2014)
- `nn/autoencoder.py` - 自編碼器 (Autoencoder)
- `nn/gan.py` - 生成對抗網路 (GAN, 2014)
- `nn/diffusion.py` - 擴散模型 (Diffusion Model, 2020)
- `nn/attention.py` - 注意力機制 (Attention, 2014)
- `nn/transformer.py` - Transformer 架構 (2017)
- `nn/gpt.py` - GPT 系列 (GPT-1/2/3, 2018-2020)
- `nn/bert.py` - BERT 模型 (2018)
- `nn/vision_transformer.py` - Vision Transformer (ViT, 2020)
- `nn/clip.py` - CLIP 模型 (2021)
- `nn/resnet.py` - ResNet 殘差網路 (2015)

### 強化學習 (Reinforcement Learning)
- `rl/q_learning.py` - Q-Learning (Watkins, 1989)
- `rl/sarsa.py` - SARSA 演算法
- `rl/dqn.py` - Deep Q-Network (DQN, 2015)
- `rl/policy_gradient.py` - 策略梯度 (Policy Gradient)
- `rl/actor_critic.py` - Actor-Critic 方法
- `rl/ppo.py` - Proximal Policy Optimization (PPO, 2017)
- `rl/a3c.py` - Asynchronous Advantage Actor-Critic (A3C)
- `rl/ddpg.py` - Deep Deterministic Policy Gradient (DDPG)
- `rl/td3.py` - Twin Delayed DDPG (TD3)
- `rl/sac.py` - Soft Actor-Critic (SAC)
- `rl/mcts.py` - 蒙地卡羅樹搜尋 (MCTS, 2006)
- `rl/reward_shaping.py` - 獎勵塑形 (Reward Shaping)
- `rl/rlhf.py` - 人類回饋強化學習 (RLHF, 2022)

### AI Agent
- `agent/base.py` - Agent 基礎介面 (感知-思考-行動循環)
- `agent/react.py` - ReAct Agent (推理 + 行動, 2022)
- `agent/tool.py` - 工具呼叫機制 (Tool Calling)
- `agent/memory.py` - 記憶機制 (短期/長期記憶, RAG)
- `agent/planning.py` - 規劃能力 (任務分解, CoT)
- `agent/langchain_style.py` - 類 LangChain 風格的 Agent 框架
- `agent/autogpt.py` - AutoGPT 簡化版 (目標導向 Agent)
- `agent/multi_agent.py` - 多 Agent 協作系統

## algorithm/ 演算法

### 演算法設計方法論 (Algorithm Design Methods)
- `method/divide_and_conquer.py` - 分治法 (Divide and Conquer)
- `method/dynamic_programming.py` - 動態規劃 (Dynamic Programming)
- `method/greedy.py` - 貪婪演算法 (Greedy Method)
- `method/backtracking.py` - 回溯法 (Backtracking)
- `method/branch_and_bound.py` - 分支限界法 (Branch and Bound)
- `method/randomized.py` - 隨機化演算法 (Randomized Algorithms)
- `method/approximation.py` - 近似演算法 (Approximation Algorithms)
- `method/parallel.py` - 平行演算法 (Parallel Algorithms)
- `method/online.py` - 線上演算法 (Online Algorithms)
- `method/recursive.py` - 遞迴思維 (Recursive Thinking)

### 排序演算法
- `sort/bubble_sort.py` - 氣泡排序 (1956)
- `sort/selection_sort.py` - 選擇排序
- `sort/insertion_sort.py` - 插入排序
- `sort/quick_sort.py` - 快速排序 (Hoare, 1960)
- `sort/merge_sort.py` - 合併排序 (von Neumann, 1945)
- `sort/heap_sort.py` - 堆積排序 (Williams, 1964)
- `sort/counting_sort.py` - 計數排序
- `sort/radix_sort.py` - 基數排序

### 搜尋演算法
- `search/linear_search.py` - 線性搜尋
- `search/binary_search.py` - 二分搜尋 (1946)
- `search/interpolation_search.py` - 內插搜尋

### 圖論演算法
- `graph/dijkstra.py` - Dijkstra 最短路徑 (1956)
- `graph/bellman_ford.py` - Bellman-Ford 演算法 (1958)
- `graph/floyd_warshall.py` - Floyd-Warshall 演算法 (1962)
- `graph/kruskal.py` - Kruskal 最小生成樹 (1956)
- `graph/prim.py` - Prim 最小生成樹 (1930)
- `graph/topological_sort.py` - 拓撲排序
- `graph/strongly_connected.py` - 強連通分量 (Kosaraju/Tarjan)

### 動態規劃
- `dp/fibonacci.py` - 費波那契數列
- `dp/knapsack.py` - 背包問題
- `dp/lis.py` - 最長遞增子序列
- `dp/lcs.py` - 最長共同子序列
- `dp/edit_distance.py` - 編輯距離

### 字串演算法
- `string/naive.py` - 樸素字串匹配
- `string/kmp.py` - KMP 演算法 (1970)
- `string/boyer_moore.py` - Boyer-Moore 演算法 (1977)
- `string/rabin_karp.py` - Rabin-Karp 演算法 (1987)

### 數論演算法
- `math/gcd.py` - 輾轉相除法 (歐幾里得)
- `math/sieve.py` - 埃拉托斯特尼篩法
- `math/modular_exponentiation.py` - 模冪運算
- `math/extended_gcd.py` - 擴展歐幾里得演算法

## interpreter/ 解譯器

### Lisp 家族
- `lisp/reader.py` - S-表達式解析器
- `lisp/evaluator.py` - Lisp 求值器
- `lisp/env.py` - 環境模型
- `lisp/special_forms.py` - 特殊形式 (lambda, define, if)

### FORTH
- `forth/stack.py` - 堆疊機實作
- `forth/parser.py` - FORTH 解析器
- `forth/dictionary.py` - 字典 (詞典)
- `forth/interpreter.py` - FORTH 解譯器

### 簡單語言
- `calc/lexer.py` - 計算器詞法分析器
- `calc/parser.py` - 計算器語法分析器
- `calc/eval.py` - 計算器求值器

### 虛擬機器
- `vm/stack_vm.py` - 堆疊式虛擬機器
- `vm/register_vm.py` - 暫存器式虛擬機器

### Scheme
- `scheme/interpreter.py` - 簡易 Scheme 解譯器

## theory/ 計算理論

### 自動機
- `automata/dfa.py` - 確定性有限狀態自動機 (DFA)
- `automata/nfa.py` - 非確定性有限狀態自動機 (NFA)
- `automata/nfa_to_dfa.py` - NFA 轉 DFA (子集構造法)
- `automata/pda.py` - 下推自動機 (PDA)
- `automata/turing.py` - 圖靈機模擬器

### 正規語言
- `regex/engine.py` - 正規表達式引擎 (從頭實作)
- `regex/nfa_builder.py` - 正規表達式轉 NFA (Thompson 構造法)

### Lambda 演算
- `lambda_calculus/parser.py` - Lambda 表達式解析器
- `lambda_calculus/reducer.py` - Beta 化簡
- `lambda_calculus/encoder.py` - Church 編碼

### 細胞自動機
- `cellular/game_of_life.py` - 康威生命遊戲 (1970)
- `cellular/rule30.py` - Rule 30 細胞自動機

### 可計算性理論
- `computability/halting.py` - 停機問題演示
- `computability/busy_beaver.py` - 忙碌海狸問題
- `computability/godel_incompleteness.py` - 哥德尔不完备定理演示 (1931)
- `computability/godel_number.py` - 哥德尔數編碼

### 形式語言
- `grammar/cfg.py` - 上下文無關文法
- `grammar/cyk.py` - CYK 演算法 (Cocke-Younger-Kasami)

### 計算複雜度 (Computational Complexity)
- `complexity/p_vs_np.py` - P vs NP 問題演示
- `complexity/np_complete.py` - NP-完備性簡介 (Cook-Levin 定理, 1971)
- `complexity/sat.py` - SAT 問題求解器 (布林可滿足性)
- `complexity/reduction.py` - 多項式時間歸約 (Polynomial-time Reduction)
- `complexity/tsp.py` - 旅行推銷員問題 (TSP) - NP-hard
- `complexity/knapsack_nphard.py` - 背包問題的 NP-hard 版本
- `complexity/clique.py` - 最大團問題 (Clique Problem)
- `complexity/vertex_cover.py` - 頂點覆蓋問題 (Vertex Cover)

## 實作原則

1. **歷史價值**：優先選取對資訊科學發展有重要影響的演算法與系統
2. **可讀性**：程式碼清晰易懂，包含適當註釋
3. **教學性**：適合作為學習教材，展現核心概念
4. **純 Python**：盡量使用純 Python 實作，減少外部依賴
5. **測試**：每個實作都包含測試程式或範例使用方式
