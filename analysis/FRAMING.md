# Reframing the contribution

A paper/thesis-ready reframing of JSD-MP's central claim, grounded in the
numbers in [`SUMMARY.md`](SUMMARY.md) (corrected joint-vs-disjoint analysis) and
[`SWEEP.md`](SWEEP.md) (controlled sensitivity sweep).

## The problem with the current framing

The work is currently framed as **"joint VNF+VNFM placement yields higher
revenue than disjoint placement."** Two issues:

1. **It is partly contradicted by our own data.** On USnet with default
   (slack) management constraints, joint and disjoint are statistically
   indistinguishable in acceptance, and joint revenue is in fact *marginally
   lower* (−0.2% to −0.9%, paired Wilcoxon p<0.01) — because accounting for
   management when it does not bind diverts VNF placement for no benefit.
2. **"Higher revenue" understates the mechanism.** Where joint *does* win, it
   does not win by a few percent of revenue; it wins by **accepting chains that
   disjoint placement strands** — a feasibility effect, not a cost effect.

Averaging revenue smooths over a **bimodal** reality: a disjoint run either
nearly succeeds or **collapses** (e.g. FatTree-80: disjoint accepts
`[24,77,29,33,24,32,72,…]` of 80), because the post-hoc manager step is
infeasible for the layout the VNF stage chose.

## The reframed thesis

> **Management-aware joint placement is a feasibility-preservation mechanism.
> By accounting for VNFM constraints while placing VNFs, it keeps chains
> admissible that a management-blind (disjoint) pipeline would reject after the
> fact. Its value is therefore *conditional*: large exactly when management
> constraints bind (tight manager radius, limited manager capacity, scarce
> manager resources), and negligible — even slightly negative — when they do
> not.**

This is sharper, fully consistent with the data, and turns a soft comparison
into a characterization: *not whether joint helps, but when and why.*

## Draft abstract (new framing)

> Network operators must place service-function chains (VNFs) and also provide
> each chain with a VNF Manager (VNFM) subject to capacity, latency-radius, and
> co-location constraints. Most placement work optimizes VNFs and treats
> management as an afterthought, placing managers only after the VNFs are fixed.
> We show that this *disjoint* approach is not merely suboptimal but
> **frequently infeasible**: management-blind VNF layouts strand whole chains
> because no admissible manager exists. We formulate the **joint** VNF+VNFM
> placement problem (JSD-MP), prove it NP-hard, and give a near-optimal
> dynamic-programming heuristic whose cost is management-aware. Against an exact
> CPLEX baseline the heuristic stays within X% while running orders of magnitude
> faster. Crucially, we **characterize when joint placement matters**: a
> controlled study over manager radius, capacity, and offered load shows the
> joint advantage is a feasibility effect that appears *if and only if* a
> management constraint binds, reaching up to N percentage points of additional
> chain acceptance and vanishing under slack management or compute saturation.

(Fill X% and N from the at-scale optimal-gap run and the real-topology sweep.)

## Contribution bullets (new framing)

1. **Problem & hardness.** Formalize JSD-MP (joint VNF placement + capacitated,
   radius-constrained VNFM placement); NP-hardness. *(Optionally: cast the VNFM
   subproblem as capacitated facility location with coverage.)*
2. **Algorithm.** A management-aware DP/Viterbi heuristic (Bari) that steers VNF
   placement toward management-feasible layouts; near-optimal vs CPLEX, fast.
3. **The feasibility insight (headline).** Joint placement's benefit is
   feasibility preservation, not revenue tuning — disjoint placement is
   *bimodally* prone to management-infeasibility collapse.
4. **The conditional characterization (headline).** A boundary over
   (radius × capacity × load) delimiting where joint placement pays off; a
   controlled on/off experiment establishes the constraint as the *cause*.

## Evidence already in hand

| Regime | Joint accept | Disjoint accept | Reading |
|---|---|---|---|
| USnet, default (slack) mgmt | ~100% | ~100% (CV 0) | joint adds nothing; revenue −0.2…−0.9% (p<0.01) |
| FatTree, default VNFM | ~100% | ~20–87% (bimodal) | joint preserves feasibility; up to ~100%+ revenue uplift |
| USnet + 4-hop radius | ~100% | ~35–94% | tightening one constraint flips the regime |
| Constraint toggle (sweep) | ~100% (immune) | gap +12–19pp ON → **0pp OFF** | constraint is the *cause*; effect decays under load |

The constraint-toggle result is the keystone: with the management constraint
removed, disjoint **equals** joint at every load; switch it on and the gap
appears. Joint acceptance is identical either way — it is immune because it
placed VNFs with management in mind.

## How to restructure the paper

- **Lead** Introduction and Abstract with feasibility + the conditional claim,
  not "more revenue."
- **Promote** the acceptance-rate / feasibility figures (and the constraint
  toggle) to the main results; **demote** mean-revenue line plots to support.
- **Add** the (radius × capacity × load) boundary as the central figure.
- **Keep** the USnet-default null result *in* — as honest evidence delimiting
  the regime (a strength, not a weakness).
- **De-emphasize** the thin oabu-vs-bari margin (~1.7%); reintroduce it only if
  tied to a specific binding regime.

## One-line takeaway for the paper

> Joint placement does not make good layouts better; it makes infeasible layouts
> feasible — exactly when management constraints bite.
