# 資訊論 — 通道編碼定理 (Channel Coding Theorem)

## 歷史背景

香農第二定理（通道編碼定理）是資訊論的基石之一，於 1948 年提出。該定理證明了在雜訊通道上存在可靠通訊的可能性，只要傳輸速率低於通道容量。

## 核心原理

### 通道編碼定理（香農第二定理）
對於離散無記憶通道，若傳輸速率 R < C（通道容量），則存在編碼方案使得錯誤機率趨近於 0。反之，若 R > C，則任何編碼的錯誤機率都有正的下界。

### 關鍵概念
- **通道容量 C**：可可靠傳輸的最大速率
- **傳輸速率 R = k/n**：k 位元資料編碼為 n 位元碼字
- **典型的隨機編碼**：使用隨機碼本可達到容量

### 重複碼示例
最簡單的編碼：將每個位元重複 n 次
- 速率 R = 1/n
- 當 n → ∞，BER → 0（如果 R < C）
- 實際上效率很低，但理論上可行

### 現代編碼
- 低密度奇偶檢查碼（LDPC）
- 渦輪碼（Turbo Codes）
- 極化碼（Polar Codes）

## 使用範例

```python
from channel_coding_theorem import shannon_limit_demo, simulate_transmission

# 示範香農極限
shannon_limit_demo()

# 模擬特定編碼
bits = [1, 0, 1, 1, 0]
ber, cer = simulate_transmission(bits, 0.1, 7, 1000)
print(f"BER: {ber}, CER: {cer}")
```

## 參考資料

- Shannon, C. E. (1948). A Mathematical Theory of Communication. Bell System Technical Journal.
- Richardson, T., & Urbanke, R. (2008). Modern Coding Theory. Cambridge University Press.
