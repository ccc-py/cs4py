"""
Trie（前綴樹 / 字典樹）資料結構

支援插入、搜尋、前綴匹配，以及單字頻率統計。
"""

from typing import Dict, Optional, List


class TrieNode:
    """
    Trie 的節點類別

    每個節點包含一個子節點字典和一個標記（是否為單字結尾），
    以及該單字的出現次數。
    """

    def __init__(self) -> None:
        """初始化一個 Trie 節點"""
        self.children: Dict[str, 'TrieNode'] = {}
        self.is_end_of_word: bool = False
        self.frequency: int = 0  # 該單字出現的次數


class Trie:
    """
    Trie（前綴樹）資料結構

    用於高效儲存和搜尋字串集合，特別適合前綴相關操作。
    """

    def __init__(self) -> None:
        """初始化一個空的 Trie"""
        self.root: TrieNode = TrieNode()

    def insert(self, word: str) -> None:
        """
        插入一個單字到 Trie 中

        如果單字已存在，則增加其頻率計數。

        參數:
            word: 要插入的單字
        """
        node: TrieNode = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end_of_word = True
        node.frequency += 1

    def search(self, word: str) -> bool:
        """
        搜尋單字是否存在於 Trie 中

        參數:
            word: 要搜尋的單字

        回傳:
            如果單字存在則回傳 True，否則回傳 False
        """
        node: Optional[TrieNode] = self._find_node(word)
        return node is not None and node.is_end_of_word

    def get_frequency(self, word: str) -> int:
        """
        取得單字在 Trie 中的出現次數

        參數:
            word: 要查詢的單字

        回傳:
            單字的出現次數，不存在則回傳 0
        """
        node: Optional[TrieNode] = self._find_node(word)
        if node is not None and node.is_end_of_word:
            return node.frequency
        return 0

    def starts_with(self, prefix: str) -> bool:
        """
        檢查是否有以給定前綴開頭的單字

        參數:
            prefix: 要檢查的前綴

        回傳:
            如果存在以該前綴開頭的單字則回傳 True
        """
        return self._find_node(prefix) is not None

    def get_words_with_prefix(self, prefix: str) -> List[str]:
        """
        取得所有以給定前綴開頭的單字

        參數:
            prefix: 前綴字串

        回傳:
            所有符合前綴的單字列表
        """
        node: Optional[TrieNode] = self._find_node(prefix)
        if node is None:
            return []
        result: List[str] = []
        self._collect_words(node, prefix, result)
        return result

    def _find_node(self, prefix: str) -> Optional[TrieNode]:
        """
        根據前綴找到對應的節點

        參數:
            prefix: 前綴字串

        回傳:
            對應的 TrieNode，如果不存在則回傳 None
        """
        node: TrieNode = self.root
        for char in prefix:
            if char not in node.children:
                return None
            node = node.children[char]
        return node

    def _collect_words(self, node: TrieNode, prefix: str, result: List[str]) -> None:
        """
        遞迴收集從當前節點開始的所有單字

        參數:
            node: 當前節點
            prefix: 當前累積的前綴
            result: 用於儲存結果的列表
        """
        if node.is_end_of_word:
            # 加入重複次數
            for _ in range(node.frequency):
                result.append(prefix)
        for char, child in node.children.items():
            self._collect_words(child, prefix + char, result)

    def delete(self, word: str) -> bool:
        """
        從 Trie 中刪除一個單字

        參數:
            word: 要刪除的單字

        回傳:
            如果成功刪除則回傳 True，否則回傳 False
        """
        if not self.search(word):
            return False

        node: TrieNode = self.root
        path: List[Tuple[TrieNode, str]] = []  # 記錄路徑

        for char in word:
            path.append((node, char))
            node = node.children[char]

        # 減少頻率或標記為非單字結尾
        node.frequency -= 1
        if node.frequency == 0:
            node.is_end_of_word = False

        # 如果該節點還有其他用途，不需要清理
        if node.children or node.is_end_of_word:
            return True

        # 從葉節點向上清理無用的節點
        for parent, char in reversed(path):
            if not parent.children[char].children and not parent.children[char].is_end_of_word:
                del parent.children[char]
            else:
                break

        return True


# 為了讓 delete 方法中的 Tuple 型別提示能工作
from typing import Tuple


if __name__ == "__main__":
    # 示範 Trie 的使用
    trie: Trie = Trie()

    # 插入單字
    words: List[str] = ["apple", "app", "application", "apt", "banana", "band"]
    print("插入單字:", words)
    for word in words:
        trie.insert(word)
    print()

    # 搜尋單字
    test_words: List[str] = ["app", "apple", "appl", "banana", "band", "cat"]
    print("搜尋測試:")
    for word in test_words:
        found: bool = trie.search(word)
        freq: int = trie.get_frequency(word) if found else 0
        print(f"  '{word}': {'找到' if found else '未找到'} (頻率: {freq})")
    print()

    # 前綴匹配
    prefixes: List[str] = ["app", "ban", "cat"]
    print("前綴匹配測試:")
    for prefix in prefixes:
        has_prefix: bool = trie.starts_with(prefix)
        if has_prefix:
            matched: List[str] = trie.get_words_with_prefix(prefix)
            print(f"  '{prefix}': 找到 {len(matched)} 個單字: {matched}")
        else:
            print(f"  '{prefix}': 無匹配")
    print()

    # 頻率測試
    print("頻率測試:")
    trie.insert("apple")
    trie.insert("apple")
    print(f"  'apple' 出現次數: {trie.get_frequency('apple')}")
    print()

    # 刪除測試
    print("刪除測試:")
    print(f"  刪除 'apple': {trie.delete('apple')}")
    print(f"  'apple' 剩餘頻率: {trie.get_frequency('apple')}")
    print(f"  刪除 'cat': {trie.delete('cat')}")
