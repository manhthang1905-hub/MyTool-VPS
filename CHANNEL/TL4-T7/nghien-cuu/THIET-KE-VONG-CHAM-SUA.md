# Vòng CHẤM → SỬA → CHẤM LẠI — thiết kế 09/09/2026 (chưa làm, chờ chủ kênh gật)

Mục đích duy nhất: chọn ra kịch bản GIỮ CHÂN người xem, theo đúng tinh thần template TL4-T7: prompt đơn giản,
làm vài bản rồi chọn, không thêm luật. Chủ kênh 09/09: *"chấm sửa xong chấm lại vài lần cũng được"*.

## Vì sao vòng hiện tại chưa hội tụ về "hay"

Hiện có: viết 3 bản → chấm chọn 1 → hoàn thiện (mã vứt nếu dài > ×1,25) → viết 3 hook → chấm chọn → vá → ghép → nắn độ dài.
Ba lỗ, đều là lỗ ĐƯỜNG ỐNG, không phải lỗ lời nhắc:
1. Bản ghép cuối (hook mới + thân đã nắn) chưa bao giờ được chấm như MỘT bài. 0012: hook mới cắt mất nghịch lý + Savanna mà bộ chấm bảo giữ.
2. Bộ chấm chỉ nhìn kịch bản gốc; không biết người xem gốc THÍCH chỗ nào (248 bình luận), cũng không biết kênh mình ĐÃ ĐO
   được gì về giữ chân (V2 giữ 54% ở mốc 10%, V3 39%; V7 AVD rơi đúng lúc ý 1 vào ở 3:55).
3. Mã vứt bản sửa vì độ dài, trước khi bộ chấm kịp so — bản sửa đúng thứ bộ chấm chê mất trắng.

## Vòng mới

```
VIẾT 3 bản ─► CHẤM chọn 1 ─► VIẾT 3 hook ─► CHẤM chọn 1 ─► GHÉP
                                                            │
        ┌───────────────────────────────────────────────────┘
        ▼
  CHẤM TOÀN BÀI (bản đồ rớt) ─► VÁ đúng chỗ rớt lớn nhất ─► CHẤM SO (cũ / mới, cùng bản đồ rớt)
        ▲                                                          │ mới hơn → nhận; không hơn → giữ cũ
        └────────── lặp tối đa 3 vòng, dừng sớm khi "không còn chỗ kém gốc" hoặc 2 vòng liền không hơn ──┘
        ▼
  NẮN ĐỘ DÀI ─► CHẤM LẦN CUỐI: "so với gốc, mất gì đáng giữ? câu nào nghe hụt?" ─► vá nếu mất ─► giọng đọc
```

### Bộ chấm toàn bài — một lời nhắc, ba nguồn sự thật, một câu hỏi

Nguồn sự thật đưa vào (dữ liệu, không phải luật):
- **kịch bản gốc** (đã có);
- **30 bình luận nhiều like nhất của video gốc** (yt-dlp, miễn phí) — "người xem gốc khen chỗ nào, nhớ câu nào";
- **sự thật đã đo của chính kênh** (5–8 dòng, tool tự sinh từ chi-so): mốc rớt thật của video gần nhất, AVD, chỗ ý 1 vào và
  AVD rơi ở đó; lần trước bộ chấm đoán rớt ở đâu và thực tế rớt ở đâu.

Câu hỏi: *"Hình dung người xem gốc đang xem bản này. Vẽ bản đồ rớt: chia bài thành 6–8 đoạn, mỗi đoạn ước còn bao nhiêu %
người xem so với đoạn tương ứng của gốc, và vì sao. Chỗ nào KÉM gốc nhất? Bài này có còn giữ đủ những câu người xem gốc
nhớ không?"* Trả JSON: `ban_do_rot[]`, `cho_kem_nhat`, `mat_gi_cua_goc`, `giu_hay_sua`.

### Vá — sửa đúng MỘT chỗ, cả bài đi cùng

Vá nhận `cho_kem_nhat` + `mat_gi_cua_goc`, sửa tại chỗ, trả nguyên bài. Chặn duy nhất bằng mã: trùng chữ với bản trước
< 50% (viết lại từ đầu) thì bỏ. Không chặn độ dài — nắn độ dài đứng sau.

### Chấm so — cũ và mới cạnh nhau

Cùng lời nhắc chấm toàn bài, hai bản, hỏi thêm: "bản nào giữ người hơn, và bản mới có làm mất gì của bản cũ không".
Mới hơn thì nhận. Đây là cửa thật; rào chắn số là cửa giả.

### Dừng
- Bộ chấm trả `giu_hay_sua = "giữ"` (không còn chỗ kém gốc), hoặc
- 2 vòng liền bản mới không được chọn, hoặc
- 3 vòng.
Chi phí: mỗi vòng 3 lượt gọi (chấm, vá, so) → tối đa ~9 lượt + 1 lượt cuối. Mỗi vòng ghi `1-vong-N.txt` để chủ kênh soi.

## Cái làm vòng này HỌC được — nối với số thật

Sau khi video có đường giữ chân trong Studio (giờ 85+), tool ghi cạnh nhau: bản đồ rớt bộ chấm đã đoán ↔ đường rớt thật.
Chỗ đoán sai thành 2–3 dòng "sự thật đã đo" cho lần chấm sau. Không có khối này, vòng chấm-sửa chỉ hội tụ về gu của model;
có khối này, nó hội tụ về khán giả thật của kênh. Đây là điểm khác biệt duy nhất so với "chấm nhiều lần cho chắc".

## Việc phụ (ngoài chấm-sửa)
- Chữ bìa chép của đối thủ trùng > 80% với chữ bìa video trước của kênh → gọi AI viết chữ bìa (1 lượt). 0012 = V7.

## Không làm
- Không thêm luật cứng (vị trí ý 1, CTA, từ cấm) vào lời nhắc viết. Những thứ ấy đi vào "sự thật đã đo" cho bộ chấm tự
  cân — ví dụ: "V7: ý 1 vào ở 3:55, AVD 4:40, người xem rời đúng lúc danh sách bắt đầu".
