"""
區塊鏈交易結構（UTXO 模型）
實作交易輸入、輸出與簽章驗證
"""

import hashlib
import json
from typing import List, Dict, Optional, Any


class TransactionInput:
    """交易輸入，引用之前的交易輸出"""

    def __init__(self, txid: str, output_index: int, signature: Optional[str] = None) -> None:
        self.txid: str = txid  # 前筆交易 ID
        self.output_index: int = output_index  # 輸出索引
        self.signature: Optional[str] = signature  # 簽章

    def __repr__(self) -> str:
        return f"TxInput(txid={self.txid[:8]}..., idx={self.output_index})"


class TransactionOutput:
    """交易輸出，指定接收者與金額"""

    def __init__(self, address: str, amount: float) -> None:
        self.address: str = address  # 接收者地址
        self.amount: float = amount  # 金額

    def __repr__(self) -> str:
        return f"TxOutput(addr={self.address[:10]}..., amt={self.amount})"


class Transaction:
    """交易類別，包含輸入與輸出"""

    def __init__(self, inputs: List[TransactionInput], outputs: List[TransactionOutput]) -> None:
        self.inputs: List[TransactionInput] = inputs
        self.outputs: List[TransactionOutput] = outputs
        self.txid: str = self.calculate_txid()

    def calculate_txid(self) -> str:
        """計算交易 ID（交易的雜湊值）"""
        tx_data: Dict[str, Any] = {
            'inputs': [{'txid': inp.txid, 'output_index': inp.output_index} for inp in self.inputs],
            'outputs': [{'address': out.address, 'amount': out.amount} for out in self.outputs]
        }
        tx_string: str = json.dumps(tx_data, sort_keys=True)
        return hashlib.sha256(tx_string.encode()).hexdigest()

    def sign_input(self, input_index: int, private_key: str) -> None:
        """
        簽署交易輸入
        簡化版：使用私鑰對交易 ID 進行簽章
        """
        if input_index >= len(self.inputs):
            raise IndexError("輸入索引超出範圍")

        # 簡化版簽章：將私鑰與交易 ID 結合後雜湊
        sign_data: str = private_key + self.txid
        signature: str = hashlib.sha256(sign_data.encode()).hexdigest()
        self.inputs[input_index].signature = signature

    def verify_input(self, input_index: int, public_key: str) -> bool:
        """
        驗證交易輸入的簽章
        簡化版：檢查簽章是否正確
        """
        if input_index >= len(self.inputs):
            return False

        tx_input: TransactionInput = self.inputs[input_index]
        if not tx_input.signature:
            return False

        # 簡化版驗證：用公鑰重新計算簽章
        verify_data: str = public_key + self.txid
        expected_signature: str = hashlib.sha256(verify_data.encode()).hexdigest()

        return tx_input.signature == expected_signature

    def get_total_input(self, utxo_set: Dict[str, TransactionOutput]) -> float:
        """計算交易輸入總額"""
        total: float = 0.0
        for tx_input in self.inputs:
            key: str = f"{tx_input.txid}:{tx_input.output_index}"
            if key in utxo_set:
                total += utxo_set[key].amount
        return total

    def get_total_output(self) -> float:
        """計算交易輸出總額"""
        return sum(output.amount for output in self.outputs)

    def __repr__(self) -> str:
        return f"Transaction(txid={self.txid[:10]}..., inputs={len(self.inputs)}, outputs={len(self.outputs)})"


class UTXOSet:
    """未花費交易輸出集合（UTXO Set）"""

    def __init__(self) -> None:
        self.utxos: Dict[str, TransactionOutput] = {}

    def add_utxo(self, txid: str, output_index: int, output: TransactionOutput) -> None:
        """加入 UTXO"""
        key: str = f"{txid}:{output_index}"
        self.utxos[key] = output

    def remove_utxo(self, txid: str, output_index: int) -> None:
        """移除 UTXO（花費後）"""
        key: str = f"{txid}:{output_index}"
        if key in self.utxos:
            del self.utxos[key]

    def process_transaction(self, tx: Transaction) -> bool:
        """處理交易，更新 UTXO 集合"""
        # 檢查輸入是否都存在
        for tx_input in tx.inputs:
            key: str = f"{tx_input.txid}:{tx_input.output_index}"
            if key not in self.utxos:
                return False

        # 移除已花費的輸出
        for tx_input in tx.inputs:
            self.remove_utxo(tx_input.txid, tx_input.output_index)

        # 加入新的輸出
        for i, tx_output in enumerate(tx.outputs):
            self.add_utxo(tx.txid, i, tx_output)

        return True


if __name__ == "__main__":
    # 建立 UTXO 集合（模擬區塊鏈狀態）
    utxo_set: UTXOSet = UTXOSet()

    # 建立一筆初始交易（Coinbase）
    coinbase_output: TransactionOutput = TransactionOutput("Alice_address", 50.0)
    coinbase: Transaction = Transaction(
        inputs=[],
        outputs=[coinbase_output]
    )
    utxo_set.process_transaction(coinbase)
    print(f"Coinbase 交易: {coinbase}")

    # Alice 發送 30 給 Bob
    alice_private_key: str = "alice_private_key_123"
    alice_public_key: str = "alice_public_key_456"

    tx_input: TransactionInput = TransactionInput(coinbase.txid, 0)
    tx: Transaction = Transaction(
        inputs=[tx_input],
        outputs=[
            TransactionOutput("Bob_address", 30.0),
            TransactionOutput("Alice_address", 20.0)  # 找零
        ]
    )

    # 簽署交易
    tx.sign_input(0, alice_private_key)
    print(f"\nAlice 轉帳給 Bob: {tx}")

    # 驗證簽章
    is_valid: bool = tx.verify_input(0, alice_public_key)
    print(f"簽章驗證: {'成功' if is_valid else '失敗'}")

    # 處理交易
    success: bool = utxo_set.process_transaction(tx)
    print(f"交易處理: {'成功' if success else '失敗'}")
    print(f"UTXO 數量: {len(utxo_set.utxos)}")
