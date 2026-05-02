# 反應式智能體 (Reactive Agent)

## 歷史背景

反應式智能體的概念由 Rodney Brooks 於 1986 年在論文《A Robust Layered Control System for a Mobile Robot》中正式提出。當時主流的「符號 AI」主張智能體需要建立世界模型、進行推理規劃，但 Brooks 挑戰了這個觀點。

他提出**包容架構（Subsumption Architecture）**，認為：
- 複雜行為可由簡單行為組合而成
- 不需要複雜的內部表徵
- 「世界就是最好的模型」
- 智能體應直接對感官輸入做出反應

## 反應式 vs 審慎式智能體

| 特性 | 反應式（Reactive） | 審慎式（Deliberative） |
|------|-------------------|----------------------|
| 內部狀態 | 無或極少 | 有完整的世界模型 |
| 決策方式 | 刺激-反應規則 | 符號推理、規劃 |
| 處理速度 | 快（直接映射） | 慢（需要推理） |
| 適應性 | 弱（規則固定） | 強（可重新規劃） |
| 典型應用 | 簡單機器人、即時反應 | 規劃型 AI、任務執行 |

## 核心原理

### 刺激-反應規則

反應式智能體的核心是**條件-動作規則**：

```
if 前方有牆 then 右轉
if 前方空地 then 前進
if 偵測到食物 then 趨近
```

### 包容架構（Subsumption Architecture）

Brooks 提出的多層行為架構：

```
┌─────────────────────────────────┐
│  第 3 層：路徑規劃（最高優先級）│
├─────────────────────────────────┤
│  第 2 層：避障                  │
├─────────────────────────────────┤
│  第 1 層：游蕩（最低優先級）    │
└─────────────────────────────────┘
```

高層行為可以**抑制**（inhibit）低層行為的輸出，實現行為的動態切換。

## 使用範例

### 建立簡單反應式智能體

```python
from agent.reactive_agent import ReactiveAgent, ReactiveRule, Direction

agent = ReactiveAgent("MyAgent")

# 加入規則
agent.add_rule(ReactiveRule(
    condition=lambda p: p['up'] == CellType.GOAL.value,
    action=Direction.UP,
    name="目標在上"
))
```

### 在網格世界執行

```python
from agent.reactive_agent import GridWorld, create_goal_seeking_agent

world = GridWorld(width=10, height=10)
world.set_agent(0, 0)
world.set_goal(9, 9)

agent = create_goal_seeking_agent()

for step in range(100):
    action, reached = agent.run_step(world)
    if reached:
        print(f"到達目標！步數：{step + 1}")
        break
```

## Brooks 的包容架構實例

Brooks 的經典論文中展示了多層行為：

1. **第 1 層：避碰**（Avoidance）- 不撞到東西
2. **第 2 層：游蕩**（Wander）- 隨機移動探索
3. **第 3 層：追光**（Homing）- 朝光源移動

高層行為會「包容」低層行為的輸出，例如當追光源時，避碰規則仍然有效（作為安全網）。

## 在人工智慧中的應用

1. **即時機器人控制**：掃地機器人、無人機避障
2. **遊戲 AI**：非玩家角色（NPC）的反應行為
3. **嵌入式系統**：資源受限環境下的決策
4. **混合式架構**：結合反應式（快速反應）與審慎式（長期規劃）

## 參考資料

- Brooks, R. A. (1986). A Robust Layered Control System for a Mobile Robot. *IEEE Journal of Robotics and Automation*, 2(1), 14-23.
- Brooks, R. A. (1991). Intelligence without Representation. *Artificial Intelligence*, 47(1-3), 139-159.
- Arkin, R. C. (1998). *Behavior-Based Robotics*. MIT Press.
