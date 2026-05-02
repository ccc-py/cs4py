"""
Okapi BM25 排名函數實作

現代搜尋引擎的標準排名函數，結合詞頻飽和度和文件長度正規化。
"""

from typing import Dict, List, Tuple
import math
import re


class BM25:
    """Okapi BM25 排名演算法"""
    
    def __init__(self, k1: float = 1.5, b: float = 0.75) -> None:
        """
        初始化 BM25
        
        Args:
            k1: 詞頻飽和參數，通常 1.2-2.0
            b: 長度正規化參數，通常 0.75
        """
        self.k1 = k1
        self.b = b
        self.documents: List[str] = []
        self.doc_lengths: List[int] = []  # 每個文件的長度（詞數）
        self.avgdl: float = 0.0  # 平均文件長度
        self.df: Dict[str, int] = {}  # 文件頻率
        self.N: int = 0  # 總文件數
        self.vocabulary: set = set()
        
    def _tokenize(self, text: str) -> List[str]:
        """分詞"""
        return re.findall(r'\w+', text.lower())
    
    def fit(self, documents: List[str]) -> None:
        """
        從文件集合學習統計資訊
        
        Args:
            documents: 文件列表
        """
        self.documents = documents
        self.N = len(documents)
        self.doc_lengths = []
        self.df = {}
        
        # 計算文件長度和文件頻率
        for doc in documents:
            tokens = self._tokenize(doc)
            self.doc_lengths.append(len(tokens))
            
            # 計算 DF（使用集合去重）
            for token in set(tokens):
                self.df[token] = self.df.get(token, 0) + 1
                self.vocabulary.add(token)
        
        # 計算平均文件長度
        if self.N > 0:
            self.avgdl = sum(self.doc_lengths) / self.N
        else:
            self.avgdl = 0.0
    
    def compute_tf(self, term: str, doc_idx: int) -> float:
        """計算詞彙在文件中的詞頻"""
        tokens = self._tokenize(self.documents[doc_idx])
        return tokens.count(term.lower())
    
    def compute_idf(self, term: str) -> float:
        """計算 IDF 值"""
        df = self.df.get(term.lower(), 0)
        if df == 0:
            return 0.0
        # BM25 IDF 公式
        return math.log((self.N - df + 0.5) / (df + 0.5) + 1)
    
    def score(self, query: str, doc_idx: int) -> float:
        """
        計算查詢和單一文件的 BM25 分數
        
        BM25 公式：
        score = Σ IDF(qi) * (tf * (k1 + 1)) / (tf + k1 * (1 - b + b * dl/avgdl))
        
        Args:
            query: 查詢字串
            doc_idx: 文件索引
            
        Returns:
            BM25 分數
        """
        query_tokens = self._tokenize(query)
        doc_length = self.doc_lengths[doc_idx]
        
        # 長度正規化因子
        length_norm = 1.0 - self.b + self.b * (doc_length / self.avgdl)
        
        score = 0.0
        for token in set(query_tokens):  # 查詢詞去重
            tf = self.compute_tf(token, doc_idx)
            if tf == 0:
                continue
            
            idf = self.compute_idf(token)
            
            # BM25 詞項分數
            numerator = tf * (self.k1 + 1)
            denominator = tf + self.k1 * length_norm
            score += idf * numerator / denominator
        
        return score
    
    def rank(self, query: str) -> List[Tuple[int, float]]:
        """
        根據查詢對所有文件排名
        
        Args:
            query: 查詢字串
            
        Returns:
            排序後的 (文件索引, 分數) 列表
        """
        if self.N == 0:
            return []
        
        scores = []
        for doc_idx in range(self.N):
            s = self.score(query, doc_idx)
            scores.append((doc_idx, s))
        
        # 按分數降序排序
        scores.sort(key=lambda x: x[1], reverse=True)
        return scores


if __name__ == "__main__":
    # 示範用法
    print("=== BM25 示範 ===\n")
    
    # 準備文件
    documents = [
        "The quick brown fox jumps over the lazy dog",
        "A quick brown dog outpaces a fast fox",
        "The lazy dog sleeps all day in the sun",
        "The fox is quick and brown and likes to run",
        "Quick brown foxes jump over lazy dogs in the park"
    ]
    
    # 建立 BM25 模型
    bm25 = BM25(k1=1.5, b=0.75)
    bm25.fit(documents)
    
    print("1. 統計資訊:")
    print(f"   總文件數: {bm25.N}")
    print(f"   平均文件長度: {bm25.avgdl:.2f}")
    print(f"   詞彙表大小: {len(bm25.vocabulary)}")
    
    print("\n2. IDF 值（部分詞彙）:")
    for term in ["quick", "fox", "lazy", "dog"]:
        print(f"   {term}: IDF = {bm25.compute_idf(term):.4f}")
    
    print("\n3. 查詢排名:")
    query = "quick brown fox"
    rankings = bm25.rank(query)
    for doc_idx, score in rankings:
        print(f"  文件 {doc_idx}: {score:.4f}")
        print(f"    {documents[doc_idx][:50]}...")
    
    print("\n4. 不同參數的影響:")
    for k1, b in [(1.0, 0.5), (1.5, 0.75), (2.0, 0.75)]:
        bm25_test = BM25(k1=k1, b=b)
        bm25_test.fit(documents)
        top_score = bm25_test.rank(query)[0][1]
        print(f"  k1={k1}, b={b}: 最高分 = {top_score:.4f}")
