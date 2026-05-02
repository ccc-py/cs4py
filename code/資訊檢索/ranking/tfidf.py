"""
TF-IDF 權重計算

實作 TF-IDF 加權方法，包含詞頻（原始、對數正規化）和逆文件頻率。
"""

from typing import Dict, List, Tuple
import math
import re


class TfidfVectorizer:
    """TF-IDF 向量化器"""
    
    def __init__(self, use_log_tf: bool = True, smooth_idf: bool = True) -> None:
        """
        初始化 TF-IDF 向量化器
        
        Args:
            use_log_tf: 是否使用對數正規化詞頻
            smooth_idf: 是否平滑 IDF（加 1 到分母）
        """
        self.use_log_tf = use_log_tf
        self.smooth_idf = smooth_idf
        self.vocabulary_: Dict[str, int] = {}  # 詞彙到索引的映射
        self.idf_: Dict[str, float] = {}  # IDF 值
        self.doc_count_: int = 0
    
    def _tokenize(self, text: str) -> List[str]:
        """分詞：轉小寫，擷取字母數字詞"""
        return re.findall(r'\w+', text.lower())
    
    def _compute_tf(self, tokens: List[str]) -> Dict[str, float]:
        """計算詞頻（TF）"""
        tf = {}
        token_count = len(tokens)
        
        if token_count == 0:
            return tf
        
        # 計算原始詞頻
        for token in tokens:
            tf[token] = tf.get(token, 0.0) + 1.0
        
        # 正規化
        if self.use_log_tf:
            # 對數正規化：1 + log(tf)
            for token in tf:
                tf[token] = 1.0 + math.log(tf[token])
        else:
            # 原始詞頻除以文件長度
            for token in tf:
                tf[token] /= token_count
        
        return tf
    
    def fit(self, documents: List[str]) -> None:
        """
        從文件集合學習 IDF 值
        
        Args:
            documents: 文件列表
        """
        self.doc_count_ = len(documents)
        df = {}  # 文件頻率：包含詞彙的文件數
        
        # 建立詞彙表和計算 DF
        for doc in documents:
            tokens = set(self._tokenize(doc))  # 去重計算 DF
            for token in tokens:
                df[token] = df.get(token, 0) + 1
                if token not in self.vocabulary_:
                    self.vocabulary_[token] = len(self.vocabulary_)
        
        # 計算 IDF
        for token, doc_freq in df.items():
            if self.smooth_idf:
                # 平滑 IDF：log((N + 1) / (df + 1)) + 1
                self.idf_[token] = math.log(
                    (self.doc_count_ + 1) / (doc_freq + 1)
                ) + 1.0
            else:
                # 標準 IDF：log(N / df)
                self.idf_[token] = math.log(self.doc_count_ / doc_freq)
    
    def transform(self, documents: List[str]) -> List[Dict[str, float]]:
        """
        將文件轉換為 TF-IDF 向量
        
        Returns:
            每個文件的 TF-IDF 向量（詞彙到分數的字典）
        """
        vectors = []
        
        for doc in documents:
            tokens = self._tokenize(doc)
            tf = self._compute_tf(tokens)
            tfidf = {}
            
            for token, tf_val in tf.items():
                if token in self.idf_:
                    tfidf[token] = tf_val * self.idf_[token]
            
            vectors.append(tfidf)
        
        return vectors
    
    def rank_documents(self, query: str, documents: List[str]) -> List[Tuple[int, float]]:
        """
        根據查詢對文件排名
        
        Args:
            query: 查詢字串
            documents: 候選文件列表
            
        Returns:
            排序後的 (文件索引, 分數) 列表，分數由高到低
        """
        self.fit(documents)
        doc_vectors = self.transform(documents)
        
        # 計算查詢向量
        query_tokens = self._tokenize(query)
        query_tf = self._compute_tf(query_tokens)
        query_vector = {}
        for token, tf_val in query_tf.items():
            if token in self.idf_:
                query_vector[token] = tf_val * self.idf_[token]
        
        # 計算餘弦相似度
        scores = []
        for doc_idx, doc_vector in enumerate(doc_vectors):
            similarity = self._cosine_similarity(query_vector, doc_vector)
            scores.append((doc_idx, similarity))
        
        # 按分數降序排序
        scores.sort(key=lambda x: x[1], reverse=True)
        return scores
    
    def _cosine_similarity(self, vec1: Dict[str, float], 
                          vec2: Dict[str, float]) -> float:
        """計算兩個向量的餘弦相似度"""
        # 計算點積
        dot_product = 0.0
        all_tokens = set(vec1.keys()) | set(vec2.keys())
        for token in all_tokens:
            dot_product += vec1.get(token, 0.0) * vec2.get(token, 0.0)
        
        # 計算範數
        norm1 = math.sqrt(sum(v * v for v in vec1.values()))
        norm2 = math.sqrt(sum(v * v for v in vec2.values()))
        
        if norm1 == 0 or norm2 == 0:
            return 0.0
        
        return dot_product / (norm1 * norm2)


if __name__ == "__main__":
    # 示範用法
    print("=== TF-IDF 示範 ===\n")
    
    # 準備文件
    documents = [
        "The quick brown fox jumps over the lazy dog",
        "A quick brown dog outpaces a fast fox",
        "The lazy dog sleeps all day in the sun",
        "The fox is quick and brown and likes to run"
    ]
    
    # 建立 TF-IDF 向量化器
    vectorizer = TfidfVectorizer(use_log_tf=True, smooth_idf=True)
    vectorizer.fit(documents)
    
    print("1. 詞彙表:")
    for token, idx in sorted(vectorizer.vocabulary_.items()):
        print(f"  {token}: IDF = {vectorizer.idf_[token]:.4f}")
    
    print("\n2. 文件 TF-IDF 向量（前 5 個詞）:")
    vectors = vectorizer.transform(documents)
    for doc_idx, vec in enumerate(vectors):
        print(f"  文件 {doc_idx}: {dict(list(vec.items())[:5])}")
    
    print("\n3. 查詢排名:")
    query = "quick brown fox"
    rankings = vectorizer.rank_documents(query, documents)
    for doc_idx, score in rankings:
        print(f"  文件 {doc_idx}: 分數 {score:.4f}")
        print(f"    內容: {documents[doc_idx][:50]}...")
    
    print("\n4. 不同 TF 方法比較:")
    vec_raw = TfidfVectorizer(use_log_tf=False)
    rankings_raw = vec_raw.rank_documents(query, documents)
    print("  使用原始詞頻:")
    for doc_idx, score in rankings_raw:
        print(f"    文件 {doc_idx}: {score:.4f}")
