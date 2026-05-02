"""
資訊理論 - 循環冗餘檢查 (CRC)

實作 CRC-8, CRC-32 等多項式檢查碼。
"""

from typing import List, Dict


# 常見 CRC 多項式（正規表示，最高位隱含）
CRC_POLYNOMIALS: Dict[str, int] = {
    'CRC-8': 0x07,      # x^8 + x^2 + x + 1
    'CRC-8-ATM': 0x07,
    'CRC-16-CCITT': 0x1021,  # x^16 + x^12 + x^5 + 1
    'CRC-32': 0x04C11DB7,    # IEEE 802.3
}


def crc_calculate(data: List[int], polynomial: int, width: int) -> int:
    """
    計算 CRC 檢查碼
    
    使用查表法（bit-by-bit 版本）
    
    Args:
        data: 輸入資料位元組列表
        polynomial: 生成多項式（正規形式）
        width: CRC 寬度（位元數）
        
    Returns:
        CRC 值
    """
    # 初始值
    crc = 0
    msb_mask = 1 << (width - 1)
    poly = polynomial
    
    for byte in data:
        for i in range(8):
            bit = (byte >> (7 - i)) & 1
            msb = (crc >> (width - 1)) & 1
            
            crc <<= 1
            if msb ^ bit:
                crc ^= poly
            crc &= (1 << width) - 1  # 保留 width 位
    
    return crc


def crc8(data: List[int]) -> int:
    """CRC-8 計算 (多項式: x^8 + x^2 + x + 1)"""
    return crc_calculate(data, CRC_POLYNOMIALS['CRC-8'], 8)


def crc16_ccitt(data: List[int]) -> int:
    """CRC-16-CCITT 計算"""
    return crc_calculate(data, CRC_POLYNOMIALS['CRC-16-CCITT'], 16)


def crc32(data: List[int]) -> int:
    """CRC-32 計算 (IEEE)"""
    return crc_calculate(data, CRC_POLYNOMIALS['CRC-32'], 32)


def verify_crc(data: List[int], crc_value: int, polynomial: int, width: int) -> bool:
    """
    驗證 CRC
    
    Args:
        data: 資料部分
        crc_value: 附加的 CRC 值
        polynomial: 生成多項式
        width: CRC 寬度
        
    Returns:
        驗證是否通過
    """
    computed = crc_calculate(data, polynomial, width)
    return computed == crc_value


def inject_error(data: List[int], byte_pos: int, bit_pos: int) -> List[int]:
    """
    注入錯誤（用於測試）
    
    Args:
        data: 原資料
        byte_pos: 位元組位置
        bit_pos: 位元位置 (0-7)
        
    Returns:
        包含錯誤的資料
    """
    corrupted = data.copy()
    corrupted[byte_pos] ^= (1 << bit_pos)
    return corrupted


if __name__ == "__main__":
    # 示範：CRC-8
    print("=== CRC-8 示範 ===")
    data = [0x01, 0x02, 0x03, 0x04]
    crc = crc8(data)
    print(f"資料: {[hex(d) for d in data]}")
    print(f"CRC-8: 0x{crc:02X}")
    
    # 驗證
    is_valid = verify_crc(data, crc, CRC_POLYNOMIALS['CRC-8'], 8)
    print(f"驗證結果: {is_valid}")
    
    # 注入錯誤
    corrupted = inject_error(data, 1, 3)
    is_valid = verify_crc(corrupted, crc, CRC_POLYNOMIALS['CRC-8'], 8)
    print(f"錯誤後驗證: {is_valid}")
    
    # 示範：CRC-32
    print("\n=== CRC-32 示範 ===")
    data = [ord(c) for c in "Hello, World!"]
    crc = crc32(data)
    print(f"字串: 'Hello, World!'")
    print(f"CRC-32: 0x{crc:08X}")
    
    # 示範：不同 CRC 標準
    print("\n=== 不同 CRC 標準比較 ===")
    data = [0x12, 0x34, 0x56, 0x78]
    print(f"CRC-8:   0x{crc8(data):02X}")
    print(f"CRC-16:  0x{crc16_ccitt(data):04X}")
    print(f"CRC-32:  0x{crc32(data):08X}")
