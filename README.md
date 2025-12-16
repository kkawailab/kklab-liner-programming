# 線形計画法チュートリアル（Python / Julia）

このリポジトリは、PythonとJuliaを使った線形計画法（Linear Programming）の学習用チュートリアルです。

## 目次

### 第1章: 線形計画法の基礎
- 線形計画法とは
- 混合整数線形計画法とは
- 基本用語の解説（目的関数、制約条件、決定変数）
- 実行可能領域と最適解

| Python版 | Jupyter Notebook版 | Julia版 |
|----------|-------------------|---------|
| [chapter01_basics.py](./chapters/chapter01_basics.py) | [chapter01_basics.ipynb](./notebooks/chapter01_basics.ipynb) | [chapter01_basics.ipynb](./notebooks_julia/chapter01_basics.ipynb) |

### 第2章: SciPyによる線形計画法 / JuMPの基本
- SciPyのインストール
- `scipy.optimize.linprog()`の使い方
- 例題1: 基本的な線形計画問題
- 例題2: 等式制約を含む問題
- 例題3: リソース配分問題

| Python版 | Jupyter Notebook版 | Julia版 |
|----------|-------------------|---------|
| [chapter02_scipy.py](./chapters/chapter02_scipy.py) | [chapter02_scipy.ipynb](./notebooks/chapter02_scipy.ipynb) | [chapter02_jump_basics.ipynb](./notebooks_julia/chapter02_jump_basics.ipynb) |

### 第3章: PuLPによる線形計画法 / JuMPの応用
- PuLPのインストール
- PuLPの基本的な使い方
- 例題1: 最大化問題
- 例題2: 最小化問題
- 例題3: 複数の制約条件を持つ問題

| Python版 | Jupyter Notebook版 | Julia版 |
|----------|-------------------|---------|
| [chapter03_pulp.py](./chapters/chapter03_pulp.py) | [chapter03_pulp.ipynb](./notebooks/chapter03_pulp.ipynb) | [chapter03_jump_advanced.ipynb](./notebooks_julia/chapter03_jump_advanced.ipynb) |

### 第4章: 混合整数線形計画法
- 整数変数と二値変数
- 例題1: 整数制約付き問題
- 例題2: 二値変数を使った論理制約
- 例題3: 製造計画問題

| Python版 | Jupyter Notebook版 | Julia版 |
|----------|-------------------|---------|
| [chapter04_milp.py](./chapters/chapter04_milp.py) | [chapter04_milp.ipynb](./notebooks/chapter04_milp.ipynb) | [chapter04_milp.ipynb](./notebooks_julia/chapter04_milp.ipynb) |

### 第5章: 実践的な例題集
- 例題1: 生産計画問題
- 例題2: 輸送問題
- 例題3: ダイエット問題（栄養最適化）
- 例題4: ナップサック問題
- 例題5: 従業員スケジューリング問題

| Python版 | Jupyter Notebook版 | Julia版 |
|----------|-------------------|---------|
| [chapter05_examples.py](./chapters/chapter05_examples.py) | [chapter05_examples.ipynb](./notebooks/chapter05_examples.ipynb) | [chapter05_examples.ipynb](./notebooks_julia/chapter05_examples.ipynb) |

## 環境構築

### Python

```bash
# 依存関係のインストール
pip install scipy pulp jupyterlab

# または uv を使用する場合
uv sync
```

### Julia

```julia
# Juliaの対話環境で以下を実行
using Pkg
Pkg.add(["JuMP", "HiGHS", "IJulia"])
```

IJuliaをインストールすると、JupyterLabからJuliaカーネルを使用できます。

## 実行方法

### Python版

各章のPythonファイルを直接実行できます：

```bash
python chapters/chapter01_basics.py
python chapters/chapter02_scipy.py
python chapters/chapter03_pulp.py
python chapters/chapter04_milp.py
python chapters/chapter05_examples.py
```

### Jupyter Notebook版

JupyterLabを起動してノートブックを開きます：

```bash
# JupyterLabを起動
jupyter lab

# または uv を使用する場合
uv run jupyter lab
```

起動後、`notebooks/` フォルダ内の `.ipynb` ファイルを開いてください。

### Julia Jupyter Notebook版

JupyterLabを起動し、Juliaカーネルを選択してノートブックを開きます：

```bash
# JupyterLabを起動
jupyter lab
```

起動後、`notebooks_julia/` フォルダ内の `.ipynb` ファイルを開いてください。
カーネルとして「Julia」を選択します。

## ファイル構成

```
kklab-liner-programming/
├── README.md
├── pyproject.toml
├── chapters/                # Python版チュートリアル
│   ├── chapter01_basics.py
│   ├── chapter02_scipy.py
│   ├── chapter03_pulp.py
│   ├── chapter04_milp.py
│   └── chapter05_examples.py
├── notebooks/               # Python Jupyter Notebook版チュートリアル
│   ├── chapter01_basics.ipynb
│   ├── chapter02_scipy.ipynb
│   ├── chapter03_pulp.ipynb
│   ├── chapter04_milp.ipynb
│   └── chapter05_examples.ipynb
└── notebooks_julia/         # Julia Jupyter Notebook版チュートリアル
    ├── chapter01_basics.ipynb
    ├── chapter02_jump_basics.ipynb
    ├── chapter03_jump_advanced.ipynb
    ├── chapter04_milp.ipynb
    └── chapter05_examples.ipynb
```

## 参考資料

### Python
- [Real Python - Hands-On Linear Programming](https://realpython.com/linear-programming-python/)
- [SciPy Documentation](https://docs.scipy.org/doc/scipy/reference/optimize.html)
- [PuLP Documentation](https://coin-or.github.io/pulp/)

### Julia
- [JuMP Documentation](https://jump.dev/JuMP.jl/stable/)
- [HiGHS Documentation](https://highs.dev/)
- [JuMP Tutorials](https://jump.dev/JuMP.jl/stable/tutorials/)

## 更新履歴

| 日付 | 内容 |
|------|------|
| 2025-12-17 | 初版リリース：Pythonスクリプト版チュートリアル（第1章〜第5章）を追加 |
| 2025-12-17 | Python Jupyter Notebook版を追加 |
| 2025-12-17 | Julia Jupyter Notebook版（JuMP, HiGHS使用）を追加 |
| 2025-12-17 | CLAUDE.md を追加 |
| 2025-12-17 | Notebookの実行結果を保存 |
