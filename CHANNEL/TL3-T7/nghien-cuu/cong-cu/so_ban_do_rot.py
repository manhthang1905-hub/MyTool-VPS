# -*- coding: utf-8 -*-
"""Đặt bản đồ rớt bộ chấm ĐOÁN (trong thư mục lượt) cạnh đường giữ chân THẬT (chi-so).

Chạy: python so_ban_do_rot.py <thư mục lượt> <mã video YouTube> [<mã kênh chi-so, mặc định TL4-T7>]
Ví dụ: python so_ban_do_rot.py "D:/.../PROJECTS/AUTO/TL4-T7-v2/0001" AbCdEfGhIjK

In ra các dòng sẵn để dán vào nghien-cuu/su-that-cham.txt — bộ chấm lần sau đọc được chỗ nó đoán sai.
"""
import io
import json
import os
import sys

GOC = r"D:\New folder\shopapi\tools\kho-github"
sys.path.insert(0, GOC)


def main() -> None:
    if len(sys.argv) < 3:
        print(__doc__)
        return
    luot, ma_video = sys.argv[1], sys.argv[2]
    kenh = sys.argv[3] if len(sys.argv) > 3 else "TL4-T7"
    from core.chi_so_ytb import doc_kenh
    from core.vong_cham_sua import so_voi_that

    tep = None
    for ten in ("1-ban-do-rot-cuoi.json", "1-ban-do-rot-ghep.json"):
        p = os.path.join(luot, ten)
        if os.path.isfile(p):
            tep = p
            break
    if not tep:
        print("Lượt này không có 1-ban-do-rot-*.json (kênh chưa bật so_vong_cham?)")
        return
    ban_do = json.load(io.open(tep, encoding="utf-8"))
    moi_nhat = None
    for b in doc_kenh(kenh, goc=os.path.join(GOC, "CHANNEL")):
        if b.video_id == ma_video and b.retention and (
                moi_nhat is None or (b.moc_gio or 0) >= (moi_nhat.moc_gio or 0)):
            moi_nhat = b
    if moi_nhat is None:
        print("Chưa có đường giữ chân của", ma_video, "trong chi-so — Studio thường trả sau vài ngày.")
        return
    dong = so_voi_that(ban_do, moi_nhat.retention)
    if not dong:
        print("Bản đồ rớt không có den_pct/con_lai — bộ chấm trả thiếu trường.")
        return
    print("Dán vào nghien-cuu/su-that-cham.txt:")
    print("- {0} ({1}, mốc {2}h) — bộ chấm đoán so với thật:".format(
        (moi_nhat.tieu_de or ma_video)[:48], ma_video, moi_nhat.moc_gio))
    for d in dong:
        print("  " + d)


if __name__ == "__main__":
    main()
