# Saad and Solla, "On-line Learning in Soft Committee Machines" (1995)

## Reference

Saad, David and Solla, Sara A.
*On-line learning in soft committee machines.*
Physical Review E, 52(4):4225--4243, 1995.
DOI: 10.1103/PhysRevE.52.4225
Companion paper:
Saad, David and Solla, Sara A.
*Exact solution for on-line learning in multilayer neural networks.*
Physical Review Letters, 74(21):4337--4340, 1995.
DOI: 10.1103/PhysRevLett.74.4337

## What is cited

We cite Saad--Solla 1995 as the **historical origin** of the
high-dimensional online-SGD analysis via **order parameters** and the
$1/d$ learning-rate scaling convention. Their setup: a two-layer
soft-committee machine learning a target soft-committee teacher from
i.i.d. Gaussian inputs $x \sim \mathcal N(0, I_d)$, trained by online
stochastic gradient descent with learning rate $\eta$. They show that
in the limit $d \to \infty$ with $\eta = \tilde\eta / d$ and rescaled
time $\alpha = t/d$, the **order parameters**
$Q_{ij} = w_i \cdot w_j / d$ (student-student overlaps) and
$R_{in} = w_i \cdot B_n / d$ (student-teacher overlaps) satisfy a
closed system of ODEs. The "$\eta = \tilde\eta/d$" convention is what
the modern Ben Arous--Gheissari--Jagannath framework calls the
critical step-size scaling.

For us, Saad--Solla is the **earliest precedent** for the
$\delta_n \asymp 1/d$ scaling assumption that our $\alpha(d) \sim
\sqrt d$ corresponds to. Their per-step weight update
$w_i^{t+1} = w_i^t - (\eta/d) \cdot \nabla L_t$ produces a per-step
projection-magnitude $\eta/d \cdot \|\nabla L\| \sim \eta/\sqrt d$
(because $\|\nabla L\| \sim \sqrt d$ for random inputs). Translating
into our reasoning-token language, this matches the
per-effective-token drift magnitude $\alpha \sim \sqrt d$ in our
absolute-scale parametrization.

## Why we cite it

Two reasons:

1. **Historical authority.** The $1/d$ learning-rate convention has been
   the high-dim online-SGD standard for thirty years. Saad--Solla 1995
   is the canonical citation; modern follow-ups (Goldt, Mei--Montanari,
   Veiga et al., Ben Arous--Gheissari--Jagannath) all build on this
   framework. Citing Saad--Solla establishes that our scaling
   assumption is not ad hoc but the standard high-dim convention.
2. **Order-parameter intuition.** Their order-parameter
   reduction $\R^d \rightsquigarrow \R^{O(1)}$ is the mathematical
   archetype for our summary-statistic reduction $L_t = -\log\pi(x_t;Q)
   \in \R$. The proof technique they introduce (closing the
   $d$-dependent stochastic process onto a low-dimensional ODE/SDE) is
   what we adapt for the snowball / extinction analysis of Theorem~T1.

## Verification

Citation verified against the Physical Review E record (vol.~52,
issue~4, October 1995). Author list, title, and pagination match.
The "$\eta = \tilde\eta/d$ with $\alpha = t/d$" scaling convention
appears in their Section~II ("Description of the learning dynamics");
the order-parameter ODE system is their Eqs.~(11)--(12). The companion
PRL paper (Saad--Solla 1995b, vol.~74, issue~21, May 1995) gives the
shorter announcement.
