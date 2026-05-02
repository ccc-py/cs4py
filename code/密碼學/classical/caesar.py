"""
凱薩密碼 (Caesar Cipher)

歷史背景：
凱薩密碼是最古老的替換密碼之一，由羅馬共和國的凱薩大帝（Julius Caesar）用於
軍事通信。他將每個字母向右移動固定位置來加密信息，通常移位為3。

原理：
將明文中的每個字母按照字母表順序移位固定數量。例如移位3時，A→D, B→E, ..., Z→C。
解密時將密文字母反向移位。

作者：cs4py 專案
"""

from typing import List, Tuple


def encrypt(plaintext: str, shift: int) -> str:
    """加密明文
    
    Args:
        plaintext: 明文文字
        shift: 移位數量 (0-25)
    
    Returns:
        密文
    """
    shift = shift % 26
    result = []
    
    for char in plaintext:
        if char.isalpha():
            # 判斷是否為大寫字母
            base = ord('A') if char.isupper() else ord('a')
            # 移位加密
            encrypted = chr((ord(char) - base + shift) % 26 + base)
            result.append(encrypted)
        else:
            # 非字母字符保持不變
            result.append(char)
    
    return ''.join(result)


def decrypt(ciphertext: str, shift: int) -> str:
    """解密密文
    
    Args:
        ciphertext: 密文文字
        shift: 移位數量 (0-25)
    
    Returns:
        明文
    """
    # 解密即為反向移位
    return encrypt(ciphertext, -shift)


def brute_force(ciphertext: str) -> List[Tuple[int, str]]:
    """暴力破解：嘗試所有25種移位
    
    Args:
        ciphertext: 密文文字
    
    Returns:
        所有移位對應的解密結果列表
    """
    results = []
    for shift in range(26):
        decrypted = decrypt(ciphertext, shift)
        results.append((shift, decrypted))
    return results


def frequency_analysis(ciphertext: str) -> int:
    """使用頻率分析自動檢測最可能的移位
    
    原理：英文中字母E出現頻率最高（約12.7%），通過比較密文與標準頻率分佈
    來找出最可能的移位值。
    
    Args:
        ciphertext: 密文文字
    
    Returns:
        最可能的移位值
    """
    # 英文標準頻率表（A-Z）
    english_freq = [
        0.08167, 0.01492, 0.02782, 0.04253, 0.12702, 0.02228, 0.02015,
        0.06094, 0.06966, 0.00153, 0.00772, 0.04025, 0.02406, 0.06749,
        0.07507, 0.01929, 0.00095, 0.05987, 0.06327, 0.09056, 0.02758,
        0.00978, 0.02360, 0.00150, 0.01974, 0.00074
    ]
    
    # 計算密文字母頻率
    ciphertext_clean = ''.join(c.upper() for c in ciphertext if c.isalpha())
    if not ciphertext_clean:
        return 0
    
    total = len(ciphertext_clean)
    chi_squared_min = float('inf')
    best_shift = 0
    
    # 對每個可能的移位計算卡方統計量
    for shift in range(26):
        chi_squared = 0.0
        observed = [0] * 26
        
        # 計算移位後的觀察頻率
        for char in ciphertext_clean:
            idx = (ord(char) - ord('A') - shift) % 26
            observed[idx] += 1
        
        # 計算卡方統計量
        for i in range(26):
            expected = english_freq[i] * total
            if expected > 0:
                chi_squared += ((observed[i] - expected) ** 2) / expected
        
        if chi_squared < chi_squared_min:
            chi_squared_min = chi_squared
            best_shift = shift
    
    return best_shift


def crack(ciphertext: str) -> Tuple[int, str]:
    """破解凱薩密碼，返回移位值和明文
    
    Args:
        ciphertext: 密文文字
    
    Returns:
        元組 (移位值, 明文)
    """
    shift = frequency_analysis(ciphertext)
    plaintext = decrypt(ciphertext, shift)
    return shift, plaintext


if __name__ == "__main__":
    # 演示1：基本加密解密
    print("=== 凱薩密碼演示 ===\n")
    
    plaintext = "HELLO WORLD"
    shift = 3
    ciphertext = encrypt(plaintext, shift)
    decrypted = decrypt(ciphertext, shift)
    
    print(f"明文: {plaintext}")
    print(f"移位: {shift}")
    print(f"密文: {ciphertext}")
    print(f"解密: {decrypted}")
    print()
    
    # 演示2：暴力破解
    print("=== 暴力破解演示 ===")
    ciphertext = "KHOOR ZRUOG"
    results = brute_force(ciphertext)
    for shift, text in results[:5]:  # 只顯示前5個
        print(f"移位 {shift:2d}: {text}")
    print("...")
    print()
    
    # 演示3：頻率分析自動破解
    print("=== 頻率分析自動破解 ===")
    ciphertext = "XLMW MW E GEIWEV GMTLIV"
    shift, plaintext = crack(ciphertext)
    print(f"密文: {ciphertext}")
    print(f"檢測到移位: {shift}")
    print(f"破解明文: {plaintext}")
    print()
    
    # 演示4：英文句子加密
    print("=== 英文句子加密 ===")
    message = "The quick brown fox jumps over the lazy dog"
    encrypted = encrypt(message, 7)
    decrypted = decrypt(encrypted, 7)
    print(f"原文: {message}")
    print(f"加密: {encrypted}")
    print(f"解密: {decrypted}")
