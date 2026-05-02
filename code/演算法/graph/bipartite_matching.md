# 二分图最大匹配（Hopcroft-Karp 算法）

## 历史背景
Hopcroft-Karp 算法由 John Hopcroft 和 Richard Karp 于 1973 年提出，是求解二分图最大匹配的经典高效算法，时间复杂度为 O(E√V)，远优于朴素的增广路算法（O(VE)）。该算法通过分层广度优先搜索（BFS）批量寻找最短增广路，再结合深度优先搜索（DFS）更新匹配，大幅减少了增广次数，被广泛应用于任务分配、资源调度、推荐系统等领域。

## 核心原理
### 二分图定义
二分图（Bipartite Graph）的节点可划分为两个不相交的集合 U 和 V，所有边仅连接 U 和 V 中的节点，不存在内部边。匹配（Matching）是边的集合，满足每个节点最多属于一条边；最大匹配是边数最多的匹配。

### Hopcroft-Karp 算法步骤
1. **BFS 分层**：从未匹配的 U 部节点出发，构建分层图，记录每个节点到起始点的最短距离，直到找到未匹配的 V 部节点。
2. **DFS 增广**：基于分层图，寻找所有最短增广路（从不匹配 U 部节点到不匹配 V 部节点的路径），批量更新匹配关系。
3. 重复上述两步，直到无法找到新的增广路，此时的匹配即为最大匹配。

## 使用示例
### 任务分配场景
假设有 3 个工人和 3 个任务，每个工人可胜任的任务如下：
- 工人0：任务0、任务1
- 工人1：任务1、任务2
- 工人2：任务0、任务2

目标是为每个工人分配最多一个任务，每个任务最多分配给一个工人，求最大可完成的任务数。

### 代码调用
```python
from bipartite_matching import HopcroftKarp

num_u = 3  # 工人数量
num_v = 3  # 任务数量
edges = [
    (0, 0), (0, 1),
    (1, 1), (1, 2),
    (2, 0), (2, 2)
]
hk = HopcroftKarp(num_u, num_v, edges)
max_match, matches = hk.max_matching()

print("最大匹配数:", max_match)  # 输出 3
print("匹配结果:", matches)       # 输出 {0:0, 1:1, 2:2}
```

### 输出结果
```
=== 二分图最大匹配示例（任务分配）===
工人数量: 3, 任务数量: 3
最大匹配数: 3
匹配结果（工人 -> 任务）:
  工人0 -> 任务0
  工人1 -> 任务1
  工人2 -> 任务2
```

## 参考资料
1. Hopcroft, J. E., & Karp, R. M. (1973). *An n^5/2 algorithm for maximum matchings in bipartite graphs*. SIAM Journal on Computing, 2(4), 225-231.
2. Wikipedia: [Hopcroft–Karp algorithm](https://zh.wikipedia.org/wiki/Hopcroft%E2%80%93Karp%E7%AE%97%E6%B3%95)
3. Wikipedia: [二分图](https://zh.wikipedia.org/wiki/%E4%BA%8C%E5%88%86%E5%9B%BE)
4. Wikipedia: [匹配 (图论)](https://zh.wikipedia.org/wiki/%E5%8C%B9%E9%85%8D_(%E5%9B%BE%E8%AE%BA))
