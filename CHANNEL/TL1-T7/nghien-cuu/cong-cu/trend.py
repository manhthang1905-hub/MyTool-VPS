# -*- coding: utf-8 -*-
"""Đột biến gần: trang chủ máy ảo + sổ đối thủ, gom theo chủ đề, tỷ lệ thắng."""
import csv, io, os, re, statistics, datetime as dt
NC = r"D:\New folder\shopapi\tools\kho-github\CHANNEL\TL4-T7\nghien-cuu"
HOM_NAY = dt.date(2026, 9, 9)
MOC = HOM_NAY - dt.timedelta(days=21)
LOAI = re.compile(r"雑学|漫画|恋愛|ゆっくり|2ch|２ｃｈ|反応集|スカッと|速報|野球|サッカー|ゲーム|ドラマ|BGM|ホラー|ニュース|政治|海外の反応|料理|アニメ")
GIA = re.compile(r"50代|60代|70代|老後|定年|シニア|中年|孫|年金|人生後半")
TAM_LY = re.compile(r"心理|脳科学|メンタル|HSP|内向|自己肯定感|生きづらい|繊細|考えすぎ|劣等感|承認欲求|アドラー|ユング|認知|うつ|不安|愛着|孤独|一人|1人|ひとり|人間関係|性格|特徴|理由|脳")
CHU_DE = [
    ("家/ở nhà", r"家にい|家から|家を愛|家が好き|外に出ない|出かけない|インドア|引きこも"),
    ("一人/thích một mình", r"一人|1人|ひとり|孤独|独り"),
    ("友達少ない", r"友達|友人|親友"),
    ("SNS", r"SNS|スマホ|インスタ"),
    ("独り言", r"独り言|ひとりごと"),
    ("ブランド/流行に興味ない", r"ブランド|流行|興味がない|興味が持てない|スポーツ"),
    ("気づきすぎる/HSP", r"気づきすぎ|敏感|繊細|HSP"),
    ("雑談/会話苦手", r"雑談|会話|話すこと|コミュ"),
    ("人混み/誰といても疲れる", r"人混み|疲れる|群れ"),
    ("部屋/片付け", r"部屋|片付け|掃除"),
    ("知能/賢い/IQ", r"知能|賢い|IQ|天才|頭が|頭の|知性"),
    ("静かな限界/諦め", r"限界|諦め|言わなくなった|頑張り"),
    ("他人の視線/世間の正解", r"視線|世間|モノサシ|正解を|他人の"),
]


def d_(s):
    m = re.match(r"(\d{4})-(\d{2})-(\d{2})", s or "")
    return dt.date(int(m.group(1)), int(m.group(2)), int(m.group(3))) if m else None


def n_(s):
    m = re.search(r"\d+", str(s or "").replace(",", "").replace(".", ""))
    return float(m.group()) if m else 0


def chu_de(t):
    return [ten for ten, p in CHU_DE if re.search(p, t or "")]


out = []
# ---------- A. TRANG CHỦ ----------
tc = list(csv.DictReader(io.open(os.path.join(NC, "trang-chu.csv"), encoding="utf-8-sig")))
luot = sorted(set(r["Lúc quét"] for r in tc))
out.append(f"TRANG CHỦ máy ảo: {len(tc)} dòng · lượt quét: {luot}")
theo_ma = {}
for r in tc:
    if r.get("Short") or LOAI.search((r["Tiêu đề"] or "") + (r["Kênh"] or "")):
        continue
    if not TAM_LY.search(r["Tiêu đề"] or ""):
        continue
    m = r["Mã video"]
    cu = theo_ma.get(m)
    if cu is None or n_(r["Lượt xem"]) > n_(cu["Lượt xem"]):
        theo_ma[m] = dict(r, so_luot=1)
    else:
        cu["so_luot"] += 1
    if cu is not None and cu is not theo_ma[m]:
        theo_ma[m]["so_luot"] = cu["so_luot"] + 1
moi = []
for r in theo_ma.values():
    ng = d_(r["Đăng"])
    if ng and ng >= MOC:
        tuoi = max((HOM_NAY - ng).days, 1)
        moi.append((n_(r["Lượt xem"]) / tuoi, n_(r["Lượt xem"]), tuoi, r))
moi.sort(key=lambda x: (x[0], x[1]), reverse=True)
out.append(f"\nA1. Video TÂM LÝ trên trang chủ đăng ≤ 21 ngày (khử trùng, {len(moi)} video), xếp theo view/ngày:")
for vpd, v, tuoi, r in moi[:45]:
    out.append(f"  {v:>8.0f} view · {vpd:>6.0f}/ngày · {tuoi:>2}d · {r['Dài']:>6} · {r['Kênh'][:16]:16} · già:{'CÓ' if GIA.search(r['Tiêu đề']) else '-':3} · {'/'.join(chu_de(r['Tiêu đề']))[:26]:26} · {r['Tiêu đề'][:70]}")
# A2. video tâm lý (mọi tuổi) hiện trên trang chủ nhiều lượt nhất
lap = sorted(theo_ma.values(), key=lambda r: -r["so_luot"])
out.append("\nA2. Video tâm lý máy đẩy lên trang chủ LẶP LẠI nhiều lượt nhất:")
for r in lap[:15]:
    out.append(f"  {r['so_luot']} lượt · {n_(r['Lượt xem']):>8.0f} view · đăng {r['Đăng']} · {r['Kênh'][:16]:16} · {r['Tiêu đề'][:70]}")
# A3. chủ đề trên trang chủ ≤21 ngày
dem = {}
for vpd, v, tuoi, r in moi:
    for c in chu_de(r["Tiêu đề"]) or ["(khác)"]:
        d = dem.setdefault(c, [0, 0, 0, set()])
        d[0] += 1; d[1] += v; d[2] = max(d[2], v); d[3].add(r["Kênh"])
out.append("\nA3. Chủ đề trên trang chủ (video ≤21 ngày): số video · tổng view · max · số kênh")
for c, (n, tv, mx, ks) in sorted(dem.items(), key=lambda x: -x[1][1]):
    out.append(f"  {c:28} {n:3} video · {tv:>8.0f} view · max {mx:>7.0f} · {len(ks)} kênh")

# ---------- B. SỔ ĐỐI THỦ ----------
ct = list(csv.DictReader(io.open(os.path.join(NC, "content.csv"), encoding="utf-8-sig")))
subs = {}
try:
    for r in csv.DictReader(io.open(os.path.join(NC, "doi-thu.csv"), encoding="utf-8-sig")):
        if r.get("Kênh"):
            subs[r["Kênh"]] = r.get("Subs") or "?"
except Exception as e:
    out.append(f"(doi-thu.csv: {e})")
theo_kenh = {}
for r in ct:
    theo_kenh.setdefault(r["Kênh"], []).append(n_(r["View"]))
trung_vi = {k: statistics.median(v) for k, v in theo_kenh.items() if v}
moi2 = []
for r in ct:
    ng = d_(r["Ngày đăng"])
    if not ng or ng < MOC or ng.day == 9 and ng.month != 9:  # ngày giả (=09) của tháng cũ
        continue
    if LOAI.search((r["Tiêu đề video"] or "") + (r["Kênh"] or "")):
        continue
    v = n_(r["View"]); tv = trung_vi.get(r["Kênh"], 0) or 1
    tuoi = max((HOM_NAY - ng).days, 1)
    moi2.append((v / tv, v, v / tuoi, tuoi, r))
moi2.sort(key=lambda x: (x[0], x[1]), reverse=True)
moi.sort(key=lambda x: (x[0], x[1]), reverse=True)
out.append(f"\nB1. SỔ ĐỐI THỦ: video đăng ≤ 21 ngày ({len(moi2)}), xếp theo VƯỢT (view ÷ trung vị kênh):")
for vuot, v, vpd, tuoi, r in moi2[:45]:
    out.append(f"  ×{vuot:>5.1f} · {v:>7.0f} view · {vpd:>5.0f}/ngày · {tuoi:>2}d · {r['Thời lượng']:>6} · {r['Kênh'][:14]:14} · TV {trung_vi.get(r['Kênh'],0):>6.0f} · sub {subs.get(r['Kênh'],'?'):>7} · làm:{r['Đã làm'] or '-':4} · {(r['Tuyến / Kênh'] or '')[:12]:12} · già:{'CÓ' if GIA.search((r['Tiêu đề video'] or '')+(r['Hashtag'] or '')) else '-':3} · {r['Tiêu đề video'][:64]}")

# B2. chủ đề: toàn sổ vs 21 ngày; tỷ lệ thắng = % video ≥×3 trung vị kênh
out.append("\nB2. CHỦ ĐỀ — toàn sổ (không loại trừ) | 21 ngày gần: số video · số kênh · max · %thắng(≥×3 TV kênh) · kênh nhỏ(<10k sub) thắng")
for ten, p in CHU_DE:
    tat = [r for r in ct if re.search(p, r["Tiêu đề video"] or "") and not LOAI.search((r["Tiêu đề video"] or "") + (r["Kênh"] or ""))]
    def tk(rs):
        n = len(rs); ks = len(set(r["Kênh"] for r in rs)); mx = max((n_(r["View"]) for r in rs), default=0)
        th = sum(1 for r in rs if n_(r["View"]) >= 3 * (trung_vi.get(r["Kênh"], 0) or 1))
        nho = sum(1 for r in rs if n_(r["View"]) >= 3 * (trung_vi.get(r["Kênh"], 0) or 1) and n_(subs.get(r["Kênh"], "0")) < 10000)
        return n, ks, mx, (100 * th / n if n else 0), nho
    a = tk(tat)
    gan = [r for r in tat if (d_(r["Ngày đăng"]) or dt.date(2000, 1, 1)) >= MOC and not (d_(r["Ngày đăng"]).day == 9 and d_(r["Ngày đăng"]).month != 9)]
    b = tk(gan)
    out.append(f"  {ten:28} TOÀN: {a[0]:3} video/{a[1]:2} kênh · max {a[2]:>7.0f} · thắng {a[3]:4.0f}% · nhỏ thắng {a[4]:2} ‖ 21d: {b[0]:2} video/{b[1]:2} kênh · max {b[2]:>6.0f} · thắng {b[3]:3.0f}%")

io.open(os.path.join(os.path.dirname(__file__), "trend.txt"), "w", encoding="utf-8").write("\n".join(out))
print("ok")
