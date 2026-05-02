# 卷積神經網路 (Convolutional Neural Network)

## 歷史背景

CNN 的起源可追溯至 1980 年代 Kunihiko Fukushima 提出的 Neocognitron。1989 年 Yann LeCun 將反向傳播應用於卷積層，提出 LeNet。1998 年 LeNet-5 成功應用於手寫郵政編碼識別。2012 年 AlexNet 在 ImageNet 競賽中取得突破性成果，標誌著深度學習時代的到來。後續的 VGG、GoogLeNet、ResNet 等架構不斷推動計算機視覺的發展。

## 核心原理

### 卷積層 (Conv2D)

卷積操作使用濾核 (Kernel) 在輸入圖像上滑動，計算局部區域的加權和：

```
Output[i, j] = Σ Σ Input[i+u, j+v] * Kernel[u, v]
```

**優點**：
- **局部感受野**：每個神經元只連接局部區域，保留空間結構
- **權值共享**：同一濾核在全圖使用，大幅減少參數量
- **平移不變性**：特徵檢測器在全圖有效

### 池化層 (Pooling)

池化層進行下採樣，常見操作：
- **Max Pooling**：取區域最大值，保留最顯著特徵
- **Average Pooling**：取區域平均值，平滑特徵

### 反向傳播

CNN 的反向傳播需要計算：
1. **d_weights**：∂L/∂W = Σ ∂L/∂Output * Input_padded
2. **d_input**：∂L/∂Input = 濾核旋轉 180 度後與 ∂L/∂Output 做卷積

## 使用範例

```python
from nn.cnn import CNN, ConvLayer, ReLULayer, LinearLayer, Softmax

# 建立網路
net = CNN()
net.layers.append(ConvLayer(c_in=1, c_out=4, k_size=3))
net.layers.append(ReLULayer())
net.layers.append(LinearLayer(n_in=..., n_out=10)) # 根據輸入尺寸計算

# 訓練
out = net.forward(image)
loss, d_loss = Softmax.loss(Softmax.forward(out), target)
net.backward(d_loss, lr=0.01)
```

## 參考資料

- LeCun, Y., et al. (1998). Gradient-based learning applied to document recognition.
- Krizhevsky, A., et al. (2012). ImageNet classification with deep convolutional neural networks.
