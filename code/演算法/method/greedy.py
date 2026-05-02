"""
貪婪演算法 (Greedy Algorithms)
實作經典的貪婪演算法：活動選擇、分數背包、霍夫曼編碼
"""

from typing import List, Tuple, Dict, Optional
import heapq


def activity_selection(start: List[int], finish: List[int]) -> List[int]:
    """
    活動選擇問題 - 選出最多的相容活動
    
    Args:
        start: 每個活動的開始時間列表
        finish: 每個活動的結束時間列表
        
    Returns:
        被選中活動的索引列表
    """
    n = len(start)
    # 建立活動列表並按結束時間排序
    activities = list(range(n))
    activities.sort(key=lambda i: finish[i])
    
    selected = []
    last_finish = -1
    
    for i in activities:
        if start[i] >= last_finish:
            selected.append(i)
            last_finish = finish[i]
    
    # 按原始順序排序返回
    selected.sort()
    return selected


def activity_selection_verbose(start: List[int], finish: List[int]) -> None:
    """印出活動選擇的詳細過程"""
    n = len(start)
    activities = list(range(n))
    activities.sort(key=lambda i: finish[i])
    
    print("按結束時間排序後的活動：")
    for i in activities:
        print(f"  活動 {i}: [{start[i]}, {finish[i]})")
    
    selected = []
    last_finish = -1
    
    print("\n選擇過程：")
    for i in activities:
        if start[i] >= last_finish:
            selected.append(i)
            print(f"  選擇活動 {i}: [{start[i]}, {finish[i]})")
            last_finish = finish[i]
        else:
            print(f"  跳過活動 {i}: [{start[i]}, {finish[i]}) - 與已選活動衝突")
    
    print(f"\n共選擇 {len(selected)} 個活動: {sorted(selected)}")


def fractional_knapsack(weights: List[float], values: List[float], capacity: float) -> Tuple[float, List[Tuple[int, float]]]:
    """
    分數背包問題 - 物品可以分割
    
    Args:
        weights: 物品重量列表
        values: 物品價值列表
        capacity: 背包容量
        
    Returns:
        (最大總價值, [(物品索引, 選取分數)] 列表)
    """
    n = len(weights)
    # 計算價值密度（價值/重量）
    items = list(range(n))
    items.sort(key=lambda i: values[i] / weights[i], reverse=True)
    
    total_value = 0.0
    selections = []
    remaining = capacity
    
    for i in items:
        if remaining >= weights[i]:
            # 全部拿取
            total_value += values[i]
            selections.append((i, 1.0))
            remaining -= weights[i]
        else:
            # 部分拿取
            fraction = remaining / weights[i]
            total_value += values[i] * fraction
            selections.append((i, fraction))
            break
    
    return total_value, selections


def huffman_encode(text: str) -> Tuple[Dict[str, str], Dict[str, str], 'HuffmanNode']:
    """
    霍夫曼編碼 - 建立最佳前綴編碼
    
    Args:
        text: 要編碼的文字
        
    Returns:
        (編碼表, 解碼表, 霍夫曼樹根節點)
    """
    if not text:
        return {}, {}, None
    
    # 統計字元頻率
    freq = {}
    for ch in text:
        freq[ch] = freq.get(ch, 0) + 1
    
    # 建立霍夫曼樹
    class HuffmanNode:
        def __init__(self, char: Optional[str] = None, freq: int = 0):
            self.char = char
            self.freq = freq
            self.left = None
            self.right = None
        
        def __lt__(self, other):
            return self.freq < other.freq
    
    # 使用最小堆建立樹
    heap = []
    for char, f in freq.items():
        node = HuffmanNode(char, f)
        heapq.heappush(heap, node)
    
    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)
        
        merged = HuffmanNode(freq=left.freq + right.freq)
        merged.left = left
        merged.right = right
        heapq.heappush(heap, merged)
    
    root = heap[0] if heap else None
    
    # 建立編碼表
    def build_codes(node: Optional[HuffmanNode], prefix: str = "", codes: Dict = {}):
        if node is None:
            return
        
        if node.char is not None:
            codes[node.char] = prefix or "0"  # 單一字元特殊处理
            return
        
        build_codes(node.left, prefix + "0", codes)
        build_codes(node.right, prefix + "1", codes)
    
    codes = {}
    build_codes(root)
    
    # 建立解碼表
    decode_table = {v: k for k, v in codes.items()}
    
    return codes, decode_table, root


def huffman_decode(encoded: str, decode_table: Dict[str, str]) -> str:
    """
    霍夫曼解碼
    
    Args:
        encoded: 編碼後的位元字串
        decode_table: 解碼表
        
    Returns:
        解碼後的文字
    """
    result = []
    current = ""
    
    for bit in encoded:
        current += bit
        if current in decode_table:
            result.append(decode_table[current])
            current = ""
    
    return ''.join(result)


if __name__ == "__main__":
    # 測試活動選擇問題
    print("=== 活動選擇問題 ===")
    start = [1, 3, 0, 5, 8, 5]
    finish = [2, 4, 6, 7, 9, 9]
    print(f"活動開始時間: {start}")
    print(f"活動結束時間: {finish}")
    selected = activity_selection(start, finish)
    print(f"選中的活動索引: {selected}")
    print()
    activity_selection_verbose(start, finish)
    
    # 測試分數背包問題
    print("\n=== 分數背包問題 ===")
    weights = [10, 20, 30]
    values = [60, 100, 120]
    capacity = 50
    
    total_value, selections = fractional_knapsack(weights, values, capacity)
    print(f"物品重量: {weights}")
    print(f"物品價值: {values}")
    print(f"背包容量: {capacity}")
    print(f"最大總價值: {total_value}")
    print("選取情況:")
    for idx, fraction in selections:
        print(f"  物品 {idx}: 拿取 {fraction*100:.0f}% (重量 {weights[idx]}, 價值 {values[idx]})")
    
    # 測試霍夫曼編碼
    print("\n=== 霍夫曼編碼 ===")
    text = "this is an example for huffman encoding"
    print(f"原始文字: {text}")
    
    codes, decode_table, root = huffman_encode(text)
    print(f"編碼表: {codes}")
    
    # 編碼
    encoded = ''.join(codes[ch] for ch in text)
    print(f"編碼結果: {encoded[:50]}...")
    print(f"原始長度: {len(text) * 8} bits")
    print(f"編碼長度: {len(encoded)} bits")
    
    # 解碼
    decoded = huffman_decode(encoded, decode_table)
    print(f"解碼結果: {decoded}")
    print(f"解碼正確: {decoded == text}")
