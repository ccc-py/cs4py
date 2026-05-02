# π 估計 (Pi Estimation)

## 歷史背景

### 擲飛鏢法

蒙地卡羅方法估計 π 是最著名的機率算法範例之一。這個方法直觀地展示了如何用隨機性解決確定性問題。

### 布豐投針法

布豐投針問題由法國自然學家喬治-路易·勒克萊爾（喬治-路易·布豐伯爵）於 1777 年提出，是幾何機率的第一個問題。這個實驗在 1901 年由義大利數學家 Mario Lazzarini 實際執行，他宣稱投擲 3408 次針得到了 π ≈ 355/113 的精確結果。

## 核心原理

### 擲飛鏢法

在單位正方形 $[0,1] \times [0,1]$ 內隨機投擲點，四分之一圓 $x^2 + y^2 \leq 1$ 的面積為 $\pi/4$，正方形面積為 1。

$$
\frac{\text{圓內點數}}{\text{總點數}} \approx \frac{\pi}{4}
$$

因此：

$$
\pi \approx 4 \times \frac{\text{圓內點數}}{\text{總點數}}
$$

### 布豐投針法

在平面上畫間距為 $d$ 的平行線，隨機投擲長度為 $l$ (其中 $l \leq d$) 的針。

針與線相交的機率為：

$$
P = \frac{2l}{\pi d}
$$

因此：

$$
\pi = \frac{2l}{P \cdot d} \approx \frac{2l \cdot n_{\text{針數}}}{d \cdot n_{\text{相交數}}}
$$

## 收斂性分析

蒙地卡羅估計的標準誤差為：

$$
\text{SE} = \frac{\sigma}{\sqrt{N}}
$$

其中 $\sigma$ 是樣本標準差，$N$ 是樣本數。這意味著要將誤差減半，需要四倍的樣本數。

## 使用範例

```python
from monte_carlo.pi_estimation import estimate_pi_dart_throwing, buffon_needle

# 擲飛鏢法估計 π
pi_est = estimate_pi_dart_throwing(n_darts=10000)
print(f"π ≈ {pi_est:.6f}")

# 布豐投針法估計 π
pi_est2 = buffon_needle(n_needles=10000, needle_length=1.0, line_spacing=2.0)
print(f"π ≈ {pi_est2:.6f}")
```

## 誤差比較

| 方法 | 樣本數 | 典型誤差 |
|------|--------|----------|
| 擲飛鏢法 | 1,000 | ~0.05 |
| 擲飛鏢法 | 10,000 | ~0.016 |
| 擲飛鏢法 | 100,000 | ~0.005 |
| 布豐投針法 | 10,000 | ~0.02 |

## 參考資料

1. Buffon, G. L. L. (1777). *Essai d'arithmétique morale*. Histoire naturelle, générale et particulière, Supplément, 4, 46-123.
2. Metropolis, N. (1987). The beginning of the Monte Carlo method. *Los Alamos Science*, 15, 125-130.
3. Mazhdrakov, M., Benov, D., & Valkanov, N. (2018). *The Monte Carlo Method: Engineering Applications*. ACMO Academic Press.
