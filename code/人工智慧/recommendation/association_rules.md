# 關聯規則挖掘 (Association Rules Mining)

## 歷史背景

關聯規則挖掘最早由 Agrawal 等人在 1993 年提出，用於發現超市交易數據中的有趣關係，即著名的「購物籃分析」。最經典的例子是「啤酒與尿布」的故事：通過分析發現，週末下午購買尿布的顧客往往也會購買啤酒，超市因此可以將這兩類商品擺放在一起以增加銷售。

Apriori 算法是關聯規則挖掘中最著名的算法，由 Agrawal 和 Srikant 在 1994 年提出。該算法利用「頻繁項集的所有子集也必須是頻繁的」這一性質，大幅減少了搜索空間。

## 核心原理

### 1. 基本概念

給定交易數據集 $D$，每筆交易包含一組物品。

- **支持度 (Support)**：項集 $X$ 出現的頻率
  $$\text{support}(X) = \frac{\text{包含}X\text{的交易數}}{|D|}$$

- **置信度 (Confidence)**：在包含前件 $A$ 的交易中，也包含後件 $B$ 的比例
  $$\text{confidence}(A \Rightarrow B) = \frac{\text{support}(A \cup B)}{\text{support}(A)}$$

- **提升度 (Lift)**：衡量規則的有效性
  $$\text{lift}(A \Rightarrow B) = \frac{\text{confidence}(A \Rightarrow B)}{\text{support}(B)}$$
  若 lift > 1，表示 $A$ 和 $B$ 正相關；若 lift = 1，表示獨立；若 lift < 1，表示負相關。

### 2. Apriori 算法

**核心思想**：頻繁項集的所有子集都是頻繁的；非頻繁項集的超集都是非頻繁的。

**算法步驟**：
1. 掃描數據，找出所有頻繁1項集
2. 使用頻繁 $k-1$ 項集生成候選 $k$ 項集
3. 剪枝：移除包含非頻繁子集的候選
4. 掃描數據計算候選的支持度，找出頻繁 $k$ 項集
5. 重複步驟2-4直到無法生成更大的頻繁項集

### 3. 規則生成

對於每個頻繁項集 $X$，生成非空真子集 $A \subset X$，形成規則 $A \Rightarrow X \setminus A$，計算置信度和提升度，保留滿足閾值的規則。

## 使用範例

```python
from association_rules import apriori, generate_rules, market_basket_analysis

# 交易數據
transactions = [
    ["牛奶", "麵包", "雞蛋"],
    ["牛奶", "麵包", "奶油"],
    ["麵包", "雞蛋", "奶油"],
    ["牛奶", "雞蛋"],
    ["麵包", "奶油"],
    ["牛奶", "麵包", "雞蛋", "奶油"],
    ["牛奶", "麵包"],
    ["雞蛋", "奶油"],
    ["麵包", "雞蛋"],
    ["牛奶", "奶油"]
]

# 挖掘頻繁項集
frequent_itemsets, support_dict = apriori(transactions, min_support=0.3)
print(f"頻繁項集: {frequent_itemsets}")

# 生成關聯規則
rules = generate_rules(frequent_itemsets, support_dict, min_confidence=0.5, num_transactions=len(transactions))
for antecedent, consequent, support, confidence, lift in rules:
    print(f"{antecedent} => {consequent} (支持度={support:.2f}, 置信度={confidence:.2f}, 提升度={lift:.2f})")

# 或直接調用市場籃子分析
market_basket_analysis(transactions, min_support=0.3, min_confidence=0.5)
```

## 參考資料

1. Agrawal, R., Imieliński, T., & Swami, A. (1993). Mining association rules between sets of items in large databases. *SIGMOD*, 207-216.
2. Agrawal, R., & Srikant, R. (1994). Fast algorithms for mining association rules. *VLDB*, 487-499.
3. Han, J., Pei, J., & Yin, Y. (2000). Mining frequent patterns without candidate generation. *SIGMOD*, 1-12.
