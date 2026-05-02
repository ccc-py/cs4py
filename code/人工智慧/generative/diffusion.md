# 扩散模型（Diffusion Model）

## 歷史背景

擴散模型（Diffusion Model）的概念最早由 Jascha Sohl-Dickstein 等人在 2015 年的論文《Deep Unsupervised Learning using Nonequilibrium Thermodynamics》中提出。隨後，Denoising Diffusion Probabilistic Models (DDPM) 由 Jonathan Ho 等人在 2020 年提出，並在圖像生成任務中取得了突破性成果，成為當前最流行的生成模型之一（如 Stable Diffusion、DALL-E 2）。

## 核心原理

### 前向過程（加噪）

前向過程逐步向數據添加高斯噪聲，經過 T 步後，數據變為標準正態分布：

```
q(x_t | x_{t-1}) = N(x_t; sqrt(1-β_t) * x_{t-1}, β_t * I)
```

其中 β_t 是噪聲調度（noise schedule）。

### 反向過程（去噪）

學習反向轉換，從噪聲逐步恢復數據：

```
p_θ(x_{t-1} | x_t) = N(x_{t-1}; μ_θ(x_t, t), σ_t^2 * I)
```

### 訓練目標

擴散模型通過訓練神經網絡預測添加的噪聲來學習：

```
L = ||ε - ε_θ(x_t, t)||²
```

其中 ε 是實際添加的噪聲，ε_θ 是模型預測的噪聲。

### 生成過程

從隨機噪聲 x_T ~ N(0, I) 開始，逐步去噪：

```
for t = T, T-1, ..., 1:
    x_{t-1} = (x_t - sqrt(1-α_t) * ε_θ(x_t, t)) / sqrt(α_t) + noise
```

## 使用範例

```python
from diffusion import DiffusionModel, generate_target_data

# 創建擴散模型
model = DiffusionModel(n_steps=50, hidden_size=16)

# 生成目標數據（例如：均值為3的正態分布）
target_data = generate_target_data(n_samples=100, mean=3.0, std=1.0)

# 訓練
for epoch in range(200):
    for _ in range(50):
        x_start = random.choice(target_data)
        loss = model.train_step(x_start)

# 生成新樣本
generated_samples = model.sample(n_samples=10)
print(f"生成的樣本：{[round(v, 2) for v in generated_samples]}")
```

## 參考資料

1. Sohl-Dickstein, J., et al. (2015). Deep unsupervised learning using nonequilibrium thermodynamics. ICML.
2. Ho, J., Jain, A., & Abbeel, P. (2020). Denoising diffusion probabilistic models. NeurIPS.
3. Nichol, A. Q., & Dhariwal, P. (2021). Improved denoising diffusion probabilistic models. ICML.
4. [Diffusion Models Tutorial](https://lilianweng.github.io/lil-log/2021/07/11/diffusion-models.html)
5. [Understanding Diffusion](https://www.assemblyai.com/blog/diffusion-models-for-beginners/)
