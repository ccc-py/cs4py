# BDI 智能體架構

## 歷史背景

BDI（Belief-Desire-Intention）架構源於 **Michael Bratman** 1987 年的哲學著作《Intention, Plans, and Practical Reason》，他提出人類的行動理性需要三個要素：信念、慾望、意圖。

1990 年代，**Anand Rao** 與 **Michael Georgeff** 將 Bratman 的理論形式化為可計算的 BDI 架構：

- **1991**：Rao & Georgeff 發表 BDI 邏輯模型，定義了 BDI 的形式語意
- **1990s**：開發 **PRS（Procedural Reasoning System）**，第一個實用的 BDI 系統
- **後續發展**：dMARS、JACK、Jadex 等 BDI 平台廣泛應用於工業界

### 應用領域

BDI 架構特別適合需要「慎思（Deliberation）」與「反應（Reaction）」並存的系統：

- **多智能體系統（MAS）**：澳洲的空運模擬系統（1990s）
- **機器人**：自主導航與任務執行
- **工業自動化**：流程控制與異常處理
- **遊戲 AI**：NPC 的動態決策

## 核心概念

### BDI 三元組

```
Belief（信念）：智能體對世界的認知
    ↓ 感知
Desire（慾望）：智能體想要達成的目標
    ↓ 慎思（Deliberation）
Intention（意圖）：智能體承諾執行的計畫
    ↓ 執行
Action（動作）：實際執行的行為
```

### 1. Belief（信念）

智能體對當前世界的認知，包括：
- 自身位置、狀態
- 環境中的物體與其狀態
- 歷史資訊（已完成的任務等）

信念會隨著感知（perception）持續更新。

### 2. Desire（慾望）

智能體想要達成的目標，特點：
- 可能有多個慾望同時存在
- 慾望之間可能衝突（例如：要快又要省油）
- 每個慾望有優先級（priority）

**慾望生成**：根據當前信念產生新的目標。例如，看到包裹就產生「配送包裹」的慾望。

### 3. Intention（意圖）

從慾望中選出、並承諾執行的目標，特點：
- 智能體「承諾」要完成的目標
- 會持續執行直到完成或失敗
- 每個意圖關聯一個「計畫（Plan）」

**意圖的承諾性**：一旦選為意圖，智能體會持續執行，不會因為新慾望的出現而輕易放棄。

### 4. Plan（計畫）

達成目標的具體步驟，包含：
- 一系列動作（Action）的序列
- 每個動作有前置條件（precondition）與效果（effect）
- 計畫庫（Plan Library）：針對不同目標的可用計畫集合

### 5. BDI 循環（BDI Loop）

```
┌─────────────────────────────────┐
│          BDI 循環              │
│  ┌─────────────────────────┐   │
│  │ 1. 更新信念（感知）     │   │
│  └───────────┬─────────────┘   │
│              ↓                  │
│  ┌─────────────────────────┐   │
│  │ 2. 生成慾望             │   │
│  └───────────┬─────────────┘   │
│              ↓                  │
│  ┌─────────────────────────┐   │
│  │ 3. 慎思（選擇目標）     │   │
│  └───────────┬─────────────┘   │
│              ↓                  │
│  ┌─────────────────────────┐   │
│  │ 4. 手段目的推理（選計畫）│   │
│  └───────────┬─────────────┘   │
│              ↓                  │
│  ┌─────────────────────────┐   │
│  │ 5. 執行意圖（執行動作） │   │
│  └───────────┬─────────────┘   │
│              ↓                  │
│  檢查意圖狀態 → 完成/失敗       │
│              ↓                  │
│         回到步驟 1               │
└─────────────────────────────────┘
```

## 程式碼架構說明

### 核心類別

#### `Belief` - 信念
```python
@dataclass
class Belief:
    agent_location: Optional[Location]  # 智能體位置
    packages: Dict[str, Package]         # 包裹資訊
    locations: Dict[str, Location]       # 地點資訊
    delivery_history: List[str]          # 配送歷史
    obstacles: Set[Tuple[int, int]]      # 障礙物
```

#### `Desire` - 慾望
```python
@dataclass
class Desire:
    id: str                    # 唯一識別碼
    description: str           # 描述
    priority: int              # 優先級（越大越優先）
    precondition: Callable     # 前置條件函數
    achieved: bool             # 是否已完成
```

#### `Plan` 與 `Action` - 計畫與動作
```python
@dataclass
class Action:
    name: str                             # 動作名稱
    preconditions: List[Callable]          # 前置條件
    effects: List[Callable]                # 執行效果

@dataclass
class Plan:
    name: str                 # 計畫名稱
    goal: str                 # 要達成的目標
    steps: List[Action]       # 動作序列
    current_step: int         # 當前執行步驟
```

#### `BDIAgent` - BDI 智能體
主要方法：
- `update_beliefs(world)`：從環境更新信念
- `generate_desires()`：根據信念生成慾望
- `deliberate()`：慎思，選擇要執行的慾望
- `means_ends_reasoning(desire)`：為慾望選擇計畫
- `execute_intentions(world)`：執行當前所有意圖
- `bdi_cycle(world)`：執行完整 BDI 循環

## 使用範例

### 基本使用

```python
from bdi_agent import BDIAgent, DeliveryWorld

# 建立環境
world = DeliveryWorld()
world.add_location("倉庫", 1, 1)
world.add_location("車站", 5, 3)
world.add_package("pkg1", "車站")
world.set_agent_location("倉庫")

# 建立 BDI 智能體
agent = BDIAgent("配送員")
agent.update_beliefs(world)  # 初始化信念

# 加入計畫到計畫庫
# ...

# 執行 BDI 循環
for i in range(10):
    results = agent.bdi_cycle(world)
    print("\n".join(results))
```

### 配送任務示範

執行程式：
```bash
python bdi_agent.py
```

輸出範例：
```
=== BDI 智能體 - 配送任務示範 ===

=== BDI 循環 #1 ===
信念更新: 位置=倉庫
慾望數: 3
選擇慾望: 配送包裹 pkg1 到 車站
採用意圖: 配送pkg1計畫
執行意圖 (1 個):
  → 執行: 移動到 車站
  → 執行: 配送 pkg1

✓ 完成: 配送包裹 pkg1 到 車站
```

## BDI 與其他架構的比較

| 特性 | 反應式（Reactive） | 審慎式（Deliberative） | BDI |
|------|-------------------|----------------------|-----|
| 反應速度 | 快 | 慢 | 中等（可快速反應） |
| 長期規劃 | 無 | 有 | 有（通過意圖） |
| 目標管理 | 無 | 有 | 有（通過慾望） |
| 可解釋性 | 低 | 中等 | 高（信念-慾望-意圖皆可檢視） |
| 適用場景 | 簡單反射行為 | 複雜規劃問題 | 需要兼顧反應與規劃的任務 |

## 參考資料

1. **原始文獻**：
   - Bratman, M. E. (1987). *Intention, Plans, and Practical Reason*. Harvard University Press.
   - Rao, A. S., & Georgeff, M. P. (1991). *Modeling rational agents within a BDI-architecture*. KR'91.
   - Rao, A. S., & Georgeff, M. P. (1992). *An abstract architecture for rational agents*. KR'92.

2. **教科書**：
   - Wooldridge, M. (2009). *An Introduction to MultiAgent Systems* (2nd ed.). Wiley. Chapter 3.
   - Bordini, R. H., et al. (2007). *Programming Multi-Agent Systems in AgentSpeak using Jason*. Wiley.

3. **平台與工具**：
   - **Jason**：基於 AgentSpeak(L) 的 BDI 平台 [http://jason.sourceforge.net/](http://jason.sourceforge.net/)
   - **JACK**：商用 BDI 平台 [https://www.agent-software.com/](https://www.agent-software.com/)
   - **Jadex**：基於 Java 的 BDI 框架 [https://www.activecomponents.org/](https://www.activecomponents.org/)

4. **線上資源**：
   - [BDI Architecture Overview (Wikipedia)](https://en.wikipedia.org/wiki/BDI_software_model)
   - [An Introduction to BDI Agents (Video)](https://www.youtube.com/)
   - [Agent-Oriented Programming](https://www.cs.mcgill.ca/~jorg/teaching/ai/lectures/11/bdi.html)

5. **應用案例**：
   - Air Combat Simulation (Rao, Georgeff, 1991)
   - Urban Traffic Management (AUML, 2000s)
   - Autonomous Robots (ROS + BDI, 2010s)
