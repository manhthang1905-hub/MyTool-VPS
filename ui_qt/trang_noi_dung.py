"""Trang **NỘI DUNG** — mọi thứ về CÁI VIDEO, gom vào một chỗ (chế độ VPS).

Chủ dự án, 21/09/2026: *"thiết kế lại all để phù hợp với tool auto trên vps
này"*. Ba trang, không phải mười ba (xem `core/che_do_vps.py`). Trang này là
trang thứ hai: *cái máy đang làm nội dung gì, và nội dung ấy được đặt thế nào*.

═══ BỌC LẠI, KHÔNG VIẾT LẠI ═══

Bốn màn hình dưới đây đã chạy nhiều tháng trên máy thật. Viết lại chúng cho
"gọn" là vứt đi chừng ấy thứ đã sửa đúng, và không ai nhớ hết được những ca
lẻ chúng đang xử lý. Nên chúng vào đây NGUYÊN CON, làm tab con:

    Duyệt & đăng   `trang_trung_tam.TrangTrungTam` — tiến độ từng lượt, hàng
                   chờ duyệt, hiệu quả 24/48/72 giờ, nhật ký, cài đặt kênh
    Sản xuất       `trang_auto.TrangTuDong` — dây chuyền tám khâu, chạy tay
    Đối thủ        `trang_phan_tich.TrangPhanTich` — nghiên cứu, công thức V7
    Quản lý kênh   `trang_quan_ly_kenh.TrangQuanLyKenh` — MỌI thiết lập của
                   từng kênh, sửa ngay trên giao diện (không mở kenh.yaml)

Không màn hình nào của bản sáu-tab bị mất; chúng chỉ đổi cửa vào.
"""

from __future__ import annotations

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QScrollArea, QTabWidget, QVBoxLayout, QWidget

from .widgets import tieu_de_trang

__all__ = ["TrangNoiDung", "TAB_CON"]

#: Nhãn các tab con, theo thứ tự hiện ra. Nhãn NGẮN — `MyTool/CLAUDE.md`.
TAB_CON = ("Duyệt && đăng", "Sản xuất", "Đối thủ", "Quản lý kênh")


class TrangNoiDung(QWidget):
    def __init__(self, app):
        super().__init__()
        self._app = app

        doc = QVBoxLayout(self)
        doc.setContentsMargins(16, 12, 16, 12)
        doc.setSpacing(8)
        doc.addWidget(tieu_de_trang(
            "Nội dung",
            "Video nào chờ duyệt, lấy nguồn từ đâu, và mỗi kênh được đặt thế nào.",
            "noi-dung"))

        self.tabs = QTabWidget()
        from .trang_auto import TrangTuDong  # noqa: PLC0415
        from .trang_phan_tich import TrangPhanTich  # noqa: PLC0415
        from .trang_quan_ly_kenh import TrangQuanLyKenh  # noqa: PLC0415
        from .trang_trung_tam import TrangTrungTam  # noqa: PLC0415

        self.duyet = TrangTrungTam(app)
        self.san_xuat = TrangTuDong(app)
        self.doi_thu = TrangPhanTich(app)
        self.quan_ly = TrangQuanLyKenh(app)
        for trang, ten in ((self.duyet, TAB_CON[0]), (self.san_xuat, TAB_CON[1]),
                           (self.doi_thu, TAB_CON[2]), (self.quan_ly, TAB_CON[3])):
            self.tabs.addTab(self._cuon(trang), ten)
        doc.addWidget(self.tabs, 1)

    @staticmethod
    def _cuon(trang: QWidget) -> QWidget:
        """Mỗi tab con nằm trong vùng cuộn DỌC riêng.

        Bốn màn hình này vốn là TRANG cấp cao, mỗi cái được `CuaSoChinh._boc_cuon`
        bọc một vùng cuộn. Thành tab con thì cái vỏ ấy không còn — và màn hình
        cao hơn cửa sổ bị cắt đáy, đúng lỗi `tests/test_bo_cuc.py` canh. Bọc lại
        ở đây, một chỗ.
        """
        cuon = QScrollArea()
        cuon.setWidget(trang)
        cuon.setWidgetResizable(True)
        cuon.setFrameShape(QScrollArea.NoFrame)
        cuon.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        cuon.setMinimumWidth(1)
        return cuon

    def mo_tab(self, ten: str) -> None:
        """Mở một tab con theo nhãn — cho trang khác gọi sang."""
        for i in range(self.tabs.count()):
            if self.tabs.tabText(i) == ten:
                self.tabs.setCurrentIndex(i)
                return

    # ── Chuyển tiếp cho cửa sổ chính ─────────────────────────────────────────

    def doi_du_an(self, ten: str) -> None:
        for con in (self.duyet, self.san_xuat, self.doi_thu, self.quan_ly):
            tiep = getattr(con, "doi_du_an", None)
            if tiep is not None:
                try:
                    tiep(ten)
                except Exception:  # noqa: BLE001 — một mục hỏng không kéo mục kia
                    pass
