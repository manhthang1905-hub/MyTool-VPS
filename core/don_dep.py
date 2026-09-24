"""Dọn đĩa VPS sau khi video đã đăng — chỉ xoá thứ NẶNG không ai dùng lại nữa.

═══ VÌ SAO CÓ TỆP NÀY (18/09/2026) ═══

Chủ dự án: một video đăng xong rồi thì 5–6 GB ảnh cảnh + clip + mp3 giọng đọc
của lượt đó chỉ còn nằm chật đĩa VPS — chẳng ai mở lại. Muốn tool TỰ XOÁ, an
toàn, sau khi chắc chắn video đã lên sóng.

"An toàn" ở đây có ba lớp:

1. **Chỉ xoá thứ NẶNG, không đụng thứ NHỎ mà việc khác còn đọc.** `0-doi-thu.txt`
   (chặn remake trùng nguồn, `core/da_lam.py`), `1-*.txt`/`3-phu-de.srt`/
   `4-canh.json` (`core/chi_so_ytb.su_that_tu_luot`, dùng làm chuẩn so cho vòng
   chấm-sửa lượt sau), `trang-thai.json`, `_van-tay-*.json` (so nội dung để biết
   "đã có sẵn" — `core/auto_khau.VanTay`), và tấm ảnh bìa ĐÃ CHỌN — không tệp nào
   trong số này to, và xoá đi là làm hỏng một tính năng khác đang sống nhờ nó.
   Chỉ `5-anh/`, `6-clip/`, `8-video.mp4`, `9-video-capcut.mp4`,
   `2-giong-doc.mp3`, ảnh bìa CHƯA chọn, và tệp tạm `*.tam` mới bị xoá.

2. **Chỉ xoá lượt đã ĐĂNG THẬT, và chỉ sau một hạn ân xá.** Đọc đúng dòng kế
   hoạch (`core/ke_hoach_dang.py`) — "Trạng thái đăng" phải là "ĐÃ ĐĂNG" (máy) hay
   "ĐÃ ĐĂNG (tay)" (`core/ban_giao_dang.TRANG_THAI_DANG_TAY`). Hạn ân xá
   (`don_sau_gio` trong `kenh.yaml`, mặc định 24 giờ) chừa chỗ cho ca YouTube xử
   lý hỏng phải tải lại. Và nếu `8-video.mp4` mới hơn cả lúc đăng — tức có ai vừa
   dựng lại — thì bỏ qua cả lượt, không đoán mò lý do.

3. **Không bao giờ đi ra khỏi hai thư mục được phép.** Mọi đường xoá đều được
   `os.path.realpath` rồi kiểm nằm THẬT SỰ trong `PROJECTS/AUTO/<kênh>/` (thư
   mục lượt) hoặc thư mục `thu_muc_done` của kênh (gói bàn giao) — lệch một chữ
   trong tên lượt/CSV cũng không đủ để đường xoá trồi ra ngoài. Không theo
   symlink/junction: gặp là bỏ qua, không xoá.

Mặc định của MỌI hàm ở đây là **không xoá gì** (`thuc_hien=False`) — trả về kế
hoạch để nơi gọi (hoặc người) xem trước. Chỉ khi kênh khai `tu_don: true` trong
`kenh.yaml` thì `don_theo_cai_dat` mới cho xoá thật; mặc định của khoá đó cũng
là tắt.

Không mạng, không Qt, không phụ thuộc phần còn lại của tool.
"""

from __future__ import annotations

import datetime
import glob
import json
import os
import shutil
import stat as _stat
from typing import Any, Callable, Dict, List, Optional, Sequence

from . import ban_giao_dang, ke_hoach_dang, ghi_dia
from .auto import duong_luot
from .kenh import doc_kenh

__all__ = [
    "TEN_MARKER", "TEN_LOG", "TRANG_THAI_DA_DANG",
    "ung_vien_don", "don", "don_tat_ca", "don_theo_cai_dat", "don_khan",
]

#: Tên tệp đánh dấu "lượt này đã dọn", nằm ngay trong thư mục lượt.
TEN_MARKER = "da-don.json"
#: Nhật ký gộp của kênh, nằm ở `CHANNEL/<kênh>/tu-chay/` — cùng thư mục sổ ngày
#: của `core/tu_chay.py`.
TEN_LOG = "don-dep.log"

#: Hai chuỗi trạng thái coi là "đã đăng thật" — máy tự đăng hoặc chủ đăng tay.
TRANG_THAI_DA_DANG = ("ĐÃ ĐĂNG", ban_giao_dang.TRANG_THAI_DANG_TAY)

#: Tệp/thư mục NẶNG trong một lượt — tên đúng bằng sản phẩm khâu, xem `core/auto.KHAU`.
_MUC_NANG = ("5-anh", "6-clip", "8-video.mp4", "9-video-capcut.mp4", "2-giong-doc.mp3")

_THU_MUC_THUMB = "7-thumbnail"

#: Cờ reparse point của Windows (junction, symlink thư mục) — `stat` định nghĩa
#: hằng này trên mọi hệ điều hành dù chỉ có ý nghĩa trên Windows.
_CO_REPARSE = getattr(_stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0x400)


# ── Đường dẫn an toàn ────────────────────────────────────────────────────────


def _la_lien_ket(duong: str) -> bool:
    """`True` nếu `duong` là symlink hay junction — đừng đi theo, đừng xoá xuyên."""
    try:
        st = os.lstat(duong)
    except OSError:
        return False
    if _stat.S_ISLNK(st.st_mode):
        return True
    return bool(getattr(st, "st_file_attributes", 0) & _CO_REPARSE)


def _duong_thuc(duong: str) -> str:
    return os.path.normcase(os.path.normpath(os.path.realpath(duong)))


def _trong_thu_muc(duong: str, cha: str) -> bool:
    """`True` nếu `duong` nằm THẬT SỰ (đã theo đường dẫn thực) bên trong `cha`."""
    if not duong or not cha:
        return False
    con = _duong_thuc(duong)
    goc = _duong_thuc(cha)
    return con != goc and (con + os.sep).startswith(goc + os.sep)


# ── Đọc kế hoạch đăng ────────────────────────────────────────────────────────


def _thoi_diem_dang(dong: Dict[str, str]) -> Optional[datetime.datetime]:
    """Ngày+giờ đăng của một dòng kế hoạch, hoặc `None` nếu chưa biết được.

    Trống thì trả `None` — kể cả cho lượt đăng tay: `ghi_nhan_dang_tay` chỉ đổi
    cột trạng thái của một dòng ĐÃ CÓ mà không đụng ngày giờ, nên trống ở đây có
    thể là "chưa ai từng ghi mốc" chứ không phải lỗi đọc. Chỗ gọi bỏ qua lượt
    này (đường an toàn) thay vì đoán một mốc không có thật.
    """
    ngay = (dong.get("Ngày đăng") or "").strip()
    gio = (dong.get("Giờ đăng") or "").strip()
    if not ngay:
        return None
    ngay_dt = None
    for mau in ("%d/%m/%Y", "%Y-%m-%d"):
        try:
            ngay_dt = datetime.datetime.strptime(ngay, mau)
            break
        except ValueError:
            continue
    if ngay_dt is None:
        return None
    if gio:
        for mau in ("%H:%M", "%H:%M:%S"):
            try:
                gio_t = datetime.datetime.strptime(gio, mau).time()
                return datetime.datetime.combine(ngay_dt.date(), gio_t)
            except ValueError:
                continue
    return ngay_dt


# ── Tìm thứ NẶNG còn lại trong một lượt ──────────────────────────────────────


def _kich_thuoc(duong: str) -> int:
    if os.path.isdir(duong):
        tong = 0
        for cha, _thu, tep in os.walk(duong):
            for t in tep:
                try:
                    tong += os.path.getsize(os.path.join(cha, t))
                except OSError:
                    pass
        return tong
    try:
        return os.path.getsize(duong)
    except OSError:
        return 0


def _anh_bia_chua_chon(thu_muc_luot: str) -> List[str]:
    """Ảnh bìa CHƯA được chọn — cùng luật chọn với `ban_giao_dang._tim_thumb`.

    Gọi thẳng hàm ấy để chắc chắn giữ ĐÚNG tấm mà bàn giao từng lấy: chưa ai bấm
    "Chọn" (không có `CHON-*`) thì bàn giao tự lấy tấm đầu theo bảng chữ cái —
    dọn dẹp phải giữ đúng tấm đó, không phải xoá sạch vì "không thấy CHON-".
    """
    thu_muc = os.path.join(thu_muc_luot, _THU_MUC_THUMB)
    if not os.path.isdir(thu_muc) or _la_lien_ket(thu_muc):
        return []
    giu = ban_giao_dang._tim_thumb(thu_muc_luot)  # noqa: SLF001 — dùng chung luật chọn
    ra = []
    try:
        ten_tep = sorted(os.listdir(thu_muc))
    except OSError:
        return []
    for ten in ten_tep:
        p = os.path.join(thu_muc, ten)
        if not os.path.isfile(p) or _la_lien_ket(p):
            continue
        if giu and os.path.normcase(os.path.abspath(p)) == os.path.normcase(os.path.abspath(giu)):
            continue
        ra.append(p)
    return ra


def _muc_nang_trong_luot(thu_muc_luot: str) -> List[str]:
    """Đường dẫn tuyệt đối mọi thứ NẶNG còn nằm trong một thư mục lượt."""
    ra: List[str] = []
    for ten in _MUC_NANG:
        p = os.path.join(thu_muc_luot, ten)
        if os.path.exists(p) and not _la_lien_ket(p):
            ra.append(p)
    ra.extend(_anh_bia_chua_chon(thu_muc_luot))
    try:
        ra.extend(
            p for p in glob.glob(os.path.join(thu_muc_luot, "**", "*.tam"), recursive=True)
            if os.path.isfile(p) and not _la_lien_ket(p)
        )
    except OSError:
        pass
    return ra


# ── Ứng viên ─────────────────────────────────────────────────────────────────


def ung_vien_don(goc: str, ma_kenh: str, *,
                 bay_gio: Optional[datetime.datetime] = None,
                 cho_gio: Optional[float] = None) -> List[Dict[str, Any]]:
    """Những lượt của `ma_kenh` đủ điều kiện dọn NGAY BÂY GIỜ.

    Mỗi phần tử: `{"kenh", "luot", "ma_goi", "thu_muc_luot", "duong" (danh sách
    đường tuyệt đối sẽ xoá), "bytes"}`. Không xoá gì ở đây — hàm này chỉ ĐỌC.
    """
    if bay_gio is None:
        bay_gio = datetime.datetime.now()
    kenh = doc_kenh(goc, ma_kenh)
    if cho_gio is None:
        cho_gio = kenh.don_sau_gio
    han = datetime.timedelta(hours=max(0.0, float(cho_gio)))

    auto_goc = os.path.join(goc, "PROJECTS", "AUTO", ma_kenh)
    thu_muc_done = (kenh.thu_muc_done or "").strip()

    cot, hang = ke_hoach_dang.doc_bang(goc, ma_kenh)
    if "Mã gói" not in cot or "Trạng thái đăng" not in cot:
        return []
    tien_to = ma_kenh + "-"

    o_ma = cot.index("Mã gói")
    da_thay: set = set()
    trung: set = set()
    for hang_tho in hang:
        ma = (hang_tho[o_ma] if o_ma < len(hang_tho) else "").strip()
        if not ma:
            continue
        if ma in da_thay:
            trung.add(ma)
        da_thay.add(ma)

    ra: List[Dict[str, Any]] = []
    for hang_tho in hang:
        dong = {ten: (hang_tho[i] if i < len(hang_tho) else "") for i, ten in enumerate(cot)}
        ma = (dong.get("Mã gói") or "").strip()
        if not ma or ma in trung:
            # Mã trùng nhiều dòng — không còn "MỘT" dòng rõ ràng để tin theo,
            # bỏ qua thay vì đoán dòng nào đúng.
            continue
        if (dong.get("Trạng thái đăng") or "").strip() not in TRANG_THAI_DA_DANG:
            continue
        if not ma.startswith(tien_to):
            continue  # sổ của kênh khác lẫn vào, hoặc mã không đúng khuôn — bỏ qua
        luot = ma[len(tien_to):]
        if not luot:
            continue

        thu_muc_luot = duong_luot(goc, ma_kenh, luot)
        # Phải nằm ĐÚNG một cấp dưới AUTO/<kênh> — chặn mã lượt mang "..\" hay "/".
        if os.path.normcase(os.path.normpath(os.path.dirname(thu_muc_luot))) \
                != os.path.normcase(os.path.normpath(auto_goc)):
            continue
        if not os.path.isdir(thu_muc_luot) or _la_lien_ket(thu_muc_luot):
            continue
        if not _trong_thu_muc(thu_muc_luot, auto_goc):
            continue

        moc = _thoi_diem_dang(dong)
        if moc is None:
            continue
        if bay_gio - moc < han:
            continue

        video = os.path.join(thu_muc_luot, "8-video.mp4")
        if os.path.isfile(video) and os.path.getmtime(video) > moc.timestamp():
            continue  # video mới hơn lúc đăng — vừa dựng lại, đừng đụng

        duong_xoa = _muc_nang_trong_luot(thu_muc_luot)

        goi_duong = ""
        if thu_muc_done:
            ung = os.path.join(thu_muc_done, ma)
            if os.path.isdir(ung) and not _la_lien_ket(ung) \
                    and _trong_thu_muc(ung, thu_muc_done):
                goi_duong = ung
        if goi_duong:
            duong_xoa.append(goi_duong)

        if not duong_xoa:
            continue  # đã sạch từ trước — không có gì để dọn

        ra.append({
            "kenh": ma_kenh,
            "luot": luot,
            "ma_goi": ma,
            "thu_muc_luot": thu_muc_luot,
            "duong": duong_xoa,
            "bytes": sum(_kich_thuoc(p) for p in duong_xoa),
            #: Mốc đăng THẬT của lượt này, dạng CHUỖI ISO (không phải `datetime`
            #: sống) — dùng để xếp thứ tự "cũ nhất trước" ở `don_khan` (dọn
            #: khẩn, xem đó). Chuỗi, không phải `datetime`, vì `dict` này có
            #: thể đi thẳng vào sổ ngày JSON (`core/tu_chay.py` ghi nguyên kết
            #: quả `don_khan` vào `run["dia"]["don_khan"]`) — `datetime` sống
            #: làm `json.dump` (không `default=`) ném lỗi giữa một lượt đang
            #: XOÁ DỞ, còn tệ hơn cả không ghi được sổ. Chuỗi ISO của cùng một
            #: định dạng vẫn so sánh CŨ/MỚI đúng bằng so sánh chuỗi thường.
            "moc_dang": moc.isoformat(),
        })
    return ra


# ── Xoá thật ─────────────────────────────────────────────────────────────────


def _duong_ghi_luot(thu_muc_luot: str, duong: str) -> str:
    """Đường hiển thị trong sổ: tương đối với thư mục lượt nếu nằm trong đó."""
    if _trong_thu_muc(duong, thu_muc_luot):
        return os.path.relpath(duong, thu_muc_luot).replace("\\", "/")
    return duong


def _ghi_marker(thu_muc_luot: str, ma_goi: str, da_xoa: Sequence[str],
                so_bytes: int, luc: datetime.datetime) -> None:
    ghi_dia.ghi_json(os.path.join(thu_muc_luot, TEN_MARKER), {
        "ma_goi": ma_goi,
        "luc": luc.strftime("%Y-%m-%d %H:%M:%S"),
        "bytes": so_bytes,
        "xoa": [_duong_ghi_luot(thu_muc_luot, p) for p in da_xoa],
    })


def _ghi_log(goc: str, ma_kenh: str, ma_goi: str, so_bytes: int,
            so_muc: int, luc: datetime.datetime) -> None:
    duong = os.path.join(goc, "CHANNEL", ma_kenh, "tu-chay", TEN_LOG)
    os.makedirs(os.path.dirname(duong), exist_ok=True)
    dong = "{0}\tgói {1}\txoá {2} mục\t{3} byte\n".format(
        luc.strftime("%Y-%m-%d %H:%M:%S"), ma_goi, so_muc, so_bytes)
    try:
        with open(duong, "a", encoding="utf-8") as tep:
            tep.write(dong)
    except OSError:
        pass  # nhật ký là để xem lại, không phải van an toàn — hỏng thì bỏ qua


def _xoa_mot_ung_vien(goc: str, ma_kenh: str, u: Dict[str, Any],
                      bay_gio: datetime.datetime) -> Optional[Dict[str, Any]]:
    """Xoá thật các đường trong MỘT ứng viên (một phần tử của `ung_vien_don`);
    ghi tệp đánh dấu + nhật ký nếu xoá được ít nhất một mục. Trả `None` nếu
    không xoá được gì (đã sạch từ trước, hoặc mọi đường đều là liên kết).

    Tách riêng khỏi `don()` để `don_khan` (dọn khẩn, xem đó) dùng lại ĐÚNG một
    cơ chế xoá — không viết lại luật an toàn (bỏ qua liên kết, ghi marker/log)
    ở một chỗ thứ hai."""
    da_xoa: List[str] = []
    for p in u["duong"]:
        if _la_lien_ket(p):
            continue
        try:
            if os.path.isdir(p):
                shutil.rmtree(p)
            elif os.path.isfile(p):
                os.remove(p)
            else:
                continue
        except OSError:
            continue
        da_xoa.append(p)
    if not da_xoa:
        return None
    _ghi_marker(u["thu_muc_luot"], u["ma_goi"], da_xoa, u["bytes"], bay_gio)
    _ghi_log(goc, ma_kenh, u["ma_goi"], u["bytes"], len(da_xoa), bay_gio)
    return {**u, "da_xoa": da_xoa}


def don(goc: str, ma_kenh: str, *, thuc_hien: bool = False,
        bay_gio: Optional[datetime.datetime] = None,
        cho_gio: Optional[float] = None) -> Dict[str, Any]:
    """Dọn các lượt đã đăng (quá hạn ân xá) của một kênh.

    `thuc_hien=False` (mặc định): chỉ TÍNH, không đụng đĩa — trả kế hoạch +
    tổng byte sẽ giải phóng. `thuc_hien=True`: xoá đúng những đường đã tính,
    ghi tệp đánh dấu `da-don.json` vào từng thư mục lượt và thêm một dòng vào
    `CHANNEL/<kênh>/tu-chay/don-dep.log`.

    Gọi lại nhiều lần là an toàn: lượt đã dọn sạch không còn gì NẶNG để tính
    vào ứng viên nữa (`ung_vien_don`), nên lần gọi sau không làm gì thêm.
    """
    if bay_gio is None:
        bay_gio = datetime.datetime.now()
    ke_hoach = ung_vien_don(goc, ma_kenh, bay_gio=bay_gio, cho_gio=cho_gio)
    ket_qua: Dict[str, Any] = {
        "kenh": ma_kenh,
        "thuc_hien": bool(thuc_hien),
        "ung_vien": ke_hoach,
        "tong_bytes": sum(u["bytes"] for u in ke_hoach),
    }
    if not thuc_hien:
        return ket_qua

    da_don: List[Dict[str, Any]] = []
    for u in ke_hoach:
        ket = _xoa_mot_ung_vien(goc, ma_kenh, u, bay_gio)
        if ket is not None:
            da_don.append(ket)
    ket_qua["da_don"] = da_don
    return ket_qua


def don_tat_ca(goc: str, kenh_list: Sequence[str], thuc_hien: bool) -> Dict[str, Dict[str, Any]]:
    """Gọi `don` cho từng kênh trong `kenh_list`. Trả `{mã kênh: kết quả}`."""
    return {ma: don(goc, ma, thuc_hien=thuc_hien) for ma in kenh_list}


def don_theo_cai_dat(goc: str, ma_kenh: str) -> Dict[str, Any]:
    """Dọn kênh này NẾU `kenh.yaml` bật `tu_don`; không thì báo lý do, không đụng gì.

    Cửa dọn THƯỜNG (cuối mỗi lượt `--tat-ca`, xem `core/tu_chay.chay_tat_ca`) —
    mặc định của `tu_don` là tắt, nên một kênh mới không tự nhiên bị dọn khi
    chủ chưa bật cờ. `don_khan` bên dưới là cửa DỌN KHẨN (giữa lượt, khi đĩa
    chạm ngưỡng an toàn) — cùng luật `tu_don`, không nới lỏng gì thêm.
    """
    kenh = doc_kenh(goc, ma_kenh)
    if not kenh.tu_don:
        return {"kenh": ma_kenh, "chay": False,
               "ly_do": "kênh chưa bật `tu_don` trong kenh.yaml — không đụng gì."}
    ket_qua = don(goc, ma_kenh, thuc_hien=True, cho_gio=kenh.don_sau_gio)
    ket_qua["chay"] = True
    return ket_qua


# ── Dọn KHẨN — đĩa chạm ngưỡng an toàn giữa lượt, hoặc vừa dính ENOSPC ───────


def _con_trong_gb(goc: str) -> Optional[float]:
    try:
        _tong, _dung, con = shutil.disk_usage(goc)
    except OSError:
        return None
    return con / 1024 ** 3


def don_khan(goc: str, danh_sach_kenh: Sequence[str], *, nguong_gb: float,
            bay_gio: Optional[datetime.datetime] = None,
            con_trong_gb_fn: Optional[Callable[[str], Optional[float]]] = None) -> Dict[str, Any]:
    """DỌN KHẨN — gọi từ `core/tu_chay.py` khi van đĩa trống thấy đĩa chạm/dưới
    ngưỡng an toàn (trước khi mở video mới), hoặc vừa dính lỗi ĐĨA ĐẦY
    (`ENOSPC`/`WinError 112`) giữa chừng sản xuất.

    ═══ AN TOÀN — GIỐNG HỆT DỌN THƯỜNG, KHÔNG NỚI LỎNG GÌ ═══

    Chỉ dọn kênh đã tự bật `tu_don: true` (cùng luật `don_theo_cai_dat`, cùng
    hạn ân xá `don_sau_gio` của từng kênh) — khẩn cấp không phải lý do để lật
    lại một cờ chủ dự án đã CHỌN tắt. Kênh chưa bật `tu_don` bị BỎ QUA hoàn
    toàn, dù đĩa có sắp đầy tới đâu; tên các kênh bị bỏ qua trả về trong
    `bo_qua_khong_tu_don` để nơi gọi ghi rõ vào sổ ngày (không giấu giới hạn
    này). Mọi luật an toàn khác (chỉ video ĐÃ ĐĂNG, chỉ thứ NẶNG, không đi ra
    ngoài `PROJECTS/AUTO/<kênh>/` hay `thu_muc_done`) đi qua nguyên `ung_vien_don`
    + `_xoa_mot_ung_vien` — không viết lại.

    ═══ THỨ TỰ: CŨ NHẤT TRƯỚC, DỪNG NGAY KHI ĐỦ ═══

    Gom ứng viên (`ung_vien_don`) của MỌI kênh trong `danh_sach_kenh` đã bật
    `tu_don`, xếp theo `moc_dang` tăng dần (lượt đăng lâu đời nhất trước — xa
    ngày đăng nhất thì ít khả năng còn cần xem/tải lại), rồi xoá TỪNG lượt một,
    đo lại dung lượng trống sau MỖI lượt, dừng ngay khi đã vượt `nguong_gb`
    hoặc hết ứng viên — không xoá quá tay khi đã đủ.

    Trả về `dict` có `da_chay` (có thật sự dọn gì không), `con_truoc_gb`/
    `con_sau_gb`, `da_giai_phong_bytes`, `theo_kenh` ({mã kênh: byte đã xoá}),
    `da_don` (chi tiết từng lượt đã xoá), `bo_qua_khong_tu_don`.
    """
    bay_gio = bay_gio or datetime.datetime.now()
    do_dia = con_trong_gb_fn or _con_trong_gb
    con_luc_dau = do_dia(goc)

    if con_luc_dau is not None and con_luc_dau >= nguong_gb:
        return {"da_chay": False, "con_truoc_gb": con_luc_dau, "con_sau_gb": con_luc_dau,
               "da_giai_phong_bytes": 0, "theo_kenh": {}, "da_don": [],
               "bo_qua_khong_tu_don": [],
               "ly_do": "đĩa còn {0:.1f} GB, đã ≥ ngưỡng {1:.1f} GB — không cần dọn khẩn."
                       .format(con_luc_dau, nguong_gb)}

    ung_vien_tat_ca: List[Dict[str, Any]] = []
    bo_qua: List[str] = []
    for ma in danh_sach_kenh:
        try:
            kenh = doc_kenh(goc, ma)
        except Exception:  # noqa: BLE001 — một kênh đọc hỏng không được chặn cả lượt dọn khẩn
            continue
        if not kenh.tu_don:
            bo_qua.append(ma)
            continue
        try:
            ung_vien_tat_ca.extend(ung_vien_don(goc, ma, bay_gio=bay_gio, cho_gio=kenh.don_sau_gio))
        except Exception:  # noqa: BLE001 — kế hoạch đăng của MỘT kênh hỏng không chặn kênh khác
            continue

    # Chuỗi ISO cùng định dạng so được CŨ/MỚI đúng bằng so sánh chuỗi thường —
    # thiếu (không nên xảy ra, `ung_vien_don` luôn kèm mốc) thì đẩy xuống CUỐI
    # (`"￿"`, sau mọi chuỗi ngày thật) — an toàn hơn: không đoán bừa một
    # lượt không rõ tuổi là "cũ nhất", đứng xoá trước tiên.
    ung_vien_tat_ca.sort(key=lambda u: u.get("moc_dang") or "￿")

    theo_kenh: Dict[str, int] = {}
    da_don: List[Dict[str, Any]] = []
    tong_bytes = 0
    con_hien_tai = con_luc_dau
    for u in ung_vien_tat_ca:
        if con_hien_tai is not None and con_hien_tai >= nguong_gb:
            break
        ket = _xoa_mot_ung_vien(goc, u["kenh"], u, bay_gio)
        if ket is None:
            continue
        da_don.append(ket)
        theo_kenh[u["kenh"]] = theo_kenh.get(u["kenh"], 0) + int(u["bytes"])
        tong_bytes += int(u["bytes"])
        con_hien_tai = do_dia(goc)

    return {"da_chay": True, "con_truoc_gb": con_luc_dau, "con_sau_gb": con_hien_tai,
           "da_giai_phong_bytes": tong_bytes, "theo_kenh": theo_kenh, "da_don": da_don,
           "bo_qua_khong_tu_don": bo_qua}
