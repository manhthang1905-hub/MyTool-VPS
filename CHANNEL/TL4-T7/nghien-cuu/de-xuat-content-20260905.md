# Đề xuất content từ danh bạ đối thủ — 05/09/2026 21:05

> **SỬA 21:30.** Bảng top 20 dưới đây xếp ba video **đã làm** ở hạng 2, 10, 18 (2kdX8jBx6gY スポーツに
> 興味がない人の脳, WBWa4D9a1R0 一人でいても寂しくない人の脳, GJjYlTjNV8g 1人の時間を好む人ほどメンタルが強い)
> vì cột "Đã làm" chỉ đọc thư mục AUTO mà ba video ấy làm tay trước khi có AUTO. Anh đưa danh sách
> nguồn lúc 21:20. Hậu quả: câu *"chưa ai trong kênh khai thác không hứng thú thể thao"* ở mục 3 và 5
> là **sai** — #2 chính là video đó và anh đã làm. Đã sửa gốc: `nghien-cuu/da-lam.txt` + `core/da_lam.py`
> đọc thêm tệp ấy; bảng mới nằm ở `bao-cao-mot-nut.md` (chạy lại được bằng nút "Một nút").

Mục đích (anh nói 20:50): *"có 1 danh bạ đối thủ đúng chủ đề để từ đối thủ đó tìm ra content."*
Bản này đi đúng ba bước: **danh bạ sạch → bể content đúng tuyến → xếp hạng**. Không dùng AI, toàn
yt-dlp + luật cứng, nên mọi số ở đây tái lập được bằng `python -m pytest` và hai kịch bản trong thư mục tạm.

## 1. Danh bạ sau lượt cào trang chủ máy ảo

| | trước | sau |
|---|---|---|
| theo dõi | 19 | **24** (bỏ 4 cũ, thêm 9 mới) |
| bỏ | 0 | **44** |
| hộp thư chờ anh quyết | 35 | **4** (CORE LIFE STORY, ライフパッチ, 人生逆転の習慣, 大神さんの謎解き部屋 — self-help chung) |

Bỏ 4 kênh cũ: 大人の心理雑学 + カップ麺…雑学 (雑学), 暮らしを整える時間 (video 57 phút, view trung vị 341),
人の本音研究所 (view trung vị 582). **344 dòng content.csv (33%) đến từ 4 kênh này** — từ nay không quét,
và mọi xếp hạng phải lọc theo trạng thái danh bạ (bản này đã lọc).

Thêm 9: ズレは才能【心の仕組み】, こころノート心理学, 心理のコトノハ, 心理ラボ, ココロの魔法, The Door to Essence,
ちょっと元気になれる心理学, 癒しの心理学, 心のゆらぎ研究室. Thước chấm: cửa máy của tool (đúng tiếng · cùng khổ
15 phút · view trung vị ≥ 1.000) + cổng 雑学/要約/tóm sách + % tiêu đề gắn 50代/60代/老後 + % tiêu đề khớp
tuyến lệch nhịp. Bảng chấm đủ 72 kênh: `scratchpad/ung-vien-cham.csv`.

## 2. Bể content đúng tuyến (1.235 dòng → 178 ứng viên)

| bước lọc | số dòng |
|---|---|
| tổng content.csv | 1.235 |
| − kênh đã bỏ | 367 |
| − đã làm (đánh dấu) | 4 |
| − từ loại trừ trong tiêu đề | 21 |
| − tiêu đề lấy tuổi làm nhân vật chính | 70 |
| − không khớp tuyến lệch nhịp | 595 |
| **= ứng viên tuyến lệch nhịp** | **178** |

Khớp tuyến = nhãn `nguoi-song-lech-nhip-so-dong` có sẵn, HOẶC tiêu đề dính từ khoá tuyến (一人/ひとり/孤独/友達/
SNS/群れ/人付き合い/雑談/内向…). Xếp theo **vượt quy mô kênh** (view ÷ view trung vị của chính kênh — thước
"video này có gì khác thường"), rồi view tuyệt đối, cộng điểm nếu tiêu đề có khuôn gỡ tội (実は/本当は/才能/隠された).

## 3. Top 20 (GT = có khuôn gỡ tội · ✓ = đã làm)

| # | vượt | view | đăng | tiêu đề | kênh | mã |
|---|---|---|---|---|---|---|
| 1 | ×25+ | 742k | 24/05 | GT 【心理学】家から出たくない人が、実はすごい脳を持つ理由 | わたしの心理学 | aO4baOl4Yw8 |
| 2 | ×25+ | 587k | 14/04 | スポーツに興味がない人の脳が持っている"特殊な報酬回路"の正体 | ひとり時間の脳科学 | 2kdX8jBx6gY |
| 3 | ×25+ | 405k | 11/06 | GT 【心理学】スポーツ観戦に興味がない人だけが持っている特徴 | 心理学のおはなし | zb2KiFeC5l4 |
| 4 | ×25+ | 352k | 10/03 | GT 「一人でいても寂しくない人」に共通する、深い心理的特徴 | わかりやすい心理学 | C6zjnbCsLds |
| 5 | ×25+ | 263k | 11/03 | GT 高知能者が家を愛する科学的理由 | 心理学のおやつ | pEnLbFXIB88 |
| 6 | ×25+ | 248k | 04/05 | 【脳科学】片付けられない人の脳は"多くの情報"を処理している | ひとり時間の脳科学 | 3nDJ2_cdbBw |
| 7 | ×25+ | 171k | 01/04 | GT 休日に一歩も外に出ない人の脳が、実は「最も進化した脳」 ✓(V4 làm bản của 心と脳のカラクリ) | ひとり時間の脳科学 | i2ZqttlKeDw |
| 8 | ×25+ | 165k | 04/03 | GT 「一人が落ち着く人」に共通する心理的特徴とは | わかりやすい心理学 | Vweg7wsBrF8 |
| 9 | ×25+ | 157k | 19/03 | GT 「誰といても少し疲れる人」に共通する心理的特徴とは | わかりやすい心理学 | Vrz0Fp0mRDA |
| 10 | ×25+ | 122k | 18/04 | GT 一人でいても寂しくない人の脳が、実は「最も成熟した脳」である理由 | ひとり時間の脳科学 | WBWa4D9a1R0 |
| 11 | ×25+ | 138k | 25/05 | 一人で「この7つのこと」を実践しているなら、あなたの知能は本物です | お金の心理 | FbC6_SFR5GQ |
| 12 | ×21,7 | 325k | 27/05 | GT なぜか部屋が汚くなる人の「恐ろしい特徴」｜片付けられない人に隠された4つの才能 | ひととき心理学 | mE_PjAFv_TU |
| 13 | ×23,3 | 119k | 20/06 | GT なぜあなたは、一人で走りたくなるのか｜ソロライダーの心理学 | 夜の心理学 | 4PMu7uDCx_s |
| **14** | ×22,0 | 220k | 08/03 | GT **SNSをしない人の特徴 — V8 ĐÃ CHỌN** | 心理学のおやつ | H1fZAMiOwW0 |
| 15 | ×17,5 | 50k | 17/03 | GT 「静かな孤独を選べる人」に共通する心理的特徴とは | わかりやすい心理学 | weUIxPEZLLk |
| 16 | ×16,1 | 66k | 02/06 | GT あなたが次第に孤立していく衝撃的な理由。孤独なのではなく、格が上がった証拠です | お金の心理 | pOuiCHgOJK0 |
| 17 | ×14,5 | 217k | 02/07 | GT 【心理学】SNSをしない人に隠された「恐ろしい特徴」 (cùng đề với V8) | ひととき心理学 | chtJcARctJo |
| 18 | ×11,6 | 419k | 08/04 | GT 1人の時間を好む人ほど「メンタルが強い」驚きの理由 | 心理の栞 | GJjYlTjNV8g |
| 19 | ×15,7 | 33k | 28/08 | 一度冷めると絶対に縁を切る人の心理｜冷酷なのではなく、脳が出す生存信号？ | 幸福心理学 | kwDkU63wcbw |
| 20 | ×14,5 | 77k | 16/07 | GT 気を遣いすぎる人が最後に孤独になる本当の理由 | 一日ひとつの心理学 | UcPz7fw3y-I |

Đủ 178 dòng: `scratchpad/xep-hang-lech-nhip.csv`. **V8 (H1fZAMiOwW0) đứng 14/178 — top 8%, giữ nguyên.**

Chú ý #2, #3: "không hứng thú thể thao" nằm ngay trong từ khoá nhận biết của tuyến, hai video này ×25+
quy mô kênh (587k và 405k) — đúng insight "ai cũng thế, mình thì không" mà chưa video nào của kênh khai thác.
#1 (742k) và #7 (171k) cùng một ý "không ra khỏi nhà = não tốt"; V4 đã làm bản của 心と脳のカラクリ (P5Qp0OlJSgc)
và không nổ — nên #1/#7 chỉ đáng làm nếu đổi góc, không remake nguyên tiêu đề lần nữa.

## 4. Hai điều 9 kênh mới dạy được (quan trọng hơn số ứng viên chúng góp)

**9 kênh mới góp 27/178 ứng viên, hầu hết ×<2 quy mô kênh.** Cào trang chủ làm danh bạ dày hơn nhưng KHÔNG mở
thêm bể content đúng tuyến — vì chính feed quanh tài khoản kênh đã nghiêng 片付け/習慣/老後 (17/25 kênh mới
gắn thẻ tuổi già). Đây là số đo độc lập thứ ba nói cùng một điều với bảng tuổi Studio và với phân loại V3/V4.

**(a) ズレは才能【心の仕組み】 (@ZureTalent)** — 7,7k subs, view trung vị 10k, video 9:34, **cả kênh là một
tuyến lệch nhịp**: 友達が少ない人の本当の理由 (58k, ×5,8) · 人混みが苦手な人の本当の理由 (25k) · 一人でいても寂しくない人の脳
(24k) · 一人が好きな人の本当の理由 (23k) · SNSをやらない人だけが気づいていること (12k). Tiêu đề NGẮN, không 【心理学】,
không "恐ろしい特徴", không số đếm. Đây là kênh đồng tuyến đúng nghĩa để theo dõi hằng ngày: nó nổ ở đâu, ta biết
tệp trẻ hơn đang thích gì.

**(b) Cụm remake nguyên tiêu đề.** 心理ラボ, こころノート心理学, ちょっと元気になれる心理学 đều remake ĐÚNG các hit
mà TL4-T7 cũng remake: 子供時代 (V5), この5つを一人で (V6), 休日に一歩も外に出ない (V4), SNSをしない人の特徴 (V8).
Kết quả của họ: ×1,0–1,3 quy mô kênh, 495–2.900 view. Khớp với V1/V4/V5/V6 của mình. Kết luận đo được:
**remake nguyên tiêu đề một hit cũ là lối đã đông người — hit cũ không nổ lại cho kênh nhỏ.** Video nổ của các
kênh nhỏ trong cụm (ズレは才能 ×5,8; 心理ラボ 独り言 ×6,8; ちょっと元気 職場で地頭がいい人ほど一人で ×4,6) đều là
GÓC MỚI trong tuyến, không phải bản chép tiêu đề.

## 5. Việc kế tiếp (theo thứ tự)

1. **V8 giữ H1fZAMiOwW0** — đọc V7 @13h sáng 06/09 trước, theo mốc đã chốt (≥200 imp mặt phân phối = mở).
2. **V9/V10:** lấy insight "không hứng thú thể thao" (#2, #3) — chưa ai trong kênh khai thác, ×25+ ở hai kênh khác
   nhau, và là từ khoá gốc của tuyến. Viết góc riêng, không chép nguyên tiêu đề (mục 4b).
3. **Đánh "Đã làm" cho nguồn của V2, V3, V7** trong content.csv — hiện chỉ 4/7 lượt được đánh, bộ chấm của tool
   sẽ đề xuất lại thứ đã làm.
4. **Quét ズレは才能 mỗi ngày** cùng lượt quét đối thủ; nếu nó ra video ×3+ trong 7 ngày → ứng viên remake góc.
5. Hộp thư còn 4 kênh self-help chung: anh quyết giữ/bỏ trong tab Nghiên cứu.
6. 4 tiêu đề trang chủ "lưỡng lự" chưa phân — không đáng tốn AI.
