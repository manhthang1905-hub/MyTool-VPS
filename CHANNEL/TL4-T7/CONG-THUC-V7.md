# CÔNG THỨC V7 — CÁCH CHỌN CONTENT (file sống)

Tên đặt theo video 7, video đầu tiên chọn bằng cách này. Mọi thứ ở đây vẫn là **giả thuyết đang được
kiểm**, chưa phải luật. File này để: (1) ghi luật đang dùng, (2) ghi bằng chứng, (3) đăng ký trước
cái sẽ kiểm ở video sau, (4) sửa luật khi số nói khác.

**Cách dùng file:**
- Trước khi chọn video mới → đọc mục 1, chạy mục 2, ghi lựa chọn + dự đoán vào mục 5.
- Khi video đủ 48 giờ → điền kết quả vào mục 3, chấm dự đoán ở mục 5.
- Luật nào bị số bác → sửa mục 1, ghi lý do vào mục 6. Không xoá lịch sử.

Nhật ký chi tiết từng ngày: `NHAT-KY-KENH.md`.

**Công cụ (từ 18/09/2026):** tab **Phân tích & Nghiên cứu → mục Công thức V7** (mục con cuối). **MỘT NÚT** ở
mục Đối thủ chạy luôn V7: đầu chuỗi bổ sung kênh còn thiếu từ pool, cuối chuỗi chấm + AI thẩm định (nếu có ví);
mở mục là tự chấm lại. Mục này chấm cả sổ đối thủ theo thang 100 điểm (`core/cong_thuc_v7.py`), ghi `nghien-cuu/cham-v7-<ngày>.csv|.md`,
có sổ dự đoán `nghien-cuu/so-chon-v7.csv` và nút "Kiểm 48 giờ". Thêm hai nút:
"Thẩm định bằng AI" (`core/cong_thuc_v7_ai.py` — AI xem cụm, dạng, tệp tuổi, trùng đề tài của 60 dòng đầu;
số đo không đổi; nhớ trong `nghien-cuu/v7-tham-dinh.json`) và "Bổ sung kênh còn thiếu" (kênh của video trong
pool chưa có trong sổ → hộp thư đối thủ, miễn phí). Trọng số, từ khoá cụm, ngưỡng nằm trong
`nghien-cuu/cong-thuc-v7.json` — **sửa luật ở mục 1 thì sửa cả tệp đó**. Script rời `cham_pool.py` là
bản nháp đầu, không còn dùng.

| Thang | Tối đa | Cách tính |
|---|---|---|
| Cụm đang thắng | 30 | cụm từ khoá của ứng viên có video thắng → 30 × (0,5 + 0,5 × sức thắng) |
| Bảng video đề xuất | 25 | có chính video: hệ số bấm × hệ số xem, 0,8 → 0 điểm, 1,4 → 25; chỉ có cụm: trần 15 |
| Nguồn nổ thật | 20 | gấp < 3 lần → 0, 8 lần → 15, ≥ 25 lần → 20; kênh nguồn < 1.500 view trung vị trừ 5 |
| Đang lên | 15 | Tăng/ngày > 0: 15 × (0,3 + 0,7 × thứ hạng) |
| Khuôn | 10 | 12–21 phút 5 (8–30 phút 2) · chân dung 5 · cách làm 0 |

Loại trước khi chấm: đã làm (kể cả `PROJECTS/AUTO/<kênh>-v2`) · kênh nguồn "bỏ" · nhắm người lớn tuổi ·
từ loại trừ (sau khi bỏ nhãn 【】) · dài < 8 hoặc > 40 phút. Xếp loại: ≥ 75 Làm ngay · 60–74 Nên làm · 45–59 Dự bị.

---

## 1. LUẬT ĐANG DÙNG — bản 3 (17/09/2026)

**Nguyên lý:** phục vụ đúng khán giả đang xem kênh. ~96% view đến từ trang chủ + cột đề xuất bên phải.
Cột đề xuất nhìn thấy được: Studio ghi lại từng video đã dẫn khách sang video mình.

Chọn qua 5 cửa, theo thứ tự:

| # | Cửa | Vì sao (bằng chứng ở mục 3–4) |
|---|---|---|
| 1 | **Cụm đang thắng trên chính kênh.** Video nào của kênh đang lên → làm tiếp đúng chủ đề đó. | V10 thắng → V11, V12 cùng cụm, giống nhau, cả hai thắng. Tín hiệu mạnh nhất. |
| 2 | **Có tín hiệu trong bảng đề xuất của video đang thắng.** Lọc đối thủ cùng chủ đề → chấm tỷ lệ bấm × thời lượng xem (mục 2). | V7, V10 có tín hiệu → thắng. V8, V9 không có → không nổ. |
| 3 | **Đúng insight tệp của kênh.** Loại tiêu đề nhắm người già (60代, 70代, 老後, 1950年代, 昭和, 定年, 孫…). | Bảng đề xuất phản ánh người ĐANG xem (61% trên 55 tuổi) → điểm cao dễ kéo về content người già. |
| 4 | **Cùng DẠNG với video thắng:** chân dung người ("người như thế này thì…", "người giàu không làm gì"), không phải "cách làm". | V7, V10, V11, V12 đều là chân dung. |
| 5 | **Nguồn nổ thật và còn đang lên:** ≥ 8× trung vị view kênh nguồn · kênh nguồn không quá yếu · 12–21 phút · Tăng/ngày > 0 · chưa làm. | V9: nguồn 277× trên kênh trung vị 429 → chết. Nguồn khoẻ là điều kiện cần, không đủ. |

**Tín hiệu từ tệp cũ không tính** (bảng đề xuất của V1–V6). Nó cho ra 猫 và cụm cha mẹ–con, đều bị loại.

**Nguồn remake thường KHÔNG phải chính dòng trong bảng đề xuất.** Bảng cho ĐỀ TÀI; sổ đối thủ cho
BẢN ĐỂ VIẾT LẠI (V7, V10 đều remake video khác cùng đề tài).

## 2. CÁCH CHẤM BẢNG ĐỀ XUẤT

Studio → video → Số liệu phân tích → Phạm vi tiếp cận → "Nội dung giúp người xem tìm thấy video này"
→ xuất bảng. Làm với **mọi video đang thắng**, không chỉ một.

Hai cột **là số của video MÌNH**, đo trên khách đến từ video kia:
- Tỷ lệ bấm = khi video mình hiện cạnh video đó, bao nhiêu % bấm sang mình.
- Thời lượng xem = khách từ video đó xem video mình bao lâu.

**Bản tay (cho khán giả):** dòng Tổng làm mốc; dòng vượt cả 2 mốc = điểm cao; dưới 10 lượt xem bỏ qua.

**Bản máy (`cham_pool.py`):** gộp mọi video trong `VIDEO_V7`.
```
Hệ số bấm B = (Σ lượt bấm thật + 10) / (Σ hiển thị × mốc bấm của video mình + 10)
Hệ số xem X = (Σ lượt xem × thời lượng / mốc xem của video mình + 10) / (Σ lượt xem + 10)
ĐIỂM = B × X      (> 1 = tốt hơn trung bình hàng xóm)
```
Mốc = dòng Tổng của từng video → video dài ngắn khác nhau vẫn so được. +10 chặn dòng 1–3 lượt xem.

**Bẫy dữ liệu:** cột CTR trong `traffic-related.xlsx` sai (gấp 16 lần), AVD rỗng → dùng
`traffic-related.csv` hoặc raw `*reach_viewers*join*.json`. Raw chỉ có top 50 dòng. Video dưới ~24 giờ
chưa có hiển thị theo dòng. yt-dlp mở từng video bị chặn; danh sách phẳng của kênh vẫn chạy — gọi ít.

## 3. BẰNG CHỨNG — mọi video

Thước đo chính: **lượt hiển thị ở mốc 48 giờ** (so cùng tuổi).

| Video | Mã | Chọn bằng | Cụm | Hiển thị @13h | **Hiển thị @48h** | Bấm @48h | Kết quả |
|---|---|---|---|---|---|---|---|
| V1–V6 | | trước công thức | một mình / linh tinh | — | 104 – 1.268 | | không nổ |
| **V7** | `32CA4WuHgVc` | bảng đề xuất V1: dòng IQ/EQ cao 11,1% | trí tuệ × một mình | 3.911 | **20.717** | 4,22% | **thắng** |
| V8 | `v4qSum0iCMg` | không theo bảng | một mình (bạn ít) | 1.015 | 2.604 | 2,07% | không nổ |
| V9 | `EpQf-4Il-rU` | không theo bảng, "sát V7" | một mình × trí tuệ | 306 | 3.502 | 2,77% | chậm |
| **V10** | `9nwb8g1tQK8` | trùng tín hiệu 物欲 15% (hạng 1) | vật chất / không phô trương | 1.859 | **29.921** | 6,03% | **thắng** |
| **V11** | `2cmZWXmtNRU` | cụm V10 + dòng trong bảng 9,3% | người giàu không phô trương | 5.120 | **158.896** | 5,56% | **thắng lớn** |
| **V12** | `dJMe6I5Ka4k` | cụm V10, nguồn khác cùng đề tài | người giàu không phô trương | 7.420 | _chờ_ | | seed cao nhất kênh |

Kênh 15/09 23:37 → 17/09 18:21: +44.236 view · +2.100 giờ · +191 đăng ký. 17/09: 3.823 giờ · 388 đăng ký.

## 4. ĐÃ BỊ BÁC BỎ

| Ngày | Giả thuyết | Số bác |
|---|---|---|
| 07/09 | Giờ đăng là yếu tố chính | V6 đăng đúng khung vẫn 823 hiển thị |
| 12/09 | Cỡ cụm trong bảng dự báo kết quả | V7 có cụm nhỏ nhất, kết quả to nhất |
| 12/09 | Cụm bấm cao nhất là cụm nên làm | Lúc chọn V7, cụm cao nhất là vật chất, không phải trí tuệ |
| 12/09 | Nguồn càng to càng thắng | V9 nguồn 277× vẫn chậm |
| 17/09 | Chấm điểm bảng đề xuất là đủ để chọn | Điểm cao kéo ra khỏi cụm đang thắng (精神年齢, 記憶力) và về content người già (1950年代生まれ) → thêm cửa 1, 3, 4 |
| 17/09 | Tín hiệu từ bảng của video cũ cũng tính | 猫 (bảng V3, 25%) không có ở video thắng nào, cụm một mình V8/V9 không nổ |

## 5. ĐĂNG KÝ TRƯỚC — chờ kiểm

Ngưỡng @48h: **thắng ≥ 20.000** (mốc V7) · **trung bình 6.000–20.000** · **trượt < 6.000** (mốc V8/V9).

| Video | Nguồn | Giả thuyết đang kiểm | Dự đoán | Kết quả | Đúng? |
|---|---|---|---|---|---|
| V12 | (cụm V10/V11) | Làm tiếp cụm đang thắng, dù giống video trước, vẫn thắng | ≥ 20.000 @48h | | |
| V13 | `GXNctv0oVSM` 【雑学】昔より物欲が減った人の心理 · カップ麺 (= kênh nguồn V12) · 127.000 · ×9,8 · +2.953/ngày · 19:53 | Cửa 1+3+4+5 đủ, cửa 2 mỏng (3 lượt xem) vẫn thắng | ≥ 20.000 @48h | | |
| V14 | `qxffZf5K2OY` 金持ちが死んでも「掃除」だけは自分でやる理由 · お金の心理 · 238.000 · ×56 · +1.476/ngày · 19:41 | Nguồn chưa có trong bảng, chỉ có đề tài gần (dọn nhà 18,18% ở V11) | ≥ 20.000 @48h | | |
| cụm | V10→V14 | **Cụm có bão hoà không?** Video thứ 5 cùng cụm | bấm @48h V13/V14 ≥ 4,5% (V11 5,56%) | | |

Đọc kết quả:
- V13 và V14 đều thắng → cửa 1 (cụm đang thắng) mạnh hơn cửa 2; bảng đề xuất chỉ cần để xếp hạng.
- V13 thắng, V14 trượt → cửa 2 là bắt buộc, không làm nguồn chưa có tín hiệu.
- Cả hai trượt, bấm tụt dưới 4% → cụm bão hoà; tìm cụm mới từ bảng đề xuất.

Dự bị: `dtMGDnZTdaE` 物欲が止まらない人へ (đúng cụm, nóng nhất +5.167/ngày; trượt cửa 4, kênh nguồn yếu,
điểm bảng 0,97) · `3ZiG9HjSyBA` 物を減らせる人 (×32, đứng yên) · `OIo-hAuWxXw` お金が残る人の習慣 (×10,8, đứng yên).

## 6. NHẬT KÝ SỬA CÔNG THỨC

| Ngày | Bản | Thay đổi | Lý do |
|---|---|---|---|
| 05/09 | 1 | Chọn đề tài từ dòng bấm cao trong bảng đề xuất | V1 bảng có dòng IQ/EQ 11,1% → V7 thắng |
| 12/09 | 2 | Tách: bảng cho ĐỀ TÀI, sổ đối thủ cho NGUỒN (≥ 8× trung vị kênh, 12–21 phút, còn nhích). Gom cụm, tách dòng cũ/mới | V10 thắng dù remake video khác dòng trong bảng; V9 nguồn to vẫn chậm |
| 18/09 | 4 | Tách tab riêng. AI thẩm định cụm/dạng/tệp/trùng đề tài thay từ khoá cho nhóm đầu bảng; trùng ≥ 70% với video đã đăng trừ 20 điểm; AI nói "nhắm người lớn tuổi" thì loại. Bổ sung kênh còn thiếu từ pool | Từ khoá sai ở dữ liệu thật: "脳", 【雑学】, không biết 「これ」を一人でやれる人は高IQ trùng V7 |
| 17/09 | 3 | Chấm bảng bằng tỷ lệ bấm × thời lượng xem, gộp mọi video đang thắng. Thêm cửa 1 (cụm đang thắng), cửa 3 (insight tệp), cửa 4 (dạng chân dung). Bỏ tín hiệu từ tệp cũ | Chủ kênh chỉ ra V11·V12 giống nhau vẫn thắng; điểm bảng kéo ra ngoài cụm và về tệp già |
