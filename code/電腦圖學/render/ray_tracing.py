"""基礎光線追蹤 (Basic Ray Tracing)

實作基礎光線追蹤演算法，包含光線-球體相交、反射和漫射著色。
輸出 PPM 格式影像檔案。
"""

from typing import List, Tuple, Optional
import math


class Vec3:
    """3D 向量類別"""
    def __init__(self, x: float, y: float, z: float):
        self.x, self.y, self.z = x, y, z
    
    def __add__(self, other: 'Vec3') -> 'Vec3':
        return Vec3(self.x + other.x, self.y + other.y, self.z + other.z)
    
    def __sub__(self, other: 'Vec3') -> 'Vec3':
        return Vec3(self.x - other.x, self.y - other.y, self.z - other.z)
    
    def __mul__(self, t: float) -> 'Vec3':
        return Vec3(self.x * t, self.y * t, self.z * t)
    
    def dot(self, other: 'Vec3') -> float:
        return self.x * other.x + self.y * other.y + self.z * other.z
    
    def length(self) -> float:
        return math.sqrt(self.dot(self))
    
    def normalize(self) -> 'Vec3':
        l = self.length()
        return Vec3(self.x/l, self.y/l, self.z/l) if l > 0 else self


class Ray:
    """光線類別"""
    def __init__(self, origin: Vec3, direction: Vec3):
        self.origin = origin
        self.direction = direction.normalize()


class Sphere:
    """球體類別"""
    def __init__(self, center: Vec3, radius: float, color: Tuple[float, float, float]):
        self.center = center
        self.radius = radius
        self.color = color  # RGB 0-1
    
    def intersect(self, ray: Ray) -> Optional[float]:
        """計算光線與球體的交點，返回 t 值（距離）"""
        oc = ray.origin - self.center
        a = ray.direction.dot(ray.direction)
        b = 2.0 * oc.dot(ray.direction)
        c = oc.dot(oc) - self.radius * self.radius
        discriminant = b * b - 4 * a * c
        
        if discriminant < 0:
            return None
        
        t = (-b - math.sqrt(discriminant)) / (2.0 * a)
        return t if t > 0.001 else None  # 避免自相交


def trace_ray(ray: Ray, spheres: List[Sphere], lights: List[Vec3], depth: int = 0) -> Tuple[float, float, float]:
    """追蹤光線，返回顏色 (r, g, b)"""
    if depth > 3:  # 最大遞迴深度
        return (0.0, 0.0, 0.0)
    
    # 找出最近的交點
    min_t = float('inf')
    hit_sphere = None
    
    for sphere in spheres:
        t = sphere.intersect(ray)
        if t is not None and t < min_t:
            min_t = t
            hit_sphere = sphere
    
    if hit_sphere is None:
        # 背景色（天空藍漸層）
        t = 0.5 * (ray.direction.y + 1.0)
        return (1.0 - t) * 1.0 + t * 0.5, (1.0 - t) * 1.0 + t * 0.7, (1.0 - t) * 1.0 + t * 1.0
    
    # 計算交點和法向量
    hit_point = ray.origin + ray.direction * min_t
    normal = (hit_point - hit_sphere.center).normalize()
    
    # 漫射著色
    color = hit_sphere.color
    light_intensity = 0.1  # 環境光
    
    for light in lights:
        light_dir = (light - hit_point).normalize()
        diff = max(0.0, normal.dot(light_dir))
        light_intensity += diff * 0.9
    
    r = min(1.0, color[0] * light_intensity)
    g = min(1.0, color[1] * light_intensity)
    b = min(1.0, color[2] * light_intensity)
    
    return (r, g, b)


def render_scene(width: int, height: int, spheres: List[Sphere], lights: List[Vec3]) -> str:
    """渲染場景，輸出 PPM 格式字串"""
    lines = [f"P3\n# Ray Traced Scene\n{width} {height}\n255"]
    
    camera = Vec3(0.0, 0.0, -5.0)
    viewport_height = 2.0
    viewport_width = 2.0 * width / height
    focal_length = 1.0
    
    horizontal = Vec3(viewport_width, 0.0, 0.0)
    vertical = Vec3(0.0, viewport_height, 0.0)
    lower_left = camera - horizontal * 0.5 - vertical * 0.5 - Vec3(0.0, 0.0, focal_length)
    
    for j in range(height - 1, -1, -1):
        for i in range(width):
            u = i / (width - 1)
            v = j / (height - 1)
            
            direction = lower_left + horizontal * u + vertical * v - camera
            ray = Ray(camera, direction)
            
            r, g, b = trace_ray(ray, spheres, lights)
            lines.append(f"{int(r*255)} {int(g*255)} {int(b*255)}")
    
    return '\n'.join(lines)


if __name__ == "__main__":
    print("基礎光線追蹤演示")
    print("=" * 40)
    
    # 定義場景物件
    spheres = [
        Sphere(Vec3(0.0, 0.0, 0.0), 1.0, (1.0, 0.3, 0.3)),   # 紅色球
        Sphere(Vec3(2.0, 0.0, 1.0), 1.0, (0.3, 1.0, 0.3)),   # 綠色球
        Sphere(Vec3(-2.0, 0.5, 1.0), 0.8, (0.3, 0.3, 1.0)),  # 藍色球
    ]
    
    lights = [
        Vec3(5.0, 10.0, -5.0),
        Vec3(-5.0, 5.0, 5.0),
    ]
    
    # 渲染小圖（100x100）
    print("渲染中...")
    ppm = render_scene(100, 100, spheres, lights)
    
    # 儲存為檔案
    with open("/Users/Shared/ccc/project/cs4py/code/電腦圖學/render/output.ppm", "w") as f:
        f.write(ppm)
    print("已儲存至 render/output.ppm")
    print(f"影像大小: 100x100 像素")
