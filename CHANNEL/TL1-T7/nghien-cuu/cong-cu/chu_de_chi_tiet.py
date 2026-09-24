# -*- coding: utf-8 -*-
import csv, io, os, re, glob, statistics, datetime as dt
NC = r"D:\New folder\shopapi\tools\kho-github\CHANNEL\TL4-T7\nghien-cuu"
CS = r"D:\New folder\shopapi\tools\kho-github\CHANNEL\TL4-T7\chi-so"
HOM_NAY = dt.date(2026, 9, 9); MOC = HOM_NAY - dt.timedelta(days=21)
LOAI = re.compile(r"雑学|漫画|恋愛|ゆっくり|2ch|２ｃｈ|反応集|スカッと|速報|野球|サッカー|ゲーム|ドラマ|BGM|ホラー|ニュース|政治|海外の反応|料理|アニメ|PIVOT|学識|ダイヤモンド")
GIA = re.compile(r"50代|60代|70代|老後|定年|シニア|中年|孫|年金|人生後半|歳を")
ct = list(csv.DictReader(io.open(os.path.join(NC, "content.csv"), encoding="utf-8-sig")))
dt_ = {r["Kênh"]: r for r in csv.DictReader(io.open(os.path.join(NC, "doi-thu.csv"), encoding="utf-8-sig"))}
tk = {}
for r in ct:
    tk.setdefault(r["Kênh"], []).append(float(re.sub(r"\D", "", r["View"]) or 0))
TV = {k: statistics.median(v) for k, v in tk.items()}
def n(s): return float(re.sub(r"\D", "", str(s or "")) or 0)
def d(s):
    m = re.match(r"(\d{4})-(\d{2})-(\d{2})", s or ""); return dt.date(*map(int, m.groups())) if m else None
def that(s):  # ngày giả = ngày 09 của tháng cũ
    x = d(s); return x if x and not (x.day == 9 and x.month != 9) else None
def dong(r):
    v = n(r["View"]); tv = TV.get(r["Kênh"], 0) or 1; k = dt_.get(r["Kênh"], {})
    ng = that(r["Ngày đăng"]); tuoi = (HOM_NAY - ng).days if ng else None
    tuoi_s = ("%3dd" % tuoi) if tuoi is not None else r["Ngày đăng"][:7]
    m = re.search(r"v=([\w-]{11})", r["Link video"] or ""); mid = m.group(1) if m else "?"
    gia = "CÓ" if GIA.search((r["Tiêu đề video"] or "") + (r["Hashtag"] or "") + (r["Mô tả"] or "")[:300]) else "-"
    return (f"×{v/tv:>5.1f} · {v:>7.0f} · {tuoi_s:>7} · đà {r['Tăng/ngày'] or '-':>5} · {r['Thời lượng']:>6} · {r['Kênh'][:13]:13} sub {k.get('Subs','?'):>6} {k.get('Trạng thái','')[:8]:8} · làm:{r['Đã làm'] or '-':4} · già:{gia:2} · {r['Tiêu đề video'][:72]} · {mid}")
out = []
def khoi(ten, pat, chi_moi=False, top=25, loc_tuyen=None):
    rs = [r for r in ct if re.search(pat, r["Tiêu đề video"] or "") and not LOAI.search((r["Tiêu đề video"] or "") + (r["Kênh"] or ""))]
    if loc_tuyen: rs = [r for r in rs if loc_tuyen in (r["Tuyến / Kênh"] or "")]
    if chi_moi: rs = [r for r in rs if that(r["Ngày đăng"]) and that(r["Ngày đăng"]) >= MOC]
    rs.sort(key=lambda r: -n(r["View"]))
    out.append(f"\n### {ten} — {len(rs)} video" + (" (≤21 ngày)" if chi_moi else ""))
    for r in rs[:top]: out.append("  " + dong(r))
khoi("BRAND/流行/興味がない — toàn sổ", r"ブランド|流行|興味がない|興味が持てない|興味がない")
khoi("独り言 — toàn sổ", r"独り言|ひとりごと")
khoi("友達少ない — ≤21 ngày", r"友達|友人|親友", chi_moi=True)
khoi("一人 × 知能/IQ/賢い/天才 — toàn sổ", r"(?=.*(一人|1人|ひとり|孤独|独り))(?=.*(知能|IQ|賢い|天才|知的|頭が|頭の|脳が優秀|高性能|特殊な脳))")
khoi("家 — ≤21 ngày", r"家にい|家から|家を愛|家が好き|外に出ない|出かけない|インドア|引きこも|何もできない", chi_moi=True)
khoi("Tuyến lệch nhịp — ≤21 ngày, xếp theo view", r".", chi_moi=True, top=40, loc_tuyen="lech-nhip")
# pool của 8 video mình có chạm chủ đề nào
out.append("\n### POOL của 8 video mình — hàng xóm chạm các chủ đề ứng viên (imp · CTR · view · AVD)")
pat = re.compile(r"ブランド|流行|興味がない|独り言|友達|知能|IQ|賢い|天才|家にい|家から|家が好き|外に出ない")
for vid in ["2sOMyQxOdKE", "uFgiOL4yskg", "dR8fA42KTCY", "48EhWA__29k", "0fAIs-DTgw8", "UpkC5cEO_VA", "32CA4WuHgVc", "v4qSum0iCMg"]:
    fs = [f for f in glob.glob(os.path.join(CS, vid, "*h", "traffic-related.csv"))]
    if not fs: continue
    f = max(fs, key=lambda p: int(re.search(r"(\d+)h", p).group(1)))
    for r in csv.DictReader(io.open(f, encoding="utf-8-sig")):
        t = r.get("Source title") or ""
        if pat.search(t) and not LOAI.search(t):
            out.append(f"  {vid[:6]} · {r['Thumbnail impressions'] or 0:>4} imp · ctr {r['Thumbnail click-through rate (%)'] or '-':>5} · {r['Views'] or 0:>2} view · avd {r['Average view duration'] or '-':>8} · {t[:75]}")
io.open(os.path.join(os.path.dirname(__file__), "chu_de.txt"), "w", encoding="utf-8").write("\n".join(out)); print("ok")
