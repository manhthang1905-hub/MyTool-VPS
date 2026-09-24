"""MyTool đang chạy trên VPS, cạnh chính thư mục `vm/` nó phải nuôi.

═══ KIẾN TRÚC (chốt ở `vm/KE-HOACH-5-KENH.md`, bước E) ═══

Trên VPS, thứ DUY NHẤT hiện ra màn hình là MyTool đầy đủ (bản Studio này),
cài như một thư mục ANH EM (`MyTool\\`) nằm CẠNH `vm\\` và các thư mục trình
duyệt từng kênh — không còn bảng Tkinter riêng của `vm/giao_dien.py` nữa (nó
tự lui khi thấy dấu này, xem `vm/giao_dien.py::da_dung_mytool_vps`).

Dấu hiệu là một tệp `vps.json` NẰM NGAY TRONG thư mục MyTool (cạnh
`shopapi_studio_qt.py`)::

    {"vm_dir": "<đường tuyệt đối tới thư mục vm/ anh em>", ...}

Bộ cài (`vm/cai_dat_vps.py`, việc của một phiên khác) ghi tệp này một lần lúc
cài; mọi thứ trong tệp này CHỈ ĐỌC, không ghi.

Không import Qt — module này chạy sớm trong `main()` của
`shopapi_studio_qt.py`, kể cả khi PyQt5 hỏng, và cũng phải test được không
cần dựng cửa sổ nào.
"""

from __future__ import annotations

import json
import os
from typing import Any, Dict, Optional, Sequence, Tuple

__all__ = ["TEN_MARKER", "la_vps", "doc", "thu_muc_vm", "trang_mo_dau",
           "loc_trang", "TRANG_VPS", "KHOA_TRANG_VPS", "KHOA_TRANG_TRUNG_TAM"]

#: Tên tệp dấu hiệu, nằm cạnh `shopapi_studio_qt.py`.
TEN_MARKER = "vps.json"

#: Khoá trang mở đầu khi ở chế độ VPS — màn hình **Điều khiển**
#: (`ui_qt/trang_dieu_khien.py`).
KHOA_TRANG_TRUNG_TAM = "dieu-khien"


def _duong_marker(goc: str) -> str:
    return os.path.join(goc, TEN_MARKER)


def la_vps(goc: str) -> bool:
    """Máy này có đang chạy MyTool ở "chế độ VPS" không — chỉ nhìn tệp có
    mặt hay không, không đọc nội dung (đọc hỏng thì việc khác lo, câu hỏi
    của hàm này chỉ là "có" hay "không")."""
    try:
        return os.path.isfile(_duong_marker(goc))
    except OSError:
        return False


def doc(goc: str) -> Dict[str, Any]:
    """Đọc `vps.json`. Không có tệp, hay tệp hỏng, đều trả về `{}` —
    đường khởi động không được ném lỗi vì một tệp cấu hình xấu."""
    try:
        with open(_duong_marker(goc), "r", encoding="utf-8") as tep:
            gia_tri = json.load(tep)
    except (OSError, ValueError):
        return {}
    return gia_tri if isinstance(gia_tri, dict) else {}


def thu_muc_vm(goc: str) -> str:
    """Thư mục `vm/` anh em mà máy này phải giám sát — đã kiểm tồn tại.

    Ném `FileNotFoundError` khi không ở chế độ VPS, thiếu khoá `vm_dir`,
    hay đường dẫn đó không còn là một thư mục (bị xoá, đổi tên, ổ đĩa rớt).
    Nơi gọi (móc khởi động) tự bọc `try/except` — lỗi ở đây không được
    chặn tool mở lên, chỉ là giám sát không bật được.
    """
    du = doc(goc)
    vm_dir = str(du.get("vm_dir") or "").strip()
    if not vm_dir:
        raise FileNotFoundError(
            "vps.json không có 'vm_dir' — bộ cài VPS chưa ghi xong hoặc tệp hỏng")
    if not os.path.isdir(vm_dir):
        raise FileNotFoundError(
            "vm_dir trong vps.json không phải thư mục đang có: {0}".format(vm_dir))
    return vm_dir


def trang_mo_dau(goc: str) -> Optional[str]:
    """Trang mở đầu khi MyTool chạy ở chế độ VPS, hay `None` để giữ mặc
    định thường (`CuaSoChinh.TRANG_DAU`).

    Thuần đọc — vỏ Qt (`ui_qt/app.py`, việc của một phiên khác) là nơi
    thật sự dùng giá trị này để chọn trang mở đầu.
    """
    return KHOA_TRANG_TRUNG_TAM if la_vps(goc) else None


#: ═══ BA TRANG, KHÔNG PHẢI MỘT KHÚC CẮT CỦA MƯỜI BA ═══
#:
#: Bản trước giữ lại 6 trong 13 tab của bản máy nhà. Chủ dự án xem bản ấy trên
#: máy thật, 21/09/2026: *"cái giao diện nó xấu quá"*, *"tab vps có cần đâu"*,
#: *"thiết kế lại all để phù hợp với tool auto trên vps này"*, *"vì mọi thứ là
#: auto nên nó sẽ cần các tính năng cả phần để kiểm soát quản lý"*.
#:
#: Sáu tab ấy là sáu mảnh của một tool DÙNG TAY bị cắt bớt, không phải hình
#: của một máy chạy không người trông. Máy này trả lời đúng ba câu, mỗi câu
#: một trang:
#:
#:   ĐIỀU KHIỂN   máy còn sống không, bốn kênh đang ở khâu nào, tắt/bật cái gì
#:   NỘI DUNG     video nào chờ duyệt, đối thủ, công thức, cài đặt từng kênh
#:   MÁY & VÍ     nhật ký, sự cố, lịch Windows, báo động, số dư, nạp tiền
#:
#: Không trang nào của bản cũ bị VỨT: chúng thành tab con bên trong ba trang
#: này (`ui_qt/trang_noi_dung.py`, `ui_qt/trang_may_vi.py`). Trang DUY NHẤT bị
#: bỏ hẳn là tab "VPS" (`chrome-sach` → `ui_qt/trang_vps.py`): nó để THUÊ máy
#: ảo rồi bấm Remote Desktop vào máy — ngồi ngay trên chính máy đó thì vô
#: nghĩa. Phần hạ tầng của tab ấy (trạm 8765 + cài tiện ích) KHÔNG mất, nó
#: nằm trong "Máy & Ví → Trạm & tiện ích".
#:
#: Bớt trang ở đây cũng là bớt việc lúc mở tool: `_dung_cac_trang()` dựng HẾT
#: các trang trong danh sách nav ngay lúc khởi động.
TRANG_VPS = (
    ("dieu-khien", "", "Điều khiển"),
    ("noi-dung", "", "Nội dung"),
    # Viết MỘT dấu `&`, y như mọi nhãn khác trong `ui_qt.app.TRANG`: Qt coi `&`
    # trong nhãn nút là phím tắt và giấu nó đi, nên `ThanhBen` tự nhân đôi lúc
    # dựng nút. Nhân đôi sẵn ở đây là nhân đôi hai lần → hiện ra "Máy && Ví".
    ("may-vi", "", "Máy & Ví"),
)

#: Khoá của ba trang trên — để nơi khác hỏi "khoá này có ở chế độ VPS không".
KHOA_TRANG_VPS = tuple(muc[0] for muc in TRANG_VPS)


def loc_trang(
    goc: str, trang: Sequence[Tuple[str, str, str]]
) -> Tuple[Tuple[str, str, str], ...]:
    """Danh sách trang thanh bên: ba trang VPS, hay nguyên danh sách máy nhà.

    Nhận `trang` thay vì tự đọc `ui_qt.app.TRANG` để module này (không được
    import Qt) khỏi phải kéo theo `ui_qt` — nơi gọi (`CuaSoChinh.__init__`)
    tự truyền `self.TRANG_SAN_PHAM` vào.

    Ở chế độ VPS hàm này **thay** danh sách chứ không lọc nó: ba trang VPS là
    ba cái vỏ gom lại, không phải ba mục có sẵn trong `ui_qt.app.TRANG` (thêm
    chúng vào đó là máy nhà cũng mọc ba tab thừa).
    """
    if not la_vps(goc):
        return tuple(trang)
    return tuple(TRANG_VPS)
