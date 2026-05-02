# 中國剩餘定理 (Chinese Remainder Theorem, CRT)

## 歷史背景

中國剩餘定理是中國古代數學的重要成就，最早記載於公元 5 世紀的《孫子算經》。

### 孫子算經問題

```
今有物不知其數，
三三數之剩二，
五五數之剩三，
七七數之剩二，
問物幾何？

答案：23
```

這個問題可以用同餘方程組表示：
```
x ≡ 2 (mod 3)
x ≡ 3 (mod 5)
x ≡ 2 (mod 7)
```

## 定理內容

### 標準形式

給定一組同餘方程：
```
x ≡ a₁ (mod n₁)
x ≡ a₂ (mod n₂)
...
x ≡ aₖ (mod nₖ)
```

若所有模數 n₁, n₂, ..., nₖ 兩兩互質，則：
- 存在唯一解 x 滿足所有方程
- 解在模 N = n₁ × n₂ × ... × nₖ 下唯一

### 解法

```
步驟：
1. 計算 N = n₁ × n₂ × ... × nₖ
2. 對於每個 i：
   - 計算 Ni = N / ni
   - 計算 Mi = Ni 在模 ni 下的反元素（Ni × Mi ≡ 1 mod ni）
   - 計算 term_i = ai × Ni × Mi
3. 答案：x = (Σ term_i) mod N
```

## 擴展歐幾里得演算法

計算模反元素需要擴展歐幾里得演算法：

```
找到整數 x, y 使得：ax + by = gcd(a, b)

遞迴版：
if b == 0: return (a, 1, 0)
else:
    (gcd, x1, y1) = extended_gcd(b, a mod b)
    return (gcd, y1, x1 - (a//b) * y1)
```

## 逐步合併法

當模數不必兩兩互質時，可以使用逐步合併：

```
合併兩個方程：
x ≡ a₁ (mod n₁)
x ≡ a₂ (mod n₂)

1. 計算 g = gcd(n₁, n₂)
2. 若 (a₁ - a₂) 不能被 g 整除，無解
3. 否則，新方程為：
   x ≡ a (mod lcm(n₁, n₂))
   其中 a = a₁ + n₁ × ((a₂ - a₁)/g × m₁) mod (lcm/g)
```

## 程式碼說明

### 中國剩餘定理核心

```python
def chinese_remainder(remainders, moduli):
    N = product(moduli)
    result = 0

    for i in range(len(moduli)):
        Ni = N // moduli[i]
        Mi = mod_inverse(Ni, moduli[i])
        result += remainders[i] * Ni * Mi

    return result % N
```

### 模反元素

```python
def mod_inverse(a, m):
    gcd, x, _ = extended_gcd(a, m)
    if gcd != 1:
        return None  # 反元素不存在
    return x % m
```

## 應用場景

### 1. RSA-CRT

使用 CRT 加速 RSA 解密：
```
將解密運算分別在 mod p 和 mod q 下進行，
再用 CRT 合併結果，速度提升約 4 倍。
```

### 2. 大整數運算

將大整數表示為一組小模數下的餘數，運算更快。

### 3. 系統設計

周期性事件的時間計算（如「每 3 天、每 5 天、每 7 天」）。

## 計算範例

```
孫子問題：
x ≡ 2 (mod 3)
x ≡ 3 (mod 5)
x ≡ 2 (mod 7)

步驟：
N = 3 × 5 × 7 = 105

i=1: N₁ = 35, M₁ = 35⁻¹ mod 3 = 2⁻¹ mod 3 = 2
     term₁ = 2 × 35 × 2 = 140

i=2: N₂ = 21, M₂ = 21⁻¹ mod 5 = 1⁻¹ mod 5 = 1
     term₂ = 3 × 21 × 1 = 63

i=3: N₃ = 15, M₃ = 15⁻¹ mod 7 = 1⁻¹ mod 7 = 1
     term₃ = 2 × 15 × 1 = 30

x = (140 + 63 + 30) mod 105 = 233 mod 105 = 23
```

## 參考資料

- 孫子算經（公元 5 世紀）
- Knuth, D. E. (1997). *The Art of Computer Programming, Volume 2: Seminumerical Algorithms* (3rd ed.). Addison-Wesley.
- Cormen, T. H., et al. (2009). *Introduction to Algorithms* (3rd ed.). MIT Press. (Chapter 31.5)
- 李儼（1954）《中算史論叢》
