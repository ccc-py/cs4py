"""
恩尼格瑪密碼機 (Enigma Machine) - 簡化版

歷史背景：
恩尼格瑪密碼機由德國工程師亞瑟·謝爾比烏斯（Arthur Scherbius）於1918年發明，
二戰期間被德國軍方廣泛使用。其加密強度極高，直到波蘭數學家和英國
布萊切利園（Bletchley Park）的圖靈等人破解。

原理：
恩尼格瑪由以下組件構成：
1. 插線板（Plugboard）：交換字母對
2. 三個轉子（Rotor）：每個內部有26字母的替換映射
3. 反射板（Reflector）：將信號反射回轉子
4. 轉子步進機制：每次按鍵後右側轉子前進一位

作者：cs4py 專案
"""

from typing import List, Dict, Tuple


# 歷史上使用的轉子配線（簡化表示）
ROTOR_I = "EKMFLGDQVZNTOWYHXUSPAIBRCJ"
ROTOR_II = "AJDKSIRUXBLHWTMCQGZNPYFVOE"
ROTOR_III = "BDFHJLCPRTXVZNYEIWGAKMUSQO"

# 反射板配置（固定配對）
REFLECTOR_B = "YRUHQSLDPXNGOKMIEBFZCWVJAT"

# 轉子步進位置（當轉到特定字母時，左側轉子步進）
NOTCH_I = 'Q'
NOTCH_II = 'E'
NOTCH_III = 'V'


class Rotor:
    """轉子類別"""
    
    def __init__(self, wiring: str, notch: str, position: int = 0):
        """初始化轉子
        
        Args:
            wiring: 配線映射（26個字母的替換）
            notch: 步進位置
            position: 初始位置（0=A, 1=B, ..., 25=Z）
        """
        self.wiring = wiring
        self.notch = ord(notch) - ord('A')
        self.position = position
        # 反向映射（用於反射後的路徑）
        self.reverse_wiring = [''] * 26
        for i, c in enumerate(wiring):
            self.reverse_wiring[ord(c) - ord('A')] = chr(i + ord('A'))
    
    def forward(self, char: str) -> str:
        """向前轉換（從輸入到反射板方向）"""
        # 考慮轉子位置偏移
        idx = (ord(char) - ord('A') + self.position) % 26
        result = self.wiring[idx]
        # 反向偏移
        result_idx = (ord(result) - ord('A') - self.position) % 26
        return chr(result_idx + ord('A'))
    
    def backward(self, char: str) -> str:
        """向後轉換（從反射板返回方向）"""
        idx = (ord(char) - ord('A') + self.position) % 26
        result = self.reverse_wiring[idx]
        result_idx = (ord(result) - ord('A') - self.position) % 26
        return chr(result_idx + ord('A'))
    
    def step(self) -> bool:
        """步進轉子，返回是否觸發下一個轉子步進
        
        Returns:
            是否需要下個轉子步進
        """
        self.position = (self.position + 1) % 26
        return self.position == self.notch


class Reflector:
    """反射板類別"""
    
    def __init__(self, wiring: str):
        """初始化反射板"""
        self.wiring = wiring
    
    def reflect(self, char: str) -> str:
        """反射字母"""
        idx = ord(char) - ord('A')
        return self.wiring[idx]


class Plugboard:
    """插線板類別"""
    
    def __init__(self, connections: List[Tuple[str, str]] = None):
        """初始化插線板
        
        Args:
            connections: 字母對列表，如 [('A', 'B'), ('C', 'D')]
        """
        self.mapping = {chr(i + ord('A')): chr(i + ord('A')) for i in range(26)}
        if connections:
            for a, b in connections:
                self.mapping[a.upper()] = b.upper()
                self.mapping[b.upper()] = a.upper()
    
    def process(self, char: str) -> str:
        """處理字母（交換如果已連接）"""
        return self.mapping.get(char.upper(), char)


class EnigmaMachine:
    """恩尼格瑪密碼機"""
    
    def __init__(self, rotor_config: List[Tuple[str, int]] = None, 
                 plugboard_connections: List[Tuple[str, str]] = None):
        """初始化恩尼格瑪機
        
        Args:
            rotor_config: 轉子配置列表 [(轉子名稱, 初始位置), ...]
                         預設使用三個轉子
            plugboard_connections: 插線板連接
        """
        # 預設轉子配置
        if rotor_config is None:
            rotor_config = [('I', 0), ('II', 0), ('III', 0)]
        
        # 創建轉子
        rotor_map = {
            'I': (ROTOR_I, NOTCH_I),
            'II': (ROTOR_II, NOTCH_II),
            'III': (ROTOR_III, NOTCH_III)
        }
        
        self.rotors = []
        for name, pos in rotor_config:
            wiring, notch = rotor_map[name]
            self.rotors.append(Rotor(wiring, notch, pos))
        
        # 創建反射板
        self.reflector = Reflector(REFLECTOR_B)
        
        # 創建插線板
        self.plugboard = Plugboard(plugboard_connections)
    
    def set_rotor_positions(self, positions: List[int]) -> None:
        """設置轉子位置
        
        Args:
            positions: 位置列表（0-25）
        """
        for rotor, pos in zip(self.rotors, positions):
            rotor.position = pos
    
    def step_rotors(self) -> None:
        """步進轉子（從右到左）"""
        # 右側轉子總是步進
        carry = self.rotors[2].step()
        
        # 如果右側轉子到達缺口，中間轉子步進
        if carry:
            carry = self.rotors[1].step()
            # 如果中間轉子到達缺口，左側轉子步進
            if carry:
                self.rotors[0].step()
    
    def encrypt_char(self, char: str) -> str:
        """加密單個字符
        
        Args:
            char: 輸入字符
        
        Returns:
            加密後的字符
        """
        if not char.isalpha():
            return char
        
        char = char.upper()
        
        # 步進轉子
        self.step_rotors()
        
        # 插線板（輸入）
        c = self.plugboard.process(char)
        
        # 通過轉子（正向）
        for rotor in reversed(self.rotors):
            c = rotor.forward(c)
        
        # 反射板
        c = self.reflector.reflect(c)
        
        # 通過轉子（反向）
        for rotor in self.rotors:
            c = rotor.backward(c)
        
        # 插線板（輸出）
        c = self.plugboard.process(c)
        
        return c
    
    def encrypt(self, text: str) -> str:
        """加密文本
        
        Args:
            text: 輸入文本
        
        Returns:
            加密後的文本
        """
        result = []
        for char in text:
            result.append(self.encrypt_char(char))
        return ''.join(result)
    
    def decrypt(self, text: str) -> str:
        """解密文本（恩尼格瑪是對稱的）
        
        Args:
            text: 密文
        
        Returns:
            明文
        """
        return self.encrypt(text)


def create_default_enigma() -> EnigmaMachine:
    """創建預設配置的恩尼格瑪機"""
    return EnigmaMachine(
        rotor_config=[('I', 0), ('II', 0), ('III', 0)],
        plugboard_connections=[('A', 'B'), ('C', 'D')]
    )


if __name__ == "__main__":
    print("=== 恩尼格瑪密碼機演示 ===\n")
    
    # 演示1：基本加密解密
    print("演示1：基本加密")
    enigma = create_default_enigma()
    enigma.set_rotor_positions([0, 0, 0])  # A, A, A
    
    plaintext = "HELLO"
    ciphertext = enigma.encrypt(plaintext)
    print(f"明文: {plaintext}")
    print(f"密文: {ciphertext}")
    
    # 解密需要相同初始位置
    enigma.set_rotor_positions([0, 0, 0])
    decrypted = enigma.decrypt(ciphertext)
    print(f"解密: {decrypted}")
    print()
    
    # 演示2：不同位置
    print("演示2：不同轉子位置")
    enigma = create_default_enigma()
    enigma.set_rotor_positions([4, 18, 13])  # E, S, N
    
    plaintext = "SECRET MESSAGE"
    ciphertext = enigma.encrypt(plaintext)
    print(f"明文: {plaintext}")
    print(f"密文: {ciphertext}")
    
    enigma.set_rotor_positions([4, 18, 13])
    decrypted = enigma.decrypt(ciphertext)
    print(f"解密: {decrypted}")
    print()
    
    # 演示3：轉子步進機制
    print("演示3：轉子步進機制")
    enigma = create_default_enigma()
    enigma.set_rotor_positions([0, 0, 0])
    
    print("輸入字符，觀察轉子位置變化:")
    text = "ABC"
    for char in text:
        # 顯示步進前位置
        positions = [r.position for r in enigma.rotors]
        encrypted = enigma.encrypt_char(char)
        new_positions = [r.position for r in enigma.rotors]
        print(f"  輸入: {char} | 轉子位置: {positions} -> {new_positions} | 輸出: {encrypted}")
