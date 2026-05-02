"""
MinHash

用於快速估計兩個集合的 Jaccard 相似度。
常用於文件相似度檢測、重複內容識別等場景。
"""

import hashlib
import random
from typing import Set, List, Any, Tuple, Optional


class MinHash:
    """
    MinHash 演算法
    
    使用多個雜湊函數的最小雜湊值來估計 Jaccard 相似度。
    Jaccard 相似度定義為 |A ∩ B| / |A ∪ B|。
    """
    
    def __init__(self, num_hashes: int = 128, seed: int = 42):
        """
        初始化 MinHash
        
        參數:
            num_hashes: 雜湊函數的數量 (越多越準確，但越慢)
            seed: 隨機種子，用於產生不同的雜湊函數
        """
        self.num_hashes = num_hashes
        self.seed = seed
        # 預先產生雜湊函數的參數 (a, b 用於線性變換)
        self.hash_params = self._generate_hash_functions(num_hashes, seed)
    
    @staticmethod
    def _generate_hash_functions(
        n: int, 
        seed: int
    ) -> List[Tuple[int, int]]:
        """
        產生 n 個不同的雜湊函數參數
        
        參數:
            n: 雜湊函數數量
            seed: 隨機種子
        
        返回:
            參數列表 [(a1, b1), (a2, b2), ...]
        """
        random.seed(seed)
        params = []
        for _ in range(n):
            a = random.randint(1, 2**32 - 1)
            b = random.randint(0, 2**32 - 1)
            params.append((a, b))
        return params
    
    def _hash_value(self, value: int, a: int, b: int, 
                   prime: int = 2**32 - 5) -> int:
        """
        使用線性變換計算雜湊值: h(x) = (a*x + b) mod prime
        
        參數:
            value: 要雜湊的值
            a, b: 雜湊函數參數
            prime: 大質數
        
        返回:
            雜湊值
        """
        return (a * value + b) % prime
    
    def compute_signature(self, items: Set[Any]) -> List[int]:
        """
        計算集合的 MinHash 簽章
        
        參數:
            items: 輸入集合
        
        返回:
            MinHash 簽章 (長度為 num_hashes 的列表)
        """
        # 將集合元素轉為整數
        int_items = set()
        for item in items:
            if isinstance(item, bytes):
                data = item
            elif isinstance(item, str):
                data = item.encode('utf-8')
            else:
                data = str(item).encode('utf-8')
            # 使用雜湊產生整數
            h = int(hashlib.md5(data).hexdigest()[:8], 16)
            int_items.add(h)
        
        # 計算每個雜湊函數的最小值
        signature = []
        for a, b in self.hash_params:
            min_hash = float('inf')
            for value in int_items:
                h = self._hash_value(value, a, b)
                if h < min_hash:
                    min_hash = h
            signature.append(min_hash)
        
        return signature
    
    @staticmethod
    def estimate_jaccard(
        sig1: List[int], 
        sig2: List[int]
    ) -> float:
        """
        使用 MinHash 簽章估計 Jaccard 相似度
        
        參數:
            sig1: 第一個簽章
            sig2: 第二個簽章
        
        返回:
            Jaccard 相似度的估計值
        """
        if len(sig1) != len(sig2):
            raise ValueError("簽章長度必須相同")
        
        # 計算相同雜湊值的比率
        matches = sum(1 for h1, h2 in zip(sig1, sig2) if h1 == h2)
        return matches / len(sig1)
    
    def jaccard_similarity(self, set1: Set[Any], set2: Set[Any]) -> float:
        """
        計算兩個集合的 Jaccard 相似度
        
        參數:
            set1: 第一個集合
            set2: 第二個集合
        
        返回:
            Jaccard 相似度的估計值
        """
        sig1 = self.compute_signature(set1)
        sig2 = self.compute_signature(set2)
        return self.estimate_jaccard(sig1, sig2)
    
    def exact_jaccard(self, set1: Set[Any], set2: Set[Any]) -> float:
        """
        計算精確的 Jaccard 相似度（用於比較）
        
        參數:
            set1: 第一個集合
            set2: 第二個集合
        
        返回:
            精確的 Jaccard 相似度
        """
        if not set1 and not set2:
            return 1.0
        intersection = len(set1 & set2)
        union = len(set1 | set2)
        return intersection / union if union > 0 else 1.0


class MinHashLSH:
    """
    使用 MinHash 和局部敏感雜湊 (LSH) 進行近似最近鄰搜尋
    """
    
    def __init__(self, num_hashes: int = 128, num_bands: int = 32, seed: int = 42):
        """
        初始化 MinHash LSH
        
        參數:
            num_hashes: MinHash 雜湊函數數量
            num_bands: LSH 的 band 數量
            seed: 隨機種子
        """
        if num_hashes % num_bands != 0:
            raise ValueError("num_hashes 必須能被 num_bands 整除")
        
        self.num_hashes = num_hashes
        self.num_bands = num_bands
        self.rows_per_band = num_hashes // num_bands
        self.minhash = MinHash(num_hashes, seed)
        self.bands = {}  # {band_index: {hash_value: [doc_ids]}}
    
    def _get_bands(self, signature: List[int]) -> List[Tuple[int, int]]:
        """
        將簽章分割成多個 band
        
        參數:
            signature: MinHash 簽章
        
        返回:
            [(band_index, hash_of_band), ...]
        """
        bands = []
        for i in range(self.num_bands):
            start = i * self.rows_per_band
            end = start + self.rows_per_band
            band_sig = tuple(signature[start:end])
            band_hash = hash(band_sig)
            bands.append((i, band_hash))
        return bands
    
    def add(self, doc_id: Any, items: Set[Any]) -> None:
        """
        加入一個文件
        
        參數:
            doc_id: 文件 ID
            items: 文件的詞集合
        """
        sig = self.minhash.compute_signature(items)
        bands = self._get_bands(sig)
        
        for band_idx, band_hash in bands:
            if band_idx not in self.bands:
                self.bands[band_idx] = {}
            if band_hash not in self.bands[band_idx]:
                self.bands[band_idx][band_hash] = []
            self.bands[band_idx][band_hash].append(doc_id)
    
    def query(self, items: Set[Any]) -> List[Any]:
        """
        查詢與給定集合相似的文件
        
        參數:
            items: 查詢集合
        
        返回:
            候選文件 ID 列表
        """
        sig = self.minhash.compute_signature(items)
        bands = self._get_bands(sig)
        
        candidates = set()
        for band_idx, band_hash in bands:
            if band_idx in self.bands and band_hash in self.bands[band_idx]:
                candidates.update(self.bands[band_idx][band_hash])
        
        return list(candidates)


if __name__ == "__main__":
    print("=== MinHash 測試 ===\n")
    
    # 測試 1: 基本功能
    print("1. 基本功能測試")
    mh = MinHash(num_hashes=128, seed=42)
    
    set1 = {"apple", "banana", "cherry", "date"}
    set2 = {"banana", "cherry", "date", "elderberry"}
    
    jaccard_est = mh.jaccard_similarity(set1, set2)
    jaccard_exact = mh.exact_jaccard(set1, set2)
    
    print(f"   集合 1: {set1}")
    print(f"   集合 2: {set2}")
    print(f"   精確 Jaccard: {jaccard_exact:.4f}")
    print(f"   MinHash 估計: {jaccard_est:.4f}")
    
    # 測試 2: 不同雜湊函數數量的影響
    print(f"\n2. 雜湊函數數量的影響")
    set3 = set(range(100))
    set4 = set(range(80, 180))  # 重疊 20 個元素
    
    exact = len(set3 & set4) / len(set3 | set4)
    print(f"   精確 Jaccard: {exact:.4f}")
    print(f"   {'雜湊數':>8} {'估計值':>10} {'誤差':>10}")
    for n in [16, 32, 64, 128, 256]:
        mh = MinHash(num_hashes=n, seed=42)
        est = mh.jaccard_similarity(set3, set4)
        error = abs(est - exact)
        print(f"   {n:>8} {est:>10.4f} {error:>10.4f}")
    
    # 測試 3: 完全相同和完全不同的集合
    print(f"\n3. 極端情況測試")
    set_full = {1, 2, 3, 4, 5}
    set_same = {1, 2, 3, 4, 5}
    set_disjoint = {6, 7, 8, 9, 10}
    
    mh = MinHash(num_hashes=128)
    print(f"   相同集合 Jaccard: {mh.jaccard_similarity(set_full, set_same):.4f}")
    print(f"   不相交集合 Jaccard: {mh.jaccard_similarity(set_full, set_disjoint):.4f}")
    
    # 測試 4: MinHash LSH
    print(f"\n4. MinHash LSH 測試")
    lsh = MinHashLSH(num_hashes=128, num_bands=32)
    
    # 加入一些文件
    docs = [
        {"這", "是", "一個", "測試", "文件"},
        {"這", "是", "另一個", "測試", "文件"},
        {"完全", "不同", "的", "內容"},
        {"這", "是", "一個", "測試", "文件", "包含", "更多", "詞"},
    ]
    
    for i, doc in enumerate(docs):
        lsh.add(i, doc)
    
    # 查詢相似的文價
    query = {"這", "是", "一個", "測試"}
    candidates = lsh.query(query)
    print(f"   查詢: {query}")
    print(f"   候選文件 ID: {candidates}")
    
    # 顯示與每個文件的實際 Jaccard
    print(f"   實際 Jaccard:")
    for i, doc in enumerate(docs):
        j = mh.jaccard_similarity(query, doc)
        print(f"     文件 {i}: {j:.4f}")
