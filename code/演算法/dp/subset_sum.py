"""
子集和問題 (Subset Sum Problem)

包含：
1. 決策版本 - 是否存在子集和等於目標值
2. 重構版本 - 找出一個滿足條件的子集
3. 使用布林 DP 表
4. 回溯法找出實際子集
"""

from typing import List, Optional, Tuple


def subset_sum_decision(nums: List[int], target: int) -> bool:
    """
    子集和問題 - 決策版本
    
    判斷是否存在一個子集，其元素和等於目標值。
    使用動態規劃，時間複雜度 O(n * target)。
    
    Args:
        nums: 整數列表
        target: 目標和
        
    Returns:
        True 如果存在滿足條件的子集，否則 False
    """
    if target < 0:
        return False
    if target == 0:
        return True  # 空子集
    
    n = len(nums)
    # dp[i][j] 表示使用前 i 個元素是否可以組成和 j
    # 使用滾動陣列優化空間
    dp = [False] * (target + 1)
    dp[0] = True  # 空子集可以組成和 0
    
    for num in nums:
        # 從後往前更新，避免重複使用同一個元素
        for j in range(target, num - 1, -1):
            if dp[j - num]:
                dp[j] = True
    
    return dp[target]


def subset_sum_reconstruct(nums: List[int], target: int) -> Optional[List[int]]:
    """
    子集和問題 - 重構版本
    
    找出一個子集，其元素和等於目標值。
    使用 DP 表並回溯找出實際的子集。
    
    時間複雜度：O(n * target)
    空間複雜度：O(n * target)
    
    Args:
        nums: 整數列表
        target: 目標和
        
    Returns:
        一個滿足條件的子集，如果不存在則返回 None
    """
    if target < 0:
        return None
    if target == 0:
        return []  # 空子集
    
    n = len(nums)
    
    # dp[i][j] 表示使用前 i 個元素是否可以組成和 j
    dp = [[False] * (target + 1) for _ in range(n + 1)]
    dp[0][0] = True
    
    # 填充 DP 表
    for i in range(1, n + 1):
        num = nums[i - 1]
        for j in range(target + 1):
            # 不使用第 i 個元素
            dp[i][j] = dp[i - 1][j]
            # 使用第 i 個元素（如果可能的話）
            if j >= num and dp[i - 1][j - num]:
                dp[i][j] = True
    
    # 如果不存在滿足條件的子集
    if not dp[n][target]:
        return None
    
    # 回溯找出子集
    subset = []
    i, j = n, target
    while i > 0 and j > 0:
        num = nums[i - 1]
        # 檢查是否使用了第 i 個元素
        if j >= num and dp[i - 1][j - num]:
            subset.append(num)
            j -= num
        i -= 1
    
    return subset[::-1]  # 反轉得到原順序


def subset_sum_all(nums: List[int], target: int) -> List[List[int]]:
    """
    找出所有滿足條件的子集
    
    Args:
        nums: 整數列表
        target: 目標和
        
    Returns:
        所有滿足條件的子集列表
    """
    if target < 0:
        return []
    if target == 0:
        return [[]]
    
    n = len(nums)
    dp = [[False] * (target + 1) for _ in range(n + 1)]
    dp[0][0] = True
    
    # 填充 DP 表
    for i in range(1, n + 1):
        num = nums[i - 1]
        for j in range(target + 1):
            dp[i][j] = dp[i - 1][j]
            if j >= num and dp[i - 1][j - num]:
                dp[i][j] = True
    
    # 回溯找出所有子集
    def backtrack(i: int, j: int) -> List[List[int]]:
        if i == 0:
            return [[]] if j == 0 else []
        
        result = []
        num = nums[i - 1]
        
        # 不使用第 i 個元素
        if dp[i - 1][j]:
            result.extend(backtrack(i - 1, j))
        
        # 使用第 i 個元素
        if j >= num and dp[i - 1][j - num]:
            for subset in backtrack(i - 1, j - num):
                result.append(subset + [num])
        
        return result
    
    return backtrack(n, target)


def subset_sum_count(nums: List[int], target: int) -> int:
    """
    計算滿足條件的子集數量
    
    Args:
        nums: 整數列表
        target: 目標和
        
    Returns:
        滿足條件的子集數量
    """
    if target < 0:
        return 0
    
    dp = [0] * (target + 1)
    dp[0] = 1  # 空子集
    
    for num in nums:
        for j in range(target, num - 1, -1):
            dp[j] += dp[j - num]
    
    return dp[target]


def demo_basic():
    """基本示範"""
    print("=" * 60)
    print("子集和問題 - 基本示範")
    print("=" * 60)
    
    nums = [3, 34, 4, 12, 5, 2]
    
    # 決策版本
    print("\n1. 決策版本")
    print(f"數組: {nums}")
    
    test_cases = [9, 11, 25, 37]
    for target in test_cases:
        exists = subset_sum_decision(nums, target)
        print(f"  是否存在子集和為 {target}? {exists}")
    
    # 重構版本
    print("\n2. 重構版本（找出子集）")
    for target in [9, 11, 25]:
        subset = subset_sum_reconstruct(nums, target)
        if subset:
            print(f"  目標 {target}: 找到子集 {subset}，和 = {sum(subset)}")
        else:
            print(f"  目標 {target}: 不存在滿足條件的子集")
    
    # 顯示 DP 表
    print("\n3. DP 表視覺化（目標 = 9）")
    target = 9
    n = len(nums)
    dp = [[False] * (target + 1) for _ in range(n + 1)]
    dp[0][0] = True
    
    for i in range(1, n + 1):
        num = nums[i - 1]
        for j in range(target + 1):
            dp[i][j] = dp[i - 1][j]
            if j >= num and dp[i - 1][j - num]:
                dp[i][j] = True
    
    print("  DP 表（行表示元素，列表示和）:")
    print("  ", end="")
    for j in range(target + 1):
        print(f"{j:3d} ", end="")
    print()
    for i in range(n + 1):
        if i == 0:
            print("  ∅: ", end="")
        else:
            print(f"  {nums[i-1]:2d}: ", end="")
        for j in range(target + 1):
            print(" T " if dp[i][j] else " F ", end="")
        print()


def demo_all_subsets():
    """找出所有子集的示範"""
    print("\n" + "=" * 60)
    print("子集和問題 - 所有滿足條件的子集")
    print("=" * 60)
    
    nums = [1, 2, 3, 4, 5]
    target = 5
    
    print(f"\n數組: {nums}")
    print(f"目標: {target}")
    
    subsets = subset_sum_all(nums, target)
    print(f"所有和為 {target} 的子集:")
    for i, subset in enumerate(subsets, 1):
        print(f"  {i}. {subset} = {sum(subset)}")
    
    print(f"\n共有 {len(subsets)} 個子集")


def demo_count():
    """計數示範"""
    print("\n" + "=" * 60)
    print("子集和問題 - 子集數量")
    print("=" * 60)
    
    nums = [1, 2, 3, 4, 5]
    
    print(f"\n數組: {nums}")
    for target in range(0, 16):
        count = subset_sum_count(nums, target)
        if count > 0:
            print(f"  目標 {target:2d}: {count} 個子集")


if __name__ == "__main__":
    demo_basic()
    demo_all_subsets()
    demo_count()
