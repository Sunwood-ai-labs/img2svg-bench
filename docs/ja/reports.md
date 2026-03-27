# レポート

## 生成物

`scripts/build_vtracer_report.py` は次の情報から `output/vtracer/experiments/report.md` を作成します。

- `output/vtracer/experiments/experiment_summary.csv`
- `output/vtracer/experiments/` 配下の SVG 成果物

生成されたレポートを見開くと、プリセット別の結果を短時間で確認できます。

## 公開サンプル結果

公開 README / docs でも実際の生成結果が見えるように、代表的な SVG を `docs/public/results/` に限定して同梱しています。

| kiyoka_1 / clean | kiyoka_1 / poster |
| --- | --- |
| ![kiyoka_1 clean](/results/kiyoka-1-clean.svg) | ![kiyoka_1 poster](/results/kiyoka-1-poster.svg) |
| `129.7 KB` / `93 paths` / `1.30 s` | `61.1 KB` / `36 paths` / `0.44 s` |

| kiyoka_2 / clean | kiyoka_2 / poster |
| --- | --- |
| ![kiyoka_2 clean](/results/kiyoka-2-clean.svg) | ![kiyoka_2 poster](/results/kiyoka-2-poster.svg) |
| `210.0 KB` / `123 paths` / `0.84 s` | `108.2 KB` / `46 paths` / `0.51 s` |

ここに載せるのは軽量な代表例だけに留め、全プリセットの比較はローカル生成される `report.md` を参照する前提です。

## 追加で公開している派生結果

- [kiyoka_1 detail](/results/kiyoka-1-detail.svg): `detail / 1.63 MB / 3268 paths / 11.29 s`
- [kiyoka_1 binary_ink](/results/kiyoka-1-binary-ink.svg): `binary_ink / 219.8 KB / 8 paths / 0.20 s`
- [kiyoka_2 detail](/results/kiyoka-2-detail.svg): `detail / 2.07 MB / 3884 paths / 13.65 s`
- [kiyoka_2 binary_ink](/results/kiyoka-2-binary-ink.svg): `binary_ink / 40.2 KB / 9 paths / 0.18 s`

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
