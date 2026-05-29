# Reasoning as noisy Riemannian SGD on the LayerNorm sphere — 完整推导导读

本文档面向**本科数学背景**的读者，一步步推导每个结果、解释概念背后的直觉、并指出每一步为什么重要。读完之后你应该能完整复述这篇论文在做什么、怎么做、得到了什么，以及**哪些地方是诚实标注的理想化**。

**前置知识**：微积分、线性代数、基本概率（随机变量、条件期望、方差、Markov 不等式）。martingale、sub-Gaussian、球面几何、Berry–Esseen、Sudakov minoration 这些会在用到时简单介绍。

**一句话概括**：

> 把"thinking LLM 的一段思考"看成在 **LayerNorm 球面**上对**交叉熵**做的**带噪 Riemannian SGD（带动量）**。是否解码出正确答案，取决于一个**单一全局参数**——每步朝正确方向迈进的概率 $p$（净对齐率 $\delta=2p-1$）——是否越过一个由架构决定的**临界值 $\lambda_c\sim 1/\sqrt{T_{\max} d}$**。越过则成功，落在下方则失败。**模型越大（$d$ 越大）、思考越长（$T_{\max}$ 越大），临界值越低**，于是 reasoning 更容易成功。

**全文结构**：

- §1 现象、问题与整体思路
- §2 数学设定（球面、动力学、loss、margin、indicator）
- §3 唯一的行为假设 A1 + 架构假设 A2
- §4 数学工具速览
- §5 Riemannian gradient 与"为什么叫 descent"（只是 motivation）
- §6 球面的代价：retraction 稳定性
- §7 核心引理 I — 信号下界（净漂移 $\delta c$ 的恒等式）
- §8 核心引理 II — 错误 logit 的上界与下界
- §9 loss-to-margin 桥接
- §10 Theorem R1 — 两侧相变
- §11 Theorem R2 — 临界窗口的 Gaussian 形状
- §12 Theorem R3′ — cone confinement（为什么它不是 ODE）
- §13 诚实标注（working stylizations / caveats）
- §14 结论与 insight
- 附录：核心公式速查

**相对旧版（"snowball / phase-transition", Round 7）的关键变化**：

- **答案改为单 token（$n=1$）**：$W_U\in\mathbb R^{|\mathcal V|\times d}$ 就是 LLM **真实的 linear head**，不再是 $|\mathcal V|^n\times d$ 的"序列线性化"虚构物。于是 $\arg\max$ logit **就是** greedy 解码，$D_{\text{true}}=D_{\text{lin}}$，旧版那条"只能单向蕴含、失败界只对线性代理成立"的免责声明**整个消失**。
- **几何改为球面 / Riemannian**：状态 $x_t$ 活在 LayerNorm 球面，LayerNorm 充当 retraction，追踪的是**角度**（margin 方向），不是半径。
- **删掉 snowball region**：旧版只在 $\{L<L^\star\}$ 里施加对齐率约束，这几乎是"假设你已经在收敛盆地里"。新版的假设是**全局**的，相变是**结论**而不是预设。
- **假设塌成两条**：唯一行为假设 A1（速率 $p$ + 幅度 $c$）+ 架构假设 A2。
- **结果从 5 个减到 3 个**：R1（两侧相变）、R2（临界窗口 Gaussian）、R3′（cone confinement）。旧版 T3/T5/T6 删除；ODE 只作为标注 remark 出现。

---

## §1 现象、问题与整体思路

### 1.1 Thinking LLM 与 test-time scaling

OpenAI o1、DeepSeek R1、Qwen-3 Thinking 这类模型在回答前先生成一段思考（reasoning tokens），再输出答案。经验上：思考越长（生成越多 reasoning token），答对概率越高——这条曲线叫 **test-time scaling law**。

我们要回答的数学问题是：

- **临界条件**：什么时候 reasoning 必然成功？什么时候必然失败？
- **模型大小的作用**：为什么大模型 reason 得好、小模型不行？
- **临界窗口**：在成功/失败的边界附近，成功概率以什么形态过渡？
- **轨迹几何**：reasoning 轨迹在状态空间里长什么样？

### 1.2 核心 insight

> Reasoning 不是"每个 token 都精确做一步梯度下降"，而是 **"在各向同性噪声里，少数朝正确方向的 token 累积出信号"**。

把每步看成一次带噪更新。每步对"正确 token 方向"的投影，**符号**是正（朝答案）还是负（背答案）由一个概率 $p$ 控制，**幅度**有一个下界 $c$。净漂移正比于 $\delta c$，其中 $\delta:=2p-1$。与之竞争的是高维噪声：错误方向的 logit 像 $|\mathcal V|-1$ 个近正交的 sub-Gaussian，幅度 $\sim 1/\sqrt d$，横跨 $T_{\max}$ 步后噪声尺度 $\sim\sqrt{\log|\mathcal V|/(T_{\max} d)}$。

信号 $\delta c$ 与噪声 $\sqrt{\log|\mathcal V|/(T_{\max} d)}$ 的较量，给出临界率

$$\boxed{\;\lambda_c \sim \frac{1}{\sqrt{T_{\max}\, d}}\;}$$

**这就是大模型 + 长思考更易成功的根源。**

### 1.3 三个定理

- **R1（两侧相变）**：$\delta\ge\sqrt2\,\lambda_c$ ⇒ 成功（高概率）；$\delta\le\lambda_c/\sqrt2$ ⇒ 失败（高概率）。两侧都对**真**解码器成立。
- **R2（临界窗口）**：在 $\delta$ 落在 $(\lambda_c/\sqrt2,\sqrt2\,\lambda_c)$ 时，成功概率 $=\Phi(z)+O(\text{Berry–Esseen})$，是光滑的 sigmoid 过渡，临界点恰好 $1/2$。
- **R3′（cone confinement）**：超临界时，轨迹的角度会进入并停留在围绕正确方向的一个球冠里，终端 margin 集中在信号水平 $\delta c\rho_0/M$。这是**有限步、有限维**的几何陈述，不是 ODE。

---

## §2 数学设定

### 2.1 LayerNorm 球面（`def:sphere`）

LayerNorm 把激活归一化到固定范数；我们用标准约定 $\|x\|_2=\sqrt d$。于是状态活在

$$\mathcal M_d := \{x\in\mathbb R^d : \|x\|_2=\sqrt d\},$$

一个半径 $\sqrt d$ 的球面（光滑子流形）。$x$ 处的切空间 $T_x\mathcal M_d=\{v:\langle x,v\rangle=0\}$。

**为什么是球面而不是球**：旧版有个失败的尝试——追踪半径 $r=\|x\|$ 当 order parameter，但 LayerNorm 让 $r\equiv\sqrt d$ 恒定，半径毫无信息。**正确的做法是追踪角度**（$x$ 与正确方向的夹角余弦），这正是下面的 angular margin。

### 2.2 动力学：带 retraction 的 Riemannian SGDM（`def:dynamics`）

一个 attention head 读成"一步带动量的 SGD + 归一化回球面"。给定步长 $\alpha\in(0,1]$（softmax 自权重，自适应学习率）和随机伪梯度值向量 $V_t$：

$$\tilde x_t = (1-\alpha)\,x_{t-1} + \alpha\, V_t,\qquad x_t = \sqrt d\,\frac{\tilde x_t}{\|\tilde x_t\|_2}.$$

- 第一步是 **SGDM**：衰减因子 $1-\alpha$、步长 $\alpha$，$-V_t$ 当伪梯度。写成 $\tilde x_t-x_{t-1}=\alpha(V_t-x_{t-1})$ 就看出这是 EMA/动量结构。
- 第二步是 **retraction**（即 LayerNorm）：把 $\tilde x_t$ 投回球面。

**展开（`lem:running_average`）**：未归一化的迭代是值向量的凸组合

$$\tilde x_T = \sum_{k=0}^T w_{T,k} V_k,\quad w_{T,k}\ge0,\quad \sum_k w_{T,k}=1,\quad \tau:=\tfrac1T\sum_t w_{T,t}=\tfrac1T,$$

约定 $V_0:=x_0$，且 $w_{T,0}=O(1/T)$——**初始状态 $x_0$ 随 $T$ 增大被冲刷掉**（只贡献 $O(1/T)$）。这是后面"零初始条件"的根据。

**关键警示**：$\sum_k w_{T,k}=1$ 只对**未归一化**的 $\tilde x_T$ 成立，**绝不能用在归一化后的 $x_T$ 上**——从 $\tilde x_T$ 到 $x_T$ 的过渡是 `lem:retraction_stability` 的工作（§6）。

**没有 per-step 收敛速率（`rem:sgdm_reading`）**：因为权重和为 1，每步权重 $\tau=1/T$，轨迹**没有** per-step 的几何收缩率。所以全文不走 Foster–Lyapunov 的"每步 loss 下降"路线，而是围绕**横跨 $T_{\max}$ 的累积鞅集中**。（旧版的 T2 收敛率定理就死在这个不兼容上，现已不再尝试。）

### 2.3 交叉熵 loss（`def:loss`）

$W_U\in\mathbb R^{|\mathcal V|\times d}$ 是**真实的** unembedding（linear head），行 $W_U^a$ 对应 token $a$。单 token 答案：正确 token $a^\star$，答案集 $\mathcal A=\{a^\star\}$。softmax 概率 $p=\mathrm{softmax}(W_U x)$。**交叉熵**：

$$L(x;Q) = \log\Big(\sum_{a} e^{\langle W_U^a,x\rangle}\Big) - \langle W_U^{a^\star},x\rangle = -\log p_{a^\star}\in[0,\infty).$$

**关键性质**：作为 log-sum-exp 减线性，$L$ 在 $\mathbb R^d$ 上**凸**。球面 $\mathcal M_d$ 是（非凸的）约束集。

Euclidean 梯度（`fac:gradient_form`，标准结果）：$\nabla L = W_U^\top(p-e_{a^\star})$。

### 2.4 Angular margin、logit margin、解码器（`def:angular_margin`–`def:decoder`）

- **Angular margin**（进度统计量）：

$$m_t := \frac{\langle W_U^{a^\star},x_t\rangle}{\|W_U^{a^\star}\|_2\,\sqrt d}\in[-1,1],$$

因为 $\|x_t\|=\sqrt d$ 固定，这是个纯余弦。追踪它等价于追踪正确 logit（差一个固定因子）。

- **Logit margin**：$\mathrm{Margin}(x;Q):=\langle W_U^{a^\star},x\rangle-\max_{a\ne a^\star}\langle W_U^a,x\rangle$。

- **真解码器**：$D_{\text{true}}(x):=\arg\max_a\langle W_U^a,x\rangle$。单 token 时这**就是** greedy 解码，没有任何代理。成功事件：

$$\{D_{\text{true}}(x_T)=a^\star\}=\{\mathrm{Margin}(x_T;Q)>0\}.$$

**这就是 $n=1$ 带来的诚实性升级**：所有结论（成功 **和** 失败）都直接对真解码器成立。

### 2.5 行 incoherence（`def:incoherence`）

相变的维度标度来自一个 $W_U$ 的几何性质：不同 token 行近正交。

$$\mu(W_U):=\max_{a\ne a'}\frac{|\langle W_U^a,W_U^{a'}\rangle|}{\|W_U^a\|_2\|W_U^{a'}\|_2}\quad(\text{最大归一化off-diagonal Gram entry}).$$

高维下典型 $\mu=O(\sqrt{\log|\mathcal V|/d})\ll1$。

### 2.6 Filtration 与 descent indicator（`def:descent_indicator`）

设 $\hat\rho:=W_U^{a^\star}/\|W_U^{a^\star}\|_2$ 为**单位正确行**。每步**正确方向投影**

$$\pi_t := \langle V_t,\hat\rho\rangle\in[-M,M],$$

即值向量 $V_t$ 在正确方向上的分量。**符号 indicator** $\zeta_t:=\mathrm{sign}(\pi_t)\in\{-1,+1\}$。filtration $\mathcal F_t=\sigma(x_0,\dots,x_t,\pi_1,\dots,\pi_t)$。

**为什么 indicator 定在正确方向上（`rem:descent_indicator_role`，至关重要）**：旧版（skeleton）一度想用"loss 下降的符号" $\mathrm{sign}\langle\Delta x_t,-\mathrm{grad}\,L\rangle$ 来定义，但这有个**传递性缺口**——内积对齐不传递，**降低 loss 的一步不一定抬高正确 token 的 logit**。所以这里直接把行为量定义在**正确方向**上：约束的是 $\pi_t$ 的符号率与幅度。Riemannian gradient 只作为"为什么叫 descent"的 motivation（§5），**不进入漂移计算**。

---

## §3 唯一的行为假设 A1 + 架构假设 A2

### 3.1 A1：全局正确方向对齐（`ass:descent`）

存在常数 $p\in[0,1]$ 和 $c\in(0,1]$，使得**对每一步** $k\ge1$：

- **(a) 符号率**：$\Pr[\zeta_k=+1\mid\mathcal F_{k-1}]=p$，对所有 $k$、**与 loss 值、状态区域、时间无关**。记净对齐率 $\delta:=2p-1\in[-1,1]$。
- **(b) 幅度下界**：$\mathbb E[|\pi_k|\mid\mathcal F_{k-1}]\ge c\,\rho_0$。
- **(c) 符号⊥幅度**：给定 $\mathcal F_{k-1}$，符号 $\zeta_k$ 与幅度 $|\pi_k|$ 条件独立。
- **(d) 漂移方向**：$\mathbb E[V_k\mid\mathcal F_{k-1}]=\beta_k\hat\rho$，其中 $\beta_k=\mathbb E[\pi_k\mid\mathcal F_{k-1}]$——即**系统性更新的唯一方向是正确行 $W_U^{a^\star}$，其余都是零均值噪声**。

**净漂移恒等式（这是堵住缺口的关键，`eq:net_drift`）**：由 (c)，$\pi_k=\zeta_k|\pi_k|$ 且二者条件独立，所以

$$\mathbb E[\pi_k\mid\mathcal F_{k-1}]=\mathbb E[\zeta_k\mid\mathcal F_{k-1}]\cdot\mathbb E[|\pi_k|\mid\mathcal F_{k-1}]=\delta\cdot\mathbb E[|\pi_k|\mid\mathcal F_{k-1}].$$

这是个**恒等式**（对 $\delta$ 任何符号都成立）。配上 (b)，当 $\delta\ge0$ 得净漂移下界 $\mathbb E[\pi_k\mid\mathcal F_{k-1}]\ge\delta c\rho_0$；一般地 $|\mathbb E[\pi_k\mid\mathcal F_{k-1}]|\le|\delta|M$。**没有**经过 loss 梯度的传递。

**全局、无 snowball、无初始条件（`rem:descent_globality`）**：(a)(b) 用同一组常数对所有 $k$ 成立，没有 $L^\star$ 门控、没有特权子水平集。初始 $x_0$ 任意（含反极点最坏情形），因为 $x_0$ 被 $w_{T,0}=O(1/T)$ 冲刷掉、且 A2(5) 的各向同性噪声非退化把轨迹推离测度零的反极点集。

- **(c) 是什么（`rem:descent_independence`）**：它控制反对齐步——没有它，一个背向答案的步可能带任意大的幅度压垮有利步，净漂移就不会分解。"幅度与方向无关"是干净的充分条件（例如 $\pi_k$ 是固定非负幅度律的符号混合，Rademacher 型）。
- **(d) 是什么、有多强**：它说每步的**系统性**部分恰好指向答案。这是**最吃重的建模理想化**——见 §13。它的用处：让 incoherence 把漂移转成对**错误行**的小界（$|\langle W_U^a,\mathbb E[V_k]\rangle|\le M\mu_0 R_U$）。

### 3.2 A2：有界架构与有界 score 区（`ass:bounded_architecture`）

1. **Unembedding**：incoherence $\mu(W_U)\le\mu_0$，行范数 $\rho_0\le\|W_U^a\|_2\le R_U$。
2. **值向量**：$\|V_t\|_2\le M$ a.s.
3. **Q/K 投影**：$\|W_Q\|_{\mathrm{op}},\|W_K\|_{\mathrm{op}}\le W_{QK}$。
4. **有界 score 区**：scaled dot-product score $|\langle q,k_t\rangle|\le S$，$S=O(1)$（关于 $d$）。
5. **各向同性噪声（尺度 $1/d$）**：$V_t=\mathbb E[V_t\mid\mathcal F_{t-1}]+\xi_t$，$\xi_t$ 在切空间上协方差 $\frac{\sigma_{\min}^2}{d}I\preceq\mathrm{Cov}(\xi_t)\preceq\frac{\sigma_{\max}^2}{d}I$。下界用于 anti-concentration 与反极点冲刷；上界是喂给 Azuma 的逐方向涨落尺度。

**不再需要 incoherence gap（`rem:architecture_realism`）**：旧 skeleton 想从 gap $\mu_0<\rho_0^2/R_U^2$ "推出" $c$；现在 $c$ 是**假设**的正数，gap 不再 load-bearing。$\mu_0$ 只在两处被用：`lem:incorrect_max` 的漂移项 $\mu_0 R_U M$、`lem:incorrect_max_lower` 的成对去相关。

**有界 score 区的诚实标注**：在 $\|x\|=\sqrt d$ 下，Cauchy–Schwarz 给 $|\langle q,k_t\rangle|\le W_{QK}^2 d/\sqrt{d_k}$（raw 单位），所以 $S=O(1)$ 是对**归一化约定**的真假设，不是自动成立。**当它失效**（raw bounded-entry 范式、$S\sim\sqrt d$）时，$S_T\le e^{2S}/T$ 变 vacuous、headline 标度丢失——所以把 $S=O(1)$ 显式标为 named hypothesis。

---

## §4 数学工具速览

- **凸组合 / running average（`lem:running_average`）**：$\tilde x_T=\sum w_{T,k}V_k$，$\sum w=1$。见 §2.2。
- **高维近正交（`lem:orthogonality`）**：固定单位向量 $e$、$u$ 均匀分布于球面，则 $\mathbb E\langle e,u\rangle^2=1/d$；sub-Gaussian 尾 $\Pr[|\langle e,u\rangle|>t/\sqrt d]\le2e^{-ct^2}$；**且**有配套 small-ball 下界 $\Pr[\langle e,u\rangle>t/\sqrt d]\ge c''e^{-C''t^2}$。这是 $1/\sqrt d$ 的来源，也是 anti-concentration 的输入。
- **softmax 二次变差（`lem:quad_variation`）**：$|\langle q,k_t\rangle|\le S$ ⇒ $\max_t w_{T,t}\le\frac{1}{1+(T-1)e^{-2S}}\le e^{2S}/T$，故 $S_T:=\sum_t w_{T,t}^2\le e^{2S}/T$。这是 $1/\sqrt T$ 的来源（取代旧版"uniform attention"隐藏假设）。
- **Azuma（鞅尾，含 maximal 不等式，`lem:azuma`）**：差分 $|M_t|\le c_M$、条件方差 $\le2\sigma^2/d$，则 $\Pr[\max_{t\le T}|\sum_{s\le t}M_s|>2\sigma\sqrt{T\log(2/\delta)/d}]\le\delta$。$\max_t$ 形式供 R3′ 的"全程"控制。
- **Berry–Esseen for martingales（Hall–Heyde 1980, Thm 3.6）**：把鞅和的标准化分布与 $\Phi$ 的 Kolmogorov 距离，由累积条件三阶矩 / 方差$^{3/2}$ 控制。用于 R2。
- **Sudakov minoration + Borell–TIS（Vershynin Thm 7.4.1 / 5.2.3）**：Gaussian 过程的 max 由成对距离**下界**控制（对相关性鲁棒）。用于 R1 失败分支（§8.2）。

**$1/\sqrt{T_{\max} d}$ 的两个来源（诚实拆分）**：噪声尺度 $=$（$1/\sqrt d$，来自 incoherence / 投影方差）$\times$（$1/\sqrt T$，来自 $S_T\le e^{2S}/T$）。**不**用球面集中（Lévy）去凑 $\sqrt T$ 因子。

---

## §5 Riemannian gradient 与"为什么叫 descent"（`lem:riem_gradient`，motivation）

切投影 $P_x^\perp=I-xx^\top/\|x\|^2$；**Riemannian gradient** $\mathrm{grad}\,L=P_x^\perp\nabla L$（Boumal §2.4）。

凸性给一个有用的**几何事实**：正确行方向上负梯度分量恒正，

$$\langle W_U^{a^\star},-\nabla L\rangle=(1-p_{a^\star})\|W_U^{a^\star}\|^2-\sum_{a\ne a^\star}p_a\langle W_U^{a^\star},W_U^a\rangle\ge(1-p_{a^\star})(\rho_0^2-\mu_0 R_U^2),$$

只在 $p_{a^\star}\to1$（已到最优）时消失。

**它的角色被降为 motivation**：它解释"抬高正确 logit 倾向于降低交叉熵"，从而 dynamics 配叫"descent / SGD on cross-entropy"。但它**不推导 $c$、不进入漂移**（理由见 §2.6 的传递性缺口）。这是相对 skeleton 的一处关键修正——也是分阶段审计抓到的第一个真 bug。

---

## §6 球面的代价：retraction 稳定性（`lem:retraction_stability`）

凸组合 $\tilde x_T$ 活在球**内**，归一化（LayerNorm）把它投回球**面**得 $x_T$。这步引入曲率二阶项。由 Boumal Prop 5.44（球面二阶 retraction，pullback 误差 $O(\|s\|^3)$）+ 半径 $\sqrt d$ 重标：

- 把任一固定行的 logit 从 $\tilde x_T$ 转到 $x_T$，误差是 raw 尺度 $O(1/d)$、角度尺度 $O(1/d^{1.5})$。
- 关键策略：**所有信号下界先在 $\tilde x_T$ 上证**（那里 $\sum w=1$ 成立），再转到 $x_T$ 付这个误差。因为该误差被 $O(1/\sqrt{T_{\max} d})$ 的噪声尺度**主导**，R1/R2/R3′ 不受影响。

（成功/margin 事件 $\{\mathrm{Margin}>0\}$ 在正缩放 $x_T=\sqrt d\,\tilde x_T/\|\tilde x_T\|$ 下不变，所以 R1 的比较直接在 $\tilde x_T$ 上做，retraction 误差根本不进入。）

---

## §7 核心引理 I — 信号下界（`lem:signal_floor`）

**结论**：在 A1+A2 下，以概率 $\ge1-\delta_2$，

$$\langle W_U^{a^\star},\tilde x_T\rangle\ \ge\ \underbrace{\delta\,c\,\rho_0}_{\text{漂移}}\ -\ \underbrace{2R_U M\sqrt{\tfrac{S_T\log(2/\delta_2)}{d}}}_{\text{噪声}},$$

并经 §6 转到 $x_T$（付 $O(1/d^{1.5})$）。

**推导骨架**：
- **漂移**：$\langle W_U^{a^\star},\tilde x_T\rangle=\sum_k w_{T,k}\langle W_U^{a^\star},V_k\rangle$，取条件期望、用 §3.1 的**净漂移恒等式** $\mathbb E[\pi_k]=\delta\,\mathbb E[|\pi_k|]\ge\delta c\rho_0$、再用 $\sum w=1$，得漂移 $\ge\delta c\rho_0$。**与 $T$ 无关**（凸组合归一化使每步权重和恒为 1，所以信号不随 $T$ 累积）。
- **噪声**：中心化部分是鞅差，条件方差 $\le w_{T,k}^2 R_U^2 M^2/d$（$1/d$ 来自 `lem:orthogonality`），Azuma + $S_T\le e^{2S}/T$（$1/T$）给涨落尺度 $\asymp R_U M e^S/\sqrt{Td}$。

**这就是 $\sqrt{T_{\max} d}$ 标度的第二来源**：信号（$T$ 无关）与噪声（$\sim1/\sqrt{Td}$）的较量决定相变。

---

## §8 核心引理 II — 错误 logit 的上界与下界

### 8.1 上界（`lem:incorrect_max`）

$$\max_{a\ne a^\star}\langle W_U^a,\tilde x_T\rangle\ \le\ \underbrace{\mu_0 R_U|D|}_{\text{漂移，靠 incoherence + (d)}}\ +\ \underbrace{2R_U M\sqrt{\tfrac{S_T\log(2(|\mathcal V|-1)/\delta_1)}{d}}}_{\text{噪声，对 }|\mathcal V|-1\text{ 行 union}},$$

其中 $D=\langle\hat\rho,\mathbb E\tilde x_T\rangle$ 是**共享的**正确方向漂移幅度。漂移项小，靠的是 A1(d)：$\mathbb E[V_k]\propto\hat\rho$，所以错误行 $a$ 的系统性投影 $\le\mu_0 R_U|D|$（incoherence）。

### 8.2 下界 / anti-concentration（`lem:incorrect_max_lower`，失败分支的引擎）

失败分支要的是**相反**的东西：错误 logit 的**最大值的下界**——当 $\delta$ 亚临界时，**某个**错误 token 反超正确 token。

$$\max_{a\ne a^\star}\langle W_U^a,x_T\rangle\ \ge\ \sigma_T\sqrt{2\kappa(1-\mu_0)\log(|\mathcal V|-1)}\ -\ \mu_0 R_U|D|,$$

以概率 $\ge1-(|\mathcal V|-1)^{-c_3}$。

**为什么不能"把上界反过来"**：union bound 只能**上**界一个 max。下界 max 需要**去相关 + small-ball**。

**证明路线（Sudakov + Borell–TIS，在失败分支局部特化 Gaussian 噪声）**：
- 把 A2(5) 的噪声在**本引理内**特化为各向同性 Gaussian（scope-fenced，仅此处用）。于是中心化错误投影 $Z_a=\langle W_U^a,\tilde x_T-\mathbb E\tilde x_T\rangle$ 条件 Gaussian，成对相关 $\le\mu_0$（标量协方差使其**精确**约化为归一化 Gram entry，**无 Berry–Esseen 项、无 $\mu_0$ 区限制**），成对距离 $\ge\sqrt{2(1-\mu_0)}\,\sigma_T\cdot O(1)$。
- **Sudakov minoration**（Vershynin Thm 7.4.1）：$|\mathcal V|-1$ 个成对分离的点 ⇒ $\mathbb E[\max_a Z_a]\ge c\,\sigma_T\sqrt{(1-\mu_0)\log(|\mathcal V|-1)}$。
- **Borell–TIS 集中**（Vershynin Thm 5.2.3，Lipschitz 常数 $=$ 最大坐标标准差 $\asymp\sigma_T$）：max 以高概率不低于其均值的一半。

**为什么用 Sudakov 而不是第二矩**：分阶段审计抓到的第二个真 bug——原 skeleton 用第二矩 / Paley–Zygmund，其成对协方差界 $\mathrm{Cov}\le\mu_0\Pr\Pr$ 在**固定 $\mu_0$** 下会塌（高阈值处 $\Pr[\text{both}]/(\Pr\Pr)\approx|\mathcal V|^{\Theta(\mu_0)}$ 多项式爆炸，$\mathrm{Var}\,N\gg(\mathbb E N)^2$）。Sudakov 走**几何距离**，对相关性鲁棒，配 Gaussian 特化后对所有 $\mu_0<1$ 成立。

**诚实代价**：$\kappa\le1/16$ 且 Sudakov 常数 $c$ 数值未定，所以"失败可证地反超成功"的 crossover $|\mathcal V|$ 在显式常数下**极大**（示意性 $\sim10^{25}$）。因此**两侧相变是 asymptotic-in-$|\mathcal V|$ 的陈述**；成功分支的常数是正常的架构量级。

---

## §9 loss-to-margin 桥接（`lem:loss_to_margin`）

单 token（$\mathcal A=\{a^\star\}$）时，解码阈值 $L^\star=\log2$：

$$L(x;Q)<\log2\ \Longrightarrow\ \mathrm{Margin}(x;Q)>0\ \Longleftrightarrow\ D_{\text{true}}(x)=a^\star.$$

直觉：$L<\log2 \Leftrightarrow p_{a^\star}>1/2$，正确概率过半 ⇒ 正确 logit 严格最大 ⇒ greedy 解码成功。**单 token 让这一步是双向、干净的**（多 token 时只能单向，这正是旧版的麻烦来源）。

---

## §10 Theorem R1 — 两侧相变（`thm:R1`）

设 A1、A2 与**温和 incoherence 条件** $\mu_0<\rho_0/R_U$（典型 $\rho_0=R_U=1$ 时即 $\mu_0<1$，自动成立），临界率

$$\boxed{\ \lambda_c=c_1\sqrt{\tfrac{\log|\mathcal V|}{T_{\max} d}},\qquad c_1=\frac{2\sqrt2\,e^S R_U M}{c\,\rho_0(\rho_0-\mu_0 R_U)/R_U}.\ }$$

- **(i) 成功分支**：$\delta\ge\sqrt2\,\lambda_c$ ⇒ $\Pr[D_{\text{true}}(x_{T_{\max}})=a^\star]\ge1-\delta_{\text{fail}}-\frac{1}{|\mathcal V|-1}$。
- **(ii) 失败分支**：$0\le\delta\le\lambda_c/\sqrt2$ ⇒ $\Pr[D_{\text{true}}(x_{T_{\max}})=a^\star]\le\delta_{\text{fail}}+\frac{1}{|\mathcal V|-1}$。

标度 $\lambda_c\propto1/\sqrt{T_{\max} d}$。

**证明关键 — 漂移共享（避免 $\Theta(1)$ 陷阱）**：天真地看，错误 max 的漂移项 $\mu_0 R_U M$ 是 $\Theta(1)$，会压垮临界信号 $\lambda_c\cdot(\dots)\to0$，破坏 headline。解决：正确与错误漂移**共享**同一系统性幅度 $D\in[\delta c\rho_0,\delta M]$（靠 A1(d)）。比较的是 **margin** 漂移

$$\langle W_U^{a^\star}-W_U^{\hat a},\mathbb E\tilde x_T\rangle=D(\langle W_U^{a^\star},\hat\rho\rangle-\langle W_U^{\hat a},\hat\rho\rangle)\ge D(\rho_0-\mu_0 R_U)\ge\delta c\rho_0(\rho_0-\mu_0 R_U),$$

那个 $\Theta(1)$ 项消失，margin 漂移随 $D\to0$ 在临界处 $\to0$。这要求 $\rho_0-\mu_0 R_U>0$，即温和条件 $\mu_0<\rho_0/R_U$。再与 margin 噪声 $\nu\asymp R_U M e^S\sqrt{\log/(T_{\max}d)}$ 比较，$\sqrt2$ slack 吸收对数失配与 $(1-\mu_0)$ 等常数，得阈值。失败分支由 §8.2 的 anti-concentration 给出。

**推论（最小解码维度，`rem:min_dimension`）**：成功需要

$$d\ \ge\ \frac{2c_1^2\log|\mathcal V|}{\delta^2\,T_{\max}},$$

即在对齐率 $\delta$ 下解码所需维度 $\sim\log|\mathcal V|/(\delta^2 T_{\max})$——**越难的问题（$\delta$ 越小）所需维度按平方增长**。（降为 remark，因为它只是 R1(i) 的代数反解，无独立下游用途。）

---

## §11 Theorem R2 — 临界窗口的 Gaussian 形状（`thm:R2`）

R1 留下中间窗口 $\delta\in(\lambda_c/\sqrt2,\sqrt2\,\lambda_c)$ 没说。R2 用 Hall–Heyde 鞅 Berry–Esseen 把它刻画为光滑 sigmoid：

$$\boxed{\ \Pr[D_{\text{true}}(x_{T_{\max}})=a^\star]=\Phi(z)+O(\epsilon_{\text{BE}}),\quad z=\frac{(\delta-\lambda_c)\,c\rho_0(\rho_0-\mu_0 R_U)}{\sigma_{T_{\max}}}.\ }$$

其中 $\sigma_{T_{\max}}^2\le4R_U^2M^2e^{2S}/(T_{\max}d)$，$\epsilon_{\text{BE}}=O\big(e^S/\sqrt{T_{\max}}+\sqrt{\log|\mathcal V|/(T_{\max}d)}\big)$。

**证明关键修复**：Berry–Esseen 施加在**固定方向** $W_U^{a^\star}$ 的正确 logit 鞅上（终端泛函与数据无关），错误一侧作为好事件上确定的阈值，被 `lem:incorrect_max`（上）与 `lem:incorrect_max_lower`（下）夹住。（这是 Phase-D 审稿抓到并修的：原先 BE 施加在 data-dependent 终端上，不合法。）

- **边界值**：$z=0$ at $\delta=\lambda_c$ ⇒ $\Phi(0)=1/2$——临界点恰好 50% 成功率。
- **过渡宽度（`cor:R2_width` + `rem:R2_width_relative`，不可混淆）**：**绝对**宽度（$\delta$ 上从 0.1 到 0.9）$w_{\text{abs}}=\Theta(1/\sqrt{T_{\max}d})$（headline，随 $T_{\max}d\to\infty$ 收窄，恢复 R1 阶跃）；**相对**宽度 $w_{\text{rel}}=w_{\text{abs}}/\lambda_c=\Theta(1/\sqrt{\log|\mathcal V|})$（与 $d,T_{\max}$ 无关）。两者是不同的量，分开陈述。

---

## §12 Theorem R3′ — cone confinement（`thm:R3prime`）

描述**轨迹本身**的几何（不只终点）。超临界 $\delta\ge\sqrt2\,\lambda_c$ 下，设目标角度 $m^\star:=\delta c\rho_0/M$（信号下界的角度单位，一个 $O(1)$ 余弦），球冠 $C=\{x\in\mathcal M_d:m(x)\ge m^\star-\varepsilon\}$。则以概率 $\ge1-\delta_{\text{fail}}-(|\mathcal V|-1)^{-1}$：

- **(i) 进入并停留**：存在 burn-in $T_0=O(1)$（rescaled time，等价 $O(\sigma_{T_{\max}}^{-2}\varepsilon^2)$ raw 步），使 $x_t\in C$ 对所有 $T_0\le t\le T_{\max}$。
- **(ii) 终端集中**：$|m_{T_{\max}}-m^\star|\le O(1/\sqrt{T_{\max}d})$。

**证明用 Azuma 的 maximal 不等式在整个 horizon 上一致控制**涨落（不是 drift recurrence、不是 per-step 收缩）。burn-in 来自 $x_0$ 冲刷（$w_{t,0}=O(1/t)$）。

**为什么它不是 ODE（`rem:R3prime_ode`，诚实标注）**：很想用标量漂移 ODE $\dot m=\delta c\rho_0/M-m$（稳定不动点恰是 $m^\star$）来概括，但**这从 A1 推不出来**，且全文没用它。要让它严格需要两条**额外** stylization：

- **(AS) 渐近平稳性**：loss-分层的下降过程 $(\zeta_t,L_t)$ 需渐近平稳（遍历 / 可和混合），时间平均漂移才能收敛为 $m$ 的状态函数（参 Saad–Solla online learning、Ben Arous 等高维 SGD scaling limit）。
- **(L$\lambda$) Lipschitz 闭合性**：条件漂移须能写成 $m_{t-1}$ 单独的 Lipschitz 函数（closability）。

R3′ 刻意避开两者：它是有限步、用 maximal 不等式证的 confinement，**不携带隐藏 ODE 或 closability**。因 $\sum w=1$ 阻断 per-step Foster–Lyapunov 率，强行造 per-step 率正是 ODE 会偷偷塞进来的东西——我们不塞。

---

## §13 诚实标注（working stylizations / caveats）

| 风格化 / 假设 | 哪里用 | 状态 |
|---|---|---|
| **A1(d)**：系统性更新恰指向正确方向，其余零均值噪声 | R1/R2/R3′ 全局 | **最吃重的建模理想化**；$1/\sqrt{T_{\max}d}$ headline 靠它（否则固定 off-target drift 把阈值推到 $\Theta(1)$）。显式陈述，非隐藏。 |
| **A1(c)**：符号⊥幅度 | 净漂移恒等式 | 控制反对齐尾的干净充分条件；Rademacher 型即满足。 |
| **失败分支特化 Gaussian 噪声** | 仅 `lem:incorrect_max_lower` | scope-fenced；成功分支与 R2 用一般 sub-Gaussian（R2 自己用鞅 CLT 推正态，不能特化否则循环）。 |
| **失败分支 crossover $|\mathcal V|$ 极大** | R1(ii) | Sudakov 常数松（$\kappa\le1/16$、$c$ 未定）；两侧相变是 **asymptotic-in-$|\mathcal V|$**。成功分支常数正常。 |
| **有界 score $S=O(1)$** | `lem:quad_variation`, R1/R2/R3′ | LayerNorm 范式下成立；raw bounded-entry 下 $S\sim\sqrt d$，$S_T$ 界 vacuous，标度丢失。已 named。 |
| **retraction 指数 $O(1/d)$ raw / $O(1/d^{1.5})$ 角度** | `lem:retraction_stability` | 两个指数都诚实写出；任一都被 $1/\sqrt{T_{\max}d}$ 噪声主导，不影响结论。 |
| **(AS)+(L$\lambda$)** | 仅 R3′ 的 ODE remark | 明确标为"非 A1 可推"，全文不用。 |

**与旧版相比的诚实性升级**：$n=1$ 使 $D_{\text{true}}=D_{\text{lin}}$，**失败界也对真解码器成立**（旧版做不到）；去掉 snowball 使相变是**结论**而非预设。

---

## §14 结论与 insight

### 14.1 一句话

> **Reasoning = 在 LayerNorm 球面上对真·交叉熵做的带噪 Riemannian SGD。** 是否解码正确，由单一全局对齐率 $\delta=2p-1$ 与临界值 $\lambda_c\sim1/\sqrt{T_{\max}d}$ 的较量决定。信号 $\delta c$ 不随思考长度累积（凸组合归一化），但高维噪声随 $\sqrt{T_{\max}d}$ 被压制——所以**模型越大、思考越长，越容易把少数对齐 token 积成确定信号**。

### 14.2 三个结果

1. **R1**：两侧相变 $\lambda_c\sim1/\sqrt{T_{\max}d}$，越过即成功、落下即失败（均对真解码器）。
2. **R2**：临界窗口内成功概率 $=\Phi(z)+O(\epsilon_{\text{BE}})$，sigmoid 过渡，临界点 50%。
3. **R3′**：超临界时轨迹被吸入并困在围绕答案的球冠，终端 margin 集中在 $\delta c\rho_0/M$。

### 14.3 终极 message

> 瓶颈不是 reasoning 步数本身，而是 **"$\delta\times\sqrt{d}$" 信噪比**。当模型变大、训练把 $p$ 抬高（$\delta$ 增大），reasoning 就**自动**从相变左侧穿到右侧，**不需要改 reasoning 算法本身**。这是 thinking-LLM 缩放规律的微观机理。

### 14.4 公开问题

1. A1(d) 的弱化版（允许有界 off-target drift）下相变阈值如何变化？
2. 失败分支 crossover $|\mathcal V|$ 的常数收紧（去掉 asymptotic-in-$|\mathcal V|$ 的代价）。
3. R2 的 $\Phi(z)$ 形状在真实 LLM 上的密采样验证。
4. R3′ 的 ODE 极限在 (AS)+(L$\lambda$) 下的严格化（即旧 T5 的正确形式）。

---

## 附录：核心公式速查

**关键定义**：
- 球面 $\mathcal M_d=\{\|x\|_2=\sqrt d\}$；递推 $\tilde x_t=(1-\alpha)x_{t-1}+\alpha V_t$，$x_t=\sqrt d\,\tilde x_t/\|\tilde x_t\|$。
- $L(x;Q)=\log\sum_a e^{\langle W_U^a,x\rangle}-\langle W_U^{a^\star},x\rangle=-\log p_{a^\star}$（凸）。
- angular margin $m_t=\langle W_U^{a^\star},x_t\rangle/(\|W_U^{a^\star}\|\sqrt d)$；logit margin $\mathrm{Margin}=\langle W_U^{a^\star},x\rangle-\max_{a\ne a^\star}\langle W_U^a,x\rangle$。
- $D_{\text{true}}(x)=\arg\max_a\langle W_U^a,x\rangle$（$=$ greedy；成功 $\Leftrightarrow\mathrm{Margin}>0$）。
- 投影 $\pi_t=\langle V_t,\hat\rho\rangle$，$\hat\rho=W_U^{a^\star}/\|W_U^{a^\star}\|$；indicator $\zeta_t=\mathrm{sign}(\pi_t)$。

**唯一行为假设 A1**：$\Pr[\zeta_t=+1\mid\mathcal F_{t-1}]=p$（$\delta=2p-1$）；$\mathbb E[|\pi_t|\mid\mathcal F_{t-1}]\ge c\rho_0$；$\zeta_t\perp|\pi_t|\mid\mathcal F_{t-1}$；$\mathbb E[V_t\mid\mathcal F_{t-1}]=\beta_t\hat\rho$。
**净漂移恒等式**：$\mathbb E[\pi_t\mid\mathcal F_{t-1}]=\delta\,\mathbb E[|\pi_t|\mid\mathcal F_{t-1}]\ge\delta c\rho_0$。

**核心常数**：
- $S_T=\sum_t w_{T,t}^2\le e^{2S}/T$（`lem:quad_variation`）。
- $c_1=\dfrac{2\sqrt2\,e^S R_U M}{c\rho_0(\rho_0-\mu_0 R_U)/R_U}$，$\lambda_c=c_1\sqrt{\log|\mathcal V|/(T_{\max}d)}$。温和 incoherence $\mu_0<\rho_0/R_U$。

**三个定理 in one shot**：

| 定理 | 主要结论 |
|---|---|
| R1 | $\delta\ge\sqrt2\lambda_c\Rightarrow$ 成功 $\ge1-\delta_{\text{fail}}-\frac{1}{|\mathcal V|-1}$；$\delta\le\lambda_c/\sqrt2\Rightarrow$ 失败（真解码器，Sudakov anti-concentration） |
| R2 | $\delta\in(\lambda_c/\sqrt2,\sqrt2\lambda_c)\Rightarrow\Pr[\text{success}]=\Phi(z)+O(\epsilon_{\text{BE}})$，$z\propto(\delta-\lambda_c)\sqrt{T_{\max}d}$，临界点 $1/2$ |
| R3′ | 超临界 $\Rightarrow$ 轨迹进入并困在球冠 $C=\{m\ge m^\star-\varepsilon\}$，$m^\star=\delta c\rho_0/M$，终端 $|m_{T_{\max}}-m^\star|\le O(1/\sqrt{T_{\max}d})$ |

---

**版本信息**：本 PAPER-SUMMARY.md 反映 sphere/Riemannian 重写版（2026-05-29）。
- 几何：LayerNorm 球面 $\mathcal M_d$，Riemannian SGD + retraction
- 答案：单 token（$n=1$），$D_{\text{true}}=D_{\text{lin}}$
- 假设数：2（A1 全局行为 + A2 架构）；无 snowball、无初始条件
- 结果数：3（R1 相变、R2 临界窗口、R3′ cone confinement）
- 引理：running-average、riem-gradient(motivation)、orthogonality、quad-variation、retraction-stability、incorrect-max(上)、signal-floor、Azuma、loss-to-margin、incorrect-max-lower(Sudakov)
- 外部引用：vaswani2017attention、vershynin2018、freedman1975tail、hallheyde1980、saad1995online、benarous2022highdim、boumal2023
- 诚实标注：见 §13（最吃重者为 A1(d) 与失败分支的 asymptotic-in-$|\mathcal V|$）

如需深入，请直接 grep paper 中对应的 `\Cref` label。
