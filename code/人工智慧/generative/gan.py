"""
生成对抗网络（GAN）简化实现
包括生成器和判别器，使用极小极大训练
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
        self.grad_weights = None
        self.grad_bias = None
    
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

def sigmoid_derivative(x: float) -> float:
    s = sigmoid(x)
    return s * (1 - s)


class Generator:
    """生成器：从噪声z生成假数据"""
    def __init__(self, latent_size: int, hidden_size: int, output_size: int):
        self.latent_size = latent_size
        self.fc1 = DenseLayer(latent_size, hidden_size)
        self.fc2 = DenseLayer(hidden_size, output_size)
        self.learning_rate = 0.0002
    
    def forward(self, z: List[float]) -> List[float]:
        """生成假样本"""
        h = self.fc1.forward(z)
        h = [relu(v) for v in h]
        output = self.fc2.forward(h)
        output = [sigmoid(v) for v in output]
        return output
    
    def train(self, z: List[float], disc_grad: List[float]) -> None:
        """训练生成器（通过判别器的梯度）"""
        # 前向传播
        h = self.fc1.forward(z)
        h_activated = [relu(v) for v in h]
        output = self.fc2.forward(h_activated)
        
        # 反向传播
        grad_output = [disc_grad[i] * sigmoid_derivative(output[i]) 
                      for i in range(len(disc_grad))]
        grad_h = self.fc2.backward(grad_output, self.learning_rate)
        grad_h_activated = [grad_h[i] * relu_derivative(h_activated[i]) 
                           for i in range(len(grad_h))]
        self.fc1.backward(grad_h_activated, self.learning_rate)


class Discriminator:
    """判别器：判断输入是真实还是生成"""
    def __init__(self, input_size: int, hidden_size: int):
        self.input_size = input_size
        self.fc1 = DenseLayer(input_size, hidden_size)
        self.fc2 = DenseLayer(hidden_size, 1)
        self.learning_rate = 0.0002
    
    def forward(self, x: List[float]) -> float:
        """返回判别概率（标量）"""
        h = self.fc1.forward(x)
        h = [relu(v) for v in h]
        output = self.fc2.forward(h)
        prob = sigmoid(output[0])
        return prob
    
    def backward(self, x: List[float], target: float) -> float:
        """训练判别器，返回梯度用于生成器"""
        # 前向传播
        h = self.fc1.forward(x)
        h_activated = [relu(v) for v in h]
        output = self.fc2.forward(h_activated)
        pred = sigmoid(output[0])
        
        # 损失梯度（BCE导数）
        # error = pred - target
        error = pred - target
        
        # 输出层梯度
        grad_output = [error * sigmoid_derivative(output[0])]
        grad_h = self.fc2.backward(grad_output, self.learning_rate)
        
        # 隐藏层梯度
        grad_h_activated = [grad_h[i] * relu_derivative(h_activated[i]) 
                           for i in range(len(grad_h))]
        input_grad = self.fc1.backward(grad_h_activated, self.learning_rate)
        
        return error  # 返回误差用于生成器


class GAN:
    """GAN训练框架"""
    def __init__(self, latent_size: int, data_size: int, hidden_size: int = 16):
        self.latent_size = latent_size
        self.data_size = data_size
        self.generator = Generator(latent_size, hidden_size, data_size)
        self.discriminator = Discriminator(data_size, hidden_size)
    
    def sample_latent(self, batch_size: int) -> List[List[float]]:
        """从先验分布采样潜在向量"""
        return [[random.gauss(0, 1) for _ in range(self.latent_size)] 
                for _ in range(batch_size)]
    
    def sample_real(self, batch_size: int, data: List[List[float]]) -> List[List[float]]:
        """采样真实数据"""
        return [data[random.randint(0, len(data) - 1)] for _ in range(batch_size)]
    
    def train_step(self, real_data: List[List[float]]) -> Tuple[float, float]:
        """单步训练：训练判别器和生成器"""
        batch_size = len(real_data)
        
        # 训练判别器
        d_loss_real = 0.0
        d_loss_fake = 0.0
        
        # 真实数据
        for x_real in real_data:
            _ = self.discriminator.forward(x_real)
            error = self.discriminator.backward(x_real, target=1.0)
            d_loss_real += error ** 2
        
        # 生成数据
        z_batch = self.sample_latent(batch_size)
        for z in z_batch:
            x_fake = self.generator.forward(z)
            error = self.discriminator.backward(x_fake, target=0.0)
            d_loss_fake += error ** 2
        
        # 训练生成器
        g_loss = 0.0
        z_batch = self.sample_latent(batch_size)
        for z in z_batch:
            x_fake = self.generator.forward(z)
            pred = self.discriminator.forward(x_fake)
            # 生成器希望判别器认为假数据是真实的（target=1）
            error = self.discriminator.backward(x_fake, target=1.0)
            self.generator.train(z, [error])
            g_loss += (pred - 1.0) ** 2
        
        return (d_loss_real + d_loss_fake) / (2 * batch_size), g_loss / batch_size


def generate_target_distribution(n_samples: int, data_size: int) -> List[List[float]]:
    """生成目标分布数据（例如：特定的二进制模式）"""
    data = []
    for _ in range(n_samples):
        sample = []
        for i in range(data_size):
            # 创建一个偏置分布：前一半特征更可能是1
            prob = 0.8 if i < data_size // 2 else 0.2
            sample.append(1.0 if random.random() < prob else 0.0)
        data.append(sample)
    return data


def sample_from_generator(generator: Generator, latent_size: int, n_samples: int) -> List[List[float]]:
    """从生成器采样"""
    samples = []
    for _ in range(n_samples):
        z = [random.gauss(0, 1) for _ in range(latent_size)]
        sample = generator.forward(z)
        samples.append(sample)
    return samples


if __name__ == "__main__":
    print("训练生成对抗网络（GAN）...")
    
    latent_size = 4
    data_size = 8
    hidden_size = 8
    n_epochs = 500
    batch_size = 16
    
    gan = GAN(latent_size, data_size, hidden_size)
    real_data = generate_target_distribution(100, data_size)
    
    for epoch in range(n_epochs):
        # 采样真实数据批次
        batch_real = gan.sample_real(batch_size, real_data)
        d_loss, g_loss = gan.train_step(batch_real)
        
        if (epoch + 1) % 100 == 0:
            print(f"Epoch {epoch+1}/{n_epochs}, D Loss: {d_loss:.4f}, G Loss: {g_loss:.4f}")
    
    print("\n测试训练后的GAN：")
    print("真实数据样例：")
    for i in range(3):
        print(f"  {[round(v, 2) for v in real_data[i]]}")
    
    print("\n生成数据样例：")
    fake_samples = sample_from_generator(gan.generator, latent_size, 3)
    for i, sample in enumerate(fake_samples):
        print(f"  {[round(v, 2) for v in sample]}")
    
    # 计算简单统计
    real_mean = [sum(r[i] for r in real_data) / len(real_data) for i in range(data_size)]
    fake_mean = [sum(f[i] for f in fake_samples) / len(fake_samples) for i in range(data_size)]
    print(f"\n真实数据均值：{[round(v, 2) for v in real_mean]}")
    print(f"生成数据均值：{[round(v, 2) for v in fake_mean]}")
