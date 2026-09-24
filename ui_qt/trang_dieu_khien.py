"""Trang **ĐIỀU KHIỂN** — màn hình mở đầu của máy VPS chạy kênh tự động.

Chủ dự án xem bản trước trên máy thật (1416×1039), 21/09/2026: *"cái giao diện
nó xấu quá"*, *"thiết kế lại all để phù hợp với tool auto trên vps này"*, *"vì
mọi thứ là auto nên nó sẽ cần các tính năng cả phần để kiểm soát quản lý"*.

═══ BỐN THỨ ĐO ĐƯỢC TRÊN ẢNH CHỤP, VÀ CÁCH TRANG NÀY CHỮA ═══

1. **40% cửa sổ phía dưới bỏ trống.** Bảng "Tiến độ" tám khâu nằm nép trong
   một mục tab bé tí, còn nửa dưới màn hình trắng trơn. Ở đây mỗi kênh là MỘT
   CỘT chạy hết chiều cao: tám khâu của `core/tu_chay.py` xếp dọc trong cột,
   nên chỗ trống ấy chính là chỗ chứa thông tin.
2. **Dải trên là bảy hộp to nhỏ lệch nhau**, và phơi tên khoá kỹ thuật
   (`tu_dang`, `tu_tra_loi_cmt`) ra mặt người dùng. Ở đây dải sức khoẻ chỉ còn
   những ô CÙNG CỠ, và mọi tên đều là tiếng Việt (`_TEN_MAY`).
3. **Dải đỏ nhồi sáu việc vào một dòng chạy dài.** Ở đây nó là một dòng ngắn
   "⚠ N việc cần xem" bấm để mở ra danh sách, việc nặng đứng trước.
4. **Thẻ kênh toàn dấu "—", tên tiếng Nhật cắt cụt giữa chừng.** Ở đây đầu cột
   là MÃ KÊNH + tên tệp khán giả ngắn gọn; tên Nhật đầy đủ nằm ở tooltip.

═══ LẦN DỌN THỨ HAI, 22/09/2026 ═══

Chủ dự án xem bản trên (1416×995): *"những gì đang hiển thị ở tab điều khiển
tao xem rất khó quản lý - rất khó hiểu nó đang như nào. tao nghĩ mỗi kênh có 1
mục cài đặt để cài giờ đăng rồi all các thứ để kiểm soát kênh đó - còn nội
dung ở ngoài thì cần thể hiện. nói chung nó là auto nên phải tối giản phải đơn
giản dễ dùng"*.

Nên chia làm hai tầng, dứt khoát:

* **Cột kênh = CHỈ TÌNH TRẠNG.** Đứng đầu cột là MỘT CÂU bằng lời thường
  ("Đang tạo ảnh — 116/141 cảnh"), chữ to nhất cột, bấm vào thì mở nhật ký
  của chính kênh ấy. Dưới nó: video hôm nay, dây chuyền tám khâu, một dòng
  số, và đúng hai nút. Ô "Hôm nay" chứa nhật ký thô, bốn ô tích và ô ngân
  sách ĐÃ RỜI KHỎI CỘT.
* **Hộp ⚙ Cài đặt của từng kênh** (`HopCaiDatKenh`) gom mọi núm vặn của đúng
  kênh đó: giờ đăng · phút mở phiên trước giờ đăng · bốn công tắc (tự chạy ·
  tự đăng · trả lời bình luận · tự dọn) · tiền mỗi ngày. Sửa là lưu ngay,
  không có nút Lưu. Chỗ lưu KHÔNG đổi: `kenh.yaml` cho những thứ về sản xuất,
  `may-ao.json` cho những thứ về máy ảo.

Của CẢ MÁY thì vẫn ở dải trên: tạm dừng tất cả · lịch chạy hằng ngày · ổ đĩa,
ví, tiền · dòng "N việc cần xem" (nay nhóm theo kênh, mỗi việc kèm một câu
nói làm gì tiếp theo).

═══ KHÔNG HỎI MÁY CHỦ ĐỂ LÀM MỚI ═══

CLAUDE.md luật 4, y như trang Trung tâm: đọc lại TỆP trên máy mỗi 30 giây, số
dư ví tối đa 5 phút một lần, lịch Windows 5 phút một lần.
"""

from __future__ import annotations

import re as _re
import time
from typing import Any, Dict, List, Optional

from PyQt5.QtCore import QLocale, Qt, QTime, QTimer, pyqtSignal
from PyQt5.QtWidgets import (
    QCheckBox, QDialog, QFrame, QHBoxLayout, QLabel, QMenu, QMessageBox,
    QPlainTextEdit, QScrollArea, QSpinBox, QTimeEdit, QVBoxLayout, QWidget,
)

from core import trung_tam as tt
from core.money import MICRO_PER_VND, format_vnd

from . import theme
from .trang_trung_tam import (
    GB_DIA_HONG, GB_DIA_LUU_Y, GIAY_HOI_LICH, GIAY_HOI_VI, HONG, LUU_Y,
    NHIP_LAM_MOI_MS, THUONG, VND_VI_HONG, VND_VI_LUU_Y, _CHU_BAO, _MAU_BAO,
    _TEN_MAY, _OChiSo, _cat, _giam_sat, _gon, _muc_bao, _nang, _pt, _ten_tep,
    _tep_ngan, _vnd_gon,
)
from .widgets import (HopXuongDong, gio_hhmm, lan_chay_gon, mo_thu_muc, nhan,
                      nut_phu, the)

__all__ = ["TrangDieuKhien", "CotKenh", "HopCaiDatKenh", "HopNhatKyKenh",
           "DAU_KHAU", "CHU_KHAU", "cau_tinh_trang", "tien_do_nhat_ky",
           "gon_dong_nhat_ky"]

#: Dấu đứng trước tên khâu. Mỗi dấu LUÔN đi kèm chữ (cột "Trạng thái" của
#: tooltip và chữ phụ bên phải) — người không phân biệt được màu vẫn đọc ra.
DAU_KHAU = {"xong": "✓", "dang": "◑", "cho": "○", "hong": "✕", "bo-qua": "–"}

#: Chữ cho từng trạng thái khâu — dùng ở tooltip và ở chữ phụ.
CHU_KHAU = {"xong": "xong", "dang": "đang chạy", "cho": "chờ", "hong": "LỖI",
            "bo-qua": "bỏ qua"}

_MAU_KHAU_CHU = {"xong": theme.XANH, "dang": theme.NHAN, "hong": theme.DO,
                 "bo-qua": theme.XAM}

#: Cắt phần KỸ THUẬT ra khỏi một dòng nhật ký trước khi cho lên màn hình.
#:
#: ═══ VÌ SAO ═══
#:
#: Chụp màn hình thật ngày 22/09/2026: ô "Hôm nay" của ba cột kênh cùng phơi
#: nguyên một vết lỗi Python hai mươi dòng —
#: `(FileNotFoundError: Could not find module 'C:\\Users\\...\\ctranslate2.dll'
#: (or one of its dependencies). Try using the full)` — lặp y hệt ba lần và
#: chiếm trọn khoảng giữa màn hình. Câu tiếng Việt hữu ích ("Dừng ở Viết kịch
#: bản: không lấy được lời thoại của video tư liệu… thường là máy thiếu bộ thư
#: viện chạy Visual C++") thì bị đẩy lún vào giữa đống chữ ấy.
#:
#: `CLAUDE.md`, mục "Cách viết cho hợp chỗ này": không dùng từ kỹ thuật trên
#: giao diện — khách không biết `FileNotFoundError` hay `ctranslate2.dll` là gì,
#: và người đọc màn hình này lúc 8 giờ sáng chỉ cần biết *kênh nào dừng ở khâu
#: nào vì chuyện gì*.
#:
#: Không XOÁ phần kỹ thuật — nó vẫn cần cho việc truy lỗi — mà dồn nguyên văn
#: vào tooltip của chính ô ấy.
_KY_THUAT = _re.compile(
    r"\((?:[A-Za-z_][A-Za-z0-9_.]*(?:Error|Exception|Warning)\b|[A-Za-z]:\\)"
    r"[^()]*(?:\([^()]*\)[^()]*)*\)"
)

#: Dài hơn chừng này thì cắt — đủ để đọc hết một câu, không đủ để tràn cột.
#: 210 chứ không phải 150: đo trên dòng lỗi thật (397 ký tự), mốc 150 cắt ngay
#: giữa chữ "thườ…" làm mất đúng câu hướng dẫn đáng giá nhất — *"thường là máy
#: thiếu bộ thư viện chạy Visual C++"*. Người đọc ô này cần câu ấy hơn là cần
#: ô ngắn.
_DAI_TOI_DA_MOT_DONG = 210


def gon_dong_nhat_ky(dong: str) -> str:
    """Một dòng nhật ký đã bỏ vết lỗi kỹ thuật và cắt cho vừa bề rộng cột."""
    chu = _KY_THUAT.sub("", str(dong or ""))
    chu = _re.sub(r"\s+", " ", chu).strip()
    # Dấu chấm/phẩy bị bỏ lại lơ lửng sau khi gỡ khối trong ngoặc.
    chu = _re.sub(r"\s+([.,;:])", r"\1", chu)
    chu = _re.sub(r"([(:,;]\s*)+$", "", chu).strip()
    if len(chu) > _DAI_TOI_DA_MOT_DONG:
        # Cắt ở RANH GIỚI, không cắt giữa chữ: ưu tiên hết câu (`.` `;`), không
        # có thì lùi về khoảng trắng gần nhất. Cắt giữa chữ vừa khó đọc vừa dễ
        # làm mất nghĩa của đúng mấy chữ cuối — thứ thường là lời khuyên.
        cat = chu[:_DAI_TOI_DA_MOT_DONG]
        for dau in (". ", "; ", ", "):
            i = cat.rfind(dau)
            if i >= _DAI_TOI_DA_MOT_DONG // 2:
                return cat[:i + 1].rstrip()
        i = cat.rfind(" ")
        chu = (cat[:i] if i >= _DAI_TOI_DA_MOT_DONG // 2 else cat).rstrip() + "…"
    return chu

#: Khoá `workspace/trung-tam.json` nhớ những kênh mà nút "Tạm dừng tất cả" đã
#: tắt — để nút "Bật lại" không bật nhầm kênh vốn đã tắt từ trước.
KHOA_TAM_DUNG = "tam_dung_kenh"


# ═══ MỘT CÂU TÌNH TRẠNG — THỨ ĐỌC ĐẦU TIÊN TRONG MỖI CỘT ════════════════════
#
# Chủ dự án, 22/09/2026: *"những gì đang hiển thị ở tab điều khiển tao xem rất
# khó quản lý - rất khó hiểu nó đang như nào"*. Cột cũ bắt người ta ghép câu
# trả lời từ bốn chỗ: dải trạng thái ngắn cụt, tám dấu khâu, ô nhật ký thô và
# hai con số. Ở đây mỗi cột nói MỘT CÂU, bằng lời thường, chữ to nhất cột.
#
# `core.trung_tam.trang_thai_bay_gio` đã cho sẵn một câu, nhưng nó viết cho ô
# hẹp của bảng cũ ("Đang làm video · khâu Ảnh", "Chờ duyệt", "Dở ở khâu Clip").
# Hàm dưới đây dịch nó sang lời nói và gắn thêm tiến độ. Không đụng `core/` —
# chỉ đọc lại đúng ảnh chụp đang có, không thêm một lượt hỏi nào.

#: Tám khâu nói thành VIỆC ĐANG LÀM.
VIEC_KHAU = {
    "kich-ban": "Đang viết kịch bản",
    "giong-doc": "Đang thu giọng đọc",
    "phu-de": "Đang làm phụ đề",
    "bang-canh": "Đang chia cảnh",
    "anh": "Đang tạo ảnh",
    "clip": "Đang tạo clip",
    "thumbnail": "Đang làm ảnh bìa",
    "dung": "Đang ghép video",
}

#: Đơn vị đếm của khâu — để "116/141" đọc thành "116/141 cảnh".
DON_VI_KHAU = {"bang-canh": "cảnh", "anh": "cảnh", "clip": "cảnh"}

#: Vòng tự chạy tự đánh số việc trong nhật ký bằng `[N/M]` (đo trên nhật ký
#: thật của cả ba kênh ngày 22/09/2026: 203–228 dòng có dấu này). Chỉ nhận dấu
#: trong NGOẶC VUÔNG — "22/09" hay một đường dẫn có gạch chéo không lọt vào.
_TIEN_DO = _re.compile(r"\[(\d{1,4})/(\d{1,4})\]")

#: Dấu đứng trước câu tình trạng. Luôn đi kèm CHỮ (chính là câu ấy) — người
#: không phân biệt được màu vẫn đọc ra kênh đang thế nào.
DAU_TINH_TRANG = {"dang": "◑", "cho": "⏱", "ok": "✓", "loi": "✕",
                  "canh_bao": "⚠", "nghi": "–", "tat": "–"}

#: Màu của viền + nền cột, theo đúng câu tình trạng. Bốn mức, không phải ba:
#: "đang chạy / chờ đăng / đã đăng" là kênh KHOẺ, và một cột trắng trơn không
#: nói được điều đó.
TOT = "tot"
_MAU_COT = {
    TOT: (theme.XANH, theme.XANH_NEN, theme.XANH_VIEN),
    LUU_Y: (theme.CAM, theme.VANG_NEN, theme.VANG_VIEN),
    HONG: (theme.DO, theme.DO_NEN, theme.DO_VIEN),
    THUONG: (theme.CHU, theme.THE, theme.VIEN),
}

#: Mức "Bây giờ" của `core` → màu cột.
_MUC_COT = {"dang": TOT, "cho": TOT, "ok": TOT, "loi": HONG, "canh_bao": LUU_Y}


def muc_mau_cot(muc_bay_gio: Any) -> str:
    """Mức màu của cột (`tot`/`luu_y`/`hong`/`thuong`) từ mức của `core`."""
    return _MUC_COT.get(str(muc_bay_gio or ""), THUONG)


def tien_do_nhat_ky(nhat_ky: Any) -> str:
    """`"116/141"` — tiến độ việc đang chạy, lấy từ dấu `[N/M]` của nhật ký."""
    for dong in reversed(list(nhat_ky or [])[-80:]):
        tim = _TIEN_DO.search(str(dong))
        if not tim:
            continue
        lam, tong = int(tim.group(1)), int(tim.group(2))
        if 1 <= lam <= tong and tong >= 2:
            return "{0}/{1}".format(lam, tong)
    return ""


def _cat_chu(chu: str, toi_da: int = 88) -> str:
    chu = str(chu or "").strip()
    if len(chu) <= toi_da:
        return chu
    cat = chu[:toi_da]
    i = cat.rfind(" ")
    return (cat[:i] if i >= toi_da // 2 else cat).rstrip() + "…"


def _khau_dang(k: Dict[str, Any], trang: str) -> Dict[str, Any]:
    for d in ((k.get("luot") or {}).get("khau") or []):
        if str(d.get("trang_thai") or "") == trang:
            return d
    return {}


def _viec_khau(ma_khau: str, ten_ngan: str = "") -> str:
    """"anh" → "Đang tạo ảnh"."""
    return VIEC_KHAU.get(ma_khau) or "Đang làm {0}".format(
        (ten_ngan or ma_khau or "video").lower())


def _lam_gi(ma_khau: str, ten_ngan: str = "") -> str:
    """"anh" → "tạo ảnh" — phần đuôi để ghép vào "Dừng khi …"."""
    viec = _viec_khau(ma_khau, ten_ngan)
    return viec[len("Đang "):] if viec.startswith("Đang ") else viec.lower()


def cau_tinh_trang(k: Dict[str, Any]) -> str:
    """MỘT câu tiếng Việt nói kênh này đang thế nào — thuần, bài kiểm gọi thẳng.

    Ví dụ: `Đang tạo ảnh — 116/141 cảnh` · `Xong, chờ bạn duyệt` ·
    `Đã hẹn đăng 20:00 hôm nay` · `Dừng khi tạo ảnh — máy chủ ảnh bận` ·
    `Hôm nay chưa chạy` · `Chỉ đăng, không sản xuất`.
    """
    bay = k.get("bay_gio") or {}
    goc = str(bay.get("chu") or "").strip()
    chi_tiet = str(bay.get("chi_tiet") or "").strip()

    if goc.startswith("Đang làm video"):
        d = _khau_dang(k, "dang")
        ma_khau = str(d.get("ma") or "")
        if ma_khau:
            cau = _viec_khau(ma_khau, str(d.get("ten_ngan") or ""))
        elif "khâu" in goc:
            cau = "Đang làm " + goc.split("khâu", 1)[1].strip().lower()
        else:
            cau = "Đang làm video"
        tien = tien_do_nhat_ky(k.get("nhat_ky"))
        if tien:
            dv = DON_VI_KHAU.get(ma_khau, "")
            cau += " — {0}{1}".format(tien, " " + dv if dv else "")
        return cau
    if goc.startswith("Đang chọn video"):
        return "Đang chọn video cho hôm nay"
    if goc.startswith("Đang đăng"):
        return "Đang đăng lên YouTube"

    if goc.startswith("Lỗi: khâu "):
        d = _khau_dang(k, "hong")
        ly_do = gon_dong_nhat_ky(str(d.get("loi") or chi_tiet))
        # `chi_tiet` của `core` là "Tạo ảnh từng cảnh: <lý do>" — bỏ phần tên
        # khâu đi, vì câu này đã tự nói kênh dừng ở việc nào rồi.
        if ":" in ly_do and not d.get("loi"):
            ly_do = ly_do.split(":", 1)[1].strip() or ly_do
        return _cat_chu("Dừng khi {0}{1}".format(
            _lam_gi(str(d.get("ma") or ""), str(d.get("ten_ngan") or "")),
            " — " + ly_do if ly_do else ""))
    if goc.startswith("Lỗi bàn giao"):
        ly_do = gon_dong_nhat_ky(chi_tiet)
        return _cat_chu("Dừng khi chuyển sang máy đăng"
                        + (" — " + ly_do if ly_do else ""))
    if goc.startswith("Lỗi"):
        ly_do = gon_dong_nhat_ky(goc.split(":", 1)[1] if ":" in goc else chi_tiet)
        return _cat_chu("Dừng vì " + (ly_do or "chưa rõ lý do"))

    if goc.startswith("Chờ duyệt"):
        return "Xong, chờ bạn duyệt"
    if goc.startswith("Đã đăng"):
        return "Đã lên sóng hôm nay"
    if goc.startswith("Chờ đăng "):
        return "Đã hẹn đăng {0} hôm nay".format(goc[len("Chờ đăng "):].strip())
    if goc.startswith("Chờ phiên "):
        gio = str(k.get("dang_luc") or "").split()[-1:] or [""]
        return ("Đã hẹn đăng {0} hôm nay".format(gio[0]) if gio[0]
                else "Đã hẹn đăng hôm nay")
    if goc.startswith("Hẹn đăng "):
        phan = goc[len("Hẹn đăng "):].split()
        if len(phan) == 2:
            return "Đã hẹn đăng {1} ngày {0}".format(phan[0], phan[1])
        return "Đã hẹn đăng " + " ".join(phan)
    if goc.startswith("Quá giờ đăng "):
        return "Quá giờ đăng {0} mà chưa thấy lên sóng".format(
            goc[len("Quá giờ đăng "):].strip())
    if goc.startswith("Xong, chưa bàn giao"):
        return "Xong, chưa chuyển sang máy đăng"
    if goc.startswith("Nghỉ: vượt trần tiền"):
        return "Nghỉ vì đã tiêu hết tiền hôm nay"
    if goc.startswith("Dở ở khâu "):
        d = _khau_dang(k, "cho") or _khau_dang(k, "dang")
        return "Dở dang ở {0} — lượt sau làm tiếp".format(
            _lam_gi(str(d.get("ma") or ""), goc[len("Dở ở khâu "):].strip()))
    if goc.startswith("Chưa đặt trần tiền"):
        return "Chưa đặt tiền mỗi ngày — chưa sản xuất được"
    if goc.startswith("Nghỉ hôm nay"):
        return "Hôm nay nghỉ, không có video mới"
    if goc.startswith("Chờ lịch "):
        return "Chờ tới {0} rồi tự chạy".format(goc[len("Chờ lịch "):].strip())
    if goc.startswith("Chưa bật lịch"):
        return "Lịch hằng ngày đang tắt — sẽ không tự chạy"
    if goc.startswith("Chưa chạy hôm nay"):
        return "Hôm nay chưa chạy"
    if goc.startswith("Tắt tự chạy"):
        return "Đang tắt — kênh này không tự làm video"
    return _cat_chu(goc or "Chưa đọc được tình trạng")


#: Bấm vào câu tình trạng thì mở hộp nhật ký của KÊNH ĐÓ — mỗi cột một câu
#: gợi ý "làm gì tiếp theo", gom theo mức nặng nhẹ.
GOI_Y_VIEC = (
    ("Dừng ", "→ bấm “Chạy lại” ở cột kênh"),
    ("Chưa đặt tiền", "→ mở ⚙ Cài đặt, đặt tiền mỗi ngày"),
    ("Xong, chờ bạn duyệt", "→ vào Nội dung duyệt giờ đăng"),
    ("Xong, chưa chuyển", "→ bấm “Chạy lại” để chuyển sang máy đăng"),
    ("Quá giờ đăng", "→ xem máy đăng ở Máy & Ví"),
    ("Dở dang", "→ bấm “Chạy ngay” để làm tiếp"),
    ("Lịch hằng ngày đang tắt", "→ bấm “Bật lịch” ở dòng trên"),
    ("Nghỉ vì đã tiêu hết tiền", "→ mở ⚙ Cài đặt, nâng tiền mỗi ngày"),
)


def goi_y_viec(cau: str) -> str:
    """Một câu ngắn nói LÀM GÌ TIẾP THEO cho một câu tình trạng."""
    for dau, goi in GOI_Y_VIEC:
        if str(cau or "").startswith(dau):
            return goi
    return "→ mở ⚙ Cài đặt của kênh"


class _NhanBam(QLabel):
    """Nhãn bấm được — câu tình trạng, bấm vào thì mở nhật ký của kênh ấy."""

    bam = pyqtSignal()

    def __init__(self, cha: Optional[QWidget] = None):
        super().__init__(cha)
        self.setCursor(Qt.PointingHandCursor)

    def mousePressEvent(self, su_kien) -> None:  # noqa: N802 — tên do Qt quy định
        self.bam.emit()
        su_kien.accept()


def _giay_gon(giay: Any) -> str:
    try:
        giay = int(giay or 0)
    except (TypeError, ValueError):
        return ""
    if giay <= 0:
        return ""
    if giay < 60:
        return "{0} giây".format(giay)
    return "{0} phút".format(max(1, giay // 60))


class HopNhatKyKenh(QDialog):
    """Nhật ký hôm nay của ĐÚNG MỘT kênh — mở bằng cách bấm câu tình trạng.

    Ô này trước nằm ngay trong cột, cao chừng 200px, và ba cột cùng phơi một
    vết lỗi Python hai mươi dòng y hệt nhau. Nó là thứ người ta đọc khi đã
    biết kênh nào hỏng — tức là bước THỨ HAI, không phải thứ nhất. Mỗi dòng
    vẫn đi qua `gon_dong_nhat_ky`; nguyên văn nằm ở tooltip để còn truy lỗi.
    """

    def __init__(self, ma: str, cha: Optional[QWidget] = None):
        super().__init__(cha)
        self._ma = ma
        self.setWindowTitle("Nhật ký hôm nay — " + ma)
        self.resize(720, 460)
        doc = QVBoxLayout(self)
        doc.setContentsMargins(14, 12, 14, 12)
        doc.setSpacing(8)
        self._nhan_dau = QLabel("")
        self._nhan_dau.setWordWrap(True)
        self._nhan_dau.setStyleSheet("font-size:14px;font-weight:600;")
        doc.addWidget(self._nhan_dau)
        self.o_nhat_ky = QPlainTextEdit()
        self.o_nhat_ky.setReadOnly(True)
        self.o_nhat_ky.setFrameShape(QFrame.NoFrame)
        self.o_nhat_ky.setStyleSheet(
            "QPlainTextEdit{{background:{0};border:1px solid {1};border-radius:8px;"
            "padding:6px 8px;font-size:12px;color:{2};}}".format(
                theme.NEN, theme.VIEN, theme.CHU))
        doc.addWidget(self.o_nhat_ky, 1)
        hang = QHBoxLayout()
        hang.addStretch(1)
        hang.addWidget(nut_phu("Đóng", self.close, rong=90))
        doc.addLayout(hang)

    def nap(self, k: Dict[str, Any]) -> None:
        self._nhan_dau.setText(cau_tinh_trang(k))
        nk = [str(d) for d in (k.get("nhat_ky") or [])]
        o_cuoi = self.o_nhat_ky.verticalScrollBar()
        o_day = o_cuoi.value() >= o_cuoi.maximum() - 2
        self.o_nhat_ky.setPlainText(
            "\n".join(gon_dong_nhat_ky(d) for d in nk[-200:]) if nk
            else "(hôm nay kênh này chưa chạy lượt nào)")
        self.o_nhat_ky.setToolTip("\n".join(nk[-40:]) if nk else "")
        if o_day:
            o_cuoi.setValue(o_cuoi.maximum())


class HopCaiDatKenh(QDialog):
    """MỌI thứ kiểm soát của ĐÚNG MỘT kênh — mở bằng nút ⚙ trên cột.

    Chủ dự án, 22/09/2026: *"tao nghĩ mỗi kênh có 1 mục cài đặt để cài giờ
    đăng rồi all các thứ để kiểm soát kênh đó - còn nội dung ở ngoài thì cần
    thể hiện"*. Nên cột ngoài chỉ còn TÌNH TRẠNG, còn mọi núm vặn về đây.

    Một cột dọc, mỗi dòng một việc, mỗi việc một câu giải thích ngay dưới.
    **Không có nút Lưu** — sửa là ghi. Ba cửa ghi, đều là cửa có sẵn:
    `core.trung_tam.ghi_cai_kenh` cho `kenh.yaml` (giờ đăng · tự chạy · tự
    dọn · tiền mỗi ngày) và `core.vm_cai_dat.luu` cho `may-ao.json` (tự đăng ·
    trả lời bình luận · phút mở phiên).
    """

    xin_cong_tac = pyqtSignal(str, str, bool)
    xin_ngan_sach = pyqtSignal(str, int)
    xin_gio_dang = pyqtSignal(str, str)
    xin_phut_phien = pyqtSignal(str, int)

    #: Bốn công tắc, nhãn NGẮN và bằng TIẾNG VIỆT. Khoá kỹ thuật (`tu_dang`,
    #: `tu_tra_loi_cmt`) chỉ sống trong mã, không bao giờ hiện lên màn hình —
    #: `MyTool/CLAUDE.md`, mục "Cách viết cho hợp chỗ này".
    CONG_TAC = (
        ("tu_chay", "Tự chạy",
         "Mỗi ngày máy tự làm một video mới cho kênh này."),
        ("tu_dang", "Tự đăng",
         "BẬT là video tự lên sóng, không ai duyệt trước."),
        ("tu_tra_loi_cmt", "Trả lời bình luận",
         "Máy tự trả lời bình luận dưới video của kênh này."),
        ("tu_don", "Tự dọn",
         "Video đã lên sóng thì xoá ảnh, clip và bản dựng cho nhẹ ổ đĩa."),
    )

    def __init__(self, ma: str, cha: Optional[QWidget] = None):
        super().__init__(cha)
        self._ma = ma
        self._dang_nap = False
        self.setWindowTitle("Cài đặt kênh " + ma)
        self.setMinimumWidth(430)
        self.setStyleSheet("QDialog{{background:{0};}}".format(theme.THE))

        doc = QVBoxLayout(self)
        doc.setContentsMargins(16, 14, 16, 14)
        doc.setSpacing(4)

        dau = QLabel("Cài đặt kênh " + ma)
        dau.setStyleSheet("font-size:16px;font-weight:700;")
        doc.addWidget(dau)
        nh = QLabel("Sửa ở đây là lưu ngay, không cần bấm gì thêm.")
        nh.setWordWrap(True)
        nh.setStyleSheet("color:{0};font-size:11px;".format(theme.CHU_MO))
        doc.addWidget(nh)
        doc.addSpacing(6)

        # ── Giờ đăng ────────────────────────────────────────────────────────
        self.o_gio_dang = QTimeEdit(QTime(20, 0))
        self.o_gio_dang.setDisplayFormat("HH:mm")
        self.o_gio_dang.setFixedWidth(90)
        self.o_gio_dang.timeChanged.connect(
            lambda _t: self._bao_gio_dang())
        self.nhan_gio_dang = self._them(
            "Giờ đăng", self.o_gio_dang,
            "Video làm xong sẽ được hẹn lên sóng vào giờ này mỗi ngày.", doc)

        # ── Phút mở phiên ───────────────────────────────────────────────────
        self.o_phut_phien = QSpinBox()
        self.o_phut_phien.setRange(5, 600)
        self.o_phut_phien.setSingleStep(5)
        self.o_phut_phien.setSuffix(" phút")
        self.o_phut_phien.setFixedWidth(110)
        self.o_phut_phien.valueChanged.connect(
            lambda _v: self._hen_phien.start())
        self._them("Mở phiên trước giờ đăng", self.o_phut_phien,
                   "Máy mở trình duyệt của kênh trước giờ đăng chừng này phút, "
                   "để kịp quét số liệu và trả lời bình luận.", doc)

        # ── Bốn công tắc ────────────────────────────────────────────────────
        self.o_cong_tac: Dict[str, QCheckBox] = {}
        for khoa, ten, giai in self.CONG_TAC:
            o = QCheckBox(ten)
            o.setStyleSheet("font-size:13px;font-weight:600;")
            o.setToolTip(giai)
            o.toggled.connect(
                lambda bat, kh=khoa: self._bao_cong_tac(kh, bool(bat)))
            doc.addWidget(o)
            doc.addWidget(self._giai(giai))
            doc.addSpacing(4)
            self.o_cong_tac[khoa] = o

        # ── Tiền mỗi ngày ───────────────────────────────────────────────────
        self.o_ngan_sach = QSpinBox()
        self.o_ngan_sach.setRange(0, 50_000_000)
        self.o_ngan_sach.setSingleStep(50_000)
        self.o_ngan_sach.setGroupSeparatorShown(True)
        # Việt Nam ngăn nhóm bằng dấu CHẤM (5.000.000), không phải dấu phẩy —
        # Qt lấy dấu theo "vùng" của tiến trình, mà tiến trình chạy ở vùng C.
        self.o_ngan_sach.setLocale(QLocale(QLocale.Vietnamese, QLocale.Vietnam))
        self.o_ngan_sach.setSuffix(" ₫")
        self.o_ngan_sach.setFixedWidth(160)
        self.o_ngan_sach.setToolTip(
            "Trần tiền mỗi NGÀY cho kênh này.\n"
            "Để 0 nghĩa là KHÔNG SẢN XUẤT GÌ CẢ — không phải “bỏ trần”.\n"
            "Muốn không giới hạn thì đặt một con số rất cao.")
        self.o_ngan_sach.valueChanged.connect(lambda _v: self._hen_ngan_sach())
        self._them("Tiền mỗi ngày", self.o_ngan_sach,
                   "Trần tiền kênh này được tiêu trong một ngày. Muốn không "
                   "giới hạn thì đặt một con số rất cao.", doc)

        self.nhan_canh_ns = QLabel("")
        self.nhan_canh_ns.setWordWrap(True)
        self.nhan_canh_ns.setStyleSheet(
            "color:{0};font-size:12px;font-weight:600;".format(theme.CAM))
        doc.addWidget(self.nhan_canh_ns)

        doc.addSpacing(8)
        chi = QLabel("Giọng đọc, bộ vẽ, màu chữ bìa: ở Nội dung → Quản lý kênh")
        chi.setWordWrap(True)
        # Nền + viền của nhãn này vẽ bằng stylesheet, mà Qt không cộng phần
        # `padding` ấy vào chiều cao nó tự xin — thiếu dòng dưới là chữ bị xén
        # mất nửa dưới ngay trong hộp.
        chi.setMinimumHeight(34)
        chi.setStyleSheet(
            "QLabel{{background:{0};border:1px solid {1};border-radius:8px;"
            "padding:6px 9px;color:{2};font-size:12px;}}".format(
                theme.NHAN_NHAT, theme.VIEN, theme.NHAN_DAM))
        doc.addWidget(chi)

        doc.addStretch(1)
        hang = QHBoxLayout()
        hang.addStretch(1)
        hang.addWidget(nut_phu("Đóng", self.close, rong=90))
        doc.addLayout(hang)

        #: Gõ số là gõ từng phím — gom lại rồi mới ghi xuống tệp.
        self._hen = QTimer(self)
        self._hen.setSingleShot(True)
        self._hen.setInterval(800)
        self._hen.timeout.connect(
            lambda: self.xin_ngan_sach.emit(self._ma, self.o_ngan_sach.value()))
        self._hen_phien = QTimer(self)
        self._hen_phien.setSingleShot(True)
        self._hen_phien.setInterval(800)
        self._hen_phien.timeout.connect(
            lambda: self.xin_phut_phien.emit(self._ma, self.o_phut_phien.value()))
        self._hen_gio = QTimer(self)
        self._hen_gio.setSingleShot(True)
        self._hen_gio.setInterval(800)
        self._hen_gio.timeout.connect(
            lambda: self.xin_gio_dang.emit(
                self._ma, self.o_gio_dang.time().toString("HH:mm")))

    # ── Dựng ─────────────────────────────────────────────────────────────────

    @staticmethod
    def _giai(chu: str) -> QLabel:
        nh = QLabel(chu)
        nh.setWordWrap(True)
        nh.setStyleSheet("color:{0};font-size:11px;".format(theme.CHU_MO))
        return nh

    def _them(self, ten: str, o: QWidget, giai: str, doc: QVBoxLayout) -> QLabel:
        hang = QHBoxLayout()
        hang.setContentsMargins(0, 0, 0, 0)
        hang.setSpacing(8)
        nh = QLabel(ten)
        nh.setWordWrap(False)
        nh.setStyleSheet("font-size:13px;font-weight:600;")
        hang.addWidget(nh)
        hang.addWidget(o)
        hang.addStretch(1)
        doc.addLayout(hang)
        nh_giai = self._giai(giai)
        doc.addWidget(nh_giai)
        doc.addSpacing(6)
        return nh_giai

    # ── Nạp dữ liệu ──────────────────────────────────────────────────────────

    def nap(self, k: Dict[str, Any], cai_vm: Dict[str, Any]) -> None:
        self._dang_nap = True
        try:
            gio = str(k.get("gio_dang") or "").strip()
            t = QTime.fromString(gio, "HH:mm") if gio else QTime(20, 0)
            if not self.o_gio_dang.hasFocus():
                self.o_gio_dang.blockSignals(True)
                self.o_gio_dang.setTime(t if t.isValid() else QTime(20, 0))
                self.o_gio_dang.blockSignals(False)
            # Giờ đăng chỉ có tác dụng khi kênh được phép tự hẹn lịch. Nói
            # thẳng ra, đừng để người ta đặt một con số rồi không thấy gì xảy
            # ra — `MyTool/CLAUDE.md`, "Nói thật khi hỏng".
            self.nhan_gio_dang.setText(
                "Video làm xong sẽ được hẹn lên sóng vào giờ này mỗi ngày."
                if k.get("tu_duyet") else
                "Kênh này đang chờ bạn duyệt từng video, nên giờ đăng chưa "
                "dùng tới. Bật “Tự đăng, không chờ duyệt” ở Nội dung → Quản "
                "lý kênh thì giờ này mới có tác dụng.")

            if not self.o_phut_phien.hasFocus():
                try:
                    phut = int(cai_vm.get("phien_truoc_phut") or 60)
                except (TypeError, ValueError):
                    phut = 60
                self.o_phut_phien.blockSignals(True)
                self.o_phut_phien.setValue(max(5, min(600, phut)))
                self.o_phut_phien.blockSignals(False)

            gia_tri = {
                "tu_chay": bool(k.get("tu_chay")),
                "tu_don": bool(k.get("tu_don")),
                "tu_dang": bool(cai_vm.get("tu_dang")),
                "tu_tra_loi_cmt": bool(cai_vm.get("tu_tra_loi_cmt")),
            }
            for khoa, o in self.o_cong_tac.items():
                o.blockSignals(True)
                o.setChecked(gia_tri.get(khoa, False))
                o.blockSignals(False)

            tran = int(k.get("ngan_sach_ngay") or 0)
            if not self.o_ngan_sach.hasFocus():
                self.o_ngan_sach.blockSignals(True)
                self.o_ngan_sach.setValue(tran)
                self.o_ngan_sach.blockSignals(False)
            self.nhan_canh_ns.setText(
                "0₫ = KHÔNG sản xuất gì cả" if tran <= 0 else "")
        finally:
            self._dang_nap = False

    # ── Người bấm ────────────────────────────────────────────────────────────

    def _bao_cong_tac(self, khoa: str, bat: bool) -> None:
        if not self._dang_nap:
            self.xin_cong_tac.emit(self._ma, khoa, bat)

    def _hen_ngan_sach(self) -> None:
        if not self._dang_nap:
            self._hen.start()

    def _bao_gio_dang(self) -> None:
        if not self._dang_nap:
            self._hen_gio.start()


class CotKenh(QFrame):
    """MỘT kênh = MỘT cột chạy hết chiều cao cửa sổ.

    Cột này CHỈ NÓI TÌNH TRẠNG. Mọi núm vặn đã dọn sang hộp ⚙ Cài đặt của
    đúng kênh ấy (`HopCaiDatKenh`) — chủ dự án, 22/09/2026: *"mỗi kênh có 1
    mục cài đặt để cài giờ đăng rồi all các thứ để kiểm soát kênh đó - còn nội
    dung ở ngoài thì cần thể hiện"*.

    Từ trên xuống: mã kênh + tệp khán giả · **một câu tình trạng** (chữ to
    nhất cột, bấm được để mở nhật ký) · video hôm nay + giờ đăng · dây chuyền
    tám khâu · một dòng số · đúng hai nút.

    Ba thứ đã BỎ HẲN khỏi cột, vì chúng làm cột rối chứ không trả lời câu
    "kênh này đang thế nào": ô "Hôm nay" chứa nhật ký thô (ba cột cùng phơi
    một vết lỗi y hệt nhau), bốn ô tích, và ô ngân sách.

    Vì sao cột dọc chứ không phải thẻ ngang: dây chuyền của `core/tu_chay.py`
    có tám khâu chạy TUẦN TỰ, và một danh sách dọc tám dòng chính là hình của
    cái tuần tự ấy.
    """

    #: Bề rộng một cột. Đo ngược từ cửa sổ thật 1416: trừ thanh bên 240 và lề
    #: trang 2×16 còn 1144px cho bốn cột và ba khoảng cách 8px → tối đa 280.
    #: Lấy 236 để ở cửa sổ 1280 (còn 1008px) bốn cột vẫn nằm CÙNG MỘT HÀNG
    #: (4×236 + 24 = 968). Ở 1024 chúng tự xuống thành hai hàng, không tràn.
    RONG = 236
    _RONG_TRONG = RONG - 20

    chon_kenh = pyqtSignal(str)
    xin_chay = pyqtSignal(str)
    xin_cai_dat = pyqtSignal(str)
    xin_nhat_ky = pyqtSignal(str)

    #: Bốn công tắc nay ở `HopCaiDatKenh`. Giữ tên cũ ở đây để mã ngoài (và
    #: bài kiểm cũ) còn tra được bảng nhãn tiếng Việt.
    CONG_TAC = HopCaiDatKenh.CONG_TAC

    def __init__(self, ma: str, cha: Optional[QWidget] = None):
        super().__init__(cha)
        self._ma = ma
        self._muc = THUONG
        self._muc_mau = THUONG
        self._dang_nap = False
        #: Hộp ⚙ Cài đặt của đúng kênh này — trang gắn vào lúc dựng cột. Bốn ô
        #: tích, ô tiền và ô giờ đăng sống TRONG hộp ấy, không trong cột.
        self.hop_cai: Optional[HopCaiDatKenh] = None
        #: Hộp nhật ký của kênh này — mở bằng cách bấm câu tình trạng.
        self.hop_nhat_ky: Optional[HopNhatKyKenh] = None
        self.setObjectName("cotKenh")
        self.setFixedWidth(self.RONG)

        doc = QVBoxLayout(self)
        doc.setContentsMargins(10, 9, 10, 9)
        doc.setSpacing(4)

        # ── 1. Kênh nào ─────────────────────────────────────────────────────
        hang_ten = QHBoxLayout()
        hang_ten.setContentsMargins(0, 0, 0, 0)
        hang_ten.setSpacing(6)
        self._nhan_ten = QLabel(ma)
        self._nhan_ten.setWordWrap(False)
        self._nhan_ten.setStyleSheet("font-size:15px;font-weight:700;")
        hang_ten.addWidget(self._nhan_ten)
        self._nhan_tep = QLabel("—")
        self._nhan_tep.setWordWrap(False)
        self._nhan_tep.setMinimumWidth(1)
        self._nhan_tep.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self._nhan_tep.setStyleSheet("color:{0};font-size:11px;".format(theme.CHU_MO))
        hang_ten.addWidget(self._nhan_tep, 1)
        doc.addLayout(hang_ten)

        # ── 2. MỘT CÂU TÌNH TRẠNG — thứ đọc đầu tiên, chữ to nhất cột ───────
        self._nhan_tt = _NhanBam()
        self._nhan_tt.setWordWrap(True)
        self._nhan_tt.setMinimumWidth(1)
        self._nhan_tt.bam.connect(lambda: self.xin_nhat_ky.emit(self._ma))
        doc.addWidget(self._nhan_tt)

        # ── 3. Video hôm nay + giờ đăng ─────────────────────────────────────
        # Tiêu đề tiếng Nhật dài — cắt gọn, bản đầy đủ nằm ở tooltip.
        self._nhan_video = QLabel("—")
        self._nhan_video.setWordWrap(True)
        self._nhan_video.setMinimumWidth(1)
        self._nhan_video.setStyleSheet("font-size:12px;")
        doc.addWidget(self._nhan_video)

        self._nhan_dang = QLabel("")
        self._nhan_dang.setWordWrap(False)
        self._nhan_dang.setStyleSheet("color:{0};font-size:11px;".format(theme.CHU_MO))
        doc.addWidget(self._nhan_dang)

        doc.addWidget(self._gach())

        # ── 4. Dây chuyền tám khâu ──────────────────────────────────────────
        self._khau: Dict[str, QLabel] = {}
        self._khau_phu: Dict[str, QLabel] = {}
        from core.auto import KHAU  # noqa: PLC0415 — chỉ cần lúc dựng cột

        # Cột được kéo cao hết cửa sổ (`TrangDieuKhien._chinh_cao_cot`). Chỗ
        # dư rơi vào KHOẢNG GIỮA TÁM KHÂU, chứ không dồn thành một mảng trắng:
        # dây chuyền giãn ra thành một đường chạy dọc suốt cột — đúng hình
        # của cái tuần tự nó đang mô tả. Cửa sổ thấp thì các khoảng này co về
        # 0 và cột lại gọn như cũ.
        for i, (ma_khau, ten_khau, _tien, _sp) in enumerate(KHAU):
            if i:
                doc.addStretch(1)
            hang = QHBoxLayout()
            hang.setContentsMargins(0, 0, 0, 0)
            hang.setSpacing(4)
            chinh = QLabel("○ " + tt.TEN_KHAU_NGAN.get(ma_khau, ten_khau))
            chinh.setWordWrap(False)
            chinh.setToolTip(ten_khau)
            phu = QLabel("")
            phu.setWordWrap(False)
            phu.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            phu.setStyleSheet("color:{0};font-size:11px;".format(theme.CHU_MO))
            hang.addWidget(chinh, 1)
            hang.addWidget(phu)
            doc.addLayout(hang)
            self._khau[ma_khau] = chinh
            self._khau_phu[ma_khau] = phu

        doc.addWidget(self._gach())

        # ── 5. MỘT dòng số ──────────────────────────────────────────────────
        hang_so = QHBoxLayout()
        # 2px bên phải: dấu ₫ rộng hơn ô chữ Qt chừa cho nó, không có lề này
        # thì "86k₫" bị cắt mất cái đuôi ngay sát mép thẻ.
        hang_so.setContentsMargins(0, 0, 2, 0)
        hang_so.setSpacing(6)
        self._nhan_7ng = QLabel("7 ngày: —")
        self._nhan_7ng.setWordWrap(False)
        self._nhan_7ng.setMinimumWidth(1)
        self._nhan_7ng.setStyleSheet("font-size:12px;")
        hang_so.addWidget(self._nhan_7ng, 1)
        self._nhan_tien = QLabel("Hôm nay: —")
        self._nhan_tien.setWordWrap(False)
        self._nhan_tien.setMinimumWidth(1)
        self._nhan_tien.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self._nhan_tien.setStyleSheet("font-size:12px;")
        hang_so.addWidget(self._nhan_tien)
        doc.addLayout(hang_so)

        # ── 6. Đúng hai nút ─────────────────────────────────────────────────
        hang_nut = QHBoxLayout()
        hang_nut.setContentsMargins(0, 0, 0, 0)
        hang_nut.setSpacing(6)
        self._nut_chay = nut_phu("Chạy ngay", lambda: self.xin_chay.emit(self._ma),
                                 rong=106)
        self._nut_chay.setToolTip(
            "Làm video hôm nay cho kênh này ngay bây giờ. Tốn tiền thật, trong "
            "trần mỗi ngày. Chạy riêng — đóng tool không dừng nó.")
        hang_nut.addWidget(self._nut_chay)
        # Cùng một CHỖ với "Chạy ngay" — chỉ một trong hai hiện ra, tuỳ lượt
        # hôm nay có hỏng hay không. Hai nút thật vì câu chữ và lời nhắc của
        # chúng khác nhau, nhưng người xem luôn chỉ thấy MỘT.
        self._nut_lai = nut_phu("Chạy lại", lambda: self.xin_chay.emit(self._ma),
                                rong=106)
        self._nut_lai.setToolTip(
            "Lượt hôm nay hỏng ở một khâu — chạy lại để làm tiếp từ đúng khâu "
            "đó, không làm lại từ đầu, không trả tiền lại cho khâu đã xong.")
        self._nut_lai.setVisible(False)
        hang_nut.addWidget(self._nut_lai)
        self._nut_cai = nut_phu("⚙ Cài đặt",
                                lambda: self.xin_cai_dat.emit(self._ma))
        self._nut_cai.setToolTip(
            "Giờ đăng, các công tắc tự chạy và tiền mỗi ngày của riêng kênh này.")
        hang_nut.addWidget(self._nut_cai, 1)
        doc.addLayout(hang_nut)

        self._ve_vien()

    @staticmethod
    def _gach() -> QFrame:
        v = QFrame()
        v.setFrameShape(QFrame.HLine)
        v.setFixedHeight(1)
        v.setStyleSheet("background:{0};border:none;".format(theme.VIEN))
        return v

    # ── Nạp dữ liệu ──────────────────────────────────────────────────────────

    def nap(self, k: Dict[str, Any], cai_vm: Dict[str, Any]) -> None:
        self._dang_nap = True
        try:
            self._nap_that(k, cai_vm)
        finally:
            self._dang_nap = False

    #: Câu tình trạng đang hiện — bài kiểm đọc thẳng, không phải bóc từ nhãn.
    cau: str = ""

    def _nap_that(self, k: Dict[str, Any], cai_vm: Dict[str, Any]) -> None:
        bay = k.get("bay_gio") or {}
        self._muc = _muc_bao(bay.get("muc"))
        self._muc_mau = muc_mau_cot(bay.get("muc"))

        ten_day = str(k.get("ten") or k.get("ma") or "")
        _cat(self._nhan_ten, k.get("ma") or "", 108)
        self._nhan_ten.setToolTip(ten_day)

        ma_tep = k.get("tep") or ""
        _cat(self._nhan_tep, _tep_ngan(ma_tep), self._RONG_TRONG - 112)
        self._nhan_tep.setToolTip(
            "Tệp khán giả: {0}\n{1}".format(_tep_ngan(ma_tep), _ten_tep(ma_tep))
            if ma_tep else "Kênh chưa chọn tệp khán giả.")

        # ── Câu tình trạng ──────────────────────────────────────────────────
        # Dấu (✓ ◑ ⏱ ⚠ ✕) đi kèm CHỮ, không bao giờ đi một mình: màu và dấu
        # chỉ nhắc lại điều chính câu ấy đã nói.
        self.cau = cau_tinh_trang(k)
        chu, nen, vien = _MAU_COT[self._muc_mau]
        dau = DAU_TINH_TRANG.get(str(bay.get("muc") or ""), "")
        self._nhan_tt.setText((dau + "  " if dau else "") + self.cau)
        self._nhan_tt.setToolTip("{0}\n\n{1}\n\nBấm để xem nhật ký hôm nay của "
                                 "kênh này.".format(
                                     self.cau,
                                     bay.get("chi_tiet") or bay.get("chu") or ""))
        self._nhan_tt.setStyleSheet(
            "QLabel{{background:{0};border:1px solid {1};border-radius:8px;"
            "padding:6px 8px;color:{2};font-size:14px;font-weight:700;}}".format(
                nen if self._muc_mau != THUONG else theme.NEN,
                vien if self._muc_mau != THUONG else theme.VIEN, chu))

        td = str((k.get("video") or {}).get("tieu_de") or "")
        _cat(self._nhan_video, td or "— chưa có video hôm nay",
             (self._RONG_TRONG - 4) * 2)
        self._nhan_video.setToolTip(td or "Hôm nay kênh này chưa chọn video nào.")
        luc = str(k.get("dang_luc") or "")
        self._nhan_dang.setText("Đăng: " + luc if luc else "")
        self._nhan_dang.setVisible(bool(luc))
        self._nhan_dang.setToolTip(
            "Ngày giờ video hôm nay được hẹn lên sóng." if luc else "")

        co_hong = self._ve_khau(k)

        n7 = k.get("bay_ngay") or {}
        if n7.get("so_video"):
            self._nhan_7ng.setText("7 ngày: {0} · {1}".format(
                _gon(n7.get("views")), _pt(n7.get("ctr"))))
            self._nhan_7ng.setToolTip(
                "{0} video đăng trong 7 ngày: tổng lượt xem {1} · tỷ lệ bấm {2} · "
                "đăng ký mới {3}".format(n7.get("so_video"), _gon(n7.get("views")),
                                         _pt(n7.get("ctr")), _gon(n7.get("dang_ky"))))
        else:
            self._nhan_7ng.setText("7 ngày: —")
            self._nhan_7ng.setToolTip(
                "Chưa có video nào đăng trong 7 ngày (hoặc chưa có số liệu).")

        tien = k.get("tien") or {}
        self._nhan_tien.setText("Hôm nay: " + _vnd_gon(tien.get("hom_nay")))
        self._nhan_tien.setToolTip(
            "Hôm nay kênh này đã tiêu khoảng {0} (số tool ước, không phải số ví "
            "trừ thật) trên trần {1} mỗi ngày.".format(
                _vnd_gon(tien.get("hom_nay")),
                _vnd_gon(tien.get("tran")) if tien.get("tran") else "chưa đặt"))

        # Đúng MỘT nút chạy hiện ra: "Chạy lại" khi lượt hôm nay hỏng, còn lại
        # là "Chạy ngay". Không bao giờ hai nút cùng lúc.
        lai = bool(co_hong) and not k.get("dang_chay")
        self._nut_lai.setVisible(lai)
        self._nut_chay.setVisible(not lai)
        self._nut_chay.setEnabled(not k.get("dang_chay"))
        self._nut_chay.setToolTip(
            "Kênh đang chạy — đợi lượt này xong." if k.get("dang_chay")
            else "Làm video hôm nay cho kênh này ngay bây giờ. Tốn tiền thật, "
                 "trong trần mỗi ngày.")
        self._nut_lai.setEnabled(lai)
        if self.hop_cai is not None:
            self.hop_cai.nap(k, cai_vm)
        self._ve_vien()

    def _ve_khau(self, k: Dict[str, Any]) -> bool:
        """Vẽ tám khâu. Trả về: lượt này có khâu nào ĐANG HỎNG không.

        Cột "phút" của các khâu ĐÃ XONG đi vào tooltip. Nó là chuyện để truy
        về sau, không phải chuyện của lúc liếc màn hình — và tám con số xám
        chạy dọc cột làm cái đang chạy chìm nghỉm giữa bảy cái đã xong. Chỗ
        bên phải ấy nay chỉ dành cho TIẾN ĐỘ của khâu đang chạy, hoặc "LỖI".
        """
        khau = {d.get("ma"): d for d in ((k.get("luot") or {}).get("khau") or [])}
        tien = tien_do_nhat_ky(k.get("nhat_ky"))
        co_hong = False
        for ma_khau, nh in self._khau.items():
            d = khau.get(ma_khau) or {}
            trang = str(d.get("trang_thai") or "")
            if trang == "hong":
                co_hong = True
            dau = DAU_KHAU.get(trang, "○")
            ten = tt.TEN_KHAU_NGAN.get(ma_khau, ma_khau)
            nh.setText("{0} {1}".format(dau, ten))
            mau = _MAU_KHAU_CHU.get(trang, theme.CHU_MO)
            nh.setStyleSheet("font-size:12px;color:{0};{1}".format(
                mau, "font-weight:600;" if trang in ("dang", "hong") else ""))
            phu = self._khau_phu[ma_khau]
            if trang == "hong":
                phu.setText("LỖI")
                phu.setStyleSheet("color:{0};font-size:11px;font-weight:600;".format(theme.DO))
            elif trang == "dang":
                phu.setText(tien)
                phu.setStyleSheet("color:{0};font-size:11px;font-weight:600;".format(theme.NHAN))
            else:
                phu.setText("")
                phu.setStyleSheet("color:{0};font-size:11px;".format(theme.CHU_MO))
            tip = "{0} — {1}".format(
                d.get("ten") or ten, CHU_KHAU.get(trang, "chưa tới lượt"))
            lau = _giay_gon(d.get("giay"))
            if lau:
                tip += "\nMất {0}".format(lau)
            if d.get("loi"):
                tip += "\n{0}".format(str(d.get("loi"))[:300])
            nh.setToolTip(tip)
            phu.setToolTip(tip)
        return co_hong

    def _ve_vien(self) -> None:
        _chu, nen, vien = _MAU_COT[self._muc_mau]
        self.setStyleSheet(
            "QFrame#cotKenh{{background:{0};border:2px solid {1};"
            "border-radius:12px;}}".format(
                theme.THE if self._muc_mau == THUONG else nen,
                theme.VIEN if self._muc_mau == THUONG else vien))

    # ── Lối tắt sang hộp ⚙ Cài đặt ───────────────────────────────────────────
    #
    # Bốn ô tích, ô tiền và câu cảnh báo "0₫" sống trong `HopCaiDatKenh`, chứ
    # KHÔNG còn trong cột. Mấy cái tên dưới đây chỉ trỏ sang đó, để mã và bài
    # kiểm cũ hỏi "ô tích của kênh này đâu" vẫn nhận được đúng cái ô ấy.

    @property
    def _o_cong_tac(self) -> Dict[str, QCheckBox]:
        return self.hop_cai.o_cong_tac if self.hop_cai is not None else {}

    @property
    def _o_ngan_sach(self):
        return self.hop_cai.o_ngan_sach if self.hop_cai is not None else None

    @property
    def _nhan_canh_ns(self):
        return self.hop_cai.nhan_canh_ns if self.hop_cai is not None else None

    @property
    def _hen(self):
        return self.hop_cai._hen if self.hop_cai is not None else None  # noqa: SLF001

    @property
    def _o_nhat_ky(self):
        """Ô nhật ký nay ở `HopNhatKyKenh`, mở bằng cách bấm câu tình trạng."""
        hop = getattr(self, "hop_nhat_ky", None)
        return hop.o_nhat_ky if hop is not None else None

    def mousePressEvent(self, su_kien) -> None:  # noqa: N802 — tên do Qt quy định
        self.chon_kenh.emit(self._ma)
        super().mousePressEvent(su_kien)


class TrangDieuKhien(QWidget):
    """Màn hình mở đầu trên VPS: sức khoẻ máy · việc cần xem · bốn cột kênh."""

    def __init__(self, app):
        super().__init__()
        self._app = app
        self._anh: Optional[Dict[str, Any]] = None
        self._may: Dict[str, Dict[str, Any]] = {}
        self._cai_vm: Dict[str, Dict[str, Any]] = {}
        self._lich: Optional[Dict[str, Any]] = None
        self._lich_luc = 0.0
        self._vi_luc = 0.0
        self._dang_nap = False
        self._dong = False
        self._cot: Dict[str, CotKenh] = {}
        self._hop_cai: Dict[str, HopCaiDatKenh] = {}
        self._hop_nhat_ky: Dict[str, HopNhatKyKenh] = {}
        self._mo_viec = False

        doc = QVBoxLayout(self)
        doc.setContentsMargins(16, 12, 16, 12)
        doc.setSpacing(8)
        doc.addWidget(self._hang_tieu_de())
        doc.addWidget(self._dai_suc_khoe())
        doc.addWidget(self._dai_viec())
        doc.addWidget(self._hang_lich())
        doc.addWidget(self._khoi_cot(), 1)

        self._dong_ho = QTimer(self)
        self._dong_ho.timeout.connect(lambda: self.lam_moi(bat_buoc=False))
        self._dong_ho.start(NHIP_LAM_MOI_MS)

        self._hoi_lich()
        self.lam_moi()

    # ── Vòng đời ─────────────────────────────────────────────────────────────

    def _con_song(self) -> bool:
        return not self._dong and not getattr(self._app, "_dang_dong", False)

    def closeEvent(self, event) -> None:  # noqa: N802 — tên do Qt quy định
        self._dong = True
        self._dong_ho.stop()
        super().closeEvent(event)

    # ── Dải trên ─────────────────────────────────────────────────────────────

    def _hang_tieu_de(self) -> QWidget:
        from .huong_dan import nut_huong_dan  # noqa: PLC0415

        hop = QWidget()
        ngang = QHBoxLayout(hop)
        ngang.setContentsMargins(0, 0, 0, 0)
        ngang.setSpacing(8)
        tieu = nhan("Điều khiển", "h1")
        tieu.setWordWrap(False)
        ngang.addWidget(tieu)
        self._nhan_luc = nhan("", "muted")
        self._nhan_luc.setMinimumWidth(1)
        ngang.addWidget(self._nhan_luc, 1)
        self._nut_tam_dung = nut_phu("Tạm dừng tất cả", self._tam_dung_tat_ca,
                                     rong=150)
        self._nut_tam_dung.setToolTip(
            "Tắt vòng tự chạy của MỌI kênh trong một cú bấm. Lượt đang chạy dở "
            "vẫn chạy nốt; từ lượt sau thì không kênh nào tự làm nữa.")
        ngang.addWidget(self._nut_tam_dung)
        ngang.addWidget(nut_phu("Làm mới", lambda: self.lam_moi(), rong=90))
        nut_hd = nut_huong_dan("dieu-khien", hop)
        if nut_hd is not None:
            ngang.addWidget(nut_hd)
        return hop

    def _dai_suc_khoe(self) -> QWidget:
        """Ô sức khoẻ của CÁI MÁY, mọi ô cùng cỡ, mọi tên bằng tiếng Việt."""
        hop = HopXuongDong(8)
        self._den: Dict[str, _OChiSo] = {}
        self._hop_den = hop

        self._o_dia = _OChiSo("Ổ đĩa còn")
        self._o_dia.setToolTip(
            "Chỗ trống còn lại trên ổ đặt tool. Mỗi video chiếm khoảng 0,4–0,9 GB "
            "trước khi dọn. Bấm để mở thư mục.")
        self._o_dia.clicked.connect(lambda: mo_thu_muc(self._app.base_dir))
        hop.addWidget(self._o_dia)

        self._o_vi = _OChiSo("Ví")
        self._o_vi.setToolTip("Số dư ví. Hết tiền là mọi kênh ngừng sản xuất. "
                              "Bấm để mở trang Máy & Ví.")
        self._o_vi.clicked.connect(self._mo_vi)
        hop.addWidget(self._o_vi)

        self._o_tien = _OChiSo("Tiền đã tiêu")
        self._o_tien.setToolTip(
            "Tiền ƯỚC TÍNH các kênh tự chạy đã tiêu — số tool ước lúc cho sản "
            "xuất, không phải số ví trừ thật.")
        hop.addWidget(self._o_tien)
        return hop

    def _dai_viec(self) -> QWidget:
        """MỘT dòng ngắn "⚠ N việc cần xem", bấm để mở danh sách.

        Bản trước nhồi cả sáu việc vào một dòng chạy dài ngang màn hình — dòng
        ấy đọc được đúng việc đầu tiên. Ở đây dòng chỉ nói CÓ MẤY VIỆC; bấm thì
        chúng rơi xuống thành danh sách, việc nặng (✕) đứng trên việc nhẹ (⚠).
        """
        hop = QWidget()
        v = QVBoxLayout(hop)
        v.setContentsMargins(0, 0, 0, 0)
        v.setSpacing(4)
        self._nut_viec = nut_phu("", self._gap_viec)
        self._nut_viec.setVisible(False)
        v.addWidget(self._nut_viec)
        self._hop_viec = QWidget()
        self._v_viec = QVBoxLayout(self._hop_viec)
        self._v_viec.setContentsMargins(6, 0, 0, 0)
        self._v_viec.setSpacing(2)
        self._hop_viec.setVisible(False)
        v.addWidget(self._hop_viec)
        return hop

    def _gap_viec(self) -> None:
        self._mo_viec = not self._mo_viec
        self._ve_viec()

    def _hang_lich(self) -> QWidget:
        """Hai cái đồng hồ của cả máy: giờ chạy hằng ngày và giờ phiên đăng."""
        khung = the()
        ngoai = QVBoxLayout(khung)
        ngoai.setContentsMargins(12, 7, 12, 7)
        ngoai.setSpacing(0)
        # `HangXuongDong`, KHÔNG phải `QHBoxLayout`: hàng ngang cứng cộng dồn
        # bề rộng tối thiểu của bảy ô lại và không co xuống nữa — đo được
        # 1.048px, tức cả trang không lọt cửa sổ 760 mà `tests/test_bo_cuc.py`
        # canh. Hàng biết xuống dòng thì tối thiểu chỉ bằng MỘT ô.
        hop = HopXuongDong(8)
        ngoai.addWidget(hop)
        ngang = hop.hang

        nh = nhan("Chạy hằng ngày lúc")
        nh.setWordWrap(False)
        ngang.addWidget(nh)
        self._o_gio_lich = QTimeEdit(QTime(2, 0))
        self._o_gio_lich.setDisplayFormat("HH:mm")
        self._o_gio_lich.setToolTip(
            "Giờ máy tự chạy lần lượt mọi kênh đã bật “Tự chạy”. Máy phải đang "
            "bật và đã đăng nhập vào đúng giờ này.")
        ngang.addWidget(self._o_gio_lich)
        self._nut_lich = nut_phu("Bật lịch", self._bat_tat_lich, rong=100)
        ngang.addWidget(self._nut_lich)
        self._nhan_lich = nhan("đang xem…", "muted")
        self._nhan_lich.setMinimumWidth(1)
        self._nhan_lich.setMaximumWidth(340)
        self._nhan_lich.setWordWrap(False)
        ngang.addWidget(self._nhan_lich)

        # "Phút mở phiên trước giờ đăng" từng đứng ở đây và ghi cho MỌI kênh
        # một lượt. Nó là thiết lập của TỪNG kênh, nên nay nằm trong hộp
        # ⚙ Cài đặt của kênh, cạnh chính cái giờ đăng mà nó đếm ngược từ đó.
        return khung

    # ── Bốn cột kênh ─────────────────────────────────────────────────────────

    def _khoi_cot(self) -> QWidget:
        self._khung_cot = the()
        v = QVBoxLayout(self._khung_cot)
        v.setContentsMargins(12, 10, 12, 10)
        v.setSpacing(6)
        self._hop_cot = HopXuongDong(8)
        v.addWidget(self._hop_cot)
        self._nhan_trong = nhan(
            "Chưa kênh nào bật tự chạy. Mở “Nội dung → Quản lý kênh” để bật, "
            "hoặc thêm kênh mới ở đó.", "muted")
        v.addWidget(self._nhan_trong)
        v.addStretch(1)
        return self._khung_cot

    #: Chiều cao đang đặt cho các cột — nhớ lại để lần chỉnh sau không đặt lại
    #: đúng con số cũ (đặt lại là một vòng layout nữa, và layout gọi resize).
    _cao_cot_dang_dat = 0

    def resizeEvent(self, su_kien) -> None:  # noqa: N802 — tên do Qt quy định
        super().resizeEvent(su_kien)
        self._chinh_cao_cot()

    def _cao_vung(self) -> int:
        """Chiều cao NHÌN THẤY của trang — trang nằm trong một vùng cuộn
        (`CuaSoChinh._boc_cuon`), nên `self.height()` là chiều cao đã kéo dài
        ra chứ không phải chỗ người ta thật sự nhìn thấy."""
        w = self.parentWidget()
        while w is not None:
            if isinstance(w, QScrollArea):
                return max(1, w.viewport().height())
            w = w.parentWidget()
        return max(1, self.height())

    def _chinh_cao_cot(self) -> None:
        """Kéo các cột cao hết phần cửa sổ còn lại.

        ═══ VÌ SAO PHẢI TỰ TÍNH ═══

        Đây chính là chỗ chữa lỗi chủ dự án chỉ ra: ảnh chụp cửa sổ thật
        1416×1039 có **40% phía dưới trắng trơn**. `HangXuongDong` xếp mọi thứ
        theo `sizeHint()`, tức đúng chiều cao "vừa đủ chữ" (≈420px) — thừa bao
        nhiêu nó để trống bấy nhiêu, và không có cách nào bảo một flow layout
        "chia đều chiều cao" mà không tự tính.

        Nên tính: đếm xem một hàng chứa được mấy cột ở bề rộng hiện tại, suy ra
        số hàng, rồi chia chiều cao còn lại cho số hàng. Không bao giờ ép xuống
        dưới chiều cao tự nhiên của cột — hẹp quá thì thà có thanh cuộn còn hơn
        cắt cụt hai cái nút.
        """
        cot = list(self._cot.values())
        if not cot:
            return
        rong_o = max(1, self._hop_cot.width())
        moi_hang = max(1, (rong_o + 8) // (CotKenh.RONG + 8))
        so_hang = max(1, -(-len(cot) // moi_hang))
        # Đo theo VÙNG NHÌN THẤY, không theo chiều cao của chính cái thẻ đang
        # chứa cột: thẻ ấy cao lên theo cột, nên lấy nó làm thước là tự đo bằng
        # chính thứ mình vừa đặt — cột phình thêm một nấc mỗi lần vẽ lại.
        con_lai = self._cao_vung() - self._khung_cot.y() - 24 - (so_hang - 1) * 8
        tu_nhien = max(c.sizeHint().height() for c in cot)
        cao = max(tu_nhien, con_lai // so_hang)
        if cao == self._cao_cot_dang_dat:
            return
        self._cao_cot_dang_dat = cao
        for c in cot:
            c.setFixedHeight(cao)

    def _ve_cot(self, kenh: List[Dict[str, Any]]) -> None:
        con = {k["ma"] for k in kenh}
        for ma in [m for m in self._cot if m not in con]:
            cu = self._cot.pop(ma)
            self._hop_cot.removeWidget(cu)
            cu.setParent(None)
            cu.deleteLater()
            for kho in (self._hop_cai, self._hop_nhat_ky):
                hop = kho.pop(ma, None)
                if hop is not None:
                    hop.close()
                    hop.deleteLater()
        for k in kenh:
            ma = k["ma"]
            c = self._cot.get(ma)
            if c is None:
                c = CotKenh(ma, self._hop_cot)
                c.xin_chay.connect(self._chay_ngay)
                c.xin_cai_dat.connect(self._mo_cai_dat)
                c.xin_nhat_ky.connect(self._mo_nhat_ky_kenh)
                # Hai hộp của kênh này treo vào TRANG, không vào cột: cột chỉ
                # được chứa tình trạng. Dựng sẵn (rỗng, chưa hiện) để lần bấm
                # đầu mở ra ngay, không phải đợi dựng.
                hop = HopCaiDatKenh(ma, self)
                hop.xin_cong_tac.connect(self._doi_cong_tac)
                hop.xin_ngan_sach.connect(self._doi_ngan_sach)
                hop.xin_gio_dang.connect(self._doi_gio_dang)
                hop.xin_phut_phien.connect(self._doi_phut_phien)
                c.hop_cai = hop
                self._hop_cai[ma] = hop
                nk = HopNhatKyKenh(ma, self)
                c.hop_nhat_ky = nk
                self._hop_nhat_ky[ma] = nk
                self._hop_cot.addWidget(c)
                self._cot[ma] = c
            c.nap(k, self._cai_vm.get(ma) or {})
            nk = self._hop_nhat_ky.get(ma)
            if nk is not None and nk.isVisible():
                nk.nap(k)
            c.setVisible(True)
        self._nhan_trong.setVisible(not kenh)
        self._cao_cot_dang_dat = 0      # số cột đổi → tính lại chiều cao
        self._chinh_cao_cot()

    # ── Việc cần xem ─────────────────────────────────────────────────────────

    #: Tên nhóm cho những việc KHÔNG thuộc riêng kênh nào.
    NHOM_MAY = "Cả máy"

    def viec_theo_nhom(self) -> List[tuple]:
        """`[(tên nhóm, [(mức, câu, làm gì tiếp theo)])]` — thuần, kiểm được.

        Nhóm THEO KÊNH, vì đó là cách người ta xử lý: mở đúng cột ấy ra rồi
        làm. Nhóm "Cả máy" (ổ đĩa, ví, lịch, ba con máy ảo) đứng đầu — nó
        chặn MỌI kênh, nên sửa nó trước là sửa được nhiều nhất.
        """
        anh = self._anh or {}
        may: List[tuple] = []

        con = (anh.get("o_dia") or {}).get("con_gb")
        if con is not None and con < GB_DIA_LUU_Y:
            may.append((HONG if con < GB_DIA_HONG else LUU_Y,
                        "Ổ đĩa chỉ còn {0:.0f} GB".format(con),
                        "→ bật “Tự dọn” ở ⚙ Cài đặt của từng kênh"))

        muc_vi = self._muc_vi()
        if muc_vi != THUONG:
            may.append((muc_vi, "Ví chỉ còn {0}".format(
                format_vnd(getattr(self._app, "last_wallet_micro", None))),
                "→ nạp tiền ở trang Máy & Ví"))

        if self._gio_lich() == "" and any(k.get("tu_chay") for k in anh.get("kenh") or []):
            may.append((LUU_Y, "Lịch chạy hằng ngày đang tắt",
                        "→ bấm “Bật lịch” ở dòng trên"))

        if self._co_may():
            for ten, tt_may in self._may.items():
                if not (tt_may or {}).get("song"):
                    may.append((HONG, "{0} đã tắt".format(_TEN_MAY.get(ten, ten)),
                                "→ bấm vào ô máy ở trên rồi chọn “Bật lại”"))

        thu_tu = {HONG: 0, LUU_Y: 1, THUONG: 2}
        ra: List[tuple] = []
        if may:
            ra.append((self.NHOM_MAY,
                       sorted(may, key=lambda x: thu_tu.get(x[0], 9))))

        theo_kenh: List[tuple] = []
        for k in anh.get("kenh") or []:
            m = _muc_bao((k.get("bay_gio") or {}).get("muc"))
            if m == THUONG:
                continue
            cau = cau_tinh_trang(k)
            theo_kenh.append((str(k.get("ma") or ""),
                              [(m, cau, goi_y_viec(cau))]))
        theo_kenh.sort(key=lambda g: thu_tu.get(g[1][0][0], 9))
        return ra + theo_kenh

    def viec_can_xem(self) -> List[tuple]:
        """`[(mức, câu ngắn)]` — bản phẳng của `viec_theo_nhom`, việc nặng trước."""
        ra: List[tuple] = []
        for ten_nhom, muc_viec in self.viec_theo_nhom():
            for m, chu, _goi in muc_viec:
                ra.append((m, chu if ten_nhom == self.NHOM_MAY
                           else "{0}: {1}".format(ten_nhom, chu)))
        thu_tu = {HONG: 0, LUU_Y: 1, THUONG: 2}
        return sorted(ra, key=lambda x: thu_tu.get(x[0], 9))

    def _ve_viec(self) -> None:
        nhom = self.viec_theo_nhom()
        so = sum(len(v) for _t, v in nhom)
        self._nut_viec.setVisible(bool(so))
        while self._v_viec.count():
            muc = self._v_viec.takeAt(0)
            w = muc.widget()
            if w is not None:
                w.deleteLater()
        if not so:
            self._hop_viec.setVisible(False)
            return
        muc_cao = THUONG
        for _ten, muc_viec in nhom:
            for m, _chu, _goi in muc_viec:
                muc_cao = _nang(muc_cao, m)
        chu_mau, nen, vien = _MAU_BAO[muc_cao]
        self._nut_viec.setText("{0} {1} việc cần xem   {2}".format(
            _CHU_BAO[muc_cao], so, "▾" if self._mo_viec else "▸"))
        self._nut_viec.setStyleSheet(
            "QPushButton{{background:{0};border:1px solid {1};border-radius:10px;"
            "padding:6px 12px;color:{2};font-size:13px;font-weight:600;"
            "text-align:left;}}".format(nen, vien, chu_mau))
        self._nut_viec.setToolTip("\n".join(c for _m, c in self.viec_can_xem()))
        self._hop_viec.setVisible(self._mo_viec)
        if not self._mo_viec:
            return
        for ten_nhom, muc_viec in nhom:
            dau_nhom = nhan(ten_nhom)
            dau_nhom.setMinimumWidth(1)
            dau_nhom.setStyleSheet(
                "color:{0};font-size:12px;font-weight:700;".format(theme.CHU))
            self._v_viec.addWidget(dau_nhom)
            for m, chu, goi in muc_viec:
                mau = _MAU_BAO[m][0]
                nh = nhan("    {0} {1}   {2}".format(_CHU_BAO[m] or "·", chu, goi))
                nh.setMinimumWidth(1)
                nh.setStyleSheet("color:{0};font-size:12px;".format(mau))
                self._v_viec.addWidget(nh)

    # ── Sức khoẻ máy ─────────────────────────────────────────────────────────

    def _co_may(self) -> bool:
        return bool((self._anh or {}).get("la_vps")
                    and _giam_sat(self._app) is not None and self._may)

    def _ve_may(self) -> None:
        if not self._co_may():
            for o in self._den.values():
                o.setVisible(False)
            return
        for ten, tt_may in self._may.items():
            o = self._den.get(ten)
            if o is None:
                o = _OChiSo(_TEN_MAY.get(ten, ten))
                o.clicked.connect(lambda t=ten: self._menu_may(t))
                self._hop_den.addWidget(o)
                self._den[ten] = o
            o.setVisible(True)
            song = bool((tt_may or {}).get("song"))
            o.dat("đang chạy" if song else "ĐÃ TẮT", THUONG if song else HONG)
            tip = ["Đang chạy" if song else "ĐANG TẮT"]
            if (tt_may or {}).get("lan_khoi"):
                tip.append("Đã tự bật lại {0} lần".format(tt_may.get("lan_khoi")))
            if (tt_may or {}).get("loi_cuoi"):
                tip.append("Lỗi gần nhất: {0}".format(str(tt_may.get("loi_cuoi"))[:200]))
            o.setToolTip("\n".join(tip) + "\nBấm để bật lại hoặc xem nhật ký.")

    def _menu_may(self, ten: str) -> None:
        menu = QMenu(self)
        menu.addAction("Bật lại", lambda: self._khoi_dong_lai(ten))
        menu.addAction("Xem nhật ký", lambda: self._xem_nhat_ky(ten))
        nut = self._den.get(ten)
        menu.exec_(nut.mapToGlobal(nut.rect().bottomLeft()) if nut
                   else self.cursor().pos())

    def _khoi_dong_lai(self, ten: str) -> None:
        gs = _giam_sat(self._app)
        if gs is None:
            return
        self._app.run_bg(lambda: gs.khoi_dong_lai(ten),
                         on_ok=lambda _k: self.lam_moi(),
                         on_err=self._app.show_error)

    def _xem_nhat_ky(self, ten: str) -> None:
        mo = getattr(self._app, "show_page", None)
        if mo is not None:
            mo("may-vi")
        trang = self._app.trang("may-vi") if hasattr(self._app, "trang") else None
        xem = getattr(trang, "xem_nhat_ky_may", None)
        if xem is not None:
            xem(ten)

    def _ve_dia(self) -> None:
        dia = (self._anh or {}).get("o_dia") or {}
        con = dia.get("con_gb")
        if con is None:
            self._o_dia.dat("chưa đọc được")
            return
        muc = HONG if con < GB_DIA_HONG else (LUU_Y if con < GB_DIA_LUU_Y else THUONG)
        them = {HONG: " — sắp đầy", LUU_Y: " — hơi chật", THUONG: ""}[muc]
        self._o_dia.dat("{0:.0f} GB{1}".format(con, them), muc)

    def _muc_vi(self) -> str:
        if getattr(self._app, "client", None) is None:
            return THUONG
        micro = getattr(self._app, "last_wallet_micro", None)
        if micro is None:
            return THUONG
        vnd = int(micro) / MICRO_PER_VND
        if vnd < VND_VI_HONG:
            return HONG
        return LUU_Y if vnd < VND_VI_LUU_Y else THUONG

    def _ve_vi(self) -> None:
        if getattr(self._app, "client", None) is None:
            self._o_vi.dat("chưa đăng nhập", LUU_Y,
                           "Chưa đăng nhập thì kênh không sản xuất được. "
                           "Bấm để mở trang Máy & Ví.")
            return
        micro = getattr(self._app, "last_wallet_micro", None)
        self._o_vi.dat(format_vnd(micro) if micro is not None else "—", self._muc_vi())
        if self._vi_luc and time.monotonic() - self._vi_luc < GIAY_HOI_VI:
            return
        if not self.isVisible():
            return          # trang ẩn không ai xem — không hỏi máy chủ
        self._vi_luc = time.monotonic()
        client = self._app.client

        def viec():
            from core.api import fetch_balance  # noqa: PLC0415

            return fetch_balance(client)

        def xong(so_du) -> None:
            ghi = getattr(self._app, "note_balance", None)
            if ghi is not None:
                ghi(so_du)
            from core.api import wallet_micro  # noqa: PLC0415

            self._o_vi.dat(format_vnd(wallet_micro(so_du)), self._muc_vi())
            self._ve_viec()

        self._app.run_bg(viec, on_ok=xong, on_err=lambda _l: None)

    def _mo_vi(self) -> None:
        mo = getattr(self._app, "show_page", None)
        if mo is not None:
            mo("may-vi")

    # ── Lịch hằng ngày ───────────────────────────────────────────────────────

    def _hoi_lich(self) -> None:
        goc = self._app.base_dir

        def viec():
            from core import lich_tu_chay  # noqa: PLC0415

            return lich_tu_chay.trang_thai(goc)

        def xong(ket) -> None:
            self._lich = dict(ket or {})
            self._lich_luc = time.monotonic()
            self._ve_lich()

        self._app.run_bg(viec, on_ok=xong, on_err=lambda _l: None)

    def _gio_lich(self) -> Optional[str]:
        """`None` = chưa hỏi được; `""` = lịch đang tắt; hoặc `"HH:MM"`.

        Đi qua `gio_hhmm` chứ KHÔNG cắt `[:5]`: Windows in giờ theo định dạng
        vùng của máy — xem ghi chú trong `ui_qt/widgets.py::gio_hhmm`.
        """
        if self._lich is None:
            return None
        if not self._lich.get("da_dang_ky"):
            return ""
        return gio_hhmm(self._lich.get("gio"))

    def _ve_lich(self) -> None:
        gio = self._gio_lich()
        if gio is None:
            self._nhan_lich.setText("đang xem lịch của Windows…")
            return
        if gio:
            t = QTime.fromString(gio, "HH:mm")
            if t.isValid() and not self._o_gio_lich.hasFocus():
                self._o_gio_lich.setTime(t)
            self._nut_lich.setText("Tắt lịch")
            cuoi = lan_chay_gon((self._lich or {}).get("lan_chay_cuoi"))
            ket = str((self._lich or {}).get("ket_qua_cuoi") or "").strip()
            # Trên MÀN HÌNH chỉ KẾT QUẢ lần chạy cuối ("chạy xong, không kênh
            # nào lỗi") — đó là câu người ta cần. Mốc thời gian Windows in ra
            # là chuỗi 12 tiếng dài loằng ngoằng, nó thuộc về tooltip.
            chu = "đang BẬT" + (" · " + ket if ket else "")
            self._nhan_lich.setText(chu)
            self._nhan_lich.setToolTip(
                "Lịch ShopAPI-TuChay đang bật, chạy {0} mỗi ngày.{1}".format(
                    gio, "\nLần chạy cuối: {0} — {1}".format(cuoi, ket or "?")
                    if cuoi else "\nChưa chạy lần nào."))
        else:
            self._nut_lich.setText("Bật lịch")
            self._nhan_lich.setText("đang TẮT — không kênh nào tự chạy khi bạn vắng")

    def _bat_tat_lich(self) -> None:
        goc = self._app.base_dir
        bat = self._nut_lich.text() == "Bật lịch"
        gio = self._o_gio_lich.time().toString("HH:mm")

        def viec():
            from core import lich_tu_chay  # noqa: PLC0415

            return lich_tu_chay.dang_ky(goc, gio=gio) if bat else lich_tu_chay.huy(goc)

        def xong(ket) -> None:
            _ok, msg = ket
            self._app.show_message("Lịch chạy hằng ngày", msg or "Xong.")
            self._hoi_lich()

        self._app.run_bg(viec, on_ok=xong, on_err=self._app.show_error)

    # ── Hai hộp của từng kênh ────────────────────────────────────────────────

    def _mo_cai_dat(self, ma: str) -> None:
        """Mở hộp ⚙ Cài đặt của ĐÚNG kênh này.

        `show()` chứ không `exec_()`: hộp không khoá cửa sổ chính, nên nhật ký
        30 giây vẫn chạy và người ta vẫn liếc được ba cột kia trong lúc sửa.
        """
        hop = self._hop_cai.get(ma)
        if hop is None:
            return
        k = self._kenh(ma)
        if k is not None:
            hop.nap(k, self._cai_vm.get(ma) or {})
        hop.show()
        hop.raise_()
        hop.activateWindow()

    def _mo_nhat_ky_kenh(self, ma: str) -> None:
        """Bấm câu tình trạng → nhật ký hôm nay của chính kênh ấy."""
        hop = self._hop_nhat_ky.get(ma)
        if hop is None:
            return
        k = self._kenh(ma)
        if k is not None:
            hop.nap(k)
        hop.show()
        hop.raise_()
        hop.activateWindow()

    # ── Kiểm soát ────────────────────────────────────────────────────────────

    def _chay_ngay(self, ma: str) -> None:
        k = self._kenh(ma) or {}
        if not k.get("ngan_sach_ngay"):
            self._app.show_message(
                "Chưa đặt trần tiền",
                "Kênh {0} đang để trần 0₫, nghĩa là KHÔNG sản xuất gì cả. Bấm "
                "“⚙ Cài đặt” ở cột kênh, đặt “Tiền mỗi ngày” rồi bấm lại.".format(ma))
            return
        hoi = QMessageBox.question(
            self, "Chạy ngay",
            "Làm video hôm nay cho kênh {0} ngay bây giờ?\n\nTốn tiền thật, "
            "trong trần {1}/ngày. Video mất khoảng 2–4 giờ.".format(
                ma, _vnd_gon(k.get("ngan_sach_ngay"))))
        if hoi != QMessageBox.Yes:
            return
        goc = self._app.base_dir

        def xong(ket) -> None:
            ok, msg = ket
            if not ok:
                self._app.show_message("Chưa chạy được", msg)
            self._nhan_luc.setText(msg)
            QTimer.singleShot(3000, self.lam_moi)

        self._app.run_bg(lambda: tt.chay_ngay(goc, ma), on_ok=xong,
                         on_err=self._app.show_error)

    def _doi_cong_tac(self, ma: str, khoa: str, bat: bool) -> None:
        """Bốn công tắc, HAI nơi lưu — mỗi nơi đúng một đường ghi có sẵn.

        `tu_chay` và `tu_don` là quyết định về SẢN XUẤT, nằm trong `kenh.yaml`
        (`core.trung_tam.ghi_cai_kenh`). `tu_dang` và `tu_tra_loi_cmt` là lệnh
        cho MÁY ẢO, nằm trong `CHANNEL/<kênh>/may-ao.json`
        (`core.vm_cai_dat.luu`) — trạm đính kèm nó vào phản hồi mỗi lượt agent
        hỏi việc, nên gạt ở đây là máy ảo nhận trong một nhịp tim.
        """
        if not self._con_song() or not ma:
            return
        goc = self._app.base_dir
        try:
            if khoa in ("tu_chay", "tu_don"):
                tt.ghi_cai_kenh(goc, ma, **{khoa: bool(bat)})
            else:
                from core import vm_cai_dat  # noqa: PLC0415

                vm_cai_dat.luu(goc, ma, **{khoa: bool(bat)})
        except Exception as loi:  # noqa: BLE001
            self._app.show_error(loi)
            return
        if khoa == "tu_chay" and bat and not (self._kenh(ma) or {}).get("ngan_sach_ngay"):
            self._app.show_message(
                "Chưa đặt trần tiền",
                "Đã bật tự chạy cho {0}, nhưng trần tiền mỗi ngày đang là 0₫ — "
                "tool sẽ KHÔNG sản xuất cho tới khi bạn đặt một con số ở ô "
                "“Tiền mỗi ngày” ngay trong hộp cài đặt này.".format(ma))
        self.lam_moi()

    def _doi_ngan_sach(self, ma: str, gia_tri: int) -> None:
        if not self._con_song() or not ma:
            return
        try:
            tt.ghi_cai_kenh(self._app.base_dir, ma, ngan_sach_ngay=int(gia_tri))
        except Exception as loi:  # noqa: BLE001
            self._app.show_error(loi)

    def _doi_gio_dang(self, ma: str, gio: str) -> None:
        """Giờ đăng của kênh — khoá `gio_dang` trong `kenh.yaml`.

        Cùng một cửa ghi mà "Nội dung → Quản lý kênh" đang dùng
        (`core.trung_tam.ghi_cai_kenh`), và cùng khoá mà `core/tu_chay.py` đọc
        để hẹn giờ lên sóng (`_tim_gio_trong`). `core` không có cửa nào khác
        để đặt giờ đăng mặc định cho một kênh.
        """
        if not self._con_song() or not ma or not gio:
            return
        try:
            tt.ghi_cai_kenh(self._app.base_dir, ma, gio_dang=str(gio))
        except Exception as loi:  # noqa: BLE001
            self._app.show_error(loi)

    def _doi_phut_phien(self, ma: str, phut: int) -> None:
        """Phút mở phiên trước giờ đăng — của RIÊNG kênh này."""
        if not self._con_song() or not ma:
            return
        try:
            from core import vm_cai_dat  # noqa: PLC0415

            vm_cai_dat.luu(self._app.base_dir, ma, phien_truoc_phut=int(phut))
        except Exception as loi:  # noqa: BLE001 — lưu hỏng phải nói, không văng
            self._app.show_error(loi)

    def _tam_dung_tat_ca(self) -> None:
        """Một cú bấm dừng vòng tự chạy của MỌI kênh — và bật lại đúng chừng ấy.

        Danh sách kênh vừa bị dừng được nhớ trong `workspace/trung-tam.json`.
        Không nhớ thì nút "Bật lại" sẽ bật cả những kênh chủ dự án đã cố ý tắt
        từ trước — tức là nút hoàn tác tự ý làm thêm việc không ai nhờ.
        """
        if not self._con_song():
            return
        goc = self._app.base_dir
        dang_tam = list((tt.doc_cai(goc) or {}).get(KHOA_TAM_DUNG) or [])
        if dang_tam:
            self._bat_lai(dang_tam)
            return
        dang_bat = [k["ma"] for k in ((self._anh or {}).get("kenh") or [])
                    if k.get("tu_chay")]
        if not dang_bat:
            self._app.show_message(
                "Không có gì để dừng",
                "Hiện không kênh nào đang bật tự chạy.")
            return
        hoi = QMessageBox.question(
            self, "Tạm dừng tất cả",
            "Tắt tự chạy cho {0} kênh ({1})?\n\nLượt đang chạy dở vẫn chạy nốt. "
            "Từ lượt sau thì không kênh nào tự làm video nữa, cho tới khi bạn "
            "bấm “Bật lại”.".format(len(dang_bat), ", ".join(dang_bat)))
        if hoi != QMessageBox.Yes:
            return
        da_tat = []
        for ma in dang_bat:
            try:
                tt.ghi_cai_kenh(goc, ma, tu_chay=False)
            except Exception as loi:  # noqa: BLE001
                self._app.show_error(loi)
                continue
            da_tat.append(ma)
        try:
            tt.luu_cai(goc, **{KHOA_TAM_DUNG: da_tat})
        except Exception:  # noqa: BLE001 — nhớ hụt thì nút Bật lại biến mất, không sập
            pass
        self.lam_moi()

    def _bat_lai(self, cac_ma: List[str]) -> None:
        goc = self._app.base_dir
        for ma in cac_ma:
            try:
                tt.ghi_cai_kenh(goc, ma, tu_chay=True)
            except Exception as loi:  # noqa: BLE001
                self._app.show_error(loi)
        try:
            tt.luu_cai(goc, **{KHOA_TAM_DUNG: []})
        except Exception:  # noqa: BLE001
            pass
        self.lam_moi()

    def _ve_nut_tam_dung(self) -> None:
        dang_tam = list((tt.doc_cai(self._app.base_dir) or {}).get(KHOA_TAM_DUNG) or [])
        if dang_tam:
            self._nut_tam_dung.setText("Bật lại tất cả")
            self._nut_tam_dung.setToolTip(
                "Bật lại tự chạy cho đúng {0} kênh đã bị nút “Tạm dừng tất cả” "
                "tắt: {1}.".format(len(dang_tam), ", ".join(dang_tam)))
        else:
            self._nut_tam_dung.setText("Tạm dừng tất cả")
            self._nut_tam_dung.setToolTip(
                "Tắt vòng tự chạy của MỌI kênh trong một cú bấm. Lượt đang chạy "
                "dở vẫn chạy nốt; từ lượt sau thì không kênh nào tự làm nữa.")

    # ── Làm mới ──────────────────────────────────────────────────────────────

    def _kenh(self, ma: str) -> Optional[Dict[str, Any]]:
        for k in (self._anh or {}).get("kenh") or []:
            if k.get("ma") == ma:
                return k
        return None

    def lam_moi(self, bat_buoc: bool = True) -> None:
        if not self._con_song() or (not bat_buoc and not self.isVisible()):
            return
        if self._dang_nap:
            return
        self._dang_nap = True
        goc = self._app.base_dir
        gio_lich = self._gio_lich()
        gs = _giam_sat(self._app)
        if self._lich is not None and time.monotonic() - self._lich_luc > GIAY_HOI_LICH:
            self._hoi_lich()

        def viec():
            anh = tt.anh_chup(goc, co_nhom=False, gio_lich=gio_lich)
            may = {}
            if gs is not None:
                try:
                    may = dict(gs.trang_thai() or {})
                except Exception:  # noqa: BLE001
                    may = {}
            cai_vm = {}
            try:
                from core import vm_cai_dat  # noqa: PLC0415

                for k in anh.get("kenh") or []:
                    cai_vm[k["ma"]] = dict(vm_cai_dat.doc(goc, k["ma"]))
            except Exception:  # noqa: BLE001 — thiếu tệp thì dùng mặc định
                pass
            return anh, may, cai_vm

        def loi(e) -> None:
            self._dang_nap = False
            self._nhan_luc.setText("Không đọc được: {0}".format(str(e)[:120]))

        self._app.run_bg(viec, on_ok=self._nhan_anh, on_err=loi)

    def _nhan_anh(self, ket) -> None:
        self._dang_nap = False
        if not self._con_song():
            return
        anh, may, cai_vm = ket
        self._anh = anh
        self._may = may
        self._cai_vm = cai_vm
        tien = anh.get("tien") or {}
        self._o_tien.dat("~{0} hôm nay".format(_vnd_gon(tien.get("hom_nay"))),
                         THUONG,
                         "Hôm nay ~{0}, tháng này ~{1} (ước tính).".format(
                             _vnd_gon(tien.get("hom_nay")),
                             _vnd_gon(tien.get("thang"))))
        self._nhan_luc.setText("cập nhật {0}".format(str(anh.get("luc") or "")[11:16]))
        self._ve_dia()
        self._ve_vi()
        self._ve_lich()
        self._ve_may()
        self._ve_cot(list(anh.get("kenh") or []))
        self._ve_viec()
        self._ve_nut_tam_dung()
