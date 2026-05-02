# 樸素貝氏分類器 (Naive Bayes Classifier)

## 歷史背景

樸素貝氏分類器基於托馬斯·貝葉斯 (Thomas Bayes, 1702-1761) 的貝葉斯定理。貝葉斯的論文《An Essay towards solving a Problem in the Doctrine of Chances》於 1763 年由 Richard Price 整理並發表，奠定了貝葉斯機率的基礎。

1950 年代，R. A. Fisher 等人將貝葉斯方法應用於統計分類問題。到了 1990 年代，隨著電子郵件的普及，樸素貝氏成為垃圾郵件過濾的主流方法（如 Sahami et al. 1998 年的經典論文）。

由於其簡單、高效且在許多實際問題上表現良好，樸素貝氏至今仍是文字分類和垃圾郵件偵測的常用基準模型。

## 核心原理

### 貝葉斯定理

貝葉斯定理描述了在已知某些條件下，事件發生的機率：

```
P(y|x) = P(x|y) * P(y) / P(x)
```

其中：
- **P(y|x)**：後驗機率，給定特徵 x 時類別 y 的機率
- **P(x|y)**：似然度，給定類別 y 時特徵 x 出現的機率
- **P(y)**：先驗機率，類別 y 出現的機率
- **P(x)**：證據，特徵 x 出現的機率（常數，可忽略）

### 樸素假設

「樸素」(Naive) 來自於一個強假設：**給定類別 y 時，所有特徵 x_i 互相獨立**。

因此：

```
P(x|y) = P(x₁|y) × P(x₂|y) × ... × P(xₙ|y) = Π P(x_i|y)
```

### 多項式模型 (Multinomial NB)

用於離散計數資料（如文字分類中的詞頻）：

```
P(word_i | class) = (count(word_i) + α) / (total_words + α × |vocabulary|)
```

其中 α 為拉普拉斯平滑 (Laplace smoothing) 參數，用於避免零機率問題。

### 高斯模型 (Gaussian NB)

用於連續特徵，假設每個特徵在給定類別下服從高斯分佈：

```
P(x_i | y) = N(x_i | μ_{y,i}, σ²_{y,i})
```

其中 μ 和 σ² 分別為該類別下特徵的均值和方差。

### 對數機率

實作中通常使用對數機率以避免下溢：

```
log P(y|x) ∝ log P(y) + Σ log P(x_i|y)
```

## 使用範例

### 垃圾郵件分類 (MultinomialNB)

```python
from ml.naive_bayes import MultinomialNB

# 訓練資料
documents = [
    "buy now cheap viagra pills",
    "win money now claim your prize",
    "meeting scheduled for tomorrow",
    "please review the attached document",
]
labels = ["spam", "spam", "ham", "ham"]

# 訓練模型
nb = MultinomialNB(alpha=1.0)
nb.fit(documents, labels)

# 預測
test = "free money click here now"
print(nb.predict(test))  # 輸出: spam

# 查看各類別機率
proba = nb.predict_proba(test)
print(proba)  # {'spam': -5.23, 'ham': -8.91}
```

### 連續特徵分類 (GaussianNB)

```python
from ml.naive_bayes import GaussianNB

# 特徵矩陣 X，標籤 y
X = [
    [5.1, 3.5], [4.9, 3.0],  # setosa
    [7.0, 3.2], [6.4, 3.2],  # versicolor
]
y = ["setosa", "setosa", "versicolor", "versicolor"]

# 訓練模型
gnb = GaussianNB()
gnb.fit(X, y)

# 預測
print(gnb.predict([5.0, 3.4]))  # 輸出: setosa
```

## 複雜度

### 多項式樸素貝氏
- **訓練時間**：O(N × M)，N 為文件數，M 為詞彙表大小
- **預測時間**：O(M)，與詞彙表大小成正比
- **空間**：O(C × M)，C 為類別數

### 高斯樸素貝氏
- **訓練時間**：O(N × D)，N 為樣本數，D 為特徵數
- **預測時間**：O(C × D)，C 為類別數，D 為特徵數
- **空間**：O(C × D)

## 優缺點

### 優點
- 訓練和預測速度極快
- 對缺失資料不敏感
- 在小資料集上表現良好
- 適合高維度資料（如文字）

### 缺點
- 特徵獨立假設在現實中通常不成立
- 對於特征相關性強的問題效果較差
- 需要先驗機率準確

## 參考資料

1. Thomas Bayes (1763). "An Essay towards solving a Problem in the Doctrine of Chances"
2. Sahami, M. et al. (1998). "A Bayesian approach to filtering junk e-mail"
3. Manning, C. D. et al. (2008). "Introduction to Information Retrieval" - Chapter 13
4. scikit-learn 文件: https://scikit-learn.org/stable/modules/naive_bayes.html
