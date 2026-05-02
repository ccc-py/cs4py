# 割点与桥检测（Tarjan 算法）

## 历史背景
Tarjan 算法由美国计算机科学家 Robert Tarjan 于 1972 年在其论文《Depth-first search and linear graph algorithms》中首次提出。该算法是图论领域最具影响力的经典算法之一，能够在线性时间 O(V+E) 内完成无向图的割点（Articulation Point / Cut Vertex）和桥（Bridge / Cut Edge）检测，广泛应用于网络可靠性分析、社交网络连通性检测、电路设计等领域。

## 核心原理
Tarjan 算法的核心是深度优先搜索（DFS）与两个关键变量的维护：
1. **发现时间（Discovery Time, `disc[u]`）**：节点 `u` 在 DFS 遍历中被首次访问的时间戳，全局唯一递增。
2. **Low-link 值（`low[u]`）**：从节点 `u` 出发，通过任意条树边和最多一条回边（Back Edge），能够到达的最早（最小）发现时间。

### 割点判断规则
对于 DFS 树中的节点 `u`：
- 若 `u` 是根节点（无父节点），且有 **2 个及以上子节点**，则 `u` 是割点。
- 若 `u` 不是根节点，且存在子节点 `v` 满足 `low[v] >= disc[u]`，则 `u` 是割点（移除 `u` 后，子节点 `v` 所在的子树与图的其他部分断开）。

### 桥判断规则
对于 DFS 树中的边 `(u, v)`（`u` 是 `v` 的父节点）：
- 若 `low[v] > disc[u]`，则边 `(u, v)` 是桥（移除该边后，图会分裂为两个连通分量）。

## 使用示例
### 代码调用
```python
from articulation import TarjanGraph

# 定义图结构：6 个节点，边列表
edges = [
    (0, 1), (1, 2), (2, 0),  # 三角形组件1
    (1, 3),                   # 桥连接两个组件
    (3, 4), (4, 5), (5, 3)    # 三角形组件2
]
detector = TarjanGraph(6, edges)
articulation_points, bridges, disc, low = detector.find_articulation_bridges()

print("割点:", sorted(articulation_points))  # 输出 [1, 3]
print("桥:", sorted(bridges))                # 输出 [(1, 3)]
```

### 输出结果
```
=== Tarjan 算法示例 ===
节点数: 6
发现时间 (disc): [0, 1, 2, 3, 4, 5]
Low-link 值 (low): [0, 0, 0, 1, 3, 3]
割点集合: [1, 3]
桥集合: [(1, 3)]
```

## 参考资料
1. Tarjan, R. (1972). *Depth-first search and linear graph algorithms*. SIAM Journal on Computing, 1(2), 146-160.
2. Wikipedia: [双连通分量](https://zh.wikipedia.org/wiki/%E5%8F%8C%E8%BF%9E%E9%80%9A%E5%88%86%E9%87%8F)
3. Wikipedia: [桥 (图论)](https://zh.wikipedia.org/wiki/%E6%A1%A5_(%E5%9B%BE%E8%AE%BA))
4. Wikipedia: [关节点](https://zh.wikipedia.org/wiki/%E5%85%B3%E8%8A%82%E7%82%B9)
