Assignment 3 
31372

from itertools import combinations
import pandas as pd

transactions = [
    {"Fiction", "Mystery", "Fantasy"},
    {"Fiction", "Mystery"},
    {"Fiction", "Fantasy", "SciFi"},
    {"Mystery", "Fantasy"},
    {"Fiction", "Mystery", "Fantasy", "SciFi"},
    {"Fiction", "SciFi"},
    {"Mystery", "SciFi"},
    {"Fiction", "Mystery", "Fantasy"},
    {"Fantasy", "SciFi"},
    {"Fiction", "Mystery", "SciFi"},
]

MIN_SUPPORT = 0.40
MIN_CONFIDENCE = 0.60


def support(itemset, transactions):
    count = sum(1 for t in transactions if itemset.issubset(t))
    return count / len(transactions)


def get_frequent_1_itemsets(transactions, min_support):
    items = set()
    for t in transactions:
        items.update(t)

    L1 = {}
    for item in items:
        fs = frozenset({item})
        sup = support(fs, transactions)
        if sup >= min_support:
            L1[fs] = sup
    return L1


def generate_candidates(prev_frequent_itemsets, k):
    prev_itemsets = list(prev_frequent_itemsets.keys())
    candidates = set()

    for i in range(len(prev_itemsets)):
        for j in range(i + 1, len(prev_itemsets)):
            union = prev_itemsets[i] | prev_itemsets[j]
            if len(union) == k:
                candidates.add(union)

    pruned = set()
    for cand in candidates:
        subsets = combinations(cand, k - 1)
        if all(frozenset(s) in prev_frequent_itemsets for s in subsets):
            pruned.add(cand)

    return pruned


def apriori(transactions, min_support):
    all_frequent_itemsets = {}

    Lk = get_frequent_1_itemsets(transactions, min_support)
    all_frequent_itemsets.update(Lk)

    k = 1
    while Lk:
        k += 1
        candidates = generate_candidates(Lk, k)
        if not candidates:
            break

        Lk_next = {}
        for cand in candidates:
            sup = support(cand, transactions)
            if sup >= min_support:
                Lk_next[cand] = sup

        if not Lk_next:
            break

        all_frequent_itemsets.update(Lk_next)
        Lk = Lk_next

    return all_frequent_itemsets


def generate_rules(frequent_itemsets, min_confidence):
    rules = []
    for itemset, itemset_support in frequent_itemsets.items():
        if len(itemset) < 2:
            continue

        items = list(itemset)
        for r in range(1, len(items)):
            for antecedent_tuple in combinations(items, r):
                antecedent = frozenset(antecedent_tuple)
                consequent = itemset - antecedent

                antecedent_support = frequent_itemsets.get(antecedent) or support(antecedent, transactions)
                consequent_support = frequent_itemsets.get(consequent) or support(consequent, transactions)

                confidence = itemset_support / antecedent_support
                lift = confidence / consequent_support

                if confidence >= min_confidence:
                    rules.append({
                        "Rule": f"{set(antecedent)} -> {set(consequent)}",
                        "Support": round(itemset_support, 2),
                        "Confidence": round(confidence, 2),
                        "Lift": round(lift, 2),
                    })
    return rules


frequent_itemsets = apriori(transactions, MIN_SUPPORT)

freq_df = pd.DataFrame(
    [{"Itemset": set(k), "Support": round(v, 2)} for k, v in frequent_itemsets.items()]
).sort_values("Support", ascending=False).reset_index(drop=True)
print(freq_df)

rules = generate_rules(frequent_itemsets, MIN_CONFIDENCE)
rules_df = pd.DataFrame(rules).sort_values("Confidence", ascending=False).reset_index(drop=True)
print(rules_df)
