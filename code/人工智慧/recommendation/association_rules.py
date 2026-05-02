"""關聯規則挖掘與Apriori算法實作"""

from typing import List, Tuple, Dict, Set
from collections import defaultdict


def generate_candidates(prev_frequent: List[Set[str]], k: int) -> List[Set[str]]:
    """生成k項候選集

    Args:
        prev_frequent: 前一輪的頻繁項集
        k: 當前項集大小

    Returns:
        候選k項集列表
    """
    candidates = []
    n = len(prev_frequent)
    for i in range(n):
        for j in range(i + 1, n):
            itemset_i = list(prev_frequent[i])
            itemset_j = list(prev_frequent[j])
            itemset_i.sort()
            itemset_j.sort()
            if itemset_i[:k-2] == itemset_j[:k-2]:
                candidate = prev_frequent[i] | prev_frequent[j]
                if len(candidate) == k:
                    candidates.append(candidate)
    return candidates


def prune_candidates(candidates: List[Set[str]], prev_frequent: List[Set[str]]) -> List[Set[str]]:
    """剪枝：移除包含非頻繁子集的候選項集

    Args:
        candidates: 候選項集列表
        prev_frequent: 前一輪的頻繁項集

    Returns:
        剪枝後的候選項集列表
    """
    prev_set = set(frozenset(s) for s in prev_frequent)
    pruned = []
    for candidate in candidates:
        all_subsets_frequent = True
        items = list(candidate)
        for i in range(len(items)):
            subset = set(items[:i] + items[i+1:])
            if frozenset(subset) not in prev_set:
                all_subsets_frequent = False
                break
        if all_subsets_frequent:
            pruned.append(candidate)
    return pruned


def apriori(transactions: List[List[str]], min_support: float) -> Tuple[Dict[frozenset, int], Dict[frozenset, float]]:
    """Apriori算法挖掘頻繁項集

    Args:
        transactions: 交易數據，每筆交易為物品列表
        min_support: 最小支持度閾值（0到1之間）

    Returns:
        (頻繁項集字典, 支持度字典)
    """
    num_transactions = len(transactions)
    min_count = min_support * num_transactions
    item_counts = defaultdict(int)
    for transaction in transactions:
        for item in transaction:
            item_counts[frozenset([item])] += 1
    frequent_1 = []
    frequent_itemsets = {}
    for item, count in item_counts.items():
        if count >= min_count:
            frequent_1.append(item)
            frequent_itemsets[item] = count
    prev_frequent = [set(s) for s in frequent_1]
    k = 2
    while prev_frequent:
        candidates = generate_candidates(prev_frequent, k)
        candidates = prune_candidates(candidates, prev_frequent)
        candidate_counts = defaultdict(int)
        for transaction in transactions:
            transaction_set = set(transaction)
            for candidate in candidates:
                if candidate.issubset(transaction_set):
                    candidate_counts[frozenset(candidate)] += 1
        current_frequent = []
        for candidate, count in candidate_counts.items():
            if count >= min_count:
                frequent_itemsets[candidate] = count
                current_frequent.append(set(candidate))
        prev_frequent = current_frequent
        k += 1
    support_dict = {itemset: count / num_transactions for itemset, count in frequent_itemsets.items()}
    return frequent_itemsets, support_dict


def generate_rules(frequent_itemsets: Dict[frozenset, int], support_dict: Dict[frozenset, float],
                   min_confidence: float, num_transactions: int) -> List[Tuple[Set[str], Set[str], float, float, float]]:
    """從頻繁項集生成關聯規則

    Args:
        frequent_itemsets: 頻繁項集字典
        support_dict: 支持度字典
        min_confidence: 最小置信度閾值
        num_transactions: 交易總數

    Returns:
        規則列表，每條規則為(前件, 後件, 支持度, 置信度, 提升度)
    """
    rules = []
    for itemset, count in frequent_itemsets.items():
        if len(itemset) < 2:
            continue
        items = list(itemset)
        for i in range(1, len(items)):
            from itertools import combinations
            for antecedent_tuple in combinations(items, i):
                antecedent = set(antecedent_tuple)
                consequent = set(items) - antecedent
                antecedent_frozen = frozenset(antecedent)
                if antecedent_frozen not in frequent_itemsets:
                    continue
                support = count / num_transactions
                confidence = count / frequent_itemsets[antecedent_frozen]
                consequent_support = support_dict.get(frozenset(consequent), 0)
                lift = confidence / consequent_support if consequent_support > 0 else 0
                if confidence >= min_confidence:
                    rules.append((antecedent, consequent, support, confidence, lift))
    return rules


def market_basket_analysis(transactions: List[List[str]], min_support: float = 0.2,
                           min_confidence: float = 0.5) -> None:
    """市場籃子分析演示

    Args:
        transactions: 交易數據
        min_support: 最小支持度
        min_confidence: 最小置信度
    """
    print("=== 市場籃子分析 ===")
    print(f"交易數量: {len(transactions)}")
    print(f"最小支持度: {min_support}, 最小置信度: {min_confidence}")
    frequent_itemsets, support_dict = apriori(transactions, min_support)
    print(f"\n頻繁項集數量: {len(frequent_itemsets)}")
    for itemset, support in sorted(support_dict.items(), key=lambda x: -x[1])[:10]:
        print(f"  {set(itemset)}: 支持度={support:.3f}")
    rules = generate_rules(frequent_itemsets, support_dict, min_confidence, len(transactions))
    print(f"\n關聯規則數量: {len(rules)}")
    for antecedent, consequent, support, confidence, lift in sorted(rules, key=lambda x: -x[3])[:10]:
        print(f"  {antecedent} => {consequent}")
        print(f"    支持度={support:.3f}, 置信度={confidence:.3f}, 提升度={lift:.3f}")


if __name__ == "__main__":
    # 示例交易數據
    transactions = [
        ["牛奶", "麵包", "雞蛋"],
        ["牛奶", "麵包", "奶油"],
        ["麵包", "雞蛋", "奶油"],
        ["牛奶", "雞蛋"],
        ["麵包", "奶油"],
        ["牛奶", "麵包", "雞蛋", "奶油"],
        ["牛奶", "麵包"],
        ["雞蛋", "奶油"],
        ["麵包", "雞蛋"],
        ["牛奶", "奶油"]
    ]
    print("關聯規則挖掘演示")
    market_basket_analysis(transactions, min_support=0.3, min_confidence=0.5)
