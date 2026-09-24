# Nhật ký phát triển trên VPS này

Ghi những gì đã đổi / thử / hỏng ngay trên MÁY NÀY — khác nhật ký chung của tool. Mỗi mục: ngày, việc, kết quả.

## 2026-09-22 — Thiết kế lại giao diện VPS: 6 tab → 3 trang, bốn cột kênh, mọi núm vặn lên GUI

**Vì sao sửa:** Chủ dự án xem bản sáu-tab trên chính máy này (cửa sổ 1416×1039),
21/09/2026: *"cái giao diện nó xấu quá"*, *"tab vps có cần đâu"*, *"thiết kế lại
all để phù hợp với tool auto trên vps này"*, *"vì mọi thứ là auto nên nó sẽ cần
các tính năng cả phần để kiểm soát quản lý"*, rồi *"tao muốn nó đơn giản hiệu
quả mà có thể quản lý và thiết lập all ở gui để chủ động"*.

Đo được trên ảnh chụp: 40% cửa sổ phía dưới trắng trơn; dải trên là bảy hộp to
nhỏ lệch nhau và phơi tên khoá kỹ thuật `tu_dang` / `tu_tra_loi_cmt`; dải đỏ
nhồi sáu việc vào một dòng chạy dài; thẻ kênh toàn dấu "—" và tên Nhật cắt cụt;
cột trái có ô "DỰ ÁN" vô nghĩa với máy auto, còn nút to nhất góc dưới trái là
"Cập nhật: đã tắt".

**Đã làm:**

* `core/che_do_vps.py` — chế độ VPS không còn LỌC `ui_qt.app.TRANG` nữa mà THAY
  nó bằng ba trang riêng: `dieu-khien` · `noi-dung` · `may-vi`. Trang mở đầu đổi
  sang `dieu-khien`.
* `ui_qt/trang_dieu_khien.py` (mới) — mỗi kênh MỘT CỘT chạy hết chiều cao cửa
  sổ: tám khâu của `tu_chay.py`, nhật ký hôm nay của chính kênh ấy, số 7 ngày,
  tiền, bốn công tắc (tự chạy · tự đăng · trả lời bình luận · tự dọn), ô ngân
  sách/ngày, Chạy ngay / Chạy lại. Thêm dải sức khoẻ, dòng "N việc cần xem" gập
  được, hàng giờ lịch + giờ phiên đăng, và nút **Tạm dừng tất cả** (nhớ danh
  sách kênh vừa tắt trong `workspace/trung-tam.json` để nút "Bật lại" không bật
  nhầm kênh vốn đã tắt).
* `ui_qt/trang_noi_dung.py` + `ui_qt/trang_may_vi.py` (mới) — BỌC các trang sẵn
  có làm tab con, không viết lại: Trung tâm, Video sản xuất tự động, Phân tích &
  Nghiên cứu, Quản lý kênh, Chỉ số/Trạm (bản `phan=("cai","tram")`), Tài khoản &
  Cài đặt. Trang duy nhất bỏ hẳn là tab "VPS" (`ui_qt/trang_vps.py`: thuê máy ảo
  rồi Remote Desktop vào chính máy mình đang ngồi).
* `ui_qt/trang_quan_ly_kenh.py` — thẻ Tự chạy nay sửa được HẾT trên giao diện:
  giọng đọc (kèm cảnh báo trùng giọng trong nhóm qua `core.nhom_kenh.kiem_trung_lap`),
  trần tiền (nói rõ 0₫ = KHÔNG sản xuất), tự đăng, trả lời bình luận, tự dọn +
  `don_sau_gio`, `phut_muc_tieu`, `nhan_tieu_de`, `so_ban_nhap`, bộ vẽ (16 khoá
  `style.yaml` từ `CHANNEL/_KHUON/ve/`) và màu chữ ảnh bìa. Công tắc "Bật đăng
  tự động" cũ (đi theo một ô chọn kênh KHÁC) đã dời lên thẻ này.
* `ui_qt/trang_may_vi.py` — bật/tắt và đổi giờ CẢ HAI lịch Windows
  (`ShopAPI-TuChay`, `ShopAPI-CanhTram`), kênh báo động Telegram (ghi
  `bao-dong.json`, nút "Gửi thử một tin"), nhật ký ba máy con, và nút cập nhật
  tool (dời khỏi góc dưới trái thanh bên).
* `ui_qt/app.py` — chế độ VPS: bỏ ô "DỰ ÁN" ở cột trái, không gắn nút cập nhật
  vào thanh bên, và dựng ba trang mới (nạp muộn, máy nhà không tốn công nạp).

**Lỗi thật tìm ra và đã sửa:** giao diện báo "Lịch hằng ngày ĐANG TẮT" và gắn
"⚠ Chưa bật lịch" lên MỌI kênh trong khi `ShopAPI-TuChay` đang chạy thật.
Nguyên nhân: `core.lich_tu_chay.trang_thai()` trả `gio` đúng như `schtasks` in
ra theo ĐỊNH DẠNG VÙNG của máy — trên máy này là `"2:00:00 AM"` — còn giao diện
cắt `chuỗi[:5]` thành `"2:00:"`, thứ mà `core.trung_tam._gio()` không dựng lại
được. Thêm `ui_qt/widgets.gio_hhmm` (nhận cả `HH:MM`, `HH:MM:SS`,
`H:MM:SS AM/PM`, `SA`/`CH`) và dùng nó ở cả ba chỗ đọc giờ lịch. Kèm theo:
`lan_chay_gon` bỏ mốc giả `11/30/1999` của Windows, và `_TEN_MAY` thêm hai khoá
`tu_dang`/`tu_tra_loi_cmt` (đây chính là chỗ tên khoá kỹ thuật lọt ra màn hình).
`core.trung_tam.mo_ta_tep` nay nhận cả SLUG tệp khán giả, nên cột "Tệp" hiện
"Tò mò" thay vì `nguoi-to-mo-xem-minh-la-kieu-nguoi-nao`.
`core/khoi_dong_vps.py` quét mọi trang để tìm bản giữ trạm 8765 — không thì bỏ
tab `chrome-sach` là trạm KHÔNG bao giờ tự bật và ba con `vm/` ngồi câm.

**Hai lỗi nữa bắt được khi dựng thử trên dữ liệu thật:** (1) thẻ Tự chạy đọc
`tep` của kênh bằng `findData` trên MÃ SỐ, mà bốn kênh thật khai bằng SLUG —
ô rơi về "(chưa chọn)" và cú tự lưu kế tiếp ghi `tep: ""`, tức kênh mất tệp
khán giả mà không ai bấm gì; nay nhớ nguyên văn giá trị trong tệp và chỉ ghi đè
khi người dùng thật sự chọn tệp khác. (2) câu cảnh báo của
`core.nhom_kenh.kiem_trung_lap` viết cho người đọc NHẬT KÝ nên có kèm tên khoá
(`voice_id`, `style_name`…); lên màn hình thì dịch sang chữ thường
(`_bo_ten_khoa`). Nhân đó phát hiện: **cả bốn kênh đang dùng CHUNG một giọng
đọc** — giao diện nay nói thẳng điều đó ngay dưới ô Giọng đọc.

**Đã test:** `python -m pytest tests/ -q` → 150 failed, 3454 passed, 7 skipped,
2 errors. 134/150 lượt fail nằm ở `test_vm_agent` · `test_vm_phien` ·
`test_vm_nhieu_kenh` · `test_goi_vps` (bộ test đòi `vm/` nằm LỒNG trong
`MyTool/`, máy này để `vm/` nằm CẠNH — nền cũ, xem mục 2026-09-19); phần còn
lại là các bài chấm nội dung / ffmpeg / khuôn kênh không đụng tới giao diện.
Bài mới: `tests/test_giao_dien_vps.py` (21 lượt, qua hết). Sửa
`tests/test_bo_cuc.py::test_du_tam_trang_deu_dung_len_duoc` để nó đo theo
`che_do_vps.loc_trang` thay vì `TRANG` trần. Đã dựng thử cả ba trang bằng
`QT_QPA_PLATFORM=offscreen` trên dữ liệu THẬT của máy (ảnh trong
`workspace/anh-thu/`) — không mở cửa sổ nào, không gọi mạng.

## 2026-09-19 — Tool không mở được: thiếu hẳn `core/secrets.py`

**Vì sao sửa:** `CHAY-GON.vbs` báo `ModuleNotFoundError: No module named 'core.secrets'`
(qua `shopapi_studio_qt.py` → `ui_qt/app.py` → `core/api.py` → `core/config.py`).
`core/config.py`, `core/vps_rieng.py` và hai bài test (`tests/test_kho_bi_mat_khong_mat_khoa.py`,
`tests/test_vps.py`) đều đòi `core.secrets.SecretStore` / `secrets_path_for` /
`encryption_available`, nhưng file này chưa từng được `git commit` (tra
`git log --all -- "**/secrets.py"` ra rỗng) nên bản giải nén sang VPS này không
có — không phải lỗi giải nén, mà file gốc chưa tồn tại ở nơi gửi đi.

**Đã làm:** Viết `core/secrets.py` theo đúng hợp đồng mà `config.py`/`vps_rieng.py`
đã mô tả sẵn trong docstring + theo hành vi hai bài test đòi hỏi: kho JSON mã
hoá bằng DPAPI (bảo vệ một khoá Fernet ngẫu nhiên, dữ liệu mã hoá bằng
`cryptography` — đúng gói đã có sẵn trong `requirements.txt` với ghi chú
"cat giu khoa API tren may khach"); máy không phải Windows thì lưu chữ thường
kèm `SecretStore.warning`. Bắt được thêm một lỗi khi viết: `ctypes.windll.kernel32.LocalFree`
không khai `argtypes` thì ném `ArgumentError: int too long to convert` trên
Windows 64-bit (con trỏ vượt 32-bit) — đã khai `argtypes`/`restype` cho
`LocalFree`, `CryptProtectData`, `CryptUnprotectData`.

**Đã test:** `python -m pytest tests/ -q` (cài thêm `pytest` bằng `pip install --user`,
vì máy này chưa có sẵn cho Python hệ thống — không có `.venv` riêng của tool).
Toàn bộ test liên quan tới `secrets`/`vps`/`config` qua (70 passed). 23 test còn
lại fail vì lý do khác hẳn, không liên quan: chúng đòi thư mục `MyTool/vm/`
(agent.py, CAI-DAT-VM.bat…) nằm LỒNG bên trong `MyTool/`, còn trên VPS này `vm/`
là thư mục ANH EM cạnh `MyTool/` (đúng bố cục mô tả ở `CLAUDE.local.md`) — việc
đóng gói/dò `vm/` lồng đó không phải phạm vi lần sửa này. Mở thử tool bằng
`pythonw.exe shopapi_studio_qt.py` trực tiếp: không còn văng lỗi, không sinh
`LOI-KHOI-DONG.txt`, tiến trình chạy được tới lúc tắt bằng tay.

**Tệp đã sửa:** `core/secrets.py` (mới, chưa từng có trong git). Bản vá cần
được mang về kho gốc — xem hướng dẫn ở `CLAUDE.local.md`.

## 2026-09-19 — Sau khi có `core/secrets.py`, tool vẫn sập khi mở bằng CHAY-GON.vbs (pythonw)

**Vì sao sửa:** Vá xong `core/secrets.py` ở trên, mở lại bằng `pythonw.exe` (đúng
đường CHAY-GON.vbs dùng) vẫn sập, ghi vào `workspace/su-co.log`:
`AttributeError: 'NoneType' object has no attribute 'reconfigure'` tại
`core/chi_so_ytb/gom.py:20`, gọi từ lúc dựng tab "Phân tích" (`TrangPhanTich` →
`TrangCongThucV7` → `core.cong_thuc_v7` → `core.chi_so_ytb.gom`, xem
`ui_qt/app.py:452`). Lý do: `pythonw.exe` không có console nên `sys.stdout` là
`None`, mà hai file `core/chi_so_ytb/gom.py` và `core/chi_so_ytb/giai_ma.py`
gọi `sys.stdout.reconfigure(encoding="utf-8")` ngay ở mức module — chạy ĐÚNG
khi tự thực thi bằng `python gom.py ...` (có console), nhưng ở đây chúng còn bị
**import** làm thư viện từ `core/cong_thuc_v7.py`, nên đụng `sys.stdout is None`
là sập cả cửa sổ chính, chưa kịp hiện lên.

**Đã làm:** Bọc `if sys.stdout is not None:` quanh dòng `reconfigure` ở cả hai
file.

**Đã test:** Mở lại bằng `pythonw.exe shopapi_studio_qt.py`, chờ 8 giây rồi kiểm
tra tiến trình — VẪN CÒN SỐNG (trước khi vá thì đã sập/đứng ở hộp thoại lỗi
trong khoảng đó), và `workspace/su-co.log` không có dòng mới (mốc thời gian vẫn
dừng ở lần sập trước khi vá). `python -m pytest tests/ -q`: 3335 passed / 141
failed / 7 skipped — toàn bộ fail còn lại là các test đòi `MyTool/vm/` lồng bên
trong (bố cục khác VPS này dùng, xem mục sửa `core/secrets.py` ở trên), không
liên quan tới `chi_so_ytb`.

**Tệp đã sửa:** `core/chi_so_ytb/gom.py`, `core/chi_so_ytb/giai_ma.py`. Cả hai
cần mang về kho gốc cùng đợt với `core/secrets.py`.

## 2026-09-19 — Vá xong hai lỗi trên, chủ dự án bấm CHAY-GON.vbs vẫn "không lên"

**Vì sao sửa:** Sau hai lỗi ở trên, chủ dự án tự tay chạy `CHAY-GON.vbs` và báo
màn hình vẫn trống. Kiểm tra trực tiếp trên máy (không phải qua log — lần này
tiến trình KHÔNG sập): `tasklist` thấy `pythonw.exe` sống khoẻ, `py-spy dump`
cho thấy `MainThread` nằm yên trong `app.exec_()` — đúng trạng thái một app Qt
đã dựng xong, không kẹt, không văng lỗi. Soi bằng `EnumWindows`/`GetWindowLong`
(P/Invoke qua PowerShell) thì cửa sổ chính CÓ THẬT — đúng kích thước, đúng toạ
độ trên màn hình — nhưng cờ `WS_VISIBLE` của Windows KHÔNG được bật, nên
Windows không vẽ nó ra dù bên trong Qt nghĩ là đã `show()` xong. Thử lại nhiều
lần (ba tiến trình `pythonw.exe` khởi động riêng biệt, kể cả một `QMessageBox`
trơn không có mã của tool) đều dính đúng kiểu này — tức đây không phải lỗi
trong mã của MyTool, mà là trục trặc ở tầng phiên RDP/Windows của VPS này lúc
đó (dựng cửa sổ xong nhưng "quên" hiện).

**Đã làm:**
1. Ép hiện ngay cửa sổ đang chờ bằng `ShowWindow`/`SetForegroundWindow` gọi từ
   tiến trình khác (PowerShell) — đang chờ chủ dự án xác nhận có thấy tool
   sau bước này không.
2. Dọn các tiến trình/cửa sổ trùng do bấm mở nhiều lần trong lúc chờ (một hộp
   thoại "My Tool đang mở rồi" cũng bị dính cùng lỗi vô hình, đứng chờ bấm suốt
   nhiều phút không ai thấy).
3. Thêm `cua_so.raise_()` + `cua_so.activateWindow()` ngay sau `cua_so.show()`
   trong `shopapi_studio_qt.py::main()` — hai lời gọi này cũng đi xuống
   `SetForegroundWindow` phía Windows, tức tự động làm lại đúng cú ép tay vừa
   làm ở bước 1, ngay từ trong tiến trình, phòng khi phiên RDP lại rơi vào đúng
   kiểu này ở lần mở sau.

**Đã test:** Không viết được test tự động cho lỗi tầng hệ điều hành này (bộ
test không mở cửa sổ thật, và đây không phải lỗi logic Python để mô phỏng
bằng unit test). Đã xác nhận qua `py-spy dump` + `EnumWindows`/`GetWindowLong`
rằng tiến trình khoẻ mạnh và cờ `WS_VISIBLE` bật lên đúng khi bị ép — CHƯA có
xác nhận bằng mắt từ chủ dự án là màn hình thật đã hiện tool. Dòng
`raise_()/activateWindow()` mới thêm không đổi hành vi tool lúc mọi thứ bình
thường (hai lời gọi này vô hại, chỉ đưa cửa sổ ra trước — `python -m pytest
tests/ -q` vẫn 3335 passed / 141 failed y như trước, không tăng fail nào).

**Cập nhật cùng ngày — bản vá đầu (`raise_()` + `activateWindow()`) KHÔNG ăn
thua:** Chủ dự án tự tay chạy `CHAY-GON.vbs` sau bản vá đó, báo vẫn không thấy
gì. Đúng — vì `raise_()`/`activateWindow()` là đường Qt bình thường, mà Qt đã
đánh dấu nội bộ "đã show" từ trước nên hai hàm đó chỉ đổi thứ tự Z-order/focus,
KHÔNG phát lại lệnh `ShowWindow` mà lúc đầu đã lặng lẽ hỏng. Đã đổi hẳn sang gọi
THẲNG `ctypes.windll.user32.ShowWindow(hwnd, SW_SHOW)` +
`SetForegroundWindow(hwnd)` trên `int(cua_so.winId())` — bỏ qua sổ sách nội bộ
của Qt, bắn lại vài lần ở các mốc trễ 0/300/1500/4000 ms qua `QTimer.singleShot`
(hàm `_ep_hien_that_su`, phòng khi phiên hiển thị chưa "tỉnh" kịp ngay lần đầu).

**Đã test lại cho đúng nghĩa** (lần trước chỉ xác nhận bằng cách TỰ TAY ép hiện
qua PowerShell, không phải tool tự làm được): dọn sạch mọi tiến trình
`pythonw.exe`/hộp thoại cũ đang treo (một số bị "kẹt" vô hình từ nhiều lượt bấm
thử trước đó, có một tiến trình giữ khoá `.dang-mo.lock` dù cửa sổ đã đóng —
xoá khoá, tắt hết), rồi bật lại một bản sạch và THEO DÕI bằng `EnumWindows` từ
ngay tiến trình Python đang mở nó, KHÔNG đụng tay ép gì thêm: cửa sổ tự
`vis=True` ngay khi vừa xuất hiện (~9 giây sau khi bấm), không cần ai ép từ
bên ngoài. Đây mới là bằng chứng bản vá thật sự có tác dụng.

**Nếu còn gặp lại:** Ngắt rồi nối lại phiên RDP thường ép Windows vẽ lại toàn
bộ cửa sổ đang treo — thử trước khi nghi mã có lỗi. Nếu tool báo "đang mở rồi"
mà bấm "Tắt bản cũ, mở bản này" không hết, kiểm tra `.dang-mo.lock` cạnh tool:
tiến trình cũ có thể đã đóng cửa sổ nhưng chưa thoát hẳn (một luồng nền của
gói tự động hoá trình duyệt — `trio` — từng thấy giữ tiến trình sống sau khi
cửa sổ đã đóng, xem `py-spy dump --pid <pid>` để soi luồng nào còn chạy).

**Tệp đã sửa:** `shopapi_studio_qt.py` (thay `raise_()/activateWindow()` bằng
`_ep_hien_that_su()` dùng `ctypes` thẳng).

**Xác nhận cuối:** Chủ dự án tự nhấp đúp `CHAY-GON.vbs`, xác nhận **mở được**.
Bốn lỗi trên (thiếu `core/secrets.py`, crash `reconfigure`, cửa sổ không hiện)
coi như xong.

## 2026-09-19 — Bớt tab cho đúng việc VPS này làm (đơ lúc mở + tính năng thừa)

**Vì sao sửa:** Sau khi mở được, chủ dự án góp ý hai điều: (1) giao diện đơ lúc
mở — đo được nguyên nhân là `_dung_cac_trang()` dựng HẾT 13 tab ngay lúc khởi
động, kể cả tab không ai bấm tới; (2) *"tính năng nhiều quá trên máy này đâu
cần nhiều thế"* — máy này chỉ tự chạy kênh 100% (nghiên cứu → chọn nguồn →
sản xuất → đăng → trả lời bình luận), không ai ngồi viết kịch bản/đọc voice/
dựng video tay ở đây.

**Đã làm:** Thêm `core.che_do_vps.loc_trang()` — khi có `vps.json` (chế độ
VPS), lọc `TRANG_SAN_PHAM` xuống còn đúng 6 tab khớp việc máy đang làm:
`trung_tam, chrome-sach (VPS), phan-tich (Phân tích & Nghiên cứu), auto (Video
sản xuất tự động), quan-ly-kenh, wallet`. Bỏ hẳn nhóm LÀM VIDEO (viết kịch bản,
voice, phụ đề, prompt visuals, tạo ảnh/video, edit — 6 tab) và "Skill miễn
phí". Máy KHÔNG có `vps.json` (bản khách thường) thì `loc_trang` trả nguyên
danh sách 13 tab, không đổi gì — chỉ VPS mới bị bớt.

Nối vào `CuaSoChinh.__init__` (`ui_qt/app.py`) ở đúng chỗ dựng `self._nav` —
cả thanh bên (`ThanhBen`) lẫn `_dung_cac_trang()` đều đọc từ `self._nav`, nên
bớt tab ở đây tự động bớt luôn phần dựng widget lúc khởi động (đúng chỗ gây
đơ), không cần sửa hai nơi. Tiêu đề nhóm ("LÀM VIDEO", "CÔNG CỤ YTB") gắn theo
khoá tab đầu nhóm nên tự biến mất theo, không để lại dòng trỏ vào khoảng trống
(cơ chế có sẵn, không phải sửa thêm).

**Đã test:** Kiểm bằng script độc lập (không dựng Qt) — máy thường: `loc_trang`
trả nguyên 13 tab; giả `vps.json`: còn đúng 6 khoá `trung_tam, chrome-sach,
phan-tich, auto, quan-ly-kenh, wallet`, đúng thứ tự cũ. `python -m pytest tests/
-q -k "trung_tam or che_do_vps or sidebar or thanh_ben or nav"`: 77 passed.
Chưa đo lại thời gian mở tool thực tế sau khi bớt tab (cần chủ dự án tự đóng
mở lại tool — bản đang chạy trong RAM vẫn là bản CŨ, 13 tab).

**Tệp đã sửa:** `core/che_do_vps.py` (thêm `KHOA_TRANG_VPS` + `loc_trang`),
`ui_qt/app.py` (gọi `loc_trang` khi dựng `self._nav`).

## 2026-09-21 — Dựng 3 kênh em + bịt các lỗ khiến máy "chết im lặng"

**Vì sao sửa:** Chủ dự án muốn một VPS chạy 4 kênh YouTube tâm lý Nhật tự động
100% trong nhiều năm. Khảo sát máy thật lúc 17:47 tìm ra bốn thứ chặn cứng mục
tiêu ấy, không cái nào nằm trong logic sản xuất:

1. **Trạm 8765 chỉ sống trong tiến trình Qt.** Grep toàn kho: `Tram(...)` chỉ
   được dựng ở `ui_qt/trang_chi_so_ytb.py`. Mà `vm/nguon_tool.py` lấy kế hoạch
   đăng DUY NHẤT qua `GET /ke-hoach`. Đóng cửa sổ là video sản xuất xong nằm
   chết trong thư mục — không lỗi, không cảnh báo, không bao giờ lên sóng.
   Đúng trạng thái máy lúc khảo sát: không ai nghe 8765, `agent.log` đầy
   `WinError 10061`.
2. **Hai bộ giám sát giết lẫn nhau.** `core/giam_sat_vm.py` (trong tool) và
   `vm/giao_dien.py` cùng nuôi ba con của `vm/`, cùng dùng `taskkill /F /T`.
   Agent mới thấy cổng khoá 8767 bị giữ thì giết bản cũ — kèm CẢ CÂY CON, tức
   Chrome của kênh. Đo được: 278 dòng "dọn agent cũ" nhưng chỉ 14 lần khởi
   động thật, các lần dọn đi theo CẶP cách nhau 8–9 giây, kèm 238 dòng "Chrome
   đang tắt — đã mở lại". Thư mục Crashpad RỖNG và Event Log không có
   Application Error nào cho `chrome.exe` — Chrome không tự hỏng, nó BỊ GIẾT.
3. **Không có kênh báo động nào ra khỏi máy**, và sổ sách (`agent.log`,
   `trang-thai.json`, `replied/*.txt`) phình vô hạn.
4. **`vm/giao_dien.py` tự cập nhật LÙI được.** Dòng 799 so `moi != doc_phien_ban()`
   — KHÁC chứ không phải MỚI HƠN. VERSION trên kho cũ hơn cũng bật cờ, rồi
   `lam_moi()` tự gọi `cap_nhat()` không hỏi ai: giết ba tiến trình con rồi
   giải nén đè. Máy này mang nhiều bản vá chưa từng có trên GitHub.

**Đã làm:**
- `tram_nen.py` + `core/tram_nen.py` + `core/canh_tram.py`: trạm chạy được
  KHÔNG cần Qt, bắt tay nhường cổng hai chiều với cửa sổ tool (gói dò UDP +
  tệp cờ `xin-nhuong`), chó giữ nhà hỏi cả UDP lẫn `GET /ke-hoach`.
  `core/lich_tu_chay.py` thêm `dang_ky_canh_tram`.
- `vm/agent.py::mot_minh`: thêm `CHONG_GIANH_CHO_GIAY = 120` — vừa thay chỗ
  xong thì bản kế tiếp THOÁT thay vì giành lại. Cắt vòng lặp ở chỗ rẻ nhất,
  giữ nguyên nết "nhấp đúp thì bản mới thay chỗ" cho người dùng thật.
- `core/bao_dong.py` (mới): bắn cảnh báo ra Telegram/webhook, chống spam
  1 giờ/loại, đọc `bao-dong.json`. Đi qua `core/mang_an_toan.dang_json` (thêm
  mới) chứ không `urlopen` trần — `tests/test_mang_an_toan.py` cấm, và thân
  yêu cầu ở đây mang khoá bot.
- `vm/agent.py::ghi` xoay vòng ở 5 MB giữ 3 bản; `trang-thai.json` dọn khoá
  theo ngày quá 60 ngày; `replied/<kênh>.txt` giữ 5.000 id gần nhất THEO THỨ
  TỰ THỜI GIAN (sort chữ cái sẽ bỏ nhầm id mới → trả lời trùng).
- Van đĩa: `core/tu_chay.py` kiểm dung lượng trước khi mở video mới, nhận
  riêng ENOSPC/WinError 112, gọi `don_dep.don_khan()` (mới) dọn video ĐÃ ĐĂNG
  cũ nhất trước.
- Tắt cập nhật GitHub: `vm/giao_dien.py` cờ `CHO_PHEP_CAP_NHAT = False` chặn
  cả ba đường (dò định kỳ, tự áp dụng, nút bấm tay); `ui_qt/cap_nhat.py`
  thêm `_tat_tren_vps()` bám `vps.json` — bản gửi khách KHÔNG đổi.
- Làm lại khối A/B của `ui_qt/trang_trung_tam.py`: mỗi kênh một thẻ cạnh nhau,
  ba mức màu luôn kèm chữ, ổ đĩa đứng đầu. Bảng cũ giữ nguyên sau nút "Bảng".
- Dựng 3 kênh em qua `nhom_kenh.tao_kenh_trong_nhom`, nhóm `tam-ly-nhat`;
  TL4-T7 đổi `mau_cua_tool` → `kenh_rieng` (cập nhật không còn ghi đè được số
  đo tay), khai `nhom`/`tep`, bật `tu_don`. Tách bản sắc: mỗi kênh một bộ vẽ,
  màu chữ bìa, ảnh nhân vật, nhãn tiêu đề, `2d-hook.md`, `6-seo.md` riêng —
  `kiem_trung_lap` từ 6 cảnh báo xuống còn 1 (giọng đọc, chờ chủ dự án).

**Đã test:** Trạm nền 41 test; báo động + dọn sổ 31; van đĩa + dọn 78; giao
diện Trung tâm 22 (và `test_trang_trung_tam.py` cũ xanh trở lại). Chống giành
chỗ kiểm bằng bốn ca thật: chưa từng thay → giết 1; vừa thay xong → giết 0;
`--thay` → giết 1; mốc cũ hơn 120s → giết 1.

**Chạy thật trên máy này lúc 21:06–21:09:** chó giữ nhà phát hiện trạm chết và
bật `tram_nen.py` không cần cửa sổ (nghe 8765, `GET /ke-hoach` trả 200); bật tool thì
trạm nền NHƯỜNG cổng cho cửa sổ rồi tự thoát sạch; agent mới nối trạm, phục vụ
4 kênh, tải extension riêng từng kênh, chạy phiên TL1-T7. Số "dọn agent cũ"
đứng nguyên 278 và "đã mở lại" đứng nguyên 238 — **bug giết Chrome không tái
phát**. Lịch đã đặt: `ShopAPI-TuChay` 02:00, `ShopAPI-CanhTram` mỗi 5 phút,
`ShopAPI-TramLucDangNhap` lúc đăng nhập.

**Còn nợ:** `voice_id` 4 kênh vẫn trùng (cần mã giọng thật từ cổng giọng nói);
`bao-dong.json` chưa có nên báo động đang CÂM; `vm/tokens/` rỗng nên máy trả
lời bình luận chưa chạy cho kênh nào; `ui_qt/huong_dan.py` chưa tả cách xem
thẻ mới; `2d-hook.md` của TL2/TL3 dài 935/969 ký tự, hơn trần 900 mà
`test_viet_hook.py` áp cho TL4-T7 và khuôn.

**Lưu ý vận hành:** `may_dang.py` đăng bằng PyAutoGUI nhận diện ảnh — nó NHÌN
màn hình. Ngắt RDP kiểu thường làm Windows ngừng vẽ, PyAutoGUI chụp màn hình
đen và mọi thao tác đăng hỏng trong im lặng. Trước khi ngắt phải chuyển phiên
về console: `tscon <id> /dest:console`.

## 2026-09-22 — Ngày đầu ba kênh em chạy thật: sáu tầng lỗi, và bài học "một thay đổi một lần"

**Vì sao:** Lịch 02:00 chạy lần đầu cho TL1/TL2/TL3-T7 — cả ba chết ở khâu đầu
(`kich-ban`), 3 lần thử, "không lấy được lời thoại video tư liệu". Truy tới đâu lộ
tầng dưới tới đó, vì ba kênh chưa từng chạy thật một lần nào.

**Sáu tầng, theo thứ tự lộ ra (bằng chứng đo trên máy):**
1. Thiếu Visual C++ Redistributable → `ctranslate2.dll` có mà không nạp
   (`msvcp140.dll`, `vcruntime140*.dll` vắng). `aka.ms` chỉ IPv4, máy tắt IPv4 →
   cài qua PyPI (`pip install msvc-runtime`, `files.pythonhosted.org` có AAAA).
   Whisper nạp được, mô hình `models/faster-whisper-small` nạp từ đĩa OK.
2. YouTube chặn IP VPS với `yt-dlp`/`youtube-transcript-api` (`IpBlocked`,
   "IP belonging to a cloud provider"); cookie gỡ được cửa bot nhưng vẫn không có
   luồng tiếng; nâng yt-dlp không cứu. Trình duyệt kênh từ cùng IP vào bình
   thường → xây đường "extension hút bảng phụ đề" (`core/loi_thoai.py`,
   `/loi-thoai/can-lay` + `POST /loi-thoai`, `ytb_extension/loi-thoai.js`,
   `vm/agent.lay_loi_thoai`, kho `CHANNEL/_NHOM/<nhóm>/loi-thoai/`). Đường proxy
   (`core/mang_youtube.py`, `mang-youtube.json`) cũng đã có — chưa có proxy.
3. **Ba hồ sơ kênh mới chưa bao giờ nạp extension.** Chromium 143/151 phớt lờ
   `--load-extension` (launcher chuyển cờ tới nơi, Chrome bỏ); cờ
   `--disable-features=DisableLoadExtensionCommandLineSwitch` đo hai lần: vô
   tác dụng. TL4-T7 sống nhờ đăng ký "unpacked" bền cũ trỏ `vm	ien-ich` phẳng
   (bản 2.6.2). Đường sống: `Extensions.loadUnpacked` qua DevTools
   (`--remote-debugging-port=930x --remote-allow-origins=*
   --enable-unsafe-extension-debugging`), KHÔNG bền → nạp mỗi lần mở
   (`vm/agent.mo_chrome_kenh`). Có đăng ký bền thật thì đồng bộ mã vào đúng thư
   mục ấy thay vì nạp đôi (`dong_bo_tien_ich_ben`) — vết tạm của chính DevTools
   (trỏ thư mục per-kênh) KHÔNG được tính là bền (dính thật 11:48).
4. YouTube `replaceState` gỡ `&shopapi_lt=1` trước `document_idle` → script tưởng
   tab người xem, im lặng thoát. Sửa: background giữ `tabId` từ
   `tabs.onUpdated`, `lt-dau.js` cắm cờ `sessionStorage` ở `document_start`,
   content script hỏi `lt_hoi`; thêm `lt_log` để hết mù.
5. Khối "Bản chép lời" có HAI nút, nút đầu ẩn → chọn nút đang hiện.
6. Trang xem dựng chậm >12s vì extension đang cào 22 video rác của TL1 song song
   → nới 12→30s, cuộn tới mô tả, chờ 25s/video ở cả hai đầu, và dòng chẩn đoán
   DOM khi trượt. Extension 2.7.3. **Chưa xác nhận được bằng phiên sạch** — ba
   lần chạy đều trúng lúc trạm bị agent sửa mã làm chết (`name '_loc' is not
   defined`: trạm giữ module nạp giữa chừng).

**Việc khác trong ngày:** vòng chấm-sửa theo giữ chân thật bật cho TL1/2/3
(`so_vong_cham: 2` + `2g/2h` từ khuôn; TL4-T7 giữ 0 làm đối chứng với
`TL4-T7-v2` — đã lỡ bật rồi hoàn lại); nối bảng nhóm vào chọn nguồn
(`cong_diem_anh_em`, trần ½ cột cụm, không vượt ứng viên tự thắng, không ra
khỏi tệp); lọc video rác theo `ngay_bat_dau` (TL4 2026-08-22; kênh em
2026-09-21) cắm vào `bang-tom-tat`, `video_cua_kenh`, `da_co_video_thang`,
`bang_nhom`, `trung_tam`, extension; ảnh nhân vật + phong cách riêng ba kênh
theo ảnh chủ dự án chọn (`kiem_trung_lap` còn đúng dòng giọng đọc); tắt cào
Studio/trang chủ cho ba kênh mới (`may-ao.json`, chờ 1s) vì số liệu của chúng
là video cũ — chủ dự án tự xoá trên YouTube, `chi-so/` đã dời sang `.rac-*`.

**Lỗi của người điều phối, ghi để không lặp:** để nhiều agent sửa `core/` trong
lúc tool đang chạy thật — trạm nạp lười module giữa chừng, chết ba lần; bộ
test của một nhánh ghi 110 dòng kênh giả "K1" vào `vm/agent.log` thật (đã dọn,
test đã cô lập); tự bật vòng chấm-sửa lên TL4-T7 phá cặp đối chứng (hoàn lại);
đổ oan lần trạm chết cho `gom.py reconfigure` — `su-co.log` chỉ có mục cũ
19/09. `tests/test_nhan_ban_kenh.py::test_kenh_mau_ship_kem_tool_co_co_mau[TL4-T7]`
đỏ CÓ CHỦ ĐÍCH trên máy này (TL4-T7 là kênh riêng, không phải mẫu).

**Kiểm cuối ngày:** nạp dưới `pythonw` OK; 272 test của mọi nhánh hôm nay xanh;
trạm + agent sống; lịch 02:00 còn nguyên. Còn nợ: xác nhận đường lời thoại qua
trình duyệt bằng một phiên sạch; nút "tự đào content" trên GUI cho kênh mới;
cập nhật `cau-hinh.json` từ phía vm; `background.js` chưa qua `node --check`.

**Bổ sung 13:20 — vì sao tool chết 4 lần hôm nay:** nhật ký phiên Windows
(`TerminalServices-LocalSessionManager`) ghi **10:40:34 ĐĂNG NHẬP MỚI** (mọi thứ
trong phiên cũ chết theo — đó là lúc chủ dự án nói "máy reset") và **12:50:50
phiên bị một kết nối RDP khác chiếm** (mã 39) → tool chết ngay sau. Chó giữ
nhà `ShopAPI-CanhTram` ở chế độ "Interactive only" bị Windows từ chối chạy
(0x800710E0) lúc phiên chập chờn → trạm nằm chết. Đã đổi sang chạy bằng SYSTEM
(`dang_ky_canh_tram(..., du_chua_dang_nhap=True)`): trạm sống không cần phiên;
agent/trình duyệt/PyAutoGUI vẫn cần MỘT phiên RDP ổn định — rời máy thì ngắt
kết nối (không đăng xuất), và đừng nối từ hai thiết bị cùng lúc.

**Bổ sung 14:50 — ĐÃ THÔNG.** Bỏ hẳn cách bấm nút/đọc bảng: `loi-thoai.js` 2.7.4
đọc `ytInitialPlayerResponse.captions…captionTracks` ngay trong trang xem, chọn
tiếng Nhật (người làm > tự động), tải `baseUrl&fmt=json3` cùng phiên trình
duyệt kênh (IPv6), gom chữ; bấm-bảng chỉ còn dự phòng. Phiên TL1-T7 14:45–14:49:
**4 lấy được · 3 không có phụ đề · 1 chưa về** — bốn lời thoại tiếng Nhật thật
(9.725–30.000 ký tự) vào kho, gồm cả video 6lmI99cnR1o/lSZhocwA9J0 mà bốn lượt
bấm-bảng trước đó đều báo nhầm "không có". `i2EAnLd8Duo` (làm hỏng đêm 22/09)
thật sự không có phụ đề.

Proxy IPv4 chủ dự án mua (homeproxy.vn) **không dùng được từ VPS này**: bật
binding IPv4 chỉ nhận `192.168.88.104`, không gateway, không hàng xóm ARP — máy
không có đường IPv4 ra Internet; API proxy và các proxy đều là IPv4. Đã thử
gateway `.1`/`.254`: không ra. Van IPv4 đã tắt lại, cờ `van-ipv4.json` đã nhổ.

Thêm: `vm/may-ao.json` ba kênh em tắt cào Studio/trang chủ (chờ 1 giây) vì
chưa có video của tool; số liệu cũ đã cào dời sang `chi-so.rac-*`. Nhật ký
phiên Windows giải thích 4 lần tool chết: 10:40 đăng nhập RDP mới, 12:50 phiên
bị kết nối RDP khác chiếm; chó giữ nhà nay chạy bằng SYSTEM.

**Bổ sung 15:10 — lỗi cuối: kênh kế tiếp bị coi là "đã chạy".** 
dò 
Image Name                     PID Session Name        Session#    Mem Usage
========================= ======== ================ =========== ============
System Idle Process              0 Services                   0          8 K
System                           4 Services                   0        108 K
Registry                       104 Services                   0     66,172 K
smss.exe                       272 Services                   0      1,028 K
csrss.exe                      404 Services                   0      5,404 K
wininit.exe                    492 Services                   0      6,836 K
services.exe                   636 Services                   0     10,420 K
lsass.exe                      656 Services                   0     18,248 K
svchost.exe                    780 Services                   0      3,860 K
svchost.exe                    800 Services                   0     13,888 K
fontdrvhost.exe                820 Services                   0      3,728 K
svchost.exe                    916 Services                   0     14,100 K
svchost.exe                    972 Services                   0     13,704 K
svchost.exe                    328 Services                   0    178,252 K
svchost.exe                    700 Services                   0      6,760 K
svchost.exe                   1076 Services                   0     11,980 K
svchost.exe                   1148 Services                   0     17,696 K
svchost.exe                   1260 Services                   0      8,620 K
svchost.exe                   1288 Services                   0      8,908 K
svchost.exe                   1296 Services                   0     11,772 K
svchost.exe                   1304 Services                   0      8,196 K
svchost.exe                   1336 Services                   0      8,168 K
svchost.exe                   1388 Services                   0      6,356 K
svchost.exe                   1448 Services                   0     15,688 K
svchost.exe                   1468 Services                   0      8,752 K
svchost.exe                   1556 Services                   0     12,388 K
svchost.exe                   1612 Services                   0      8,764 K
svchost.exe                   1620 Services                   0      8,964 K
svchost.exe                   1652 Services                   0      3,952 K
svchost.exe                   1792 Services                   0      9,272 K
svchost.exe                   1828 Services                   0      6,340 K
svchost.exe                   1936 Services                   0     88,952 K
svchost.exe                   2032 Services                   0      4,388 K
svchost.exe                   1136 Services                   0      3,912 K
svchost.exe                   2096 Services                   0      7,104 K
svchost.exe                   2240 Services                   0      5,000 K
svchost.exe                   2332 Services                   0      3,148 K
svchost.exe                   2412 Services                   0      4,412 K
svchost.exe                   2464 Services                   0     23,212 K
svchost.exe                   2472 Services                   0      5,788 K
svchost.exe                   2520 Services                   0      1,556 K
vdservice.exe                 2540 Services                   0      1,420 K
svchost.exe                   2548 Services                   0      5,688 K
qemu-ga.exe                   2556 Services                   0      8,080 K
svchost.exe                   2568 Services                   0      7,516 K
svchost.exe                   2588 Services                   0     11,120 K
wlms.exe                      2608 Services                   0      3,224 K
svchost.exe                   2620 Services                   0     12,732 K
svchost.exe                   2644 Services                   0      8,532 K
svchost.exe                   2760 Services                   0     11,892 K
svchost.exe                   2924 Services                   0     12,136 K
svchost.exe                   3484 Services                   0      8,856 K
svchost.exe                   3596 Services                   0     13,436 K
svchost.exe                   3884 Services                   0     11,996 K
svchost.exe                   4160 Services                   0     10,196 K
msdtc.exe                     3244 Services                   0     10,600 K
svchost.exe                   3416 Services                   0     13,920 K
svchost.exe                   2132 Services                   0      8,464 K
svchost.exe                   2260 Services                   0     11,164 K
svchost.exe                   3252 Services                   0     13,252 K
csrss.exe                     4944 Console                    2      1,376 K
winlogon.exe                  4016 Console                    2      2,688 K
fontdrvhost.exe               1120 Console                    2        984 K
LogonUI.exe                    764 Console                    2     51,252 K
dwm.exe                       5748 Console                    2     23,168 K
vdagent.exe                   2072 Console                    2      3,020 K
svchost.exe                    608 Services                   0     10,472 K
svchost.exe                   2208 Services                   0     12,360 K
svchost.exe                   6644 Services                   0     10,832 K
svchost.exe                   3512 Services                   0     10,280 K
svchost.exe                   3756 Services                   0      6,852 K
svchost.exe                   5652 Services                   0      4,248 K
svchost.exe                   6820 Services                   0      6,444 K
svchost.exe                   6832 Services                   0      6,444 K
csrss.exe                     4460 RDP-Tcp#61                 7      5,860 K
winlogon.exe                  6444 RDP-Tcp#61                 7     12,052 K
fontdrvhost.exe               7260 RDP-Tcp#61                 7     10,976 K
dwm.exe                       7068 RDP-Tcp#61                 7    152,016 K
rdpclip.exe                   3116 RDP-Tcp#61                 7     14,052 K
sihost.exe                    7164 RDP-Tcp#61                 7     24,800 K
svchost.exe                   8908 RDP-Tcp#61                 7     13,060 K
svchost.exe                   8940 RDP-Tcp#61                 7     29,352 K
taskhostw.exe                 5660 RDP-Tcp#61                 7     26,684 K
explorer.exe                  8392 RDP-Tcp#61                 7    106,776 K
ShellExperienceHost.exe       3008 RDP-Tcp#61                 7     42,588 K
SearchUI.exe                  1720 RDP-Tcp#61                 7     56,232 K
RuntimeBroker.exe             7292 RDP-Tcp#61                 7     17,996 K
taskhostw.exe                 5676 RDP-Tcp#61                 7      2,376 K
RuntimeBroker.exe             7752 RDP-Tcp#61                 7     22,312 K
UniKeyNT.exe                  5896 RDP-Tcp#61                 7      8,964 K
dllhost.exe                   7728 RDP-Tcp#61                 7     11,824 K
RuntimeBroker.exe             8828 RDP-Tcp#61                 7     14,084 K
Code.exe                      6840 RDP-Tcp#61                 7     82,316 K
Code.exe                      3032 RDP-Tcp#61                 7     13,172 K
Code.exe                      4204 RDP-Tcp#61                 7     27,316 K
Code.exe                      1900 RDP-Tcp#61                 7     68,388 K
Code.exe                      2752 RDP-Tcp#61                 7    296,088 K
Code.exe                      4576 RDP-Tcp#61                 7    171,464 K
Code.exe                      5880 RDP-Tcp#61                 7     39,204 K
Code.exe                      3440 RDP-Tcp#61                 7     49,092 K
Code.exe                      6648 RDP-Tcp#61                 7    530,008 K
codex.exe                     2020 RDP-Tcp#61                 7     40,612 K
conhost.exe                   4140 RDP-Tcp#61                 7     10,744 K
Code.exe                      4364 RDP-Tcp#61                 7     36,348 K
conhost.exe                   9000 RDP-Tcp#61                 7      6,116 K
claude.exe                    3472 RDP-Tcp#61                 7    321,160 K
conhost.exe                   3628 RDP-Tcp#61                 7     11,596 K
powershell.exe                4804 RDP-Tcp#61                 7     44,516 K
pet.exe                       4648 RDP-Tcp#61                 7      4,916 K
conhost.exe                   5604 RDP-Tcp#61                 7     10,740 K
Code.exe                      3140 RDP-Tcp#61                 7    331,676 K
py.exe                        1384 RDP-Tcp#61                 7      5,988 K
conhost.exe                   7536 RDP-Tcp#61                 7     18,128 K
python.exe                    7304 RDP-Tcp#61                 7     59,696 K
Code.exe                      5064 RDP-Tcp#61                 7     74,544 K
Code.exe                       792 RDP-Tcp#61                 7    104,068 K
Code.exe                      1924 RDP-Tcp#61                 7     44,272 K
Code.exe                      5524 RDP-Tcp#61                 7     50,704 K
Code.exe                      5740 RDP-Tcp#61                 7     45,696 K
svchost.exe                   6692 RDP-Tcp#61                 7     17,936 K
WindowsInternal.Composabl      428 RDP-Tcp#61                 7     31,204 K
wscript.exe                   3540 RDP-Tcp#61                 7     18,432 K
pythonw.exe                   5184 RDP-Tcp#61                 7    704,952 K
python.exe                    6420 RDP-Tcp#61                 7     24,756 K
conhost.exe                   4276 RDP-Tcp#61                 7     10,860 K
TL2-T7.exe                    8760 RDP-Tcp#61                 7     11,316 K
chrome.exe                    8620 RDP-Tcp#61                 7    224,208 K
chrome.exe                    6896 RDP-Tcp#61                 7      7,136 K
chrome.exe                     536 RDP-Tcp#61                 7     41,184 K
chrome.exe                    8236 RDP-Tcp#61                 7     53,624 K
chrome.exe                    5128 RDP-Tcp#61                 7     19,816 K
chrome.exe                    6260 RDP-Tcp#61                 7     74,060 K
chrome.exe                     572 RDP-Tcp#61                 7    319,468 K
chrome.exe                    7700 RDP-Tcp#61                 7     86,536 K
TL2-T7.exe                    7452 RDP-Tcp#61                 7     11,528 K
chrome.exe                    8156 RDP-Tcp#61                 7    325,764 K
chrome.exe                    8724 RDP-Tcp#61                 7    274,644 K
TL2-T7.exe                    2128 RDP-Tcp#61                 7     11,456 K
chrome.exe                    3228 RDP-Tcp#61                 7     18,956 K
chrome.exe                    8640 RDP-Tcp#61                 7     24,040 K
svchost.exe                   3308 Services                   0      7,664 K
chrome.exe                    3972 RDP-Tcp#61                 7     31,952 K
python.exe                    8660 RDP-Tcp#61                 7     70,952 K
bash.exe                      5296 RDP-Tcp#61                 7      5,312 K
bash.exe                      8180 RDP-Tcp#61                 7      8,176 K
conhost.exe                    132 RDP-Tcp#61                 7     10,804 K
bash.exe                      1520 RDP-Tcp#61                 7      5,796 K
bash.exe                      1888 RDP-Tcp#61                 7      5,788 K
tasklist.exe                  7884 RDP-Tcp#61                 7      7,736 K
WmiPrvSE.exe                  8248 Services                   0      8,588 K cả tên chung `chrome.exe` — tên tiến trình con của CẢ BỐN bộ trình
duyệt. Chế độ phiên đóng kênh trước rồi mở kênh sau ngay, tiến trình cũ chưa chết
hẳn → kênh sau bị trả lời "đang chạy" → `mo_chrome_kenh` bỏ bước nạp mắt cào →
phiên rỗng. Đo: TL2-T7 mở 14:51:35 ngay sau TL1 vừa đóng, không có dòng "đã nạp",
"0 lấy được · 8 chưa về"; TL1 (14:45) và TL3 (14:59) mở lúc rảnh thì nạp được.
Sửa: launcher riêng của kênh (`<MÃ>.exe`) thì chỉ hỏi đúng tên nó. Chạy lại TL2
lúc 15:06: "đã nạp … vào TL2-T7", **1 lấy được**. 74 test liên quan xanh.
