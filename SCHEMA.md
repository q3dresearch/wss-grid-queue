# Data shape

*Generated 2026-09-15T13:14:54Z by `wss schema` from the derived rows. Do not hand-edit — regenerate after any derive.*

**You should not need to download anything to read this.**

- **245,549 observations** across 1 partition(s), in **7 series**
  - `miso.mtep.approved` — 77,020 rows, **3211 entities**
  - `miso.mtep.in-service` — 103,660 rows, **5183 entities**
  - `miso.mtep.under-evaluation` — 11,940 rows, **597 entities**
  - `miso.schedule26.charges` — 3,774 rows, **34 entities**
  - `miso.schedule26a.mvp` — 162 rows, **18 entities**
  - `nyiso.interconnection.queue` — 28,325 rows, **2174 entities**
  - `spp.interconnection.queue` — 20,668 rows, **1043 entities**
- Raw: 7 file(s), 2,996,714 bytes on disk, 2 capture date(s), 2026-09-09 → 2026-09-14

## Sources

| source | cadence | endpoints | storage | personal data | licence |
| --- | --- | ---: | --- | --- | --- |
| `miso.mtep.approved` | monthly | 1 | git | none | MISO publishes these openly; no stated reuse restriction |
| `miso.mtep.in-service` | monthly | 1 | git | none | MISO publishes these openly; no stated reuse restriction |
| `miso.mtep.under-evaluation` | monthly | 1 | git | none | MISO publishes these openly; no stated reuse restriction |
| `miso.schedule26.charges` | monthly | 1 | git | none | MISO publishes these openly; no stated reuse restriction |
| `miso.schedule26a.mvp` | monthly | 1 | git | none | MISO publishes these openly; no stated reuse restriction |
| `nyiso.interconnection.queue` | monthly | 1 | git | parties_only | NYISO publishes this openly; no stated reuse restriction |
| `spp.interconnection.queue` | monthly | 1 | git | none | SPP publishes this openly on its operations portal; no state |

## Columns

```
series_id, entity_id, observed_at, captured_at, metric, value, unit, source_id, raw_ref, parser_version
```

`entity_id` looks like: **miso.mtep.approved** `10001:21424`, `10022:21434`, `10022:21435`; **miso.mtep.in-service** `1`, `100`, `10000`; **miso.mtep.under-evaluation** `15871`, `15873`, `15991`; **miso.schedule26.charges** `zone:AMIL`, `zone:AMMO`, `zone:ATC`; **miso.schedule26a.mvp** `mvp:1203`, `mvp:2202`, `mvp:2220`; **nyiso.interconnection.queue** `queue:0001`, `queue:0002`, `queue:0003`; **spp.interconnection.queue** `feed:spp_giq`, `generationtype:Battery/Storage`, `generationtype:Hybrid`

## Metrics

| metric | series | rows | entities | type | unit | distinct | range / samples |
| --- | --- | ---: | ---: | --- | --- | ---: | --- |
| `capacity_mw` | spp.interconnection.queue | 1,024 | 1024 | number | mw | 373 | `0.1` … `1400.0` |
| `cause_of_delay` | spp.interconnection.queue | 33 | 33 | text | text | 5 | `Affected System Study`, `GIA delayed due to Affec`, `Interim IGIA effective 3` |
| `cessation_date` | spp.interconnection.queue | 18 | 18 | text | text | 16 | `1/15/2027`, `10/1/2026`, `10/24/2025` |
| `charge_2027` | miso.schedule26.charges | 102 | 34 | number | usd | 34 | `37454.02902308053` … `97120883.87051843` |
| `charge_2028` | miso.schedule26.charges | 102 | 34 | number | usd | 34 | `50521.83779539773` … `101753939.2074353` |
| `charge_2029` | miso.schedule26.charges | 102 | 34 | number | usd | 34 | `54845.384503534566` … `103678467.68001196` |
| `charge_2030` | miso.schedule26.charges | 102 | 34 | number | usd | 34 | `55293.5855021456` … `103094525.14206819` |
| `charge_2031` | miso.schedule26.charges | 102 | 34 | number | usd | 34 | `62341.12175544913` … `101284116.80769378` |
| `charge_2032` | miso.schedule26.charges | 102 | 34 | number | usd | 34 | `62335.49679867058` … `99350323.18708508` |
| `charge_2033` | miso.schedule26.charges | 102 | 34 | number | usd | 34 | `61236.99306604616` … `97397405.30033231` |
| `charge_2034` | miso.schedule26.charges | 102 | 34 | number | usd | 34 | `60138.48933342169` … `95444487.41357955` |
| `charge_2035` | miso.schedule26.charges | 102 | 34 | number | usd | 34 | `59039.98560079724` … `93491569.5268267` |
| `charge_2036` | miso.schedule26.charges | 102 | 34 | number | usd | 34 | `57941.481868172756` … `91538651.64007382` |
| `charge_2037` | miso.schedule26.charges | 102 | 34 | number | usd | 34 | `56842.978135548285` … `89585733.75332105` |
| `charge_2038` | miso.schedule26.charges | 102 | 34 | number | usd | 34 | `55744.47440292384` … `87632815.8665682` |
| `charge_2039` | miso.schedule26.charges | 102 | 34 | number | usd | 34 | `54645.97067029941` … `85679897.97981536` |
| `charge_2040` | miso.schedule26.charges | 102 | 34 | number | usd | 34 | `53547.46693767492` … `83726980.09306271` |
| `cluster` | spp.interconnection.queue | 973 | 973 | text | text | 49 | `DIS-16-2-PQ`, `DIS-17-1-PQ`, `DISIS-2009-001-6` |
| `cluster_group` | spp.interconnection.queue | 870 | 870 | text | text | 5 | `01 NORTH`, `02 NEBRASKA`, `03 CENTRAL` |
| `columns_published` | spp.interconnection.queue | 1 | 1 | number | count | 1 | `30` … `30` |
| `commercial_operation_date` | spp.interconnection.queue | 923 | 923 | text | text | 447 | `1/1/2002`, `1/1/2005`, `1/1/2006` |
| `county` | nyiso.interconnection.queue | 2,092 | 2092 | text | text | 253 | `Alb.-Col.-Dutch.`, `Albany`, `Albany-Dutchess` |
| `current_cost` | miso.mtep.approved, miso.mtep.in-service, miso.mtep.under-evaluation | 35,928 | 8979 | number | usd | 5029 | `0.0` … `1700000000.0` |
| `demand_2027` | miso.schedule26.charges | 102 | 34 | number | mw | 34 | `126777.496` … `12004548.0` |
| `demand_2028` | miso.schedule26.charges | 102 | 34 | number | mw | 34 | `128805.93593600001` … `12196620.768000001` |
| `demand_2029` | miso.schedule26.charges | 102 | 34 | number | mw | 34 | `130866.830910976` … `12391766.700288` |
| `demand_2030` | miso.schedule26.charges | 102 | 34 | number | mw | 34 | `132960.7002055516` … `12590034.967492608` |
| `demand_2031` | miso.schedule26.charges | 102 | 34 | number | mw | 34 | `135088.07140884045` … `12791475.526972491` |
| `demand_2032` | miso.schedule26.charges | 102 | 34 | number | mw | 34 | `137249.4805513819` … `12996139.13540405` |
| `demand_2033` | miso.schedule26.charges | 102 | 34 | number | mw | 34 | `139445.47224020402` … `13204077.361570515` |
| `demand_2034` | miso.schedule26.charges | 102 | 34 | number | mw | 34 | `141676.5997960473` … `13415342.599355644` |
| `demand_2035` | miso.schedule26.charges | 102 | 34 | number | mw | 34 | `143943.42539278403` … `13629988.080945335` |
| `demand_2036` | miso.schedule26.charges | 102 | 34 | number | mw | 34 | `146246.5201990686` … `13848067.89024046` |
| `developer` | nyiso.interconnection.queue | 2,174 | 2174 | text | text | 1161 | `174 Power Global Propert`, `174 Power Global Propert`, `1st Rochdale Coop Group` |
| `end_use` | nyiso.interconnection.queue | 51 | 51 | text | text | 8 | `DAT`, `DAT-AI`, `DAT-CM` |
| `expected_isd` | miso.mtep.approved, miso.mtep.in-service, miso.mtep.under-evaluation | 35,964 | 8988 | date | date | 2874 | `2002-05-01` … `2040-12-31` |
| `fuel` | nyiso.interconnection.queue | 2,056 | 2056 | text | text | 26 | `AC`, `C`, `CC` |
| `fuel_type` | spp.interconnection.queue | 371 | 371 | text | text | 30 | `Battery`, `CC`, `CT` |
| `generation_type` | spp.interconnection.queue | 1,023 | 1023 | text | text | 7 | `Battery/Storage`, `Hybrid`, `Hydro` |
| `gross_plant` | miso.schedule26a.mvp | 54 | 18 | number | usd | 18 | `4007320.0` … `1033927001.0` |
| `has_associated_studies` | spp.interconnection.queue | 1 | 1 | text | state | 1 | `yes` |
| `has_executed_gia` | spp.interconnection.queue | 184 | 184 | text | state | 1 | `yes` |
| `has_facility_report` | spp.interconnection.queue | 57 | 57 | text | state | 1 | `yes` |
| `ifs_queue_number` | spp.interconnection.queue | 201 | 201 | text | text | 201 | `IFS-2012-002-01`, `IFS-2013-001-01`, `IFS-2013-001-02` |
| `jtiq_participant` | spp.interconnection.queue | 928 | 928 | text | text | 3 | `N/A`, `No`, `Yes` |
| `listed` | spp.interconnection.queue | 1,024 | 1024 | text | state | 1 | `yes` |
| `mvp_in_service` | miso.schedule26a.mvp | 54 | 18 | date | date | 18 | `2013-12-06` … `2024-12-31` |
| `mvp_name` | miso.schedule26a.mvp | 54 | 18 | text | name | 18 | `Adair - Ottumwa 345`, `Adair-Palmyra Tap 345 kV`, `Big Stone South to Brook` |
| `nameplate_mw` | spp.interconnection.queue | 1,024 | 1024 | number | mw | 136 | `0.0` … `1694.135` |
| `original_cod` | spp.interconnection.queue | 3 | 3 | text | text | 3 | `12/31/2004`, `3/11/2016`, `5/31/2030` |
| `peak_load_mw` | nyiso.interconnection.queue | 73 | 73 | number | text | 40 | `14.3` … `1935` |
| `place` | spp.interconnection.queue | 1,020 | 1020 | text | text | 504 | `Aberdeen`, `Abernathy`, `Abernathy County` |
| `planning_status` | miso.mtep.approved, miso.mtep.in-service, miso.mtep.under-evaluation | 35,964 | 8988 | text | status | 4 | `M1 - Proposed`, `M2 - Appendix A Approved`, `M3 - Under Construction` |
| `project_id` | miso.mtep.approved | 12,844 | 3211 | number | id | 1497 | `1900` … `51406` |
| `project_name` | nyiso.interconnection.queue | 2,176 | 2174 | text | text | 1952 | `0 Highland Lake Rd - Wal`, `1 Gig Data Center East F`, `114 Hartley Rd-Goshen` |
| `project_status` | nyiso.interconnection.queue | 2,148 | 2146 | number | text | 12 | `0` … `15` |
| `proposed_cod` | nyiso.interconnection.queue | 329 | 329 | text | text | 53 | `01-2027`, `01-2028`, `01-2029` |
| `proposed_in_service` | nyiso.interconnection.queue, spp.interconnection.queue | 1,157 | 1157 | text | text | 432 | `01-2027`, `01-2028`, `01-2029` |
| `proposed_sync` | nyiso.interconnection.queue | 176 | 176 | text | text | 49 | `01-2027`, `01-2028`, `01-2030` |
| `queue_state` | nyiso.interconnection.queue | 2,176 | 2174 | text | state | 7 | `active`, `active_cluster`, `affected_system` |
| `requested_at` | nyiso.interconnection.queue, spp.interconnection.queue | 3,179 | 3179 | text | text | 1619 | `1/1/2010`, `1/1/2016`, `1/1/2017` |
| `requested_deliverability_mw` | spp.interconnection.queue | 1,024 | 1024 | number | mw | 69 | `0.0` … `1400.0` |
| `requested_injection_mw` | spp.interconnection.queue | 1,024 | 1024 | number | mw | 75 | `0.0` … `1400.0` |
| `requests_listed` | spp.interconnection.queue | 19 | 19 | number | count | 17 | `1` … `1024` |
| `rows_with_cessation_date` | spp.interconnection.queue | 1 | 1 | number | count | 1 | `18` … `18` |
| `rows_with_withdrawal_date` | spp.interconnection.queue | 1 | 1 | bool | count | 1 | `0` |
| `service_type` | spp.interconnection.queue | 1,010 | 1010 | text | text | 4 | `ER`, `ER/NR`, `ERIS` |
| `state` | nyiso.interconnection.queue, spp.interconnection.queue | 3,192 | 3192 | text | text | 23 | `AR`, `CO`, `CT` |
| `status` | spp.interconnection.queue | 1,024 | 1024 | text | text | 10 | `DISIS STAGE`, `ERAS`, `FACILITY STUDY STAGE` |
| `status_updated` | nyiso.interconnection.queue | 2,068 | 2066 | text | text | 263 | `1/31/20`, `1/31/25`, `10/31/2025` |
| `studies_available` | nyiso.interconnection.queue | 256 | 256 | text | text | 30 | `FES`, `FES, FS`, `FES, SIS` |
| `submitting_to` | miso.mtep.approved, miso.mtep.in-service, miso.mtep.under-evaluation | 35,956 | 8986 | text | name | 60 | `1803 ELECTRIC COOPERATIV`, `AEP Indiana Michigan Tra`, `AMEREN ILLINOIS` |
| `substation` | spp.interconnection.queue | 990 | 990 | text | text | 725 | `115 kV Fort Dodge Substa`, `115kV Monolith Substatio`, `115kV Strandahl sub` |
| `summer_mw` | nyiso.interconnection.queue, spp.interconnection.queue | 3,059 | 3047 | text | text | 801 | `0`, `0.0`, `0.1` |
| `target_cycle` | miso.mtep.approved, miso.mtep.in-service, miso.mtep.under-evaluation | 35,964 | 8988 | text | cycle | 23 | `MTEP03`, `MTEP05`, `MTEP06` |
| `transmission_owner` | spp.interconnection.queue | 1,006 | 1006 | text | text | 58 | `AECC`, `AECI`, `AEP` |
| `utility` | nyiso.interconnection.queue | 2,090 | 2090 | text | text | 83 | `CHG&E`, `CHGE`, `CHGE/NM-NG/NYSEG` |
| `variance_2027` | miso.schedule26.charges | 102 | 34 | number | usd | 34 | `-4152819.4727273285` … `2864761.5680387616` |
| `variance_2028` | miso.schedule26.charges | 102 | 34 | number | usd | 34 | `-3819524.6823871285` … `2991050.323114872` |
| `variance_2029` | miso.schedule26.charges | 102 | 34 | number | usd | 34 | `-629047.041574806` … `3031833.212717846` |
| `variance_2030` | miso.schedule26.charges | 102 | 34 | number | usd | 34 | `-659400.2530492842` … `2983617.81842418` |
| `variance_2031` | miso.schedule26.charges | 102 | 34 | number | usd | 34 | `-530714.539239198` … `3111677.1130361557` |
| `variance_2032` | miso.schedule26.charges | 102 | 34 | number | usd | 34 | `-555802.2153580189` … `3054398.6035306454` |
| `variance_2033` | miso.schedule26.charges | 102 | 34 | number | usd | 34 | `-604918.1019883603` … `2968159.7852281183` |
| `variance_2034` | miso.schedule26.charges | 102 | 34 | number | usd | 34 | `-654033.9886188507` … `2881920.9669255167` |
| `variance_2035` | miso.schedule26.charges | 102 | 34 | number | usd | 34 | `-703149.8752491772` … `2795682.148622766` |
| `variance_2036` | miso.schedule26.charges | 102 | 34 | number | usd | 34 | `-752265.7618795186` … `2709443.33032012` |
| `variance_2037` | miso.schedule26.charges | 102 | 34 | number | usd | 34 | `-801381.6485100016` … `2623204.5120176077` |
| `variance_2038` | miso.schedule26.charges | 102 | 34 | number | usd | 34 | `-850497.5351403579` … `2536965.6937149167` |
| `variance_2039` | miso.schedule26.charges | 102 | 34 | number | usd | 34 | `-899613.4217707813` … `2450726.8754124343` |
| `winter_mw` | nyiso.interconnection.queue, spp.interconnection.queue | 2,775 | 2775 | text | text | 735 | `0`, `0.0`, `0.1` |
| `zone` | nyiso.interconnection.queue | 1,989 | 1989 | text | text | 41 | `A`, `A, B`, `A,E,J` |

## Partitions

- `derived/observations/2026-09.csv.gz`
