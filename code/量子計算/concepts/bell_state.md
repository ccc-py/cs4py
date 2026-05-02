# Bell 態 (Bell States)

## 歷史背景

Bell 態是量子力學中最著名的糾纏態，以物理學家 John Bell 命名。1964 年，Bell 提出了著名的 Bell 不等式，證明了量子力學的預測無法用任何局部隱變數理論解釋。

1982 年，Alain Aspect 的實驗首次確認了 Bell 不等式的違反，驗證了量子糾纏的真實存在。四個 Bell 態構成了兩量子位元系統的最大糾纏基底。

## 核心原理

### 四個 Bell 態
兩量子位元的最大糾纏態有四個：

1. $|\Phi^+\rangle = \frac{1}{\sqrt{2}}(|00\rangle + |11\rangle)$
2. $|\Phi^-\rangle = \frac{1}{\sqrt{2}}(|00\rangle - |11\rangle)$
3. $|\Psi^+\rangle = \frac{1}{\sqrt{2}}(|01\rangle + |10\rangle)$
4. $|\Psi^-\rangle = \frac{1}{\sqrt{2}}(|01\rangle - |10\rangle)$

### 糾纏特性
- **不可分離**：無法寫成兩個單量子位元態的張量積
- **完美相關**：測量其中一個，另一個立即確定
- **非局域性**：這種關聯與距離無關

### Bell 不等式 (CHSH)
Classical bound: $|E(a,b) - E(a,b') + E(a',b) + E(a',b')| \leq 2$

Quantum bound: $\leq 2\sqrt{2} \approx 2.828$

## 使用範例

```python
from bell_state import create_bell_state_phi_plus, get_all_bell_states

# 建立 |Φ⁺⟩
phi_plus = create_bell_state_phi_plus()
print(phi_plus)  # (0.707+0j)|00⟩ + (0.707+0j)|11⟩

# 取得所有 Bell 態
bell_states = get_all_bell_states()
for state in bell_states:
    print(state)
```

## 應用

| 應用 | 說明 |
|---|---|
| 量子隱形傳態 | 需要 Bell 態作為資源 |
| 超密編碼 | 傳送 2 bits 只用 1 qubit |
| 量子密鑰分發 | E91 協定使用 Bell 不等式 |
| 量子計算 | 糾纏是量子優勢的來源 |

## 參考資料

1. Bell, J. S. (1964). "On the Einstein Podolsky Rosen Paradox". *Physics Physique Fizika*, 1(3), 195-200.
2. Aspect, A., et al. (1982). "Experimental Realization of Einstein-Podolsky-Rosen-Bohm Gedankenexperiment: A New Violation of Bell's Inequalities". *Physical Review Letters*, 49(2), 91-94.
3. Nielsen, M. A., & Chuang, I. L. (2010). *Quantum Computation and Quantum Information*. Cambridge University Press.
4. Clauser, J. F., et al. (1969). "Proposed Experiment to Test Local Hidden-Variable Theories". *Physical Review Letters*, 23(15), 880-884.
