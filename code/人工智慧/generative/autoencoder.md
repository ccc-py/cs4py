# 自编码器（Autoencoder）

## 歷史背景

自编码器（Autoencoder）最早由 Hinton 和 Zemel 在 1994 年的論文《Autoencoders, Minimum Description Length and Helmholtz Free Energy》中提出，是一種無監督學習的神經網絡架構。

自编码器的目標是學習數據的壓縮表示（編碼），然後能夠從這個壓縮表示重建原始輸入。它在降維、特徵學習、去噪和異常檢測等任務中有廣泛應用。

## 核心原理

### 架構

自编码器由兩個主要部分組成：

```
输入 x → [编码器 Encoder] → 潜在表示 z → [解码器 Decoder] → 重建 x'
```

- **编码器**：將輸入 x 映射到潛在表示 z = f(x)
- **解码器**：將潛在表示 z 映射回重建 x' = g(z)

### 損失函數

通常使用均方誤差（MSE）作為重建損失：

```
L(x, x') = ||x - x'||²
```

### 變體

1. **去噪自编码器（Denoising Autoencoder）**：輸入添加噪聲，訓練重建原始乾淨輸入
2. **稀疏自编码器**：在損失中添加正則化項，鼓勵稀疏的潛在表示
3. **變分自编码器（VAE）**：引入概率框架，學習潛在空間的概率分布

### 應用

- 降維和特徵提取
- 圖像去噪
- 異常檢測
- 數據生成（VAE、GAN）

## 使用範例

```python
from autoencoder import Autoencoder, generate_simple_data, add_noise

# 創建自编码器
ae = Autoencoder(input_size=8, hidden_size=6, latent_size=3)

# 生成訓練數據
data = generate_simple_data(n_samples=100, n_features=8)

# 訓練
for epoch in range(100):
    for x in data:
        x_noisy = add_noise(x, noise_level=0.2)
        loss = ae.train_step(x_noisy)

# 測試
x = [1, 0, 1, 0, 1, 0, 1, 0]
z = ae.encode(x)  # 編碼到潛在空間
x_recon = ae.decode(z)  # 從潛在空間解碼
print(f"Latent: {z}")
print(f"Reconstructed: {x_recon}")
```

## 參考資料

1. Hinton, G. E., & Zemel, R. S. (1994). Autoencoders, minimum description length and Helmholtz free energy. NeurIPS.
2. Goodfellow, I., Bengio, Y., & Courville, A. (2016). Deep Learning. MIT Press. (Chapter 14)
3. [Autoencoder - Wikipedia](https://en.wikipedia.org/wiki/Autoencoder)
4. [Tutorial on Autoencoders](https://blog.keras.io/building-autoencoders-in-python.html)
