# 基礎光線追蹤 (Basic Ray Tracing)

## 歷史背景

光線追蹤（Ray Tracing）由 Arthur Appel 在 1969 年首次提出，後來由 Turner Whitted 在 1980 年擴展為包含反射和折射的完整模型。**光線追蹤**模擬光線在場景中的傳播路徑，能夠產生高度真實的影像，包括軟陰影、反射、折射等效果。近年來，隨著硬體加速（如 NVIDIA RTX）的發展，即時光線追蹤已成為遊戲和電影的主流技術。

## 核心原理

### 光線追蹤基本概念

光線追蹤從相機位置發射光線穿過每個像素，追蹤光線與場景中物體的交互：

1. **光線生成**：從相機發射光線穿過視平面
2. **相交測試**：計算光線與最近物體的交點
3. **著色計算**：根據光照模型計算像素顏色
4. **遞迴追蹤**：處理反射和折射（可選）

### 光線-球體相交

球體方程：`(P - C) · (P - C) = r²`  
光線方程：`P(t) = O + tD`

代入後得到二次方程：
```
at² + bt + c = 0
其中:
a = D·D
b = 2(O-C)·D
c = (O-C)·(O-C) - r²
```

判別式 `Δ = b² - 4ac`：
- Δ < 0：無交點
- Δ ≥ 0：有交點，取最小的 t > 0

### 漫射著色（Lambert 模型）

```
I = I_ambient + I_diffuse * max(0, N·L)
```
- N：表面法向量
- L：指向光源的向量

## 使用範例

```python
from render.ray_tracing import Vec3, Sphere, Ray, trace_ray

# 建立場景
spheres = [
    Sphere(Vec3(0, 0, 0), 1.0, (1, 0, 0)),  # 紅球
    Sphere(Vec3(3, 0, 2), 1.5, (0, 1, 0)),  # 綠球
]
lights = [Vec3(5, 10, -5)]

# 追蹤一條光線
ray = Ray(Vec3(0, 0, -5), Vec3(0, 0, 1))
color = trace_ray(ray, spheres, lights)
print(f"顏色: {color}")
```

## 參考資料

- Whitted, T. (1980). "An improved illumination model for shaded display". *Communications of the ACM*, 23(6), 343-349.
- [Wikipedia: Ray tracing (graphics)](https://en.wikipedia.org/wiki/Ray_tracing_(graphics))
- Shirley, P., & Morley, R. K. (2003). *Realistic Ray Tracing* (2nd ed.). A K Peters.
