# はじめに

## 前提条件

- Python 3.11 以上
- [UV](https://docs.astral.sh/uv/) のインストール
- Node.js 20+（ドキュメントサイトのビルド時のみ）

## 依存関係のインストール

```powershell
uv sync
```

`pyproject.toml` に基づいて Python 依存関係を導入します。

## 背景除去（任意）

実験前に明るい端の背景を除去します。

```powershell
uv run python scripts/remove_edge_background.py --inputs path/to/input.png
```

複数画像を一度に処理できます。

```powershell
uv run python scripts/remove_edge_background.py --inputs path/to/input1.png path/to/input2.jpg
```

## ベンチマーク実行

```powershell
uv run python scripts/vtracer_experiments.py --inputs output/preprocessed/input1.nobg.png output/preprocessed/input2.nobg.png
```

`output/vtracer/experiments/experiment_summary.csv` に結果が出力されます。

## レポート生成

```powershell
uv run python scripts/build_vtracer_report.py
```

`output/vtracer/experiments/report.md` には以下が含まれます。

- プリセット別の結果
- SVG プレビュー
- 実行時間 / 構造指標

## ローカルドキュメント確認

```bash
npm install
npm run docs:dev
npm run docs:build
```
