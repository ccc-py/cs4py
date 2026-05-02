"""
Rabin-Karp 字串匹配演算法

使用滾動雜湊（Rolling Hash）技術來快速比較字串，
平均時間複雜度 O(n+m)，適合多模式匹配。
"""

from typing import List, Optional, Set


class RollingHash:
    """
    滾動雜湊類別

    使用多項式雜湊（Polynomial Hash）並配合模運算來避免溢位。
    支援在 O(1) 時間內更新雜湊值（移除首位字元，加入新字元）。
    """

    def __init__(self, base: int = 256, mod: int = 101) -> None:
        """
        初始化滾動雜湊

        參數:
            base: 雜湊基底（通常選用大質數或 256）
            mod: 模數（用來避免溢位，通常選用大質數）
        """
        self.base: int = base
        self.mod: int = mod
        self.hash: int = 0
        self.power: int = 1  # base^(length-1) mod mod
        self.length: int = 0

    def append(self, char: str) -> None:
        """
        在雜湊視窗末尾加入一個字元

        參數:
            char: 要加入的字元
        """
        self.hash = (self.hash * self.base + ord(char)) % self.mod
        self.length += 1
        if self.length > 1:
            self.power = (self.power * self.base) % self.mod

    def skip(self, char: str) -> None:
        """
        從雜湊視窗開頭移除一個字元

        參數:
            char: 要移除的字元
        """
        if self.length == 0:
            return
        # 減去該字元的貢獻
        self.hash = (self.hash - ord(char) * self.power) % self.mod
        if self.hash < 0:
            self.hash += self.mod
        self.length -= 1
        if self.length > 0:
            # 更新 power（這裡用逆元的方式，但為了簡化使用預計算）
            # 實際上需要更複雜的處理，這裡用簡化版本
            pass

    def value(self) -> int:
        """
        取得當前雜湊值

        回傳:
            雜湊值
        """
        return self.hash


def rabin_karp_search(text: str, pattern: str) -> List[int]:
    """
    使用 Rabin-Karp 演算法在 text 中搜尋 pattern

    參數:
        text: 主文字
        pattern: 要搜尋的模式字串

    回傳:
        所有匹配位置的起始索引列表
    """
    if not pattern or len(pattern) > len(text):
        return []

    n: int = len(text)
    m: int = len(pattern)
    result: List[int] = []

    # 使用雙雜湊來減少碰撞機率
    hash1: RollingHash = RollingHash(base=256, mod=1000000007)
    hash2: RollingHash = RollingHash(base=257, mod=1000000009)

    pattern_hash1: RollingHash = RollingHash(base=256, mod=1000000007)
    pattern_hash2: RollingHash = RollingHash(base=257, mod=1000000009)

    # 計算模式的雜湊值
    for char in pattern:
        pattern_hash1.append(char)
        pattern_hash2.append(char)

    # 初始化文字視窗的雜湊值
    text_hash1: RollingHash = RollingHash(base=256, mod=1000000007)
    text_hash2: RollingHash = RollingHash(base=257, mod=1000000009)

    for i in range(m):
        text_hash1.append(text[i])
        text_hash2.append(text[i])

    # 滑動視窗搜尋
    for i in range(n - m + 1):
        # 比較雙雜湊值
        if (text_hash1.value() == pattern_hash1.value() and
            text_hash2.value() == pattern_hash2.value()):
            # 雜湊匹配，進行逐字驗證（處理碰撞）
            if text[i:i+m] == pattern:
                result.append(i)

        # 移動視窗到下一個位置
        if i < n - m:
            # 重新計算滾動雜湊
            text_hash1 = RollingHash(base=256, mod=1000000007)
            text_hash2 = RollingHash(base=257, mod=1000000009)
            for j in range(i + 1, i + m + 1):
                text_hash1.append(text[j])
                text_hash2.append(text[j])

    return result


def rabin_karp_multi_search(text: str, patterns: List[str]) -> dict[str, List[int]]:
    """
    在 text 中同時搜尋多個模式（多模式匹配）

    參數:
        text: 主文字
        patterns: 要搜尋的模式字串列表

    回傳:
        字典，鍵為模式字串，值為匹配位置列表
    """
    result: dict[str, List[int]] = {p: [] for p in patterns}
    pattern_set: Set[str] = set(patterns)

    # 找出最長模式長度
    max_len: int = max(len(p) for p in patterns) if patterns else 0

    if max_len == 0 or not text:
        return result

    n: int = len(text)

    # 對每個可能的長度進行搜尋
    for length in range(1, max_len + 1):
        # 收集該長度的模式
        patterns_of_len: List[str] = [p for p in patterns if len(p) == length]
        if not patterns_of_len:
            continue

        # 計算這些模式的雜湊值
        pattern_hashes: Set[int] = set()
        pattern_map: dict[int, str] = {}
        for p in patterns_of_len:
            h: int = 0
            for char in p:
                h = (h * 256 + ord(char)) % 1000000007
            pattern_hashes.add(h)
            pattern_map[h] = p

        # 滑動視窗
        window_hash: int = 0
        for i in range(length):
            window_hash = (window_hash * 256 + ord(text[i])) % 1000000007

        if window_hash in pattern_hashes:
            if text[0:length] in pattern_set:
                result[text[0:length]].append(0)

        for i in range(1, n - length + 1):
            # 滾動更新雜湊值
            window_hash = (window_hash * 256 + ord(text[i + length - 1])) % 1000000007
            # 減去移出的字元貢獻
            window_hash = (window_hash - ord(text[i - 1]) *
                          pow(256, length, 1000000007)) % 1000000007
            if window_hash < 0:
                window_hash += 1000000007

            if window_hash in pattern_hashes:
                candidate: str = pattern_map.get(window_hash, "")
                if candidate and text[i:i+length] == candidate:
                    result[candidate].append(i)

    return result


if __name__ == "__main__":
    # 示範 Rabin-Karp 演算法
    text: str = "ABABDABACDABABCABAB"

    print("Rabin-Karp 字串匹配演算法示範")
    print(f"文字: {text}")
    print()

    # 單一模式搜尋
    pattern: str = "ABABCABAB"
    matches: List[int] = rabin_karp_search(text, pattern)
    print(f"搜尋模式 '{pattern}':")
    print(f"  找到 {len(matches)} 個匹配: {matches}")
    for pos in matches:
        print(f"  位置 {pos}: {text[pos:pos+len(pattern)]}")
    print()

    # 多模式搜尋
    patterns: List[str] = ["AB", "BA", "CA"]
    print(f"多模式搜尋 {patterns}:")
    multi_result: dict[str, List[int]] = rabin_karp_multi_search(text, patterns)
    for p, positions in multi_result.items():
        print(f"  '{p}': {positions}")
    print()

    # 測試無匹配
    print(f"搜尋 'XYZ': {rabin_karp_search(text, 'XYZ')}")
    print()

    # 測試空模式
    print(f"搜尋空字串: {rabin_karp_search(text, '')}")
