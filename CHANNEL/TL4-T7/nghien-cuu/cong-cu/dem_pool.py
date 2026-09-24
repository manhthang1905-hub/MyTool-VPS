# -*- coding: utf-8 -*-
"""Đếm pool đúng ngách + bảng tuổi + tỷ lệ lượt/người theo từng mốc, cho TL4-T7."""
import csv, glob, io, json, os, re, sys

GOC = r"D:\New folder\shopapi\tools\kho-github\CHANNEL\TL4-T7\chi-so"
MANH = "心理 メンタル 脳科学 HSP 内向 自己肯定感 生きづらい 繊細さん 考えすぎ 劣等感 承認欲求 アドラー ユング 認知 うつ 不安障害 愛着".split()
YEU = "人間関係 孤独 感情 不安 ストレス 性格 幸せ 人生 疲れ 一人 1人 ひとり 習慣 自分を 強い人 特徴 理由".split()
LOAI = "漫画 アニメ 速報 野球 サッカー ゲーム 反応集 スカッと 2ch ２ｃｈ ゆっくり ドラマ BGM 音楽 料理 ホラー ニュース 政治 海外の反応 恋愛 雑学".split()


def loai_tieu_de(t):
    if any(k in t for k in LOAI):
        return "loai"
    if any(k in t for k in MANH):
        return "dung"
    if sum(1 for k in YEU if k in t) >= 2:
        return "dung"
    return "khac"


def so_gio(p):
    m = re.match(r"(\d+)h$", os.path.basename(p))
    return int(m.group(1)) if m else -1


def doc_pool(vid):
    thu = [d for d in glob.glob(os.path.join(GOC, vid, "*h")) if os.path.isfile(os.path.join(d, "traffic-related.csv"))]
    if not thu:
        return None
    thu = [d for d in thu if os.path.isfile(os.path.join(d, "tong-quan.json"))]
    if not thu:
        return None
    d = max(thu, key=so_gio)
    tong_imp = 0; tong_view = 0
    nhom = {"dung": [0, 0, 0], "loai": [0, 0, 0], "khac": [0, 0, 0]}
    top_dung = []
    with io.open(os.path.join(d, "traffic-related.csv"), encoding="utf-8-sig") as f:
        for r in csv.DictReader(f):
            if r["Traffic source"] == "Total":
                tong_imp = float(r["Thumbnail impressions"] or 0); tong_view = float(r["Views"] or 0); continue
            imp = float(r["Thumbnail impressions"] or 0); v = float(r["Views"] or 0)
            k = loai_tieu_de(r.get("Source title") or "")
            nhom[k][0] += 1; nhom[k][1] += imp; nhom[k][2] += v
            if k == "dung":
                top_dung.append((imp, v, r.get("Thumbnail click-through rate (%)"), r.get("Average view duration"), (r.get("Source title") or "")[:70]))
    phu = sum(x[1] for x in nhom.values())
    tq = json.load(io.open(os.path.join(d, "tong-quan.json"), encoding="utf-8"))
    return dict(moc=so_gio(d), tong_imp_bang=tong_imp, tong_view_bang=tong_view, phu_imp=phu,
                imp_video=tq.get("impressions"), nhom=nhom, top_dung=sorted(top_dung, reverse=True)[:12])


def tuoi_theo_moc(vid):
    ra = []
    for d in sorted(glob.glob(os.path.join(GOC, vid, "*")), key=lambda p: (so_gio(p) if so_gio(p) >= 0 else 9999, p)):
        tq = os.path.join(d, "tong-quan.json")
        if not os.path.isfile(tq):
            continue
        q = json.load(io.open(tq, encoding="utf-8"))
        ra.append((os.path.basename(d), q.get("impressions"), q.get("views"), q.get("views_that"), q.get("unique_viewers"),
                   q.get("avd_tren_so_luot"), q.get("tuoi") or {}, q.get("nguoi_xem") or {}, q.get("vung") or {}))
    return ra


out = []
for vid in ["32CA4WuHgVc", "v4qSum0iCMg", "dR8fA42KTCY", "2sOMyQxOdKE", "UpkC5cEO_VA", "0fAIs-DTgw8"]:
    out.append("=" * 60 + "\n" + vid)
    p = doc_pool(vid)
    if p:
        out.append(f"  pool @{p['moc']}h: bảng {p['tong_imp_bang']:.0f} imp / {p['tong_view_bang']:.0f} view; các dòng cộng {p['phu_imp']:.0f} imp; video {p['imp_video']} imp"
                   f" → bảng phủ {100*p['tong_imp_bang']/max(p['imp_video'] or 1,1):.1f}% hiển thị video")
        for k, (n, imp, v) in p["nhom"].items():
            out.append(f"    {k:5} {n:4} nguồn  {imp:7.0f} imp ({100*imp/max(p['phu_imp'],1):5.1f}%)  {v:5.0f} view")
        out.append("    top đúng ngách:")
        for imp, v, ctr, avd, t in p["top_dung"]:
            out.append(f"      {imp:5.0f} imp {v:4.0f} view ctr {ctr or '-':>6} avd {avd or '-':>8}  {t}")
    else:
        out.append("  (chưa có traffic-related.csv)")
    out.append("  tuổi / lượt-người theo mốc:")
    for moc, imp, v, vt, uq, v_bang, tuoi, nx, vung in tuoi_theo_moc(vid):
        if not tuoi and not uq:
            continue
        t = " ".join(f"{k.replace('AGE_','')}:{x}" for k, x in tuoi.items())
        out.append(f"    {moc:>14} imp {imp} view {v} thật {vt} người {uq} view_bảng {v_bang} | {t} | ngxem {nx} | vùng {vung}")

# kênh theo ngày: tuổi
out.append("=" * 60 + "\nKÊNH 28 ngày — bảng tuổi theo ngày")
for d in sorted(glob.glob(os.path.join(GOC, "kenh", "kenh-*"))):
    tq = os.path.join(d, "tong-quan.json")
    if os.path.isfile(tq):
        q = json.load(io.open(tq, encoding="utf-8"))
        if q.get("tuoi"):
            out.append(f"  {os.path.basename(d)}: " + " ".join(f"{k.replace('AGE_','')}:{x}" for k, x in q["tuoi"].items())
                       + f" | view {q.get('views')} giờ {q.get('watch_hours')} sub {q.get('subs')} imp {q.get('impressions')} ctr {q.get('ctr')} avd {q.get('avd_pct')}")

# giữ chân + giờ đăng
for vid in ["32CA4WuHgVc", "v4qSum0iCMg"]:
    out.append("=" * 60 + "\n" + vid + " — retention + thông tin")
    for f in glob.glob(os.path.join(GOC, vid, "*", "retention*")):
        out.append("  retention: " + f)
    for f in sorted(glob.glob(os.path.join(GOC, vid, "*", "_thong-tin.json")))[-2:]:
        out.append("  " + f + ": " + io.open(f, encoding="utf-8").read().strip())

io.open(os.path.join(os.path.dirname(__file__), "pool.txt"), "w", encoding="utf-8").write("\n".join(out))
print("ok", len(out))
