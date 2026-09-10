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
| Q6 | Which transmission owners slip worst, and by how much? | ~12 months | **partly answered.** Who is late *today* is measurable: 24 of 50 owners with a live facility have one past its date — METC $192M, ITC $153M, American Transmission $128M. *By how much they slipped* still needs the archive, because the promise is overwritten each time it moves |
| Q7 | Does cost escalation predict cancellation? | ~24 months | needs the archive, and needs cancellations to occur |
| Q8 | Do generator queues behave like transmission queues? | ~12 months | **source added 2026-09-10.** NYISO is captured locally — a GitHub runner still gets `202` with an empty body. 96 active projects, 1,452 withdrawn, 149 delivered. On the delivered sheet the promised date is erased on **147 of 149**, which is MISO's `Current Cost` overwrite in a different column |
| Q9 | What is the shape of delivered capital over time? | nothing | **answered, and backfilled from a single capture.** $42.5B delivered 2010–2025, peaking at $5.5B in 2025. Every in-service row carries a delivery date and a cost, so the series reaches back to 2002 without an archive — but at TODAY'S costs, so it is a revised history |
| Q10 | Does approved cost escalation reach ratepayers, and how fast? | ~12 months | **base measured, join needs the archive.** 2027 indicative charges total $443M across 34 pricing zones, and three of them — METC, ATC, NSP — carry 61%. Whether escalation flows into those numbers needs both series over time |
| Q11 | How much do MISO's own five-year charge projections move? | ~12 months | needs the archive. Schedule 26 is a *projection*: today's estimate of 2027–2031 overwrites last year's estimate of the same years. It ships a `Variance` sheet, but the caption never says variance *from what* — captured vintages settle that, guessing does not |
| Q12 | Is the backfilled delivered series itself revised? | ~12 months | needs the archive. Q9 reconstructs history from today's costs; whether MISO restates a delivered project's cost after the fact is only visible across captures, and would make every backfilled series provisional |
| Q13 | Does transmission approval follow generation queue pressure? | nothing | **answered — no, and the source that was missing has been found.** `https://www.misoenergy.org/api/giqueue/getprojects` returns 3,833 projects as 2.25 MB of JSON, no key, no auth. Queue GW and MTEP dollars approved correlate at **r = 0.73 in levels and ≈ 0 year-on-year** (−0.01 at lag 0, +0.19 at lag 1, −0.28 at lag 2). The level figure is a shared decade-long trend, not a response. Stable under both reconstruction assumptions — see below |

**Q5 is the important negative result.** The obvious pitch for this repo —
"how long do transmission projects take" — is already answerable from a single
fetch, because MISO keeps the proposal cycle. Building a capture for it would
have been building an archive of something already archived. What perishes is
the *cost* and the *promise*, not the duration.

**Q13 is the only live trigger for another source.** Everything else here is
either answered, or waiting on the archive to accumulate — and waiting on time
is not a reason to widen the registry.

## Who cares, and what they would do differently

A question with no named party who would act on the answer is trivia, and
trivia does not justify a job that runs for years. Each row names a decision,
not a sector.

### Q13 in full: the queue mostly archives itself, and the answer is no

The queue file was never missing — it is behind the interactive queue page at
`/api/giqueue/getprojects`, plain JSON, no key. 3,833 projects, 27 fields.

**It is largely self-archiving, which makes this a larder question rather than a
capture.** MISO retains dead projects with their dates: `queueDate` on 99.8% of
rows and `withdrawnDate` on **2,124 of the 2,146 withdrawn (99%)**. So the queue
population at a past date can be rebuilt from a single download, and no listener
is needed to answer Q13.

**With one hole, measured rather than assumed.** Completions are *not* dated:
only **226 of 554 `Done` projects carry a `doneDate`**, so 330 finished projects
cannot be placed in time. The reconstruction was therefore run twice — once
treating them as never having left (biased upward, worse the further back you
go) and once excluding them entirely. The answer does not move:

| | lag 0 | lag 1 | lag 2 |
| --- | --- | --- | --- |
| levels, undated kept | +0.74 | +0.72 | +0.55 |
| levels, undated excluded | +0.73 | +0.69 | +0.48 |
| **year-on-year, undated kept** | **−0.04** | **+0.21** | **−0.23** |
| **year-on-year, undated excluded** | **−0.01** | **+0.19** | **−0.28** |

**So: no.** Queue pressure and transmission approval both rose through the
decade, and that shared trend is the whole of the r ≈ 0.73. Once each series is
reduced to its year-on-year change, nothing survives at any lag out to two
years. Transmission approval does not track queue pressure on an annual cadence.

**Do not quote a GW figure from this reconstruction.** Counting today's `Active`
rows gives 1,034 projects and 221.8 GW of `summerNetMW`, while MISO itself
published 944 projects and 174 GW in May 2026. The gap is unexplained — a
different date, or a different capacity basis among `summerNetMW`, `dp1ErisMw`
and `dp1NrisMw`. The correlation above is unaffected because it is scale-free,
but the level is not trustworthy enough to print.

**What still perishes here**, and why it is recorded rather than captured: the
completion dates that are missing on 59% of `Done` projects, and `studyPhase`
(1,145 at GIA, 900 Phase 1, 509 Phase 2, 253 Phase 3) which carries no
transition dates at all. Neither has a question demanding it today. The snapshot
this analysis used is kept at
`webprobes/screening/miso-giqueue-2026-09-10.json.gz` so the numbers can be
rechecked without re-fetching.


| who | questions | the decision it changes |
| --- | --- | --- |
| **State commission staff and consumer advocates** (e.g. Michigan PSC, Minnesota DOC) | Q1, Q10, Q11 | whether to contest a transmission rate filing. Today a utility's cost figure arrives with no published history to check it against; an archive turns "this project now costs X" into "this project cost Y when it was approved" |
| **Industrial energy buyers and data-centre siting teams** | Q10 | which pricing zone to build in. Three zones carry 61% of the 2027 charge and the projections move — siting on today's number without knowing how it drifts is a five-year bet on a figure nobody archives |
| **Transmission developers and EPC contractors** | Q6, Q3 | where to bid, and whose schedule to believe. METC has $192M behind schedule across 21 facilities while ITC Midwest has 80 late facilities for half the money — those are different counterparties |
| **Generation developers with queued projects** | Q13 | whether the transmission they depend on will actually arrive. This is the join that does not exist yet, and the reason Q13 is the one live `source not yet added` |
| **Energy journalists and grid analysts** | Q2, Q9, Q7 | what to write, and whether a cancellation was foreseeable. Cost escalation before a cancellation is only visible to someone who kept the earlier numbers |
| **MISO stakeholders in the MTEP process itself** | Q4 | which proposals to support. The conversion rate from *Under Evaluation* to approved is not published, and 597 projects worth $17.0B are in that state right now |

**Who this is NOT for.** Anyone who needs settlement-grade numbers. MISO states
plainly that these values are *"indicative only … not intended to be relied upon
for settlement or ratemaking purposes."* This archive is evidence about how
estimates move, not a billing record.

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
