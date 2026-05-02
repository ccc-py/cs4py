"""色彩空間轉換 (Color Space Conversions)

實作 RGB、HSV、HSL 色彩空間之間的相互轉換。
這些轉換在影像處理、電腦圖學和色彩管理中廣泛使用。
"""

from typing import Tuple


def clamp(value: float, min_val: float = 0.0, max_val: float = 1.0) -> float:
    """限制數值範圍"""
    return max(min_val, min(max_val, value))


def rgb_to_hsv(r: float, g: float, b: float) -> Tuple[float, float, float]:
    """RGB 轉 HSV
    
    Args:
        r, g, b: RGB 值 (0.0 ~ 1.0)
    
    Returns:
        (h, s, v): 色相 (0~360), 飽和度 (0~1), 明度 (0~1)
    """
    r, g, b = clamp(r), clamp(g), clamp(b)
    
    max_c = max(r, g, b)
    min_c = min(r, g, b)
    diff = max_c - min_c
    
    # 計算色相 H
    h = 0.0
    if diff != 0:
        if max_c == r:
            h = (60 * ((g - b) / diff) + 360) % 360
        elif max_c == g:
            h = 60 * ((b - r) / diff) + 120
        else:  # max_c == b
            h = 60 * ((r - g) / diff) + 240
    
    # 計算飽和度 S
    s = 0.0 if max_c == 0 else diff / max_c
    
    # 明度 V
    v = max_c
    
    return (h, s, v)


def hsv_to_rgb(h: float, s: float, v: float) -> Tuple[float, float, float]:
    """HSV 轉 RGB
    
    Args:
        h: 色相 (0~360)
        s: 飽和度 (0~1)
        v: 明度 (0~1)
    
    Returns:
        (r, g, b): RGB 值 (0.0 ~ 1.0)
    """
    h = h % 360
    s, v = clamp(s), clamp(v)
    
    c = v * s
    x = c * (1 - abs((h / 60) % 2 - 1))
    m = v - c
    
    if h < 60:
        r, g, b = c, x, 0
    elif h < 120:
        r, g, b = x, c, 0
    elif h < 180:
        r, g, b = 0, c, x
    elif h < 240:
        r, g, b = 0, x, c
    elif h < 300:
        r, g, b = x, 0, c
    else:
        r, g, b = c, 0, x
    
    return (r + m, g + m, b + m)


def rgb_to_hsl(r: float, g: float, b: float) -> Tuple[float, float, float]:
    """RGB 轉 HSL
    
    Args:
        r, g, b: RGB 值 (0.0 ~ 1.0)
    
    Returns:
        (h, s, l): 色相 (0~360), 飽和度 (0~1), 亮度 (0~1)
    """
    r, g, b = clamp(r), clamp(g), clamp(b)
    
    max_c = max(r, g, b)
    min_c = min(r, g, b)
    diff = max_c - min_c
    
    # 亮度 L
    l = (max_c + min_c) / 2
    
    # 飽和度 S
    s = 0.0
    if diff != 0:
        s = diff / (1 - abs(2 * l - 1)) if l != 0.5 else 0
        s = clamp(s)
    
    # 色相 H（與 HSV 相同）
    h = 0.0
    if diff != 0:
        if max_c == r:
            h = (60 * ((g - b) / diff) + 360) % 360
        elif max_c == g:
            h = 60 * ((b - r) / diff) + 120
        else:
            h = 60 * ((r - g) / diff) + 240
    
    return (h, s, l)


def hsl_to_rgb(h: float, s: float, l: float) -> Tuple[float, float, float]:
    """HSL 轉 RGB
    
    Args:
        h: 色相 (0~360)
        s: 飽和度 (0~1)
        l: 亮度 (0~1)
    
    Returns:
        (r, g, b): RGB 值 (0.0 ~ 1.0)
    """
    h = h % 360
    s, l = clamp(s), clamp(l)
    
    c = (1 - abs(2 * l - 1)) * s
    x = c * (1 - abs((h / 60) % 2 - 1))
    m = l - c / 2
    
    if h < 60:
        r, g, b = c, x, 0
    elif h < 120:
        r, g, b = x, c, 0
    elif h < 180:
        r, g, b = 0, c, x
    elif h < 240:
        r, g, b = 0, x, c
    elif h < 300:
        r, g, b = x, 0, c
    else:
        r, g, b = c, 0, x
    
    return (r + m, g + m, b + m)


def rgb_to_hex(r: float, g: float, b: float) -> str:
    """RGB 轉十六進位顏色碼
    
    Args:
        r, g, b: RGB 值 (0.0 ~ 1.0)
    
    Returns:
        十六進位字串，如 '#FF8000'
    """
    ri, gi, bi = int(clamp(r) * 255), int(clamp(g) * 255), int(clamp(b) * 255)
    return f'#{ri:02X}{gi:02X}{bi:02X}'


if __name__ == "__main__":
    print("色彩空間轉換演示")
    print("=" * 40)
    
    # 演示 1: 純紅色
    print("\n1. 純紅色 (#FF0000):")
    r, g, b = 1.0, 0.0, 0.0
    h, s, v = rgb_to_hsv(r, g, b)
    h2, s2, l = rgb_to_hsl(r, g, b)
    print(f"   RGB: ({r}, {g}, {b})")
    print(f"   HSV: ({h:.1f}°, {s:.2f}, {v:.2f})")
    print(f"   HSL: ({h2:.1f}°, {s2:.2f}, {l:.2f})")
    print(f"   Hex: {rgb_to_hex(r, g, b)}")
    
    # 演示 2: 還原檢查
    print("\n2. 轉換還原測試:")
    r_new, g_new, b_new = hsv_to_rgb(h, s, v)
    print(f"   HSV→RGB: ({r_new:.2f}, {g_new:.2f}, {b_new:.2f})")
    
    r_new2, g_new2, b_new2 = hsl_to_rgb(h2, s2, l)
    print(f"   HSL→RGB: ({r_new2:.2f}, {g_new2:.2f}, {b_new2:.2f})")
    
    # 演示 3: 不同顏色
    print("\n3. 不同顏色測試:")
    colors = [
        ("紅色", 1.0, 0.0, 0.0),
        ("綠色", 0.0, 1.0, 0.0),
        ("藍色", 0.0, 0.0, 1.0),
        ("黃色", 1.0, 1.0, 0.0),
        ("紫色", 0.5, 0.0, 0.5),
    ]
    for name, r, g, b in colors:
        h, s, v = rgb_to_hsv(r, g, b)
        print(f"   {name}: HSV({h:.0f}°, {s:.1f}, {v:.1f}) -> {rgb_to_hex(r, g, b)}")
