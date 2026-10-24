# One-off builder for hand-verified data (layoffs, claims, Challenger, China youth).
# Every row cites a source that was opened/searched on 2026-10-24.
import json, os
D = os.path.join(os.path.dirname(__file__), "..", "site", "data")
ASOF = "2026-10-24"
R = lambda **k: k
rows = [
 R(date="2024-10-11",company="Boeing",count=17000,label="17,000",pct="10%",sector="Aerospace",country="US",reason="Strike losses, cost cuts",src="https://www.reuters.com/business/aerospace-defense/boeing-cut-17000-jobs-delay-first-777x-delivery-strike-hits-finances-2024-10-11/",srcname="Reuters"),
 R(date="2024-12-20",company="Volkswagen",count=35000,label="35,000",pct="",sector="Auto",country="Germany",reason="Union deal: German job cuts by 2030, no forced layoffs",src="https://www.reuters.com/business/autos-transportation/vw-union-agree-cut-35000-jobs-germany-avert-strikes-2024-12-20/",srcname="Reuters"),
 R(date="2025-01-14",company="Meta",count=3600,label="~3,600",pct="5%",sector="Tech",country="US",reason="Performance-based cuts (\"lowest performers\")",src="https://www.reuters.com/technology/meta-lay-off-5-lowest-performers-plans-hire-impacted-roles-2025-01-14/",srcname="Reuters",note="5% of ~72,000 staff"),
 R(date="2025-02-24",company="Starbucks",count=1100,label="1,100",pct="",sector="Consumer",country="US",reason="Corporate turnaround",src="https://www.reuters.com/business/retail-consumer/starbucks-eliminate-more-than-1000-corporate-roles-2025-02-24/",srcname="Reuters"),
 R(date="2025-05-13",company="Microsoft",count=6000,label="~6,000",pct="3%",sector="Tech",country="US",reason="Fewer management layers",src="https://www.reuters.com/business/world-at-work/microsoft-lay-off-3-workforce-cnbc-reports-2025-05-13/",srcname="Reuters"),
 R(date="2025-05-13",company="Nissan",count=20000,label="~20,000",pct="",sector="Auto",country="Japan",reason="Re:Nissan plan, plant closures",src="https://www.reuters.com/business/autos-transportation/nissan-announces-new-cost-savings-measures-withholds-fy2025-estimates-2025-05-13/",srcname="Reuters",note="Includes 9,000 announced Nov 2024"),
 R(date="2025-06-05",company="Procter & Gamble",count=7000,label="up to 7,000",pct="15% of non-mfg",sector="Consumer",country="US",reason="2-year restructuring, tariffs",src="https://www.reuters.com/business/procter-gamble-cut-7000-jobs-over-two-years-2025-06-05/",srcname="Reuters"),
 R(date="2025-07-02",company="Microsoft",count=9000,label="~9,000",pct="<4%",sector="Tech",country="US",reason="AI spending, fewer layers",src="https://www.reuters.com/business/world-at-work/microsoft-lay-off-many-9000-employees-seattle-times-reports-2025-07-02/",srcname="Reuters"),
 R(date="2025-07-24",company="Intel",count=24000,label="~24,000",pct="15% of core",sector="Tech",country="US",reason="Turnaround under CEO Tan",src="https://www.intel.com/content/www/us/en/newsroom/news/corporate/lip-bu-tan-steps-in-the-right-direction.html",srcname="Intel / Reuters",note="Core workforce cut to ~75,000 from 99,500; layoffs + attrition"),
 R(date="2025-07-27",company="TCS",count=12000,label=">12,000",pct="2%",sector="Tech",country="India",reason="Skills mismatch, AI deployment",src="https://www.reuters.com/world/india/indian-tech-company-tcs-cut-workforce-by-2-affecting-more-than-12000-jobs-2025-07-27/",srcname="Reuters"),
 R(date="2025-09-02",company="Salesforce",count=4000,label="~4,000",pct="",sector="Tech",country="US",reason="Support roles replaced by AI agents",src="https://www.cnbc.com/2025/09/02/salesforce-ceo-confirms-4000-layoffs-because-i-need-less-heads-with-ai.html",srcname="CNBC"),
 R(date="2025-09-25",company="Accenture",count=11000,label=">11,000",pct="",sector="Tech",country="Ireland/US",reason="$865M restructuring, AI reskilling",src="https://www.reuters.com/business/accenture-posts-fourth-quarter-revenue-above-estimates-2025-09-25/",srcname="Reuters",note="Headcount fell 791k→779k Jun–Aug 2025"),
 R(date="2025-09-25",company="Bosch",count=13000,label="~13,000",pct="",sector="Auto",country="Germany",reason="Weak car market, cost gap",src="https://www.reuters.com/business/retail-consumer/bosch-cut-five-digit-number-additional-jobs-says-handelsblatt-2025-09-25/",srcname="Reuters"),
 R(date="2025-09-25",company="Starbucks",count=900,label="~900",pct="",sector="Consumer",country="US",reason="$1B restructuring, store closures",src="https://www.reuters.com/business/starbucks-close-some-stores-part-restructuring-plan-2025-09-25/",srcname="Reuters"),
 R(date="2025-09-29",company="Lufthansa",count=4000,label="4,000",pct="",sector="Airline",country="Germany",reason="Admin jobs, AI/digitalization by 2030",src="https://www.reuters.com/business/world-at-work/lufthansa-cut-4000-jobs-by-2030-2025-09-29/",srcname="Reuters"),
 R(date="2025-10-16",company="Nestlé",count=16000,label="16,000",pct="",sector="Consumer",country="Switzerland",reason="Cost cuts under new CEO",src="https://www.reuters.com/business/nestle-reports-better-than-expected-sales-growth-with-new-ceo-helm-2025-10-16/",srcname="Reuters"),
 R(date="2025-10-23",company="Target",count=1800,label="1,800",pct="8% of corporate",sector="Retail",country="US",reason="Turnaround",src="https://www.reuters.com/business/world-at-work/target-plans-lay-off-1800-employees-wsj-reports-2025-10-23/",srcname="Reuters",note="~1,000 layoffs + 800 open roles"),
 R(date="2025-10-28",company="Amazon",count=14000,label="~14,000",pct="",sector="Tech",country="US",reason="Fewer layers, AI",src="https://www.reuters.com/sustainability/amazon-lay-off-about-14000-roles-2025-10-28/",srcname="Reuters"),
 R(date="2025-10-28",company="UPS",count=48000,label="48,000",pct="",sector="Logistics",country="US",reason="Less Amazon volume, network cuts",src="https://www.reuters.com/business/world-at-work/ups-cut-34000-jobs-first-nine-months-2025-2025-10-28/",srcname="Reuters",note="Cut during 2025 (34k operational + 14k management)"),
 R(date="2025-11-20",company="Verizon",count=13000,label=">13,000",pct="~20% non-union",sector="Telecom",country="US",reason="Restructuring",src="https://www.reuters.com/business/world-at-work/verizon-cutting-more-than-13000-jobs-it-restructures-2025-11-20/",srcname="Reuters"),
 R(date="2025-11-25",company="HP Inc",count=6000,label="4,000–6,000",pct="",sector="Tech",country="US",reason="AI-driven restructuring by FY2028",src="https://www.reuters.com/business/hp-cut-about-6000-jobs-by-2028-ramps-up-ai-efforts-2025-11-25/",srcname="Reuters",note="Totals use upper end of range"),
 R(date="2025-12-01",company="Omnicom",count=4000,label=">4,000",pct="",sector="Advertising",country="US",reason="IPG merger integration",src="https://www.reuters.com/business/media-telecom/omnicom-cut-4000-jobs-shut-several-agencies-after-ipg-takeover-ft-reports-2025-12-01/",srcname="Reuters"),
 R(date="2026-01-12",company="Citigroup",count=1000,label="~1,000",pct="",sector="Financial",country="US",reason="Part of 20,000 cut plan by end-2026",src="https://www.reuters.com/sustainability/citigroup-is-set-cut-about-1000-jobs-bloomberg-news-reports-2026-01-12/",srcname="Reuters",k=True),
 R(date="2026-01-27",company="UPS",count=30000,label="up to 30,000",pct="",sector="Logistics",country="US",reason="Attrition + driver buyouts, 24 sites shut",src="https://www.reuters.com/business/retail-consumer/ups-forecasts-higher-2026-revenue-2026-01-27/",srcname="Reuters",k=True),
 R(date="2026-01-28",company="Amazon",count=16000,label="~16,000",pct="~10% corp. (with Oct)",sector="Tech",country="US",reason="Fewer layers, bureaucracy",src="https://www.aboutamazon.com/news/company-news/amazon-layoffs-corporate-jan-2026",srcname="Amazon / Reuters",k=True),
 R(date="2026-01-29",company="Dow",count=4500,label="~4,500",pct="~13%",sector="Chemicals",country="US",reason="AI & automation, weak demand",src="https://www.reuters.com/sustainability/chemicals-maker-dow-eliminate-4500-roles-targets-2-billion-core-profit-boost-2026-01-29/",srcname="Reuters",k=True),
 R(date="2026-02-26",company="Block",count=4000,label=">4,000",pct="~40%",sector="Fintech",country="US",reason="AI overhaul",src="https://www.reuters.com/business/blocks-fourth-quarter-profit-rises-announces-over-4000-job-cuts-2026-02-26/",srcname="Reuters"),
 R(date="2026-03-30",company="General Motors",count=1300,label="1,300 (temporary)",pct="",sector="Auto",country="US",reason="EV plant idled (Factory Zero)",src="https://www.reuters.com/business/autos-transportation/gm-idles-detroit-ev-plant-temporarily-laying-off-1300-2026-03-30/",srcname="Reuters",counted=False,note="Temporary layoff — excluded from totals",k=True),
 R(date="2026-03-31",company="Oracle",count=None,label="thousands (30,000 unconfirmed)",pct="",sector="Tech",country="US/India",reason="AI data-center spending",src="https://www.cnbc.com/2026/03/31/oracle-layoffs-ai-spending.html",srcname="CNBC",counted=False,note="Oracle declined to comment; 20k–30k is a TD Cowen estimate — excluded from totals",k=True),
 R(date="2026-04-14",company="Renault",count=2400,label="up to 2,400",pct="15–20% of engineers",sector="Auto",country="France",reason="Chinese competition, over 2 years",src="https://www.reuters.com/business/retail-consumer/renault-will-cut-engineering-staff-by-15-20-over-two-years-2026-04-14/",srcname="Reuters",k=True),
 R(date="2026-04-14",company="Disney",count=1000,label="~1,000",pct="",sector="Media",country="US",reason="Streamlining under CEO D'Amaro",src="https://www.reuters.com/legal/litigation/disney-eliminate-1000-positions-2026-04-14/",srcname="Reuters",k=True),
 R(date="2026-04-23",company="Nike",count=1400,label="~1,400",pct="",sector="Consumer",country="US",reason="Tech/ops consolidation",src="https://www.reuters.com/business/nike-cut-1400-jobs-2026-04-23/",srcname="Reuters",k=True),
 R(date="2026-05-13",company="Cisco",count=4000,label="<4,000",pct="<5%",sector="Tech",country="US",reason="Shift to AI, silicon, security",src="https://www.reuters.com/technology/cisco-raises-annual-revenue-forecast-2026-05-13/",srcname="Reuters",note="Totals use 4,000 (upper bound)",k=True),
 R(date="2026-05-20",company="Meta",count=8000,label="~8,000",pct="10%",sector="Tech",country="US",reason="AI capex; 6,000 open roles cancelled",src="https://www.reuters.com/world/meta-lays-out-plans-may-20-layoffs-restructuring-internal-document-says-2026-05-18/",srcname="Reuters / AP",k=True),
 R(date="2026-07-06",company="Microsoft",count=4800,label="4,800",pct="~2%",sector="Tech",country="US",reason="Sales revamp, Xbox overhaul",src="https://www.reuters.com/business/world-at-work/microsoft-joins-ai-driven-tech-layoff-wave-with-4800-job-cuts-2026-07-06/",srcname="Reuters",k=True),
 R(date="2026-09-02",company="Uber",count=3300,label="~3,300",pct="10%",sector="Tech",country="US",reason="Flatten management",src="https://www.wsj.com/livecoverage/stock-market-today-dow-sp-500-nasdaq-09-02-2026/card/Qz242lKpuPXtWvZVwe1G",srcname="WSJ",k=True),
 R(date="2026-09-10",company="Omnicom",count=None,label="15,000 net headcount drop (incl. disposals)",pct="~12.5%",sector="Advertising",country="US",reason="IPG integration; 120k→105k by end-2026",src="https://www.investing.com/news/transcripts/omnicom-at-goldman-sachs-communacopia--technology-conference-2026-integration-gains-93CH-4896507",srcname="CFO remarks (conf. transcript)",counted=False,note="Not 15,000 layoffs: includes outsourcing, disposals, attrition; overlaps Dec 2025 cut — excluded from totals",k=True),
 R(date="2026-10-23",company="American Express",count=3500,label="~3,500",pct="5%",sector="Financial",country="US",reason="Fewer layers, prepare for AI",src="https://www.cnbc.com/2026/10/23/american-express-job-cuts.html",srcname="CNBC / WSJ",note="5% confirmed; WSJ puts it at ~3,500. The 3,840 figure is 5% of end-2025 headcount",k=True),
]
for r in rows:
    r.setdefault("counted", r["count"] is not None); r.setdefault("note",""); r["kobeissi"]=r.pop("k",False); r["asof"]=ASOF
json.dump({"asof":ASOF,"rows":rows},open(f"{D}/layoffs.json","w"),ensure_ascii=False,indent=1)

kob = [
 ("UPS","30,000","Verified","Up to 30,000 operational jobs in 2026, mostly attrition/buyouts (Reuters, Bloomberg)","https://www.reuters.com/business/retail-consumer/ups-forecasts-higher-2026-revenue-2026-01-27/"),
 ("Oracle","30,000","Partly verified","Layoffs confirmed (CNBC, BBC) but Oracle never confirmed a total; 20–30k is a TD Cowen estimate","https://www.cnbc.com/2026/03/31/oracle-layoffs-ai-spending.html"),
 ("Amazon","16,000","Verified","Company statement + Reuters, 28 Jan 2026","https://www.aboutamazon.com/news/company-news/amazon-layoffs-corporate-jan-2026"),
 ("Omnicom","15,000","Partly verified","CFO: headcount 120k→105k by end-2026, includes disposals/outsourcing — not 15,000 layoffs. Reuters confirmed >4,000 cuts (Dec 2025)","https://www.reuters.com/business/media-telecom/omnicom-cut-4000-jobs-shut-several-agencies-after-ipg-takeover-ft-reports-2025-12-01/"),
 ("Meta","8,000","Verified","~10% of staff, 20 May 2026 (Reuters, AP)","https://www.reuters.com/world/meta-lays-out-plans-may-20-layoffs-restructuring-internal-document-says-2026-05-18/"),
 ("Microsoft","4,800","Verified","Microsoft blog + Reuters, 6 Jul 2026","https://blogs.microsoft.com/blog/2026/07/06/the-latest-in-our-company-transformation/"),
 ("Dow","4,500","Verified","Reuters, 29 Jan 2026","https://www.reuters.com/sustainability/chemicals-maker-dow-eliminate-4500-roles-targets-2-billion-core-profit-boost-2026-01-29/"),
 ("Cisco","<4,000","Verified","Cisco blog + Reuters, May 2026","https://blogs.cisco.com/news/our-path-forward"),
 ("American Express","3,840","Partly verified","5% cut confirmed (CNBC, 23 Oct 2026); WSJ says ~3,500. 3,840 = 5% of end-2025 headcount","https://www.cnbc.com/2026/10/23/american-express-job-cuts.html"),
 ("Uber","3,300","Verified","~10% of staff, 2 Sep 2026 (WSJ, NYT, Reuters)","https://www.wsj.com/livecoverage/stock-market-today-dow-sp-500-nasdaq-09-02-2026/card/Qz242lKpuPXtWvZVwe1G"),
 ("Renault","up to 2,400","Verified","15–20% of engineers over 2 years (Reuters); 2,400 per Automotive News","https://www.reuters.com/business/retail-consumer/renault-will-cut-engineering-staff-by-15-20-over-two-years-2026-04-14/"),
 ("Nike","1,400","Verified","Nike newsroom + Reuters, 23 Apr 2026","https://www.reuters.com/business/nike-cut-1400-jobs-2026-04-23/"),
 ("General Motors","1,300","Verified, but temporary","Temporary layoff at Detroit EV plant (Reuters) — not a permanent cut","https://www.reuters.com/business/autos-transportation/gm-idles-detroit-ev-plant-temporarily-laying-off-1300-2026-03-30/"),
 ("Disney","1,000","Verified","Reuters, AP, Apr 2026","https://www.reuters.com/legal/litigation/disney-eliminate-1000-positions-2026-04-14/"),
 ("Citigroup","1,000","Verified","Reuters (source), Jan 2026; part of 20,000 plan","https://www.reuters.com/sustainability/citigroup-is-set-cut-about-1000-jobs-bloomberg-news-reports-2026-01-12/"),
 ("Tech total 2026","135,000 across 330 companies","Verified","Layoffs.fyi shows 135,246 tech employees at 332 companies in 2026 (fetched 24 Oct 2026)","https://layoffs.fyi/"),
]
turk = [
 dict(claim="Only 25% of China's 12 million graduates found jobs",verdict="Unverified",
      facts="The graduate count is real: China expected a record 12.7 million in 2026 (Ministry of Education via Xinhua). No official source publishes a 25% job-placement rate; NBS's Sept 2026 rate for urban 16–24s (excl. students) was 18.0% unemployed.",
      src=["https://english.news.cn/20251120/3277566206e4490e94d9632d2bc5d409/c.html","https://www.caixinglobal.com/2026-10-21/chinas-youth-unemployment-rate-eases-to-18-102495753.html"]),
 dict(claim="Officially 25% of 18–25 year-olds jobless; unofficially ~40%",verdict="Misleading",
      facts="Official rate is 18.0% (Sept 2026) / 18.9% peak (Aug 2026) for ages 16–24 excl. students — not 25%. The old method peaked at 21.3% (June 2023) before NBS suspended it. The 'unofficial ~40%' likely traces to a 2023 estimate of up to 46.5% by Peking Univ. professor Zhang Dandan that counted people not looking for work.",
      src=["https://www.reuters.com/world/china/china-stop-releasing-youth-jobless-rate-data-aug-says-stats-bureau-2023-08-15/","https://www.reuters.com/article/idUSL4N3960Z5/"]),
 dict(claim="Over 40 and laid off: chance of finding a new job is zero",verdict="Unverified (hyperbole)",
      facts="No data supports 'zero'. NBS's urban unemployment rate for ages 30–59 was 3.9% in Sept 2026. NBS doesn't publish re-employment odds by age.",
      src=["https://economy.caixin.com/2026-10-21/102495714.html"]),
]
json.dump({"asof":ASOF,"kobeissi_post":"The Kobeissi Letter on X, 'Layoff Announcements in 2026' (seen by user ~23 Oct 2026)",
  "kobeissi":[dict(company=a,claimed=b,status=c,detail=d,src=e) for a,b,c,d,e in kob],
  "turkish_post":"Translated-from-Turkish X post 'Reporting from China' (seen by user ~23 Oct 2026)","turkish":turk},
  open(f"{D}/claims.json","w"),ensure_ascii=False,indent=1)

ch = {"asof":ASOF,"source":"Challenger, Gray & Christmas — Challenger Report (Dec 2024 and Sept 2026 editions)",
 "src":["https://www.challengergray.com/wp-content/uploads/2026/10/Challenger-Report-September-2026.pdf","https://www.challengergray.com/wp-content/uploads/2025/01/The-Challenger-Report-December-2024.pdf"],
 "unit":"US announced job cuts per month",
 "monthly":{"2024-10":55597,"2024-11":57727,"2024-12":38792,
  "2025-01":49795,"2025-02":172017,"2025-03":275240,"2025-04":105441,"2025-05":93816,"2025-06":47999,"2025-07":62075,"2025-08":85979,"2025-09":54064,"2025-10":153074,"2025-11":71321,"2025-12":35553,
  "2026-01":108435,"2026-02":48307,"2026-03":60620,"2026-04":83387,"2026-05":97006,"2026-06":45849,"2026-07":33429,"2026-08":52881,"2026-09":43281},
 "totals":{"2024":761358,"2025":1206374,"2026_ytd_sep":573195},
 "tech_ytd_sep_2026":165925,"ai_cited_ytd_sep_2026":120136}
json.dump(ch,open(f"{D}/challenger.json","w"),indent=1)
