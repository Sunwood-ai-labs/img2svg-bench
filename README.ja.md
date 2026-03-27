# img2svg-bench

[English](./README.md)

`img2svg-bench` は、画像から SVG を作るツールやプリセットを比較するためのローカル実行型ベンチマークリポジトリです。

現状はまず VTracer ベースラインを再現可能にすることを重視しています。

- 明るい背景の簡易除去
- 複数 VTracer プリセットの一括実行
- CSV 集計
- SVG を埋め込んだ Markdown レポート生成

## 目的

画像から SVG への変換は見た目で語られがちですが、ベンチマークにするなら入力・条件・出力指標を揃える必要があります。

このリポジトリでは次の流れをスクリプト化します。

1. 入力画像を用意する
2. 必要なら前処理する
3. 複数プリセットで SVG 化する
4. 実行時間や複雑度を集計する
5. 比較しやすい Markdown レポートを生成する

## 現在のスクリプト

- `scripts/remove_edge_background.py`
  画像の端からつながる明るい背景を flood fill で抜き、透過 PNG を保存します。
- `scripts/vtracer_experiments.py`
  複数の VTracer プリセットをまとめて実行し、`experiment_summary.csv` を出力します。
- `scripts/build_vtracer_report.py`
  CSV から Markdown レポートを作り、代表 SVG をそのまま埋め込み表示します。

## クイックスタート

まず UV で依存を入れます。

```powershell
uv sync
```

必要なら背景除去を実行します。

```powershell
uv run python scripts/remove_edge_background.py --inputs path/to/image1.png path/to/image2.jpg
```

VTracer 実験を回します。

```powershell
uv run python scripts/vtracer_experiments.py --inputs output/preprocessed/image1.nobg.png output/preprocessed/image2.nobg.png
```

Markdown レポートを生成します。

```powershell
uv run python scripts/build_vtracer_report.py
```

生成物はデフォルトで `output/` に保存され、Git には含めません。

## 現在集計している指標

- プリセットごとの実行時間
- 出力 SVG サイズ
- パス数
- fill 色数
- 出力の幅と高さ

まだ完全なベンチマークではありませんが、比較の基準線としてはかなり使える状態です。

## 今後の拡張候補

- VTracer 以外の runner を追加する
- ロゴ、キャラクター、写真、線画、図表などのデータセット分類を作る
- render-back での画像比較指標を足す
- fidelity と editability を分けて評価する
- ベンチマーク設定を versioned に保つ

## リポジトリ方針

- ローカル生成物は `output/` に置き、コミットしません
- ローカル画像や私物画像はデフォルトで公開しません
- 任意の画像を持ち込んでローカルで比較レポートを作れる構成にします
