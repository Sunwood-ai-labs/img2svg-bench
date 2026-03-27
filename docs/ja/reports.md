# レポート

## 生成物

`scripts/build_vtracer_report.py` は次の情報から `output/vtracer/experiments/report.md` を作成します。

- `output/vtracer/experiments/experiment_summary.csv`
- `output/vtracer/experiments/` 配下の SVG 成果物

生成されたレポートを見開くと、プリセット別の結果を短時間で確認できます。

## フォルダ構造

想定例:

```text
output/
  preprocessed/
    image1.nobg.png
  vtracer/
    experiments/
      image1.nobg__default.svg
      image1.nobg__clean.svg
      experiment_summary.csv
      report.md
```

## 推奨ワークフロー

1. プリセット変更後に実験を実行
2. レポートを再生成
3. ベースラインと候補結果を並べて比較
4. 実験フォルダを保管して再現可能性を担保

## 監査可能性

`experiment_summary.csv` と実験スクリプトは Git 管理し、画像や大容量生成物の共有は最小限にします。
