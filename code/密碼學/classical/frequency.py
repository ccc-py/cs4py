"""
頻率分析 (Frequency Analysis)

歷史背景：
9世紀阿拉伯學者肯迪（Al-Kindi）在《破解加密信息的方法》一書中首次
系統性地描述了頻率分析技術。他發現阿拉伯語中某些字母出現頻率較高，
通過匹配密文與明文的頻率分佈可以破解替換密碼。

原理：
自然語言中字母的出現頻率呈現特定的分佈模式。英文中E最常見（約12.7%），
其次是T、A、O、I、N等。通過計算觀察頻率與標準頻率的匹配度
（如卡方統計量），可以推測替換規則或密鑰。

作者：cs4py 專案
"""

from typing import List, Tuple, Dict
import re


# 英文標準頻率表（A-Z），來源：Oxford Languages
ENGLISH_FREQUENCIES = [
    0.08167, 0.01492, 0.02782, 0.04253, 0.12702, 0.02228, 0.02015,
    0.06094, 0.06966, 0.00153, 0.00772, 0.04025, 0.02406, 0.06749,
    0.07507, 0.01929, 0.00095, 0.05987, 0.06327, 0.09056, 0.02758,
    0.00978, 0.02360, 0.00150, 0.01974, 0.00074
]

# 字母標籤
LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'


def get_frequencies(text: str) -> List[float]:
    """計算文本中字母的相對頻率
    
    Args:
        text: 輸入文本
    
    Returns:
        長度26的列表，包含A-Z的相對頻率
    """
    text = re.sub(r'[^A-Za-z]', '', text).upper()
    freq = [0] * 26
    
    if not text:
        return freq
    
    for char in text:
        freq[ord(char) - ord('A')] += 1
    
    total = len(text)
    return [count / total for count in freq]


def chi_squared(observed: List[float], expected: List[float]) -> float:
    """計算卡方統計量（Chi-squared statistic）
    
    用於衡量觀察頻率與期望頻率的偏差程度。
    公式：χ² = Σ((O_i - E_i)² / E_i)
    
    Args:
        observed: 觀察頻率（絕對次數）
        expected: 期望頻率（相對頻率）
    
    Returns:
        卡方統計量值
    """
    if len(observed) != 26 or len(expected) != 26:
        raise ValueError("頻率列表長度必須為26")
    
    total = sum(observed)
    if total == 0:
        return 0.0
    
    chi = 0.0
    for i in range(26):
        exp_count = expected[i] * total
        if exp_count > 0:
            chi += (observed[i] - exp_count) ** 2 / exp_count
    
    return chi


def crack_caesar(ciphertext: str) -> int:
    """破解凱薩密碼，返回最可能的移位值
    
    Args:
        ciphertext: 密文文字
    
    Returns:
        最可能的移位值（0-25）
    """
    ciphertext_clean = re.sub(r'[^A-Za-z]', '', ciphertext).upper()
    if not ciphertext_clean:
        return 0
    
    total = len(ciphertext_clean)
    best_shift = 0
    best_chi = float('inf')
    
    # 對每個可能的移位計算卡方統計量
    for shift in range(26):
        observed = [0] * 26
        for char in ciphertext_clean:
            idx = (ord(char) - ord('A') - shift) % 26
            observed[idx] += 1
        
        chi = chi_squared(observed, ENGLISH_FREQUENCIES)
        
        if chi < best_chi:
            best_chi = chi
            best_shift = shift
    
    return best_shift


def crack_substitution(ciphertext: str) -> Dict[str, str]:
    """嘗試破解簡單替換密碼
    
    使用頻率分析匹配最可能的替換規則。
    
    Args:
        ciphertext: 密文文字
    
    Returns:
        替換映射表 {密文字母: 明文字母}
    """
    ciphertext_clean = re.sub(r'[^A-Za-z]', '', ciphertext).upper()
    observed_freq = get_frequencies(ciphertext_clean)
    
    # 將觀察頻率和標準頻率排序
    obs_sorted = sorted(enumerate(observed_freq), key=lambda x: x[1], reverse=True)
    std_sorted = sorted(enumerate(ENGLISH_FREQUENCIES), key=lambda x: x[1], reverse=True)
    
    # 建立映射（頻率最高的對應頻率最高的）
    mapping = {}
    for (obs_idx, _), (std_idx, _) in zip(obs_sorted, std_sorted):
        mapping[LETTERS[obs_idx]] = LETTERS[std_idx]
    
    return mapping


def apply_mapping(ciphertext: str, mapping: Dict[str, str]) -> str:
    """應用替換映射解密文本
    
    Args:
        ciphertext: 密文
        mapping: 替換映射表
    
    Returns:
        解密後的文本
    """
    result = []
    for char in ciphertext:
        if char.upper() in mapping:
            mapped = mapping[char.upper()]
            result.append(mapped if char.isupper() else mapped.lower())
        else:
            result.append(char)
    return ''.join(result)


def print_frequency_table(freq: List[float]) -> None:
    """打印頻率表
    
    Args:
        freq: 頻率列表
    """
    print("字母 | 頻率")
    print("-" * 20)
    for i, f in enumerate(freq):
        print(f"{LETTERS[i]:2s}   | {f:.4f} ({f*100:5.2f}%)")


if __name__ == "__main__":
    print("=== 頻率分析演示 ===\n")
    
    # 演示1：英文頻率表
    print("英文標準頻率表（前10個字母）:")
    print_frequency_table(ENGLISH_FREQUENCIES[:10])
    print()
    
    # 演示2：計算文本頻率
    print("=== 文本頻率分析 ===")
    text = "THE QUICK BROWN FOX JUMPS OVER THE LAZY DOG"
    freq = get_frequencies(text)
    print(f"文本: {text}")
    print("頻率分析:")
    print_frequency_table(freq)
    print()
    
    # 演示3：卡方統計量
    print("=== 卡方統計量演示 ===")
    # 模擬觀察數據
    observed = [int(f * 1000) for f in ENGLISH_FREQUENCIES]
    chi = chi_squared(observed, ENGLISH_FREQUENCIES)
    print(f"標準英文的卡方值: {chi:.2f} (應該接近0)")
    
    # 隨機分佈的卡方值
    random_obs = [38] * 26  # 均勻分佈
    chi_random = chi_squared(random_obs, ENGLISH_FREQUENCIES)
    print(f"隨機分佈的卡方值: {chi_random:.2f} (應該很大)")
    print()
    
    # 演示4：破解凱薩密碼
    print("=== 破解凱薩密碼 ===")
    original = "HELLO WORLD"
    shift = 7
    encrypted = ""
    for char in original:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            encrypted += chr((ord(char) - base + shift) % 26 + base)
        else:
            encrypted += char
    
    print(f"原文: {original}")
    print(f"加密(shift={shift}): {encrypted}")
    cracked_shift = crack_caesar(encrypted)
    print(f"破解的移位值: {cracked_shift}")
    print()
    
    # 演示5：長文本頻率分析
    print("=== 長文本頻率分析 ===")
    long_text = """
    TO BE OR NOT TO BE THAT IS THE QUESTION
    WHETHER TIS NOBLER IN THE MIND TO SUFFER
    THE SLINGS AND ARROWS OF OUTRAGEOUS FORTUNE
    """
    freq = get_frequencies(long_text)
    print("頻率最高的5個字母:")
    sorted_freq = sorted(enumerate(freq), key=lambda x: x[1], reverse=True)
    for idx, f in sorted_freq[:5]:
        print(f"  {LETTERS[idx]}: {f:.4f}")
