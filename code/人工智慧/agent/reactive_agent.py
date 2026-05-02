"""
反應式智能體 (Reactive Agent)

歷史背景：
- 1986 年 Rodney Brooks 發表《A Robust Layered Control System for a Mobile Robot》
- 提出包容架構（Subsumption Architecture），推翻當時流行的符號 AI
- 主張「世界就是最好的模型」，不需複雜的內部表徵
- 啟發了行為式機器人學（Behavior-based Robotics）的發展

核心概念：
- 反應式智能體：直接將感知映射為動作，無內部狀態或規劃
- 刺激-反應規則（Stimulus-Response Rules）：if 條件 then 動作
- 包容架構：多層行為，高層行為可抑制低層行為
- 與審慎式智能體（Deliberative Agent）不同，不進行符號推理
"""

from typing import List, Tuple, Optional, Dict, Callable, Any
from enum import Enum
from abc import ABC, abstractmethod


class Direction(Enum):
    """移動方向"""
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)
    STAY = (0, 0)

    def __str__(self):
        return self.name


class CellType(Enum):
    """網格格位類型"""
    EMPTY = 0
    WALL = 1
    GOAL = 2
    AGENT = 3
    DANGER = 4


class GridWorld:
    """簡單網格世界環境"""

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

    def set_cell(self, x: int, y: int, cell_type: CellType):
        """設定格位類型"""
        if 0 <= x < self.width and 0 <= y < self.height:
            self.grid[x][y] = cell_type.value

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

    def move_agent(self, direction: Direction) -> bool:
        """
        移動智能體

        參數：
            direction: 移動方向

        返回：
            是否成功移動
        """
        dx, dy = direction.value
        new_x = self.agent_pos[0] + dx
        new_y = self.agent_pos[1] + dy

        cell_type = self.get_cell(new_x, new_y)
        if cell_type == CellType.WALL.value:
            return False

        self.agent_pos = (new_x, new_y)
        return True

    def is_goal_reached(self) -> bool:
        """檢查是否到達目標"""
        return self.agent_pos == self.goal_pos

    def get_perception(self) -> Dict[str, int]:
        """
        取得智能體的感知資訊
        返回：前方、左方、右方、後方的格位類型
        """
        x, y = self.agent_pos
        return {
            'up': self.get_cell(x, y - 1),
            'down': self.get_cell(x, y + 1),
            'left': self.get_cell(x - 1, y),
            'right': self.get_cell(x + 1, y),
            'current': self.get_cell(x, y),
        }

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
                elif self.grid[x][y] == CellType.DANGER.value:
                    line += "X "
                else:
                    line += ". "
            lines.append(line)
        return "\n".join(lines)


class ReactiveRule:
    """刺激-反應規則"""

    def __init__(self, condition: Callable[[Dict], bool], action: Any, name: str = ""):
        """
        初始化規則

        參數：
            condition: 條件函數，輸入感知，返回布林值
            action: 當條件滿足時執行的動作
            name: 規則名稱（用於除錯）
        """
        self.condition = condition
        self.action = action
        self.name = name

    def matches(self, perception: Dict) -> bool:
        """檢查規則條件是否滿足"""
        return self.condition(perception)


class ReactiveAgent:
    """反應式智能體"""

    def __init__(self, name: str = "ReactiveAgent"):
        """
        初始化反應式智能體

        參數：
            name: 智能體名稱
        """
        self.name = name
        self.rules: List[ReactiveRule] = []
        self.step_count = 0

    def add_rule(self, rule: ReactiveRule):
        """加入一條反應規則"""
        self.rules.append(rule)

    def decide_action(self, perception: Dict) -> Any:
        """
        根據感知決定動作

        依序檢查規則，返回第一個符合條件的動作。
        若無符合規則，返回 STAY。
        """
        for rule in self.rules:
            if rule.matches(perception):
                return rule.action
        return Direction.STAY

    def run_step(self, world: GridWorld) -> Tuple[Any, bool]:
        """
        執行一個步驟

        參數：
            world: 網格世界環境

        返回：
            (執行的動作, 是否到達目標)
        """
        perception = world.get_perception()
        action = self.decide_action(perception)

        if isinstance(action, Direction):
            world.move_agent(action)

        self.step_count += 1
        return action, world.is_goal_reached()

    def __str__(self):
        return f"{self.name} (規則數：{len(self.rules)})"


def create_goal_seeking_agent() -> ReactiveAgent:
    """
    建立一個簡單的目標導向反應式智能體

    規則優先級（依加入順序）：
    1. 若前方是目標，向前移動
    2. 若左方是目標，向左移動
    3. 若右方是目標，向右移動
    4. 若前方是空地，向前移動
    5. 若右方是空地，向右移動
    6. 若左方是空地，向左移動
    7. 否則隨機移動
    """
    agent = ReactiveAgent("GoalSeeker")

    # 規則 1：前方是目標
    agent.add_rule(ReactiveRule(
        condition=lambda p: p['up'] == CellType.GOAL.value,
        action=Direction.UP,
        name="前方是目標-上"
    ))
    agent.add_rule(ReactiveRule(
        condition=lambda p: p['down'] == CellType.GOAL.value,
        action=Direction.DOWN,
        name="前方是目標-下"
    ))
    agent.add_rule(ReactiveRule(
        condition=lambda p: p['left'] == CellType.GOAL.value,
        action=Direction.LEFT,
        name="前方是目標-左"
    ))
    agent.add_rule(ReactiveRule(
        condition=lambda p: p['right'] == CellType.GOAL.value,
        action=Direction.RIGHT,
        name="前方是目標-右"
    ))

    # 規則 2：前方是空地（優先向上）
    agent.add_rule(ReactiveRule(
        condition=lambda p: p['up'] == CellType.EMPTY.value,
        action=Direction.UP,
        name="前方空地-上"
    ))
    agent.add_rule(ReactiveRule(
        condition=lambda p: p['right'] == CellType.EMPTY.value,
        action=Direction.RIGHT,
        name="前方空地-右"
    ))
    agent.add_rule(ReactiveRule(
        condition=lambda p: p['down'] == CellType.EMPTY.value,
        action=Direction.DOWN,
        name="前方空地-下"
    ))
    agent.add_rule(ReactiveRule(
        condition=lambda p: p['left'] == CellType.EMPTY.value,
        action=Direction.LEFT,
        name="前方空地-左"
    ))

    return agent


def create_obstacle_avoiding_agent() -> ReactiveAgent:
    """
    建立避障反應式智能體（遵循右手法則）

    規則：
    1. 若右方是空地，向右移動（沿牆走）
    2. 若前方是空地，向前移動
    3. 若左方是空地，向左移動
    4. 若後方是空地，向後移動
    5. 否則隨機移動
    """
    agent = ReactiveAgent("ObstacleAvoider")

    agent.add_rule(ReactiveRule(
        condition=lambda p: p['right'] == CellType.EMPTY.value,
        action=Direction.RIGHT,
        name="右手法則-右"
    ))
    agent.add_rule(ReactiveRule(
        condition=lambda p: p['up'] == CellType.EMPTY.value,
        action=Direction.UP,
        name="前方空地-上"
    ))
    agent.add_rule(ReactiveRule(
        condition=lambda p: p['left'] == CellType.EMPTY.value,
        action=Direction.LEFT,
        name="前方空地-左"
    ))
    agent.add_rule(ReactiveRule(
        condition=lambda p: p['down'] == CellType.EMPTY.value,
        action=Direction.DOWN,
        name="前方空地-下"
    ))

    return agent


def demo_simple_navigation():
    """簡單導航示範"""
    print("=== 反應式智能體導航示範 ===\n")

    # 建立環境
    world = GridWorld(width=8, height=6)
    world.set_agent(1, 1)
    world.set_goal(6, 4)

    # 加入牆壁
    for i in range(3, 7):
        world.set_cell(3, i, CellType.WALL)

    print("初始狀態：")
    print(world.to_string())
    print()

    # 建立智能體
    agent = create_goal_seeking_agent()
    print(f"智能體：{agent}")
    print("規則：目標導向，優先向目標移動\n")

    # 執行
    max_steps = 20
    for step in range(max_steps):
        action, reached = agent.run_step(world)
        print(f"步驟 {step + 1}：{action}")
        print(world.to_string())
        print()

        if reached:
            print(f"到達目標！共 {step + 1} 步")
            return

    print(f"超過最大步數 {max_steps}，未到達目標")


def demo_obstacle_avoidance():
    """避障示範"""
    print("\n=== 避障反應式智能體示範 ===\n")

    # 建立迷宮環境
    world = GridWorld(width=10, height=8)
    world.set_agent(1, 1)
    world.set_goal(8, 6)

    # 設置障礙物（迷宮牆）
    walls = [
        (3, 1), (3, 2), (3, 3), (3, 4),
        (5, 4), (5, 5), (5, 6),
        (7, 2), (7, 3), (7, 4),
    ]
    for x, y in walls:
        world.set_cell(x, y, CellType.WALL)

    print("迷宮環境：")
    print(world.to_string())
    print()

    # 使用避障智能體
    agent = create_obstacle_avoiding_agent()
    print(f"智能體：{agent}（右手法則）\n")

    max_steps = 30
    for step in range(max_steps):
        action, reached = agent.run_step(world)
        print(f"步驟 {step + 1}：{action}")

        if step % 5 == 0:  # 每 5 步顯示一次狀態
            print(world.to_string())
            print()

        if reached:
            print(f"到達目標！共 {step + 1} 步")
            return

    print(f"超過最大步數 {max_steps}")


def demo_subsumption_layers():
    """
    簡化版包容架構示範
    展示多層行為：避險 > 追目標 > 遊蕩
    """
    print("\n=== 包容架構（簡化版）示範 ===\n")

    world = GridWorld(width=6, height=6)
    world.set_agent(0, 0)
    world.set_goal(5, 5)

    # 加入危險區域
    world.set_cell(2, 2, CellType.DANGER)
    world.set_cell(2, 3, CellType.DANGER)
    world.set_cell(3, 2, CellType.DANGER)

    print("環境（X=危險，G=目標，A=智能體）：")
    print(world.to_string())
    print()

    # 定義三層行為
    class LayeredAgent(ReactiveAgent):
        def __init__(self):
            super().__init__("LayeredAgent")
            self.layers = []

        def add_layer(self, rules: List[ReactiveRule]):
            """加入一層行為（優先級由加入順序決定，後加入的優先級高）"""
            self.layers.append(rules)

        def decide_action(self, perception: Dict) -> Any:
            """從高優先級到低優先級檢查各層"""
            for layer in reversed(self.layers):
                for rule in layer:
                    if rule.matches(perception):
                        return rule.action
            return Direction.STAY

    # 建立分層智能體
    agent = LayeredAgent()

    # 第一層（最低優先級）：遊蕩
    wander_rules = [
        ReactiveRule(
            condition=lambda p: p['up'] == CellType.EMPTY.value,
            action=Direction.UP,
            name="遊蕩-上"
        ),
        ReactiveRule(
            condition=lambda p: p['right'] == CellType.EMPTY.value,
            action=Direction.RIGHT,
            name="遊蕩-右"
        ),
    ]

    # 第二層（中優先級）：追目標
    goal_rules = [
        ReactiveRule(
            condition=lambda p: p['down'] == CellType.GOAL.value,
            action=Direction.DOWN,
            name="追目標-下"
        ),
        ReactiveRule(
            condition=lambda p: p['right'] == CellType.GOAL.value,
            action=Direction.RIGHT,
            name="追目標-右"
        ),
    ]

    # 第三層（最高優先級）：避險
    avoid_rules = [
        ReactiveRule(
            condition=lambda p: p['up'] == CellType.DANGER.value,
            action=Direction.RIGHT,  # 看到上方有危險，改向右
            name="避險-上"
        ),
        ReactiveRule(
            condition=lambda p: p['left'] == CellType.DANGER.value,
            action=Direction.RIGHT,
            name="避險-左"
        ),
    ]

    agent.add_layer(wander_rules)
    agent.add_layer(goal_rules)
    agent.add_layer(avoid_rules)

    print("行為層次（優先級由高到低）：")
    print("  1. 避險（最高）")
    print("  2. 追目標")
    print("  3. 遊蕩（最低）\n")

    max_steps = 20
    for step in range(max_steps):
        perception = world.get_perception()

        # 找出哪層規則被觸發
        action = agent.decide_action(perception)
        world.move_agent(action)

        print(f"步驟 {step + 1}：{action}")

        if step % 4 == 0:
            print(world.to_string())
            print()

        if world.is_goal_reached():
            print(f"到達目標！共 {step + 1} 步")
            return

    print(f"超過最大步數 {max_steps}")


if __name__ == "__main__":
    demo_simple_navigation()
    demo_obstacle_avoidance()
    demo_subsumption_layers()
