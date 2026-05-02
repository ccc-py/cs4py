"""
文字預處理與分詞器實作

包含斷詞、小寫化、停用詞移除、簡單詞幹提取（Porter Stemmer 簡化版）。
"""

from typing import List, Set
import re


class SimpleTokenizer:
    """簡單分詞器"""
    
    def __init__(self, lowercase: bool = True, 
                 remove_stopwords: bool = True,
                 stemming: bool = False) -> None:
        """
        初始化分詞器
        
        Args:
            lowercase: 是否轉為小寫
            remove_stopwords: 是否移除停用詞
            stemming: 是否進行詞幹提取
        """
        self.lowercase = lowercase
        self.remove_stopwords = remove_stopwords
        self.stemming = stemming
        
        # 常見英文停用詞
        self.stopwords: Set[str] = {
            'a', 'an', 'and', 'are', 'as', 'at', 'be', 'by', 'for', 
            'from', 'has', 'he', 'in', 'is', 'it', 'its', 'of', 'on', 
            'that', 'the', 'to', 'was', 'will', 'with', 'i', 'you', 
            'we', 'they', 'my', 'your', 'his', 'her', 'our', 'their',
            'me', 'him', 'us', 'them', 'this', 'that', 'these', 'those',
            'am', 'been', 'being', 'do', 'does', 'did', 'have', 'had',
            'has', 'having', 'but', 'or', 'if', 'because', 'as', 'until',
            'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against',
            'between', 'into', 'through', 'during', 'before', 'after',
            'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out'
        }
    
    def tokenize(self, text: str) -> List[str]:
        """
        分詞主函數
        
        Args:
            text: 輸入文字
            
        Returns:
            分詞後的詞彙列表
        """
        # 分詞：擷取字母數字詞
        tokens = re.findall(r'\w+', text)
        
        # 小寫化
        if self.lowercase:
            tokens = [t.lower() for t in tokens]
        
        # 移除停用詞
        if self.remove_stopwords:
            tokens = [t for t in tokens if t not in self.stopwords]
        
        # 詞幹提取
        if self.stemming:
            tokens = [self.stem(t) for t in tokens]
        
        return tokens
    
    def stem(self, word: str) -> str:
        """
        簡化版 Porter Stemmer
        
        實作常見的詞幹規則：
        1. 移除複數：ies -> y, es -> , s -> (條件)
        2. 移除進行式：ing -> 
        3. 移除過去式：ed -> (條件)
        
        Args:
            word: 輸入詞彙
            
        Returns:
            詞幹
        """
        if len(word) <= 2:
            return word
        
        stem = word.lower()
        
        # 規則 1: 以 ies 結尾 -> y
        if stem.endswith('ies'):
            stem = stem[:-3] + 'y'
            return stem
        
        # 規則 2: 以 sses 結尾 -> ss
        if stem.endswith('sses'):
            stem = stem[:-2]
            return stem
        
        # 規則 3: 以 ss 結尾，保持不變
        if stem.endswith('ss'):
            return stem
        
        # 規則 4: 去除複數 s（長度 > 3）
        if stem.endswith('s') and len(stem) > 3:
            stem = stem[:-1]
        
        # 規則 5: 去除 ing（長度 > 4，且去掉後至少有 3 個字符）
        if stem.endswith('ing') and len(stem) > 4:
            stem = stem[:-3]
            if len(stem) >= 3:
                return stem
        
        # 規則 6: 去除 ed（長度 > 4，且去掉後至少有 3 個字符）
        if stem.endswith('ed') and len(stem) > 4:
            stem = stem[:-2]
            if len(stem) >= 3:
                return stem
        
        # 規則 7: 去除 ly（副詞）
        if stem.endswith('ly') and len(stem) > 4:
            stem = stem[:-2]
        
        return stem
    
    def add_stopwords(self, words: List[str]) -> None:
        """新增停用詞"""
        for word in words:
            self.stopwords.add(word.lower() if self.lowercase else word)
    
    def remove_stopwords_list(self, words: List[str]) -> None:
        """從停用詞列表中移除"""
        for word in words:
            self.stopwords.discard(word.lower() if self.lowercase else word)


class PorterStemmer:
    """
    Porter Stemmer 簡化實作
    
    基於 Martin Porter 的演算法，實作核心步驟。
    """
    
    def __init__(self) -> None:
        pass
    
    def stem(self, word: str) -> str:
        """主要詞幹提取函數"""
        if len(word) <= 2:
            return word
        
        # 步驟 1a: 處理複數和過去分詞
        word = self._step1a(word)
        
        # 步驟 1b: 處理動詞變化
        word = self._step1b(word)
        
        # 步驟 1c: 處理 y -> i
        word = self._step1c(word)
        
        # 步驟 2-4: 更複雜的規則（簡化版省略）
        
        return word
    
    def _step1a(self, word: str) -> str:
        """步驟 1a: sses -> ss, ies -> i, ss -> ss, s -> """
        if word.endswith('sses'):
            return word[:-2]
        if word.endswith('ies'):
            return word[:-3] + 'i'
        if word.endswith('ss'):
            return word
        if word.endswith('s'):
            return word[:-1]
        return word
    
    def _step1b(self, word: str) -> str:
        """步驟 1b: ed, ing 結尾處理"""
        if word.endswith('eed'):
            if len(word) > 4:
                return word[:-1]  # eed -> ee (簡化)
            return word
        
        if word.endswith('ed'):
            word = word[:-2]
            if self._ends_with_cvc(word) and len(word) >= 4:
                return word[:-1] + 'e'  # 還原 e
            return word
        
        if word.endswith('ing'):
            word = word[:-3]
            if self._ends_with_cvc(word) and len(word) >= 4:
                return word[:-1] + 'e'
            return word
        
        return word
    
    def _step1c(self, word: str) -> str:
        """步驟 1c: y -> i"""
        if word.endswith('y') and len(word) > 2:
            # 前一個字符是輔音
            if word[-2] not in 'aeiou':
                return word[:-1] + 'i'
        return word
    
    def _ends_with_cvc(self, word: str) -> bool:
        """檢查是否以輔音-母音-輔音結尾"""
        if len(word) < 3:
            return False
        return (word[-1] not in 'aeiou' and 
                word[-2] in 'aeiou' and 
                word[-3] not in 'aeiou')


if __name__ == "__main__":
    # 示範用法
    print("=== 文字預處理與分詞器示範 ===\n")
    
    # 測試文字
    text = "The quick brown foxes are jumping over the lazy dogs in the garden"
    
    print("1. 基本分詞:")
    tokenizer = SimpleTokenizer(lowercase=True, remove_stopwords=False, stemming=False)
    tokens = tokenizer.tokenize(text)
    print(f"  原文: {text}")
    print(f"  分詞: {tokens}")
    
    print("\n2. 移除停用詞:")
    tokenizer.remove_stopwords = True
    tokens_no_stop = tokenizer.tokenize(text)
    print(f"  結果: {tokens_no_stop}")
    
    print("\n3. 詞幹提取:")
    tokenizer.stemming = True
    tokens_stemmed = tokenizer.tokenize(text)
    print(f"  結果: {tokens_stemmed}")
    
    print("\n4. 測試詞幹提取:")
    test_words = ["running", "flies", "easily", "jumped", "happier"]
    print("  詞彙 -> 詞幹:")
    for word in test_words:
        stem = tokenizer.stem(word)
        print(f"    {word} -> {stem}")
    
    print("\n5. Porter Stemmer 測試:")
    porter = PorterStemmer()
    test_words2 = ["running", "flies", "easily", "jumped", "happier", "cats", "bushes"]
    for word in test_words2:
        stem = porter.stem(word)
        print(f"    {word} -> {stem}")
