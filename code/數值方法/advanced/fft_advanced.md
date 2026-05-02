# 進階快速傅立葉變換 (FFT) 應用

## 歷史背景

傅立葉變換起源於 1807 年 Joseph Fourier 的熱傳導方程求解論文。當時的法國科學院拒絕接受他的觀點，認為「不可能用三角級數表示不連續函數」。

1965 年，Cooley 和 Tukey 發表了「An algorithm for the machine calculation of complex Fourier series」，開啟了 FFT 的現代時代。事實上，Gauss 在 1805 年就已經發明了類似的方法，只是未受重視。

2000 年，Frigo 和 Johnson 開發的 FFTW（Fastest Fourier Transform in the West）成為現今最廣泛使用的 FFT 庫。

## 核心原理

### 離散傅立葉變換 (DFT)

$$X_k = \sum_{n=0}^{N-1} x_n e^{-i 2\pi kn/N}$$

直接計算需要 O(N²) 複雜度。

### Cooley-Tukey FFT

利用分治策略，將 DFT 拆分為奇偶兩部分：

$$X_k = E_k + e^{-i 2\pi k/N} O_k$$

其中 $E_k$ 是偶數項的 DFT，$O_k$ 是奇數項的 DFT。

複雜度：O(N log N)

### FFT-based 摺積

時域摺積定理：
$$(a * b)[n] \iff A(\omega) \cdot B(\omega)$$

步驟：
1. 對 a, b 做 FFT → A, B
2. 逐點相乘 C = A · B
3. 對 C 做 IFFT → 摺積結果

複雜度：O(N log N) 而非 O(N²)

### 多項式乘法

將多項式係數視為序列，即可使用 FFT 加速乘法。

## 使用範例

```python
from fft_advanced import convolve_fft, multiply_polynomials, fft, ifft

# 摺積
a = [1.0, 2.0, 3.0, 4.0]
b = [0.5, 1.0, 0.5]
c = convolve_fft(a, b)

# 多項式乘法
p = [1.0, 2.0, 3.0]  # 1 + 2x + 3x²
q = [4.0, 5.0]       # 4 + 5x
r = multiply_polynomials(p, q)  # 4 + 13x + 22x² + 15x³
```

## 參考資料

- Cooley, J. W. & Tukey, J. W. "An algorithm for the machine calculation of complex Fourier series" (1965)
- Brigham, E. O. *The Fast Fourier Transform and Its Applications* (1988)
- Press, W. H., et al. *Numerical Recipes* Chapter 12 (第 3 版)