"""
離散餘弦轉換 (Discrete Cosine Transform, DCT)

DCT 是 JPEG 圖片壓縮的核心演算法。
它將圖片從空間域轉換到頻率域，使得大部分能量集中在左上角的低頻係數，
從而可以通過量化和熵編碼實現高壓縮比。

本實作使用 2D DCT-II（最常用的形式），對 8x8 區塊進行處理。
"""

from typing import List, List as ListType
import math


def dct_1d(signal: ListType[float]) -> ListType[float]:
    """
    一維 DCT-II 轉換
    
    Args:
        signal: 輸入信號（長度為 N）
        
    Returns:
        DCT 係數列表
    """
    N = len(signal)
    result = []

    for k in range(N):
        # 計算第 k 個 DCT 係數
        coeff = 0.0
        for n in range(N):
            coeff += signal[n] * math.cos(math.pi * k * (2 * n + 1) / (2 * N))
        # 歸一化因子
        ck = math.sqrt(1 / N) if k == 0 else math.sqrt(2 / N)
        result.append(ck * coeff)

    return result


def idct_1d(coeffs: ListType[float]) -> ListType[float]:
    """
    一維反 DCT（Inverse DCT）
    
    Args:
        coeffs: DCT 係數列表
        
    Returns:
        重建的信號
    """
    N = len(coeffs)
    result = []

    for n in range(N):
        # 計算第 n 個重建值
        value = 0.0
        for k in range(N):
            ck = math.sqrt(1 / N) if k == 0 else math.sqrt(2 / N)
            value += ck * coeffs[k] * math.cos(math.pi * k * (2 * n + 1) / (2 * N))
        result.append(value)

    return result


def dct_2d(block: ListType[ListType[float]]) -> ListType[ListType[float]]:
    """
    二維 DCT-II 轉換（對 8x8 區塊）
    
    Args:
        block: 8x8 的二維列表（像素值）
        
    Returns:
        8x8 的 DCT 係數矩陣
    """
    N = len(block)
    # 先對每行做 1D DCT
    row_dct = []
    for row in block:
        row_dct.append(dct_1d(row))

    # 再對每列做 1D DCT
    result = []
    for i in range(N):
        column = [row_dct[j][i] for j in range(N)]
        result.append(dct_1d(column))

    # 轉置回正確的形式
    final = []
    for i in range(N):
        final.append([result[j][i] for j in range(N)])

    return final


def idct_2d(coeffs: ListType[ListType[float]]) -> ListType[ListType[float]]:
    """
    二維反 DCT
    
    Args:
        coeffs: 8x8 的 DCT 係數矩陣
        
    Returns:
        重建的 8x8 像素區塊
    """
    N = len(coeffs)
    # 先對每行做反 DCT
    row_idct = []
    for row in coeffs:
        row_idct.append(idct_1d(row))

    # 再對每列做反 DCT
    result = []
    for i in range(N):
        column = [row_idct[j][i] for j in range(N)]
        result.append(idct_1d(column))

    # 轉置回正確的形式
    final = []
    for i in range(N):
        final.append([result[j][i] for j in range(N)])

    return final


def quantize(coeffs: ListType[ListType[float]], quality: int = 50) -> ListType[ListType[int]]:
    """
    JPEG 量化：將 DCT 係數除以量化表並取整
    
    Args:
        coeffs: DCT 係數矩陣
        quality: 品質因子（1-100，50 為標準）
        
    Returns:
        量化後的整數係數
    """
    # JPEG 標準的亮度量化表（品質 50）
    q_table = [
        [16, 11, 10, 16, 24, 40, 51, 61],
        [12, 12, 14, 19, 26, 58, 60, 55],
        [14, 13, 16, 24, 40, 57, 69, 56],
        [14, 17, 22, 29, 51, 87, 80, 62],
        [18, 22, 37, 56, 68, 109, 103, 77],
        [24, 35, 55, 64, 81, 104, 113, 92],
        [49, 64, 78, 87, 103, 121, 120, 101],
        [72, 92, 95, 98, 112, 100, 103, 99]
    ]

    # 根據品質調整量化表
    if quality != 50:
        scale = 5000 / quality if quality < 50 else 200 - 2 * quality
        q_table = [[max(1, int((q * scale + 50) / 100)) for q in row] for row in q_table]

    N = len(coeffs)
    result = []
    for i in range(N):
        row = []
        for j in range(N):
            # 量化：係數除以量化表中的對應值
            quantized = round(coeffs[i][j] / q_table[i][j])
            row.append(int(quantized))
        result.append(row)

    return result


def dequantize(coeffs: ListType[ListType[int]], quality: int = 50) -> ListType[ListType[float]]:
    """
    反量化：將量化後的係數乘回量化表
    
    Args:
        coeffs: 量化後的整數係數
        quality: 品質因子
        
    Returns:
        反量化後的 DCT 係數
    """
    q_table = [
        [16, 11, 10, 16, 24, 40, 51, 61],
        [12, 12, 14, 19, 26, 58, 60, 55],
        [14, 13, 16, 24, 40, 57, 69, 56],
        [14, 17, 22, 29, 51, 87, 80, 62],
        [18, 22, 37, 56, 68, 109, 103, 77],
        [24, 35, 55, 64, 81, 104, 113, 92],
        [49, 64, 78, 87, 103, 121, 120, 101],
        [72, 92, 95, 98, 112, 100, 103, 99]
    ]

    if quality != 50:
        scale = 5000 / quality if quality < 50 else 200 - 2 * quality
        q_table = [[max(1, int((q * scale + 50) / 100)) for q in row] for row in q_table]

    N = len(coeffs)
    result = []
    for i in range(N):
        row = []
        for j in range(N):
            row.append(coeffs[i][j] * q_table[i][j])
        result.append(row)

    return result


def compress_block(block: ListType[ListType[float]], quality: int = 50) -> ListType[ListType[int]]:
    """
    完整的區塊壓縮流程：DCT + 量化
    
    Args:
        block: 8x8 像素區塊（值範圍 0-255）
        quality: 品質因子
        
    Returns:
        量化後的 DCT 係數
    """
    # 將像素值移至以 0 為中心（JPEG 標準做法）
    centered = [[pixel - 128.0 for pixel in row] for row in block]

    # DCT 轉換
    coeffs = dct_2d(centered)

    # 量化
    quantized = quantize(coeffs, quality)

    return quantized


def decompress_block(coeffs: ListType[ListType[int]], quality: int = 50) -> ListType[ListType[float]]:
    """
    完整的區塊解壓縮流程：反量化 + 反 DCT
    
    Args:
        coeffs: 量化後的 DCT 係數
        quality: 品質因子
        
    Returns:
        重建的 8x8 像素區塊
    """
    # 反量化
    dequant = dequantize(coeffs, quality)

    # 反 DCT
    centered = idct_2d(dequant)

    # 將像素值移回 0-255 範圍
    block = [[pixel + 128.0 for pixel in row] for row in centered]

    # 裁剪到有效範圍並取整
    block = [[max(0, min(255, round(pixel))) for pixel in row] for row in block]

    return block


def print_matrix(matrix: ListType[ListType[float]], precision: int = 2) -> None:
    """
    列印矩陣（用於除錯）
    
    Args:
        matrix: 要列印的矩陣
        precision: 小數點位數
    """
    for row in matrix:
        print(' '.join(f"{v:>{precision+4}.{precision}f}" for v in row))


if __name__ == "__main__":
    # 示範 DCT 壓縮
    print("DCT 圖片壓縮示範")
    print("="*50)

    # 建立一個簡單的 8x8 測試區塊（漸層）
    print("\n1. 原始 8x8 區塊（漸層）:")
    block = []
    for i in range(8):
        row = []
        for j in range(8):
            # 建立一個簡單的漸層圖案
            value = i * 32 + j * 4
            row.append(float(value))
        block.append(row)
    print_matrix(block, precision=1)

    # DCT 轉換
    print("\n2. DCT 係數（能量集中在左上角）:")
    centered = [[pixel - 128.0 for pixel in row] for row in block]
    dct_coeffs = dct_2d(centered)
    print_matrix(dct_coeffs, precision=1)

    # 量化
    print("\n3. 量化後的係數（高頻被捨棄）:")
    quantized = quantize(dct_coeffs, quality=50)
    print_matrix(quantized, precision=0)

    # 反量化 + 反 DCT
    print("\n4. 重建後的區塊:")
    dequant = dequantize(quantized, quality=50)
    reconstructed = idct_2d(dequant)
    reconstructed = [[pixel + 128.0 for pixel in row] for row in reconstructed]
    reconstructed = [[max(0, min(255, round(p))) for p in row] for row in reconstructed]
    print_matrix(reconstructed, precision=1)

    # 計算誤差
    print("\n5. 壓縮誤差分析:")
    total_error = 0
    for i in range(8):
        for j in range(8):
            error = abs(block[i][j] - reconstructed[i][j])
            total_error += error
    print(f"總誤差: {total_error:.2f}")
    print(f"平均誤差: {total_error/64:.2f}")

    # 完整壓縮流程
    print("\n" + "="*50)
    print("\n完整壓縮/解壓縮流程:")
    quantized2 = compress_block(block, quality=75)
    print(f"壓縮後係數數量: {sum(1 for row in quantized2 for c in row if c != 0)} / 64")
    reconstructed2 = decompress_block(quantized2, quality=75)
    print(f"解壓後驗證: {all(abs(block[i][j] - reconstructed2[i][j]) < 10 for i in range(8) for j in range(8))}")
