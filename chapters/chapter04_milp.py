"""
第4章: 混合整数線形計画法（MILP）
=================================

この章では、整数変数と二値変数を含む混合整数線形計画法を学びます。
実際の問題では、「個数」や「Yes/No の判断」など整数でなければ
意味をなさない変数が多く存在します。
"""

from pulp import (
    PULP_CBC_CMD,
    LpBinary,
    LpInteger,
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


# ============================================================
# 4.1 整数変数と二値変数
# ============================================================

print_section("4.1 整数変数と二値変数の基本")

milp_basics = """
【変数の種類】

1. 連続変数（Continuous）
   - デフォルト、任意の実数値
   - LpVariable(name="x", cat="Continuous")

2. 整数変数（Integer）
   - 整数値のみ（..., -2, -1, 0, 1, 2, ...）
   - LpVariable(name="x", cat="Integer")
   - または LpVariable(name="x", cat=LpInteger)

3. 二値変数（Binary）
   - 0または1のみ
   - LpVariable(name="x", cat="Binary")
   - または LpVariable(name="x", cat=LpBinary)

【二値変数の用途】
- Yes/No の意思決定
- 論理条件の表現
- 選択問題のモデル化
"""
print(milp_basics)


# ============================================================
# 例題1: 整数変数を含む生産計画
# ============================================================

print_section("例題1: 整数変数を含む生産計画")

problem1 = """
【問題】
工場で2種類の製品を生産します。
製品は「個」単位でしか生産できません（整数制約）。

         利益    機械時間   人員
製品A:   $50      2時間     3人
製品B:   $40      3時間     2人

制約：
- 機械時間: 1日12時間まで
- 人員: 1日10人まで

【目標】利益を最大化する生産量（整数）を求める
"""
print(problem1)

model = LpProblem(name="production_integer", sense=LpMaximize)

# 整数変数として定義
x_a = LpVariable(name="製品A", lowBound=0, cat=LpInteger)
x_b = LpVariable(name="製品B", lowBound=0, cat=LpInteger)

# 制約条件
model += 2 * x_a + 3 * x_b <= 12, "機械時間"
model += 3 * x_a + 2 * x_b <= 10, "人員"

# 目的関数
model += 50 * x_a + 40 * x_b

model.solve(PULP_CBC_CMD(msg=False))

print("【結果】")
print(f"ステータス: {LpStatus[model.status]}")
print(f"最大利益: ${value(model.objective):.0f}")
print(f"\n生産量:")
print(f"  製品A: {x_a.varValue:.0f} 個")
print(f"  製品B: {x_b.varValue:.0f} 個")

# 連続変数の場合と比較
print("\n【参考】連続変数の場合:")
model_cont = LpProblem(name="production_continuous", sense=LpMaximize)
x_a_cont = LpVariable(name="製品A", lowBound=0)
x_b_cont = LpVariable(name="製品B", lowBound=0)
model_cont += 2 * x_a_cont + 3 * x_b_cont <= 12
model_cont += 3 * x_a_cont + 2 * x_b_cont <= 10
model_cont += 50 * x_a_cont + 40 * x_b_cont
model_cont.solve(PULP_CBC_CMD(msg=False))
print(f"  製品A: {x_a_cont.varValue:.2f} 個, 製品B: {x_b_cont.varValue:.2f} 個")
print(f"  最大利益: ${value(model_cont.objective):.2f}")
print("  → 整数制約により、解が異なる場合があります")


# ============================================================
# 例題2: 二値変数による選択問題
# ============================================================

print_section("例題2: プロジェクト選択問題")

problem2 = """
【問題】
5つのプロジェクト候補があり、予算$100,000でどれを実行するか決定します。

プロジェクト  コスト      期待利益
    A        $30,000      $50,000
    B        $40,000      $60,000
    C        $25,000      $35,000
    D        $35,000      $55,000
    E        $20,000      $25,000

【目標】予算内で期待利益を最大化
"""
print(problem2)

model = LpProblem(name="project_selection", sense=LpMaximize)

# プロジェクトデータ
projects = ["A", "B", "C", "D", "E"]
cost = {"A": 30000, "B": 40000, "C": 25000, "D": 35000, "E": 20000}
profit = {"A": 50000, "B": 60000, "C": 35000, "D": 55000, "E": 25000}
budget = 100000

# 二値変数（実行する=1, しない=0）
x = {p: LpVariable(name=f"x_{p}", cat=LpBinary) for p in projects}

# 予算制約
model += lpSum(cost[p] * x[p] for p in projects) <= budget, "予算"

# 目的関数
model += lpSum(profit[p] * x[p] for p in projects)

model.solve(PULP_CBC_CMD(msg=False))

print("【結果】")
print(f"ステータス: {LpStatus[model.status]}")
print(f"期待総利益: ${value(model.objective):,.0f}")
print(f"\n選択されたプロジェクト:")
total_cost = 0
for p in projects:
    if x[p].varValue == 1:
        print(f"  {p}: コスト ${cost[p]:,}, 利益 ${profit[p]:,}")
        total_cost += cost[p]
print(f"\n使用予算: ${total_cost:,} / ${budget:,}")


# ============================================================
# 例題3: 論理制約（「どちらか一方」）
# ============================================================

print_section("例題3: 論理制約（排他的選択）")

problem3 = """
【問題】
リソース配分問題（第2章の例題）に論理制約を追加します。

機械の制約により、製品1と製品3は同時に生産できません。
「製品1を生産するなら製品3は生産しない」という制約です。

【技法】Big-M法
二値変数 y を使って、排他的制約を表現します：
  x1 <= M * y1        （y1=0 なら x1=0）
  x3 <= M * y3        （y3=0 なら x3=0）
  y1 + y3 <= 1        （y1かy3の一方のみ1）
"""
print(problem3)

model = LpProblem(name="exclusive_production", sense=LpMaximize)

# 製品の生産量（連続変数）
x = {i: LpVariable(name=f"x{i}", lowBound=0) for i in range(1, 5)}

# 製品1と3の選択を表す二値変数
y = {1: LpVariable(name="y1", cat=LpBinary), 3: LpVariable(name="y3", cat=LpBinary)}

# 利益係数
profit = {1: 20, 2: 12, 3: 40, 4: 25}

# 通常の制約
model += x[1] + x[2] + x[3] + x[4] <= 50, "人員"
model += 3 * x[1] + 2 * x[2] + x[3] <= 100, "原材料A"
model += x[2] + 2 * x[3] + 3 * x[4] <= 90, "原材料B"

# Big-M法による論理制約
M = 100  # 十分大きな数
model += x[1] <= M * y[1], "x1_bigM"
model += x[3] <= M * y[3], "x3_bigM"
model += y[1] + y[3] <= 1, "排他的制約"

# 目的関数
model += lpSum(profit[i] * x[i] for i in range(1, 5))

model.solve(PULP_CBC_CMD(msg=False))

print("【結果】")
print(f"ステータス: {LpStatus[model.status]}")
print(f"最大利益: ${value(model.objective):.2f}")
print(f"\n生産計画:")
for i in range(1, 5):
    print(f"  製品{i}: {x[i].varValue:.2f} 個")
print(f"\n選択:")
print(f"  製品1を生産: {'はい' if y[1].varValue == 1 else 'いいえ'}")
print(f"  製品3を生産: {'はい' if y[3].varValue == 1 else 'いいえ'}")


# ============================================================
# 例題4: 固定費用を含む生産計画
# ============================================================

print_section("例題4: 固定費用を含む生産計画")

problem4 = """
【問題】
各製品ラインには、稼働させると固定費用がかかります。

         変動利益/個   固定費用   最大生産量
製品A:      $10        $50         20個
製品B:      $15        $80         15個
製品C:      $8         $30         25個

総生産時間: 30時間まで
各製品の生産時間: 1時間/個

【目標】純利益を最大化
"""
print(problem4)

model = LpProblem(name="fixed_cost", sense=LpMaximize)

products = ["A", "B", "C"]
var_profit = {"A": 10, "B": 15, "C": 8}
fixed_cost = {"A": 50, "B": 80, "C": 30}
max_prod = {"A": 20, "B": 15, "C": 25}

# 生産量（整数変数）
x = {p: LpVariable(name=f"x_{p}", lowBound=0, cat=LpInteger) for p in products}

# 製品ラインの稼働フラグ（二値変数）
y = {p: LpVariable(name=f"y_{p}", cat=LpBinary) for p in products}

# 総生産時間制約
model += lpSum(x[p] for p in products) <= 30, "生産時間"

# 生産量と稼働フラグの関係
for p in products:
    model += x[p] <= max_prod[p] * y[p], f"稼働_{p}"

# 目的関数（変動利益 - 固定費用）
model += lpSum(var_profit[p] * x[p] - fixed_cost[p] * y[p] for p in products)

model.solve(PULP_CBC_CMD(msg=False))

print("【結果】")
print(f"ステータス: {LpStatus[model.status]}")
print(f"純利益: ${value(model.objective):.0f}")
print(f"\n生産計画:")
for p in products:
    status = "稼働" if y[p].varValue == 1 else "停止"
    print(f"  製品{p}: {x[p].varValue:.0f}個 ({status})")

# 内訳
print(f"\n利益の内訳:")
total_var = sum(var_profit[p] * x[p].varValue for p in products)
total_fix = sum(fixed_cost[p] * y[p].varValue for p in products)
print(f"  変動利益: ${total_var:.0f}")
print(f"  固定費用: ${total_fix:.0f}")
print(f"  純利益: ${total_var - total_fix:.0f}")


# ============================================================
# 例題5: 施設配置問題
# ============================================================

print_section("例題5: 施設配置問題")

problem5 = """
【問題】
3つの候補地から倉庫を選び、4つの店舗に製品を供給します。

倉庫の建設コストと供給能力:
  候補地1: $500,000, 能力100
  候補地2: $400,000, 能力80
  候補地3: $600,000, 能力120

各店舗の需要:
  店舗A: 40, 店舗B: 50, 店舗C: 30, 店舗D: 60

輸送コスト（$/個）:
        店舗A  店舗B  店舗C  店舗D
候補地1:   8     10     6      7
候補地2:   5      6     9     11
候補地3:   9      7     4      5

【目標】総コスト（建設+輸送）を最小化
"""
print(problem5)

model = LpProblem(name="facility_location", sense=LpMinimize)

# データ
warehouses = [1, 2, 3]
stores = ["A", "B", "C", "D"]

build_cost = {1: 500000, 2: 400000, 3: 600000}
capacity = {1: 100, 2: 80, 3: 120}
demand = {"A": 40, "B": 50, "C": 30, "D": 60}

transport_cost = {
    (1, "A"): 8,
    (1, "B"): 10,
    (1, "C"): 6,
    (1, "D"): 7,
    (2, "A"): 5,
    (2, "B"): 6,
    (2, "C"): 9,
    (2, "D"): 11,
    (3, "A"): 9,
    (3, "B"): 7,
    (3, "C"): 4,
    (3, "D"): 5,
}

# 決定変数
y = {w: LpVariable(name=f"build_{w}", cat=LpBinary) for w in warehouses}
x = {
    (w, s): LpVariable(name=f"ship_{w}_{s}", lowBound=0)
    for w in warehouses
    for s in stores
}

# 需要充足制約
for s in stores:
    model += lpSum(x[w, s] for w in warehouses) >= demand[s], f"需要_{s}"

# 供給能力制約（倉庫が建設された場合のみ供給可能）
for w in warehouses:
    model += lpSum(x[w, s] for s in stores) <= capacity[w] * y[w], f"能力_{w}"

# 目的関数
model += lpSum(build_cost[w] * y[w] for w in warehouses) + lpSum(
    transport_cost[w, s] * x[w, s] for w in warehouses for s in stores
)

model.solve(PULP_CBC_CMD(msg=False))

print("【結果】")
print(f"ステータス: {LpStatus[model.status]}")
print(f"総コスト: ${value(model.objective):,.0f}")

print(f"\n倉庫建設:")
for w in warehouses:
    status = "建設" if y[w].varValue == 1 else "建設しない"
    print(f"  候補地{w}: {status}")

print(f"\n輸送計画:")
for w in warehouses:
    if y[w].varValue == 1:
        print(f"  候補地{w}から:")
        for s in stores:
            if x[w, s].varValue > 0:
                print(f"    → 店舗{s}: {x[w, s].varValue:.0f}個")


# ============================================================
# 例題6: ロットサイズ決定問題
# ============================================================

print_section("例題6: ロットサイズ決定問題")

problem6 = """
【問題】
4期間の生産計画を立てます。

期間ごとの需要: 期間1=40, 期間2=60, 期間3=30, 期間4=50

コスト:
- 生産セットアップ費用: $100/回
- 生産費用: $5/個
- 在庫保管費用: $2/個/期間

【制約】
- 各期間の最大生産量: 80個
- 期末在庫は非負

【目標】総コストを最小化
"""
print(problem6)

model = LpProblem(name="lot_sizing", sense=LpMinimize)

periods = [1, 2, 3, 4]
demand = {1: 40, 2: 60, 3: 30, 4: 50}

setup_cost = 100
prod_cost = 5
hold_cost = 2
max_prod = 80

# 決定変数
x = {t: LpVariable(name=f"生産_{t}", lowBound=0, cat=LpInteger) for t in periods}
y = {t: LpVariable(name=f"セットアップ_{t}", cat=LpBinary) for t in periods}
inv = {t: LpVariable(name=f"在庫_{t}", lowBound=0) for t in periods}

# 初期在庫を0とする
inv[0] = 0

# 在庫バランス制約
for t in periods:
    prev_inv = inv[t - 1] if t > 1 else 0
    model += prev_inv + x[t] - demand[t] == inv[t], f"バランス_{t}"

# セットアップ制約
for t in periods:
    model += x[t] <= max_prod * y[t], f"セットアップ_{t}"

# 目的関数
model += lpSum(
    setup_cost * y[t] + prod_cost * x[t] + hold_cost * inv[t] for t in periods
)

model.solve(PULP_CBC_CMD(msg=False))

print("【結果】")
print(f"ステータス: {LpStatus[model.status]}")
print(f"総コスト: ${value(model.objective):.0f}")

print(f"\n期間別計画:")
print("期間  需要  生産  在庫  セットアップ")
print("-" * 45)
for t in periods:
    setup = "○" if y[t].varValue == 1 else "-"
    print(
        f"  {t}    {demand[t]:>3}   {x[t].varValue:>3.0f}   {inv[t].varValue:>3.0f}      {setup}"
    )


# ============================================================
# まとめ
# ============================================================

print_section("第4章のまとめ")

summary = """
この章で学んだこと：

1. 変数の種類
   - 連続変数: cat="Continuous"（デフォルト）
   - 整数変数: cat="Integer" または LpInteger
   - 二値変数: cat="Binary" または LpBinary

2. 二値変数の活用
   - Yes/No の意思決定
   - プロジェクト選択問題
   - 施設配置問題

3. Big-M法による論理制約
   - 排他的選択（AかBのどちらか一方）
   - 条件付き制約（Aを選んだらBも必要）

4. 固定費用の扱い
   - 二値変数で稼働/非稼働を表現
   - 変動費用と固定費用を分離

5. 実践的な問題
   - ロットサイズ決定
   - 施設配置問題
   - 生産計画問題

次の章では、さらに多くの実践的な例題を学びます！
"""
print(summary)


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print(" 第4章 完了！")
    print(" 次は chapter05_examples.py を実行してください")
    print("=" * 60)
