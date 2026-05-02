"""
簡單的堆疊式虛擬機器 (Stack-based Virtual Machine)

實作一個簡單的 VM，包含堆疊、指令指標、位元組碼指令，
以及一個將文字指令轉換為位元組碼的簡單組譯器。
"""

from typing import Any, Dict, List, Optional, Tuple


# 指令集定義
class OpCode:
    """操作碼常數"""
    PUSH = 0x01    # 壓入數值到堆疊
    POP = 0x02     # 彈出堆疊頂端
    ADD = 0x03     # 加法
    SUB = 0x04     # 減法
    MUL = 0x05     # 乘法
    DIV = 0x06     # 除法
    JMP = 0x07     # 無條件跳轉
    JZ = 0x08      # 為零時跳轉
    JNZ = 0x09     # 不為零時跳轉
    CALL = 0x0A    # 呼叫函式
    RET = 0x0B     # 函式返回
    PRINT = 0x0C   # 印出堆疊頂端
    HALT = 0x0D    # 停止執行
    LOAD = 0x0E    # 載入變數
    STORE = 0x0F   # 儲存變數


class VM:
    """簡單的堆疊式虛擬機器"""

    def __init__(self) -> None:
        self.stack: List[Any] = []           # 運算堆疊
        self.call_stack: List[int] = []      # 呼叫堆疊（儲存返回位址）
        self.variables: Dict[str, Any] = {}  # 變數記憶體
        self.bytecode: List[Tuple[int, Any]] = []  # 位元組碼
        self.ip: int = 0                     # 指令指標
        self.running: bool = False           # 執行狀態

    def load_bytecode(self, bytecode: List[Tuple[int, Any]]) -> None:
        """載入位元組碼"""
        self.bytecode = bytecode
        self.ip = 0
        self.stack.clear()
        self.call_stack.clear()
        self.variables.clear()

    def fetch(self) -> Tuple[int, Any]:
        """取得目前指令"""
        if self.ip >= len(self.bytecode):
            raise RuntimeError("指令指標超出範圍")
        instr = self.bytecode[self.ip]
        self.ip += 1
        if isinstance(instr, tuple):
            return instr[0], instr[1] if len(instr) > 1 else None
        return instr, None

    def execute(self, opcode: int, operand: Any) -> None:
        """執行單一指令"""
        if opcode == OpCode.PUSH:
            self.stack.append(operand)
        elif opcode == OpCode.POP:
            if self.stack:
                self.stack.pop()
        elif opcode == OpCode.ADD:
            b = self.stack.pop()
            a = self.stack.pop()
            self.stack.append(a + b)
        elif opcode == OpCode.SUB:
            b = self.stack.pop()
            a = self.stack.pop()
            self.stack.append(a - b)
        elif opcode == OpCode.MUL:
            b = self.stack.pop()
            a = self.stack.pop()
            self.stack.append(a * b)
        elif opcode == OpCode.DIV:
            b = self.stack.pop()
            a = self.stack.pop()
            if b == 0:
                raise ZeroDivisionError("除零錯誤")
            self.stack.append(a // b)
        elif opcode == OpCode.JMP:
            self.ip = operand
        elif opcode == OpCode.JZ:
            value = self.stack.pop()
            if value == 0:
                self.ip = operand
        elif opcode == OpCode.JNZ:
            value = self.stack.pop()
            if value != 0:
                self.ip = operand
        elif opcode == OpCode.CALL:
            self.call_stack.append(self.ip)
            self.ip = operand
        elif opcode == OpCode.RET:
            if not self.call_stack:
                raise RuntimeError("呼叫堆疊為空，無法返回")
            self.ip = self.call_stack.pop()
        elif opcode == OpCode.PRINT:
            if self.stack:
                print(self.stack[-1])
        elif opcode == OpCode.HALT:
            self.running = False
        elif opcode == OpCode.LOAD:
            var_name = operand
            if var_name in self.variables:
                self.stack.append(self.variables[var_name])
            else:
                raise NameError(f"變數 '{var_name}' 未定義")
        elif opcode == OpCode.STORE:
            var_name = operand
            if self.stack:
                self.variables[var_name] = self.stack.pop()
            else:
                raise RuntimeError("堆疊為空，無法儲存")
        else:
            raise RuntimeError(f"未知的操作碼: {opcode}")

    def run(self) -> None:
        """執行位元組碼"""
        self.running = True
        while self.running:
            opcode, operand = self.fetch()
            self.execute(opcode, operand)


class Assembler:
    """簡單組譯器：將文字指令轉換為位元組碼"""

    def __init__(self) -> None:
        self.labels: Dict[str, int] = {}        # 標籤對應到位址
        self.bytecode: List[Tuple[int, Any]] = []
        self.opcode_map = {
            'PUSH': OpCode.PUSH,
            'POP': OpCode.POP,
            'ADD': OpCode.ADD,
            'SUB': OpCode.SUB,
            'MUL': OpCode.MUL,
            'DIV': OpCode.DIV,
            'JMP': OpCode.JMP,
            'JZ': OpCode.JZ,
            'JNZ': OpCode.JNZ,
            'CALL': OpCode.CALL,
            'RET': OpCode.RET,
            'PRINT': OpCode.PRINT,
            'HALT': OpCode.HALT,
            'LOAD': OpCode.LOAD,
            'STORE': OpCode.STORE,
        }

    def assemble(self, source: List[str]) -> List[Tuple[int, Any]]:
        """組譯文字指令為位元組碼"""
        # 第一遍：收集標籤
        self.labels.clear()
        self.bytecode.clear()
        clean_source = []

        for line in source:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            # 處理標籤
            if line.endswith(':'):
                label = line[:-1].strip()
                self.labels[label] = len(clean_source)
                continue
            clean_source.append(line)

        # 第二遍：產生位元組碼
        for line in clean_source:
            parts = line.split()
            if not parts:
                continue
            mnemonic = parts[0].upper()

            if mnemonic not in self.opcode_map:
                raise ValueError(f"未知的指令: {mnemonic}")

            opcode = self.opcode_map[mnemonic]
            operand = None

            if len(parts) > 1:
                arg = parts[1]
                # 處理標籤參考
                if arg in self.labels:
                    operand = self.labels[arg]
                else:
                    # 嘗試解析為數字
                    try:
                        operand = int(arg)
                    except ValueError:
                        try:
                            operand = float(arg)
                        except ValueError:
                            # 當作字串（變數名稱）
                            operand = arg

            self.bytecode.append((opcode, operand))

        return self.bytecode


def factorial_program() -> List[Tuple[int, Any]]:
    """計算階乘的程式（5! = 120）"""
    # 使用組譯器產生
    source = [
        "# 計算 5! (5 的階乘)",
        "PUSH 5",       # n = 5
        "STORE n",
        "PUSH 1",
        "STORE result",
        "",
        "LOOP:",
        "LOAD n",
        "JZ DONE",      # 如果 n == 0，跳到 DONE（JZ 檢查棧頂）
        "LOAD result",
        "LOAD n",
        "MUL",          # result = result * n
        "STORE result",
        "LOAD n",
        "PUSH 1",
        "SUB",          # n = n - 1
        "STORE n",
        "JMP LOOP",
        "",
        "DONE:",
        "LOAD result",
        "PRINT",        # 印出結果
        "HALT",
    ]
    assembler = Assembler()
    return assembler.assemble(source)


def fibonacci_program() -> List[Tuple[int, Any]]:
    """計算費波那契數列的第 n 項（第 10 項 = 55）"""
    source = [
        "# 計算費波那契數列的第 10 項",
        "PUSH 10",
        "STORE n",
        "PUSH 0",
        "STORE a",      # a = 0
        "PUSH 1",
        "STORE b",      # b = 1
        "PUSH 0",
        "STORE i",      # i = 0
        "",
        "LOOP:",
        "LOAD i",
        "LOAD n",
        "SUB",
        "JZ DONE",      # 如果 i >= n，結束
        "LOAD a",
        "LOAD b",
        "ADD",
        "STORE temp",   # temp = a + b
        "LOAD b",
        "STORE a",      # a = b
        "LOAD temp",
        "STORE b",      # b = temp
        "LOAD i",
        "PUSH 1",
        "ADD",
        "STORE i",      # i = i + 1
        "JMP LOOP",
        "",
        "DONE:",
        "LOAD a",
        "PRINT",        # 印出結果
        "HALT",
    ]
    assembler = Assembler()
    return assembler.assemble(source)


if __name__ == "__main__":
    # 示範 1：計算 5!
    print("=== 示範 1：計算 5! ===")
    vm = VM()
    bytecode = factorial_program()
    vm.load_bytecode(bytecode)
    vm.run()

    # 示範 2：計算費波那契數列第 10 項
    print("\n=== 示範 2：計算費波那契數列第 10 項 ===")
    vm2 = VM()
    bytecode2 = fibonacci_program()
    vm2.load_bytecode(bytecode2)
    vm2.run()

    # 示範 3：手動建立位元組碼並執行
    print("\n=== 示範 3：手動建立位元組碼 (2 + 3) * 4 ===")
    vm3 = VM()
    # (2 + 3) * 4 = 20
    manual_bytecode = [
        (OpCode.PUSH, 2),
        (OpCode.PUSH, 3),
        OpCode.ADD,      # 2 + 3 = 5
        (OpCode.PUSH, 4),
        OpCode.MUL,      # 5 * 4 = 20
        OpCode.PRINT,
        OpCode.HALT,
    ]
    vm3.load_bytecode(manual_bytecode)
    vm3.run()
