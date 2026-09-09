# What a MISO transmission-pipeline archive would be for

Written before the registry, because the rule is: probe the shape, write the
questions down, try to answer them from what you already have, and only then
add a source. Most questions die at the third step, and that is the point.

The screening that chose this source is recorded outside this repository, in
`webprobes/catalogue.csv` under `miso.mtep`.

## The spine

**MISO publishes `Current Cost` and `Expected ISD`. Not original cost, not
promised ISD.** Every figure in every file is the current one, and the previous
value is gone — the files live at fixed URLs on `cdn.misoenergy.org` that are
overwritten in place.

That was proven, not assumed: the same URL returns one sha for its advertised
`?v=`, for a bogus `?v=19990101000000`, and for no parameter at all. The
parameter is cache-busting, not version addressing. The page still advertises
`?v=20250530143236` while `last-modified` is 2026-06-18, so the version that
link was minted for is already unrecoverable.

**$68.6B of approved transmission and $17.0B under evaluation are carried at a
cost figure that overwrites its own history.** Nobody can say what those
projects were approved at.

## The questions

Status is honest about what can be answered **today** against what needs the
archive to exist. One status — `source not yet added` — is the only one that
justifies another registry entry.

| # | question | needs | status |
| --- | --- | --- | --- |
| Q1 | **What did a project cost when it was approved, versus now?** | ~6 months | **the founding question.** `Current Cost` overwrites; no original is published anywhere |
| Q2 | How many approved projects are already late? | nothing | **answered: 118 of 1,497 approved projects (8%) are past their Expected ISD — 228 of 3,041 facility rows, carrying $952M.** Median 0.7 years over, worst 6.7 |
| Q3 | How far does `Expected ISD` slip before delivery? | ~12 months | needs the archive — the promise is overwritten each time it moves |
| Q4 | What share of *Under Evaluation* reaches Appendix A approval? | ~12 months | needs the archive. 597 projects / $17.0B are in that state today |
| Q5 | How long from proposal cycle to in-service? | nothing | **answered — and it is why this is NOT the headline.** Median 1y, p90 4y, max 15y across 5,182 delivered projects. MISO retains `Target MTEP Cycle` beside the delivered ISD, so this is a larder question and capturing adds nothing |
| Q6 | Which transmission owners slip worst, and by how much? | ~12 months | needs the archive |
| Q7 | Does cost escalation predict cancellation? | ~24 months | needs the archive, and needs cancellations to occur |
| Q8 | Do generator queues behave like transmission queues? | — | **blocked.** NYISO answers a laptop with 200 and 470,856 bytes but a GitHub runner with `202` and an empty body — a bot challenge. Local capture only; see `webprobes` row `nyiso.giq` |
| Q9 | What is the shape of delivered capital over time? | nothing | **answered, and backfilled from a single capture.** $42.5B delivered 2010–2025, peaking at $5.5B in 2025. Every in-service row carries a delivery date and a cost, so the series reaches back to 2002 without an archive — but at TODAY'S costs, so it is a revised history |
| Q10 | Does approved cost escalation reach ratepayers, and how fast? | ~12 months | needs the archive. Schedule 26 publishes indicative annual charges per pricing zone five years out; joining approved project cost to zone charges is the transmission-spend-to-bill link |
| Q11 | How much do MISO's own five-year charge projections move? | ~12 months | needs the archive. Schedule 26 is a *projection*: today's estimate of 2027–2031 charges overwrites last year's estimate of the same years, and only the current one is published |
| Q12 | Is the backfilled delivered series itself revised? | ~12 months | needs the archive. Q9 reconstructs history from today's costs; whether MISO restates a delivered project's cost after the fact is only visible across captures, and would make every backfilled series provisional |
| Q13 | Does transmission approval follow generation queue pressure? | a source | **source not yet added.** MISO's generator interconnection queue is a React app backed by a document API; the queue file itself was not found from the landing page. Until it is, generation and transmission cannot be joined |

**Q5 is the important negative result.** The obvious pitch for this repo —
"how long do transmission projects take" — is already answerable from a single
fetch, because MISO keeps the proposal cycle. Building a capture for it would
have been building an archive of something already archived. What perishes is
the *cost* and the *promise*, not the duration.

**Q13 is the only live trigger for another source.** Everything else here is
either answered, or waiting on the archive to accumulate — and waiting on time
is not a reason to widen the registry.

## What would make this worth stopping

If, after two years, `Current Cost` turns out to move for fewer than ~5% of
projects between captures, then escalation is rare enough that the annual MTEP
report covers it and this archive is redundant. That is the pre-committed exit,
written before the first capture rather than after a disappointing one.

## Two parsing traps, found while screening

**Two traps, and the second cost a wrong number before it was caught.**

*Membership in a file is not the project's status.* 169 facility rows in the
*Approved* workbook and 12 in *Under Evaluation* already carry
`M4 - Project in Service`. The files lag their own `Planning Status` column, so
any count that trusts the filename is wrong.

*The Approved workbook's grain is FACILITY, not project.* Its 3,211 rows carry
**1,497 distinct `MTEP Project ID`s**, and `Current Cost` differs across a
project's facilities in 482 of the 496 projects that have more than one — so
cost is a per-facility figure that must be summed, not deduplicated. Keying
observations on the project alone silently kept one facility's cost and
discarded the rest: $33.0B instead of $68.6B, a headline halved with no error
raised. Every count in this repo states which grain it is in.
