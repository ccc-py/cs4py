"""
SARSA 演算法 (On-Policy TD Control)

歷史背景：
- 1990 年代早期由 Richard Sutton 等人提出
- 名稱 SARSA 來自 State-Action-Reward-State-Action 的縮寫
- 與 Q-learning 幾乎同時期發展，兩者都是 TD(0) 控制方法
- 主要區別在於：SARSA 是 on-policy，Q-learning 是 off-policy
- 在探索性強的環境中，SARSA 往往學到更安全的策略（避免陷阱）

核心概念：
- SARSA 更新公式：Q(s,a) ← Q(s,a) + α[r + γ·Q(s',a') - Q(s,a)]
- On-policy：行為策略與目標策略相同（都是 ε-greedy）
- 實際採取的下一個動作 a' 被用於更新，而非 max Q(s',a')
- 由於使用 ε-greedy 策略，SARSA 會考慮探索行為，學到的策略更「保守」
- 在迷宮有陷阱的情況下，SARSA 傾向選擇遠離陷阱但安全的路徑
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
    """簡單網格世界環境（供 SARSA 使用）"""

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
            return True, -0.1  # 每步小懲罰

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


class SarsaAgent:
    """SARSA 智能體（On-Policy TD Control）"""

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
        初始化 SARSA 智能體

        參數：
            actions: 可執行的動作列表
            learning_rate: 學習率 α
            discount_factor: 折扣因子 γ
            epsilon: 探索率 ε
            epsilon_decay: ε 衰減率
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

        與 Q-learning 相同，但重點是：
        這個策略既是行為策略（用於探索），也是目標策略（用於更新）
        這就是 on-policy 的含義
        """
        if random.random() < self.epsilon:
            return random.choice(self.actions)

        if state not in self.q_table:
            self.q_table[state] = {a: 0.0 for a in self.actions}

        # 選擇 Q 值最大的動作
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
        next_action: Direction,
        done: bool
    ):
        """
        SARSA 更新

        更新公式：Q(s,a) ← Q(s,a) + α[r + γ·Q(s',a') - Q(s,a)]

        關鍵：使用實際採取的下一個動作 a' 的 Q 值
        這就是 on-policy 的特性：行為與目標一致
        """
        current_q = self.get_q_value(state, action)

        if done:
            target_q = reward
        else:
            # On-policy：使用實際選擇的下一個動作的 Q 值
            next_q = self.get_q_value(next_state, next_action)
            target_q = reward + self.gamma * next_q

        # 更新 Q 值
        new_q = current_q + self.lr * (target_q - current_q)
        if state not in self.q_table:
            self.q_table[state] = {a: 0.0 for a in self.actions}
        self.q_table[state][action] = new_q

    def decay_epsilon(self):
        """衰減探索率"""
        self.epsilon = max(self.epsilon_min, self.epsilon * self.epsilon_decay)

    def get_policy(self) -> Dict[Tuple[int, int], Direction]:
        """取得當前學習到的策略"""
        policy = {}
        for state in self.q_table:
            q_values = self.q_table[state]
            max_q = max(q_values.values())
            best_actions = [a for a, q in q_values.items() if q == max_q]
            policy[state] = random.choice(best_actions)
        return policy


def train_sarsa(
    env: GridWorld,
    agent: SarsaAgent,
    episodes: int = 500,
    max_steps: int = 100,
    start_pos: Tuple[int, int] = (0, 0)
) -> List[float]:
    """
    訓練 SARSA 智能體

    參數：
        env: 環境
        agent: SARSA 智能體
        episodes: 訓練回合數
        max_steps: 每回合最大步數
        start_pos: 起始位置

    返回：
        每回合的累積獎勵列表

    注意：SARSA 需要為每步選擇下一個動作，這就是 S-A-R-S-A 的由來
    """
    rewards_per_episode = []

    for episode in range(episodes):
        env.reset(start_pos)
        state = env.agent_pos
        action = agent.choose_action(state)  # 選擇初始動作
        total_reward = 0

        for step in range(max_steps):
            success, reward = env.move_agent(action)
            next_state = env.agent_pos
            done = env.is_terminal()

            # 選擇下一個動作（關鍵：這個動作會被用於更新）
            if not done:
                next_action = agent.choose_action(next_state)
            else:
                next_action = None

            # SARSA 更新：使用 (s, a, r, s', a')
            agent.learn(state, action, reward, next_state, next_action, done)
            total_reward += reward

            if done:
                break

            # 更新狀態與動作
            state = next_state
            action = next_action

        agent.decay_epsilon()
        rewards_per_episode.append(total_reward)

        if (episode + 1) % 100 == 0:
            print(f"回合 {episode + 1}/{episodes}，ε={agent.epsilon:.3f}，累積獎勵={total_reward:.1f}")

    return rewards_per_episode


def compare_sarsa_vs_qlearning():
    """比較 SARSA 與 Q-learning 的學習結果"""
    print("=== SARSA vs Q-learning 比較 ===\n")

    # 建立相同的環境
    def create_maze():
        env = GridWorld(width=8, height=6)
        env.set_agent(0, 0)
        env.set_goal(7, 5)
        # 陷阱靠近最短路徑
        pits = [(2, 2), (3, 3), (4, 4)]
        for x, y in pits:
            env.set_cell(x, y, CellType.PIT)
        walls = [(3, 1), (3, 2), (5, 3), (5, 4)]
        for x, y in walls:
            env.set_cell(x, y, CellType.WALL)
        return env

    actions = [Direction.UP, Direction.DOWN, Direction.LEFT, Direction.RIGHT]

    # 訓練 SARSA
    print("訓練 SARSA...")
    env_sarsa = create_maze()
    agent_sarsa = SarsaAgent(
        actions=actions,
        learning_rate=0.1,
        discount_factor=0.9,
        epsilon=1.0,
        epsilon_decay=0.995,
        epsilon_min=0.05
    )
    rewards_sarsa = train_sarsa(env_sarsa, agent_sarsa, episodes=500)

    # 匯入 Q-learning 進行比較
    from q_learning import QLearningAgent, train_q_learning

    print("\n訓練 Q-learning...")
    env_q = create_maze()
    agent_q = QLearningAgent(
        actions=actions,
        learning_rate=0.1,
        discount_factor=0.9,
        epsilon=1.0,
        epsilon_decay=0.995,
        epsilon_min=0.05
    )
    rewards_q = train_q_learning(env_q, agent_q, episodes=500)

    # 比較最後 50 回合的平均獎勵
    avg_sarsa = sum(rewards_sarsa[-50:]) / 50
    avg_q = sum(rewards_q[-50:]) / 50

    print(f"\n=== 比較結果 ===")
    print(f"SARSA 最後 50 回合平均獎勵: {avg_sarsa:.2f}")
    print(f"Q-learning 最後 50 回合平均獎勵: {avg_q:.2f}")

    # 比較學到的策略
    print("\nSARSA 學到的策略（較保守，避開陷阱）：")
    policy_sarsa = agent_sarsa.get_policy()
    for y in range(env_sarsa.height):
        line = ""
        for x in range(env_sarsa.width):
            if (x, y) == env_sarsa.goal_pos:
                line += "G "
            elif (x, y) in env_sarsa.pit_positions:
                line += "X "
            elif env_sarsa.grid[x][y] == CellType.WALL.value:
                line += "# "
            elif (x, y) in policy_sarsa:
                action = policy_sarsa[(x, y)]
                line += action.name[0] + " "
            else:
                line += ". "
        print(line)

    print("\nQ-learning 學到的策略（較激進，追求最優）：")
    policy_q = agent_q.get_policy()
    for y in range(env_q.height):
        line = ""
        for x in range(env_q.width):
            if (x, y) == env_q.goal_pos:
                line += "G "
            elif (x, y) in env_q.pit_positions:
                line += "X "
            elif env_q.grid[x][y] == CellType.WALL.value:
                line += "# "
            elif (x, y) in policy_q:
                action = policy_q[(x, y)]
                line += action.name[0] + " "
            else:
                line += ". "
        print(line)


def demo_sarsa():
    """SARSA 示範"""
    print("=== SARSA 迷宮導航示範 ===\n")

    # 建立環境（有多個陷阱）
    env = GridWorld(width=8, height=6)
    env.set_agent(0, 0)
    env.set_goal(7, 5)

    # 設定陷阱（靠近路徑）
    pits = [(2, 2), (3, 3), (4, 4), (5, 2)]
    for x, y in pits:
        env.set_cell(x, y, CellType.PIT)

    # 設定牆壁
    walls = [(3, 1), (3, 2), (5, 3), (5, 4)]
    for x, y in walls:
        env.set_cell(x, y, CellType.WALL)

    print("環境佈局（A=智能體，G=目標，X=陷阱，#=牆）：")
    print(env.to_string())
    print()

    # 建立 SARSA 智能體
    actions = [Direction.UP, Direction.DOWN, Direction.LEFT, Direction.RIGHT]
    agent = SarsaAgent(
        actions=actions,
        learning_rate=0.1,
        discount_factor=0.9,
        epsilon=1.0,
        epsilon_decay=0.995,
        epsilon_min=0.05
    )

    print("開始訓練 SARSA（On-Policy）...")
    print(f"學習率 α=0.1，折扣因子 γ=0.9")
    print(f"初始 ε=1.0，衰減率=0.995\n")

    # 訓練
    rewards = train_sarsa(env, agent, episodes=500, max_steps=100, start_pos=(0, 0))

    print(f"\n訓練完成！最終 ε={agent.epsilon:.3f}")
    print(f"Q-table 大小：{len(agent.q_table)} 個狀態\n")

    # 使用學習到的策略測試
    print("使用學習到的策略執行（無探索）：")
    env.reset((0, 0))
    agent.epsilon = 0  # 關閉探索
    state = env.agent_pos
    action = agent.choose_action(state)
    max_test_steps = 20

    for step in range(max_test_steps):
        print(f"步驟 {step + 1}：{action.name}")
        print(env.to_string())
        print()

        success, _ = env.move_agent(action)
        state = env.agent_pos

        if env.is_goal_reached():
            print(f"成功到達目標！共 {step + 1} 步")
            break

        if env.is_terminal():
            print("掉入陷阱！")
            break

        action = agent.choose_action(state)
    else:
        print(f"超過最大步數 {max_test_steps}")


if __name__ == "__main__":
    demo_sarsa()
    compare_sarsa_vs_qlearning()
