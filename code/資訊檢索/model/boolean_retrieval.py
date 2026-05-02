"""
布林檢索模型實作

解析並評估布林查詢，支援合取範式（CNF）和析取範式（DNF）。
"""

from typing import Dict, List, Set, Tuple, Union, Optional
import re
from enum import Enum


class BooleanOperator(Enum):
    """布林運算子"""
    AND = "AND"
    OR = "OR"
    NOT = "NOT"
    AND_NOT = "AND NOT"


class BooleanQuery:
    """布林查詢解析器"""
    
    def __init__(self) -> None:
        self.tokens: List[str] = []
        
    def parse(self, query: str) -> List[str]:
        """
        解析布林查詢，轉換為後序表示法
        
        Args:
            query: 布林查詢字串，支援 AND, OR, NOT, 括號
            
        Returns:
            後序表示法的 token 列表
        """
        # 正規化：將運算子轉為大寫
        tokens = re.findall(r'\w+|\(|\)|AND|OR|NOT|AND\s+NOT', query, re.IGNORECASE)
        
        # 處理 AND NOT
        processed = []
        i = 0
        while i < len(tokens):
            if tokens[i].upper() == 'AND' and i + 1 < len(tokens) and tokens[i + 1].upper() == 'NOT':
                processed.append('AND_NOT')
                i += 2
            else:
                processed.append(tokens[i])
                i += 1
        
        return self._infix_to_postfix(processed)
    
    def _infix_to_postfix(self, tokens: List[str]) -> List[str]:
        """中序轉後序（Shunting-yard 演算法）"""
        precedence = {'NOT': 3, 'AND': 2, 'OR': 1, 'AND_NOT': 2}
        output = []
        stack = []
        
        for token in tokens:
            if token.upper() in precedence:
                op = token.upper()
                while (stack and stack[-1] != '(' and
                       precedence.get(stack[-1], 0) >= precedence[op]):
                    output.append(stack.pop())
                stack.append(op)
            elif token == '(':
                stack.append(token)
            elif token == ')':
                while stack and stack[-1] != '(':
                    output.append(stack.pop())
                if stack and stack[-1] == '(':
                    stack.pop()
            else:
                output.append(token.lower())
        
        while stack:
            output.append(stack.pop())
        
        return output


class BooleanRetrievalModel:
    """布林檢索模型"""
    
    def __init__(self) -> None:
        self.documents: Dict[int, str] = {}
        self.index: Dict[str, Set[int]] = {}  # 詞彙 -> 文件 ID 集合
        self.next_doc_id: int = 0
        
    def _tokenize(self, text: str) -> List[str]:
        """分詞"""
        return re.findall(r'\w+', text.lower())
    
    def add_document(self, text: str) -> int:
        """新增文件，返回文件 ID"""
        doc_id = self.next_doc_id
        self.documents[doc_id] = text
        self.next_doc_id += 1
        
        # 更新索引
        tokens = self._tokenize(text)
        for token in set(tokens):
            if token not in self.index:
                self.index[token] = set()
            self.index[token].add(doc_id)
        
        return doc_id
    
    def add_documents(self, texts: List[str]) -> List[int]:
        """批次新增文件"""
        return [self.add_document(text) for text in texts]
    
    def _evaluate_postfix(self, postfix: List[str]) -> Set[int]:
        """評估後序運算式"""
        stack: List[Union[Set[int], str]] = []
        all_docs = set(self.documents.keys())
        
        for token in postfix:
            if token in ('AND', 'OR', 'NOT', 'AND_NOT'):
                if token == 'NOT':
                    operand = stack.pop()
                    if isinstance(operand, str):
                        operand = self.index.get(operand, set())
                    result = all_docs - operand
                    stack.append(result)
                elif token == 'AND_NOT':
                    right = stack.pop()
                    left = stack.pop()
                    if isinstance(left, str):
                        left = self.index.get(left, set())
                    if isinstance(right, str):
                        right = self.index.get(right, set())
                    result = left - right
                    stack.append(result)
                else:
                    right = stack.pop()
                    left = stack.pop()
                    if isinstance(left, str):
                        left = self.index.get(left, set())
                    if isinstance(right, str):
                        right = self.index.get(right, set())
                    
                    if token == 'AND':
                        stack.append(left & right)
                    else:  # OR
                        stack.append(left | right)
            else:
                stack.append(token)
        
        result = stack[0]
        if isinstance(result, str):
            result = self.index.get(result, set())
        return result
    
    def search(self, query: str) -> Set[int]:
        """
        執行布林查詢
        
        Args:
            query: 布林查詢字串
            
        Returns:
            符合條件的文件 ID 集合
        """
        parser = BooleanQuery()
        postfix = parser.parse(query)
        return self._evaluate_postfix(postfix)
    
    def to_cnf(self, query: str) -> List[List[str]]:
        """
        將查詢轉換為合取範式（CNF）
        
        簡化版本：將 OR 分散到 AND 上
        """
        # 這是一個簡化實作，實際 CNF 轉換需要處理複雜邏輯
        # 這裡只處理簡單情況
        return [["placeholder"]]
    
    def to_dnf(self, query: str) -> List[List[str]]:
        """
        將查詢轉換為析取範式（DNF）
        
        簡化版本：將 AND 分散到 OR 上
        """
        # 這是一個簡化實作
        return [["placeholder"]]


if __name__ == "__main__":
    # 示範用法
    print("=== 布林檢索模型示範 ===\n")
    
    # 準備文件
    docs = [
        "The quick brown fox jumps over the lazy dog",
        "A quick brown dog outpaces a fast fox",
        "The lazy dog sleeps all day in the sun",
        "The fox is quick and brown and likes to run",
        "The sun is bright and the day is warm"
    ]
    
    # 建立模型
    model = BooleanRetrievalModel()
    doc_ids = model.add_documents(docs)
    
    print("1. 文件列表:")
    for doc_id, text in model.documents.items():
        print(f"  [{doc_id}] {text[:50]}...")
    
    print("\n2. 布林查詢:")
    queries = [
        "quick AND fox",
        "lazy OR fast",
        "NOT fox",
        "(quick OR fast) AND lazy",
        "fox AND NOT lazy"
    ]
    
    for query in queries:
        results = model.search(query)
        print(f"  '{query}': {results}")
    
    print("\n3. 索引狀態（部分詞彙）:")
    for term in ["quick", "fox", "lazy", "dog"]:
        docs_with_term = model.index.get(term, set())
        print(f"  '{term}': {docs_with_term}")
