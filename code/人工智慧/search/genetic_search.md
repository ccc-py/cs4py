# 遺傳搜尋演算法 (Genetic Search Algorithm)

## 歷史背景

遺傳演算法（Genetic Algorithm）由 John Holland 於 1975 年在《Adaptation in Natural and Artificial Systems》中正式提出。雖然 Holland 奠定了理論基礎，但將 GA 應用於搜尋問題（而非單純的函數最佳化）則是後續研究者的貢獻。

本模組專注於將遺傳演算法應用於**搜尋問題**，不同於 `evolution/genetic_algorithm.py` 的連續函數最佳化，這裡處理的是離散的組合搜尋空間。

## 遺傳搜尋 vs 遺傳演算法（函數最佳化）

| 特性 | 遺傳搜尋 (Genetic Search) | 遺傳演算法 (Function Optimization) |
|------|--------------------------|-----------------------------------|
| 搜尋空間 | 離散、組合空間 | 連續或離散數值空間 |
| 染色體編碼 | 二進制、排列、符號序列 | 實數向量、二進制 |
| 應用問題 | N-皇后、TSP、排程、約束滿足 | 數學函數極值、參數調優 |
| 適應度評估 | 約束違反程度、目標達成度 | 函數值直接評估 |

## 核心原理

### 演算法流程

```
1. 初始化族群（隨機產生一組染色體）
2. 重複直到滿足終止條件：
   a. 評估每個個體的適應度
   b. 選擇：根據適應度挑選父母（競賽選擇、輪盤賭等）
   c. 交叉：父母染色體交換片段產生後代
   d. 突變：隨機改變染色體的某些基因
   e. 菁英保留：保留適應度最高的個體
3. 返回最佳解
```

### 關鍵組件

1. **編碼（Encoding）**：將搜尋問題的解表示為染色體
   - 二進制：用 0/1 序列表示是否選取某元素
   - 排列：用順序排列表示路徑、排程等

2. **適應度函數（Fitness Function）**：評估解的好壞
   - 搜尋問題中，通常將「距離目標的遠近」轉為適應度
   - 找到合法解時給予高獎勵

3. **選擇（Selection）**：挑選優良個體作為父母
   - 競賽選擇：隨機選 k 個，取最佳者
   - 輪盤賭：機率與適應度成正比

4. **交叉（Crossover）**：產生新個體
   - 單點交叉：在隨機位置切開，交換兩側
   - 均勻交叉：每個基因隨機選自父母

5. **突變（Mutation）**：維持族群多樣性
   - 位元翻轉：0 變 1，1 變 0
   - 交換變異：隨機交換兩個位置

## 使用範例

### N-皇后問題

在 N×N 棋盤上放置 N 個皇后，使其互不攻擊。

```python
from search.genetic_search import NQueensProblem, BinaryGeneticSearch

problem = NQueensProblem(n=8)
search = BinaryGeneticSearch(
    problem=problem,
    n_bits=32,  # 每個位置用足夠位元表示
    population_size=100,
    max_generations=200,
    seed=42,
)

best, fitness, history = search.run()
if problem.is_solution(best):
    print(f"找到解！\n{problem.decode(best)}")
```

### 子集和問題

從一組數字中找出子集，使其和等於目標值。

```python
from search.genetic_search import SubsetSumProblem, BinaryGeneticSearch

numbers = [3, 34, 4, 12, 5, 2]
target = 9

problem = SubsetSumProblem(numbers, target)
search = BinaryGeneticSearch(problem, n_bits=len(numbers))
best, fitness, _ = search.run()

print(problem.decode(best))  # 顯示選取結果
```

## 在人工智慧中的應用

1. **約束滿足問題（CSP）**：排程、資源分配
2. **路徑規劃**：在複雜環境中搜尋可行路徑
3. **特徵選擇**：從大量特徵中選取最優子集
4. **遊戲策略搜尋**：演化出有效的遊戲策略

## 參考資料

- Holland, J. H. (1975). *Adaptation in Natural and Artificial Systems*. University of Michigan Press.
- Goldberg, D. E. (1989). *Genetic Algorithms in Search, Optimization, and Machine Learning*. Addison-Wesley.
- Mitchell, M. (1998). *An Introduction to Genetic Algorithms*. MIT Press.
