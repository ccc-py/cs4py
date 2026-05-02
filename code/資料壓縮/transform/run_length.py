"""
行程長度編碼 (Run-Length Encoding, RLE)

最簡單的無損壓縮演算法之一，用於壓縮連續重複的資料。
將 "AAAAABBB" 編碼為 "A5B3"（5個A，3個B）。
常用於圖片壓縮（如 BMP、TIFF）和簡單資料壓縮。
"""

from typing import List, Tuple, Union


def encode(data: str) -> str:
    """
    RLE 編碼（字串版本）
    
    Args:
        data: 要壓縮的字串
        
    Returns:
        壓縮後的字串，格式為 "字元次數字元次數..."
    """
    if not data:
        return ""

    result = []
    current_char = data[0]
    count = 1

    for char in data[1:]:
        if char == current_char:
            count += 1
        else:
            result.append(f"{current_char}{count}")
            current_char = char
            count = 1

    # 處理最後一個
    result.append(f"{current_char}{count}")

    return ''.join(result)


def decode(encoded: str) -> str:
    """
    RLE 解碼（字串版本）
    
    Args:
        encoded: 壓縮後的字串
        
    Returns:
        解壓後的原始字串
    """
    result = []
    i = 0

    while i < len(encoded):
        char = encoded[i]
        i += 1
        # 讀取數字
        count_str = ""
        while i < len(encoded) and encoded[i].isdigit():
            count_str += encoded[i]
            i += 1
        count = int(count_str) if count_str else 1
        result.append(char * count)

    return ''.join(result)


def encode_binary(data: List[int], threshold: int = 3) -> List[Union[int, Tuple[int, int]]]:
    """
    RLE 編碼（二進制資料版本，適用於圖片）
    
    Args:
        data: 二進制資料列表（0 和 1，或 0-255 的灰階值）
        threshold: 最小行程長度才壓縮
        
    Returns:
        壓縮後的列表，重複部分用 (值, 次數) 表示
    """
    if not data:
        return []

    result = []
    current = data[0]
    count = 1

    for value in data[1:]:
        if value == current:
            count += 1
        else:
            if count >= threshold:
                result.append((current, count))
            else:
                # 不足 threshold 的部分直接輸出
                result.extend([current] * count)
            current = value
            count = 1

    # 處理最後一個
    if count >= threshold:
        result.append((current, count))
    else:
        result.extend([current] * count)

    return result


def decode_binary(encoded: List[Union[int, Tuple[int, int]]]) -> List[int]:
    """
    RLE 解碼（二進制資料版本）
    
    Args:
        encoded: 壓縮後的列表
        
    Returns:
        解壓後的原始資料列表
    """
    result = []
    for item in encoded:
        if isinstance(item, tuple):
            value, count = item
            result.extend([value] * count)
        else:
            result.append(item)
    return result


def encode_image(pixels: List[int], width: int) -> str:
    """
    簡單的圖片 RLE 編碼（每行獨立編碼）
    
    Args:
        pixels: 圖片的像素值列表（灰階 0-255）
        width: 圖片寬度
        
    Returns:
        壓縮後的字串
    """
    result = []

    for row_start in range(0, len(pixels), width):
        row = pixels[row_start:row_start + width]
        encoded_row = encode_binary(row)
        # 將編碼結果轉為字串
        row_str = ','.join(
            f"{v}:{c}" if isinstance(v, tuple) else str(v)
            for v in encoded_row
        )
        result.append(row_str)

    return ';'.join(result)


def decode_image(encoded: str, width: int) -> List[int]:
    """
    簡單的圖片 RLE 解碼
    
    Args:
        encoded: 壓縮後的字串
        width: 圖片寬度（此處未使用，僅為介面一致）
        
    Returns:
        解壓後的像素列表
    """
    result = []
    rows = encoded.split(';')

    for row_str in rows:
        row_data = []
        parts = row_str.split(',')
        for part in parts:
            if ':' in part:
                value, count = part.split(':')
                row_data.extend([int(value)] * int(count))
            else:
                row_data.append(int(part))
        result.extend(row_data)

    return result


if __name__ == "__main__":
    # 示範 RLE 壓縮（字串）
    sample_text = "AAAAABBBBCCCCCCDDDDEEEE"
    print(f"原始文字: {sample_text}")
    print(f"原始長度: {len(sample_text)} 字元\n")

    # 壓縮
    encoded = encode(sample_text)
    print(f"RLE 壓縮後: {encoded}")
    print(f"壓縮後長度: {len(encoded)}")
    print(f"壓縮率: {len(encoded)/len(sample_text)*100:.1f}%\n")

    # 解壓縮
    decoded = decode(encoded)
    print(f"解壓後文字: {decoded}")
    print(f"解壓是否正確: {decoded == sample_text}")

    # 示範二進制資料 RLE
    print("\n" + "="*50 + "\n")
    binary_data = [1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0, 0]
    print(f"二進制資料: {binary_data}")

    encoded_bin = encode_binary(binary_data, threshold=3)
    print(f"RLE 壓縮後: {encoded_bin}")

    decoded_bin = decode_binary(encoded_bin)
    print(f"解壓後: {decoded_bin}")
    print(f"解壓是否正確: {decoded_bin == binary_data}")

    # 示範圖片壓縮
    print("\n" + "="*50 + "\n")
    # 一個簡單的 4x4 灰階圖片（0=黑，255=白）
    image = [
        255, 255, 255, 255,
        255, 0, 0, 255,
        255, 0, 0, 255,
        255, 255, 255, 255
    ]
    print(f"4x4 圖片資料: {image}")

    encoded_img = encode_image(image, width=4)
    print(f"RLE 圖片壓縮後: {encoded_img}")

    decoded_img = decode_image(encoded_img, width=4)
    print(f"解壓是否正確: {decoded_img == image}")
