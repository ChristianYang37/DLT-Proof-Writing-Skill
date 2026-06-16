# Reasoning as implicit-loss optimization — 单 token 解码的 iff 刻画（Lean 机器验证版）

本文档面向**本科数学背景**的读者，一步步讲清这篇（很短的）结果在问什么、设定是什么、定理怎么读、怎么证、以及它**诚实地**说了/没说什么。本结果的全部数学内容已在 **Lean 4 + Mathlib** 中机器验证（kernel 检查通过，无 `sorry`、无自定义公理）。

**前置知识**：线性代数（内积、范数）、多元微积分（梯度）、一点点约束优化（Lagrange 乘子 / 一阶条件）。不需要概率论——本结果是**纯确定性**的。

**一句话**：

> 假设「reasoning」是在优化某个**隐式损失** $L$（哪怕优化得并不高效），那么 LLM 是否输出某个 token，由一个**确定性的充要条件**刻画：在 LayerNorm 球面的约束**驻点**处，模型生成答案 token $a^\star$ **当且仅当**「下降方向 $-\nabla L$ 与答案行 $W_{a^\star}$ 的对齐，严格强于与任何其它 token 行的对齐」。

---

## §1 问题与动机

把一段 reasoning 看成在隐藏状态空间 $\mathbb R^d$ 上对某个隐式损失 $L$ 做优化。两个观察：

1. **「哪怕低效」**：我们**不**假设优化高效——不假设收敛速率、不假设到达全局最优。低效优化唯一能保证的，是轨迹最终**停在一个驻点**（一阶条件成立的点）。
2. **解码本身也是优化**：下一个 token 由 $\arg\max_a \langle W_U^a, x\rangle$（贪心解码）给出，这是对 logit 的一个 $\arg\max$。

于是「reasoning 后的 token 输出」= 两个优化的复合。我们问：**在最一般的假设下，输出哪个 token 由什么充要条件决定？** 答案是一个干净的 iff，且能被 Lean 机器验证。

---

## §2 数学设定

- **状态空间** $E=\mathbb R^d$（实内积空间），内积 $\langle\cdot,\cdot\rangle$。
- **词表** $\mathcal V$（有限，$\ge 2$ 个 token）；**unembedding** $W:\mathcal V\to E$，token $a$ 的行是 $W_a$（这就是 LLM 真实的 linear head）。
- **LayerNorm 球面** $\mathcal S_r=\{x:\|x\|=r\}$，$r>0$。
- **解码器**（单 token，$n=1$，所以贪心 $\arg\max$ **就是**真解码器）：token $a$ 在 $x$ 处**被生成**当且仅当 $x$ 落在 $a$ 的**开解码锥**里：
  $$\mathrm{Gen}(a,x)\quad:\Longleftrightarrow\quad \forall b\neq a,\ \langle W_a, x\rangle > \langle W_b, x\rangle.$$
- **隐式损失** $L:E\to\mathbb R$，可微，梯度 $\nabla L$。
- **约束驻点**（reasoning「停下来」的形式化）：在球面约束下的一阶（Lagrange）条件——梯度与球面法向平行：
  $$\nabla L(x^\star)=\mu\, x^\star,\qquad \mu=\frac{\langle\nabla L(x^\star),x^\star\rangle}{r^2}.$$
  等价地：Riemannian 梯度（$\nabla L$ 到切空间的投影）为零。**这是我们对优化的唯一假设**——没有凸性、没有全局最优、没有速率。

---

## §3 主定理：decode ⟺ gradient separation

**定理**（已 Lean 验证，`Decode.decode_iff_gradient_separation`）。设 $\|x^\star\|=r$，$\nabla L(x^\star)=\mu\,x^\star$，$\mu\neq 0$。则对答案 token $a^\star$：

$$\boxed{\ \mathrm{Gen}(a^\star,x^\star)\quad\Longleftrightarrow\quad \forall b\neq a^\star,\ \ \mu\,\big\langle W_{a^\star}-W_b,\ \nabla L(x^\star)\big\rangle\ >\ 0.\ }$$

**怎么读 / 怎么证**（证明就是这几行内积代数，所以它能干净地在 Lean 里过）：

1. 由驻点性且 $\mu\neq 0$，把位置用梯度表示：$x^\star=\mu^{-1}\,\nabla L(x^\star)$。
2. 解码锥条件 $\langle W_{a^\star},x^\star\rangle>\langle W_b,x^\star\rangle$ 等价于 $\langle W_{a^\star}-W_b,\ x^\star\rangle>0$（内积的线性）。
3. 代入第 1 步：$\langle W_{a^\star}-W_b,x^\star\rangle=\mu^{-1}\langle W_{a^\star}-W_b,\nabla L(x^\star)\rangle$。
4. **符号等价**：因为 $\mu^2>0$，对任意实数 $c$ 有 $\mu^{-1}c>0\iff \mu c>0$。于是上式 $>0$ 等价于 $\mu\,\langle W_{a^\star}-W_b,\nabla L(x^\star)\rangle>0$。
5. 对所有竞争者 $b\neq a^\star$ 取 $\forall$，即得 iff。$\qquad\blacksquare$

> 注意符号是 **$>0$**（不是 $<0$）。这一点恰恰是 Lean 验证的价值：手写时极易把符号写反，而 kernel 不会放过。

---

## §4 推论：下降方向分离（$\mu<0$，约束最小情形）

**推论**（`Decode.decode_iff_descent_separation_of_neg`）。在主定理假设下若 $\mu<0$（约束**最小**的典型情形），则

$$\boxed{\ \mathrm{Gen}(a^\star,x^\star)\quad\Longleftrightarrow\quad \forall b\neq a^\star,\ \ \big\langle W_{a^\star}-W_b,\ -\nabla L(x^\star)\big\rangle\ >\ 0.\ }$$

即：**生成答案 $a^\star$ 当且仅当下降方向 $-\nabla L(x^\star)$ 与答案行 $W_{a^\star}$ 的对齐，严格强于与每个竞争者行 $W_b$ 的对齐。** 这是最贴近「reasoning 直觉」的读法——「往降损失的方向走，恰好把答案行顶到最高」。

（证明：$\mu<0$ 时 $\mu c>0\iff c<0$，而 $\langle v,-\nabla L\rangle=-\langle v,\nabla L\rangle>0\iff \langle v,\nabla L\rangle<0$，两者同条件。）

**小例子（2 个 token，便于核对符号）**：$W_1=(1,0),W_2=(0,1)$，$L(x)=-\langle (2,1),x\rangle$（把状态拉向 $(2,1)$）。球面（$r=1$）上的最小在 $x^\star=(2,1)/\sqrt5$，$\nabla L=-(2,1)$，故 $\mu=-\sqrt5<0$。生成的 token：$\langle W_1,x^\star\rangle=2/\sqrt5>\langle W_2,x^\star\rangle=1/\sqrt5$，即 $a^\star=1$。验证 iff：$\mu\langle W_1-W_2,\nabla L\rangle=(-\sqrt5)\langle(1,-1),(-2,-1)\rangle=(-\sqrt5)(-1)=\sqrt5>0$ ✓。下降方向读法：$-\nabla L=(2,1)$，$\langle W_1-W_2,(2,1)\rangle=2-1=1>0$ ✓。

---

## §5 诚实标注（这正是这版的卖点）

- **比所述更一般**：Lean linter 显示证明**根本没用到** $\|x^\star\|=r$ 和 $r>0$——只用了 $\mu\neq 0$ 和驻点性 $\nabla L(x^\star)=\mu x^\star$。所以这个刻画对**任何**满足「梯度平行于位置、乘子非零」的点都成立，在球面上或不在球面上都行。我们保留球面假设只是为了对齐 LayerNorm 的几何设定，并在 `rem:generalization` 里如实标注其未被使用（这是**加强**，不是缺陷）。
- **可微性是 setting 注记，不是 load-bearing 假设**：证明从不对 $L$ 求导，只用到 $\nabla L(x^\star)$ 这个**值**（通过驻点假设）。所以把 `Differentiable L` 放进定理假设属于「假设膨胀」，按 Occam 我们不放（Mathlib 的 `gradient` 在不可微处定义为 $0$，陈述照样有意义）。
- **$\mu$ 的符号**：一般情形条件带 $\mathrm{sign}(\mu)$；$\mu<0$ 是「损失把答案行拉过来」这类情形的典型，给出干净的下降方向读法。$\mu$ 的符号不由驻点性单独决定，所以主定理诚实地保留 $\mu$。
- **这是一个干净的「刻画」，不是深定理**：核心是几行内积代数——这恰恰是它能在今天的 Mathlib 里**端到端验证**的原因。价值在于：忠实的机器验证 + 「下降方向分离」这个可解释的读法，而非证明难度。

---

## §6 洞察（insight）：这个 iff 到底在说什么

1. **解码读的是「梯度」，不是「状态」。** 朴素地想，输出取决于轨迹停在哪（$x^\star$）。但驻点性把 $x^\star$ 与 $\nabla L(x^\star)$ 锁成平行（$x^\star=\mu^{-1}\nabla L$），于是输出**等价地由损失在停点处的梯度方向决定**。优化器的一阶信息 = 解码器的输入——这是「优化」与「解码」之间一座精确的桥。

2. **只有方向和乘子符号要紧，大小全抵消。** 条件对 $\nabla L$ 尺度不变（$L\mapsto cL,\ c>0$ 不改变输出）。决定输出的只是：(a) $\nabla L(x^\star)$ 相对行差 $W_{a^\star}-W_b$ 的**方向**；(b) $\mathrm{sign}(\mu)$（停点是「min 型」$\mu<0$ 还是「max 型」）。**整个解码结果坍缩成 $|\mathcal V|-1$ 个内积的符号模式**——连续优化里冒出离散结构。

3. **「答案」就是与下降方向最对齐的那一行。**（$\mu<0$）把「模型输出什么」重述为「下降方向 $-\nabla L$ 最指向哪一行」。损失景观（$-\nabla L$ 指哪）与输出 token（最对齐的行）是**同一个比较**。这是「reasoning = 朝答案降损失」这句直觉所能达到的最精确形式。

4. **效率与输出无关——「停在哪」与「怎么到的」解耦。** 最反直觉也最干净的一点：不需要凸、不需要全局最优、不需要速率，只要停在驻点。所以「输出哪个 token」是**停点 + 解码几何**的性质，与（可能很乱、很低效的）动力学**无关**。你那句「哪怕优化低效」被定理照单全收：效率根本不进入这个 iff。

5. **它其实与球面无关。**（linter 揭示的）证明没用上 $\|x^\star\|=r$——只要 $\nabla L\parallel x^\star$ 且 $\mu\neq0$。所以现象的本质是「梯度对齐」，而非某个特定流形。诚实地说：这既是普适性，也是局限——结果并没真正「用到」LayerNorm 几何本身。

## §7 证明出来有什么用

- **机理可解释性（白盒判据）。** 给定训练好的模型、某问题收敛后的隐藏态、以及 unembedding，可以**直接计算** $\langle W_{a^\star}-W_b,\,-\nabla L(x^\star)\rangle$ 对所有 $b$ 的符号，从而**预测**它会不会解码正确——一个可计算的白盒诊断。又因为是 **iff（充要）**，它是紧的：解码失败 $\iff$ 某竞争者行与下降方向更对齐——它**精确指出是哪个竞争者、为什么**赢。

- **把「优化直觉」钉成可检验命题。**「reasoning 在朝答案降损失」常被当口号；这个 iff 给出它**何时成立**的精确条件（下降方向必须把答案行顶过所有竞争者），把口号变成可证伪的陈述。

- **一块可信的地基 / 可复用引理。** 因为是 Lean 机器验证的，可以放心当作更大论证的一环：例如与某个「收敛到好驻点」的结果拼接得到端到端保证；或对具体损失（如交叉熵）特化。

- **一个方法论模板。** 它示范了「**最小诚实假设 + 机器验证的 iff**」这种关于 LLM 的理论主张的写法，并证明：只要把范围收到确定性、有限维、内积代数，这类主张**今天就能在 Lean 里形式化**。

## §8 为什么这样证明（方法论）

- **为什么走确定性 + Lean、丢掉概率机器。** 之前的相变/点火版堆叠概率假设（对齐率、各向同性噪声、closure）去拿「收敛」，结果既「牵强」又**无法机器验证**。退一步问最小的问题（「停在驻点后解码谁」），换来：(a) 基本只需一条诚实假设；(b) 一个**精确 iff**（没有可糊弄的常数/松弛）；(c) **可被 kernel 检查**。这正是 Lean-first skill 强制的 truth-seeking 立场：用「可证的少」换掉「动听但不可验的多」。也因此本版讲「到了驻点输出谁」、把「能不能到」留给更难且未验证的动力学——两者互补，但只有前者今天能被证实。

- **为什么把驻点性写成假设、而不去推导收敛。** 把「reasoning 停下来」编码成一阶条件 $\nabla L=\mu x$（而非证明收敛），既让 **Mathlib 依赖很轻**（不需要流形/Lagrange 理论，所以它真的能过），又**诚实划清边界**：我们刻画驻点，不声称动力学到达它。「低效优化」恰被如此捕捉——只建模终点的一阶性质，不建模路径。

- **为什么用「符号等价」这个小核。** 整个证明的核心是引理 $\mu^{-1}c>0\iff\mu c>0$（二者差一个 $\mu^2>0$）。它把「乘子符号唯一要紧之处」隔离出来，使整件事变成「清分母」，证明因此只有约十行、且能被验证。方法论：**归约到最小的诚实代数核，让 Lean 检查，再忠实渲染成 LaTeX**——顺带，正是 Lean 在此抓出了我手写时写反的符号。

- **为什么要 iff、而不是单向界。** 概率版给的是单向高概率界（越过阈值则成功）；iff 更强也更干净——它是**完整刻画**（必要且充分），无概率、无常数。对一个关于确定性解码器的白盒主张，iff 才是「对」的对象。

---

## §9 Lean 对应与验证状态

- 定理：`Decode.decode_iff_gradient_separation`、`Decode.decode_iff_descent_separation_of_neg`（外加辅助 `Decode.sign_equiv`）。
- `#print axioms` 闭包 $=\{$`propext`, `Classical.choice`, `Quot.sound`$\}$（Mathlib 的标准基底），**无 `sorry`、无自定义 `axiom`、无 `native_decide`**。
- Gate 全绿：`lean-wrapper --mode build` → `integrity_ok`；`lean_lint --style --lock` → 0/0（签名锁 SL1 成立）；`drift_check` → 0 errors，8 Lean ↔ 8 LaTeX 步骤双射；LaTeX `lint`/`latexmk` → 0 errors / `compile_ok`。
- 文件：Lean 源在 `.lean-proof/Proof/{Settings,Statements,Proofs/DecodeIff}.lean`（+ `Vacuity.lean` 非平凡性见证：假设并非空真）；人读 LaTeX 在 `sections/01-preliminaries.tex`（设定/定义）+ `sections/02-theorem-decode-iff.tex`（引理+定理+推论，每个 LaTeX 步骤都带 `% @lx-from:` 注释指回它所验证的 Lean 声明）；编译产物 `.output/main.pdf`。

---

## 附录：核心对象速查

| 对象 | 记号 | 含义 |
|---|---|---|
| 状态空间 | $E=\mathbb R^d$ | 实内积空间（隐藏态所在） |
| unembedding | $W_a$ | token $a$ 的行（真实 linear head） |
| 球面 | $\mathcal S_r=\{\|x\|=r\}$ | LayerNorm 约束集 |
| 解码器 | $\mathrm{Gen}(a,x)$ | $\forall b\neq a,\ \langle W_a,x\rangle>\langle W_b,x\rangle$（贪心 = 真解码） |
| 隐式损失 | $L$，$\nabla L$ | 可微（setting 注记） |
| 驻点性 | $\nabla L(x^\star)=\mu x^\star$ | 球面约束一阶条件（唯一优化假设） |
| 乘子 | $\mu\neq 0$ | $\mathrm{sign}(\mu)$ 携带朝向；$\mu<0$ = 约束最小 |

**主 iff**：$\mathrm{Gen}(a^\star,x^\star)\iff \forall b\neq a^\star,\ \mu\langle W_{a^\star}-W_b,\nabla L(x^\star)\rangle>0$。
**下降形（$\mu<0$）**：$\mathrm{Gen}(a^\star,x^\star)\iff \forall b\neq a^\star,\ \langle W_{a^\star}-W_b,-\nabla L(x^\star)\rangle>0$。

---

**版本信息**：Lean-verified iff 版（2026-06-02）。几何：LayerNorm 球面（但证明只需 $\mu\neq0$+驻点）；答案：单 token（$D_{\text{true}}=$ 贪心 argmax）；假设：可微 $L$ + 球面约束驻点（凸性/最优/速率均不需要）；结果：1 主定理 + 1 推论 + 1 辅助引理，全部 Lean 4 + Mathlib 机器验证。如需深入，直接读 `.lean-proof/Proof/Proofs/DecodeIff.lean`（每步带 `@lx` 注释）或 `sections/02-theorem-decode-iff.tex`。
