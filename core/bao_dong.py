"""Báo động RA NGOÀI máy — Telegram / webhook, mặc định TẮT, có chống spam.

## Vì sao KHÔNG mở rộng `core.alerts`

`core.alerts` (ví sắp cạn) cố ý THUẦN TUÝ — không gọi mạng, không đụng giao
diện — xem đúng câu đó ở docstring `assess_balance`: *"Thuần tuý — không gọi
mạng, không đụng giao diện — nên test được bằng số dựng tay."* Nhét việc gọi
Telegram/webhook (I/O mạng, có thể treo, có thể lộ token) thẳng vào đó là phá
hợp đồng ấy — mọi test hiện có của `alerts.py` (và test mới của module này)
sẽ phải phân biệt "tính toán thuần" với "có gọi mạng", dễ lẫn.

Nên: `core.bao_dong` là module RIÊNG, chỉ lo một việc — bắn một dòng chữ RA
NGOÀI máy qua một hoặc nhiều "đường dây" đã cấu hình. `core.alerts` (hoặc bất
kỳ chỗ nào khác trong tool phát hiện sự cố) gọi sang đây qua hàm công khai
:func:`bao_dong`; xem thêm :func:`core.alerts.canh_bao_ra_ngoai` — cầu nối mỏng
giữa hai module, KHÔNG đụng vào tính thuần tuý của `assess_balance`.

## Cấu hình: `bao-dong.json` — KHÔNG nằm trong `config.json`/`secrets.json`

Ba lý do tách riêng:

1. `config.json` là HỢP ĐỒNG CỐ ĐỊNH (xem đầu `core/config.py`) — thêm trường
   vào đó là thêm nghĩa vụ tương thích ngược cho một file vốn không liên quan
   gì tới việc báo động.
2. Token bot Telegram / URL webhook (có thể mang key trong query string) là bí
   mật, nhưng `secrets.json` hiện chỉ chứa đúng ba thứ (`api_key`,
   `refresh_token`, `account_email`) mà `core.config` biết cách đọc/ghi/di
   trú — nhét thêm vào đó buộc phải sửa `Config`/`to_secrets`, lan sang một
   module không liên quan.
3. Quan trọng nhất: **THIẾU FILE = TẮT HẲN, không lỗi.** Một file cấu hình
   riêng, độc lập, rỗng-là-tắt, giúp việc "chưa cấu hình thì im lặng" trở
   thành hành vi TỰ NHIÊN (không tìm thấy file) thay vì phải nhớ thêm một cờ
   `bat_bao_dong` nằm lẫn trong file khác.

Định dạng (mọi trường đều tuỳ chọn — thiếu `telegram` VÀ `webhook` thì coi như
chưa cấu hình gì, `bao_dong()` không làm gì cả):

```json
{
  "enabled": true,
  "cooldown_giay": 3600,
  "telegram": {
    "bot_token": "123456789:AAExampleTokenKhongPhaiThat",
    "chat_id": "987654321"
  },
  "webhook": {
    "url": "https://example.com/hoi-chuong-bao-dong",
    "headers": { "Authorization": "Bearer vi-du-khong-phai-that" }
  }
}
```

* `enabled`: công tắc tắt nhanh không cần xoá token (mặc định `true` NẾU file
  tồn tại — file không tồn tại thì mặc định coi như tắt, xem trên).
* `cooldown_giay`: khoảng lặng tối thiểu giữa hai lần bắn CÙNG `loai` sự cố.
  Mặc định :data:`COOLDOWN_MAC_DINH_GIAY` (1 giờ).
* `telegram`: cần cả `bot_token` lẫn `chat_id` mới tính là đã cấu hình. Lấy
  `chat_id` bằng cách nhắn bot rồi gọi `getUpdates`, hoặc dùng @userinfobot.
* `webhook`: cần `url`; `headers` tuỳ chọn (vd thêm khoá xác thực riêng của
  dịch vụ nhận — Slack incoming webhook, n8n, Discord (qua adapter), ...).

Bật CẢ HAI đường cùng lúc thì `bao_dong()` bắn cả hai — không đường nào loại
trừ đường nào; một đường lỗi không chặn đường kia (xem :func:`bao_dong`).

## Vì sao `urllib.request` chứ không phải `requests`

`core/*.py` khác gọi mạng qua `urllib.request` thuần chuẩn (xem
`core/mang_an_toan.py`, `core/anh_doi_thu.py`...) — không phải vì thiếu
`requests` trong `requirements.txt`, mà để khỏi kéo thêm phụ thuộc cho một
việc gọn (POST JSON, không cần session/retry phức tạp). Theo đúng nếp đó.

## Chống spam: vì sao khoá theo `loai`, không khoá toàn cục

Một sự cố (vd trạm chết) có thể được PHÁT HIỆN LẠI mỗi nhịp kiểm tra trong khi
một sự cố KHÁC (vd ví cạn) xảy ra đúng lúc đó — khoá TOÀN CỤC sẽ làm sự cố thứ
hai bị nuốt mất chỉ vì tới sau sự cố thứ nhất chưa đầy 1 giờ. Khoá theo `loai`
(một chuỗi tự đặt, vd `"tram_chet"`, `"vi_can"`, `"dia_day"`) thì mỗi loại sự
cố có đồng hồ chống spam RIÊNG — đúng tinh thần "công cụ chạy nhiều năm không
ai ngồi xem": báo đủ để không bỏ sót, không báo dồn tới mức bị tắt thông báo.

Bộ nhớ chống spam sống TRONG TIẾN TRÌNH (dict + khoá luồng) — tiến trình khởi
động lại thì đồng hồ reset về 0, nghĩa là có thể bắn lại ngay sau khi tool tự
khởi động lại. Chấp nhận được: tool khởi động lại vốn không phải chuyện xảy ra
mỗi phút, và "vừa khởi động lại là một tin đáng báo" cũng hợp lý hơn là mất
tích vĩnh viễn vì lỡ nhớ nhầm sang phiên chạy trước.
"""

from __future__ import annotations

import json
import os
import threading
import time
from typing import Any, Dict, Optional, Tuple

from . import mang_an_toan

__all__ = [
    "BAO_DONG_FILENAME",
    "COOLDOWN_MAC_DINH_GIAY",
    "bao_dong_path_for",
    "doc_cau_hinh_bao_dong",
    "bao_dong",
    "quen_lich_su_chong_spam",
]

#: Tên file cấu hình — nằm cạnh `config.json`/`secrets.json` nhưng KHÔNG phải
#: một trong hai file đó (xem lý do ở đầu module).
BAO_DONG_FILENAME = "bao-dong.json"

#: Khoảng lặng mặc định giữa hai lần bắn CÙNG một `loai` sự cố. 1 giờ: đủ
#: ngắn để chủ dự án biết sự cố còn đang diễn ra (không phải chỉ một lần rồi
#: im), đủ dài để một vòng lặp kiểm tra chạy mỗi vài phút không dội bom hộp
#: thoại Telegram — chạy nhiều năm mà báo dồn dập thì việc đầu tiên chủ dự án
#: làm là tắt hẳn thông báo, mất tác dụng của cả hệ thống.
COOLDOWN_MAC_DINH_GIAY = 3600.0
#: Thư mục gốc mặc định (MyTool/) — dùng khi nơi gọi không tự truyền `goc`,
#: để hàm công khai :func:`bao_dong` gọi được với đúng 3 tham số như mô tả.
_GOC_MAC_DINH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

_KHOA = threading.Lock()
#: `loai` -> mốc thời gian (giây, `time.time()`) của lần bắn gần nhất.
_LAN_BAN_CUOI: Dict[str, float] = {}


def bao_dong_path_for(goc: str) -> str:
    """`<goc>` (thư mục chứa `config.json`) → đường dẫn `bao-dong.json`.

    Cùng khuôn với :func:`core.secrets.secrets_path_for` — nhận thư mục gốc
    thay vì tự đoán, vì `core/*.py` khác cũng luôn nhận `goc`/`base_dir` từ
    nơi gọi (GUI, `tu_chay.py`...) chứ không tự suy ra vị trí cài đặt.
    """
    return os.path.join(goc, BAO_DONG_FILENAME)


def doc_cau_hinh_bao_dong(goc: str) -> Optional[Dict[str, Any]]:
    """Đọc `bao-dong.json`. Không có file / file hỏng → `None` (im lặng)."""
    try:
        with open(bao_dong_path_for(goc), "r", encoding="utf-8") as tep:
            du_lieu = json.load(tep)
    except (OSError, ValueError):
        return None
    return du_lieu if isinstance(du_lieu, dict) else None


def _kenh_telegram(cfg: Dict[str, Any]) -> Optional[Tuple[str, str]]:
    tg = cfg.get("telegram")
    if not isinstance(tg, dict):
        return None
    token = str(tg.get("bot_token") or "").strip()
    chat_id = str(tg.get("chat_id") or "").strip()
    if not token or not chat_id:
        return None
    return token, chat_id


def _kenh_webhook(cfg: Dict[str, Any]) -> Optional[Tuple[str, Optional[Dict[str, str]]]]:
    wh = cfg.get("webhook")
    if not isinstance(wh, dict):
        return None
    url = str(wh.get("url") or "").strip()
    if not url:
        return None
    headers = wh.get("headers")
    return url, (dict(headers) if isinstance(headers, dict) else None)


def _http_post(
    url: str,
    payload: Dict[str, Any],
    *,
    headers: Optional[Dict[str, str]] = None,
    timeout: float = 10.0,
) -> None:
    """Điểm DUY NHẤT chạm mạng của module này.

    Tách riêng thành hàm nhỏ để test monkeypatch ĐÚNG một chỗ này — không ai
    được gọi mạng thật trong bộ test (xem `MyTool/tests/test_bao_dong.py`).
    """
    tieu_de = {}
    if headers:
        tieu_de.update({str(k): str(v) for k, v in headers.items()})
    # Đi qua `core/mang_an_toan` chứ không `urlopen` trần: tool mang theo bộ
    # chứng chỉ của chính nó vì kho gốc của Windows hỏng theo đủ kiểu ngoài
    # tầm tay khách (xem docstring tệp ấy). Ở đây còn một lý do riêng — thân
    # yêu cầu này mang khoá bot Telegram, chen được giữa đường là đọc được nó.
    mang_an_toan.dang_json(url, payload, cho=timeout, headers=tieu_de)


def _qua_khoang_lang(loai: str, cooldown_giay: float, bay_gio: float) -> bool:
    """`True` nếu ĐANG trong khoảng lặng chống spam (nên bỏ qua lần bắn này).

    Khi KHÔNG bị chặn, tự cập nhật mốc "lần bắn gần nhất" ngay — kể cả nếu
    lần bắn này rốt cuộc gửi thất bại (mạng lỗi, token sai...): sự cố dai
    dẳng mà kênh báo cũng đang hỏng thì dội liên tục mỗi vài giây cũng vô
    ích, cứ để nhịp sau (sau `cooldown_giay`) thử lại.
    """
    with _KHOA:
        truoc = _LAN_BAN_CUOI.get(loai)
        if truoc is not None and (bay_gio - truoc) < cooldown_giay:
            return True
        _LAN_BAN_CUOI[loai] = bay_gio
        return False


def quen_lich_su_chong_spam(loai: Optional[str] = None) -> None:
    """Xoá bộ nhớ chống spam. `loai=None` → xoá hết. Dùng cho test, hoặc khi
    chủ dự án muốn ép bắn lại ngay một loại sự cố (vd vừa xử lý xong, muốn
    được báo ngay nếu nó tái phát)."""
    with _KHOA:
        if loai is None:
            _LAN_BAN_CUOI.clear()
        else:
            _LAN_BAN_CUOI.pop(loai, None)


def bao_dong(
    loai: str,
    tieu_de: str,
    chi_tiet: str = "",
    *,
    goc: Optional[str] = None,
    bay_gio: Optional[float] = None,
) -> bool:
    """API công khai — MỌI nơi trong tool phát hiện sự cố gọi hàm này.

    `loai`: mã ngắn tự đặt, DÙNG LÀM KHOÁ CHỐNG SPAM (vd `"vi_can"`,
    `"tram_chet"`, `"dia_day"`, `"lich_bo_lo"`) — cùng loại thì tối đa một lần
    mỗi `cooldown_giay`, khác loại thì độc lập nhau.
    `tieu_de`/`chi_tiet`: chữ hiện trong tin nhắn — `chi_tiet` có thể rỗng.
    `goc`: thư mục chứa `bao-dong.json` (mặc định thư mục gốc MyTool — truyền
    tay khi gọi từ test hoặc từ một cài đặt không nằm ở vị trí mặc định).

    Trả `True` nếu đã BẮN (thử gửi) tới ít nhất một kênh và không kênh nào ném
    lỗi; `False` khi: chưa cấu hình, cấu hình tắt (`enabled: false`), đang
    trong khoảng lặng chống spam, hoặc mọi kênh đều gửi lỗi.

    KHÔNG BAO GIỜ ném lỗi ra ngoài — hàm báo sự cố mà chính nó làm sập luồng
    đang cố báo sự cố thì còn tệ hơn im lặng.
    """
    try:
        thu_muc = goc if goc is not None else _GOC_MAC_DINH
        cfg = doc_cau_hinh_bao_dong(thu_muc)
        if not cfg or not bool(cfg.get("enabled", True)):
            return False

        tg = _kenh_telegram(cfg)
        wh = _kenh_webhook(cfg)
        if not tg and not wh:
            return False  # file có nhưng chưa điền đường nào -> coi như chưa cấu hình

        try:
            cooldown = float(cfg.get("cooldown_giay", COOLDOWN_MAC_DINH_GIAY))
        except (TypeError, ValueError):
            cooldown = COOLDOWN_MAC_DINH_GIAY
        cooldown = max(0.0, cooldown)

        luc = bay_gio if bay_gio is not None else time.time()
        if _qua_khoang_lang(str(loai), cooldown, luc):
            return False

        van_ban = tieu_de if not chi_tiet else "{0}\n{1}".format(tieu_de, chi_tiet)
        da_gui = False

        if tg:
            token, chat_id = tg
            try:
                _http_post(
                    "https://api.telegram.org/bot{0}/sendMessage".format(token),
                    {"chat_id": chat_id, "text": van_ban},
                )
                da_gui = True
            except Exception:  # noqa: BLE001 — một kênh hỏng không được chặn kênh kia
                pass

        if wh:
            url, headers = wh
            try:
                _http_post(
                    url,
                    {"loai": loai, "tieu_de": tieu_de, "chi_tiet": chi_tiet, "luc": luc},
                    headers=headers,
                )
                da_gui = True
            except Exception:  # noqa: BLE001
                pass

        return da_gui
    except Exception:  # noqa: BLE001 — xem lời hứa "không bao giờ ném lỗi" ở trên
        return False
