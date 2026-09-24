# CÔNG THỨC ĐANG ĐÚC — TL4-T7 — bản 1, 09/09/2026 (sau V7, trước V9/V10)

> Mục đích: gom mọi thứ ĐÃ ĐO được từ V1–V8 thành quy tắc có số, có bằng chứng, có độ tin, có điều kiện bác bỏ —
> để khi V9/V10 có video thắng thì biết chính xác quy tắc nào được xác nhận và công thức khoá lại được phần nào.
> Quy tắc ở đây CHƯA phải luật sổ tay; luật sổ tay (CLAUDE.md) chỉ nhận quy tắc đã qua ≥ 2 lần xác nhận độc lập.
> Mỗi video mới PHẢI có phiếu thí nghiệm trong `thi-nghiem/` trước khi đăng, và điền hậu kiểm ở giờ 85.

## 0. Bảng học liệu — 8 video trên cùng một thước

| video | giờ đăng JP · ngày của kênh | nguồn (thẻ già kênh nguồn) | từ khoá máy đọc | vế gỡ tội | seed @13h | CTR đề xuất sóng 1 | AVD đề xuất | pool đúng ngách | trang chủ | đỉnh hiển thị | tuổi |
|---|---|---|---|---|---|---|---|---|---|---|---|
| V1 興味が持てない人の脳 | 00:45 · kênh mới | ひとり時間 0% | 脳科学 ✓ | 特殊な報酬回路 (yếu) | 427 | ~4% | 5:18 (31%) | **34%** | 21% lượt | 4.426 | — |
| V2 1人の時間を好む人 | 22:47 · N4 của V1 | 心理の栞 0% | 心理学 ✓ | メンタルが強い ✓ | 469 | ~2,4% | 4:52 (33%) | ? | 26% | 4.538 | — |
| V3 寂しくない人の脳 | 23:45 · N2 của V2 | ひとり時間 0% | 脳科学 ✓ | 最も成熟した脳 ✓ | 577 | **1,9%** | 4:36 (30%) | 15% | có, yếu (1.598 · 3,4%) | 24.281 | 100% ≥45 · 65+ 44% |
| V4 一人で旅行 | **13:45** · N3 của V3 (cược) | ひととき **47%** | 心理学 ✓ | 本当の強さ ✓ | **41** | (số bẩn) | 2:48 (23%) | — | — | 4.236 | — |
| V5 休日に外に出ない | **18:45** · N5 của V3 (all-in 9,3k) | カラクリ **34%** | 心理学 ✓ | 最も進化した脳 ✓ | **43** | 4–9% (mẫu 67–158) | 4:29 (30%) | — | — | 527 | — |
| V6 子供時代 | 23:30 · ngày nghỉ (971→262) | おやつ 15% | 心理学 ✓ | **✗** | 67 | 13% (mẫu 67) | 3:15 (22%) | — | — | 635 | — |
| **V7 5つのこと…知能** | **23:30 T7 · ngày nghỉ (262)** | おやつ 15%, nguồn +1.803/ngày | 脳科学 ✓ | **知能…特別 ✓** | **3.911** | **3,57%** | **5:04 (31%), 96% tương tác** | 15,5% (có cụm IQ) | **14.159 · 5,78%** | **39.472** | 65+ 10% · 35–44 13% |
| V8 友達が少ない | 22:51 T2 · **N3 của V7 (cược +12,6k)** | ズレ 0% | **✗** | **✗** | 1.058 | **2,05%** | 3:53 (29%) | **3,6%** | 34 imp | 2.451 | — |

Đọc bảng: 3 video chết ở seed (V4, V5, V8-trang-chủ) đều đăng vào ngày kênh đang CƯỢC cho video khác hoặc đăng ban ngày.
2 video chết ở cổng bấm (V3, V8) đều CTR đề xuất ≤ 2%. Video duy nhất mở trang chủ (V7) là video duy nhất có ĐỦ:
ngày nghỉ + đêm muộn + từ khoá + gỡ tội trí tuệ + CTR đề xuất ≥ 3,5% + AVD đề xuất ≥ 5:00.

## 1. Cơ chế phân phối của kênh này (đã đo, mô tả bằng 4 pha)

```
đăng 23:00–00:00 JP ──► cửa THỬ giờ 12–13 (trưa JP) ──► ĐO ngày 2 (luôn tụt) ──► CƯỢC ngày 3–5 (trang chủ, tối JP 19:30–03:00)
        │                       │                                                   │
   ngày kênh đang cược?    CTR đề xuất < 2,5% → ngắt ở giờ 20–29            CTR giữ ≥ 3,5% → gia hạn từng tối (V7: 3 đợt)
   → seed ~40–70, hụt thử   CTR ≥ 3,5% & AVD đề xuất ≥ 4:30 → sang cược       CTR ~2% trên mẫu lớn → ngắt một nhát (V3 N6)
```

Điểm mới so với lý thuyết 03/09 ("ngắt một nhát"): khi CTR giữ được, cược KHÔNG bị ngắt mà gia hạn từng tối (V7 h44–52,
h69–75, tắt dần trưa T4). Tức máy chấm lại mỗi ngày trên mẫu mới; "ngắt" chỉ xảy ra khi thua.

## 2. Quy tắc — mỗi quy tắc: bằng chứng · n · độ tin · điều bác bỏ

Độ tin: **cao** = ≥3 ca cùng chiều, không ca ngược · **khá** = 2–3 ca, 0–1 ca ngược có lý do · **trung bình** = 1–2 ca ·
**thấp** = 1 ca hoặc suy diễn · **chưa thử** = chưa có video nào đo.

| # | quy tắc | bằng chứng | n | độ tin | bị bác bỏ nếu |
|---|---|---|---|---|---|
| R1 | Tiêu đề phải mang từ khoá ngách máy đọc được (脳科学 / 【心理学】). Không có → máy xếp nhầm ngách, CTR đề xuất ≤ 2%, chết ở giờ 29 | V8 (không) pool 3,6% · V1/V3/V7 (có) pool 15–34% | 1 âm / 3 dương | trung bình | V9 hoặc V10 có từ khoá mà pool < 10% |
| R2 | Phải có vế gỡ tội; gỡ tội bằng TRÍ TUỆ (知能/賢い/IQ) là vế mạnh nhất với tệp máy đang phát | V7 vs V6 (cùng nguồn おやつ, khác vế: 3.911 vs 67 seed); trong pool V7 người từ tiêu đề IQ xem 14–16 phút, từ 孤独 bỏ 0:24 | 2 | trung bình | V9 (知的) chết ở cổng bấm dù pool đúng |
| R3 | Đăng 23:00–00:00 JP để cửa thử rơi trưa JP; đăng ban ngày/chập tối hụt cửa | V1/V2/V3/V6/V7 đêm → được thử; V4 13:45 / V5 18:45 → 41–43 | 5/2 | khá | một video đêm muộn seed < 100 trên ngày nghỉ (V6 là ca ngược — nhưng V6 thiếu R2) |
| R4 | Không đăng vào ngày kênh đang CƯỢC (tổng hiển thị kênh > 5.000/ngày) — video mới không có suất thử/suất trang chủ | V4 (N3 V3) 41 · V5 (N5 V3) 43 · V8 (N3 V7) trang chủ 34 imp | 3 | khá | V10 đăng đúng ngày V9 cược mà vẫn mở trang chủ |
| R5 | Điểm rẽ sống/chết = CTR đề xuất sóng 1 ≥ 3,5% VÀ AVD đề xuất ≥ 4:30 với ≥ 90% lượt tương tác → trang chủ mở ở giờ 44–52 | V7 đạt → mở 14k; V3 1,9% → mở yếu 1,6k; V8 2,05% → không mở | 1 dương / 2 âm | trung bình | video đạt cả hai mà trang chủ không mở tới giờ 60 |
| R6 | Seed lớn không cứu được cổng bấm; seed nhỏ không giết video đêm muộn | V8 seed 1.058 chết; V3 seed 577 lên 24k | 2 | khá | — |
| R7 | Kênh nguồn gắn thẻ già ≥ 30% → tệp già + số bẩn; tránh | V4 (47%) 209 người xem lặp; V5 (34%) | 2 | trung bình | — |
| R8 | Góc 孤独/寂しい kéo 65+ (V3 44%); góc 知能 kéo trẻ hơn (V7 65+ 10%, có 35–44) | V3 vs V7 | 2 | thấp | V9 (知的) ra 65+ > 30% |
| R9 | Đọc số bằng lượt thật/người (≤ 1,5 = sạch); lượt trang chủ 74% không tương tác nên lượt công khai/người lên 2,8–3,7 mà không phải xem lặp | V7 1,1 thật/người vs 2,8–3,7 công khai; V4 bẩn thật (3,5 thật/người) | 2 | khá | — |
| R10 | Tỷ lệ đăng ký là nút thắt YPP; mời đăng ký ở cuối bài (V7 16:19/16:31) chỉ tới ~15% người | V7 0,29%/lượt, 0,75%/lượt thật; cần 1,2% | 1 | chưa thử (đòn bẩy) | V9 mời ở ~1:00–1:30 mà sub/lượt thật vẫn < 0,8% |
| R11 | Chọn đề theo trend: tỷ lệ thắng của chủ đề (≥×3 mức thường kênh) + kênh nhỏ đã thắng + chưa đông người chép; chép sau khi sóng đã đông thì xịt (家: 3 kênh chép sau + V5 đều xịt) | 家 · 独り言 (4 bản chép) · 興味がない 47% | suy diễn từ sổ | chưa thử | V10 (trend 47%, sớm) chết ở cổng bấm dù R1–R5 đạt |
| R12 | Chưa qua giờ 52 chưa kết luận; đỉnh đời video ở ngày 3–5; dự báo ở giờ 19 sai (V7) | V7, V3 | 2 | khá | — |
| R13 | Video thắng kéo video cũ: V7 nằm trong pool của V1/V3/V5/V6/V8, V3 +1,8k hiển thị sau khi V7 nổ; màn hình kết thúc từ video thắng là seed miễn phí | V7→V3; V2→V1 (03/09) | 2 | khá | — |
| R14 | Nguồn đang được máy phát (đà +/ngày cao) giúp seed? V7 nguồn +1.803/ngày seed 3.911; V4 nguồn +8.114/ngày seed 41 (nhưng V4 dính R3+R4) | 1/1 | thấp | V9 (nguồn nguội, tháng 7) seed ≥ 1.000 → đà nguồn KHÔNG cần; V10 (nguồn +7k/ngày) seed ≥ 2× V9 → có tác dụng |

## 3. Bài học V1–V8 — những dự báo SAI và vì sao (để không lặp)

1. **04/09 "kênh sụp 10 lần, có thể bị hạ điểm vĩnh viễn"** — sai. V7 seed 3.911 hai ngày sau. Cái sụp là NGÀY CƯỢC của V3
   nuốt suất của V4/V5, rồi hai ngày nghỉ. Kênh không bị hạ điểm; V6 chết vì thiếu R2, không phải vì kênh.
2. **04/09 "trùng tệp 一人 nên máy không phát nữa"** — sai. V7 vẫn 一人 và nổ nhất kênh. Cái khác là VẾ GỠ TỘI (知能).
3. **06/09 19h "V7 về 1.000–1.500 lượt"** — sai 4–6 lần. Mô hình lúc đó chỉ có sóng đề xuất, chưa biết trang chủ mở giờ 44.
4. **06/09 "V8 đổi tệp bằng nguồn 0% thẻ già + tiêu đề ngôi thứ nhất"** — chết vì bỏ R1 (không từ khoá) và R4 (đăng ngày V7
   cược). Đổi tệp mà bỏ cơ chế phân phối thì không có ai để đổi.
5. **05/09 "đo thoát tệp 55+ bằng 25–34 ≥ 18%"** — thước không đo được ở quy mô nhỏ (18% là một lô 1.400 lượt), và bị pha
   loãng ngay khi có lượt thật. Thước tuổi chỉ đọc trên bảng RIÊNG của video ≥ 3.000 lượt.
6. **Sổ đối thủ**: ngày đăng video cũ chỉ đúng tháng; cột đà 0 = chưa đo lại; doi-thu.csv sub có dòng sai 10 lần
   (ココロの窓 2.180 vs 218). Trước khi chọn nguồn, tra yt-dlp (miễn phí) để lấy tag/mô tả/sub thật.

## 4. Công thức chọn content — bản đang dùng (mỗi bước có số)

1. Tệp trước: tiêu đề thuộc tệp "ngược số đông" theo PHÂN XỬ của tuyen.csv (việc số đông làm mà mình không + xin được gỡ tội).
2. Trend: chủ đề có tỷ lệ thắng ≥ 30% toàn sổ, có kênh < 10k sub thắng, số kênh chép trong 21 ngày ≤ 3.
3. Nguồn: kênh nguồn thẻ già < 25%; không 雑学 trong tên kênh; tra yt-dlp: tag/mô tả không đóng khung tiền/tuổi; dài 12–20 phút.
4. Tiêu đề của mình: từ khoá máy đọc (脳科学 hoặc 【心理学】) + vế gỡ tội (ưu tiên trí tuệ) + hành vi bị chê; bìa 2 dòng.
5. Lịch: 23:00–00:00 JP; ngày kênh < 1.500 hiển thị (ngày nghỉ); không đăng khi video khác đang cược (> 5.000/ngày).
6. Seed miễn phí: màn hình kết thúc + thẻ từ video đang thắng; mời đăng ký ở ~1:00–1:30 và cuối.
7. Đọc số: giờ 13 (seed) · giờ 20 (CTR đề xuất) · giờ 52 (trang chủ) · giờ 85 (pool + tuổi) · 7 ngày (sub/lượt thật).

## 5. Khi V9/V10 có kết quả — cách đúc

- Mỗi phiếu thí nghiệm ghi trước: dự đoán bằng số ở từng mốc, và quy tắc nào được XÁC NHẬN / BÁC BỎ ở từng kết cục.
- Sau giờ 85: điền hậu kiểm vào phiếu → cập nhật cột "n" và "độ tin" ở bảng mục 2 → quy tắc lên "cao" thì chuyển vào
  CLAUDE.md của kênh (luật), quy tắc bị bác bỏ thì gạch và ghi lý do, không xoá.
- Công thức chỉ được gọi là "đúc xong" khi R1–R5 cùng lên "cao", tức có ≥ 3 video mở trang chủ theo cùng một đường.
