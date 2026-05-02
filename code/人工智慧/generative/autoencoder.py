"""
自编码器（Autoencoder）实现
包括编码器和解码器架构，用于降维和特征学习
"""

import random
import math
from typing import List, Tuple

class DenseLayer:
    """全连接层（纯Python实现）"""
    def __init__(self, input_size: int, output_size: int):
        # Xavier初始化
        self.weights = [[random.gauss(0, math.sqrt(2.0 / input_size)) 
                        for _ in range(input_size)] for _ in range(output_size)]
        self.bias = [0.0] * output_size
        self.input = None
        self.output = None
    
    def forward(self, x: List[float]) -> List[float]:
        """前向传播"""
        self.input = x
        self.output = [0.0] * len(self.bias)
        for i in range(len(self.bias)):
            self.output[i] = self.bias[i]
            for j in range(len(x)):
                self.output[i] += self.weights[i][j] * x[j]
        return self.output
    
    def backward(self, grad: List[float], learning_rate: float) -> List[float]:
        """反向传播，返回输入梯度"""
        input_grad = [0.0] * len(self.input)
        
        for i in range(len(self.bias)):
            # 更新权重和偏置
            for j in range(len(self.input)):
                self.weights[i][j] -= learning_rate * grad[i] * self.input[j]
            self.bias[i] -= learning_rate * grad[i]
            
            # 计算输入梯度
            for j in range(len(self.input)):
                input_grad[j] += grad[i] * self.weights[i][j]
        
        return input_grad


def sigmoid(x: float) -> float:
    """Sigmoid激活函数"""
    if x > 10:
        return 1.0
    if x < -10:
        return 0.0
    return 1.0 / (1.0 + math.exp(-x))


def sigmoid_derivative(x: float) -> float:
    """Sigmoid导数"""
    s = sigmoid(x)
    return s * (1 - s)


class Autoencoder:
    """自编码器：编码器-解码器架构"""
    def __init__(self, input_size: int, hidden_size: int, latent_size: int):
        self.input_size = input_size
        self.latent_size = latent_size
        
        # 编码器
        self.enc_fc1 = DenseLayer(input_size, hidden_size)
        self.enc_fc2 = DenseLayer(hidden_size, latent_size)
        
        # 解码器
        self.dec_fc1 = DenseLayer(latent_size, hidden_size)
        self.dec_fc2 = DenseLayer(hidden_size, input_size)
        
        self.learning_rate = 0.01
    
    def encode(self, x: List[float]) -> List[float]:
        """编码：输入 -> 潜在表示"""
        h = self.enc_fc1.forward(x)
        h = [sigmoid(v) for v in h]
        z = self.enc_fc2.forward(h)
        z = [sigmoid(v) for v in z]
        return z
    
    def decode(self, z: List[float]) -> List[float]:
        """解码：潜在表示 -> 重建输入"""
        h = self.dec_fc1.forward(z)
        h = [sigmoid(v) for v in h]
        x_recon = self.dec_fc2.forward(h)
        x_recon = [sigmoid(v) for v in x_recon]
        return x_recon
    
    def forward(self, x: List[float]) -> List[float]:
        """前向传播：编码+解码"""
        z = self.encode(x)
        x_recon = self.decode(z)
        return x_recon
    
    def mse_loss(self, pred: List[float], target: List[float]) -> float:
        """均方误差损失"""
        return sum((p - t) ** 2 for p, t in zip(pred, target)) / len(pred)
    
    def backward(self, x: List[float], x_recon: List[float]) -> None:
        """反向传播更新权重"""
        # 计算输出梯度（MSE导数）
        output_grad = [(p - t) * 2.0 / len(x) for p, t in zip(x_recon, x)]
        
        # 解码器反向传播
        dec_h_activated = [sigmoid(v) for v in self.dec_fc1.output]
        dec_grad = [output_grad[i] * sigmoid_derivative(self.dec_fc2.output[i]) 
                   for i in range(len(output_grad))]
        dec_h_grad = self.dec_fc2.backward(dec_grad, self.learning_rate)
        
        dec_h_grad_activated = [dec_h_grad[i] * sigmoid_derivative(dec_h_activated[i]) 
                               for i in range(len(dec_h_grad))]
        latent_grad = self.dec_fc1.backward(dec_h_grad_activated, self.learning_rate)
        
        # 编码器反向传播
        enc_h_activated = [sigmoid(v) for v in self.enc_fc1.output]
        enc_grad = [latent_grad[i] * sigmoid_derivative(self.enc_fc2.output[i]) 
                   for i in range(len(latent_grad))]
        enc_h_grad = self.enc_fc2.backward(enc_grad, self.learning_rate)
        
        enc_h_grad_activated = [enc_h_grad[i] * sigmoid_derivative(enc_h_activated[i]) 
                               for i in range(len(enc_h_grad))]
        self.enc_fc1.backward(enc_h_grad_activated, self.learning_rate)
    
    def train_step(self, x: List[float]) -> float:
        """单步训练"""
        x_recon = self.forward(x)
        loss = self.mse_loss(x_recon, x)
        self.backward(x, x_recon)
        return loss


def generate_simple_data(n_samples: int, n_features: int) -> List[List[float]]:
    """生成简单的测试数据（随机二进制向量）"""
    return [[random.randint(0, 1) for _ in range(n_features)] for _ in range(n_samples)]


def add_noise(x: List[float], noise_level: float = 0.1) -> List[float]:
    """为输入添加噪声（去噪自编码器）"""
    return [min(1.0, max(0.0, v + random.gauss(0, noise_level))) for v in x]


if __name__ == "__main__":
    print("训练自编码器...")
    
    # 参数
    input_size = 8
    hidden_size = 6
    latent_size = 3
    n_samples = 100
    n_epochs = 100
    
    # 创建自编码器和数据
    ae = Autoencoder(input_size, hidden_size, latent_size)
    data = generate_simple_data(n_samples, input_size)
    
    # 训练
    for epoch in range(n_epochs):
        total_loss = 0.0
        for x in data:
            # 去噪自编码器：添加噪声后重建原始
            x_noisy = add_noise(x, noise_level=0.2)
            loss = ae.train_step(x_noisy)
            total_loss += loss
        
        avg_loss = total_loss / n_samples
        if (epoch + 1) % 20 == 0:
            print(f"Epoch {epoch+1}/{n_epochs}, Average Loss: {avg_loss:.4f}")
    
    # 测试
    print("\n测试自编码器：")
    test_samples = generate_simple_data(5, input_size)
    for i, x in enumerate(test_samples):
        x_noisy = add_noise(x, noise_level=0.2)
        z = ae.encode(x_noisy)
        x_recon = ae.decode(z)
        print(f"Sample {i+1}:")
        print(f"  Original:  {[round(v, 2) for v in x]}")
        print(f"  Noisy:     {[round(v, 2) for v in x_noisy]}")
        print(f"  Latent:    {[round(v, 2) for v in z]}")
        print(f"  Reconstructed: {[round(v, 2) for v in x_recon]}")
        print()
