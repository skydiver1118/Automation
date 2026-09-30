from pathlib import Path
import json,hashlib,sys,copy,math
from datetime import datetime,timezone
import os
A=Path(__file__).resolve().parents[2]; D=Path(os.environ['V22_EVIDENCE_ROOT'])
(A/'v22/research').mkdir(parents=True,exist_ok=True)
sys.path.insert(0,str(A))
from v22_pipeline import financial_basis,canonical
S=json.loads((A/'monitoring/runs/2026-09-30T013246Z-weekly.json').read_text()); BY={x['ticker']:x for x in S['stocks']}
NOW='2026-09-30T03:09:21+00:00'; CUTOFF='2026-09-29' # Actual review time, not the later rebuild time
def record(t, facts, growth, economics, funding, risk, catalyst, cases=None, model='equity_pe', hold=None, extra=None):
 return dict(ticker=t,facts=facts,growth_rationale=growth,economics_rationale=economics,funding_assessment=funding,risk=risk,catalyst=catalyst,cases=cases,model=model,critical_gaps=hold or [],extra=extra or [])
# Five-year revenue endpoints (USD billions), common net margins, terminal P/E,
# and cumulative economic share changes. These are explicitly analyst scenarios,
# not issuer guidance or calibrated probabilities. Endpoint growth is NOT a claim
# that every intervening year grows at a constant rate.
REVIEWS=[
record('ETN',
 'Q2 revenue $8.531B, organic growth 14%, and electrical backlog growth 43%. The June 11 Mobility/Dana agreement values Mobility at about $5.1B enterprise value, includes an approximately $1.1B cash distribution to Eaton, and allows either a spin-off or split-off.',
 'Electrical and aerospace exposure supports secular growth, but projecting unchanged consolidated revenue across the announced Mobility separation would mix different business perimeters.',
 'Post-separation operating margins, share count after a possible exchange offer, and the value distributed to shareholders must be modeled separately.',
 'NSI is not an Eaton acquisition; Eaton has its own Boyd Thermal/Ultra PCS transactions and approximately $21B balance-sheet debt. Do not assume the Mobility cash distribution is already received.',
 'A simple ETN-only fivefold share-price model can omit distributed Dana equity or misstate the denominator after a split-off.',
 'Final transaction election, post-separation revenue/earnings and economic-share bridge.',
 hold=['Critical model-perimeter gap: final Mobility spin-off versus split-off treatment and pro forma shareholder-value bridge are not reconciled.'],
 extra=[('ETN_Q2','https://www.sec.gov/Archives/edgar/data/1551182/000155118226000027/etn06302026exhibit99.htm','2026-07-31'),('ETN_DANA','https://www.eaton.com/us/en-us/company/news-insights/news-releases/2026/eaton-mobility-group-enters-agreement-to-combine-with-dana.html','2026-06-11')]),
record('ZETA',
 'Q2 revenue $442.766M includes $48.1M Marigold contribution; GAAP net income $8.173M. FY2026 revenue guidance $1.811–1.824B and adjusted EBITDA $404.1–406.3M. The earlier 2028 framework targets at least $2.3B revenue.',
 'Five-year revenue endpoints of $2.5/$4.0/$6.0B bracket post-2028 deceleration, sustained platform growth, and a strong AI-adoption outcome. None extrapolates acquisition-inclusive Q2 growth unchanged for five years.',
 'Common net margins of 5/13/18% are after recurring stock compensation, interest and tax, below the 25% adjusted EBITDA ambition. Terminal P/E 18/25/30 is a valuation stress assumption, not an observed peer multiple.',
 'June cash about $310M versus debt about $197M and positive operating cash generation support internal development. Cumulative shares +10/+20/+35% allow SBC/acquisition funding; no future acquisition revenue is purchased for free in the model.',
 'Customer-data regulation, competitive platforms, acquisition integration and SBC can prevent adjusted profitability reaching common shareholders.',
 'Organic retention/revenue and common-earnings conversion; recheck 2028 framework versus actual results.',
 [[2.5,.05,18,.10],[4,.13,25,.20],[6,.18,30,.35]],
 extra=[('ZETA_Q2','https://investors.zetaglobal.com/news/news-details/2026/Zeta-Global-Reports-20th-Consecutive-Beat-and-Raise-Quarter-Achieves-the-Rule-of-64-and-Generates-Positive-GAAP-Net-Income-in-2Q26/default.aspx','2026-08-04'),('ZETA_FRAMEWORK','https://investors.zetaglobal.com/news/news-details/2026/Zeta-Global-Reports-18th-Straight-Beat-and-Raise-Quarter-and-Record-Full-Year-2025-Results/default.aspx','2026-02-24')]),
record('HUBB',
 'Q2 revenue $1.7118B and organic growth 10%; FY2026 adjusted EPS outlook $20.25–20.55. The approximately $3B NSI acquisition materially increased debt.',
 'Five-year revenue $7.5/$10/$13B brackets utility replacement demand normalizing, continued grid investment, and stronger electrification plus integration. Starting TTM includes only the acquired periods already recognized.',
 'Common margins 12/16/19% stress integration/interest costs against demonstrated operating profitability. Terminal P/E 18/23/28 assumes a mature industrial, not software economics.',
 'June cash/investments about $395M and debt about $5.56B make post-acquisition deleveraging important. Flat shares in bear/base and +5% in bull avoid assuming debt-funded buybacks.',
 'Utility order timing, acquisition leverage and cost inflation; favorable sector demand does not remove starting valuation risk.',
 'NSI cash conversion, organic grid demand and leverage reduction.',
 [[7.5,.12,18,0],[10,.16,23,0],[13,.19,28,.05]],
 extra=[('HUBB_Q2','https://hubbell.gcs-web.com/news-releases/news-release-details/hubbell-reports-second-quarter-2026-results','2026-07-28')]),
record('VST',
 'Q2 ongoing adjusted EBITDA $1.767B; FY2026 outlook $6.8–7.6B. Free cash flow before growth is not CFO less all capex. September 24 closed $1.5B junior notes intended in part to redeem preferred securities later in 2026.',
 'Revenue endpoints $20/$27/$35B represent normalized generation/retail outcomes, not a direct capitalization of spot electricity prices. Hedge roll-off and contracts delay realization.',
 'Common net margins 7/13/17% include interest, tax, depreciation and any remaining preferred distributions. P/E 12/17/21 captures commodity/regulatory cyclicality. Debt is not subtracted twice from this common-equity model.',
 'The 7.0% and 7.25% note coupons are real financing costs. No preferred redemption is assumed completed on September 29. Five-year shares 0/−10/−15% assumes only internally funded buybacks after growth spending and debt service; that is a scenario, not a promise.',
 'Fuel/power basis risk, hedge timing, leverage, preferred claims and nuclear/regulatory costs.',
 'Actual preferred redemptions, all-capex FCF, contracted demand and hedge realization.',
 [[20,.07,12,0],[27,.13,17,-.10],[35,.17,21,-.15]],
 extra=[('VST_Q2','https://investor.vistracorp.com/2026-08-07-Vistra-Reports-Second-Quarter-2026-Results','2026-08-07')]),
record('CRMD',
 'Q2 total revenue and grants $101.931M, including approximately $66.1M DefenCath and $35.8M acquired Melinta products. FY2026 revenue outlook $325–345M is below the peak trailing run rate.',
 'Endpoints $250/$450/$750M deliberately allow the TDAPA reimbursement transition to reduce near-term revenue. Base recovery relies on utilization and the existing product portfolio, not undisclosed clinical success.',
 'Common net margins 10/22/30% are below the high adjusted EBITDA outlook after taxes, interest and amortization. P/E 10/15/20 recognizes reimbursement/product concentration.',
 'June cash/investments about $257M and debt about $145M support the current products, but diluted weighted-average shares exceed basic common shares. Future dilution +10/+15/+25% covers options, awards and further funding without treating June cash as a price floor.',
 'Reimbursement reset and product concentration can invalidate the apparent low earnings multiple.',
 'Post-TDAPA price/utilization and actual common-earnings/FCF conversion.',
 [[.25,.10,10,.10],[.45,.22,15,.15],[.75,.30,20,.25]],
 extra=[('CRMD_Q2','https://cormedix.com/cormedix-therapeutics-reports-second-quarter-2026-financial-results-and-provides-business-update/','2026-08-13')]),
record('AXTI',
 'Q2 revenue $47.589M, gross margin about 44.9%, common net income $11.084M. Diluted weighted-average shares were 63.474M versus 43.710M a year earlier.',
 'Revenue $180/$400/$800M assumes very different substrate shipment ramps; the base is already several times trailing sales. AI optical demand does not establish a guaranteed AXT order.',
 'Common margins 5/14/20% allow substrate cycles, minority ownership, taxes and manufacturing reinvestment. P/E 15/23/28 deliberately normalizes unusually strong quarter margins.',
 'Existing capital raising is already in today’s share base. Additional +10/+20/+35% dilution covers future capacity/SBC; larger capex could require more and invalidate these endpoints.',
 'China production, export licenses, customer concentration and starting market value versus small revenue.',
 'Permits, paid substrate shipments, sustainable common margins and per-share growth.',
 [[.18,.05,15,.10],[.4,.14,23,.20],[.8,.20,28,.35]],
 extra=[('AXTI_Q2','https://investors.axt.com/Investors/news/news-details/2026/AXT-Inc--Announces-Second-Quarter-2026-Financial-Results/default.aspx','2026-07-30')]),
record('KTOS',
 'Q2 revenue $458.8M: 19.1% organic growth versus 30.5% total growth. FY2026 revenue outlook $1.750–1.810B, adjusted EBITDA $173–176M. The roughly $15B bid pipeline is not funded backlog.',
 'Five-year revenue $2.3/$3.6/$5.4B assumes varying conversion of funded defense programs and production scaling, not automatic capture of the bid pipeline.',
 'Common margins 5/10/14% require significant improvement from current low GAAP profitability. P/E 18/24/28 represents execution-sensitive defense growth.',
 'Q2 CFO −$11M and capex $17.2M imply −$28.2M conventional FCF; issuer adjusted FCF includes asset-sale proceeds. Shares +10/+15/+25% accommodate production investment; cash generation must improve for base/bull funding to work.',
 'Award delays, production margins, dilution and investment before customer funding.',
 'Funded awards, propulsion/unmanned output and CFO after all capex.',
 [[2.3,.05,18,.10],[3.6,.10,24,.15],[5.4,.14,28,.25]],
 extra=[('KTOS_Q2','https://www.kratosdefense.com/newsroom/kratos-reports-second-quarter-2026-financial-results','2026-08-04')]),
record('AVAV',
 'The September release covers the quarter ended August 1: revenue $480.490M, operating loss $10.871M. FY2027 outlook remains $2.125–2.225B revenue and $305–325M adjusted EBITDA. New TTM revenue is $2.002659B, not the old April fiscal-year total.',
 'Five-year revenue $2.7/$4.5/$6.5B scales the post-BlueHalo perimeter at conservative/base/strong rates. The prior 133% acquisition-inclusive quarter is not extrapolated as organic growth.',
 'Common net margins 6/10/14% remain below adjusted EBITDA margins after financing, tax, stock compensation and amortization. P/E 18/24/28 captures program and integration risk.',
 'August cash/investments $580.227M and debt/leases about $850.823M; cover-page common shares 50.820702M. Future +5/+10/+20% dilution is incremental, not a repeat of historical acquisition issuance.',
 'Integration, award timing and reported-to-adjusted earnings differences.',
 'Integration cash flow, funded backlog conversion and unchanged/raised guidance.',
 [[2.7,.06,18,.05],[4.5,.10,24,.10],[6.5,.14,28,.20]]),
record('EVLV',
 'Q2 revenue $43.753M, ARR $132.7M, net loss $9.298M and adjusted EBITDA $4.4M. FY2026 revenue guidance $180–185M. The issuer’s long-term framework discusses roughly 25% revenue CAGR through 2031.',
 'Endpoints $280/$550/$800M stress slower growth, broadly delivering the stated long-term direction, and faster adoption. ARR and upfront purchase-subscription revenue are not interchangeable.',
 'Common margins 3/12/18% are below aspirational adjusted EBITDA economics because SBC, legal costs, interest and taxes remain real. P/E 15/23/28 is a scenario valuation range.',
 'Unrestricted June cash plus short-term investments about $62.6M, less than the headline balance including restricted funds. Shares +15/+25/+40% allow funding and SBC while profitability develops.',
 'Reporting history, competitive detection products, retention, legal liabilities and customer-deployment economics.',
 'Recurring retention, reliable reporting and sustainable common earnings.',
 [[.28,.03,15,.15],[.55,.12,23,.25],[.8,.18,28,.40]],
 extra=[('EVLV_Q2','https://ir.evolvtechnology.com/news/press-releases/detail/286/evolv-technology-reports-second-quarter-financial-results','2026-08-11')]),
record('BKSY',
 'Q2 revenue about $33.3M, including $24.507M space-based intelligence/AI services. FY2026 outlook $130–150M revenue, $12–24M adjusted EBITDA and $50–60M capex. September 14 filing reports annual-meeting votes rather than new financing.',
 'Revenue $180/$400/$850M brackets slower constellation adoption, recurring-service scaling and a large international contract ramp. Unfunded contract options are not immediate annual revenue.',
 'Common margins 0/12/20% deduct satellite depreciation, stock compensation, financing and tax. The zero-margin bear is an earnings-supported value stress, not proof of zero liquidation or IP value. P/E 15/23/28.',
 'Recent $150M ATM proceeds added about 3.6M shares and are already historical financing. Future +25/+40/+55% dilution covers constellation replacement and expansion; productive capex includes satellite work in process.',
 'Launch failure, satellite replacement, government concentration and continued funding before cash conversion.',
 'Gen-3 service utilization and FCF after satellite capex.',
 [[.18,0,15,.25],[.4,.12,23,.40],[.85,.20,28,.55]],
 extra=[('BKSY_Q2','https://ir.blacksky.com/news-events/press-releases/news-details/2026/BlackSky-Reports-Second-Quarter-2026-Results/default.aspx','2026-08-06')]),
record('AMPX',
 'Q2 revenue $34.032M and gross margin 27%; FY2026 guidance at least $140M revenue, at least 28% gross margin and capex under $10M. September award ceiling $75M is not cash or revenue already earned; initial obligation is approximately $22M.',
 'Endpoints $220/$600/$1,400M bracket qualification delays, repeat defense/drone orders and a major manufacturing ramp. The >$100M multi-year Stark opportunity and $24M drone order are not each repeated every year.',
 'Common margins 3/12/18% stay below current gross margins after operating costs, SBC, interest and tax. Terminal P/E 15/23/30 requires demonstrated profitable growth, not cell-specification claims alone.',
 'Contract manufacturing reduces owned-fab capex. The government agreement has milestone-acceptance and termination risk and no company cost share; do not count its full ceiling as funding received. Shares +15/+25/+45% cover working capital, awards and expansion.',
 'Qualification/production execution, customer concentration and price competition.',
 'Repeat paid shipments, accepted award milestones and conventional FCF.',
 [[.22,.03,15,.15],[.6,.12,23,.25],[1.4,.18,30,.45]],
 extra=[('AMPX_Q2','https://ir.amprius.com/news-events/press-releases/detail/172/amprius-technologies-reports-second-quarter-2026-financial-results-and-recent-business-highlights','2026-08-06')]),
record('SSII',
 'Q2 revenue about $13.94M and net loss about $2.66M. The September update reports 238 installed systems as of September 8 and 14,103 procedures. European/US regulatory milestones are plans, not approvals.',
 'Revenue endpoints $100/$250/$600M depend on installed-base utilization and progressively broader geographic adoption. The bull case explicitly requires successful regulatory/commercial expansion.',
 'Common margins 0/10/18% and P/E 15/25/30 include service/training expense, R&D, financing and tax. An earnings-zero bear does not value possible residual cash or patents.',
 'Limited liquidity, an overdraft/leases and prior going-concern discussion prevent a debt-free interpretation. Future shares +40/+50/+60% deliberately budget financing; successful capital access is conditional, not secured by this model.',
 'Regulatory timing, low starting scale, cash runway, training and larger surgical-system competitors.',
 'Paid installations/utilization, cash resources and actual regulatory decisions.',
 [[.10,0,15,.40],[.25,.10,25,.50],[.60,.18,30,.60]]),
record('TSSI',
 'Q2 revenue $35.141M is affected by lower pass-through procurement, while integration is the higher-value activity. Trailing consolidated revenue $193.277M; Q2 operating income about $2.129M.',
 'Endpoints $200/$450/$800M model consolidated revenue with shifting integration/service mix; do not extrapolate procurement volume as recurring high-margin service growth.',
 'Common margins 2/6/9% and P/E 12/18/22 allow low-margin procurement, factoring fees, taxes and customer concentration. One-time prior tax benefits are not normalized earnings.',
 'June cash about $67.7M and debt about $38.8M support operations, but working-capital and facility capex consume cash. Shares +5/+15/+30% budget capacity/working-capital funding without free acquisitions.',
 'Dominant-customer exposure, working capital and inconsistent historical factoring-fee classifications.',
 'Integration margins, collections and growth funded without disproportionate dilution.',
 [[.20,.02,12,.05],[.45,.06,18,.15],[.80,.09,22,.30]],
 extra=[('TSSI_Q2','https://www.nasdaq.com/press-release/tss-reports-second-quarter-2026-financial-results-2026-08-13','2026-08-13')]),
record('WULF',
 'Q2 total revenue $44.767M included $31.9M HPC. The Anthropic agreement covers approximately 401MW over 20 years; roughly $19B is aggregate contractual revenue, not annual revenue.',
 'Year-five revenue $0.6/$1.6/$3.0B varies commissioning and additional tenant capacity. Base exceeds the simple annual average of the disclosed long contract; bull requires substantial new funded projects.',
 'Common net margins 5/20/30% include interest, depreciation, stock compensation, tax and noncontrolling interests. P/E 12/18/22 avoids calling pre-depreciation gross profit net earnings.',
 'June cash about $2.62B and debt/leases about $5.24B precede future construction needs. Shares +25/+35/+45% assume significant equity participation; funding and tenant acceptance are conditions, not guaranteed future profits.',
 'Concentrated tenants, construction timing, GPU/customer credit and leverage.',
 'Funded delivery, customer acceptance and common-share cash returns.',
 [[.6,.05,12,.25],[1.6,.20,18,.35],[3,.30,22,.45]],
 extra=[('WULF_Q2','https://investors.terawulf.com/news-events/press-releases/detail/144/terawulf-reports-second-quarter-2026-results','2026-08-05')]),
record('IREN',
 'FY2026 recognized revenue $707.007M includes $128.8M AI Cloud. $4B contracted ARR is not recognized annual revenue. Horizon 1 was accepted by Microsoft. June unrestricted cash $5.895591B and debt/leases $7.839526B form the starting financing bridge.',
 'Year-five revenue $3/$12/$20B assumes stalled, substantial, or very strong AI commissioning. The base/bull exceed currently operating revenue and require new funded capacity. Equivalent CAGR is not the expected path during the mining-to-AI transition.',
 'Normalized EBITDA margins 35/55/65% and EV/EBITDA 8/12/14 are conditional infrastructure assumptions after recurring SBC and operating costs. Capex is not ignored: explicit cumulative CFO/capex/equity budgets determine terminal debt, deducted once.',
 'Five-year capex $18/$60/$80B and cumulative CFO $5/$22/$35B plus new common cash $3/$8/$11B are analyst funding scenarios. Additional funding/fees $0.25/$0.5/$0.75B. Ending net debt is calculated from the starting $1.943935B, not assumed zero. Total dilution +35/+50/+70% includes non-cash awards; NVIDIA rights are not cash already received. Future financing is not committed merely because the model balances.',
 'Funding at scale, customer acceptance, hardware replacement and dilution. Noncash mining impairments are not recurring AI cash losses, but actual capital destruction cannot be wished away.',
 'Recognized AI revenue, accepted capacity, financing terms and returns per economic share.',
 [[3,.35,8,.35],[12,.55,12,.50],[20,.65,14,.70]],model='enterprise_ebitda',
 extra=[('IREN_FY26','https://www.sec.gov/Archives/edgar/data/1878848/000187884826000052/iren-20260630.htm','2026-08-27'),('IREN_FINANCE','https://irisenergy.gcs-web.com/news-releases/news-release-details/iren-closes-365bn-investment-grade-gpu-financing','2026-06-01'),('IREN_ACCEPTED','https://iren.gcs-web.com/news-releases/news-release-details/iren-delivers-horizon-1-microsoft-and-achieves-nvidia-exemplar','2026-08-13')]),
record('RGTI',
 'Q2 revenue $5.138M and operating loss $28.062M; cash/securities approximately $541M. September CHIPS agreement includes 7,739,938 common shares and up to $100M funding; later tranches are conditional.',
 'Year-five sales $40/$200/$800M already require major scaling from $13.353M trailing revenue. Contracts for research systems do not establish broad useful quantum advantage.',
 'EBITDA margin 0/10/30% and EV/EBITDA 10/20/25 are optionality scenarios, not earnings already demonstrated. Terminal net cash is retained after the modeled cash burn, unlike a P/E-only zero-earnings calculation.',
 'Economic reference adds the disclosed 7,739,938 government shares to the cover-page 333,768,747 shares. Five-year capex $150/$250/$400M and cumulative CFO −$300/−$200/−$100M stress continued R&D. New common cash $0/$100/$250M; total dilution +10/+20/+35%. The full $100M award is not booked as received funding.',
 'Technical commercialization, intense competition, cash burn and enormous expectations relative to revenue.',
 'Independent useful-computation evidence and repeat paid commercial revenue.',
 [[.04,0,10,.10],[.20,.10,20,.20],[.80,.30,25,.35]],model='enterprise_ebitda'),
record('RR',
 'Q2 revenue $1.373M; June cash plus short-term investments $339.595M. September contract calls for deployment of 200 DUST-E robots over five years but does not disclose a revenue amount.',
 'Five-year sales $15/$60/$200M require repeat paid commercial deployment beyond the disclosed unit count; the contract is not valued as 200 times an invented selling price.',
 'EBITDA margins 0/10/20% and EV/EBITDA 8/15/20 test whether operating value emerges. Terminal net cash is retained after R&D and productive capex; a cash balance is not a guaranteed stock-price floor.',
 'Starting debt/leases $0.629M less $339.595M liquid resources. Five-year capex $60/$100/$150M and CFO −$150/−$100/−$50M imply cash burn before scale. No new cash-equity proceeds assumed; shares +10/+20/+35% budget awards. A separate $5/$3/$1M terminal warrant/other-claim reserve is a cash-settlement assumption, not a second conversion-share deduction.',
 'Small sales, unproven demand, execution and capital allocation; funding can be consumed before profitable scale.',
 'Actual recognized deployment revenue, customer collections and margins.',
 [[.015,0,8,.10],[.060,.10,15,.20],[.200,.20,20,.35]],model='enterprise_ebitda'),
]
# Explicit dispositions for the remaining names. Completing a review means identifying
# a real blocker, not filling it with an invented number.
HELD={
'NBIS':('Q2 revenue $582.3M. August financing added $5.75B original-principal convertibles; an $800M note exchange involved about 15.8M Class A shares. The June share base cannot automatically serve as the September fully reconciled economic denominator.', 'Resolve post-August economic shares, note accretion/cash-versus-share settlement and net proceeds before a common-equity scenario. AGM voting eligibility is not a current outstanding-share count.', 'Power/cloud demand is strong, but funding, acceptance and terminal common claims dominate per-share value.', 'Updated post-financing cap table and cash/debt bridge.', [('NBIS_CLOSE','https://nebius.com/newsroom/nebius-group-announces-closing-of-private-offering-of-convertible-senior-notes-with-aggregate-gross-proceeds-of-approximately-5-75-billion','2026-08-24'),('NBIS_TERMS','https://www.sec.gov/Archives/edgar/data/1513845/000110465926098924/tm2623617d1_ex99-1.htm','2026-08-20')]),
'FIGR':('Kiavi closed in September after the June financial statements; approximately $590M net cash consideration and $600M July notes change the funding and business perimeter.', 'Missing combined pro forma common earnings, cash/debt/shares and a finance-company-specific valuation bridge. The normal industrial EBITDA/revenue model is not adequate.', 'Credit and funding/loan-sale economics differ from software or industrial gross margins.', 'Post-Kiavi combined financial disclosures.', []),
'RKLB':('Launch execution and funded space-systems demand are real; Neutron remains a development/capital-spending program. Headline growth includes acquisition effects.', 'Required comparable acquisition-adjusted growth remains unresolved under the existing critical-data policy. No current scenario score until that review is completed.', 'Vehicle development, cash spending and high expectations create asymmetric execution risk.', 'Separate acquired and organic revenue and reconcile Neutron funding milestones.', []),
'GRRR':('H1 revenue $78.361M and gross profit $3.844M imply approximately 4.9% gross margin. July convertible financing follows the interim cash/debt date.', 'Missing current convertible/derivative/economic-share bridge and comparable financial perimeter; do not allocate half-year cash flow into invented quarters.', 'Receivables, thin gross profit and funding outweigh a headline high revenue-growth percentage.', 'Collections and a post-July capital-claims reconciliation.', []),
'QBTS':('H1 bookings $35.5M and RPO $40.7M are not H1 revenue of about $5.9M. Quantum Circuits acquisition changes the revenue/cost perimeter.', 'Required acquisition-adjusted comparable growth is unresolved. Preserve critical-data withholding even if market prices and technicals refresh.', 'Lumpy system delivery, cash burn and gate-model integration can absorb bookings growth.', 'Acquisition-adjusted revenue and bookings-to-revenue conversion.', []),
'SOUN':('LivePerson closed September 4; the June financial base and an unchanged vendor forecast need not represent the combined business.', 'Missing post-close common shares, debt/cash, acquisition-adjusted growth and forecast perimeter; no scenario is published from the old standalone ratios.', 'Integration, customer retention, common-share dilution and competition from broader AI vendors.', 'Combined pro forma disclosure and acquired-versus-organic growth.', []),
'POET':('Commercial optical-engine revenue remains small and early-stage. Cash-flow statements do not themselves supply the missing gross-profit/valuation inputs.', 'Required comparable gross-profit and valuation inputs remain absent; a favorable optical-sector narrative cannot substitute for them.', 'Qualification timing, production economics, cash burn and repeated capital issuance.', 'Verified product gross economics and current capital structure.', []),
'OKLO':('Early ancillary engineering/fabrication revenue and test-reactor criticality are not Aurora commercial electricity sales.', 'An operating-company P/E/EBITDA projection is not a project-level value. Missing site-specific financed capex, fuel/licensing milestones and probability-adjusted project cash flows.', 'Long construction/regulatory duration and future funding; corporate cash does not prove profitable reactor economics.', 'Funded commercial site, fuel supply and licensing evidence.', []),
'APLD':('Campus construction and long-dated lease commitments have different timing from recognized annual revenue.', 'Existing comparable-growth hold plus current financing/economic-share review remain unresolved. Do not treat long-term gross lease totals as current cash flow.', 'Tenant concentration, secured funding, construction delays and common dilution.', 'Current financing bridge and acquisition/divestiture-comparable financials.', []),
'SMR':('US460 standard-design approval does not mean a site is licensed, financed and operating. Partner milestones create economic obligations.', 'Missing project-specific funding and common-share economics, including partner obligations and paired LLC units. The ordinary operating-company model is not a validated substitute.', 'Project delay, financing and payment obligations before commercial revenue.', 'Binding customer contracts and funded project economics.', []),
'EOSE':('Q2 gross margin was about −71%, with roughly 80% related-party revenue. September 14 disclosed a further $87M DOE draw, bringing draws to about $178M.', 'Missing fully reconciled preferred, derivative and subsequent financing claims against common equity. Do not add new debt cash without the associated debt/claims.', 'Negative unit economics, related-party collections, restricted cash and funding dependence.', 'Gross-margin recovery and current common-equity capital-claims waterfall.', []),
'RZLV':('H1 operating cash outflow was $91.956M. Restricted cash and unbilled/receivable balances are not interchangeable with unrestricted funding.', 'Required comparable growth plus acquisition/financing and going-concern reconciliation remain unresolved; semiannual reports do not create eight primary quarterly observations.', 'Financing, dilution, cash conversion and continuing-operation uncertainty.', 'Organic revenue and funded runway on an updated common-share basis.', []),
'SERV':('The August 6 outlook cut FY2026 revenue to $9–10M; fleet deployment targets are not recognized revenue.', 'Required comparable acquisition-adjusted growth is still unavailable. Do not reuse the earlier optimistic forecast or reweight around the missing factor.', 'Platform concentration, negative deployment gross economics and cash burn.', 'Revenue conversion, updated organic bridge and funding runway.', []),
'MU':('Latest reported fiscal Q3 revenue $41.456B and GAAP net income $28.243B; year-to-date revenue $78.959B. These unusually strong cycle margins are not five-year normalized margins.', 'The existing Candidate lacks a reviewed quality-score input ledger; fiscal Q4 is scheduled September 30. No normalized through-cycle scenario/capital basis is approved before the fresh report is reconciled.', 'Memory supply/pricing cyclicality, fabs, HBM execution and a very large starting capitalization.', 'September 30 report followed by an all-capex, through-cycle margin review.', [('MU_Q3','https://investors.micron.com/financials/quarterly-results/default.aspx','2026-06-24')]),
'LITE':('FY2026 revenue $3.014B; the release reports $524.8M GAAP operating income and a roughly $7.8B debt-extinguishment loss from note equitization. Vendor operating income and common shares require reconciliation.', 'The Candidate lacks a reviewed quality/capitalization ledger. Note equitization, true diluted shares and reported-versus-adjusted operating economics must be reconciled before scoring.', 'Optical component price/technology cycles, customer concentration and past convertible dilution.', 'Primary diluted-share and note-claim bridge plus normalized common earnings.', [('LITE_FY26','https://investor.lumentum.com/financial-news-releases/news-details/2026/Lumentum-Announces-Fourth-Quarter-and-Full-Fiscal-Year-2026-Results/default.aspx','2026-08-11')])}
for t,(facts,gap,risk,catalyst,extra) in HELD.items():
 REVIEWS.append(record(t,facts,'A five-year projection is withheld until the specified critical evidence is reconciled.','No unsupported sector/margin substitution.',gap,risk,catalyst,hold=[gap],extra=extra))
assert len(REVIEWS)==32 and {r['ticker'] for r in REVIEWS}==set(BY)

# Populate sources with exact canonical URLs and hashes of actually retrieved filings.
bydocs={t:[] for t in BY}
for x in json.loads((D/'documents.json').read_text()):
 if x['status']=='retrieved':bydocs[x['ticker']].append(x)
def sources_for(rv):
 t=rv['ticker'];sources={}
 r=BY[t]['metadata']['research']
 if r.get('primary_source','').startswith('https://'):
  sources['BASE_FINANCIALS']={'url':r['primary_source'],'as_of':str(r.get('financial_period_end') or '2026-09-06'),'date_basis':'financial period, not filing acceptance; see original audit','kind':'retained source-linked input ledger'}
 for i,doc in enumerate(bydocs[t]):
  sources[f'CURRENT_{i+1}']={k:doc[k] for k in ['url','retrieval_url','sha256','form','filed','retrieved_at']}
  sources[f'CURRENT_{i+1}'].update(as_of=doc['filed'],kind='SEC-filed document via explicitly identified public mirror')
 for sid,u,d in rv['extra']:sources[sid]={'url':u,'as_of':d,'kind':'primary issuer disclosure reviewed via web'}
 return sources

# Financial overrides repair ONLY the v2.2 calculation; original quality/monitoring
# snapshots and their scores remain immutable. Sources explain each correction.
OVERRIDES={
 'AVAV':dict(revenue_ttm=2002659000.,financial_period_end='2026-08-01',cash=580227000.,debt=850823000.,economic_shares=50820702.),
 'RGTI':dict(economic_shares=341508685.,cash=541300000.,debt=0.),
}
OVERRIDE_WHY={
 'AVAV':'TTM revenue = FY2026 $1,976.845M + quarter ended August 1 $480.490M − comparable quarter $454.676M. Use the September 10 filing cover-page common shares and current balance sheet. This corrects the old fiscal-April baseline for the scenario only.',
 'RGTI':'Economic-share reference = 333,768,747 shares on the August 3 cover-page date + 7,739,938 issued under the September government agreement. This is a disclosed-event-adjusted reference, not a claim of an audited September 29 fully diluted count. Long-term securities are included in the rounded $541.3M liquidity base; conditional grant tranches are excluded.'}
BUDGETS={
 'IREN':[(18e9,5e9,3e9,.25e9),(60e9,22e9,8e9,.5e9),(80e9,35e9,11e9,.75e9)],
 'RGTI':[(.15e9,-.30e9,0,0),(.25e9,-.20e9,.10e9,0),(.40e9,-.10e9,.25e9,0)],
 'RR':[(.06e9,-.15e9,0,0),(.10e9,-.10e9,0,0),(.15e9,-.05e9,0,0)]}
DEFINITIONS={'methodology':'MB_5X_FEASIBILITY_SHADOW_V2_2','status':'shadow_only','research_release':'2026-09-29-company-review','information_cutoff':CUTOFF,'records':{},'company_reviews':{},'disclosure':'All forecasts, terminal multiples and funding budgets are source-informed analyst assumptions, not management guidance unless explicitly identified. No calibrated probabilities or production ranks.'}
for rv in REVIEWS:
 t=rv['ticker'];stock=BY[t];m=stock['metadata'];r=m['research'];src=sources_for(rv)
 refs=list(src)
 # Include only matching evidence IDs for a reviewed event; exact event fingerprint
 # is checked by the adapter, so an old resolution cannot clear a new future filing.
 events=m.get('event_scan',{}).get('new_filings',[])
 trigger_assessment=('Reviewed the retained latest filing metadata and the cited actual disclosure. '+rv['facts']+' This resolution applies only to the exact captured trigger set; new disclosures or economic-share changes invalidate it.')
 review={'ticker':t,'reviewed_at':NOW,'information_cutoff':CUTOFF,'next_review_due':'2026-10-03','review_kind':'source_informed_analyst_scenario_review_not_independent_certification','status':'scenario_inputs_reviewed' if rv['cases'] else 'missing_critical_data','sources':src,'facts':rv['facts'],'growth_rationale':rv['growth_rationale'],'normalized_economics':rv['economics_rationale'],'funding_assessment':rv['funding_assessment'],'risk':rv['risk'],'next_review_trigger':rv['catalyst'],'critical_gaps':rv['critical_gaps'],'source_documents_retrieved':len(bydocs[t]),'original_quality_critical_reasons':m.get('score_eligibility',{}).get('critical_reasons',[]),'scope_limitations':['Company-specific hypotheses are not a fully verified six-pass opinion or validated return predictor.','No exhaustive current peer/index/ETF roster reconstruction is claimed in this scenario review.','Prices/technicals retain the completed market-session dates; financial reports retain their own period ends.']}
 DEFINITIONS['company_reviews'][t]=review
 if not rv['cases']:continue
 obs={'financial_basis_sha256':financial_basis(stock),'economic_shares':r.get('shares_outstanding'),'review_queue':m.get('review_queue') or [],'event_filings':events}
 rec={'review_status':'reviewed','reviewed_at':NOW,'valid_through':'2026-10-07','financial_basis_sha256':financial_basis(stock),'model':rv['model'],'model_rationale':rv['economics_rationale'],'funding_assessment':rv['funding_assessment'],'sources':src,'scenarios':{},'company_review':review,
      'review_resolution':{'observed_state_sha256':hashlib.sha256(canonical(obs)).hexdigest(),'conclusion':trigger_assessment,'source_ids':refs,'financial_overrides':OVERRIDES.get(t,{}),'override_rationale':OVERRIDE_WHY.get(t,'No financial input override; retained source ledger remains the starting basis.'),'override_source_ids':[k for k in refs if k.startswith('CURRENT_')] or refs}}
 revbase=OVERRIDES.get(t,{}).get('revenue_ttm',r.get('revenue_ttm'))
 for j,(name,vals) in enumerate(zip(('bear','base','bull'),rv['cases'])):
  rev5,margin,mult,dil=vals;rev5*=1e9
  inp={'revenue_cagr':(rev5/revbase)**.2-1,'dilution_5y':dil}
  if rv['model']=='equity_pe':inp.update(net_margin=margin,terminal_pe=mult)
  else:
   capex,cfo,equity,fees=BUDGETS[t][j]
   rr=dict(r);rr.update(OVERRIDES.get(t,{}));nd=rr['debt']-rr['cash']
   # Warrant cash-settlement reserve is not also counted as converted shares.
   other=([5e6,3e6,1e6][j] if t=='RR' else 0.)
   inp.update(ebitda_margin=margin,terminal_ev_ebitda=mult,net_debt_5y=nd+capex+fees-cfo-equity,preferred_claims_5y=0.,minority_claims_5y=0.,other_claims_5y=other)
  ev={}
  for f in inp:
   if f=='revenue_cagr':why=f'Analyst endpoint: ${rev5/1e9:g}B annual revenue in year five, equivalent CAGR {(rev5/revbase)**.2-1:.4%} from the disclosed ${revbase/1e9:g}B revenue base. '+rv['growth_rationale']
   elif f in ('net_margin','ebitda_margin'):why=rv['economics_rationale']+' This case uses '+str(margin*100)+'%; no source claims that this future margin is assured.'
   elif f.startswith('terminal_'):why=rv['economics_rationale']+' This case assumes '+str(mult)+'×. It is a normalized valuation assumption, not a current observed peer quotation.'
   elif f=='dilution_5y':why=rv['funding_assessment']+f' This case has {dil:+.0%} cumulative economic-share change over five years; past issuance is already in the starting share count.'
   elif f=='net_debt_5y':why='Calculated, not omitted: starting net debt + five-year productive capex + other funding uses − cumulative operating cash flow − new common-equity cash. '+rv['funding_assessment']
   elif f in ('preferred_claims_5y','minority_claims_5y'):why='Explicit analyst assumption of no new preferred or minority financing in this case; examined existing statements do not identify a material starting claim in this category. Funding is assigned to debt/common shares instead. A later claim invalidates the scenario; this is not an imputation for missing data.'
   else:why='Terminal cash-settlement reserve for warrant/other non-common claims, separate from debt. '+('Mezzanine warrants are not also included as converted shares in the dilution assumption.' if t=='RR' else 'Existing equity-linked awards are budgeted in dilution; do not charge an assumed conversion twice. Future financing is assumed debt/common only.')
   ev[f]={'rationale':why,'source_ids':refs}
  case={'label':f'{name.title()} analyst scenario; conditional assumptions, not a probability or issuer forecast. '+rv['risk'],'inputs':inp,'assumption_evidence':ev,'revenue_year5_usd':rev5,'funding_status':'conditional_scenario_not_committed_financing','return_basis':'terminal common-share price multiple excluding cash dividends; not present fair value or total return'}
  if rv['model']=='enterprise_ebitda':case['funding_bridge']={'starting_net_debt':nd,'capex_5y':capex,'cfo_5y':cfo,'new_common_cash_5y':equity,'other_funding_uses_5y':fees,'terminal_net_debt':inp['net_debt_5y'],'identity':'starting_net_debt + capex + other_uses - CFO - new_common_cash','cfo_note':'CFO is after interest, taxes and working capital; customer prepayments are not counted again as independent funding. Budgets are hypotheses, not disclosed five-year commitments.'}
  rec['scenarios'][name]=case
 DEFINITIONS['records'][t]=rec
assert len(DEFINITIONS['records'])==16
(A/'v22/assumptions.json').write_bytes(canonical(DEFINITIONS))
(A/'v22/research/source_capture_manifest.json').write_text(json.dumps({'summary':json.loads((D/'summary.json').read_text()),'documents':json.loads((D/'documents.json').read_text()),'artifact_run_id':36661061224,'artifact_id':11073878191,'source_capture_is_not_research_certification':True},indent=2)+'\n')
(A/'v22/research/calibration_access_checks.json').write_bytes((D/'calibration_access_checks.json').read_bytes())
print(NOW, 'reviews',len(DEFINITIONS['company_reviews']),'scenario sets',len(DEFINITIONS['records']))
