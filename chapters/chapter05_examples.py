"""
第5章: 実践的な例題集
=====================

この章では、様々な分野の実践的な線形計画問題を解きます。
これまで学んだ知識を総合的に活用します。
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
# 例題1: 生産計画問題（多期間）
# ============================================================

print_section("例題1: 多期間生産計画問題")

problem1 = """
【問題】
ある工場で3ヶ月間の生産計画を立てます。

月別需要予測:
  1月: 100個, 2月: 150個, 3月: 120個

コスト:
- 通常生産: $10/個（最大80個/月）
- 残業生産: $15/個（最大40個/月）
- 在庫保管: $2/個/月

初期在庫: 20個
最終在庫: 30個以上必要

【目標】総コストを最小化
"""
print(problem1)

model = LpProblem(name="multi_period_production", sense=LpMinimize)

months = [1, 2, 3]
demand = {1: 100, 2: 150, 3: 120}

# 決定変数
regular = {m: LpVariable(f"通常_{m}", 0, 80) for m in months}
overtime = {m: LpVariable(f"残業_{m}", 0, 40) for m in months}
inventory = {m: LpVariable(f"在庫_{m}", 0) for m in months}

# 初期在庫
initial_inv = 20

# 在庫バランス制約
for m in months:
    prev_inv = initial_inv if m == 1 else inventory[m - 1]
    model += (
        prev_inv + regular[m] + overtime[m] - demand[m] == inventory[m],
        f"バランス_{m}",
    )

# 最終在庫制約
model += inventory[3] >= 30, "最終在庫"

# 目的関数
model += lpSum(
    10 * regular[m] + 15 * overtime[m] + 2 * inventory[m] for m in months
)

model.solve(PULP_CBC_CMD(msg=False))

print("【結果】")
print(f"ステータス: {LpStatus[model.status]}")
print(f"総コスト: ${value(model.objective):,.0f}")

print("\n月別生産計画:")
print("月    需要  通常  残業  在庫")
print("-" * 35)
for m in months:
    print(
        f"{m}月   {demand[m]:>3}   {regular[m].varValue:>4.0f}  "
        f"{overtime[m].varValue:>4.0f}  {inventory[m].varValue:>4.0f}"
    )


# ============================================================
# 例題2: ダイエット問題（栄養最適化）
# ============================================================

print_section("例題2: ダイエット問題（栄養最適化）")

problem2 = """
【問題】
最小コストで必要な栄養素を摂取できる食事を計画します。

食品データ（100gあたり）:
            価格   カロリー  タンパク質  脂質   炭水化物
鶏肉:       $3.0     200       25g       10g      0g
魚:         $4.0     150       20g        5g      0g
米:         $1.0     350        7g        1g     77g
野菜:       $2.0      50        3g        0g     10g
卵:         $2.5     150       13g       11g      1g

1日の必要量:
- カロリー: 1800-2200 kcal
- タンパク質: 50g以上
- 脂質: 30-70g
- 炭水化物: 200-300g

【目標】コストを最小化
"""
print(problem2)

model = LpProblem(name="diet", sense=LpMinimize)

# 食品データ
foods = ["鶏肉", "魚", "米", "野菜", "卵"]
price = {"鶏肉": 3.0, "魚": 4.0, "米": 1.0, "野菜": 2.0, "卵": 2.5}
calories = {"鶏肉": 200, "魚": 150, "米": 350, "野菜": 50, "卵": 150}
protein = {"鶏肉": 25, "魚": 20, "米": 7, "野菜": 3, "卵": 13}
fat = {"鶏肉": 10, "魚": 5, "米": 1, "野菜": 0, "卵": 11}
carbs = {"鶏肉": 0, "魚": 0, "米": 77, "野菜": 10, "卵": 1}

# 決定変数（100g単位）
x = {f: LpVariable(f"x_{f}", lowBound=0) for f in foods}

# 栄養素制約
model += lpSum(calories[f] * x[f] for f in foods) >= 1800, "カロリー下限"
model += lpSum(calories[f] * x[f] for f in foods) <= 2200, "カロリー上限"
model += lpSum(protein[f] * x[f] for f in foods) >= 50, "タンパク質"
model += lpSum(fat[f] * x[f] for f in foods) >= 30, "脂質下限"
model += lpSum(fat[f] * x[f] for f in foods) <= 70, "脂質上限"
model += lpSum(carbs[f] * x[f] for f in foods) >= 200, "炭水化物下限"
model += lpSum(carbs[f] * x[f] for f in foods) <= 300, "炭水化物上限"

# 目的関数
model += lpSum(price[f] * x[f] for f in foods)

model.solve(PULP_CBC_CMD(msg=False))

print("【結果】")
print(f"ステータス: {LpStatus[model.status]}")
print(f"1日の食費: ${value(model.objective):.2f}")

print("\n食事計画（100g単位）:")
for f in foods:
    if x[f].varValue > 0.01:
        print(f"  {f}: {x[f].varValue * 100:.0f}g")

# 栄養素の計算
total_cal = sum(calories[f] * x[f].varValue for f in foods)
total_pro = sum(protein[f] * x[f].varValue for f in foods)
total_fat = sum(fat[f] * x[f].varValue for f in foods)
total_carb = sum(carbs[f] * x[f].varValue for f in foods)

print(f"\n栄養素の合計:")
print(f"  カロリー: {total_cal:.0f} kcal (1800-2200)")
print(f"  タンパク質: {total_pro:.1f}g (50以上)")
print(f"  脂質: {total_fat:.1f}g (30-70)")
print(f"  炭水化物: {total_carb:.1f}g (200-300)")


# ============================================================
# 例題3: ナップサック問題
# ============================================================

print_section("例題3: ナップサック問題")

problem3 = """
【問題】
バックパックに入れる品物を選びます。

品物:
  アイテム    重さ    価値
     A        5kg    $60
     B        3kg    $50
     C        4kg    $70
     D        2kg    $30
     E        6kg    $80
     F        1kg    $20
     G        4kg    $55

バックパックの容量: 12kg

【目標】価値の合計を最大化
"""
print(problem3)

model = LpProblem(name="knapsack", sense=LpMaximize)

items = ["A", "B", "C", "D", "E", "F", "G"]
weight = {"A": 5, "B": 3, "C": 4, "D": 2, "E": 6, "F": 1, "G": 4}
value_item = {"A": 60, "B": 50, "C": 70, "D": 30, "E": 80, "F": 20, "G": 55}
capacity = 12

# 二値変数（入れる=1, 入れない=0）
x = {i: LpVariable(f"x_{i}", cat=LpBinary) for i in items}

# 容量制約
model += lpSum(weight[i] * x[i] for i in items) <= capacity, "容量"

# 目的関数
model += lpSum(value_item[i] * x[i] for i in items)

model.solve(PULP_CBC_CMD(msg=False))

print("【結果】")
print(f"ステータス: {LpStatus[model.status]}")
print(f"総価値: ${value(model.objective):.0f}")

print("\n選択したアイテム:")
total_weight = 0
for i in items:
    if x[i].varValue == 1:
        print(f"  {i}: 重さ{weight[i]}kg, 価値${value_item[i]}")
        total_weight += weight[i]
print(f"\n使用容量: {total_weight}kg / {capacity}kg")


# ============================================================
# 例題4: 従業員スケジューリング問題
# ============================================================

print_section("例題4: 従業員スケジューリング問題")

problem4 = """
【問題】
1週間のシフトスケジュールを作成します。

曜日別の必要人数:
  月:5, 火:6, 水:7, 木:6, 金:8, 土:10, 日:4

制約:
- 各従業員は週5日連続で働く
- 利用可能な従業員: 最大15人

【目標】必要な従業員数を最小化
"""
print(problem4)

model = LpProblem(name="scheduling", sense=LpMinimize)

days = ["月", "火", "水", "木", "金", "土", "日"]
required = {"月": 5, "火": 6, "水": 7, "木": 6, "金": 8, "土": 10, "日": 4}

# シフトパターン（5日連続勤務）
# 開始日をキーとして、どの曜日に働くかを定義
shifts = {
    "月": ["月", "火", "水", "木", "金"],  # 月曜開始
    "火": ["火", "水", "木", "金", "土"],  # 火曜開始
    "水": ["水", "木", "金", "土", "日"],  # 水曜開始
    "木": ["木", "金", "土", "日", "月"],  # 木曜開始
    "金": ["金", "土", "日", "月", "火"],  # 金曜開始
    "土": ["土", "日", "月", "火", "水"],  # 土曜開始
    "日": ["日", "月", "火", "水", "木"],  # 日曜開始
}

# 決定変数（各シフトパターンの従業員数）
x = {s: LpVariable(f"shift_{s}", lowBound=0, cat=LpInteger) for s in shifts}

# 各日の必要人数を満たす制約
for d in days:
    workers_on_day = lpSum(x[s] for s in shifts if d in shifts[s])
    model += workers_on_day >= required[d], f"必要人数_{d}"

# 目的関数（総従業員数）
model += lpSum(x[s] for s in shifts)

model.solve(PULP_CBC_CMD(msg=False))

print("【結果】")
print(f"ステータス: {LpStatus[model.status]}")
print(f"必要な従業員数: {value(model.objective):.0f}人")

print("\nシフトパターン別の人数:")
for s in shifts:
    if x[s].varValue > 0:
        print(f"  {s}曜開始: {x[s].varValue:.0f}人 → 勤務日: {', '.join(shifts[s])}")

print("\n曜日別の配置人数:")
for d in days:
    actual = sum(x[s].varValue for s in shifts if d in shifts[s])
    print(f"  {d}: {actual:.0f}人 (必要: {required[d]}人)")


# ============================================================
# 例題5: 割当問題（タスク割当）
# ============================================================

print_section("例題5: 割当問題（タスク割当）")

problem5 = """
【問題】
4人の従業員に4つのタスクを割り当てます。
各従業員がタスクを完了するのにかかる時間（時間）:

        タスク1  タスク2  タスク3  タスク4
従業員A:    8       6       5       7
従業員B:    6       7       8       6
従業員C:    9       5       6       8
従業員D:    7       8       7       5

制約:
- 各従業員は1つのタスクのみ担当
- 各タスクは1人の従業員のみが担当

【目標】総作業時間を最小化
"""
print(problem5)

model = LpProblem(name="assignment", sense=LpMinimize)

workers = ["A", "B", "C", "D"]
tasks = [1, 2, 3, 4]

time_matrix = {
    ("A", 1): 8,
    ("A", 2): 6,
    ("A", 3): 5,
    ("A", 4): 7,
    ("B", 1): 6,
    ("B", 2): 7,
    ("B", 3): 8,
    ("B", 4): 6,
    ("C", 1): 9,
    ("C", 2): 5,
    ("C", 3): 6,
    ("C", 4): 8,
    ("D", 1): 7,
    ("D", 2): 8,
    ("D", 3): 7,
    ("D", 4): 5,
}

# 二値変数
x = {
    (w, t): LpVariable(f"x_{w}_{t}", cat=LpBinary) for w in workers for t in tasks
}

# 各従業員は1つのタスクのみ
for w in workers:
    model += lpSum(x[w, t] for t in tasks) == 1, f"従業員_{w}"

# 各タスクは1人のみ
for t in tasks:
    model += lpSum(x[w, t] for w in workers) == 1, f"タスク_{t}"

# 目的関数
model += lpSum(time_matrix[w, t] * x[w, t] for w in workers for t in tasks)

model.solve(PULP_CBC_CMD(msg=False))

print("【結果】")
print(f"ステータス: {LpStatus[model.status]}")
print(f"総作業時間: {value(model.objective):.0f}時間")

print("\n割当結果:")
for w in workers:
    for t in tasks:
        if x[w, t].varValue == 1:
            print(f"  従業員{w} → タスク{t} ({time_matrix[w, t]}時間)")


# ============================================================
# 例題6: カッティングストック問題
# ============================================================

print_section("例題6: カッティングストック問題")

problem6 = """
【問題】
長さ10mの原材料を切断して、必要な長さの製品を作ります。

必要な製品:
- 3mの製品: 25本
- 4mの製品: 20本
- 5mの製品: 15本

カットパターン（例）:
- パターン1: 3m×3本 = 9m使用（残り1m）
- パターン2: 3m×2本 + 4m×1本 = 10m使用
- パターン3: 4m×2本 = 8m使用
- パターン4: 5m×2本 = 10m使用
- パターン5: 3m×1本 + 4m×1本 = 7m使用
- パターン6: 5m×1本 + 3m×1本 = 8m使用
- パターン7: 5m×1本 + 4m×1本 = 9m使用

【目標】使用する原材料の本数を最小化
"""
print(problem6)

model = LpProblem(name="cutting_stock", sense=LpMinimize)

# 製品サイズと必要数
products = {3: 25, 4: 20, 5: 15}  # {長さ: 必要数}

# カットパターン {パターン名: {製品長: 本数}}
patterns = {
    "P1": {3: 3, 4: 0, 5: 0},  # 3m×3本
    "P2": {3: 2, 4: 1, 5: 0},  # 3m×2本 + 4m×1本
    "P3": {3: 0, 4: 2, 5: 0},  # 4m×2本
    "P4": {3: 0, 4: 0, 5: 2},  # 5m×2本
    "P5": {3: 1, 4: 1, 5: 0},  # 3m×1本 + 4m×1本
    "P6": {3: 1, 4: 0, 5: 1},  # 5m×1本 + 3m×1本
    "P7": {3: 0, 4: 1, 5: 1},  # 5m×1本 + 4m×1本
}

# 決定変数（各パターンを使用する回数）
x = {p: LpVariable(f"x_{p}", lowBound=0, cat=LpInteger) for p in patterns}

# 需要充足制約
for length, required in products.items():
    model += (
        lpSum(patterns[p][length] * x[p] for p in patterns) >= required,
        f"需要_{length}m",
    )

# 目的関数（使用する原材料の本数）
model += lpSum(x[p] for p in patterns)

model.solve(PULP_CBC_CMD(msg=False))

print("【結果】")
print(f"ステータス: {LpStatus[model.status]}")
print(f"使用する原材料: {value(model.objective):.0f}本")

print("\nカットパターンの使用回数:")
for p in patterns:
    if x[p].varValue > 0:
        pattern_desc = "+".join(f"{length}m×{count}" for length, count in patterns[p].items() if count > 0)
        print(f"  {p}: {x[p].varValue:.0f}回 ({pattern_desc})")

# 生産数の確認
print("\n製品の生産数:")
for length, required in products.items():
    produced = sum(patterns[p][length] * x[p].varValue for p in patterns)
    print(f"  {length}m: {produced:.0f}本 (必要: {required}本)")


# ============================================================
# 例題7: 最短経路問題
# ============================================================

print_section("例題7: 最短経路問題")

problem7 = """
【問題】
ノードAからノードFまでの最短経路を求めます。

ネットワーク（距離）:
  A → B: 4,  A → C: 2
  B → C: 1,  B → D: 5
  C → D: 8,  C → E: 10
  D → E: 2,  D → F: 6
  E → F: 3

【目標】A→Fの最短距離を求める
"""
print(problem7)

model = LpProblem(name="shortest_path", sense=LpMinimize)

# グラフの定義
edges = {
    ("A", "B"): 4,
    ("A", "C"): 2,
    ("B", "C"): 1,
    ("B", "D"): 5,
    ("C", "D"): 8,
    ("C", "E"): 10,
    ("D", "E"): 2,
    ("D", "F"): 6,
    ("E", "F"): 3,
}

nodes = ["A", "B", "C", "D", "E", "F"]
source = "A"
sink = "F"

# 決定変数（各辺を使うかどうか）
x = {e: LpVariable(f"x_{e[0]}_{e[1]}", cat=LpBinary) for e in edges}

# フロー保存制約
for n in nodes:
    outflow = lpSum(x[e] for e in edges if e[0] == n)
    inflow = lpSum(x[e] for e in edges if e[1] == n)

    if n == source:
        model += outflow - inflow == 1, f"フロー_{n}"
    elif n == sink:
        model += outflow - inflow == -1, f"フロー_{n}"
    else:
        model += outflow - inflow == 0, f"フロー_{n}"

# 目的関数
model += lpSum(edges[e] * x[e] for e in edges)

model.solve(PULP_CBC_CMD(msg=False))

print("【結果】")
print(f"ステータス: {LpStatus[model.status]}")
print(f"最短距離: {value(model.objective):.0f}")

print("\n最短経路:")
path = []
for e in edges:
    if x[e].varValue == 1:
        path.append(e)
        print(f"  {e[0]} → {e[1]}: {edges[e]}")

# 経路の順序で表示
current = source
route = [current]
while current != sink:
    for e in edges:
        if e[0] == current and x[e].varValue == 1:
            current = e[1]
            route.append(current)
            break
print(f"\n経路: {' → '.join(route)}")


# ============================================================
# 例題8: ビンパッキング問題
# ============================================================

print_section("例題8: ビンパッキング問題")

problem8 = """
【問題】
容量10の箱に、様々なサイズのアイテムを詰めます。

アイテムのサイズ:
  1: 6,  2: 5,  3: 4,  4: 4,  5: 3,  6: 3,  7: 2,  8: 2

【目標】使用する箱の数を最小化
"""
print(problem8)

model = LpProblem(name="bin_packing", sense=LpMinimize)

items = [1, 2, 3, 4, 5, 6, 7, 8]
size = {1: 6, 2: 5, 3: 4, 4: 4, 5: 3, 6: 3, 7: 2, 8: 2}
bin_capacity = 10

# 箱の数（最大でアイテム数と同じ）
bins = list(range(1, len(items) + 1))

# 決定変数
y = {b: LpVariable(f"bin_{b}", cat=LpBinary) for b in bins}  # 箱を使うか
x = {
    (i, b): LpVariable(f"item_{i}_bin_{b}", cat=LpBinary)
    for i in items
    for b in bins
}

# 各アイテムは1つの箱に入れる
for i in items:
    model += lpSum(x[i, b] for b in bins) == 1, f"アイテム_{i}"

# 箱の容量制約
for b in bins:
    model += lpSum(size[i] * x[i, b] for i in items) <= bin_capacity * y[b], f"容量_{b}"

# 対称性を破る制約（箱を番号順に使用）
for b in bins[:-1]:
    model += y[b] >= y[b + 1], f"対称性_{b}"

# 目的関数
model += lpSum(y[b] for b in bins)

model.solve(PULP_CBC_CMD(msg=False))

print("【結果】")
print(f"ステータス: {LpStatus[model.status]}")
print(f"使用する箱の数: {value(model.objective):.0f}")

print("\n箱の中身:")
for b in bins:
    if y[b].varValue == 1:
        items_in_bin = [i for i in items if x[i, b].varValue == 1]
        sizes_in_bin = [size[i] for i in items_in_bin]
        total = sum(sizes_in_bin)
        print(f"  箱{b}: アイテム{items_in_bin} (サイズ: {sizes_in_bin}, 合計: {total}/{bin_capacity})")


# ============================================================
# まとめ
# ============================================================

print_section("第5章のまとめ")

summary = """
この章で学んだ実践的な問題：

1. 多期間生産計画問題
   - 在庫を考慮した計画
   - 通常生産と残業生産

2. ダイエット問題（栄養最適化）
   - 複数の制約条件
   - 実用的な食事計画

3. ナップサック問題
   - 組合せ最適化の基本
   - 二値変数の活用

4. 従業員スケジューリング
   - シフトパターンの設計
   - 整数変数による人数決定

5. 割当問題
   - 1対1の対応関係
   - 行列形式のデータ

6. カッティングストック問題
   - パターン列挙法
   - 廃棄量の最小化

7. 最短経路問題
   - グラフ上の最適化
   - フロー保存制約

8. ビンパッキング問題
   - 容量制約付きの詰め込み
   - 対称性を破る制約

【総括】
線形計画法と混合整数線形計画法は、
ビジネスや工学の様々な問題に適用できる強力なツールです。
PuLPを使えば、Pythonで手軽に実装できます。
"""
print(summary)


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print(" チュートリアル完了！")
    print("=" * 60)
    print("""
お疲れさまでした！このチュートリアルで学んだこと：

- 第1章: 線形計画法の基礎概念
- 第2章: SciPyによる実装
- 第3章: PuLPによる実装
- 第4章: 混合整数線形計画法（MILP）
- 第5章: 実践的な例題集

次のステップ：
- より複雑な問題への挑戦
- 他のソルバー（Gurobi, CPLEX）の試用
- 大規模問題の効率的な解法の学習
""")
