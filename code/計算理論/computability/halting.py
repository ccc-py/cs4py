"""
停機問題演示 (Halting Problem)

停機問題是計算理論中最著名的不可判定問題。

問題描述：
給定一個程式 P 和輸入 I，判斷 P 在執行於 I 時是否會最終停機。

Alan Turing 在 1936 年證明了：不存在一個通用演算法
可以判定任意程式是否會停機。

證明方法：反證法（透過自我指稱產生悖論）

歷史背景：
- 1936 年：Alan Turing 證明停機問題不可判定
- 這是第一个被证明的不可判定问题
- 由此可以推导出许多其他问题的不可判定性

參考：Turing, A. M. (1936). On Computable Numbers, with an Application to the Entscheidungsproblem.
"""


def halts(program, input_data):
    """
    假設的停機判定器（實際上不存在）

    如果這個函數能正確工作，那麼它應該：
    - 返回 True 如果 program(input_data) 最終會停機
    - 返回 False 如果 program(input_data) 不會停機

    但 Turing 證明了這樣的函數不可能存在！
    """
    # 這只是一個佔位符，實際上無法實作
    raise NotImplementedError("停機判定器不存在！")


def paradox_program(f):
    """
    悖論程式：如果 f 說我會停機，我就無限循環；如果說我不會停機，我就停機

    這就是證明中的關鍵：構造一個自我指稱的程式
    """
    if halts(f, f):
        # 如果判定器說我會停機，我就無限循環
        while True:
            pass
    else:
        # 如果判定器說我不會停機，我就停機
        return


def demonstrate_paradox():
    """
    演示停機問題的悖論

    假設 halts 存在，考慮 paradox_program(paradox_program)：
    1. 如果 halts 返回 True（會停機），則 paradox_program 進入無限循環 → 矛盾！
    2. 如果 halts 返回 False（不會停機），則 paradox_program 停機 → 矛盾！

    因此 halts 不可能存在。
    """
    print("=== 停機問題悖論演示 ===")
    print()
    print("假設存在一個停機判定器 halts(program, input)")
    print("它應該能正確判斷任意程式是否會停機。")
    print()
    print("現在構造一個悖論程式：")
    print()
    print("def paradox_program(f):")
    print("    if halts(f, f):")
    print("        while True: pass  # 無限循環")
    print("    else:")
    print("        return  # 停機")
    print()
    print("考慮 paradox_program(paradox_program)：")
    print()
    print("情況 1: 如果 halts 說它會停機 → 它進入無限循環 → 矛盾！")
    print("情況 2: 如果 halts 說它不會停機 → 它停機 → 矛盾！")
    print()
    print("結論：halts 不可能存在。停機問題不可判定。")
    print()
    print("這就是 Turing 的證明！")


def simple_halting_examples():
    """展示一些簡單程式的停機行為（這些我們可以手動分析）"""
    print("=== 簡單程式的停機分析 ===")
    print()

    # 會停機的程式
    def program1():
        return 1 + 1

    print("程式 1: def program1(): return 1 + 1")
    print("結果: 會停機 ✓")
    print()

    # 會停機的迴圈
    def program2():
        for i in range(10):
            pass

    print("程式 2: def program2(): for i in range(10): pass")
    print("結果: 會停機 ✓")
    print()

    # 不會停機的程式（無限迴圈）
    def program3():
        while True:
            pass

    print("程式 3: def program3(): while True: pass")
    print("結果: 不會停機 (無限迴圈)")
    print()

    # 更微妙的例子
    def program4(n):
        while n != 1:
            if n % 2 == 0:
                n = n // 2
            else:
                n = 3 * n + 1

    print("程式 4: Collatz 猜想")
    print("  def program4(n):")
    print("      while n != 1:")
    print("          if n % 2 == 0: n = n // 2")
    print("          else: n = 3 * n + 1")
    print("結果: 對於所有測試過的 n 都會停機，但尚未證明！")
    print("      （這就是著名的 Collatz 猜想）")


def rice_theorem_simple():
    """
    Rice 定理簡介

    Rice 定理：任何關於程式行為的非平凡性質都是不可判定的。

    「非平凡」：不是所有程式都有或都没有的性質
    「關於程式行為」：只看程式的輸入輸出行為，不看實作細節

    例子：
    - 「程式是否會停機？」→ 不可判定
    - 「程式是否輸出 0？」→ 不可判定
    - 「程式是否會進入無限迴圈？」→ 不可判定
    - 「程式的原始碼是否包含 while True？」→ 可判定（這是語法性質，不是行為性質）
    """
    print("=== Rice 定理 ===")
    print()
    print("Rice 定理：任何關於程式行為的非平凡性質都是不可判定的。")
    print()
    print("例子：")
    print("  - 「程式是否會停機？」→ 不可判定")
    print("  - 「程式是否輸出 0？」→ 不可判定")
    print("  - 「程式是否會崩潰？」→ 不可判定")
    print()
    print("但這些是可判定的：")
    print("  - 「程式碼是否有語法錯誤？」→ 可判定（語法分析）")
    print("  - 「程式是否使用變數 x？」→ 可判定（程式分析）")


if __name__ == "__main__":
    demonstrate_paradox()
    print()
    print("=" * 50)
    print()
    simple_halting_examples()
    print()
    print("=" * 50)
    print()
    rice_theorem_simple()
