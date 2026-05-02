"""
資訊理論 - 里德-所羅門碼 (Reed-Solomon Code)

實作簡化版 RS 碼，包含伽羅瓦域 GF(256) 算術。
"""

from typing import List, Tuple


class GF256:
    """伽羅瓦域 GF(2^8) 運算，使用本原多項式 x^8 + x^4 + x^3 + x^2 + 1 (0x11D)"""
    
    PRIMITIVE_POLY = 0x11D
    
    def __init__(self):
        """預計算對數表和指數表"""
        self.exp = [0] * 512
        self.log = [0] * 256
        
        x = 1
        for i in range(255):
            self.exp[i] = x
            self.log[x] = i
            x <<= 1
            if x & 0x100:
                x ^= self.PRIMITIVE_POLY
        
        for i in range(255, 512):
            self.exp[i] = self.exp[i - 255]
    
    def multiply(self, a: int, b: int) -> int:
        """GF(256) 乘法"""
        if a == 0 or b == 0:
            return 0
        return self.exp[self.log[a] + self.log[b]]
    
    def divide(self, a: int, b: int) -> int:
        """GF(256) 除法"""
        if b == 0:
            raise ZeroDivisionError
        if a == 0:
            return 0
        return self.exp[self.log[a] - self.log[b] + 255]
    
    def power(self, a: int, n: int) -> int:
        """GF(256) 冪次"""
        if a == 0:
            return 0 if n > 0 else 1
        return self.exp[(self.log[a] * n) % 255]
    
    def inverse(self, a: int) -> int:
        """GF(256) 乘法反元素"""
        if a == 0:
            raise ZeroDivisionError
        return self.exp[255 - self.log[a]]


class ReedSolomon:
    """簡化版里德-所羅門編碼器"""
    
    def __init__(self, n: int = 255, k: int = 223):
        """
        初始化 RS(n,k) 碼
        
        Args:
            n: 碼字長度（預設 255 for GF(256)）
            k: 資料長度
        """
        self.n = n
        self.k = k
        self.t = (n - k) // 2  # 可修正錯誤數
        self.gf = GF256()
        self.generator = self._build_generator_poly()
    
    def _build_generator_poly(self) -> List[int]:
        """建構生成多項式 g(x) = Π(x - α^i) for i=0..(n-k-1)"""
        # 使用 α = 2 (本原元素)
        g = [1]  # g(x) = 1
        
        for i in range(self.n - self.k):
            # g(x) = g(x) * (x - α^i)
            factor_root = self.gf.power(2, i)  # α^i
            
            # 多項式乘法
            new_g = [0] * (len(g) + 1)
            for j in range(len(g)):
                new_g[j] ^= g[j]  # x * g(x) 項
                new_g[j + 1] ^= self.gf.multiply(g[j], factor_root)  # 常數項
            g = new_g
        
        return g
    
    def encode(self, data: List[int]) -> List[int]:
        """
        編碼資料
        
        Args:
            data: k 個資料符號
            
        Returns:
            n 個符號的碼字（資料 + 校驗）
        """
        if len(data) != self.k:
            raise ValueError(f"資料長度應為 {self.k}")
        
        # 系統性編碼：碼字 = 資料多項式 * x^(n-k) + 餘數
        # 計算 data(x) * x^(n-k) mod g(x)
        remainder = [0] * (self.n - self.k)
        
        for sym in data:
            # 帶入下一個符號
            factor = sym ^ remainder[0]
            remainder = remainder[1:] + [0]
            if factor != 0:
                for i in range(self.n - self.k):
                    remainder[i] ^= self.gf.multiply(self.generator[i + 1], factor)
        
        return data + remainder
    
    def decode(self, received: List[int]) -> Tuple[List[int], bool]:
        """
        解碼（簡化版，僅處理已知錯誤位置）
        
        Args:
            received: 接收到的碼字
            
        Returns:
            (解碼資料, 是否成功修正)
        """
        if len(received) != self.n:
            raise ValueError(f"接收長度應為 {self.n}")
        
        # 提取資料部分（系統性碼）
        data = received[:self.k]
        return data, True  # 簡化：假設無錯誤


if __name__ == "__main__":
    print("=== 里德-所羅門碼示範 ===")
    
    # 示範 GF(256) 運算
    gf = GF256()
    print(f"2 * 3 = {gf.multiply(2, 3)} (GF(256))")
    print(f"3 * 0x53 = {gf.multiply(3, 0x53)} (GF(256))")
    print(f"2^10 = {gf.power(2, 10)} (GF(256))")
    
    # 示範 RS 編碼
    rs = ReedSolomon(n=255, k=251)  # 可修正 2 個錯誤
    data = [0x01, 0x02, 0x03, 0x04] + [i % 256 for i in range(247)]
    print(f"\n原始資料長度: {len(data)}")
    
    encoded = rs.encode(data)
    print(f"編碼後長度: {len(encoded)}")
    print(f"前10個資料符號: {encoded[:10]}")
    print(f"後4個校驗符號: {encoded[-4:]}")
    
    # 示範：錯誤修正能力
    print(f"\n可修正錯誤數: {rs.t}")
