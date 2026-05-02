"""
变分自编码器（Variational Autoencoder, VAE）实现
包括重参数化技巧、KL散度损失
"""

import random
import math
from typing import List, Tuple

class DenseLayer:
    """全连接层"""
    def __init__(self, input_size: int, output_size: int):
        self.weights = [[random.gauss(0, math.sqrt(2.0 / input_size)) 
                        for _ in range(input_size)] for _ in range(output_size)]
        self.bias = [0.0] * output_size
        self.input = None
        self.output = None
    
    def forward(self, x: List[float]) -> List[float]:
        self.input = x
        self.output = [0.0] * len(self.bias)
        for i in range(len(self.bias)):
            self.output[i] = self.bias[i]
            for j in range(len(x)):
                self.output[i] += self.weights[i][j] * x[j]
        return self.output
    
    def backward(self, grad: List[float], learning_rate: float) -> List[float]:
        input_grad = [0.0] * len(self.input)
        for i in range(len(self.bias)):
            for j in range(len(self.input)):
                self.weights[i][j] -= learning_rate * grad[i] * self.input[j]
            self.bias[i] -= learning_rate * grad[i]
            for j in range(len(self.input)):
                input_grad[j] += grad[i] * self.weights[i][j]
        return input_grad


def relu(x: float) -> float:
    return max(0.0, x)

def relu_derivative(x: float) -> float:
    return 1.0 if x > 0 else 0.0

def sigmoid(x: float) -> float:
    if x > 10: return 1.0
    if x < -10: return 0.0
    return 1.0 / (1.0 + math.exp(-x))


class VAE:
    """变分自编码器"""
    def __init__(self, input_size: int, hidden_size: int, latent_size: int):
        self.input_size = input_size
        self.latent_size = latent_size
        
        # 编码器：输出均值和log方差
        self.enc_fc1 = DenseLayer(input_size, hidden_size)
        self.enc_fc_mu = DenseLayer(hidden_size, latent_size)
        self.enc_fc_logvar = DenseLayer(hidden_size, latent_size)
        
        # 解码器
        self.dec_fc1 = DenseLayer(latent_size, hidden_size)
        self.dec_fc2 = DenseLayer(hidden_size, input_size)
        
        self.learning_rate = 0.001
        self.beta = 1.0  # KL散度权重
    
    def encode(self, x: List[float]) -> Tuple[List[float], List[float]]:
        """编码：返回均值和log方差"""
        h = self.enc_fc1.forward(x)
        h = [relu(v) for v in h]
        mu = self.enc_fc_mu.forward(h)
        logvar = self.enc_fc_logvar.forward(h)
        return mu, logvar
    
    def reparameterize(self, mu: List[float], logvar: List[float]) -> List[float]:
        """重参数化技巧：z = mu + exp(0.5 * logvar) * epsilon"""
        z = []
        for i in range(len(mu)):
            std = math.exp(0.5 * logvar[i])
            eps = random.gauss(0, 1)
            z.append(mu[i] + std * eps)
        return z
    
    def decode(self, z: List[float]) -> List[float]:
        """解码：从潜在空间重建"""
        h = self.dec_fc1.forward(z)
        h = [relu(v) for v in h]
        x_recon = self.dec_fc2.forward(h)
        x_recon = [sigmoid(v) for v in x_recon]
        return x_recon
    
    def forward(self, x: List[float]) -> Tuple[List[float], List[float], List[float], List[float]]:
        """前向传播：返回重建、均值、log方差、采样z"""
        mu, logvar = self.encode(x)
        z = self.reparameterize(mu, logvar)
        x_recon = self.decode(z)
        return x_recon, mu, logvar, z
    
    def reconstruction_loss(self, pred: List[float], target: List[float]) -> float:
        """重建损失（Binary Cross-Entropy）"""
        loss = 0.0
        for p, t in zip(pred, target):
            p = max(1e-8, min(1 - 1e-8, p))
            loss -= (t * math.log(p) + (1 - t) * math.log(1 - p))
        return loss / len(pred)
    
    def kl_loss(self, mu: List[float], logvar: List[float]) -> float:
        """KL散度：KL(q(z|x) || p(z))，其中p(z)是标准正态"""
        # KL = -0.5 * sum(1 + logvar - mu^2 - exp(logvar))
        kl = 0.0
        for i in range(len(mu)):
            kl += 1 + logvar[i] - mu[i]**2 - math.exp(logvar[i])
        return -0.5 * kl / len(mu)
    
    def total_loss(self, pred: List[float], target: List[float], 
                   mu: List[float], logvar: List[float]) -> float:
        """总损失 = 重建损失 + beta * KL散度"""
        recon_loss = self.reconstruction_loss(pred, target)
        kl = self.kl_loss(mu, logvar)
        return recon_loss + self.beta * kl
    
    def backward(self, x: List[float], x_recon: List[float], 
                 mu: List[float], logvar: List[float], z: List[float]) -> None:
        """反向传播（简化版）"""
        # 重建梯度（BCE导数）
        recon_grad = [(p - t) / (len(x) * p * (1 - p) + 1e-8) 
                      for p, t in zip(x_recon, x)]
        
        # 解码器反向传播
        dec_h = [relu(v) for v in self.dec_fc1.output]
        dec_grad = [recon_grad[i] * relu_derivative(self.dec_fc2.output[i]) 
                   for i in range(len(recon_grad))]
        z_grad = self.dec_fc2.backward(dec_grad, self.learning_rate)
        
        dec_h_grad = [z_grad[i] * relu_derivative(dec_h[i]) 
                     for i in range(len(z_grad))]
        self.dec_fc1.backward(dec_h_grad, self.learning_rate)
        
        # 编码器梯度（简化：只考虑KL散度梯度）
        mu_grad = [self.beta * mu[i] for i in range(len(mu))]
        logvar_grad = [self.beta * 0.5 * (math.exp(logvar[i]) - 1) 
                       for i in range(len(logvar))]
        
        # 合并梯度并更新编码器
        h_activated = [relu(v) for v in self.enc_fc1.output]
        mu_grad_decoded = self.enc_fc_mu.backward(mu_grad, self.learning_rate)
        logvar_grad_decoded = self.enc_fc_logvar.backward(logvar_grad, self.learning_rate)
        
        combined_grad = [mu_grad_decoded[i] + logvar_grad_decoded[i] 
                        for i in range(len(mu_grad_decoded))]
        combined_grad_activated = [combined_grad[i] * relu_derivative(h_activated[i]) 
                                  for i in range(len(combined_grad))]
        self.enc_fc1.backward(combined_grad_activated, self.learning_rate)
    
    def train_step(self, x: List[float]) -> float:
        """单步训练"""
        x_recon, mu, logvar, z = self.forward(x)
        loss = self.total_loss(x_recon, x, mu, logvar)
        self.backward(x, x_recon, mu, logvar, z)
        return loss


def generate_binary_data(n_samples: int, n_features: int) -> List[List[float]]:
    """生成二进制数据"""
    return [[random.randint(0, 1) for _ in range(n_features)] for _ in range(n_samples)]


if __name__ == "__main__":
    print("训练变分自编码器（VAE）...")
    
    input_size = 8
    hidden_size = 6
    latent_size = 2
    n_samples = 100
    n_epochs = 100
    
    vae = VAE(input_size, hidden_size, latent_size)
    data = generate_binary_data(n_samples, input_size)
    
    for epoch in range(n_epochs):
        total_loss = 0.0
        for x in data:
            loss = vae.train_step(x)
            total_loss += loss
        
        avg_loss = total_loss / n_samples
        if (epoch + 1) % 20 == 0:
            print(f"Epoch {epoch+1}/{n_epochs}, Average Loss: {avg_loss:.4f}")
    
    print("\n测试VAE：")
    test_samples = generate_binary_data(5, input_size)
    for i, x in enumerate(test_samples):
        mu, logvar = vae.encode(x)
        z = vae.reparameterize(mu, logvar)
        x_recon = vae.decode(z)
        print(f"Sample {i+1}:")
        print(f"  Original:  {[round(v, 2) for v in x]}")
        print(f"  Latent mu: {[round(v, 2) for v in mu]}")
        print(f"  Reconstructed: {[round(v, 2) for v in x_recon]}")
        print()
    
    print("从潜在空间采样生成新数据：")
    for i in range(3):
        z = [random.gauss(0, 1) for _ in range(latent_size)]
        x_gen = vae.decode(z)
        print(f"  Sampled z: {[round(v, 2) for v in z]}")
        print(f"  Generated: {[round(v, 2) for v in x_gen]}")
