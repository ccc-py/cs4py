"""
馬可夫鏈 (Markov Chain)

實作離散時間馬可夫鏈，包含轉移矩陣、狀態模擬、
平穩分佈計算，以及文字生成應用。
"""

import random
import numpy as np
from typing import List, Dict, Tuple, Optional, Any


class MarkovChain:
    """
    離散時間馬可夫鏈
    
    狀態空間為有限集合，由轉移機率矩陣定義。
    滿足馬可夫性質：下一狀態只依賴於當前狀態。
    """
    
    def __init__(self, states: List[Any], transition_matrix: np.ndarray):
        """
        初始化馬可夫鏈
        
        參數:
            states: 狀態列表
            transition_matrix: 轉移矩陣 P[i][j] = P(j|i)
                             shape = (n_states, n_states)
        """
        self.states = states
        self.state_index = {s: i for i, s in enumerate(states)}
        self.n_states = len(states)
        
        # 驗證轉移矩陣
        if transition_matrix.shape != (self.n_states, self.n_states):
            raise ValueError("轉移矩陣維度不匹配")
        
        # 檢查每行和是否為 1
        for i in range(self.n_states):
            row_sum = np.sum(transition_matrix[i])
            if abs(row_sum - 1.0) > 1e-10:
                raise ValueError(f"第 {i} 行和不為 1: {row_sum}")
        
        self.P = transition_matrix
    
    def simulate(self, initial_state: Any, n_steps: int) -> List[Any]:
        """
        模擬馬可夫鏈的狀態序列
        
        參數:
            initial_state: 初始狀態
            n_steps: 模擬步數
        
        返回:
            狀態序列
        """
        if initial_state not in self.state_index:
            raise ValueError(f"初始狀態 {initial_state} 不在狀態空間中")
        
        sequence = [initial_state]
        current_idx = self.state_index[initial_state]
        
        for _ in range(n_steps - 1):
            # 根據轉移機率選擇下一狀態
            probs = self.P[current_idx]
            next_idx = np.random.choice(self.n_states, p=probs)
            next_state = self.states[next_idx]
            sequence.append(next_state)
            current_idx = next_idx
        
        return sequence
    
    def get_stationary_distribution(self, max_iter: int = 1000, 
                                    tol: float = 1e-10) -> np.ndarray:
        """
        計算平穩分佈 (Stationary Distribution)
        
        透過反覆乘以轉移矩陣直至收斂：
        π = πP
        
        參數:
            max_iter: 最大迭代次數
            tol: 收斂容忍度
        
        返回:
            平穩分佈 π
        """
        pi = np.ones(self.n_states) / self.n_states  # 初始均勻分佈
        
        for _ in range(max_iter):
            pi_new = pi @ self.P  # π_new = π · P
            if np.linalg.norm(pi_new - pi) < tol:
                return pi_new
            pi = pi_new
        
        return pi
    
    def get_n_step_transition(self, n: int) -> np.ndarray:
        """
        計算 n 步轉移矩陣
        
        參數:
            n: 步數
        
        返回:
            P^n (n 步轉移矩陣)
        """
        return np.linalg.matrix_power(self.P, n)
    
    def hitting_time(self, start: Any, target: Any, 
                     max_steps: int = 10000) -> Optional[int]:
        """
        計算從 start 到 target 的擊中時 (Hitting Time)
        
        參數:
            start: 起始狀態
            target: 目標狀態
            max_steps: 最大步數限制
        
        返回:
            擊中時，若超過 max_steps 則返回 None
        """
        if start not in self.state_index or target not in self.state_index:
            raise ValueError("狀態不在狀態空間中")
        
        current = start
        steps = 0
        
        while current != target and steps < max_steps:
            idx = self.state_index[current]
            probs = self.P[idx]
            next_idx = np.random.choice(self.n_states, p=probs)
            current = self.states[next_idx]
            steps += 1
        
        return steps if current == target else None


class TextGenerator:
    """
    基於馬可夫鏈的文字生成器
    
    透過學習文字中詞語的轉移機率來生成類似風格的文字。
    """
    
    def __init__(self, order: int = 1):
        """
        初始化文字生成器
        
        參數:
            order: n-gram 的階數 (1 表示一階馬可夫)
        """
        self.order = order
        self.transitions: Dict[Tuple[str, ...], Dict[str, int]] = {}
        self.vocab: List[str] = []
        self.start_tokens: List[Tuple[str, ...]] = []
    
    def train(self, text: str) -> None:
        """
        訓練模型（學習轉移機率）
        
        參數:
            text: 訓練文字
        """
        tokens = text.split()
        self.vocab = list(set(tokens))
        
        # 記錄起始 n-gram
        if len(tokens) >= self.order:
            self.start_tokens.append(tuple(tokens[:self.order]))
        
        # 統計轉移次數
        for i in range(len(tokens) - self.order):
            current = tuple(tokens[i:i + self.order])
            next_token = tokens[i + self.order]
            
            if current not in self.transitions:
                self.transitions[current] = {}
            self.transitions[current][next_token] = \
                self.transitions[current].get(next_token, 0) + 1
    
    def generate(self, max_length: int = 50) -> str:
        """
        生成文字
        
        參數:
            max_length: 最大生成長度
        
        返回:
            生成的文字
        """
        if not self.start_tokens:
            raise ValueError("模型尚未訓練")
        
        # 隨機選擇起始 n-gram
        current = random.choice(self.start_tokens)
        result = list(current)
        
        for _ in range(max_length - self.order):
            if current not in self.transitions:
                break
            
            # 根據轉移次數加權隨機選擇下一個詞
            next_candidates = self.transitions[current]
            tokens = list(next_candidates.keys())
            weights = list(next_candidates.values())
            
            next_token = random.choices(tokens, weights=weights)[0]
            result.append(next_token)
            
            # 更新當前 n-gram
            current = tuple(result[-self.order:])
        
        return ' '.join(result)


if __name__ == "__main__":
    print("=== 馬可夫鏈測試 ===\n")
    
    # 測試 1: 簡單 2 狀態馬可夫鏈
    print("1. 簡單 2 狀態馬可夫鏈")
    states = ["晴", "雨"]
    P = np.array([
        [0.9, 0.1],  # 晴 -> 晴: 0.9, 晴 -> 雨: 0.1
        [0.5, 0.5],  # 雨 -> 晴: 0.5, 雨 -> 雨: 0.5
    ])
    
    mc = MarkovChain(states, P)
    seq = mc.simulate("晴", 10)
    print(f"   初始: 晴, 模擬 10 步: {' -> '.join(seq)}")
    
    # 測試 2: 平穩分佈
    print(f"\n2. 平穩分佈")
    pi = mc.get_stationary_distribution()
    print(f"   平穩分佈: 晴={pi[0]:.4f}, 雨={pi[1]:.4f}")
    print(f"   驗證 πP = π: {np.allclose(pi @ P, pi)}")
    
    # 測試 3: n 步轉移
    print(f"\n3. n 步轉移機率")
    P_10 = mc.get_n_step_transition(10)
    print(f"   10 步後從晴到雨的機率: {P_10[0][1]:.4f}")
    print(f"   10 步後從雨到晴的機率: {P_10[1][0]:.4f}")
    
    # 測試 4: 擊中時
    print(f"\n4. 擊中時")
    hitting = mc.hitting_time("晴", "雨")
    print(f"   從晴到雨的擊中時: {hitting} 步")
    
    # 測試 5: 文字生成
    print(f"\n5. 文字生成")
    corpus = """
    我 喜歡 吃 蘋果 我 喜歡 吃 香蕉 我 喜歡 吃 水果
    你 喜歡 吃 什麼 我 喜歡 喝 水 你 喜歡 喝 什麼
    蘋果 是 水果 香蕉 是 水果 水果 很 好 吃
    """
    
    tg = TextGenerator(order=1)
    tg.train(corpus)
    print(f"   訓練完成，詞彙數: {len(tg.vocab)}")
    print(f"   生成文字: {tg.generate(15)}")
    print(f"   生成文字: {tg.generate(15)}")
    print(f"   生成文字: {tg.generate(15)}")
    
    # 測試 6: 3 狀態氣象模型
    print(f"\n6. 3 狀態氣象模型")
    states3 = ["晴", "雲", "雨"]
    P3 = np.array([
        [0.8, 0.15, 0.05],
        [0.2, 0.6, 0.2],
        [0.1, 0.3, 0.6],
    ])
    mc3 = MarkovChain(states3, P3)
    pi3 = mc3.get_stationary_distribution()
    print(f"   平穩分佈: 晴={pi3[0]:.3f}, 雲={pi3[1]:.3f}, 雨={pi3[2]:.3f}")
