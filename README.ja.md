<div align="center">
  <img src="./docs/public/logo.svg" alt="img2svg-bench logo" width="140" />
  <h1>img2svg-bench</h1>
  <p><strong>画像から SVG を作るツール・プリセット・前処理パイプラインを比較するための、ローカル実行型ベンチマークリポジトリです。</strong></p>
  <p>
    <a href="https://github.com/Sunwood-ai-labs/img2svg-bench/actions/workflows/ci.yml"><img src="https://github.com/Sunwood-ai-labs/img2svg-bench/actions/workflows/ci.yml/badge.svg" alt="CI" /></a>
    <a href="https://sunwood-ai-labs.github.io/img2svg-bench/"><img src="https://img.shields.io/badge/docs-GitHub%20Pages-0f766e" alt="Docs" /></a>
    <a href="./LICENSE"><img src="https://img.shields.io/badge/license-MIT-14b8a6" alt="MIT License" /></a>
    <img src="https://img.shields.io/badge/python-3.11%2B-334155" alt="Python 3.11+" />
    <img src="https://img.shields.io/badge/uv-managed-0ea5e9" alt="uv managed" />
    <img src="https://img.shields.io/badge/docs-VitePress-f59e0b" alt="VitePress docs" />
  </p>
  <p>
    <strong>Language:</strong>
    <a href="./README.md">English</a> |
    <a href="./README.ja.md">日本語</a>
  </p>
</div>

## 🔍 概要
`img2svg-bench` は、ラスタ画像から SVG を生成する処理を再現可能な形で比較するためのベンチマークリポジトリです。

現時点では、VTracer ベースラインを中心に次の流れを整えています。

- 明るい背景の簡易除去
- 同一入力に対する複数プリセットの一括実行
- 実行結果の CSV 集計
- SVG を埋め込んだ Markdown 比較レポート
- 英日両対応のドキュメント

## 🎯 目的
画像から SVG への変換は見た目で語られやすいですが、ベンチマークとして扱うなら入力・条件・出力指標を揃える必要があります。

このリポジトリは、次の比較ループをローカルで再現できるようにすることを目的としています。

1. 入力画像を用意する
2. 必要なら前処理する
3. 固定プリセットで SVG 化する
4. 指標を集計する
5. 比較レポートを生成する

## ✨ 特徴
- `poster` から `detail` まで複数の VTracer プリセットを比較可能
- 画像端からつながる明るい背景だけを抜く前処理
- 実行時間・SVG サイズ・パス数・色数・出力寸法を集計
- ローカル画像や生成物を Git に含めない安全設計
- GitHub Pages 前提の公開ドキュメント

## 🚀 クイックスタート
依存関係を入れます。

```powershell
uv sync
npm install
```

必要なら背景除去を行います。

```powershell
uv run python scripts/remove_edge_background.py --inputs path/to/image1.png path/to/image2.jpg
```

VTracer 実験を回します。

```powershell
uv run python scripts/vtracer_experiments.py --inputs output/preprocessed/image1.nobg.png output/preprocessed/image2.nobg.png
```

Markdown 比較レポートを生成します。

```powershell
uv run python scripts/build_vtracer_report.py
```

ドキュメントサイトをビルドします。

```powershell
npm run docs:build
```

## 🗂 リポジトリ構成
```text
.
|- datasets/                  # 任意の比較用データセット配置先
|- docs/                      # 英日対応の VitePress ドキュメント
|- scripts/                   # 前処理・実験・レポート生成スクリプト
|- output/                    # ローカル生成物（Git 管理外）
|- pyproject.toml             # UV / Python 設定
`- package.json               # Docs ツール設定
```

## 📊 現在の指標
- プリセットごとの実行時間
- 出力 SVG サイズ
- パス数
- fill 色数
- 出力の幅と高さ

まだ完全な評価系ではありませんが、再現可能な比較基盤としては十分に使える状態です。

## 🛣 今後の拡張
- VTracer 以外の runner を追加する
- ロゴ、キャラクター、線画、写真、図表などのカテゴリを整備する
- render-back 比較や視覚差分を足す
- fidelity と editability を分けて評価する
- runner / preset 設定の形式を固める

## 📚 ドキュメント
- 公開サイト: [sunwood-ai-labs.github.io/img2svg-bench](https://sunwood-ai-labs.github.io/img2svg-bench/)
- ローカル入口: [docs/ja/index.md](./docs/ja/index.md)

## 🧭 リポジトリ方針
- ローカル生成物は `output/` に保存し、コミットしません
- 私物画像や非公開画像はデフォルトで公開しません
- 手元の画像を持ち込んでローカルで比較できる構成を維持します

## ⚖️ ライセンス
このリポジトリは [MIT License](./LICENSE) で公開します。
