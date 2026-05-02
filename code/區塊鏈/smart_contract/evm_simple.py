"""
簡化版 EVM（以太坊虛擬機）實作
堆疊式虛擬機器，支援基本操作碼
"""

from typing import List, Optional, Dict, Any


class EVMInstruction:
    """EVM 指令集"""

    # 堆疊操作
    PUSH = "PUSH"
    POP = "POP"

    # 算術運算
    ADD = "ADD"
    MUL = "MUL"
    SUB = "SUB"

    # 控制流
    JUMP = "JUMP"
    JUMPI = "JUMPI"
    JUMPDEST = "JUMPDEST"

    # 環境操作
    CALL = "CALL"
    RETURN = "RETURN"
    STOP = "STOP"


class EVMStack:
    """EVM 堆疊"""

    def __init__(self, max_size: int = 1024) -> None:
        self.stack: List[int] = []
        self.max_size: int = max_size

    def push(self, value: int) -> None:
        """推入數值到堆疊"""
        if len(self.stack) >= self.max_size:
            raise Exception("堆疊溢位")
        self.stack.append(value)

    def pop(self) -> int:
        """從堆疊彈出數值"""
        if not self.stack:
            raise Exception("堆疊為空")
        return self.stack.pop()

    def peek(self) -> int:
        """查看堆疊頂端數值"""
        if not self.stack:
            raise Exception("堆疊為空")
        return self.stack[-1]

    def size(self) -> int:
        """堆疊大小"""
        return len(self.stack)


class EVMMemory:
    """EVM 記憶體（簡化版）"""

    def __init__(self) -> None:
        self.memory: Dict[int, int] = {}

    def store(self, offset: int, value: int) -> None:
        """儲存數值到記憶體"""
        self.memory[offset] = value

    def load(self, offset: int) -> int:
        """從記憶體讀取數值"""
        return self.memory.get(offset, 0)


class EVM:
    """簡化版以太坊虛擬機"""

    def __init__(self) -> None:
        self.stack: EVMStack = EVMStack()
        self.memory: EVMMemory = EVMMemory()
        self.pc: int = 0  # 程式計數器
        self.code: List[Dict[str, Any]] = []
        self.running: bool = False
        self.gas: int = 100000  # 燃料限制
        self.gas_used: int = 0

    def load_code(self, code: List[Dict[str, Any]]) -> None:
        """載入合約程式碼"""
        self.code = code
        self.pc = 0
        self.stack = EVMStack()
        self.memory = EVMMemory()
        self.running = True
        self.gas_used = 0

    def use_gas(self, amount: int) -> bool:
        """消耗燃料，返回是否足夠"""
        if self.gas_used + amount > self.gas:
            return False
        self.gas_used += amount
        return True

    def step(self) -> bool:
        """執行一個指令，返回是否繼續執行"""
        if not self.running or self.pc >= len(self.code):
            return False

        instruction: Dict[str, Any] = self.code[self.pc]
        op: str = instruction.get("op")

        if not self.use_gas(1):
            print("燃料不足！")
            return False

        # 執行指令
        if op == EVMInstruction.PUSH:
            value: int = instruction.get("value", 0)
            self.stack.push(value)
            self.pc += 1

        elif op == EVMInstruction.POP:
            self.stack.pop()
            self.pc += 1

        elif op == EVMInstruction.ADD:
            a: int = self.stack.pop()
            b: int = self.stack.pop()
            self.stack.push(a + b)
            self.pc += 1

        elif op == EVMInstruction.MUL:
            a: int = self.stack.pop()
            b: int = self.stack.pop()
            self.stack.push(a * b)
            self.pc += 1

        elif op == EVMInstruction.SUB:
            a: int = self.stack.pop()
            b: int = self.stack.pop()
            self.stack.push(b - a)  # 注意順序
            self.pc += 1

        elif op == EVMInstruction.JUMP:
            dest: int = self.stack.pop()
            self.pc = dest

        elif op == EVMInstruction.JUMPI:
            dest: int = self.stack.pop()
            condition: int = self.stack.pop()
            if condition != 0:
                self.pc = dest
            else:
                self.pc += 1

        elif op == EVMInstruction.CALL:
            # 簡化版 CALL：呼叫另一個合約（這裡只是模擬）
            address: int = self.stack.pop()
            value: int = self.stack.pop()
            print(f"呼叫合約地址 {address}，價值 {value}")
            self.pc += 1

        elif op == EVMInstruction.RETURN:
            self.running = False
            return False

        elif op == EVMInstruction.STOP:
            self.running = False
            return False

        else:
            print(f"未知指令: {op}")
            self.pc += 1

        return True

    def run(self) -> None:
        """執行整個合約"""
        while self.step():
            pass
        print(f"執行完成，消耗燃料: {self.gas_used}")


if __name__ == "__main__":
    # 建立 EVM 實例
    evm: EVM = EVM()

    # 編寫簡單合約：(5 + 3) * 2
    code: List[Dict[str, Any]] = [
        {"op": EVMInstruction.PUSH, "value": 5},
        {"op": EVMInstruction.PUSH, "value": 3},
        {"op": EVMInstruction.ADD},  # 5 + 3 = 8
        {"op": EVMInstruction.PUSH, "value": 2},
        {"op": EVMInstruction.MUL},  # 8 * 2 = 16
        {"op": EVMInstruction.STOP}
    ]

    print("執行合約: (5 + 3) * 2")
    evm.load_code(code)
    evm.run()

    # 查看結果
    if evm.stack.size() > 0:
        result: int = evm.stack.pop()
        print(f"結果: {result}")
