# Lean カーネルでの検証報告

## 結果
**ビルドに成功した。主定理が依存する公理は標準の三つだけである。**

```
'OAI.riemannZeta_ne_zero_of_seven_eighths_lt_re' depends on axioms: [propext, Classical.choice, Quot.sound]
'OAI.DirichletCharacter.LFunction_ne_zero_of_seven_eighths_lt_re' depends on axioms: [propext, Classical.choice, Quot.sound]
'QRHCheck.zeta_challenge' depends on axioms: [propext, Classical.choice, Quot.sound]
```

`QRHCheck.zeta_challenge` は、Comparator 課題文 `theorem riemannZeta_ne_zero_of_seven_eighths_lt_re {s : ℂ} (hs : (7 / 8 : ℝ) < s.re) : riemannZeta s ≠ 0` を**一字一句そのまま書き直し**、解の定理で証明したものである。これにより、解の定理の型が課題文と一致していることを確認した。Dirichlet 版（`QRHCheck.dirichlet_challenge`）も同様に型が一致した。

## 環境
| 項目 | 値 |
|---|---|
| リポジトリ | openai/math `adc7f1241b42e322a6451854ab7e4b4c146bf78a` |
| ツールチェーン | Lean 4.34.1（`5045d0056413`、darwin_aarch64 公式リリース） |
| Mathlib | `d13f23b723b8a846827a245b89c10fc7d3f11612`（公式キャッシュ cache.mathlib.org の .olean を使用） |
| PrimeNumberTheoremAnd | `c39a751132c8`＋`PrimeNumberTheoremAnd-lean4341.patch`（ローカルでビルド） |
| rellich-kondrachov | `70f85d4c1bf9`＋`rellich-kondrachov-lean4341.patch`（ローカルでビルド） |
| 対象 | `lake build OAI.NumberTheory.DirichletL.Nonvanishing` |
| ジョブ数 | 7,061（うち OAI モジュール 2,924 をローカルでエラボレートし、カーネルで検査） |
| 所要時間 | 252 分（2026-10-07 13:04–17:16 UTC、8 コア・16GB） |
| エラー | 0 件 |
| 警告 | 23 件。すべて「依存パッケージにローカル変更あり」（互換パッチの適用による）。`sorry` を含む宣言の警告は 0 件 |

## 静的検査（ビルド前）
- OAI 閉包 2,924 ファイル：`sorry`/`admit`/`axiom`/`native_decide`/`implemented_by`/`extern`/`unsafe`/`opaque`/`run_cmd`/`elab`/`macro_rules`/`initialize`/`skipKernelTC`/`addDecl` はいずれも 0 件。
- PrimeNumberTheoremAnd：`Tactic/AdditiveCombination.lean` にテスト用の `axiom qc : ℚ` と `axiom hqc : qc = 2*qc` があり、`Tactic/Simprocs.lean` に `unsafe def`（メタレベル）がある。前者を主定理が使っていないことは `#print axioms` で確認した。後者は証明項を生成するだけなので、カーネルの健全性には影響しない。

## 追加のカーネル再生（leanchecker）
- 最終 2 モジュール（`OAI.NumberTheory.DirichletL.Nonvanishing`、`...Detector.FinalAssemblyUnconditional`）：`lake env leanchecker` による再生が**エラーなしで完了**した（9 分）。
- 全 2,924 モジュールの一括再生：約 60 分で**時間切れのため打ち切った**（それまでエラー出力なし）。
- 通常のビルドでも、各宣言は環境に追加される時点で Lean カーネルが型検査している。閉包にはカーネル検査を迂回する設定（`debug.skipKernelTC`）もメタプログラミングによる宣言追加もないので、再生は追加の多重防御にあたる。

## 残る信頼仮定
1. Lean 4 カーネル（および leanchecker の再生）。
2. Mathlib の `riemannZeta` と `DirichletCharacter.LFunction` の定義が、標準的な数学的対象を表していること。
3. 公式キャッシュから取得した Mathlib の .olean。Mathlib の宣言はローカルでは再エラボレートしていない。
4. 解析の対象は、形式化された命題（ζ と Dirichlet）だけである。論文 199 頁の各命題が Lean のどの宣言に対応するかの対応表は提供されていない。したがって、Lean が検証したのは「主定理が真であること」であり、「論文の文章による証明が逐語的に正しいこと」ではない。

## 再現手順
```sh
# openai/math の lean/ ディレクトリで実行（作業環境の制約で一部のドットディレクトリを作れなかったため、依存パッケージは sparse-checkout で取得した）
lake update                      # 依存パッケージの取得と互換パッチの適用
lake exe cache get               # Mathlib の .olean
lake build OAI.NumberTheory.DirichletL.Nonvanishing
lake env lean QRHCheck.lean      # 課題文の一致確認と #print axioms
```
