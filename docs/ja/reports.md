# レポート

## 生成物

`scripts/build_vtracer_report.py` は次の情報から `output/vtracer/experiments/report.md` を作成します。

- `output/vtracer/experiments/experiment_summary.csv`
- `output/vtracer/experiments/` 配下の SVG 成果物

生成されたレポートを見開くと、プリセット別の結果を短時間で確認できます。

## 公開サンプルギャラリー

公開 README / docs でも実際の生成結果が見えるように、代表的な SVG を `docs/public/results/` に限定して同梱しています。

| Sample A / clean | Sample A / poster |
| --- | --- |
| ![Sample A clean](/results/sample-a-clean.svg) | ![Sample A poster](/results/sample-a-poster.svg) |
| `129.7 KB` / `93 paths` / `1.30 s` | `61.1 KB` / `36 paths` / `0.44 s` |

| Sample B / clean | Sample B / poster |
| --- | --- |
| ![Sample B clean](/results/sample-b-clean.svg) | ![Sample B poster](/results/sample-b-poster.svg) |
| `210.0 KB` / `123 paths` / `0.84 s` | `108.2 KB` / `46 paths` / `0.51 s` |

ここに載せるのは軽量な代表例だけに留め、全プリセットの比較はローカル生成される `report.md` を参照する前提です。

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
公開用の SVG も `docs/public/results/` に代表例だけを絞って保持します。
