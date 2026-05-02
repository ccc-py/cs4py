# 生成对抗网络（GAN）

## 歷史背景

生成對抗網絡（Generative Adversarial Network，GAN）由 Ian Goodfellow 等人在 2014 年的論文《Generative Adversarial Nets》中提出，開創了生成模型的新紀元。

GAN 通過兩個神經網絡的對抗訓練來學習數據分布：生成器（Generator）試圖生成逼真的假數據，判別器（Discriminator）試圖區分真實數據和生成數據。這種極小極大博弈最終使生成器能夠生成與真實數據無法區分的樣本。

## 核心原理

### 對抗框架

```
生成器 G: z → x_fake，其中 z ~ p(z)（通常為正態分布）
判別器 D: x → [0, 1]，輸出輸入為真實的概率
```

### 目標函數（極小極大博弈）

```
min_G max_D V(D, G) = E_x~p_data[log D(x)] + E_z~p_z[log(1 - D(G(z)))]
```

- **判別器目標**：最大化正確分類的概率（真實→1，生成→0）
- **生成器目標**：最小化 log(1 - D(G(z)))，即欺騙判別器

### 訓練過程

1. **訓練判別器**：
   - 真實數據標記為 1
   - 生成數據標記為 0
   - 更新判別器權重以最小化分類誤差

2. **訓練生成器**：
   - 固定判別器
   - 生成數據標記為 1（欺騙判別器）
   - 更新生成器權重以最大化判別器的錯誤

### 挑戰

- **模式崩潰（Mode Collapse）**：生成器只學習到部分數據模式
- **訓練不穩定**：需要精心調整超參數
- **梯度消失**：判別器過強時生成器梯度消失

## 使用範例

```python
from gan import GAN, generate_target_distribution

# 創建GAN
gan = GAN(latent_size=4, data_size=8, hidden_size=8)

# 生成目標分布數據
real_data = generate_target_distribution(n_samples=100, data_size=8)

# 訓練
for epoch in range(500):
    batch_real = gan.sample_real(batch_size=16, data=real_data)
    d_loss, g_loss = gan.train_step(batch_real)

# 從生成器採樣
z = [random.gauss(0, 1) for _ in range(4)]
fake_sample = gan.generator.forward(z)
print(f"生成的樣本：{[round(v, 2) for v in fake_sample]}")
```

## 參考資料

1. Goodfellow, I., et al. (2014). Generative adversarial nets. NeurIPS.
2. Goodfellow, I. (2016). NIPS 2016 Tutorial: Generative Adversarial Networks. arXiv:1701.00160.
3. [GAN Tutorial](https://developers.google.com/machine-learning/gan)
4. [Understanding GAN](https://towardsdatascience.com/understanding-generative-adversarial-networks-gans-856265378ec8)
