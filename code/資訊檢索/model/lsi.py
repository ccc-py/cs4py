"""
潛在語意索引 (LSI) 實作

使用 SVD 進行降維，發現詞彙-文件矩陣中的潛在語意結構。
"""

from typing import Dict, List, Tuple
import math
import re
import random


class SVD:
    """純 Python 實作的奇異值分解（使用冪迭代法）"""
    
    def __init__(self, max_iterations: int = 100, tolerance: float = 1e-6) -> None:
        """
        初始化 SVD
        
        Args:
            max_iterations: 最大迭代次數
            tolerance: 收斂容差
        """
        self.max_iterations = max_iterations
        self.tolerance = tolerance
    
    def _transpose(self, matrix: List[List[float]]) -> List[List[float]]:
        """矩陣轉置"""
        rows = len(matrix)
        cols = len(matrix[0]) if rows > 0 else 0
        return [[matrix[i][j] for i in range(rows)] for j in range(cols)]
    
    def _multiply(self, a: List[List[float]], b: List[List[float]]) -> List[List[float]]:
        """矩陣乘法"""
        a_rows, a_cols = len(a), len(a[0]) if a else 0
        b_rows, b_cols = len(b), len(b[0]) if b else 0
        
        if a_cols != b_rows:
            raise ValueError("矩陣維度不匹配")
        
        result = [[0.0] * b_cols for _ in range(a_rows)]
        for i in range(a_rows):
            for j in range(b_cols):
                for k in range(a_cols):
                    result[i][j] += a[i][k] * b[k][j]
        
        return result
    
    def _power_iteration(self, matrix: List[List[float]], 
                        vector: List[float]) -> Tuple[float, List[float]]:
        """冪迭代法求最大特徵值和特徵向量"""
        n = len(vector)
        
        for _ in range(self.max_iterations):
            # 計算 new_v = A * v
            new_v = [0.0] * n
            for i in range(len(matrix)):
                for j in range(len(matrix[0])):
                    new_v[i] += matrix[i][j] * vector[j]
            
            # 正規化
            norm = math.sqrt(sum(x * x for x in new_v))
            if norm < 1e-10:
                break
            
            new_v = [x / norm for x in new_v]
            
            # 檢查收斂
            diff = sum(abs(new_v[i] - vector[i]) for i in range(n))
            vector = new_v
            
            if diff < self.tolerance:
                break
        
        # 計算特徵值
        Av = [0.0] * n
        for i in range(len(matrix)):
            for j in range(len(matrix[0])):
                Av[i] += matrix[i][j] * vector[j]
        
        eigenvalue = sum(Av[i] * vector[i] for i in range(n))
        return eigenvalue, vector
    
    def compute_svd(self, A: List[List[float]], k: int) -> Tuple[List[List[float]], List[float], List[List[float]]]:
        """
        計算矩陣 A 的 SVD（簡化版，僅求前 k 個奇異值和向量）
        
        A ≈ U * Σ * V^T
        
        Args:
            A: 輸入矩陣 (m x n)
            k: 保留的奇異值數量
            
        Returns:
            (U, S, Vt): U 矩陣, 奇異值列表, V 轉置矩陣
        """
        m, n = len(A), len(A[0]) if A else 0
        
        # 計算 A^T * A
        At = self._transpose(A)
        AtA = self._multiply(At, A)
        
        # 計算 A * A^T（用於左奇異向量）
        AAt = self._multiply(A, At)
        
        k = min(k, min(m, n))
        
        singular_values = []
        V_vectors = []
        
        # 對 AtA 使用冪迭代求特徵值和特徵向量
        remaining = [row[:] for row in AtA]  # 剩餘矩陣
        
        for _ in range(k):
            # 隨機初始化向量
            v = [random.random() for _ in range(n)]
            norm = math.sqrt(sum(x * x for x in v))
            v = [x / norm for x in v]
            
            # 冪迭代
            sigma_sq, v = self._power_iteration(remaining, v)
            sigma = math.sqrt(abs(sigma_sq)) if sigma_sq > 0 else 0.0
            
            if sigma < 1e-10:
                break
            
            singular_values.append(sigma)
            V_vectors.append(v)
            
            # 計算對應的 u 向量: u = A * v / sigma
            u = [0.0] * m
            for i in range(m):
                for j in range(n):
                    u[i] += A[i][j] * v[j]
            u = [x / sigma for x in u]
            
            # 從剩餘矩陣中減去當前成分（ deflation）
            for i in range(n):
                for j in range(n):
                    remaining[i][j] -= sigma_sq * v[i] * v[j]
        
        # 建構 U 矩陣
        U = []
        for i in range(len(V_vectors)):
            u = [0.0] * m
            for row in range(m):
                for col in range(n):
                    u[row] += A[row][col] * V_vectors[i][col]
            if singular_values[i] > 0:
                u = [x / singular_values[i] for x in u]
            U.append(u)
        
        U = [[U[j][i] for j in range(len(U))] for i in range(m)]  # 轉置為 m x k
        
        # 建構 V^T 矩陣
        Vt = [[V_vectors[j][i] for j in range(len(V_vectors))] for i in range(n)]
        
        return U, singular_values, Vt


class LSI:
    """潛在語意索引 (Latent Semantic Indexing)"""
    
    def __init__(self, n_components: int = 2) -> None:
        """
        初始化 LSI
        
        Args:
            n_components: 潛在語意維度數量
        """
        self.n_components = n_components
        self.vocabulary: List[str] = []
        self.vocab_index: Dict[str, int] = {}
        self.doc_vectors: List[List[float]] = []  # 降維後的文件向量
        self.term_vectors: List[List[float]] = []  # 降維後的詞彙向量
        self.U: List[List[float]] = []
        self.S: List[float] = []
        self.Vt: List[List[float]] = []
        
    def _tokenize(self, text: str) -> List[str]:
        """分詞"""
        return re.findall(r'\w+', text.lower())
    
    def _build_term_doc_matrix(self, documents: List[str]) -> List[List[float]]:
        """建立詞彙-文件矩陣"""
        # 建立詞彙表
        vocab_set = set()
        for doc in documents:
            tokens = self._tokenize(doc)
            vocab_set.update(tokens)
        
        self.vocabulary = sorted(vocab_set)
        self.vocab_index = {term: idx for idx, term in enumerate(self.vocabulary)}
        
        # 建立矩陣
        m = len(self.vocabulary)
        n = len(documents)
        matrix = [[0.0] * n for _ in range(m)]
        
        for doc_idx, doc in enumerate(documents):
            tokens = self._tokenize(doc)
            for token in tokens:
                if token in self.vocab_index:
                    matrix[self.vocab_index[token]][doc_idx] += 1.0
        
        return matrix
    
    def fit(self, documents: List[str]) -> None:
        """
        從文件集合學習 LSI 模型
        
        Args:
            documents: 文件列表
        """
        # 建立詞彙-文件矩陣
        A = self._build_term_doc_matrix(documents)
        
        # 計算 SVD
        svd = SVD()
        k = min(self.n_components, len(self.vocabulary), len(documents))
        self.U, self.S, self.Vt = svd.compute_svd(A, k)
        
        # 降維後的表示
        # 文件向量: S * Vt (實際上是 Vt 的前 k 行，每列是文件向量)
        self.doc_vectors = []
        for doc_idx in range(len(documents)):
            doc_vec = [self.S[i] * self.Vt[doc_idx][i] for i in range(k)]
            self.doc_vectors.append(doc_vec)
        
        # 詞彙向量: U
        self.term_vectors = []
        for term_idx in range(len(self.vocabulary)):
            term_vec = [self.U[term_idx][i] for i in range(k)]
            self.term_vectors.append(term_vec)
    
    def query(self, query_text: str, top_k: int = 5) -> List[Tuple[int, float]]:
        """
        使用查詢進行文件排名
        
        Args:
            query_text: 查詢文字
            top_k: 返回前 k 個結果
            
        Returns:
            排序後的 (文件索引, 相似度) 列表
        """
        if not self.doc_vectors:
            return []
        
        # 建立查詢向量（在原始空間）
        query_vec = [0.0] * len(self.vocabulary)
        tokens = self._tokenize(query_text)
        for token in tokens:
            if token in self.vocab_index:
                query_vec[self.vocab_index[token]] += 1.0
        
        # 投影到潛在語意空間: q_lsi = U^T * q
        k = len(self.S)
        query_lsi = [0.0] * k
        for i in range(k):
            for j in range(len(self.vocabulary)):
                query_lsi[i] += self.U[j][i] * query_vec[j]
        
        # 計算與每個文件的餘弦相似度
        scores = []
        for doc_idx, doc_vec in enumerate(self.doc_vectors):
            sim = self._cosine_similarity(query_lsi, doc_vec)
            scores.append((doc_idx, sim))
        
        scores.sort(key=lambda x: x[1], reverse=True)
        return scores[:top_k]
    
    def _cosine_similarity(self, vec1: List[float], vec2: List[float]) -> float:
        """計算餘弦相似度"""
        dot = sum(a * b for a, b in zip(vec1, vec2))
        norm1 = math.sqrt(sum(a * a for a in vec1))
        norm2 = math.sqrt(sum(b * b for b in vec2))
        
        if norm1 < 1e-10 or norm2 < 1e-10:
            return 0.0
        
        return dot / (norm1 * norm2)


if __name__ == "__main__":
    # 示範用法
    print("=== 潛在語意索引 (LSI) 示範 ===\n")
    
    # 準備文件（有同義詞關係）
    documents = [
        "The car is very fast and the vehicle is quick",
        "The automobile runs on the road very fast",
        "The doctor works in the hospital with medicine",
        "The physician treats patients in the medical center",
        "The car and automobile are both vehicles"
    ]
    
    print("1. 文件集合:")
    for i, doc in enumerate(documents):
        print(f"  [{i}] {doc}")
    
    # 建立 LSI 模型
    lsi = LSI(n_components=2)
    lsi.fit(documents)
    
    print(f"\n2. 奇異值: {[f'{s:.4f}' for s in lsi.S]}")
    
    print("\n3. 查詢測試:")
    queries = ["fast car", "doctor medicine", "vehicle"]
    for query in queries:
        results = lsi.query(query, top_k=3)
        print(f"\n  查詢: '{query}'")
        for doc_idx, score in results:
            print(f"    文件 {doc_idx}: {score:.4f} - {documents[doc_idx][:40]}...")
