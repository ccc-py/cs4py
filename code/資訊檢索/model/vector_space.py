"""
向量空間模型實作

將文件和查詢表示為向量，使用餘弦相似度進行排名。
"""

from typing import Dict, List, Tuple
import math
import re


class VectorSpaceModel:
    """向量空間模型"""
    
    def __init__(self, use_tfidf: bool = True) -> None:
        """
        初始化向量空間模型
        
        Args:
            use_tfidf: 是否使用 TF-IDF 加權（True）或原始詞頻（False）
        """
        self.use_tfidf = use_tfidf
        self.documents: List[str] = []
        self.vocabulary: List[str] = []
        self.vocab_index: Dict[str, int] = {}
        self.doc_vectors: List[List[float]] = []
        self.idf: List[float] = []
        self.N: int = 0
        
    def _tokenize(self, text: str) -> List[str]:
        """分詞"""
        return re.findall(r'\w+', text.lower())
    
    def _build_vocabulary(self, documents: List[str]) -> None:
        """建立詞彙表"""
        vocab_set = set()
        for doc in documents:
            tokens = self._tokenize(doc)
            vocab_set.update(tokens)
        
        self.vocabulary = sorted(vocab_set)
        self.vocab_index = {term: idx for idx, term in enumerate(self.vocabulary)}
    
    def _compute_tf_vector(self, text: str) -> List[float]:
        """計算詞頻向量"""
        tokens = self._tokenize(text)
        tf = [0.0] * len(self.vocabulary)
        
        for token in tokens:
            if token in self.vocab_index:
                tf[self.vocab_index[token]] += 1.0
        
        if self.use_tfidf:
            # 不使用 TF-IDF，只返回原始詞頻
            return tf
        else:
            # 正規化：除以文件長度
            doc_len = len(tokens)
            if doc_len > 0:
                tf = [v / doc_len for v in tf]
            return tf
    
    def _compute_idf(self, documents: List[str]) -> None:
        """計算 IDF 向量"""
        df = [0.0] * len(self.vocabulary)
        
        for doc in documents:
            tokens = set(self._tokenize(doc))
            for token in tokens:
                if token in self.vocab_index:
                    df[self.vocab_index[token]] += 1.0
        
        self.idf = []
        for i in range(len(self.vocabulary)):
            if df[i] > 0:
                self.idf.append(math.log(self.N / df[i]))
            else:
                self.idf.append(0.0)
    
    def fit(self, documents: List[str]) -> None:
        """
        從文件集合建立向量空間
        
        Args:
            documents: 文件列表
        """
        self.documents = documents
        self.N = len(documents)
        
        # 建立詞彙表
        self._build_vocabulary(documents)
        
        if self.use_tfidf:
            # 計算 IDF
            self._compute_idf(documents)
            
            # 計算每個文件的 TF-IDF 向量
            self.doc_vectors = []
            for doc in documents:
                tf = self._compute_tf_vector(doc)
                # TF-IDF = TF * IDF
                tfidf = [tf[i] * self.idf[i] for i in range(len(tf))]
                self.doc_vectors.append(tfidf)
        else:
            # 使用原始詞頻向量
            self.doc_vectors = [self._compute_tf_vector(doc) for doc in documents]
    
    def _cosine_similarity(self, vec1: List[float], vec2: List[float]) -> float:
        """計算餘弦相似度"""
        dot_product = sum(a * b for a, b in zip(vec1, vec2))
        norm1 = math.sqrt(sum(a * a for a in vec1))
        norm2 = math.sqrt(sum(b * b for b in vec2))
        
        if norm1 == 0 or norm2 == 0:
            return 0.0
        
        return dot_product / (norm1 * norm2)
    
    def query(self, query_text: str) -> List[Tuple[int, float]]:
        """
        使用查詢進行文件排名
        
        Args:
            query_text: 查詢文字
            
        Returns:
            排序後的 (文件索引, 相似度) 列表
        """
        if not self.doc_vectors:
            return []
        
        # 建立查詢向量
        query_vec = self._compute_tf_vector(query_text)
        if self.use_tfidf:
            query_vec = [query_vec[i] * self.idf[i] for i in range(len(query_vec))]
        
        # 計算與每個文件的相似度
        scores = []
        for doc_idx, doc_vec in enumerate(self.doc_vectors):
            sim = self._cosine_similarity(query_vec, doc_vec)
            scores.append((doc_idx, sim))
        
        # 按相似度降序排序
        scores.sort(key=lambda x: x[1], reverse=True)
        return scores


if __name__ == "__main__":
    # 示範用法
    print("=== 向量空間模型示範 ===\n")
    
    # 準備文件
    documents = [
        "The quick brown fox jumps over the lazy dog",
        "A quick brown dog outpaces a fast fox",
        "The lazy dog sleeps all day in the sun",
        "The fox is quick and brown and likes to run"
    ]
    
    print("1. 使用 TF-IDF 加權:")
    vsm_tfidf = VectorSpaceModel(use_tfidf=True)
    vsm_tfidf.fit(documents)
    
    query = "quick brown fox"
    results = vsm_tfidf.query(query)
    for doc_idx, score in results:
        print(f"  文件 {doc_idx}: 相似度 {score:.4f}")
        print(f"    {documents[doc_idx][:50]}...")
    
    print("\n2. 使用原始詞頻（無 IDF）:")
    vsm_raw = VectorSpaceModel(use_tfidf=False)
    vsm_raw.fit(documents)
    
    results_raw = vsm_raw.query(query)
    for doc_idx, score in results_raw:
        print(f"  文件 {doc_idx}: 相似度 {score:.4f}")
    
    print("\n3. 詞彙表（前 10 個）:")
    for i, term in enumerate(vsm_tfidf.vocabulary[:10]):
        print(f"  {term}: IDF = {vsm_tfidf.idf[i]:.4f}")
