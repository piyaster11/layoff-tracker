#!/usr/bin/env python3
"""Refresh the auto-updatable series: BLS youth unemployment, NY Fed recent grads,
Layoffs.fyi annual totals, and China NBS youth rates. Run manually: python3 scripts/update.py
(No scheduled automation.) Optional env BLS_KEY for a BLS API v2 key."""
import json, os, csv, io, urllib.request, datetime
D = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "site", "data")
TODAY = datetime.date.today().isoformat()
START = "2024-10"
def get(url, data=None, headers=None):
    h = {"User-Agent": "Mozilla/5.0 layoff-tracker"}; h.update(headers or {})
    return urllib.request.urlopen(urllib.request.Request(url, data=data, headers=h), timeout=60).read()

def bls():
    ids = {"LNS14000036": "Ages 20–24", "LNS14024887": "Ages 16–24", "LNS14000000": "All ages 16+"}
    y = datetime.date.today().year
    body = {"seriesid": list(ids), "startyear": "2024", "endyear": str(y)}
    if os.environ.get("BLS_KEY"): body["registrationkey"] = os.environ["BLS_KEY"]
    d = json.loads(get("https://api.bls.gov/publicAPI/v2/timeseries/data/", json.dumps(body).encode(), {"Content-Type": "application/json"}))
    assert d["status"] == "REQUEST_SUCCEEDED", d
    out = {"asof": TODAY, "source": "U.S. Bureau of Labor Statistics, Current Population Survey (seasonally adjusted), BLS Public API v2",
           "note": "October 2025 was not collected because of the federal government shutdown.", "series": []}
    for s in d["Results"]["series"]:
        pts = sorted((f'{p["year"]}-{p["period"][1:]}', float(p["value"])) for p in s["data"] if p["period"].startswith("M") and p["value"] not in ("-", ""))
        out["series"].append({"id": s["seriesID"], "name": ids[s["seriesID"]],
            "src": f'https://data.bls.gov/timeseries/{s["seriesID"]}', "data": [[k, v] for k, v in pts if k >= START]})
    json.dump(out, open(f"{D}/us_youth.json", "w"), indent=1)

def nyfed():
    base = "https://www.newyorkfed.org/medialibrary/research/interactives/data/college-labor-market/"
    def rows(name):
        r = list(csv.reader(io.StringIO(get(base + name).decode("utf-8-sig"))))
        hdr, res = r[0], []
        for row in r[1:]:
            m, dd, yy = row[0].split("/"); k = f"{yy}-{int(m):02d}"
            if k >= START: res.append([k] + row[1:])
        return hdr, res
    h, u = rows("college-labor-unemployment-data.csv")
    h2, ue = rows("college-labor-underemployment-data.csv")
    json.dump({"asof": TODAY, "source": "Federal Reserve Bank of New York, The Labor Market for Recent College Graduates (Census/BLS Current Population Survey via IPUMS)",
        "src": "https://www.newyorkfed.org/research/college-labor-market",
        "note": "Recent graduates = ages 22–27 with a bachelor's degree or higher. Updated quarterly.",
        "unemployment": {"cols": h[1:5], "data": [[r[0]] + [float(x) for x in r[1:5]] for r in u]},
        "underemployment": {"cols": h2[1:3], "data": [[r[0]] + [float(x) for x in r[1:3]] for r in ue]}},
        open(f"{D}/nyfed.json", "w"), indent=1)

def layoffsfyi():
    d = json.loads(get("https://layoffs-fyi.onrender.com/api/annual-stats"))
    json.dump({"asof": TODAY, "source": "Layoffs.fyi (tech & startup layoffs tracker)", "src": "https://layoffs.fyi/",
               "years": [y for y in d["years"] if y["year"] >= 2024]}, open(f"{D}/layoffsfyi.json", "w"), indent=1)

def china():
    def series(slug):
        return [[r["date"], float(r["value"])] for r in json.loads(get(f"https://chinadata.live/api/v2/data/{slug}"))["data"]["data"]]
    # Values are NBS official figures; the NBS database (data.stats.gov.cn) blocks automated access,
    # so the monthly list is pulled from a public mirror of NBS data and spot-checked against Reuters/Caixin.
    checks = {"2026-09": "https://www.caixinglobal.com/2026-10-21/chinas-youth-unemployment-rate-eases-to-18-102495753.html",
              "2026-08": "https://www.reuters.com/world/asia-pacific/chinese-youth-jobless-rate-hits-one-year-high-august-2026-09-17/",
              "2026-06": "https://www.reuters.com/jp/world/china/HKWAJJZAW5IEFFHK2565BZEOEY-2026-07-20/",
              "2025-12": "https://money.usnews.com/investing/news/articles/2026-01-21/chinas-december-youth-jobless-rate-drops-to-16-5"}
    a, b = series("china-youth-unemployment"), series("china-unemployment-25-29")
    json.dump({"asof": TODAY, "source": "National Bureau of Statistics of China — monthly urban surveyed unemployment rate by age group (excluding students)",
        "src": "https://www.stats.gov.cn/sj/zxfb/202401/t20240117_1946641.html",
        "method_note": "NBS suspended the youth series after June 2023 (record 21.3% under the old method) and restarted it in Jan 2024 with a new measure that excludes students (first value: Dec 2023 = 14.9%). Numbers before and after are not comparable.",
        "verified_points": checks,
        "series": [{"id": "16-24", "name": "Ages 16–24 (excl. students)", "data": [p for p in a if p[0] >= START]},
                   {"id": "25-29", "name": "Ages 25–29 (excl. students)", "data": [p for p in b if p[0] >= START]}]},
        open(f"{D}/china_youth.json", "w"), ensure_ascii=False, indent=1)

if __name__ == "__main__":
    for f in (bls, nyfed, layoffsfyi, china):
        try: f(); print("ok", f.__name__)
        except Exception as e: print("FAILED", f.__name__, e)
    m = json.load(open(f"{D}/meta.json")) if os.path.exists(f"{D}/meta.json") else {}
    m["last_updated"] = TODAY; json.dump(m, open(f"{D}/meta.json", "w"), indent=1)
