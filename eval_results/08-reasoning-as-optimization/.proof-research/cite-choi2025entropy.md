# Choi et al., "Entropy After </think> for Reasoning Model Early Exiting" (2025)

## Reference

Choi, Junhyuck and Choi, Heewoong and Bae, Hyeonsoo and Lee, Eungbean
and Han, Jaeseung and Kang, Inho and Yoon, Sungroh.
*Entropy After </think> for Reasoning Model Early Exiting.*
arXiv preprint arXiv:2509.26522, 2025.
URL: https://arxiv.org/abs/2509.26522

## What is cited

The empirical observation: after the `</think>` token is appended to a
reasoning trajectory, the next-token entropy (Shannon entropy of the
softmax distribution at the position following `</think>`) decreases
monotonically with the reasoning length $T$ and stabilises at a
model-dependent plateau. The authors use a moving-average variance of
the entropy as an early-exit signal: when the entropy plateaus, no
further thinking is required.

## Why we cite it

\Cref{cor:entropy_decay} provides a quantitative first-principles
prediction for the entropy trajectory $H_T$: it converges in expectation
at exponential rate $\exp(-p_0 T / 8)$ to a model-dependent limit
$H_\infty(Q)$. The empirical plateau observed in \cite{choi2025entropy}
is therefore the empirical signature of the convergence predicted by
our corollary, and their EMA-based stopping rule fires precisely when
the exponentially-decaying envelope of \Cref{eq:entropy_decay_rate}
has shrunk into the irreducible floor.

This is the only direct empirical-curve-prediction-from-theory bridge
in our paper; it converts the abstract object $\|x_T - V^*(Q)\|$ into
an exactly observable inference-time quantity (next-token entropy at
`</think>`) that prior empirical work measures.

## Verification

Citation verified against arXiv record arXiv:2509.26522 (Sep 2025).
Author list, title, and abstract match the cited claim.
