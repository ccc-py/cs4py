# 量子隱形傳態 (Quantum Teleportation)

## 歷史背景

量子隱形傳態協定由 Charles Bennett、Gilles Brassard 等人在 1993 年提出，是量子資訊科學的里程碑之一。該協定展示了如何利用糾纏和古典通訊，將一個未知的量子態從一個位置「傳送」到另一個位置，而不需要實際傳送攜帶該態的粒子。

1997 年，Anton Zeilinger 團隊首次在實驗中實現了量子隱形傳態。如今，量子隱形傳態已成為量子通訊網路的基礎技術。

## 核心原理

### 協定步驟
1. **準備糾纏對**：Alice 和 Bob 共享一個 Bell 態 $|\Phi^+\rangle = \frac{1}{\sqrt{2}}(|00\rangle + |11\rangle)$
2. **Bell 態測量**：Alice 對她的兩個量子位元（要傳送的態 + 她的糾纏位元）進行 Bell 測量
3. **古典通訊**：Alice 將她的測量結果（2 bits）告訴 Bob
4. **修正**：Bob 根據接收的 2 bits 對他的糾纏位元應用相應的修正閘

### 量子電路
```
要傳送的態: |ψ⟩ = α|0⟩ + β|1⟩
Alice 的位元: |ψ⟩, |A⟩
Bob 的位元: |B⟩
糾纏對: (|00⟩ + |11⟩)/√2 在 |A⟩ 和 |B⟩ 之間

步驟:
1. CNOT (控制=|ψ⟩, 目標=|A⟩)
2. H on |ψ⟩
3. 測量 |ψ⟩ 和 |A⟩ → 得到 2 bits
4. Bob 根據 bits 應用修正:
   - 00: I
   - 01: X
   - 10: Z
   - 11: XZ
```

### 數學推導
初始三量子位元態：
$$|\psi\rangle \otimes |\Phi^+\rangle = \frac{1}{\sqrt{2}}[\alpha|000\rangle + \alpha|011\rangle + \beta|100\rangle + \beta|111\rangle]$$

經過 CNOT 和 H 後：
$$= \frac{1}{2}[|00\rangle(\alpha|0\rangle + \beta|1\rangle) + |01\rangle(\alpha|1\rangle + \beta|0\rangle) + |10\rangle(\alpha|0\rangle - \beta|1\rangle) + |11\rangle(\alpha|1\rangle - \beta|0\rangle)]$$

## 使用範例

```python
from quantum_teleportation import quantum_teleportation_detailed, QubitState

# 要傳送的態
state = QubitState([1/math.sqrt(2), 1/math.sqrt(2)])  # (|0⟩+|1⟩)/√2

# 執行隱形傳態
bob_state, r1, r2 = quantum_teleportation_detailed(state)
print(f"Bob 的狀態: {bob_state}")
print(f"修正: {r1}, {r2}")
```

## 重要特性

| 特性 | 說明 |
|---|---|
| 不違反 no-cloning theorem | 原始態被摧毀（測量） |
| 需要古典通訊 | 無法超光速通訊 |
| 100% 保真度 | 理論上無誤差 |

## 參考資料

1. Bennett, C. H., et al. (1993). "Teleporting an Unknown Quantum State via Dual Classical and Einstein-Podolsky-Rosen Channels". *Physical Review Letters*, 70(13), 1895-1899.
2. Bouwmeester, D., et al. (1997). "Experimental Quantum Teleportation". *Nature*, 390(6660), 575-579.
3. Nielsen, M. A., & Chuang, I. L. (2010). *Quantum Computation and Quantum Information*. Cambridge University Press.
4. Pirandola, S., et al. (2015). "Advances in Quantum Teleportation". *Nature Photonics*, 9(10), 641-652.
