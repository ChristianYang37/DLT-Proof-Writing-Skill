# Reasoning as implicit-loss optimization → 一个解码 iff、三条推论与一座损失-间隔桥（Lean 机器验证版）+ 速率/概率的引用-经典第二层

本文档面向**本科数学背景**的读者，一步步讲清这篇（很短的）结果在问什么、设定是什么、**五个**结论怎么读、怎么证、以及它**诚实地**说了/没说什么。**机器验证层**（主 iff + 三条推论 + 损失-间隔桥，共 **5** 个定理）已在 **Lean 4 + Mathlib** 中通过 kernel 检查（无 `sorry`、无自定义公理；`#print axioms` 闭包都 $=\{$`propext`, `Classical.choice`, `Quot.sound`$\}$）。**此外第二层（§10 / LaTeX §4 B2）回答原始的「收敛速率、成败概率」两问，但那一层是引用经典凸优化、明确标注「非机器验证」，与验证层严格分离。**

**前置知识**：线性代数（内积、范数）、多元微积分（梯度）、一点点约束优化（Lagrange 乘子 / 一阶条件）。**不需要概率论**——本结果是**纯确定性**的。

**一句话**：

> 假设「reasoning」是在优化某个**隐式损失** $L$（哪怕优化得并不高效），那么 LLM 是否输出某个 token，由一个**确定性的充要条件**刻画：在 LayerNorm 球面的约束**驻点**处，模型生成答案 token $a^\star$ **当且仅当**「梯度（按乘子符号定向后）与答案行 $W_{a^\star}$ 的对齐，严格强于与任何竞争者行的对齐」。本版给出**一个主 iff + 三条推论 + 一座损失-间隔桥**（下降方向读法 / 失败刻画 / 交叉熵特化 / $L<\log2\Rightarrow$ 解码正确），全部机器验证。**并在第二层回答原始的两问**：收敛速率（GD-on-凸 $O(1/t)$ 损失、$O(1/\Delta)$ 步即解码正确）与成功概率（$\mathrm{pass}@T\to\Pr_Q[\text{solvable}]$）——但这一层是**引用经典凸优化、非机器验证**（与验证层分离）。

---

## §1 问题与设定

把一段 reasoning 看成在隐藏状态空间 $\mathbb R^d$ 上对某个隐式损失 $L$ 做优化。两个观察：

1. **「哪怕低效」**：我们**不**假设优化高效——不假设收敛速率、不假设到达全局最优。低效优化唯一能保证的，是轨迹最终**停在一个驻点**（一阶条件成立的点）。
2. **解码本身也是优化**：下一个 token 由 $\arg\max_a \langle W_a, x\rangle$（贪心解码）给出，这是对 logit 的一个 $\arg\max$。

于是「reasoning 后的 token 输出」= 两个优化的复合。我们问：**在最一般的假设下，输出哪个 token 由什么充要条件决定？**

**数学设定**：

- **状态空间** $E$（实内积空间，complete；$\mathbb R^d=$ EuclideanSpace 是模型），内积 $\langle\cdot,\cdot\rangle$。
- **词表** $\mathcal V$（有限，$\ge 2$ 个 token）；**unembedding** $W:\mathcal V\to E$，token $a$ 的行是 $W_a$（这就是 LLM 真实的 linear head）。
- **LayerNorm 球面** $\mathcal S_r=\{x:\|x\|=r\}$，$r>0$。
- **解码器**（单 token，$n=1$，所以贪心 $\arg\max$ **就是**真解码器）：
  $$\mathrm{Gen}(a,x)\quad:\Longleftrightarrow\quad \forall b\neq a,\ \langle W_a, x\rangle > \langle W_b, x\rangle.$$
- **隐式损失** $L:E\to\mathbb R$，可微（这是 **setting 注记**，不是 load-bearing 假设——证明从不对 $L$ 求导）。
- **约束驻点**（reasoning「停下来」的形式化）：球面约束下的一阶（Lagrange）条件——梯度与球面法向平行：
  $$\nabla L(x^\star)=\mu\, x^\star.$$
  等价地：Riemannian 梯度（$\nabla L$ 到切空间的投影）为零。**这是我们对优化的唯一假设**——没有凸性、没有全局最优、没有速率。

---

## §2 主定理：decode ⟺ gradient separation

**定理**（已 Lean 验证，`Decode.decode_iff_gradient_separation`）。设 $\|x^\star\|=r$，$\nabla L(x^\star)=\mu\,x^\star$，$\mu\neq 0$。则对答案 token $a^\star$：

$$\boxed{\ \mathrm{Gen}(a^\star,x^\star)\quad\Longleftrightarrow\quad \forall b\neq a^\star,\ \ \mu\,\big\langle W_{a^\star}-W_b,\ \nabla L(x^\star)\big\rangle\ >\ 0.\ }$$

**怎么读 / 怎么证**（证明就是这几行内积代数，所以它能干净地在 Lean 里过）：

1. 由驻点性且 $\mu\neq 0$，把位置用梯度表示：$x^\star=\mu^{-1}\,\nabla L(x^\star)$。
2. 解码锥条件 $\langle W_{a^\star},x^\star\rangle>\langle W_b,x^\star\rangle$ 等价于 $\langle W_{a^\star}-W_b,\ x^\star\rangle>0$（内积线性）。
3. 代入第 1 步：$\langle W_{a^\star}-W_b,x^\star\rangle=\mu^{-1}\langle W_{a^\star}-W_b,\nabla L(x^\star)\rangle$。
4. **符号等价引理**（`Decode.sign_equiv`）：因为 $\mu^2>0$，对任意实数 $c$ 有 $\mu^{-1}c>0\iff \mu c>0$。于是上式 $>0$ 等价于 $\mu\,\langle W_{a^\star}-W_b,\nabla L(x^\star)\rangle>0$。
5. 对所有竞争者 $b\neq a^\star$ 取 $\forall$，即得 iff。$\qquad\blacksquare$

> 注意符号是 **$>0$**（不是 $<0$）。这一点恰恰是 Lean 验证的价值：手写时极易把符号写反，而 kernel 不会放过。

---

## §3 三条推论

### §3.1 推论一：下降方向分离（$\mu<0$，约束最小情形）

**推论**（`Decode.decode_iff_descent_separation_of_neg`）。在主定理假设下若 $\mu<0$（约束**最小**的典型情形），则

$$\boxed{\ \mathrm{Gen}(a^\star,x^\star)\quad\Longleftrightarrow\quad \forall b\neq a^\star,\ \ \big\langle W_{a^\star}-W_b,\ -\nabla L(x^\star)\big\rangle\ >\ 0.\ }$$

即：**生成答案 $a^\star$ 当且仅当下降方向 $-\nabla L(x^\star)$ 与答案行 $W_{a^\star}$ 的对齐，严格强于与每个竞争者行 $W_b$ 的对齐。** 这是最贴近「reasoning 直觉」的读法——「往降损失的方向走，恰好把答案行顶到最高」。（证明：$\mu<0$ 时 $\mu c>0\iff c<0$，而 $\langle v,-\nabla L\rangle=-\langle v,\nabla L\rangle>0\iff\langle v,\nabla L\rangle<0$，两者同条件。）

### §3.2 推论二：失败刻画（主 iff 的逆否 / De Morgan 对偶）

**推论**（`Decode.decode_fails_iff_some_competitor`）。在主定理假设下，

$$\boxed{\ \neg\,\mathrm{Gen}(a^\star,x^\star)\quad\Longleftrightarrow\quad \exists\, b\neq a^\star,\ \ \mu\,\big\langle W_{a^\star}-W_b,\ \nabla L(x^\star)\big\rangle\ \le\ 0.\ }$$

即：**解码失败当且仅当存在某个竞争者 $b$，它在 $\mu$-定向对齐上「打平或反超」答案行。** 这是把主 iff 取反：$\neg\forall$ 变 $\exists$，严格不等式 $>0$ 的否定恰是非严格 $\le 0$。证明就一步 `push_neg`。

> **为什么 $\le 0$（不是 $<0$）**：$>0$ 的逻辑否定是 $\le 0$（含「打平」$=0$ 的边界情形：竞争者与答案行打平，贪心 $\arg\max$ 不再严格选出 $a^\star$）。Lean 给出的正是这个**精确**边界。

**洞察（失败刻画为何有用）**：因为是 iff，它**紧**——失败不仅被检测，而且那个见证 $b$ **就是**反超的 token，criterion 直接「点名」是谁、为什么赢。（见 LaTeX `rem:fail-tight`。）

### §3.3 推论三：交叉熵特化（softmax 残差分离）

把梯度特化成**单 token 交叉熵**的字面梯度 $\nabla L=W^\top(p-e_{a^\star})$，写成对词表求和的形式

$$\nabla L(x^\star)=\sum_{c}\big(p_c-\mathbf 1[c=a^\star]\big)\,W_c,$$

其中 $p$ 是 softmax 概率向量，$e_{a^\star}$ 是 one-hot 目标。**推论**（`Decode.decode_iff_softmax_residual`，额外假设上式 `hgrad`）：

$$\boxed{\ \mathrm{Gen}(a^\star,x^\star)\ \Longleftrightarrow\ \forall b\neq a^\star,\ \ \mu\sum_{c}\big(p_c-\mathbf 1[c=a^\star]\big)\big(\langle W_{a^\star},W_c\rangle-\langle W_b,W_c\rangle\big)>0.\ }$$

**怎么读 / 怎么证**：固定 $b$，把内积代入梯度并对词表展开，得**恒等式**
$$\langle W_{a^\star}-W_b,\ \nabla L\rangle=\sum_c\big(p_c-\mathbf 1[c=a^\star]\big)\big(\langle W_{a^\star},W_c\rangle-\langle W_b,W_c\rangle\big)$$
（内积对和的分配 `inner_sum`、标量提出 `real_inner_smul_right`、行差展开 `inner_sub_left`，逐项 `Finset.sum_congr`）。再把它代进主 iff 的每个竞争者条件即可。**注意：我们不对 log-sum-exp 求导**——交叉熵的残差梯度形式是**假设** `hgrad`，定理只把对齐泛函按它改写。

**洞察（交叉熵读法）**：分离分数是一个 **Gram 矩阵加权的残差**——$\langle W_{a^\star},W_c\rangle-\langle W_b,W_c\rangle$ 比较「答案行 vs 竞争者行各自与 $W_c$ 的对齐」，权重是 softmax 残差 $p_c-\mathbf 1[c=a^\star]$（「预测减目标」）。解码成功当且仅当这个加权比较对每个竞争者都 $\mu$-定向为正，即**交叉熵残差在 unembedding 几何里把答案行顶到前面**。（见 LaTeX `rem:ce-reading`。）

---

## §4 诚实标注（这正是这版的卖点）

- **比所述更一般**：Lean linter 显示主定理证明**根本没用到** $\|x^\star\|=r$ 和 $r>0$——只用了 $\mu\neq 0$ 和驻点性 $\nabla L(x^\star)=\mu x^\star$。所以这个刻画对**任何**满足「梯度平行于位置、乘子非零」的点都成立，在球面上或不在球面上都行。**三条推论继承同样的假设**，故同样只有 $\mu\neq0$+驻点性 load-bearing。我们保留球面假设只是为了对齐 LayerNorm 几何，并在 `rem:generalization` 里如实标注其未被使用（这是**加强**，不是缺陷）。
- **可微性是 setting 注记，不是 load-bearing 假设**：证明从不对 $L$ 求导，只用 $\nabla L(x^\star)$ 这个**值**（通过驻点假设）。所以把 `Differentiable L` 放进假设属于「假设膨胀」，按 Occam 不放。
- **交叉熵特化的额外假设**：推论三新增 (i) softmax 向量 $p$、(ii) 梯度残差形式 `hgrad`、(iii) 一个良性的 `[DecidableEq V]`（仅为写出 one-hot 指示函数 $\mathbf 1[c=a^\star]$，每个有限词表都满足，不构成数学限制）。`hgrad` 是这条推论的**定义性特化**（它**就是**交叉熵假设），不是对无条件命题的偷偷削弱；并且 `hgrad` 与 $\nabla L=\mu x^\star$ **可同时满足**（见 `Proof/Vacuity.lean` 第 (4) 见证：$V=$Bool、$p=(3,0)$ 时残差和 $=2\cdot 1=$ 某 $x^2$ 损失的梯度），故推论三**非空真**。
- **$\mu$ 的符号**：一般情形条件带 $\mathrm{sign}(\mu)$；$\mu<0$ 是「损失把答案行拉过来」这类情形的典型，给出干净的下降方向读法。$\mu$ 的符号不由驻点性单独决定，所以主定理诚实地保留 $\mu$。
- **这是干净的「刻画」，不是深定理**：核心是几行内积代数——这恰恰是它能在今天的 Mathlib 里**端到端验证**的原因。价值在于忠实的机器验证 + 可解释的读法，而非证明难度。

> **重要：本确定性版本不含先前概率版本的结果。** 早先的版本（archived 在 `/Users/christian/eval08-asopt-prev-archive`）包含 **test-time scaling / 相变（phase-transition）/「点火」** 等结论；那些依赖一整套概率机器（对齐率、各向同性噪声假设、Sudakov minoration、Borell–TIS 等）来推「收敛/越阈」，既牵强又**无法机器验证**。本版**有意丢弃**那套机器，只保留能被 Lean 端到端验证的确定性 iff 刻画。两者互补：本版讲「停在驻点后解码谁」，概率版试图讲「能不能/多快到达」——但只有前者今天能被证实。

---

## §5 洞察（insight）：这四个结论到底在说什么

1. **解码读的是「梯度」，不是「状态」。** 朴素地想，输出取决于轨迹停在哪（$x^\star$）。但驻点性把 $x^\star$ 与 $\nabla L(x^\star)$ 锁成平行（$x^\star=\mu^{-1}\nabla L$），于是输出**等价地由损失在停点处的梯度方向决定**。优化器的一阶信息 = 解码器的输入——这是「优化」与「解码」之间一座精确的桥。

2. **只有方向和乘子符号要紧，大小全抵消。** 条件对 $\nabla L$ 尺度不变（$L\mapsto cL,\ c>0$ 不改变输出）。决定输出的只是：(a) $\nabla L(x^\star)$ 相对行差 $W_{a^\star}-W_b$ 的**方向**；(b) $\mathrm{sign}(\mu)$。**整个解码结果坍缩成 $|\mathcal V|-1$ 个内积的符号模式**——连续优化里冒出离散结构。失败刻画（推论二）把这点说满：失败 $\iff$ 这 $|\mathcal V|-1$ 个符号里**至少有一个**非正。

3. **「答案」就是与下降方向最对齐的那一行。**（$\mu<0$，推论一）把「模型输出什么」重述为「下降方向 $-\nabla L$ 最指向哪一行」。损失景观与输出 token 是**同一个比较**。

4. **效率与输出无关——「停在哪」与「怎么到的」解耦。** 不需要凸、不需要全局最优、不需要速率，只要停在驻点。所以「输出哪个 token」是**停点 + 解码几何**的性质，与（可能很乱、很低效的）动力学**无关**。「哪怕优化低效」被定理照单全收：效率根本不进入这些 iff。

5. **交叉熵把抽象梯度落地成可计算的 Gram 残差。**（推论三）抽象 $\nabla L$ 一旦特化成 $W^\top(p-e_{a^\star})$，分离条件就变成**只含 unembedding 内积 $\langle W_a,W_c\rangle$ 与 softmax 残差 $p_c-\mathbf 1[c=a^\star]$** 的式子——全是「白盒可算量」。这把主定理从「关于某个抽象 $L$」变成「关于真实交叉熵训练的 LLM」。

6. **它其实与球面无关。**（linter 揭示的）证明没用上 $\|x^\star\|=r$——只要 $\nabla L\parallel x^\star$ 且 $\mu\neq0$。现象的本质是「梯度对齐」，而非某个特定流形。这既是普适性，也是局限——结果并没真正「用到」LayerNorm 几何本身。

---

## §6 证明出来有什么用

- **机理可解释性（白盒判据）。** 给定训练好的模型、收敛后的隐藏态、unembedding，可**直接计算** $\mu\langle W_{a^\star}-W_b,\nabla L(x^\star)\rangle$ 对所有 $b$ 的符号，从而**预测**会不会解码正确。又因为是 **iff**，它是紧的——推论二**精确指出**解码失败 $\iff$ 哪个竞争者反超。交叉熵特化（推论三）更进一步：把这套判据写成**只含 $\langle W_a,W_c\rangle$ 和 $p$ 的可算式**，对真实交叉熵模型可落地。

- **把「优化直觉」钉成可检验命题。**「reasoning 在朝答案降损失」常被当口号；这组 iff 给出它**何时成立**的精确条件，把口号变成可证伪的陈述；失败刻画给出它**何时不成立**的精确边界。

- **一块可信的地基 / 可复用引理。** 因为是 Lean 机器验证的，可以放心当作更大论证的一环：例如与某个「收敛到好驻点」的结果拼接得到端到端保证。交叉熵特化已经示范了「对具体损失特化」这种复用。

- **一个方法论模板。** 它示范「**最小诚实假设 + 机器验证的 iff（及其逆否、其特化）**」这种关于 LLM 的理论主张的写法，并证明：只要把范围收到确定性、有限维、内积代数，这类主张**今天就能在 Lean 里形式化**。

---

## §7 为什么这样证明（方法论）

- **为什么走确定性 + Lean、丢掉概率机器。** 之前的相变/点火版堆叠概率假设去拿「收敛」，结果既「牵强」又**无法机器验证**。退一步问最小的问题（「停在驻点后解码谁」），换来：(a) 基本只需一条诚实假设；(b) 一个**精确 iff**（没有可糊弄的常数/松弛）；(c) **可被 kernel 检查**。这正是 Lean-first skill 强制的 truth-seeking：用「可证的少」换掉「动听但不可验的多」。

- **为什么把驻点性写成假设、而不去推导收敛。** 把「reasoning 停下来」编码成一阶条件 $\nabla L=\mu x$（而非证明收敛），既让 **Mathlib 依赖很轻**（不需要流形/Lagrange 理论，所以它真能过），又**诚实划清边界**：我们刻画驻点，不声称动力学到达它。「低效优化」恰被如此捕捉。

- **为什么用「符号等价」这个小核。** 整个主证明的核心是引理 $\mu^{-1}c>0\iff\mu c>0$（差一个 $\mu^2>0$）。它把「乘子符号唯一要紧之处」隔离出来，使整件事变成「清分母」，证明因此只有约十行、且能被验证。三条推论都**复用**主 iff：逆否（一步 `push_neg`）、$\mu<0$ 重写（`inner_neg_right`）、交叉熵改写（`inner_sum`/`real_inner_smul_right`/`inner_sub_left`）——每条都只是对主 iff 的**忠实再加工**，不引入新难度，也因此都过了 kernel。

- **为什么把交叉熵梯度当假设、不去微分 log-sum-exp。** 微分 softmax 在 Mathlib 里要拖入大量分析机器（可微性、链式法则、log-sum-exp 的导数），风险高且偏题。我们把**梯度的最终形式** $W^\top(p-e_{a^\star})$ 当假设，定理只做内积代数的改写——这让推论三**轻、诚实、可验证**，并明确标注「softmax 梯度本身不在本证明范围内」。

- **为什么要 iff，而不是单向界。** iff 是**完整刻画**（必要且充分），无概率、无常数。对一个关于确定性解码器的白盒主张，iff 才是「对」的对象；它的逆否（推论二）自动给出紧的失败刻画。

---

## §8 Lean 对应与验证状态（gate）

- **四个定理**：`Decode.decode_iff_gradient_separation`（主 iff）、`Decode.decode_iff_descent_separation_of_neg`（下降方向，$\mu<0$）、`Decode.decode_fails_iff_some_competitor`（失败刻画）、`Decode.decode_iff_softmax_residual`（交叉熵特化）；外加辅助引理 `Decode.sign_equiv`。
- `#print axioms` 闭包 $=\{$`propext`, `Classical.choice`, `Quot.sound`$\}$（Mathlib 标准基底），**四个定理全部**无 `sorry`、无自定义 `axiom`、无 `native_decide`。
- **Gate 全绿**：
  - `lean-wrapper.py --mode build --axioms <四个>` → `integrity_ok: true`，四个 PASS；
  - `lean_lint.py --style --lock statement.lock` → 0 errors（签名锁 SL1 对**全部四个**签名成立——两个旧的字节不变、两个新的已加入）；
  - `drift_check.py` → 0 errors，**13 Lean ↔ 13 LaTeX** 步骤双射（9 条 D4 提示为 prose 交叉引用，非阻塞）；
  - `lint.py` → 0 errors；`latexmk-wrapper.py` → `compile_ok: true`（1 个 20.3pt overfull，远低于 50pt 阈值）。
- **文件**：Lean 源在 `.lean-proof/Proof/{Settings,Statements,Proofs/DecodeIff}.lean`（+ `Vacuity.lean` 非平凡性见证，含交叉熵 `hgrad` 可满足性）；人读 LaTeX 在 `sections/01-preliminaries.tex`（设定/定义/交叉熵 setup）+ `sections/02-theorem-decode-iff.tex`（符号引理 + 主定理 + 一般性注记）+ `sections/03-corollaries.tex`（三条推论，每个 statement+proof，每步带 `% @lx-from:` 指回所验证的 Lean 声明）；编译产物 `.output/main.pdf`。

> **注（2026-06-03）**：本 §8 是「主 iff + 三条推论」**核心层**的 gate 快照（4 定理、`drift_check` 13↔13、5 页）。加入 §10.1 的**损失-间隔桥**（第 5 个验证定理 `Decode.loss_below_log2_decodes`，源 `Proof/Proofs/Bridge.lean`、LaTeX `sections/04-bridge-and-dynamics.tex`）后全部 gate 仍**全绿**：`integrity_ok`（5/5 PASS）、`lean_lint` 0/0（statement.lock 含 5 键）、`drift_check` **18↔18**、`lint` 0/0、`latexmk` `compile_ok`（**7 页**）。详见 §10。

---

## §9 附录：核心对象速查

| 对象 | 记号 | 含义 |
|---|---|---|
| 状态空间 | $E$ | 实内积空间（complete；$\mathbb R^d$ 是模型） |
| unembedding | $W_a$ | token $a$ 的行（真实 linear head） |
| 球面 | $\mathcal S_r=\{\|x\|=r\}$ | LayerNorm 约束集（证明实际未用） |
| 解码器 | $\mathrm{Gen}(a,x)$ | $\forall b\neq a,\ \langle W_a,x\rangle>\langle W_b,x\rangle$（贪心 = 真解码） |
| 隐式损失 | $L$，$\nabla L$ | 可微（setting 注记） |
| 驻点性 | $\nabla L(x^\star)=\mu x^\star$ | 球面约束一阶条件（唯一优化假设） |
| 乘子 | $\mu\neq 0$ | $\mathrm{sign}(\mu)$ 携带朝向；$\mu<0$ = 约束最小 |
| softmax 向量 | $p$，$p_c$ | token $c$ 的预测概率 |
| one-hot 目标 | $\mathbf 1[c=a^\star]$ | 答案的 one-hot $e_{a^\star}$ 的分量 |
| 交叉熵梯度 | $\sum_c(p_c-\mathbf 1[c=a^\star])W_c$ | $W^\top(p-e_{a^\star})$（推论三的假设 `hgrad`） |

**四个 boxed 结论**（与 Lean 验证的符号逐字一致）：

1. **主 iff**：$\mathrm{Gen}(a^\star,x^\star)\iff \forall b\neq a^\star,\ \mu\langle W_{a^\star}-W_b,\nabla L(x^\star)\rangle>0$。
2. **下降形（$\mu<0$）**：$\mathrm{Gen}(a^\star,x^\star)\iff \forall b\neq a^\star,\ \langle W_{a^\star}-W_b,-\nabla L(x^\star)\rangle>0$。
3. **失败刻画**：$\neg\,\mathrm{Gen}(a^\star,x^\star)\iff \exists b\neq a^\star,\ \mu\langle W_{a^\star}-W_b,\nabla L(x^\star)\rangle\le 0$。
4. **交叉熵特化**：$\mathrm{Gen}(a^\star,x^\star)\iff \forall b\neq a^\star,\ \mu\sum_c(p_c-\mathbf 1[c=a^\star])(\langle W_{a^\star},W_c\rangle-\langle W_b,W_c\rangle)>0$。

---

**版本信息**：Lean-verified 确定性版 + 引用-经典第二层（2026-06-03）。几何：LayerNorm 球面（但证明只需 $\mu\neq0$+驻点）；答案：单 token（$D_{\text{true}}=$ 贪心 argmax）；假设：可微 $L$ + 球面约束驻点（凸性/最优/速率均不需要）。**机器验证层**：**1 主 iff + 3 推论 + 1 损失-间隔桥 + 1 辅助引理（共 5 个验证定理）**，全部 Lean 4 + Mathlib（`integrity_ok`，`drift_check` 18↔18，PDF 7 页）。**第二层（§10.2 / LaTeX §4 B2）回答原始的「速率、成败概率」两问**，以**引用-经典**形式：GD-on-凸 $O(1/t)$、$t^\star=O(1/\Delta)$（$\Delta=\log2-L^\star$）、$\mathrm{pass}@T\to\Pr_Q[\text{solvable}]$（引用 Bubeck 2015 Thm 3.3，**非机器验证**，与验证层严格分离、无 `@lx-from`、非 🔵）。先前概率版的 test-time-scaling / 相变（依赖被丢弃的概率机器）archived 在 `/Users/christian/eval08-asopt-prev-archive`。如需深入：`.lean-proof/Proof/Proofs/{DecodeIff,Bridge}.lean`（每步带 `@lx`）或 `sections/`。

---

## §10 第二层（2026-06-03 增补）：损失-间隔桥 + 动力学（验证 / 引用 分离）

在四个 iff 之上新增**一个 Lean 机器验证定理**和**一节 LaTeX（§4）**，后者明确拆成「已验证」与「引用-未验证」两部分。

### §10.1 验证部分（🔵）：损失-间隔桥 `Decode.loss_below_log2_decodes`

引入单 token 交叉熵损失 $L(x)=\log\big(\sum_c \exp\langle W_c,x\rangle\big)-\langle W_{a^\star},x\rangle$（即 $-\log p_{a^\star}(x)$，`Settings.lean` 中 `def lossCE`）。**定理**（`Bridge.lean`，已机器验证）：

$$\boxed{\ L(x)<\log 2\ \Longrightarrow\ \mathrm{Gen}(a^\star,x).\ }$$

即「单 token 交叉熵跌破 $\log 2$（$\iff p_{a^\star}>1/2$）⟹ 贪心解码器输出 $a^\star$」。证明是有限非空和上的纯 log/exp 代数（`Real.exp_pos`/`Finset.sum_pos`/`Real.log_mul`/`Real.log_exp`/`Real.log_lt_log_iff`/`Finset.add_sum_erase`/`Finset.single_le_sum`/`Real.exp_lt_exp`），**从不对 $L$ 求导**，也**不依赖任何 iff 定理**（无循环）。阈值 $\log 2$ 精确：质量过半即压过所有竞争者之和。`#print axioms` 闭包 $=\{$`propext`,`Classical.choice`,`Quot.sound`$\}$。这座桥把「损失**值**」连到「解码」——是连接已验证 iff（驻点解码谁）与收敛速率叙事（损失掉多快）的纽带。`Proof/Vacuity.lean` (5a/5b) 见证假设可满足且非平凡。

### §10.2 引用部分（**经典 / 引用 / 未机器验证**，非 🔵，无 `@lx-from`）

§4 B2 以「reasoning = 在凸损失 $L$ 上做梯度下降」为模型读出后续结论，**每条均引用经典凸优化或标注为经典叙述，没有一条机器验证**：

- **命题 `prop:gd_rate`**（**引用** `\cite[Theorem 3.3]{bubeck2015}`，无本地证明）：$\smooth$-光滑凸损失上 GD（步长 $1/\smooth$）满足 $L(x_t)-L^\star\le 2\smooth\|x_1-x^\star\|^2/(t-1)=O(1/t)$，且损失单调不增。
- **推论 `cor:decode_time`**（**引用-未验证**，带短证明但无 `@lx-from`，见 `rem:cor-not-verified`）：记 $\Delta:=\log 2-L^\star>0$，则 $t>t^\star:=1+2\smooth\|x_1-x^\star\|^2/\Delta=O(1/\Delta)$ 时 $L(x_t)<\log 2$，由 §10.1 的桥得 $\mathrm{Gen}(a^\star,x_t)$——即 **$O(1/\Delta)$ 步内解码正确（多项式），且保持正确（单调下降）**。
- **注记** `rem:structural`（结构性成败：每问题确定 0/1；可成功 $\iff$ $a^\star$ 在最优 $x^\star$ 处是 argmax，**恰是主 iff 在 $x^\star$ 的取值**）、`rem:probability`（问题分布上的成功率 $\mathrm{pass}@T=\Pr_Q[\Delta(Q)>0\wedge t^\star(Q)\le T]\to\Pr_Q[\text{solvable}]$，随机梯度下平滑为 $\Phi(\cdot)$ 形）、`rem:convex`（$L$ 凸：log-sum-exp 减线性）。

引用诚实性（R13）：`refs.bib`（key `bubeck2015`）+ digest `.proof-research/cite-bubeck2015-gd-smooth-convex-rate.md`，记录**精确定理号**（Theorem 3.3，§3.2，p. 267）与**精确常数** $2\smooth\|x_1-x^\star\|^2/(t-1)$（按原文，不用更松的教科书变体）。

**验证/引用边界**在 prose 中清晰（§4 开头有方框声明；B2 开头明言「全部引用、无一机器验证」）且在 provenance 通道清晰（B1 有 5 个 `% @lx-from`，B2 一个都没有）。

### §10.3 第二层 gate（全绿，5 定理）

- `lean-wrapper.py Proof.lean --mode build --axioms <五个>` → `integrity_ok:true`，**5/5 PASS**，闭包 $=\{$`propext`,`Classical.choice`,`Quot.sound`$\}$，无 sorry/admit/axiom；
- `lean_lint.py --style --lock` → `Bridge.lean` 与 `DecodeIff.lean` 均 0 errors（SL1：新 key 已冻结，4 旧 key 字节不变）；
- `drift_check.py` → 0 errors，**18 Lean ↔ 18 LaTeX**（13 条 D4 提示非阻塞）；
- `lint.py` → 0 errors / 0 warnings；`latexmk-wrapper.py` → `compile_ok:true`，无 undef cite/ref，无 >50pt overfull；PDF 7 页。

**文件**：`Proof/Proofs/Bridge.lean`（桥，带 `@lx`）、`Proof/Settings.lean`（`def lossCE`）、`sections/04-bridge-and-dynamics.tex`（B1 验证 + B2 引用）、`refs.bib`、digest。
