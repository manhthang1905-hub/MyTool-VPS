# TL4-T7 — 心理のとまり木 — SỔ TAY VẬN HÀNH & PHÂN TÍCH

> File này là LUẬT cho mọi phiên AI làm việc trong thư mục này. Đọc hết trước khi phân tích
> bất kỳ chỉ số nào hoặc đề xuất bất kỳ thay đổi content nào. Lịch sử kênh + trạng thái
> hiện tại nằm ở `NHAT-KY-KENH.md` — PHẢI đọc file đó trước khi kết luận điều gì về kênh.

## Kênh này là gì

- Kênh YouTube **tâm lý học tiếng Nhật** cho khán giả Nhật Bản, dạng remake: viết lại
  kịch bản từ video đối thủ đã thắng (xem `kenh.yaml`, `che_do_tieu_de: nguyen_goc`).
- Mục tiêu: **bật YPP trong ~1 tháng** (1.000 subs + 4.000h xem). Ca đối chứng: kênh
  Eva Vital bật YPP với 8 video/28 ngày, video ăn nhất 88k impressions / 6,7% CTR.
- Bối cảnh chủ kênh: từng fail 100 kênh vì đoán mò không số liệu. Kênh này làm khác:
  **mọi quyết định phải bám số đo được**. Không đoán, không mẹo trôi nổi.

## Công thức 3 cổng — khung phân tích DUY NHẤT

Mỗi view đi qua 3 cổng theo thứ tự: `View = Impressions × CTR × AVD`.
Nghẽn cổng nào sửa cổng đó — chẩn sai cổng là công cốc.

| Cổng | Chỉ số | Chết | Thấp | Ổn | Tốt |
|---|---|---|---|---|---|
| 1 Phân phối | Impressions | < 1.500 | — | 20.000 | 80.000 |
| 2 Bấm | CTR tổng | — | < 3,5% | 5% | 6,5% |
| 2 Bấm | CTR nhánh đề xuất | — | < 4% | 4% | — |
| 3 Giữ chân | AVD (% độ dài) | — | < 25% | 35% | — |

Ngưỡng phụ (đo phân loại kênh — quan trọng hơn view ở giai đoạn này):
- **% view từ Nhật ≥ 80%** mới là đúng thị trường (Analytics → vị trí địa lý)
- **Pool đề xuất ≥ 50% impressions từ video đúng ngách** (bảng "được xếp cạnh video nào")
- Rơi > 45 điểm trong 30 giây đầu = cảnh báo hook (nhưng xem luật 3 bên dưới)
- Tự xem/nội bộ > 25% = số bẩn

Nguồn ngưỡng: Analytics thật của 3 kênh đối chứng (Eva Vital 88k/6,7% bật YPP; 마음 심리학
20k/8,8%; Psyche Secrets 729/3,4% chết). Bản máy đọc: `d:\New folder\topytb\chi-so\nganh\kenh1.json`.

## 9 LUẬT SẮT khi phân tích — vi phạm là phân tích sai

1. **Thiếu 1 trong 3 số của 3 cổng thì KHÔNG chẩn đoán.** Ghi "chưa đủ số, chờ mốc sau".
2. **Số tổng luôn là số ảo.** CTR/AVD phải tách theo nguồn (đề xuất / trang chủ / tìm kiếm
   / trang kênh). Ví dụ thật: video 1 CTR tổng 3,1% nhưng CTR thật ở đề xuất chỉ 2,0% —
   bị trang kênh (7 imp, 100%) và tìm kiếm (10 imp, 40%) kéo lên.
3. **Pool đề xuất sai ngách → CẤM kết luận content/thumbnail.** CTR và retention lúc đó
   đo trên khán giả nhầm. Chẩn đoán duy nhất được phép: "nút thắt = phân loại".
4. **Luật 30 giờ:** video phẳng dưới 30 tiếng chưa được gọi là chết. Máy thử theo đợt;
   đợt quét trang chủ đầu tiên của kênh này luôn đến **giờ thứ 12–13** sau đăng
   (đo trên cả 5 video). Video 2 phẳng 16 tiếng rồi mới nổ là ca điển hình.
5. **views ÷ unique_viewers > 2 trong tuần đầu = số bẩn** (có người xem lặp), CTR/AVD của
   video đó mất quyền đọc. KHÔNG quy cho chủ kênh tự xem — đã xác nhận không phải.
6. **Tiêu đề giống/lấy nguyên của đối thủ KHÔNG phải lỗi** — đó là chiến lược remake có
   chủ đích (độ giống tiêu đề tăng xác suất được xếp cạnh video nguồn gấp 7 lần, nghiên
   cứu 2.911 video). Chỉ được flag: kịch bản không viết lại thật, hoặc từ khóa lạc ngách.
7. **So sánh phải cùng mốc giờ** (video 24h so với video khác tại 24h, không so với 138h).
   Dữ liệu từng giờ nằm trong `imp_theo_gio` của tong-quan.json.
8. **Dùng "lượt xem có tương tác" / views_that_uoc**, không dùng view công khai — video
   được đẩy trang chủ chỉ giữ ~54% lượt thật; YPP tính theo lượt thật.
9. **Không bi quan chưa kiểm chứng.** Mỗi phân tích phải kết bằng: nút thắt ở đâu + việc
   cụ thể làm được tiếp theo. Không lặp lại luận điệu "ngách bão hòa", "kênh mới không có
   cửa" — kênh này tồn tại để chứng minh bằng số.

## Dữ liệu nằm đâu, đọc thế nào

```
chi-so/bang-tom-tat.csv          ← BẮT ĐẦU TỪ ĐÂY: mỗi video 1 dòng, số mới nhất
chi-so/<video_id>/<mốc>h/
    tong-quan.json               ← số chính: imp, ctr, views, views_that_uoc, unique,
                                    avd, vung (JP%), traffic, imp_theo_gio (từng giờ)
    retention.xlsx               ← đường giữ chân từng thời điểm
    traffic-related.xlsx         ← pool đề xuất: video nguồn, imp/view từng nguồn
    raw/*.json                   ← gói thô, đừng đụng
chi-so/kenh/                     ← số cấp kênh theo ngày
```

Kho số liệu gốc đầy đủ hơn (nhiều mốc lịch sử): `d:\New folder\topytb\chi-so\du-lieu\k1\`.
Bộ chụp tự động (extension + trạm nhận) chạy từ dự án `d:\New folder\topytb\chi-so\`.

**Mẫu báo cáo chuẩn** khi phân tích 1 video (giữ nguyên format này):
bảng 3 cổng với mức ĐẠT/THẤP/SỚM → khán giả (JP%, views/unique, view thật ước) →
pool đề xuất (% đúng ngách imp/views, top nguồn) → retention (rơi 0–5%, tại 10/30%,
plateau, cuối, vách giữa video) → cảnh báo → kết luận nút thắt + việc tiếp theo.

## 4 quy tắc 60 giây đầu (rút từ đường số thật — chi tiết: DOC-CHI-SO-DE-SUA-CONTENT.md)

1. Mở bằng **vật thể nhìn được**, không mở bằng cảm giác trừu tượng.
2. Câu đoạn mở **10–20 ký tự**; cả bài trung bình ~29 ký tự/câu. Bài dài = nhiều câu,
   không phải câu dài.
3. Trước giây 60 phải có **một câu hỏi đặt thẳng cho người xem**.
4. Phút đầu **không giảng cơ chế**; mỗi đoạn giải thích kèm một cảnh đời thường ngay sau.

Độ dài chuẩn: 12–15 phút, nhắm 13 (`kenh.yaml: phut_muc_tieu`). Đã khóa bằng
`tests/test_kich_ban_giu_nguoi_xem.py` (20 bài test) trong kho tool.

## Từ khóa ngách (lọc content & chấm pool)

- **Mạnh (1 từ là đủ):** 心理 メンタル 脳科学 HSP 内向 自己肯定感 生きづらい 繊細さん
  考えすぎ 劣等感 承認欲求 アドラー ユング 認知 うつ 不安障害 愛着
- **Yếu (cần ≥2 từ):** 人間関係 孤独 感情 不安 ストレス 性格 幸せ 人生 疲れ 一人 1人
  ひとり 習慣 自分を 強い人 特徴 理由
- **Loại trừ (dính là loại):** 漫画 アニメ 速報 野球 サッカー ゲーム 反応集 スカッと
  2ch ゆっくり ドラマ BGM 音楽 料理 ホラー ニュース 政治 海外の反応 恋愛 雑学

Tuyến content đang chuyển đổi tốt nhất (đo trong pool): **"một mình / cô đơn"** — 19%
người bấm, gấp rưỡi các tuyến khác. Làm tiếp tuyến đang lên, đừng đổi ngang.

## Chọn content tiếp theo — thứ tự tiêu chí (chủ kênh chốt 04/09/2026)

Nguồn: `nghien-cuu/content.csv` (video đối thủ, có cột **Tuyến / Kênh**, **Đã làm**,
View, Tăng/ngày, Ngày đăng) + `nghien-cuu/tuyen.csv` (bản đồ tệp khán giả).

Lọc theo đúng thứ tự này, **không được đảo**:

1. **ĐÚNG TUYẾN** — `Tuyến / Kênh` = tuyến kênh đang đánh (TL4-T7:
   `nguoi-song-lech-nhip-so-dong`).
2. **ĐÚNG INSIGHT TỆP** — tiêu đề phải có ĐỦ HAI VẾ theo `tuyen.csv`:
   (a) nêu thứ **xã hội hay chê** về quan hệ với người khác (一人 · 友達が少ない ·
   SNSをしない · 外に出ない · 趣味がない · 部屋が汚い · 誰といても疲れる…) VÀ
   (b) **hứa gỡ tội** (実は · 特別 · 才能 · 天才 · 賢い · 強い · 幸せ · 正解 ·
   成熟 · 進化). Thiếu vế (b) thì chỉ là mô tả, không chạm insight
   *"Ai cũng thế, mình thì không. Chắc mình có vấn đề."*
3. **CHƯA LÀM — cả mã video LẪN CHỦ ĐỀ.** Không remake lại một MẶT đã làm dù
   kênh nguồn khác. Đã làm: 一人でいても寂しくない · 1人の時間を好む ·
   一人で旅行 · 休日に外に出ない · 一人でいるのが好きな人の子供時代.
4. **ĐÀ TĂNG / VIEW** — ưu tiên `Tăng/ngày` cao (chủ kênh 04/09: *"đà tăng trước
   view cũng được"*): đà cao = máy ĐANG phát đề tài đó, chen vào dòng kéo đang
   chảy. View tổng là thước phụ.
5. **MỚI** — `Ngày đăng` gần, dùng để phân định khi 3–4 ngang nhau.

Loại thẳng bất kể điểm số: tiêu đề dính từ trong danh sách loại trừ, và kênh
nguồn có 雑学 trong tên (pool 雑学 chính là nhóm lệch ngách trong pool video 1).
Độ dài nguồn nên 8–20 phút (kênh nhắm 12–15, tool nén/khai triển được).

## Công thức đang đúc + phiếu thí nghiệm (từ 09/09/2026)

- `nghien-cuu/CONG-THUC-DANG-DUC.md` — quy tắc R1–R14 rút từ V1–V8, mỗi quy tắc có bằng chứng, n, độ tin, điều bác bỏ.
  Quy tắc ở đó CHƯA phải luật; chỉ quy tắc lên độ tin "cao" (≥ 3 ca cùng chiều) mới được chuyển vào file này.
- **Mỗi video mới phải có `nghien-cuu/thi-nghiem/V<n>-phieu.md` TRƯỚC khi đăng**: giả thuyết, biến số đổi so với video
  thắng gần nhất, điều kiện đăng (checklist), dự đoán bằng số ở giờ 13/20/52/85/7 ngày, bảng kết cục → quy tắc nào được
  xác nhận/bác bỏ. Sau giờ 85 điền hậu kiểm rồi cập nhật cột n/độ tin trong CONG-THUC-DANG-DUC.md.
- Cơ chế phân phối đã đo (V7): đăng 23:00–00:00 JP vào ngày kênh < 1.500 hiển thị → cửa thử giờ 12–13 → CTR đề xuất
  ≥ 3,5% & AVD đề xuất ≥ 4:30 → trang chủ mở giờ 44–52 → cược gia hạn từng tối khi CTR giữ. **Chưa qua giờ 52 chưa kết
  luận video không nổ** (bổ sung luật 4). Không đăng video mới vào ngày kênh đang cược (> 5.000 hiển thị/ngày).
- Công cụ đo: `nghien-cuu/cong-cu/dem_pool.py` (pool đúng ngách + tuổi theo mốc), `trend.py` (đột biến ≤21 ngày trên sổ
  + trang chủ máy ảo), `chu_de_chi_tiet.py` (chi tiết theo chủ đề + hàng xóm pool). Chạy: `python <tệp>`, kết quả .txt cạnh script.

## Nghi thức làm việc

- Trước khi phân tích: đọc `NHAT-KY-KENH.md` (trạng thái + các hồ sơ đã đóng — đừng
  phân tích lại video đã đóng hồ sơ như thể mới).
- Sau khi phân tích: **ghi thêm mục mới vào NHAT-KY-KENH.md** (ngày, mốc, số chính,
  kết luận, việc đã quyết) — phiên sau còn nối tiếp được.
- 48h đầu sau đăng: không ai được mở trang xem video (kể cả để "kiểm tra") — chỉ Analytics.
- Đăng video: 18h giờ Nhật (16h VN), nhịp 2–3 ngày/video.
