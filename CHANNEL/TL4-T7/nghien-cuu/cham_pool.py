# -*- coding: utf-8 -*-
"""CÔNG THỨC V7 — CHẤM POOL ĐỀ XUẤT (17/09/2026)

Nguồn: bảng "video đề xuất dẫn khách sang video mình" (YT_RELATED) của các video
chạy theo công thức V7, lấy bản chụp mới nhất trong chi-so/ (csv đủ dòng hoặc raw
Studio top 50).

Với mỗi video nguồn S, gộp trên mọi video của mình V mà S xuất hiện:

    B (hệ số bấm) = (Σ lượt bấm thật + K) / (Σ hiển thị × mốc bấm của V + K)
    X (hệ số xem) = (Σ lượt xem × thời lượng xem / mốc xem của V + K) / (Σ lượt xem + K)
    ĐIỂM          = B × X

- Mốc bấm / mốc xem của V = dòng Tổng trong bảng đề xuất của chính V, nên video
  dài ngắn khác nhau vẫn so được.
- B > 1: khán giả của S bấm sang mình nhiều hơn trung bình hàng xóm.
  X > 1: họ ở lại lâu hơn trung bình. ĐIỂM > 1: mỗi lượt hiển thị cạnh S mang về
  nhiều giờ xem hơn trung bình.
- K = 10 lượt "trung bình giả định" cộng vào cả tử và mẫu: dòng 1–3 lượt xem
  không nhảy lên đầu bảng vì may rủi.

Chạy:  python cham_pool.py   → in top và ghi bang-diem-pool.csv (mở bằng trang tính, lọc).
"""
import csv
import glob
import io
import json
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')
GOC = os.path.dirname(os.path.abspath(__file__))
CS = os.path.join(os.path.dirname(GOC), 'chi-so')
K = 10
# Các video chạy theo công thức V7. Thêm video mới vào đây.
VIDEO_V7 = [('V7', '32CA4WuHgVc'), ('V10', '9nwb8g1tQK8'), ('V11', '2cmZWXmtNRU'), ('V12', 'dJMe6I5Ka4k')]
CUNG_CHU_DE = ['心理', '脳', '特徴', '賢い', 'お金持ち', '金持ち', '貧乏', '一人', '1人', '１人', '孤独', '精神年齢',
               '知能', 'IQ', '物欲', '習慣', '性格', 'メンタル', '共通', '豊か', 'お金', '貯金', '節約', '幸せ', '人間関係']
KHAC_CHU_DE = ['訃報', '総理', '議員', 'ニュース', '天気', '台風', '株', 'S&P', 'FOMC', '国債', '事件', 'プーチン',
               '爆笑', '選挙', 'デモ', 'NISA', '金利', '為替', '投資', '宮さま', 'ロシア', '中国', '米国']


def _giay(t):
    p = (t or '').split(':')
    return int(p[0]) * 3600 + int(p[1]) * 60 + int(p[2]) if len(p) == 3 else None


def _bang_raw(f):
    d = json.load(io.open(f, encoding='utf-8'))
    h = d.get('href', '')
    if 'ddr_value=YT_RELATED' not in h or 'dimension=TRAFFIC_SOURCE_DETAIL' not in h:
        return None
    res = {r['key']: r['value'] for r in d['response'].get('results', [])}
    t = (res.get('2__TOP_ENTITIES_TABLE_QUERY_KEY') or {}).get('resultTable')
    if not t:
        return None
    ids = t['dimensionColumns'][0]['strings']['values']
    # Mỗi chỉ số có hai cột: % trên tổng và số tuyệt đối. Chỉ cột tuyệt đối có 'total'.
    cot = {}
    for c in t['metricColumns']:
        for loai in ('counts', 'milliseconds', 'percentages'):
            if loai in c and 'total' in c[loai]:
                vals = list(c[loai]['values'])
                for i in c.get('undefinedValueIndices', []):
                    vals[i] = None
                cot[c['metric']['type']] = vals
    if 'EXTERNAL_VIEWS' not in cot:
        return None
    tong = {}
    for c in res['0__TOTALS_SUMS_QUERY_KEY']['resultTable']['metricColumns']:
        for loai in ('counts', 'milliseconds', 'percentages'):
            if loai in c:
                tong[c['metric']['type']] = c[loai].get('total')
    vids = (res.get('2__TOP_ENTITIES_TABLE_QUERY_KEY_TRAFFIC_SOURCE_DETAIL_ANALYTICS_REFERRER_VIDEO') or {})
    ten = {v['videoId']: v for v in vids.get('getCreatorVideos', {}).get('videos', [])}
    dong = []
    for i, s in enumerate(ids):
        lay = lambda k: (cot.get(k) or [None] * len(ids))[i]
        vid = s.split('.', 1)[1]
        avd = lay('AVERAGE_WATCH_TIME')
        dong.append(dict(vid=vid, imp=lay('VIDEO_THUMBNAIL_IMPRESSIONS') or 0, ctr=lay('VIDEO_THUMBNAIL_IMPRESSIONS_VTR'),
                         view=lay('EXTERNAL_VIEWS') or 0, avd=(avd / 1000 if avd is not None else None),
                         title=ten.get(vid, {}).get('title', ''), dai=ten.get(vid, {}).get('lengthSeconds')))
    return dict(imp=tong.get('VIDEO_THUMBNAIL_IMPRESSIONS') or 0, ctr=tong.get('VIDEO_THUMBNAIL_IMPRESSIONS_VTR'),
                view=tong.get('EXTERNAL_VIEWS') or 0, avd=(tong.get('AVERAGE_WATCH_TIME') or 0) / 1000,
                dong=dong, f=f)


def _bang_csv(f):
    rows = list(csv.DictReader(io.open(f, encoding='utf-8-sig')))
    if not rows or int(rows[0].get('Thumbnail impressions') or 0) == 0:
        return None
    dong = []
    for r in rows[1:]:
        if '.' not in (r['Traffic source'] or ''):
            continue
        c = r['Thumbnail click-through rate (%)']
        dong.append(dict(vid=r['Traffic source'].split('.', 1)[1], imp=int(r['Thumbnail impressions'] or 0),
                         ctr=float(c) if c not in ('', None) else None, view=int(float(r['Views'] or 0)),
                         avd=_giay(r['Average view duration']), title=r['Source title'], dai=None))
    t = rows[0]
    return dict(imp=int(t['Thumbnail impressions']), ctr=float(t['Thumbnail click-through rate (%)']),
                view=int(float(t['Views'])), avd=_giay(t['Average view duration']), dong=dong, f=f)


def bang_moi_nhat(vid):
    ung = []
    for f in glob.glob(os.path.join(CS, vid, '*', 'raw', '*join*')):
        try:
            b = _bang_raw(f)
        except (ValueError, KeyError):
            b = None
        if b:
            ung.append(b)
    for f in glob.glob(os.path.join(CS, vid, '*', 'traffic-related.csv')):
        b = _bang_csv(f)
        if b:
            ung.append(b)
    # Tổng hiển thị lớn nhất = bản mới nhất; hoà thì lấy bản nhiều dòng hơn.
    return max(ung, key=lambda b: (b['imp'], b['view'], len(b['dong']))) if ung else None


def cham():
    bang = {}
    for ten, vid in VIDEO_V7:
        b = bang_moi_nhat(vid)
        if b and b['ctr'] and b['avd']:
            bang[ten] = b
    cua_minh = {vid for _, vid in VIDEO_V7}
    for f in glob.glob(os.path.join(CS, '*')):
        if os.path.isdir(f) and len(os.path.basename(f)) == 11:
            cua_minh.add(os.path.basename(f))
    nguon = {}
    for ten, b in bang.items():
        for r in b['dong']:
            if r['vid'] in cua_minh:
                continue
            g = nguon.setdefault(r['vid'], dict(title='', dai=None, bt=0.0, bk=0.0, xv=0.0, xn=0, imp=0, view=0, tu={}))
            g['title'] = g['title'] or r['title']
            g['dai'] = g['dai'] or r['dai']
            g['tu'][ten] = r
            g['imp'] += r['imp']
            g['view'] += r['view']
            if r['imp'] and r['ctr'] is not None:
                g['bt'] += r['imp'] * r['ctr'] / 100
                g['bk'] += r['imp'] * b['ctr'] / 100
            if r['view'] and r['avd'] is not None:
                g['xv'] += r['view'] * r['avd'] / b['avd']
                g['xn'] += r['view']
    for g in nguon.values():
        g['B'] = (g['bt'] + K) / (g['bk'] + K)
        g['X'] = (g['xv'] + K) / (g['xn'] + K)
        g['D'] = g['B'] * g['X']
    return bang, nguon


def main():
    bang, nguon = cham()
    for ten, b in bang.items():
        print('%-4s mốc bấm %.2f%% · mốc xem %d:%02d · %d dòng · %s' % (
            ten, b['ctr'], b['avd'] // 60, b['avd'] % 60, len(b['dong']), os.path.relpath(b['f'], CS)))
    so = {}
    for r in csv.DictReader(io.open(os.path.join(GOC, 'content.csv'), encoding='utf-8-sig')):
        v = (r.get('Link video') or '').split('v=')[-1].split('&')[0]
        if v:
            so[v] = r
    ra = os.path.join(GOC, 'bang-diem-pool.csv')
    with io.open(ra, 'w', encoding='utf-8-sig', newline='') as fo:
        w = csv.writer(fo)
        w.writerow(['Điểm', 'Hệ số bấm', 'Hệ số xem', 'Lượt xem sang kênh mình', 'Hiển thị', 'Có ở video',
                    'Cùng chủ đề', 'Mã video', 'Tiêu đề', 'Kênh (sổ)', 'View (sổ)', 'Ngày đăng (sổ)', 'Link'])
        for k, g in sorted(nguon.items(), key=lambda kg: -kg[1]['D']):
            t = g['title']
            cung = 'x' if any(c in t for c in CUNG_CHU_DE) and not any(c in t for c in KHAC_CHU_DE) else ''
            s = so.get(k, {})
            w.writerow(['%.2f' % g['D'], '%.2f' % g['B'], '%.2f' % g['X'], g['view'], g['imp'], ','.join(g['tu']),
                        cung, k, t, s.get('Kênh', ''), s.get('View', ''), s.get('Ngày đăng', ''),
                        'https://www.youtube.com/watch?v=' + k])
    print('\nĐã ghi %s (%d nguồn)' % (ra, len(nguon)))
    print('\nTOP cùng chủ đề, điểm > 1, từ 10 lượt xem sang kênh mình:')
    for k, g in sorted(nguon.items(), key=lambda kg: -kg[1]['D']):
        t = g['title']
        if g['D'] <= 1 or g['view'] < 10:
            continue
        if not (any(c in t for c in CUNG_CHU_DE) and not any(c in t for c in KHAC_CHU_DE)):
            continue
        print('  %.2f  B %.2f X %.2f  %3d xem  %-12s %s  %s' % (g['D'], g['B'], g['X'], g['view'], ','.join(g['tu']), k, t[:60]))


if __name__ == '__main__':
    main()
