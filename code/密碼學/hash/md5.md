# MD5 雜湊函數 (MD5 Hash Function)

## 歷史背景
MD5（Message-Digest Algorithm 5）由羅納德·李維斯特（Ronald Rivest）於1991年設計，發表於 RFC 1321。它是 MD4 的改進版本，曾被廣泛用於文件完整性驗證和數位簽章。

然而，MD5 的安全性在2000年代後期被徹底破解：
- 2004年：王小雲團隊發現快速碰撞攻擊
- 2008年：研究人員展示偽造 SSL 證書
- 2012年：建議全面棄用 MD5

## 核心原理
MD5 將任意長度輸入轉換為128位（16字節）雜湊值：

1. **訊息填充**：附加 0x80、填充 0、附加長度（64位小端序）
2. **初始化**：4個32位狀態變數
3. **壓縮函數**：64輪操作，分4輪每輪16次
   - 使用4個邏輯函數：F, G, H, I
   - 64個常數（正弦函數）
4. **輸出**：4個32位字串接

## 使用範例
```python
from md5 import md5_hex

# 計算 MD5
message = b"hello world"
hash_value = md5_hex(message)
print(f"MD5: {hash_value}")

# 空字串
empty = md5_hex(b"")
print(f"MD5(''): {empty}")
```

## 參考資料
- [MD5 - Wikipedia](https://en.wikipedia.org/wiki/MD5)
- Rivest, R. (1992). *RFC 1321 - The MD5 Message-Digest Algorithm*
- Wang, X., & Yu, H. (2005). *How to Break MD5 and Other Hash Functions*
