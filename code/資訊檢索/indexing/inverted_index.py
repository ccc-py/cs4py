"""
反向索引實作

從文件集合建立反向索引，支援位置資訊和布林查詢。
"""

from collections import defaultdict
from typing import Dict, List, Set, Tuple
import re


class InvertedIndex:
    """反向索引類別，支援詞彙位置和布林查詢"""
    
    def __init__(self) -> None:
        # index[term][doc_id] = [positions]
        self.index: Dict[str, Dict[int, List[int]]] = defaultdict(
            lambda: defaultdict(list)
        )
        self.documents: Dict[int, str] = {}
        self.doc_ids: Set[int] = set()
    
    def _tokenize(self, text: str) -> List[str]:
        """簡單分詞：轉小寫，擷取字母數字詞"""
        return re.findall(r'\w+', text.lower())
    
    def add_document(self, doc_id: int, text: str) -> None:
        """新增文件到索引"""
        self.documents[doc_id] = text
        self.doc_ids.add(doc_id)
        tokens = self._tokenize(text)
        for pos, term in enumerate(tokens):
            self.index[term][doc_id].append(pos)
    
    def get_postings(self, term: str) -> Dict[int, List[int]]:
        """取得詞彙的投寄列表"""
        return self.index.get(term, {})
    
    def boolean_and(self, term1: str, term2: str) -> Set[int]:
        """布林 AND 查詢"""
        post1 = set(self.index.get(term1, {}).keys())
        post2 = set(self.index.get(term2, {}).keys())
        return post1 & post2
    
    def boolean_or(self, term1: str, term2: str) -> Set[int]:
        """布林 OR 查詢"""
        post1 = set(self.index.get(term1, {}).keys())
        post2 = set(self.index.get(term2, {}).keys())
        return post1 | post2
    
    def boolean_not(self, term: str) -> Set[int]:
        """布林 NOT 查詢"""
        post = set(self.index.get(term, {}).keys())
        return self.doc_ids - post
    
    def phrase_query(self, phrase: str) -> Set[int]:
        """片語查詢（詞彙連續出現）"""
        terms = self._tokenize(phrase)
        if not terms:
            return set()
        
        # 取得第一個詞的出現文件
        result = set(self.index.get(terms[0], {}).keys())
        
        for doc_id in list(result):
            positions = self.index[terms[0]][doc_id]
            # 檢查後續詞是否依序出現
            for i, term in enumerate(terms[1:], 1):
                if term not in self.index:
                    result.discard(doc_id)
                    break
                next_positions = self.index[term][doc_id]
                # 檢查是否存在位置差為 i
                if not any(pos + i in next_positions for pos in positions):
                    result.discard(doc_id)
                    break
        
        return result
    
    def boolean_query(self, query: str) -> Set[int]:
        """解析並執行布林查詢（支援 AND, OR, NOT, 括號）"""
        tokens = re.findall(r'\w+|\(|\)|AND|OR|NOT', query.upper())
        return self._evaluate_postfix(self._infix_to_postfix(tokens))
    
    def _infix_to_postfix(self, tokens: List[str]) -> List[str]:
        """中序轉後序（Shunting-yard 演算法）"""
        precedence = {'NOT': 3, 'AND': 2, 'OR': 1}
        output = []
        stack = []
        
        for token in tokens:
            if token.isalnum():
                output.append(token.lower())
            elif token in precedence:
                while (stack and stack[-1] != '(' and
                       precedence.get(stack[-1], 0) >= precedence[token]):
                    output.append(stack.pop())
                stack.append(token)
            elif token == '(':
                stack.append(token)
            elif token == ')':
                while stack and stack[-1] != '(':
                    output.append(stack.pop())
                stack.pop()  # 移除 '('
        
        while stack:
            output.append(stack.pop())
        
        return output
    
    def _evaluate_postfix(self, postfix: List[str]) -> Set[int]:
        """評估後序運算式"""
        stack = []
        
        for token in postfix:
            if token in ('AND', 'OR', 'NOT'):
                if token == 'NOT':
                    operand = stack.pop()
                    if isinstance(operand, str):
                        operand = set(self.index.get(operand, {}).keys())
                    result = self.doc_ids - operand
                    stack.append(result)
                else:
                    right = stack.pop()
                    left = stack.pop()
                    if isinstance(left, str):
                        left = set(self.index.get(left, {}).keys())
                    if isinstance(right, str):
                        right = set(self.index.get(right, {}).keys())
                    
                    if token == 'AND':
                        stack.append(left & right)
                    else:  # OR
                        stack.append(left | right)
            else:
                stack.append(token)
        
        result = stack[0]
        if isinstance(result, str):
            result = set(self.index.get(result, {}).keys())
        return result


if __name__ == "__main__":
    # 示範用法
    print("=== 反向索引示範 ===\n")
    
    # 建立索引
    idx = InvertedIndex()
    docs = {
        1: "The quick brown fox jumps over the lazy dog",
        2: "A quick brown dog outpaces a fast fox",
        3: "The lazy dog sleeps all day",
        4: "The fox is quick and brown"
    }
    
    for doc_id, text in docs.items():
        idx.add_document(doc_id, text)
    
    # 顯示索引
    print("1. 反向索引內容：")
    for term in sorted(idx.index.keys()):
        postings = idx.index[term]
        print(f"  {term}: {dict(postings)}")
    
    # 布林查詢
    print("\n2. 布林查詢：")
    print(f"  'quick' AND 'fox': {idx.boolean_and('quick', 'fox')}")
    print(f"  'lazy' OR 'fast': {idx.boolean_or('lazy', 'fast')}")
    print(f"  NOT 'fox': {idx.boolean_not('fox')}")
    
    # 片語查詢
    print("\n3. 片語查詢：")
    print(f"  'quick brown': {idx.phrase_query('quick brown')}")
    
    # 複雜布林查詢
    print("\n4. 複雜布林查詢：")
    query = "(quick AND fox) OR (lazy AND dog)"
    print(f"  查詢: {query}")
    print(f"  結果: {idx.boolean_query(query)}")
    
    query2 = "NOT fox AND lazy"
    print(f"  查詢: {query2}")
    print(f"  結果: {idx.boolean_query(query2)}")
