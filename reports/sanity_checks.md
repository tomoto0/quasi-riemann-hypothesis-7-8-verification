# 構造的テスト：既知の障壁と整合性（7/8 論文）

対象：openai/math `adc7f1241b42`、*The Quasi-Riemann Hypothesis: A Zero-Free Half-Plane Re s>7/8*（199頁）と、その Lean 形式化（`lean/ComparatorChallenges/QuasiRiemannHypothesis.lean`、解の側の閉包 2,924 ファイル）。

ここで扱うのは、「詳細に読む前に、既知の理由だけで即座に誤りと判定できるか」という検査である。結果をまとめると、**即座に棄却できる構造的欠陥は見つからなかった**。

## T1. Euler 積テスト（Davenport–Heilbronn 型の反例）— 合格

**問い**：この論証は、関数等式と Dirichlet 級数しか持たない関数にもそのまま適用できてしまうか。そうであれば、σ>1/2 に零点を持つ Davenport–Heilbronn 関数や、σ>1 に零点を持つ Hurwitz・Epstein ゼータ関数が反例になる。

**所見**：論証は次の三点で Euler 積と乗法性を本質的に使っている。
1. 局所 Euler 恒等式（`lem:local-euler`、TeX 4010 行）は、Poisson 行の係数が素数ごとに分解することを示し、$\zeta_F^S(6z)L^S(w,\chi_u)/L^S(x,\eta\bar\chi_u)\cdot\mathcal H_{\eta,u}$ という形を導く。主行 $u=1$ に $1/L(s,\eta)$ が現れるのはこの分解による。
2. 零点検出器は、イデアル Möbius 係数 $\mu(\mathfrak a)\psi(\mathfrak a)$ を持つ「逆多項式」を使う（§8、§17）。
3. 背理法は「$\mathbb Q(\sqrt{-3})$ 上の有限位数 Hecke 指標の族」という、ひねりについて閉じた族の上限 $\beta_*$ に対して行われる。Poisson 行は族の別のメンバーを生み、それらの零点も $\le\beta_*$ である。

Davenport–Heilbronn 関数は Euler 積を持たず、この族にも属さない。したがって論証はこの関数には移植できず、反例にはならない。TeX 中の出現数は、"Euler product/factor" が 22 件、Möbius が 96 件（§17 に 52 件）、multiplicativ が 36 件である。

## T2. 「単一の零点は密度評価では排除できない」障壁 — 合格（設計上回避している）

**問い**：零点密度評価 $N(\sigma,T)\ll T^{A(1-\sigma)}$ は零点の「個数」を抑えるだけで、零点が一つ存在することを否定できない。論文はこの点で誤った推論をしていないか。

**所見**：目標 $L$ 関数の零点は**数えられていない**。零点の存在は、$1/L$ の Mellin 信号 $f_\eta(Z)$ が $Z^{C(\beta_*)}$ の大きさを持つこと（Landau 型）として捉えられ、プローブの直接上界 $Z^{C(\sigma_0)+\omega}$ と矛盾させられる。密度型の行数評価（命題 9.2、19.2）は、Poisson 側に現れる**他の**ひねり行の寄与を抑えるためだけに使われる。これは密度評価の正しい使い方である。

命題 2.1（連続性原理）は全行を検証し、正しいと判断した（`issue_log.csv` の I-001）。

## T3. 一様性（族の上限に対するブートストラップ）— 合格（構造上）

- 命題 2.1 が要求するのは、指数 $\omega,\sigma$ が $\eta$ に依存しないことだけである。暗黙の定数、下限閾値、除外集合、$H_\eta$ は $\eta$ に依存してよい。上限 $\beta_*$ が到達されなくても、$\epsilon_*$ が一様であれば $\Re\rho>\beta_*-\epsilon_*$ となる零点を持つ $\eta$ が存在し、矛盾が生じる。この論理は正しい。
- Part II の余裕は次の通りで、いずれも目標指標に依存しない：$m_{\rm lo}=\Delta$、$m_{\rm hi}=\tfrac{51}{64}\Delta$、$m_{\rm small}=63/800$、$m_w=23/960$、$m_z=13/9600$、主正規化子の $\kappa_P<\tfrac78\min\ell_i$。
- 高さ $T_1=Z^{\tau_\eta}$ の指数 $\tau_\eta$ は $\eta$ ごとに選ばれる。損失 $(1+T_1)^{A}$ は余裕の半分以下に抑えるよう後から選ばれ（`lem:late-height-closure`）、一様性は保たれる。

## T4. 既知の結果との整合性 — 矛盾なし

| 帰結 | 既知の事実との関係 |
|---|---|
| $\zeta$ が $\Re s>7/8$ で零点を持たない | RH の数値検証（高さ約 $3\cdot10^{12}$ まで全零点が臨界線上）と矛盾しない |
| Landau–Siegel 零点が $(7/8,1)$ に存在しない | Siegel の定理（非実効）や Goldfeld–Gross–Zagier と矛盾しない。予想される真実の方向への強化である |
| $n(p)\ll(\log p)^A$（Vinogradov 予想） | 弱 GRH（BIMS）からの既知の帰結であり、論理は正しい（I-004） |
| Hecke（$\mathbb Q(\sqrt{-3})$）と Dirichlet に限定 | 立方テータ関数が Eisenstein 整数に結び付いた手法なので、範囲の限定は自然である。一般の Dedekind ゼータは主張していない |

## T5. 循環論法の有無 — なし

- 節レベルの参照グラフは非巡回である（`dependency_graph.png`）。前方参照 11 件はすべて「後で証明する」という予告である。
- Part II は Part I の結論 $\beta_*\le11/12$ だけを入力とし、Part I は自明な $\beta_*\le1$ と命題 2.1 だけを使う。

## T6. 7/8 という値の出所（障壁分析への入力）

低評価と Mellin 正規化から、境界は**厳密に**次で決まる（TeX 8641 行、式 `old-eq:5.11`）。
$$C(s)=\tfrac{l_x}{2}+s-1+\tfrac h6,\qquad \text{低評価指数}=\tfrac{l_x}{2}+\tfrac b{12}\quad\Longrightarrow\quad \sigma_0=1-\tfrac h6+\tfrac b{12}.$$
- Part I（$h=1/2,\ b=0$）：$\sigma_0=11/12$ ✓
- Part II（$h=13/16,\ b=1/8$）：$\sigma_0=7/8$ ✓

ここで $h=1-l_x+\ell$ は Poisson 周波数の高さ、$1/6$ は $\zeta_F(6z)$ の極 $z=1/6$（周波数 $ua^6$ の六乗部分）に由来する。さらに、7/8 で止まる明示的な仮定が複数ある。
- `lem:bin-contour-accounting` は「$\sigma_0\in[7/8,1)$」を仮定している。
- 局所 Euler 恒等式の第二領域は $x_r\ge7/8$ である。
- `lem:plain` は $\kappa=2\beta_*-1\ge3/4$、すなわち $\beta_*\ge7/8$ を仮定している。

詳しくは `barrier_analysis.md` を参照。

## T7. 形式化の健全性に関する危険要因 — 静的検査では問題なし

- 課題文の忠実性：`riemannZeta_ne_zero_of_seven_eighths_lt_re {s : ℂ} (hs : (7/8:ℝ) < s.re) : riemannZeta s ≠ 0` は **Mathlib の定義だけ**で書かれており、独自定義を含まない。Dirichlet 版も Mathlib の `DirichletCharacter.LFunction` を使う。一方、Hecke 版は課題ファイル内に独自の `LFunction` 定義（約 10KB）を持つので、その忠実性は別途確認が必要である（$\zeta$ と Dirichlet の主張には影響しない）。
- 許可された公理：`propext`, `Quot.sound`, `Classical.choice`（Comparator 設定）。
- 閉包 2,924 ファイル（約 49 万行）を grep した結果、`sorry` / `admit` / `axiom` / `native_decide` / `implemented_by` / `extern` / `unsafe` / `opaque` / `run_cmd` / `elab` / `macro_rules` / `initialize` / `skipKernelTC` / `addDecl` はいずれも **0 件**だった。
- 外部依存は Mathlib（`d13f23b`）、PrimeNumberTheoremAnd（`c39a751`、2MB の互換パッチあり）、RellichKondrachov だけである。
- **残る信頼仮定**：Lean カーネル、依存パッケージとパッチ（上記の公理検査で間接的に確認できる）、Mathlib の `riemannZeta` の定義。カーネルでの実際の検証結果は `lean_build_report.md` に記録する。
