"""
第3章: PuLPによる線形計画法
============================

この章では、PuLPを使って線形計画問題を解く方法を学びます。
PuLPは直感的なAPIを提供し、より自然に問題を定義できます。
"""

from pulp import (
    PULP_CBC_CMD,
    LpMaximize,
    LpMinimize,
    LpProblem,
    LpStatus,
    LpVariable,
    lpSum,
    value,
)


def print_section(title: str) -> None:
    """セクションタイトルを表示する"""
    print("\n" + "=" * 60)
    print(f" {title}")
    print("=" * 60 + "\n")


def print_pulp_result(model) -> None:
    """PuLPの最適化結果を表示する"""
    print(f"ステータス: {LpStatus[model.status]}")
    print(f"目的関数の最適値: {value(model.objective):.4f}")
    print("決定変数の最適値:")
    for var in model.variables():
        print(f"  {var.name} = {var.varValue:.4f}")


# ============================================================
# 3.1 PuLPの基本
# ============================================================

print_section("3.1 PuLPの基本")

pulp_basics = """
PuLPはSciPyと比べて以下の利点があります：

1. 直感的な問題定義
   - Pythonの演算子（+, -, *, <=, >=, ==）で制約を定義
   - 最大化/最小化を直接指定可能

2. 複数のソルバーに対応
   - CBC（デフォルト）
   - GLPK
   - Gurobi, CPLEX など

3. 整数変数・二値変数のサポート
   - 混合整数線形計画法（MILP）に対応

【基本的な流れ】
1. LpProblem でモデルを作成
2. LpVariable で決定変数を定義
3. += 演算子で制約と目的関数を追加
4. solve() で最適化を実行
5. 結果を取得
"""
print(pulp_basics)


# ============================================================
# 例題1: 基本的な最大化問題
# ============================================================

print_section("例題1: 基本的な最大化問題")

problem1 = """
【問題】
  最大化:  z = x + 2y

  制約条件:
    2x + y  <= 20
    -4x + 5y <= 10
    -x + 2y >= -2
    x >= 0, y >= 0
"""
print(problem1)

# 1. モデルの作成（最大化問題）
model = LpProblem(name="example1", sense=LpMaximize)

# 2. 決定変数の定義
x = LpVariable(name="x", lowBound=0)  # x >= 0
y = LpVariable(name="y", lowBound=0)  # y >= 0

# 3. 制約条件の追加
model += 2 * x + y <= 20, "constraint_red"
model += -4 * x + 5 * y <= 10, "constraint_blue"
model += -x + 2 * y >= -2, "constraint_yellow"

# 4. 目的関数の追加
model += x + 2 * y, "objective"

# 5. 最適化実行
model.solve(PULP_CBC_CMD(msg=False))

# 6. 結果表示
print("【結果】")
print_pulp_result(model)

print("\n【解釈】")
print("最適解は x≈6.43, y≈7.14 で、最大値は約20.71です。")


# ============================================================
# 例題2: 基本的な最小化問題
# ============================================================

print_section("例題2: 基本的な最小化問題")

problem2 = """
【問題】
  最小化:  z = 3x + 2y

  制約条件:
    x + y  >= 4
    2x + y >= 6
    x >= 0, y >= 0
"""
print(problem2)

# モデルの作成（最小化問題）
model = LpProblem(name="example2", sense=LpMinimize)

# 決定変数の定義
x = LpVariable(name="x", lowBound=0)
y = LpVariable(name="y", lowBound=0)

# 制約条件の追加（PuLPでは>=も直接使える！）
model += x + y >= 4, "constraint1"
model += 2 * x + y >= 6, "constraint2"

# 目的関数の追加
model += 3 * x + 2 * y

# 最適化実行
model.solve(PULP_CBC_CMD(msg=False))

# 結果表示
print("【結果】")
print_pulp_result(model)

print("\n【解釈】")
print("最小値は x=2, y=2 のとき z=10 です。")


# ============================================================
# 例題3: 等式制約を含む問題
# ============================================================

print_section("例題3: 等式制約を含む問題")

problem3 = """
【問題】
  最大化:  z = x + 2y

  制約条件:
    2x + y  <= 20
    -4x + 5y <= 10
    -x + 2y >= -2
    -x + 5y = 15   （等式制約）
    x >= 0, y >= 0
"""
print(problem3)

model = LpProblem(name="example3", sense=LpMaximize)

x = LpVariable(name="x", lowBound=0)
y = LpVariable(name="y", lowBound=0)

# 不等式制約
model += 2 * x + y <= 20, "red"
model += -4 * x + 5 * y <= 10, "blue"
model += -x + 2 * y >= -2, "yellow"

# 等式制約（== を使用）
model += -x + 5 * y == 15, "green"

# 目的関数
model += x + 2 * y

model.solve(PULP_CBC_CMD(msg=False))

print("【結果】")
print_pulp_result(model)


# ============================================================
# 例題4: 複数変数の問題
# ============================================================

print_section("例題4: 複数変数と辞書を使った定義")

problem4 = """
【問題】リソース配分問題
4種類の製品の生産計画を最適化します。

          利益    人員   原材料A   原材料B
製品1:    $20     1       3         0
製品2:    $12     1       2         1
製品3:    $40     1       1         2
製品4:    $25     1       0         3

制約：人員50、原材料A100、原材料B90
"""
print(problem4)

model = LpProblem(name="resource_allocation", sense=LpMaximize)

# 辞書を使って複数の変数を定義
products = ["P1", "P2", "P3", "P4"]
x = {p: LpVariable(name=f"x_{p}", lowBound=0) for p in products}

# 利益係数
profit = {"P1": 20, "P2": 12, "P3": 40, "P4": 25}

# 資源消費量
manpower = {"P1": 1, "P2": 1, "P3": 1, "P4": 1}
material_a = {"P1": 3, "P2": 2, "P3": 1, "P4": 0}
material_b = {"P1": 0, "P2": 1, "P3": 2, "P4": 3}

# 制約条件（lpSumを使用）
model += lpSum(manpower[p] * x[p] for p in products) <= 50, "人員制約"
model += lpSum(material_a[p] * x[p] for p in products) <= 100, "原材料A"
model += lpSum(material_b[p] * x[p] for p in products) <= 90, "原材料B"

# 目的関数
model += lpSum(profit[p] * x[p] for p in products), "総利益"

model.solve(PULP_CBC_CMD(msg=False))

print("【結果】")
print(f"ステータス: {LpStatus[model.status]}")
print(f"最大利益: ${value(model.objective):.2f}")
print("\n生産計画:")
for p in products:
    print(f"  {p}: {x[p].varValue:.2f} 個")


# ============================================================
# 例題5: ブレンド問題（飼料配合）
# ============================================================

print_section("例題5: ブレンド問題（飼料配合）")

problem5 = """
【問題】
2種類の原料（A, B）を混ぜて飼料を作ります。
飼料は最低限の栄養素を含む必要があります。

           コスト   タンパク質   脂肪   繊維
原料A:     $5/kg      30%        10%    5%
原料B:     $8/kg      20%        15%    10%

必要量:
- タンパク質: 最低25%
- 脂肪: 最低12%
- 繊維: 最大8%

【目標】100kgの飼料を最小コストで作る
"""
print(problem5)

model = LpProblem(name="feed_mix", sense=LpMinimize)

# 各原料の使用量（kg）
a = LpVariable(name="原料A", lowBound=0)
b = LpVariable(name="原料B", lowBound=0)

# 総量制約
model += a + b == 100, "総量"

# 栄養素制約（パーセンテージで計算）
model += 0.30 * a + 0.20 * b >= 25, "タンパク質最低"
model += 0.10 * a + 0.15 * b >= 12, "脂肪最低"
model += 0.05 * a + 0.10 * b <= 8, "繊維最大"

# 目的関数（コスト最小化）
model += 5 * a + 8 * b, "総コスト"

model.solve(PULP_CBC_CMD(msg=False))

print("【結果】")
print(f"ステータス: {LpStatus[model.status]}")
print(f"最小コスト: ${value(model.objective):.2f}")
print(f"\n配合:")
print(f"  原料A: {a.varValue:.2f} kg")
print(f"  原料B: {b.varValue:.2f} kg")

# 栄養素の確認
protein = 0.30 * a.varValue + 0.20 * b.varValue
fat = 0.10 * a.varValue + 0.15 * b.varValue
fiber = 0.05 * a.varValue + 0.10 * b.varValue
print(f"\n栄養素:")
print(f"  タンパク質: {protein:.2f}% (最低25%)")
print(f"  脂肪: {fat:.2f}% (最低12%)")
print(f"  繊維: {fiber:.2f}% (最大8%)")


# ============================================================
# 例題6: 輸送問題
# ============================================================

print_section("例題6: 輸送問題")

problem6 = """
【問題】
3つの工場から4つの倉庫へ製品を輸送します。

供給量:
- 工場1: 100個
- 工場2: 150個
- 工場3: 120個

需要量:
- 倉庫A: 80個
- 倉庫B: 90個
- 倉庫C: 110個
- 倉庫D: 90個

輸送コスト（$/個）:
        倉庫A  倉庫B  倉庫C  倉庫D
工場1:    8      6      10     9
工場2:    9      12     13     7
工場3:    14     9      16     5

【目標】総輸送コストを最小化
"""
print(problem6)

model = LpProblem(name="transportation", sense=LpMinimize)

# データ定義
factories = ["F1", "F2", "F3"]
warehouses = ["WA", "WB", "WC", "WD"]

supply = {"F1": 100, "F2": 150, "F3": 120}
demand = {"WA": 80, "WB": 90, "WC": 110, "WD": 90}

cost = {
    ("F1", "WA"): 8,
    ("F1", "WB"): 6,
    ("F1", "WC"): 10,
    ("F1", "WD"): 9,
    ("F2", "WA"): 9,
    ("F2", "WB"): 12,
    ("F2", "WC"): 13,
    ("F2", "WD"): 7,
    ("F3", "WA"): 14,
    ("F3", "WB"): 9,
    ("F3", "WC"): 16,
    ("F3", "WD"): 5,
}

# 決定変数：各ルートの輸送量
x = {
    (f, w): LpVariable(name=f"x_{f}_{w}", lowBound=0)
    for f in factories
    for w in warehouses
}

# 供給制約
for f in factories:
    model += lpSum(x[f, w] for w in warehouses) <= supply[f], f"供給_{f}"

# 需要制約
for w in warehouses:
    model += lpSum(x[f, w] for f in factories) >= demand[w], f"需要_{w}"

# 目的関数
model += lpSum(cost[f, w] * x[f, w] for f in factories for w in warehouses)

model.solve(PULP_CBC_CMD(msg=False))

print("【結果】")
print(f"ステータス: {LpStatus[model.status]}")
print(f"最小輸送コスト: ${value(model.objective):.2f}")
print("\n輸送計画:")
print("        " + "  ".join(f"{w:>6}" for w in warehouses))
for f in factories:
    row = [f"{x[f, w].varValue:>6.0f}" for w in warehouses]
    print(f"{f}:     " + "  ".join(row))


# ============================================================
# 例題7: 投資ポートフォリオ問題
# ============================================================

print_section("例題7: 投資ポートフォリオ問題")

problem7 = """
【問題】
3種類の投資先に$100,000を配分します。

           期待リターン   リスク
株式:         12%         高
債券:          6%         低
不動産:        9%         中

制約：
- 株式への投資は全体の50%以下
- 債券への投資は最低20%
- 不動産への投資は$30,000以下

【目標】期待リターンを最大化
"""
print(problem7)

model = LpProblem(name="portfolio", sense=LpMaximize)

# 決定変数（投資額）
stock = LpVariable(name="株式", lowBound=0)
bond = LpVariable(name="債券", lowBound=0)
real_estate = LpVariable(name="不動産", lowBound=0)

total_investment = 100000

# 総額制約
model += stock + bond + real_estate == total_investment, "総額"

# 各資産の制約
model += stock <= 0.5 * total_investment, "株式上限"
model += bond >= 0.2 * total_investment, "債券下限"
model += real_estate <= 30000, "不動産上限"

# 目的関数（期待リターン）
model += 0.12 * stock + 0.06 * bond + 0.09 * real_estate

model.solve(PULP_CBC_CMD(msg=False))

print("【結果】")
print(f"ステータス: {LpStatus[model.status]}")
print(f"期待リターン: ${value(model.objective):,.2f}")
print(f"\n投資配分:")
print(f"  株式: ${stock.varValue:,.2f} ({stock.varValue / total_investment * 100:.1f}%)")
print(f"  債券: ${bond.varValue:,.2f} ({bond.varValue / total_investment * 100:.1f}%)")
print(
    f"  不動産: ${real_estate.varValue:,.2f} ({real_estate.varValue / total_investment * 100:.1f}%)"
)


# ============================================================
# まとめ
# ============================================================

print_section("第3章のまとめ")

summary = """
この章で学んだこと：

1. PuLPの基本的な使い方
   - LpProblem: モデルの作成
   - LpVariable: 決定変数の定義
   - += 演算子: 制約と目的関数の追加

2. SciPyとの違い
   - 最大化/最小化を直接指定可能
   - >=, <=, == をそのまま使用可能
   - より直感的なコード

3. 辞書とlpSumの活用
   - 複数変数を効率的に管理
   - lpSum で合計を簡潔に表現

4. 様々な問題への応用
   - リソース配分問題
   - ブレンド問題
   - 輸送問題
   - ポートフォリオ問題

次の章では、整数変数を扱う混合整数線形計画法を学びます！
"""
print(summary)


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print(" 第3章 完了！")
    print(" 次は chapter04_milp.py を実行してください")
    print("=" * 60)
