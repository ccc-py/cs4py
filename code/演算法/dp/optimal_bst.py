"""
最優二叉搜尋樹 (Optimal Binary Search Tree)

包含：
1. 給定鍵值和搜尋頻率，建構期望搜尋成本最小的 BST
2. 動態規劃解法
3. Knuth 優化（選擇性實作）
4. 樹的結構重建與視覺化
"""

from typing import List, Tuple, Optional
import sys


def optimal_bst_dp(keys: List[int], freq: List[float]) -> Tuple[float, List[List[Optional[int]]]]:
    """
    最優二叉搜尋樹 - 動態規劃解法
    
    給定 n 個鍵值（已排序）和對應的搜尋頻率（或機率），
    建構一棵二叉搜尋樹，使得期望搜尋成本最小。
    
    期望搜尋成本 = Σ freq[i] * (depth[i] + 1)
    其中 depth[i] 是鍵值 i 在樹中的深度。
    
    時間複雜度：O(n³)
    空間複雜度：O(n²)
    
    Args:
        keys: 已排序的鍵值列表（遞增）
        freq: 對應的搜尋頻率（或機率）
        
    Returns:
        (最小期望成本, root_table) - root_table 用於重建樹結構
    """
    n = len(keys)
    
    # 前綴和陣列，用於快速計算 freq[i..j] 的和
    prefix_sum = [0] * (n + 1)
    for i in range(n):
        prefix_sum[i + 1] = prefix_sum[i] + freq[i]
    
    # dp[i][j] 表示鍵值 i..j 構成的最優 BST 的最小期望成本
    dp = [[0.0] * n for _ in range(n)]
    # root[i][j] 記錄鍵值 i..j 構成的最優 BST 的根節點索引
    root = [[None] * n for _ in range(n)]
    
    # 初始化：單個節點的情況
    for i in range(n):
        dp[i][i] = freq[i]
        root[i][i] = i
    
    # 計算長度從 2 到 n 的子問題
    for length in range(2, n + 1):  # length 是子問題的大小
        for i in range(n - length + 1):
            j = i + length - 1
            
            # 找出以哪個節點作為根可以得到最小成本
            min_cost = sys.float_info.max
            best_root = None
            
            # 嘗試每個可能的根節點 k
            for k in range(i, j + 1):
                # 左子樹成本（如果存在）
                left_cost = dp[i][k - 1] if k > i else 0.0
                # 右子樹成本（如果存在）
                right_cost = dp[k + 1][j] if k < j else 0.0
                # 當前節點為根的成本
                # 注意：所有在 i..j 範圍內的節點深度都增加 1
                cost = left_cost + right_cost + (prefix_sum[j + 1] - prefix_sum[i])
                
                if cost < min_cost:
                    min_cost = cost
                    best_root = k
            
            dp[i][j] = min_cost
            root[i][j] = best_root
    
    return dp[0][n - 1], root


def optimal_bst_knuth(keys: List[int], freq: List[float]) -> Tuple[float, List[List[Optional[int]]]]:
    """
    最優二叉搜尋樹 - 使用 Knuth 優化
    
    Knuth 證明了對於最優 BST，滿足：
    root[i][j-1] <= root[i][j] <= root[i+1][j]
    
    這個性質可以將時間複雜度從 O(n³) 降到 O(n²)。
    
    Args:
        keys: 已排序的鍵值列表
        freq: 搜尋頻率
        
    Returns:
        (最小期望成本, root_table)
    """
    n = len(keys)
    
    prefix_sum = [0] * (n + 1)
    for i in range(n):
        prefix_sum[i + 1] = prefix_sum[i] + freq[i]
    
    dp = [[0.0] * n for _ in range(n)]
    root = [[None] * n for _ in range(n)]
    
    # 初始化
    for i in range(n):
        dp[i][i] = freq[i]
        root[i][i] = i
    
    # Knuth 優化：root[i][j-1] <= root[i][j] <= root[i+1][j]
    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            
            # 根據 Knuth 優化，搜索範圍縮小
            left_bound = root[i][j - 1] if j > i else i
            right_bound = root[i + 1][j] if i < j else j
            
            min_cost = sys.float_info.max
            best_root = None
            
            for k in range(left_bound, right_bound + 1):
                left_cost = dp[i][k - 1] if k > i else 0.0
                right_cost = dp[k + 1][j] if k < j else 0.0
                cost = left_cost + right_cost + (prefix_sum[j + 1] - prefix_sum[i])
                
                if cost < min_cost:
                    min_cost = cost
                    best_root = k
            
            dp[i][j] = min_cost
            root[i][j] = best_root
    
    return dp[0][n - 1], root


def reconstruct_tree(root_table: List[List[Optional[int]]], keys: List[int], i: int, j: int) -> Optional[dict]:
    """
    從 root table 重建 BST 結構
    
    Args:
        root_table: DP 過程中記錄的根節點表
        keys: 鍵值列表
        i, j: 當前子樹的範圍
        
    Returns:
        樹的字典表示，如 {"key": 10, "left": {...}, "right": {...}}
    """
    if i > j:
        return None
    
    root_idx = root_table[i][j]
    if root_idx is None:
        return None
    
    return {
        "key": keys[root_idx],
        "left": reconstruct_tree(root_table, keys, i, root_idx - 1),
        "right": reconstruct_tree(root_table, keys, root_idx + 1, j)
    }


def print_tree(tree: Optional[dict], prefix: str = "", is_left: bool = False):
    """列印樹結構（文字形式）"""
    if tree is None:
        return
    
    if tree["right"]:
        print_tree(tree["right"], prefix + ("│   " if is_left else "    "), False)
    
    print(prefix + ("└── " if is_left else "┌── ") + str(tree["key"]))
    
    if tree["left"]:
        print_tree(tree["left"], prefix + ("    " if is_left else "│   "), True)


def print_dp_table(dp: List[List[float]], keys: List[int]):
    """列印 DP 表"""
    n = len(keys)
    print("\nDP 表（最小期望成本）:")
    print("    ", end="")
    for j in range(n):
        print(f"{keys[j]:6d} ", end="")
    print()
    
    for i in range(n):
        print(f"{keys[i]:2d}: ", end="")
        for j in range(n):
            if j < i:
                print("   -   ", end="")
            else:
                print(f"{dp[i][j]:6.2f} ", end="")
        print()


def demo_basic():
    """基本示範"""
    print("=" * 60)
    print("最優二叉搜尋樹 - 基本示範")
    print("=" * 60)
    
    # 範例：鍵值和頻率
    keys = [10, 20, 30, 40, 50]
    freq = [4, 2, 6, 3, 1]  # 搜尋頻率
    
    print(f"\n鍵值: {keys}")
    print(f"頻率: {freq}")
    print(f"總頻率: {sum(freq)}")
    
    # 計算最優 BST
    min_cost, root_table = optimal_bst_dp(keys, freq)
    print(f"\n最小期望搜尋成本: {min_cost:.2f}")
    
    # 重建樹結構
    tree = reconstruct_tree(root_table, keys, 0, len(keys) - 1)
    print("\n最優 BST 結構:")
    print_tree(tree)
    
    # 顯示 DP 表
    print_dp_table([[root_table[i][j] if i <= j else 0 for j in range(len(keys))] for i in range(len(keys))], keys)


def demo_comparison():
    """比較普通 DP 和 Knuth 優化"""
    print("\n" + "=" * 60)
    print("普通 DP vs Knuth 優化")
    print("=" * 60)
    
    import time
    
    # 測試不同大小的輸入
    test_cases = [
        (list(range(10, 110, 10)), [float(i) for i in range(10, 0, -1)] * 10),
        (list(range(10, 210, 10)), [float(i) for i in range(20, 0, -1)] * 10),
    ]
    
    for keys, freq in test_cases[:1]:  # 只測試一個，避免太慢
        keys = keys[:10]
        freq = freq[:10]
        print(f"\n鍵值數量: {len(keys)}")
        
        # 普通 DP
        start = time.perf_counter()
        cost1, _ = optimal_bst_dp(keys, freq)
        time1 = time.perf_counter() - start
        print(f"普通 DP: 成本 = {cost1:.2f}, 時間 = {time1 * 1000:.3f} ms")
        
        # Knuth 優化
        start = time.perf_counter()
        cost2, _ = optimal_bst_knuth(keys, freq)
        time2 = time.perf_counter() - start
        print(f"Knuth 優化: 成本 = {cost2:.2f}, 時間 = {time2 * 1000:.3f} ms")
        print(f"加速比: {time1/time2:.2f}x")


def demo_different_freqs():
    """不同頻率分佈的示範"""
    print("\n" + "=" * 60)
    print("不同頻率分佈對最優 BST 的影響")
    print("=" * 60)
    
    keys = [10, 20, 30, 40, 50]
    
    test_cases = [
        ("均勻分佈", [2, 2, 2, 2, 2]),
        ("遞增頻率", [1, 2, 3, 4, 5]),
        ("遞減頻率", [5, 4, 3, 2, 1]),
        ("中間高頻", [1, 2, 5, 2, 1]),
    ]
    
    for name, freq in test_cases:
        print(f"\n{name}:")
        print(f"  頻率: {freq}")
        min_cost, root_table = optimal_bst_dp(keys, freq)
        print(f"  最小期望成本: {min_cost:.2f}")
        
        tree = reconstruct_tree(root_table, keys, 0, len(keys) - 1)
        print("  樹根:", tree["key"] if tree else "None")


if __name__ == "__main__":
    demo_basic()
    demo_different_freqs()
    demo_comparison()
