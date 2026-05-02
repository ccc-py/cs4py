"""
硬幣找零問題 (Coin Change Problem)

歷史背景：
- 硬幣找零是經典的動態規劃問題，屬於無界背包（Unbounded Knapsack）的特例
- 與 0-1 背包不同，每種硬幣可以使用無限次
- 應用於貨幣系統分析、資源分配、付款優化等領域

問題定義：
1. 最小硬幣數：給定不同面額的硬幣和目標金額，找出湊成金額所需的最少硬幣數
2. 組合數：有多少種方式可以湊成目標金額
"""

from typing import List, Tuple, Optional


def min_coins(coins: List[int], amount: int) -> int:
    """
    找出湊成目標金額所需的最少硬幣數

    原理：
    dp[x] = 湊成金額 x 所需的最少硬幣數
    dp[0] = 0（金額 0 不需要硬幣）
    對於每個金額 x，嘗試每種硬幣：
    dp[x] = min(dp[x - coin] + 1 for coin in coins if coin <= x)

    時間複雜度：O(amount * len(coins))
    空間複雜度：O(amount)

    Args:
        coins: 硬幣面額列表
        amount: 目標金額

    Returns:
        最少硬幣數，無法湊成則返回 -1
    """
    dp = [float('inf')] * (amount + 1)
    dp[0] = 0

    for x in range(1, amount + 1):
        for coin in coins:
            if coin <= x:
                dp[x] = min(dp[x], dp[x - coin] + 1)

    return dp[amount] if dp[amount] != float('inf') else -1


def min_coins_with_reconstruction(coins: List[int], amount: int) -> Tuple[int, List[int]]:
    """
    找出最少硬幣數並重建使用的硬幣

    Returns:
        (最少硬幣數, 硬幣列表)，無法湊成則返回 (-1, [])
    """
    dp = [float('inf')] * (amount + 1)
    dp[0] = 0
    used_coin = [-1] * (amount + 1)  # 記錄湊成 x 時使用的硬幣

    for x in range(1, amount + 1):
        for coin in coins:
            if coin <= x and dp[x - coin] + 1 < dp[x]:
                dp[x] = dp[x - coin] + 1
                used_coin[x] = coin

    if dp[amount] == float('inf'):
        return -1, []

    # 重建硬幣序列
    result = []
    x = amount
    while x > 0:
        coin = used_coin[x]
        result.append(coin)
        x -= coin

    return dp[amount], result


def count_ways(coins: List[int], amount: int) -> int:
    """
    計算湊成目標金額的方式數（組合數）

    原理：
    dp[x] = 湊成金額 x 的方式數
    dp[0] = 1（金額 0 只有一種方式：不使用任何硬幣）

    注意：這裡 coins 的順序不影響結果（組合而非排列）

    時間複雜度：O(amount * len(coins))
    空間複雜度：O(amount)

    Args:
        coins: 硬幣面額列表
        amount: 目標金額

    Returns:
        方式數（可能很大，使用 int）
    """
    dp = [0] * (amount + 1)
    dp[0] = 1

    for coin in coins:
        for x in range(coin, amount + 1):
            dp[x] += dp[x - coin]

    return dp[amount]


def count_ways_with_coins(coins: List[int], amount: int) -> Tuple[int, List[List[int]]]:
    """
    計算方式數並返回所有組合（僅適合小金額）

    注意：當金額較大時，組合數可能非常多，不建議使用此函數
    """
    # 這裡只返回方式數，不枚舉所有組合（避免爆炸）
    return count_ways(coins, amount), []


if __name__ == "__main__":
    print("=== 硬幣找零問題 (Coin Change) 測試 ===\n")

    # 測試 1：最小硬幣數
    print("1. 最小硬幣數：")
    test_cases = [
        ([1, 2, 5], 11),
        ([2], 3),
        ([1, 2, 5], 0),
        ([1, 5, 10, 25], 30),
    ]

    for coins, amount in test_cases:
        min_c, used = min_coins_with_reconstruction(coins, amount)
        if min_c == -1:
            print(f"  硬幣 {coins} 湊 {amount}：無法湊成")
        else:
            print(f"  硬幣 {coins} 湊 {amount}：最少 {min_c} 枚，使用 {used}")
    print()

    # 測試 2：組合數
    print("2. 組合數計算：")
    coins = [1, 2, 5]
    for amount in [0, 1, 2, 3, 4, 5, 10]:
        ways = count_ways(coins, amount)
        print(f"  硬幣 {coins} 湊 {amount}：{ways} 種方式")
    print()

    # 測試 3：無法湊成的情況
    print("3. 無法湊成的情況：")
    coins = [2, 5]
    amounts = [1, 3, 7]
    for amount in amounts:
        result = min_coins(coins, amount)
        print(f"  硬幣 {coins} 湊 {amount}：{result}")
    print()

    # 測試 4：重建硬幣使用
    print("4. 重建硬幣使用：")
    coins = [1, 5, 10, 25]
    amount = 67
    min_c, used = min_coins_with_reconstruction(coins, amount)
    print(f"  硬幣 {coins} 湊 {amount}")
    print(f"  最少硬幣數：{min_c}")
    print(f"  使用硬幣：{used}")
    print(f"  驗證：總和 = {sum(used)}")
    print()

    # 測試 5：大金額測試
    print("5. 較大金額測試：")
    coins = [1, 5, 10, 25]
    amount = 100
    min_c = min_coins(coins, amount)
    ways = count_ways(coins, amount)
    print(f"  硬幣 {coins} 湊 {amount}")
    print(f"  最少硬幣數：{min_c}")
    print(f"  組合數：{ways}")
