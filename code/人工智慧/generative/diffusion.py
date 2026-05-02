"""
扩散模型（Diffusion Model）简化实现（1D）
包括前向加噪过程和反向去噪过程
"""

import random
import math
from typing import List, Tuple

class SimpleMLP:
    """简单的多层感知机（纯Python实现）"""
    def __init__(self, input_size: int, hidden_size: int, output_size: int):
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.output_size = output_size
        
        # Xavier初始化
        self.W1 = [[random.gauss(0, math.sqrt(1.0 / input_size)) 
                    for _ in range(input_size)] for _ in range(hidden_size)]
        self.b1 = [0.0] * hidden_size
        
        self.W2 = [[random.gauss(0, math.sqrt(1.0 / hidden_size)) 
                    for _ in range(hidden_size)] for _ in range(output_size)]
        self.b2 = [0.0] * output_size
        
        # 缓存用于反向传播
        self.input = None
        self.hidden = None
        self.hidden_activated = None
    
    def relu(self, x: float) -> float:
        return max(0.0, x)
    
    def relu_derivative(self, x: float) -> float:
        return 1.0 if x > 0 else 0.0
    
    def forward(self, x: List[float]) -> List[float]:
        """前向传播"""
        self.input = x
        
        # 隐藏层
        self.hidden = [0.0] * self.hidden_size
        for i in range(self.hidden_size):
            self.hidden[i] = self.b1[i]
            for j in range(self.input_size):
                self.hidden[i] += self.W1[i][j] * x[j]
        self.hidden_activated = [self.relu(h) for h in self.hidden]
        
        # 输出层（线性）
        output = [0.0] * self.output_size
        for i in range(self.output_size):
            output[i] = self.b2[i]
            for j in range(self.hidden_size):
                output[i] += self.W2[i][j] * self.hidden_activated[j]
        
        return output
    
    def backward(self, grad: List[float], learning_rate: float) -> None:
        """反向传播更新权重"""
        # 输出层梯度
        output_grad = grad
        
        # 更新输出层权重
        for i in range(self.output_size):
            for j in range(self.hidden_size):
                self.W2[i][j] -= learning_rate * output_grad[i] * self.hidden_activated[j]
            self.b2[i] -= learning_rate * output_grad[i]
        
        # 隐藏层梯度
        hidden_grad = [0.0] * self.hidden_size
        for j in range(self.hidden_size):
            for i in range(self.output_size):
                hidden_grad[j] += output_grad[i] * self.W2[i][j]
            hidden_grad[j] *= self.relu_derivative(self.hidden[j])
        
        # 更新隐藏层权重
        for j in range(self.hidden_size):
            for k in range(self.input_size):
                self.W1[j][k] -= learning_rate * hidden_grad[j] * self.input[k]
            self.b1[j] -= learning_rate * hidden_grad[j]


class DiffusionModel:
    """简化的1D扩散模型"""
    def __init__(self, n_steps: int = 100, hidden_size: int = 16):
        self.n_steps = n_steps
        # 噪声调度：线性beta从0.0001到0.02
        self.betas = [0.0001 + (0.02 - 0.0001) * i / (n_steps - 1) 
                     for i in range(n_steps)]
        # 计算alpha和alpha_bar
        self.alphas = [1.0 - beta for beta in self.betas]
        self.alpha_bars = [1.0] * n_steps
        for i in range(n_steps):
            if i == 0:
                self.alpha_bars[i] = self.alphas[i]
            else:
                self.alpha_bars[i] = self.alpha_bars[i-1] * self.alphas[i]
        
        # 噪声预测网络：输入(数据x_t, 时间步t)，输出预测的噪声
        # 时间步嵌入：简单one-hot编码
        self.time_embed_size = 16
        self.model = SimpleMLP(input_size=1 + self.time_embed_size, 
                              hidden_size=hidden_size, output_size=1)
        self.learning_rate = 0.001
    
    def time_embedding(self, t: int) -> List[float]:
        """时间步嵌入（简化：sinusoidal embedding简化版）"""
        emb = [0.0] * self.time_embed_size
        for i in range(self.time_embed_size):
            # 简单的周期编码
            freq = 1.0 / (10000 ** (2 * i / self.time_embed_size))
            emb[i] = math.sin(t * freq)
        return emb
    
    def q_sample(self, x_start: float, t: int, noise: float = None) -> Tuple[float, float]:
        """前向过程：在步骤t给x_start添加噪声
        
        返回 (x_t, noise)
        """
        if noise is None:
            noise = random.gauss(0, 1)
        
        # x_t = sqrt(alpha_bar_t) * x_start + sqrt(1 - alpha_bar_t) * noise
        alpha_bar_t = self.alpha_bars[t]
        x_t = math.sqrt(alpha_bar_t) * x_start + math.sqrt(1 - alpha_bar_t) * noise
        return x_t, noise
    
    def predict_noise(self, x_t: float, t: int) -> float:
        """使用神经网络预测噪声"""
        # 拼接输入：x_t 和时间嵌入
        time_emb = self.time_embedding(t)
        input_vec = [x_t] + time_emb
        output = self.model.forward(input_vec)
        return output[0]
    
    def train_step(self, x_start: float) -> float:
        """单步训练：预测噪声"""
        # 随机采样时间步
        t = random.randint(0, self.n_steps - 1)
        
        # 生成噪声并前向采样
        noise = random.gauss(0, 1)
        x_t, _ = self.q_sample(x_start, t, noise)
        
        # 预测噪声
        noise_pred = self.predict_noise(x_t, t)
        
        # 损失：均方误差
        loss = (noise_pred - noise) ** 2
        
        # 反向传播
        grad = [2 * (noise_pred - noise)]  # 对预测噪声的梯度
        self.model.backward(grad, self.learning_rate)
        
        return loss
    
    def p_sample(self, x_t: float, t: int) -> float:
        """反向过程：去噪一步（简化：使用预测噪声）"""
        # 预测噪声
        noise_pred = self.predict_noise(x_t, t)
        
        # 计算去噪后的x_{t-1}
        # x_{t-1} = (x_t - sqrt(1-alpha_t) * noise_pred) / sqrt(alpha_t)
        alpha_t = self.alphas[t]
        if t > 0:
            beta_t = self.betas[t]
            x_prev = (x_t - math.sqrt(beta_t) * noise_pred) / math.sqrt(alpha_t)
            # 添加少量噪声（除了最后一步）
            noise = random.gauss(0, 1)
            x_prev += math.sqrt(beta_t) * noise
        else:
            x_prev = x_t  # t=0时，直接返回
        
        return x_prev
    
    def sample(self, n_samples: int = 1) -> List[float]:
        """从随机噪声生成样本"""
        samples = []
        for _ in range(n_samples):
            # 从标准正态开始
            x = random.gauss(0, 1)
            # 反向去噪
            for t in range(self.n_steps - 1, -1, -1):
                x = self.p_sample(x, t)
            samples.append(x)
        return samples


def generate_target_data(n_samples: int, mean: float = 3.0, std: float = 1.0) -> List[float]:
    """生成目标分布数据（正态分布）"""
    return [random.gauss(mean, std) for _ in range(n_samples)]


if __name__ == "__main__":
    print("训练扩散模型（简化1D）...")
    
    n_steps = 50
    hidden_size = 16
    n_epochs = 200
    n_samples = 100
    
    # 创建模型和目标数据
    model = DiffusionModel(n_steps=n_steps, hidden_size=hidden_size)
    target_data = generate_target_data(n_samples, mean=3.0, std=1.0)
    
    # 训练
    for epoch in range(n_epochs):
        total_loss = 0.0
        for _ in range(50):  # 每epoch训练50步
            x_start = target_data[random.randint(0, len(target_data) - 1)]
            loss = model.train_step(x_start)
            total_loss += loss
        
        avg_loss = total_loss / 50
        if (epoch + 1) % 50 == 0:
            print(f"Epoch {epoch+1}/{n_epochs}, Average Loss: {avg_loss:.4f}")
    
    # 生成样本
    print("\n生成样本：")
    generated = model.sample(n_samples=10)
    print("生成的样本：", [round(v, 2) for v in generated])
    
    # 比较均值和方差
    target_mean = sum(target_data) / len(target_data)
    target_var = sum((x - target_mean) ** 2 for x in target_data) / len(target_data)
    gen_mean = sum(generated) / len(generated)
    gen_var = sum((x - gen_mean) ** 2 for x in generated) / len(generated)
    
    print(f"\n目标分布：均值={target_mean:.2f}, 方差={target_var:.2f}")
    print(f"生成分布：均值={gen_mean:.2f}, 方差={gen_var:.2f}")
