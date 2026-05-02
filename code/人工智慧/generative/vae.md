# 变分自编码器（VAE）

## 歷史背景

变分自编码器（Variational Autoencoder，VAE）由 Diederik P. Kingma 和 Max Welling 在 2013 年的論文《Auto-Encoding Variational Bayes》中提出，是一種生成模型，結合了深度學習和變分推斷（Variational Inference）。

VAE 通過學習數據的概率潛在表示，能夠生成新的、與訓練數據相似的樣本，是深度生成模型的重要里程碑。

## 核心原理

### 概率框架

VAE 假設數據 x 是由潛在變量 z 生成的：

```
p(x) = ∫ p(x|z) * p(z) dz
```

其中：
- **p(z)**：先驗分布（通常為標準正態分布 N(0, I)）
- **p(x|z)**：似然函數（解碼器）
- **q(z|x)**：近似後驗分布（編碼器）

### 重參數化技巧（Reparameterization Trick）

為了使隨機節點可微，將採樣過程重參數化：

```
z = μ + σ ⊙ ε，其中 ε ~ N(0, I)
```

這樣梯度可以通過 μ 和 σ 反向傳播。

### 損失函數

VAE 的損失由兩部分組成：

```
L = -E[log p(x|z)] + D_KL(q(z|x) || p(z))
```

- **重建損失**：期望對數似然（如 BCE）
- **KL 散度**：正則化項，使 q(z|x) 接近先驗 p(z)

### 生成新數據

訓練完成後，從先驗 p(z) 採樣 z，通過解碼器生成新樣本。

## 使用範例

```python
from vae import VAE, generate_binary_data

# 創建VAE
vae = VAE(input_size=8, hidden_size=6, latent_size=2)

# 訓練
data = generate_binary_data(n_samples=100, n_features=8)
for epoch in range(100):
    for x in data:
        loss = vae.train_step(x)

# 重建
x = [1, 0, 1, 0, 1, 0, 1, 0]
mu, logvar = vae.encode(x)
z = vae.reparameterize(mu, logvar)
x_recon = vae.decode(z)

# 生成新樣本
z_new = [random.gauss(0, 1) for _ in range(2)]
x_gen = vae.decode(z_new)
```

## 參考資料

1. Kingma, D. P., & Welling, M. (2013). Auto-encoding variational bayes. ICLR.
2. Doersch, C. (2016). Tutorial on variational autoencoders. arXiv:1606.05908.
3. [VAE Tutorial](https://tutorials.models.fit/autoencoder/variational-autoencoder.html)
4. [Understanding VAE](https://jeremykun.com/2019/02/12/what-does-it-mean-that-a-variational-autoencoder-learns-a-probability-distribution/)
