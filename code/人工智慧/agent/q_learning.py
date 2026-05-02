"""
Q-learning 演算法 (Model-Free 強化學習)

歷史背景：
- 1989 年 Christopher Watkins 在博士論文《Learning from Delayed Rewards》中提出
- 首個結合時序差分（TD）學習與動作價值（Action-Value）的方法
- 屬於 off-policy 學習，學習最優策略的同時遵循探索策略
- 奠定了現代強化學習的基礎，是 DQN 等深度 RL 方法的前身

核心概念：
- Q-table：狀態-動作價值表，儲存每個狀態下各動作的預期累積獎勵
- Q-learning 更新公式：Q(s,a) ← Q(s,a) + α[r + γ·max_a' Q(s',a') - Q(s,a)]
- ε-greedy 策略：以 ε 機率隨機探索，以 1-ε 機率選擇當前最優動作
- 探索衰減（Exploration Decay）：隨訓練進行逐漸降低 ε，平衡探索與利用
- Off-policy：學習目標是最優策略（greedy），但實際行為遵循 ε-greedy
"""

from typing import Dict, Tuple, Optional, List, Any
from enum import Enum
import random


class Direction(Enum):
    """移動方向"""
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)

    def __str__(self):
        return self.name


class CellType(Enum):
    """網格格位類型"""
    EMPTY = 0
    WALL = 1
    GOAL = 2
    AGENT = 3
    PIT = 4  # 陷阱（負獎勵）


class GridWorld:
    """簡單網格世界環境（供 Q-learning 使用）"""

    def __init__(self, width: int, height: int):
        """
        初始化網格世界

        參數：
            width: 寬度
            height: 高度
        """
        self.width = width
        self.height = height
        self.grid: List[List[int]] = [[CellType.EMPTY.value] * height for _ in range(width)]
        self.agent_pos: Tuple[int, int] = (0, 0)
        self.goal_pos: Optional[Tuple[int, int]] = None
        self.pit_positions: List[Tuple[int, int]] = []

    def set_cell(self, x: int, y: int, cell_type: CellType):
        """設定格位類型"""
        if 0 <= x < self.width and 0 <= y < self.height:
            self.grid[x][y] = cell_type.value
            if cell_type == CellType.PIT:
                self.pit_positions.append((x, y))

    def set_agent(self, x: int, y: int):
        """設定智能體位置"""
        self.agent_pos = (x, y)

    def set_goal(self, x: int, y: int):
        """設定目標位置"""
        self.goal_pos = (x, y)
        self.set_cell(x, y, CellType.GOAL)

    def get_cell(self, x: int, y: int) -> int:
        """取得格位類型值"""
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.grid[x][y]
        return CellType.WALL.value  # 邊界視為牆

    def move_agent(self, direction: Direction) -> Tuple[bool, float]:
        """
        移動智能體

        參數：
            direction: 移動方向

        返回：
            (是否成功移動, 獎勵值)
        """
        dx, dy = direction.value
        new_x = self.agent_pos[0] + dx
        new_y = self.agent_pos[1] + dy

        cell_type = self.get_cell(new_x, new_y)

        # 撞牆
        if cell_type == CellType.WALL.value:
            return False, -0.5

        # 移動
        self.agent_pos = (new_x, new_y)

        # 計算獎勵
        if (new_x, new_y) == self.goal_pos:
            return True, 10.0  # 到達目標
        elif (new_x, new_y) in self.pit_positions:
            return True, -5.0  # 掉入陷阱
        else:
            return True, -0.1  # 每步小懲罰（鼓勵最短路徑）

    def is_goal_reached(self) -> bool:
        """檢查是否到達目標"""
        return self.agent_pos == self.goal_pos

    def is_terminal(self) -> bool:
        """檢查是否終止（到達目標或陷阱）"""
        pos = self.agent_pos
        return pos == self.goal_pos or pos in self.pit_positions

    def reset(self, start_pos: Optional[Tuple[int, int]] = None):
        """重置智能體到起始位置"""
        if start_pos:
            self.agent_pos = start_pos
        else:
            self.agent_pos = (0, 0)

    def to_string(self) -> str:
        """將世界狀態轉為字串"""
        lines = []
        for y in range(self.height):
            line = ""
            for x in range(self.width):
                if (x, y) == self.agent_pos:
                    line += "A "
                elif (x, y) == self.goal_pos:
                    line += "G "
                elif self.grid[x][y] == CellType.WALL.value:
                    line += "# "
                elif self.grid[x][y] == CellType.PIT.value:
                    line += "X "
                else:
                    line += ". "
            lines.append(line)
        return "\n".join(lines)


class QLearningAgent:
    """Q-learning 智能體"""

    def __init__(
        self,
        actions: List[Direction],
        learning_rate: float = 0.1,
        discount_factor: float = 0.9,
        epsilon: float = 1.0,
        epsilon_decay: float = 0.995,
        epsilon_min: float = 0.01
    ):
        """
        初始化 Q-learning 智能體

        參數：
            actions: 可執行的動作列表
            learning_rate: 學習率 α，控制新資訊覆蓋舊資訊的速度
            discount_factor: 折扣因子 γ，衡量未來獎勵的重要性
            epsilon: 探索率 ε，隨機探索的機率
            epsilon_decay: ε 衰減率，每回合乘以此值
            epsilon_min: ε 的最小值
        """
        self.actions = actions
        self.lr = learning_rate
        self.gamma = discount_factor
        self.epsilon = epsilon
        self.epsilon_decay = epsilon_decay
        self.epsilon_min = epsilon_min
        self.q_table: Dict[Tuple[int, int], Dict[Direction, float]] = {}

    def get_q_value(self, state: Tuple[int, int], action: Direction) -> float:
        """取得 Q 值，若不存在則返回 0"""
        if state not in self.q_table:
            self.q_table[state] = {a: 0.0 for a in self.actions}
        return self.q_table[state].get(action, 0.0)

    def choose_action(self, state: Tuple[int, int]) -> Direction:
        """
        ε-greedy 策略選擇動作

        以 ε 機率隨機探索，以 1-ε 機率選擇當前 Q 值最大的動作
        """
        if random.random() < self.epsilon:
            return random.choice(self.actions)

        if state not in self.q_table:
            self.q_table[state] = {a: 0.0 for a in self.actions}

        # 選擇 Q 值最大的動作（若有相同則隨機選）
        q_values = self.q_table[state]
        max_q = max(q_values.values())
        best_actions = [a for a, q in q_values.items() if q == max_q]
        return random.choice(best_actions)

    def learn(
        self,
        state: Tuple[int, int],
        action: Direction,
        reward: float,
        next_state: Tuple[int, int],
        done: bool
    ):
        """
        Q-learning 更新

        更新公式：Q(s,a) ← Q(s,a) + α[r + γ·max_a' Q(s',a') - Q(s,a)]

        關鍵：即使實際採取的動作不是 next_action，仍使用 max Q(s',a') 更新
        這就是 off-policy 的特性
        """
        current_q = self.get_q_value(state, action)

        if done:
            target_q = reward
        else:
            # Off-policy：使用下一狀態的最大 Q 值
            next_q_values = [self.get_q_value(next_state, a) for a in self.actions]
            target_q = reward + self.gamma * max(next_q_values)

        # 更新 Q 值
        new_q = current_q + self.lr * (target_q - current_q)
        if state not in self.q_table:
            self.q_table[state] = {a: 0.0 for a in self.actions}
        self.q_table[state][action] = new_q

    def decay_epsilon(self):
        """衰減探索率"""
        self.epsilon = max(self.epsilon_min, self.epsilon * self.epsilon_decay)

    def get_policy(self) -> Dict[Tuple[int, int], Direction]:
        """取得當前學習到的策略（每個狀態選擇 Q 值最大的動作）"""
        policy = {}
        for state in self.q_table:
            q_values = self.q_table[state]
            max_q = max(q_values.values())
            best_actions = [a for a, q in q_values.items() if q == max_q]
            policy[state] = random.choice(best_actions)
        return policy


def train_q_learning(
    env: GridWorld,
    agent: QLearningAgent,
    episodes: int = 500,
    max_steps: int = 100,
    start_pos: Tuple[int, int] = (0, 0)
) -> List[float]:
    """
    訓練 Q-learning 智能體

    參數：
        env: 環境
        agent: Q-learning 智能體
        episodes: 訓練回合數
        max_steps: 每回合最大步數
        start_pos: 起始位置

    返回：
        每回合的累積獎勵列表
    """
    rewards_per_episode = []

    for episode in range(episodes):
        env.reset(start_pos)
        state = env.agent_pos
        total_reward = 0

        for step in range(max_steps):
            action = agent.choose_action(state)
            success, reward = env.move_agent(action)
            next_state = env.agent_pos
            done = env.is_terminal()

            agent.learn(state, action, reward, next_state, done)
            total_reward += reward
            state = next_state

            if done:
                break

        agent.decay_epsilon()
        rewards_per_episode.append(total_reward)

        if (episode + 1) % 100 == 0:
            print(f"回合 {episode + 1}/{episodes}，ε={agent.epsilon:.3f}，累積獎勵={total_reward:.1f}")

    return rewards_per_episode


def demo_q_learning():
    """Q-learning 示範"""
    print("=== Q-learning 迷宮導航示範 ===\n")

    # 建立環境
    env = GridWorld(width=8, height=6)
    env.set_agent(0, 0)
    env.set_goal(7, 5)

    # 設定陷阱
    pits = [(2, 2), (3, 3), (4, 4)]
    for x, y in pits:
        env.set_cell(x, y, CellType.PIT)

    # 設定牆壁
    walls = [(3, 1), (3, 2), (5, 3), (5, 4)]
    for x, y in walls:
        env.set_cell(x, y, CellType.WALL)

    print("環境佈局（A=智能體，G=目標，X=陷阱，#=牆）：")
    print(env.to_string())
    print()

    # 建立 Q-learning 智能體
    actions = [Direction.UP, Direction.DOWN, Direction.LEFT, Direction.RIGHT]
    agent = QLearningAgent(
        actions=actions,
        learning_rate=0.1,
        discount_factor=0.9,
        epsilon=1.0,
        epsilon_decay=0.995,
        epsilon_min=0.05
    )

    print("開始訓練...")
    print(f"學習率 α=0.1，折扣因子 γ=0.9")
    print(f"初始 ε=1.0，衰減率=0.995\n")

    # 訓練
    rewards = train_q_learning(env, agent, episodes=500, max_steps=100, start_pos=(0, 0))

    print(f"\n訓練完成！最終 ε={agent.epsilon:.3f}")
    print(f"Q-table 大小：{len(agent.q_table)} 個狀態\n")

    # 顯示學習到的策略
    print("學習到的策略（Greedy）：")
    policy = agent.get_policy()
    for y in range(env.height):
        line = ""
        for x in range(env.width):
            if (x, y) == env.goal_pos:
                line += "G "
            elif (x, y) in env.pit_positions:
                line += "X "
            elif env.grid[x][y] == CellType.WALL.value:
                line += "# "
            elif (x, y) in policy:
                action = policy[(x, y)]
                line += action.name[0] + " "
            else:
                line += ". "
        print(line)
    print()

    # 使用學習到的策略測試
    print("使用學習到的策略執行（無探索）：")
    env.reset((0, 0))
    agent.epsilon = 0  # 關閉探索
    state = env.agent_pos
    max_test_steps = 20

    for step in range(max_test_steps):
        action = agent.choose_action(state)
        print(f"步驟 {step + 1}：{action.name}")
        print(env.to_string())
        print()

        success, _ = env.move_agent(action)
        state = env.agent_pos

        if env.is_goal_reached():
            print(f"成功到達目標！共 {step + 1} 步")
            break
        elif env.is_terminal():
            print("掉入陷阱！")
            break
    else:
        print(f"超過最大步數 {max_test_steps}")


def compare_learning_curve():
    """比較不同學習率的學習曲線"""
    print("\n=== 學習率比較 ===\n")

    env = GridWorld(width=6, height=6)
    env.set_agent(0, 0)
    env.set_goal(5, 5)
    env.set_cell(3, 3, CellType.PIT)

    actions = [Direction.UP, Direction.DOWN, Direction.LEFT, Direction.RIGHT]

    learning_rates = [0.01, 0.1, 0.5]
    results = {}

    for lr in learning_rates:
        agent = QLearningAgent(
            actions=actions,
            learning_rate=lr,
            discount_factor=0.9,
            epsilon=1.0,
            epsilon_decay=0.995,
            epsilon_min=0.05
        )

        rewards = train_q_learning(env, agent, episodes=200, max_steps=50)
        results[lr] = rewards
        print(f"學習率 {lr}：最後 10 回合平均獎勵 = {sum(rewards[-10:])/10:.2f}")

    print("\n結論：較大的學習率收斂快但可能震盪，較小的學習率穩定但收斂慢")


if __name__ == "__main__":
    demo_q_learning()
    compare_learning_curve()
