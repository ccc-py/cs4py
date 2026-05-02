"""
BDI 智能體架構 (Belief-Desire-Intention)

歷史背景：
- 1990 年代由 Anand Rao 與 Michael Georgeff 基於 Michael Bratman 的哲學理論提出
- Bratman 於 1987 年提出人類行動理性需要 Belief-Desire-Intention 三要素
- Rao & Georgeff 將其形式化為可計算的 BDI 架構（BDI Architecture）
- 最初實作為 PRS（Procedural Reasoning System），後發展為 dMARS、JACK 等系統
- BDI 架構廣泛應用於多智能體系統、機器人、工業自動化等領域

核心概念：
- Belief（信念）：智能體對世界的認知與知識
- Desire（慾望）：智能體想要達成的目標（可能多個，可能有衝突）
- Intention（意圖）：智能體當前承諾執行的計畫
- Plan Library（計畫庫）：達成目標的可選計畫集合
- Deliberation（慎思）：從 Desires 中選擇要轉為 Intentions 的過程
- Means-ends Reasoning（手段目的推理）：為 Intention 選擇合適的 Plan

BDI 循環（BDI Loop）：
1. 更新 Beliefs（感知環境變化）
2. 生成/更新 Desires（產生新的目標）
3. Deliberation（選擇要執行的意圖）
4. Means-ends Reasoning（為意圖選擇計畫）
5. 執行計畫中的動作
6. 檢查意圖是否完成或失敗，若完成則移除
"""

from typing import Dict, List, Optional, Set, Any, Callable, Tuple
from enum import Enum
from dataclasses import dataclass, field
from abc import ABC, abstractmethod
import random


class Location:
    """位置座標"""

    def __init__(self, name: str, x: int, y: int):
        self.name = name
        self.x = x
        self.y = y

    def distance_to(self, other: 'Location') -> float:
        """計算兩點間的曼哈頓距離"""
        return abs(self.x - other.x) + abs(self.y - other.y)

    def __eq__(self, other):
        return isinstance(other, Location) and self.name == other.name

    def __hash__(self):
        return hash(self.name)

    def __repr__(self):
        return f"Location({self.name}, {self.x}, {self.y})"


@dataclass
class Package:
    """包裹"""
    id: str
    destination: Location
    picked_up: bool = False

    def __repr__(self):
        status = "已取件" if self.picked_up else "待取件"
        return f"Package({self.id} → {self.destination.name}, {status})"


@dataclass
class Belief:
    """信念：智能體對世界的認知"""
    agent_location: Optional[Location] = None
    packages: Dict[str, Package] = field(default_factory=dict)
    locations: Dict[str, Location] = field(default_factory=dict)
    delivery_history: List[str] = field(default_factory=list)
    obstacles: Set[Tuple[int, int]] = field(default_factory=set)

    def update_location(self, location: Location):
        """更新智能體位置信念"""
        self.agent_location = location

    def add_package(self, package: Package):
        """加入包裹資訊"""
        self.packages[package.id] = package

    def get_package(self, package_id: str) -> Optional[Package]:
        """取得包裹資訊"""
        return self.packages.get(package_id)

    def mark_package_picked_up(self, package_id: str):
        """標記包裹已取件"""
        if package_id in self.packages:
            self.packages[package_id].picked_up = True

    def add_obstacle(self, x: int, y: int):
        """加入障礙物資訊"""
        self.obstacles.add((x, y))

    def get_known_packages(self) -> List[Package]:
        """取得所有已知包裹"""
        return list(self.packages.values())

    def get_pending_packages(self) -> List[Package]:
        """取得待配送的包裹（未取件）"""
        return [p for p in self.packages.values() if not p.picked_up]


@dataclass
class Desire:
    """慾望：智能體想要達成的目標"""
    id: str
    description: str
    priority: int = 1  # 優先級（數字越大越優先）
    precondition: Optional[Callable[[Belief], bool]] = None
    achieved: bool = False

    def is_achievable(self, belief: Belief) -> bool:
        """檢查慾望是否可達成（滿足前置條件）"""
        if self.precondition is None:
            return True
        return self.precondition(belief)

    def __repr__(self):
        status = "已完成" if self.achieved else "進行中"
        return f"Desire({self.description}, 優先級={self.priority}, {status})"


@dataclass
class Action:
    """動作"""
    name: str
    preconditions: List[Callable[[Belief], bool]] = field(default_factory=list)
    effects: List[Callable[[Belief], None]] = field(default_factory=list)

    def is_applicable(self, belief: Belief) -> bool:
        """檢查動作是否可執行（滿足前置條件）"""
        return all(precond(belief) for precond in self.preconditions)

    def execute(self, belief: Belief) -> bool:
        """執行動作，返回是否成功"""
        if not self.is_applicable(belief):
            return False
        for effect in self.effects:
            effect(belief)
        return True

    def __repr__(self):
        return f"Action({self.name})"


@dataclass
class Plan:
    """計畫：一系列動作的序列"""
    name: str
    goal: str  # 此計畫要達成的目標描述
    steps: List[Action] = field(default_factory=list)
    current_step: int = 0

    def is_complete(self) -> bool:
        """檢查計畫是否完成"""
        return self.current_step >= len(self.steps)

    def get_current_action(self) -> Optional[Action]:
        """取得當前應執行的動作"""
        if self.current_step < len(self.steps):
            return self.steps[self.current_step]
        return None

    def advance(self):
        """前進到下一個動作"""
        self.current_step += 1

    def reset(self):
        """重置計畫（重新開始）"""
        self.current_step = 0

    def __repr__(self):
        return f"Plan({self.name}, 進度={self.current_step}/{len(self.steps)})"


@dataclass
class Intention:
    """意圖：智能體承諾執行的計畫"""
    desire: Desire
    plan: Plan
    status: str = "active"  # active, completed, failed

    def __repr__(self):
        return f"Intention({self.desire.description} via {self.plan.name}, {self.status})"


class DeliveryWorld:
    """配送世界環境"""

    def __init__(self, width: int = 10, height: int = 10):
        self.width = width
        self.height = height
        self.locations: Dict[str, Location] = {}
        self.packages: Dict[str, Package] = {}
        self.agent_location: Optional[Location] = None
        self.obstacles: Set[Tuple[int, int]] = set()

    def add_location(self, name: str, x: int, y: int):
        """加入地點"""
        self.locations[name] = Location(name, x, y)

    def add_package(self, package_id: str, dest_name: str):
        """加入包裹"""
        if dest_name in self.locations:
            self.packages[package_id] = Package(
                id=package_id,
                destination=self.locations[dest_name]
            )

    def set_agent_location(self, location_name: str):
        """設定智能體位置"""
        if location_name in self.locations:
            self.agent_location = self.locations[location_name]

    def add_obstacle(self, x: int, y: int):
        """加入障礙物"""
        self.obstacles.add((x, y))

    def move_to(self, target: Location) -> Tuple[bool, str]:
        """移動到目標位置（簡化：假設可以直達）"""
        if self.agent_location == target:
            return True, f"已在 {target.name}"

        # 檢查路徑上是否有障礙物（簡化檢查）
        self.agent_location = target
        return True, f"移動到 {target.name}"

    def pickup_package(self, package_id: str) -> Tuple[bool, str]:
        """取件"""
        if package_id not in self.packages:
            return False, f"包裹 {package_id} 不存在"
        pkg = self.packages[package_id]
        if pkg.picked_up:
            return False, f"包裹 {package_id} 已被取走"
        if self.agent_location != self._find_package_location(package_id):
            return False, f"不在包裹 {package_id} 的位置"
        pkg.picked_up = True
        return True, f"已取件 {package_id}"

    def deliver_package(self, package_id: str) -> Tuple[bool, str]:
        """配送包裹"""
        if package_id not in self.packages:
            return False, f"包裹 {package_id} 不存在"
        pkg = self.packages[package_id]
        if not pkg.picked_up:
            return False, f"包裹 {package_id} 尚未取件"
        if self.agent_location != pkg.destination:
            return False, f"不在配送目的地 {pkg.destination.name}"
        return True, f"已配送 {package_id} 到 {pkg.destination.name}"

    def _find_package_location(self, package_id: str) -> Optional[Location]:
        """查找包裹所在位置（簡化：假設在起點）"""
        # 實際應從環境取得，此處簡化為固定位置
        return self.locations.get("倉庫")

    def to_string(self) -> str:
        """將世界狀態轉為字串"""
        lines = []
        for y in range(self.height):
            line = ""
            for x in range(self.width):
                if self.agent_location and (x, y) == (self.agent_location.x, self.agent_location.y):
                    line += "A "
                elif (x, y) in self.obstacles:
                    line += "# "
                elif any(loc.x == x and loc.y == y for loc in self.locations.values()):
                    loc_name = next(loc.name[0] for loc in self.locations.values()
                                    if loc.x == x and loc.y == y)
                    line += loc_name[0] + " "
                else:
                    line += ". "
            lines.append(line)
        return "\n".join(lines)


class BDIAgent:
    """BDI 智能體"""

    def __init__(self, name: str = "BDIAgent"):
        self.name = name
        self.belief: Belief = Belief()
        self.desires: List[Desire] = []
        self.intentions: List[Intention] = []
        self.plan_library: Dict[str, List[Plan]] = {}  # goal -> plans
        self.step_count = 0

    def update_beliefs(self, world: DeliveryWorld):
        """
        更新信念（感知環境）

        這是 BDI 循環的第一步：從環境中獲取最新資訊
        """
        # 更新位置
        if world.agent_location:
            self.belief.update_location(world.agent_location)

        # 更新包裹資訊
        for pkg_id, pkg in world.packages.items():
            if pkg_id not in self.belief.packages:
                self.belief.add_package(Package(pkg_id, pkg.destination, pkg.picked_up))
            else:
                if pkg.picked_up:
                    self.belief.mark_package_picked_up(pkg_id)

        # 更新地點資訊
        for loc_name, loc in world.locations.items():
            if loc_name not in self.belief.locations:
                self.belief.locations[loc_name] = loc

        # 更新障礙物
        for obs in world.obstacles:
            self.belief.add_obstacle(obs[0], obs[1])

    def generate_desires(self):
        """
        生成慾望

        根據當前信念產生想要達成的目標
        """
        # 清除已完成的慾望
        self.desires = [d for d in self.desires if not d.achieved]

        # 為每個待配送的包裹產生配送慾望
        for pkg in self.belief.get_pending_packages():
            desire_id = f"deliver_{pkg.id}"
            if not any(d.id == desire_id for d in self.desires):
                desire = Desire(
                    id=desire_id,
                    description=f"配送包裹 {pkg.id} 到 {pkg.destination.name}",
                    priority=2,  # 配送優先級較高
                    precondition=lambda b, p=pkg: any(
                        not pp.picked_up for pp in b.packages.values()
                    )
                )
                self.desires.append(desire)

        # 為未取件的包裹產生取件慾望
        for pkg in self.belief.get_pending_packages():
            desire_id = f"pickup_{pkg.id}"
            if not any(d.id == desire_id for d in self.desires):
                desire = Desire(
                    id=desire_id,
                    description=f"取件 {pkg.id}",
                    priority=1,  # 取件優先級較低（先取件才能配送）
                )
                self.desires.append(desire)

    def deliberate(self) -> Optional[Desire]:
        """
        慎思：從慾望中選擇要轉為意圖的目標

        策略：選擇優先級最高且可達成的慾望
        """
        # 過濾出可達成的慾望
        achievable = [d for d in self.desires if d.is_achievable(self.belief) and not d.achieved]

        if not achievable:
            return None

        # 按優先級排序（降序）
        achievable.sort(key=lambda d: d.priority, reverse=True)
        return achievable[0]

    def means_ends_reasoning(self, desire: Desire) -> Optional[Plan]:
        """
        手段目的推理：為慾望選擇合適的計畫

        從計畫庫中選擇第一個適用的計畫
        """
        if desire.id not in self.plan_library:
            return None

        plans = self.plan_library[desire.id]
        for plan in plans:
            # 檢查計畫中的所有動作是否都適用
            if all(action.is_applicable(self.belief) for action in plan.steps):
                return plan

        # 如果沒有完全適用的計畫，返回第一個（會在執行時處理不適用的情況）
        return plans[0] if plans else None

    def add_plan(self, goal_id: str, plan: Plan):
        """加入計畫到計畫庫"""
        if goal_id not in self.plan_library:
            self.plan_library[goal_id] = []
        self.plan_library[goal_id].append(plan)

    def execute_intentions(self, world: DeliveryWorld) -> List[str]:
        """
        執行意圖

        執行當前所有活躍意圖的下一個動作
        返回執行的動作描述列表
        """
        results = []
        completed_intentions = []

        for intention in self.intentions:
            if intention.status != "active":
                continue

            # 取得當前要執行的動作
            action = intention.plan.get_current_action()
            if action is None:
                # 計畫完成
                intention.status = "completed"
                intention.desire.achieved = True
                self.belief.delivery_history.append(intention.desire.id)
                results.append(f"✓ 完成: {intention.desire.description}")
                completed_intentions.append(intention)
                continue

            # 檢查動作是否適用
            if not action.is_applicable(self.belief):
                intention.status = "failed"
                results.append(f"✗ 失敗: {action.name} 不適用")
                completed_intentions.append(intention)
                continue

            # 執行動作
            success = action.execute(self.belief)
            if success:
                results.append(f"→ 執行: {action.name}")
                intention.plan.advance()
            else:
                results.append(f"✗ 執行失敗: {action.name}")

        # 移除已完成的意圖
        self.intentions = [i for i in self.intentions if i.status == "active"]

        return results

    def bdi_cycle(self, world: DeliveryWorld) -> List[str]:
        """
        BDI 主循環

        完整的一輪 BDI 推理與執行
        """
        self.step_count += 1
        results = [f"\n=== BDI 循環 #{self.step_count} ==="]

        # 1. 更新信念
        self.update_beliefs(world)
        results.append(f"信念更新: 位置={self.belief.agent_location.name if self.belief.agent_location else 'None'}")

        # 2. 生成慾望
        self.generate_desires()
        results.append(f"慾望數: {len(self.desires)}")

        # 3. 慎思：選擇慾望
        selected_desire = self.deliberate()
        if selected_desire and not any(i.desire.id == selected_desire.id for i in self.intentions):
            results.append(f"選擇慾望: {selected_desire.description}")

            # 4. 手段目的推理：選擇計畫
            plan = self.means_ends_reasoning(selected_desire)
            if plan:
                intention = Intention(selected_desire, plan)
                self.intentions.append(intention)
                results.append(f"採用意圖: {plan.name}")
            else:
                results.append(f"無可用計畫達成: {selected_desire.description}")
        elif selected_desire:
            results.append(f"慾望 {selected_desire.description} 已在執行中")

        # 5. 執行意圖
        if self.intentions:
            results.append(f"執行意圖 ({len(self.intentions)} 個):")
            action_results = self.execute_intentions(world)
            results.extend([f"  {r}" for r in action_results])

        return results

    def __repr__(self):
        return f"BDIAgent({self.name}, 慾望={len(self.desires)}, 意圖={len(self.intentions)})"


def create_delivery_agent() -> BDIAgent:
    """
    建立一個配送 BDI 智能體

    包含：
    - 計畫庫：取件計畫、配送計畫
    - 預定義的動作
    """
    agent = BDIAgent("DeliveryAgent")

    # === 定義動作 ===

    # 移動到倉庫
    move_to_warehouse = Action(
        name="移動到倉庫",
        preconditions=[lambda b: b.agent_location is not None],
        effects=[lambda b: setattr(b, 'agent_location', b.locations.get('倉庫'))]
    )

    # 移動到目的地（通用）
    def create_move_to_dest_action(dest_name: str) -> Action:
        return Action(
            name=f"移動到 {dest_name}",
            preconditions=[lambda b: b.agent_location is not None],
            effects=[lambda b, dn=dest_name: setattr(b, 'agent_location', b.locations.get(dn))]
        )

    # 取件動作
    def create_pickup_action(pkg_id: str) -> Action:
        return Action(
            name=f"取件 {pkg_id}",
            preconditions=[
                lambda b: b.agent_location is not None and b.agent_location.name == "倉庫"
            ],
            effects=[lambda b, pid=pkg_id: b.mark_package_picked_up(pid)]
        )

    # 配送動作
    def create_deliver_action(pkg_id: str) -> Action:
        return Action(
            name=f"配送 {pkg_id}",
            preconditions=[
                lambda b, pid=pkg_id: pid in b.packages and b.packages[pid].picked_up,
                lambda b, pid=pkg_id: b.agent_location == b.packages[pid].destination if pid in b.packages else False
            ],
            effects=[lambda b, pid=pkg_id: b.delivery_history.append(pid)]
        )

    # === 建立計畫 ===

    # 取件計畫 A1：直接去倉庫取件
    pickup_plan_a1 = Plan(
        name="取件計畫A1",
        goal="pickup",
        steps=[move_to_warehouse, Action("等待取件", effects=[lambda b: None])]  # 簡化：假設到倉庫就完成取件
    )

    # 配送計畫 D1：移動到目的地並配送
    def create_delivery_plan(pkg_id: str, dest_name: str) -> Plan:
        return Plan(
            name=f"配送計畫_{pkg_id}",
            goal=f"deliver_{pkg_id}",
            steps=[
                create_move_to_dest_action(dest_name),
                create_deliver_action(pkg_id)
            ]
        )

    # 加入計畫庫（簡化：使用通用計畫）
    # 實際應根據具體目標動態生成計畫
    agent.add_plan("pickup_pkg1", Plan(
        name="取件pkg1計畫",
        goal="pickup_pkg1",
        steps=[move_to_warehouse]
    ))

    return agent


def demo_bdi_delivery():
    """BDI 配送智能體示範"""
    print("=== BDI 智能體 - 配送任務示範 ===\n")

    # 建立環境
    world = DeliveryWorld(width=10, height=10)
    world.add_location("倉庫", 1, 1)
    world.add_location("車站", 5, 3)
    world.add_location("公園", 8, 2)
    world.add_location("學校", 3, 7)
    world.add_location("醫院", 7, 8)

    world.add_package("pkg1", "車站")
    world.add_package("pkg2", "公園")
    world.add_package("pkg3", "學校")

    world.set_agent_location("倉庫")

    print("環境設定：")
    print("地點：倉庫(1,1), 車站(5,3), 公園(8,2), 學校(3,7), 醫院(7,8)")
    print("包裹：pkg1→車站, pkg2→公園, pkg3→學校")
    print(f"智能體起始位置：{world.agent_location.name}\n")

    # 建立 BDI 智能體
    agent = BDIAgent("配送員")

    # 手動加入初始信念
    agent.update_beliefs(world)

    # 建立計畫庫（根據實際包裹動態生成）
    for pkg_id, pkg in world.packages.items():
        # 取件計畫
        move_to_warehouse = Action(
            name="移動到倉庫",
            preconditions=[],
            effects=[lambda b: None]  # 簡化
        )

        # 配送計畫
        move_to_dest = Action(
            name=f"移動到 {pkg.destination.name}",
            preconditions=[],
            effects=[lambda b, d=pkg.destination: setattr(b, 'agent_location', d)]
        )

        deliver = Action(
            name=f"配送 {pkg_id}",
            preconditions=[],
            effects=[lambda b, pid=pkg_id: b.delivery_history.append(pid)]
        )

        delivery_plan = Plan(
            name=f"配送{pkg_id}計畫",
            goal=f"deliver_{pkg_id}",
            steps=[move_to_dest, deliver]
        )

        agent.add_plan(f"deliver_{pkg_id}", delivery_plan)

    print("BDI 智能體已就緒")
    print(f"計畫庫：{len(agent.plan_library)} 個目標類型\n")

    # 執行 BDI 循環
    max_cycles = 10
    for cycle in range(max_cycles):
        results = agent.bdi_cycle(world)
        print("\n".join(results))

        # 檢查是否所有包裹都已配送
        if all(pkg_id in agent.belief.delivery_history for pkg_id in world.packages):
            print(f"\n✓ 所有包裹已配送完成！")
            break

        # 簡化：手動更新世界狀態（實際應由環境反饋）
        if agent.intentions:
            for intention in agent.intentions:
                if intention.plan.current_step < len(intention.plan.steps):
                    action = intention.plan.steps[intention.plan.current_step]
                    # 模擬執行
                    if "移動到" in action.name:
                        dest_name = action.name.replace("移動到 ", "")
                        if dest_name in world.locations:
                            world.set_agent_location(dest_name)
                    elif "配送" in action.name:
                        pkg_id = action.name.replace("配送 ", "")
                        if pkg_id in world.packages:
                            world.packages[pkg_id].picked_up = True

    print(f"\n=== 配送任務總結 ===")
    print(f"總循環次數：{agent.step_count}")
    print(f"已配送：{agent.belief.delivery_history}")
    print(f"剩餘慾望：{[d.description for d in agent.desires if not d.achieved]}")


def demo_bdi_concepts():
    """BDI 核心概念示範"""
    print("\n=== BDI 核心概念展示 ===\n")

    print("1. 信念（Belief）：智能體知道的資訊")
    belief = Belief()
    belief.update_location(Location("起點", 0, 0))
    belief.add_package(Package("p1", Location("終點", 5, 5)))
    print(f"   位置：{belief.agent_location}")
    print(f"   包裹：{belief.get_known_packages()}\n")

    print("2. 慾望（Desire）：想要達成的目標")
    desire1 = Desire("d1", "送達包裹 p1", priority=2)
    desire2 = Desire("d2", "返回基地", priority=1)
    print(f"   {desire1}")
    print(f"   {desire2}\n")

    print("3. 意圖（Intention）：承諾執行的計畫")
    plan = Plan("送達計畫", "送達包裹", [
        Action("前往終點"),
        Action("交付包裹")
    ])
    intention = Intention(desire1, plan)
    print(f"   {intention}\n")

    print("4. BDI 循環：")
    print("   Step 1: 更新信念（感知環境）")
    print("   Step 2: 生成慾望（產生目標）")
    print("   Step 3: 慎思（選擇目標）")
    print("   Step 4: 手段目的推理（選擇計畫）")
    print("   Step 5: 執行意圖（執行動作）")
    print("   Step 6: 檢查完成狀態\n")

    print("BDI 架構的優點：")
    print("  - 反應性：能快速回應環境變化（通過信念更新）")
    print("  - 慎思性：能進行多步規劃（通過意圖執行）")
    print("  - 適應性：能動態調整目標優先級（通過慾望管理）")
    print("  - 可解釋性：信念-慾望-意圖皆可被檢視與解釋")


if __name__ == "__main__":
    demo_bdi_concepts()
    demo_bdi_delivery()
