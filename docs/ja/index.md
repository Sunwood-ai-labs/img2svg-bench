---
layout: home

hero:
  name: img2svg-bench
  text: 画像から SVG への変換を再現可能に比較する
  tagline: UV 管理のスクリプト、Markdown レポート、GitHub Pages ドキュメントで、ツール・プリセット・前処理を比較できます。
  image:
    src: /logo.svg
    alt: img2svg-bench logo
  actions:
    - theme: brand
      text: はじめに
      link: /ja/getting-started
    - theme: alt
      text: GitHub
      link: https://github.com/Sunwood-ai-labs/img2svg-bench

features:
  - title: ローカル実行前提
    details: 私物画像を公開せずに、手元で実験と比較を完結できます。
  - title: 再現しやすい比較
    details: CSV 集計と SVG 埋め込みレポートで、結果を何度でも見直せます。
  - title: 拡張しやすい構成
    details: まずは VTracer をベースラインにしつつ、将来的に runner を増やせます。
---

## このプロジェクトが測るもの

`img2svg-bench` は、まず比較の土台として次の指標を集計します。

- プリセットごとの実行時間
- 出力 SVG サイズ
- パス数
- fill 色数
- 出力寸法

今後は、ここに fidelity や render-back 指標を重ねていく想定です。

現在の VTracer ベースラインから公開している SVG サンプルは [レポート](/ja/reports) ページで確認できます。
