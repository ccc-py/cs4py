"""
後綴樹 (Suffix Tree - 簡化版)

歷史背景：
- 後綴樹由 Weiner 於 1973 年提出
- Ukkonen 於 1995 年提出線性時間建構演算法
- 後綴樹是字串處理的強大工具
- 簡化版使用 Trie 的概念，便於理解

應用場景：
- 字串匹配（找子字串）
- 最長重複子字串
- 最長公共子字串
- DNA 序列分析
"""

from typing import Dict, List, Optional, Tuple


class SuffixTrieNode:
    """後綴 Trie 節點（簡化版後綴樹）"""

    def __init__(self):
        self.children: Dict[str, 'SuffixTrieNode'] = {}
        self.is_end: bool = False  # 標記後綴起點


class SuffixTrie:
    """後綴 Trie（簡化版後綴樹，便於理解）"""

    def __init__(self, text: str):
        """
        初始化並建構後綴 Trie

        Args:
            text: 輸入字串
        """
        self.text = text
        self.root = SuffixTrieNode()

    def build(self) -> None:
        """
        建構後綴 Trie

        原理：
        1. 對每個後綴 text[i:]，從根開始插入
        2. 沿著 Trie 走，若無對應邊則創建

        時間複雜度：O(n²)（簡化版）
        空間複雜度：O(n²)

        若使用 Ukkonen 演算法可達 O(n)
        """
        n = len(self.text)
        for i in range(n):
            self._insert_suffix(i)

    def _insert_suffix(self, start: int) -> None:
        """插入從 start 開始的後綴"""
        node = self.root
        for i in range(start, len(self.text)):
            ch = self.text[i]
            if ch not in node.children:
                node.children[ch] = SuffixTrieNode()
            node = node.children[ch]
        node.is_end = True

    def search(self, pattern: str) -> bool:
        """
        搜尋模式字串

        Args:
            pattern: 要搜尋的模式

        Returns:
            是否找到該模式
        """
        node = self.root
        for ch in pattern:
            if ch not in node.children:
                return False
            node = node.children[ch]
        return True

    def find_longest_repeated(self) -> str:
        """
        找最長重複子字串

        原理：
        1. 遍歷 Trie，找最深的內部節點（有多個分支）
        2. 從根到該節點的路徑即為重複子字串

        時間複雜度：O(n²)
        空間複雜度：O(n²)

        Returns:
            最長重複子字串
        """
        state = {"max_len": 0, "result": ""}
        self._dfs_longest(self.root, "", state)
        return state["result"]

    def _dfs_longest(self, node: SuffixTrieNode, current: str,
                     state: dict) -> None:
        """DFS 找最長重複子字串"""
        # 若有多個子節點或是後綴起點，更新結果
        if len(node.children) > 1 or node.is_end:
            if len(current) > state["max_len"]:
                state["max_len"] = len(current)
                state["result"] = current

        for ch, child in node.children.items():
            self._dfs_longest(child, current + ch, state)


def build_sample_trie() -> SuffixTrie:
    """建立示例後綴 Trie"""
    trie = SuffixTrie("banana")
    trie.build()
    return trie


if __name__ == "__main__":
    print("=== 後綴樹/後綴 Trie (Suffix Tree/Trie) 測試 ===\n")

    # 測試 1：基本搜尋
    print("1. 基本搜尋（文字：banana）：")
    trie1 = build_sample_trie()
    patterns = ["ana", "ban", "nana", "xyz", "a", ""]
    for p in patterns:
        found = trie1.search(p)
        print(f"  搜尋 '{p}'：{found}")
    print()

    # 測試 2：最長重複子字串
    print("2. 最長重複子字串：")
    test_strings = ["banana", "abcdefab", "mississippi", "aaaa"]
    for s in test_strings:
        trie = SuffixTrie(s)
        trie.build()
        longest = trie.find_longest_repeated()
        print(f"  字串 '{s}'：最長重複子字串 = '{longest}'")
    print()

    # 測試 3：空字串
    print("3. 空字串：")
    trie3 = SuffixTrie("")
    trie3.build()
    print(f"  搜尋 'a'：{trie3.search('a')}")
    print(f"  最長重複：'{trie3.find_longest_repeated()}'")
    print()

    # 測試 4：單一字元重複
    print("4. 單一字元重複（aaaaaa）：")
    trie4 = SuffixTrie("aaaaaa")
    trie4.build()
    longest = trie4.find_longest_repeated()
    print(f"  最長重複子字串：'{longest}'")
    print()

    # 測試 5：無重複子字串
    print("5. 無重複子字串（abcde）：")
    trie5 = SuffixTrie("abcde")
    trie5.build()
    longest = trie5.find_longest_repeated()
    print(f"  最長重複子字串：'{longest}'（空表示無重複）")
    print()
    print("測試完成！")
