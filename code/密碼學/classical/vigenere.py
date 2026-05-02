"""
維吉尼亞密碼 (Vigenère Cipher)

歷史背景：
維吉尼亞密碼由16世紀法國密碼學家布萊斯·德·維吉尼亞（Blaise de Vigenère）
發明，曾被稱為「不可破解的密碼」（le chiffre indéchiffrable）。它使用
多表替換技術，比凱薩密碼安全得多，直到19世紀才被卡西斯基（Kasiski）破解。

原理：
使用關鍵字（key）來決定每個字母的移位量。關鍵字的每個字母對應一個移位值
（A=0, B=1, ..., Z=25），明文中的每個字母使用對應的移位進行凱薩加密。

作者：cs4py 專案
"""

from typing import List, Dict
import re


def encrypt(plaintext: str, key: str) -> str:
    """使用維吉尼亞密碼加密
    
    Args:
        plaintext: 明文文字
        key: 密鑰（只使用字母）
    
    Returns:
        密文
    """
    key = re.sub(r'[^A-Za-z]', '', key).upper()
    if not key:
        raise ValueError("密鑰不能為空")
    
    result = []
    key_index = 0
    
    for char in plaintext:
        if char.isalpha():
            # 計算移位值
            shift = ord(key[key_index % len(key)]) - ord('A')
            base = ord('A') if char.isupper() else ord('a')
            encrypted = chr((ord(char) - base + shift) % 26 + base)
            result.append(encrypted)
            key_index += 1
        else:
            result.append(char)
    
    return ''.join(result)


def decrypt(ciphertext: str, key: str) -> str:
    """使用維吉尼亞密碼解密
    
    Args:
        ciphertext: 密文文字
        key: 密鑰（只使用字母）
    
    Returns:
        明文
    """
    key = re.sub(r'[^A-Za-z]', '', key).upper()
    if not key:
        raise ValueError("密鑰不能為空")
    
    result = []
    key_index = 0
    
    for char in ciphertext:
        if char.isalpha():
            # 計算移位值
            shift = ord(key[key_index % len(key)]) - ord('A')
            base = ord('A') if char.isupper() else ord('a')
            decrypted = chr((ord(char) - base - shift) % 26 + base)
            result.append(decrypted)
            key_index += 1
        else:
            result.append(char)
    
    return ''.join(result)


def kasiski_examination(ciphertext: str, max_key_length: int = 20) -> Dict[int, float]:
    """卡西斯基測試：檢測密鑰長度
    
    原理：重複的密文片段可能對應相同的明文序列，它們之間的距離gcd
    可能暗示密鑰長度。
    
    Args:
        ciphertext: 密文文字
        max_key_length: 最大測試的密鑰長度
    
    Returns:
        字典 {密鑰長度: 可能性分數}
    """
    ciphertext_clean = re.sub(r'[^A-Za-z]', '', ciphertext).upper()
    scores = {}
    
    # 尋找重複的3字母序列
    for length in range(3, 6):
        distances = []
        for i in range(len(ciphertext_clean) - length):
            seq = ciphertext_clean[i:i+length]
            # 尋找其他出現位置
            for j in range(i+length, len(ciphertext_clean) - length + 1):
                if ciphertext_clean[j:j+length] == seq:
                    distances.append(j - i)
        
        # 計算各長度的gcd
        if distances:
            for key_len in range(1, max_key_length + 1):
                count = sum(1 for d in distances if d % key_len == 0)
                if key_len not in scores:
                    scores[key_len] = 0
                scores[key_len] += count
    
    # 正規化分數
    total = sum(scores.values()) if scores else 1
    return {k: v/total for k, v in sorted(scores.items())}


def index_of_coincidence(text: str) -> float:
    """計算重合指數（Index of Coincidence）
    
    用於評估文本的隨機性。英文約0.0667，隨機文本約0.0385。
    
    Args:
        text: 輸入文本
    
    Returns:
        重合指數值
    """
    text = re.sub(r'[^A-Za-z]', '', text).upper()
    if len(text) < 2:
        return 0.0
    
    freq = [0] * 26
    for char in text:
        freq[ord(char) - ord('A')] += 1
    
    ic = 0.0
    n = len(text)
    for count in freq:
        ic += count * (count - 1)
    
    return ic / (n * (n - 1)) if n > 1 else 0.0


def find_key_length(ciphertext: str, max_length: int = 20) -> int:
    """使用重合指數法尋找最可能的密鑰長度
    
    Args:
        ciphertext: 密文文字
        max_length: 最大測試長度
    
    Returns:
        最可能的密鑰長度
    """
    ciphertext_clean = re.sub(r'[^A-Za-z]', '', ciphertext).upper()
    best_length = 1
    best_score = 0.0
    
    for key_len in range(1, max_length + 1):
        # 將密文按密鑰位置分組
        groups = ['' for _ in range(key_len)]
        for i, char in enumerate(ciphertext_clean):
            groups[i % key_len] += char
        
        # 計算每組的平均重合指數
        avg_ic = sum(index_of_coincidence(g) for g in groups) / key_len
        
        # 接近英文的重合指數表示可能的密鑰長度
        if avg_ic > best_score:
            best_score = avg_ic
            best_length = key_len
    
    return best_length


def frequency_analysis_at_position(ciphertext: str, position: int, key_length: int) -> str:
    """對特定密鑰位置進行頻率分析，推測該位置的密鑰字母
    
    Args:
        ciphertext: 密文文字
        position: 密鑰位置（0-indexed）
        key_length: 密鑰長度
    
    Returns:
        推測的密鑰字母
    """
    # 英文標準頻率
    english_freq = [
        0.08167, 0.01492, 0.02782, 0.04253, 0.12702, 0.02228, 0.02015,
        0.06094, 0.06966, 0.00153, 0.00772, 0.04025, 0.02406, 0.06749,
        0.07507, 0.01929, 0.00095, 0.05987, 0.06327, 0.09056, 0.02758,
        0.00978, 0.02360, 0.00150, 0.01974, 0.00074
    ]
    
    ciphertext_clean = re.sub(r'[^A-Za-z]', '', ciphertext).upper()
    
    # 收集該位置的字母
    letters = []
    for i, char in enumerate(ciphertext_clean):
        if i % key_length == position:
            letters.append(char)
    
    if not letters:
        return 'A'
    
    total = len(letters)
    best_shift = 0
    best_chi = float('inf')
    
    # 嘗試每個可能的移位
    for shift in range(26):
        observed = [0] * 26
        for char in letters:
            idx = (ord(char) - ord('A') - shift) % 26
            observed[idx] += 1
        
        # 計算卡方統計量
        chi = sum((observed[i] - english_freq[i] * total) ** 2 / (english_freq[i] * total)
                 for i in range(26) if english_freq[i] > 0)
        
        if chi < best_chi:
            best_chi = chi
            best_shift = shift
    
    return chr(best_shift + ord('A'))


def crack(ciphertext: str, max_key_length: int = 20) -> str:
    """破解維吉尼亞密碼，推測密鑰
    
    Args:
        ciphertext: 密文文字
        max_key_length: 最大密鑰長度
    
    Returns:
        推測的密鑰
    """
    # 尋找密鑰長度
    key_length = find_key_length(ciphertext, max_key_length)
    
    # 對每個位置進行頻率分析
    key = ''
    for pos in range(key_length):
        key += frequency_analysis_at_position(ciphertext, pos, key_length)
    
    return key


if __name__ == "__main__":
    print("=== 維吉尼亞密碼演示 ===\n")
    
    # 演示1：基本加密解密
    plaintext = "ATTACK AT DAWN"
    key = "LEMON"
    ciphertext = encrypt(plaintext, key)
    decrypted = decrypt(ciphertext, key)
    
    print(f"明文: {plaintext}")
    print(f"密鑰: {key}")
    print(f"密文: {ciphertext}")
    print(f"解密: {decrypted}")
    print()
    
    # 演示2：密鑰長度檢測
    print("=== 密鑰長度檢測 ===")
    ciphertext = "LXFOPVEFRNHR"
    key_len = find_key_length(ciphertext, 10)
    print(f"密文: {ciphertext}")
    print(f"檢測到密鑰長度: {key_len}")
    print()
    
    # 演示3：重合指數
    print("=== 重合指數 ===")
    english_text = "THETRUTHISRARELYPUREANDNEVERSIMPLE"
    random_text = "XQZJKLMWBCVNTRFGHJKOPLKIHUYTREWQASD"
    print(f"英文文本 IC: {index_of_coincidence(english_text):.4f}")
    print(f"隨機文本 IC: {index_of_coincidence(random_text):.4f}")
    print()
    
    # 演示4：破解演示
    print("=== 破解演示 ===")
    original_text = "THEQUICKBROWNFOXJUMPSOVERTHERAZYDOG"
    key = "SECRET"
    encrypted = encrypt(original_text, key)
    cracked_key = crack(encrypted)
    decrypted = decrypt(encrypted, cracked_key)
    
    print(f"原文: {original_text}")
    print(f"密鑰: {key}")
    print(f"密文: {encrypted}")
    print(f"破解密鑰: {cracked_key}")
    print(f"破解明文: {decrypted}")
