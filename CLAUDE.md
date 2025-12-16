# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

線形計画法（LP）と混合整数線形計画法（MILP）の学習用チュートリアル。Python（SciPy, PuLP）とJulia（JuMP, HiGHS）の両方に対応。

## Commands

### Python

```bash
# 依存関係のインストール
uv sync

# チュートリアルの実行
python chapters/chapter01_basics.py
python chapters/chapter02_scipy.py
python chapters/chapter03_pulp.py
python chapters/chapter04_milp.py
python chapters/chapter05_examples.py

# Jupyter Notebookの起動
uv run jupyter lab
```

### Julia

```julia
# パッケージのインストール（初回のみ）
using Pkg
Pkg.add(["JuMP", "HiGHS", "IJulia"])
```

## Architecture

3つの形式で同じチュートリアル内容を提供：

- `chapters/` - Python スクリプト版（SciPy, PuLP使用）
- `notebooks/` - Python Jupyter Notebook版
- `notebooks_julia/` - Julia Jupyter Notebook版（JuMP, HiGHS使用）

各章の対応：
| 章 | Python | Julia |
|----|--------|-------|
| 第1章 | LP基礎概念 | LP基礎概念 |
| 第2章 | SciPy (`linprog`) | JuMP基本 |
| 第3章 | PuLP | JuMP応用 |
| 第4章 | MILP（整数/二値変数） | MILP |
| 第5章 | 実践例題 | 実践例題 |

## Dependencies

- Python 3.13+, scipy, pulp, jupyterlab
- Julia: JuMP, HiGHS, IJulia
