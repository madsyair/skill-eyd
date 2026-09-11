# eyd — Skill Claude untuk Menulis Bahasa Indonesia yang Baik dan Benar

Skill ini memandu Claude menulis dan menyunting teks berbahasa Indonesia sesuai **Ejaan Bahasa Indonesia yang Disempurnakan Edisi V (EYD V, 2022)**, dengan kalimat efektif dan paragraf padu. Skill ini dibangun untuk kebutuhan penulisan akademik dan kedinasan (artikel jurnal, skripsi/tesis, laporan, dokumen akreditasi, surat dinas, modul ajar), tetapi juga berlaku untuk tulisan populer.

Skill ini membedakan tulisan yang **benar** (kaidah EYD V dan tata bahasa) dari tulisan yang **baik** (jelas, konkret, bertenaga, terstruktur sesuai jenisnya, berpihak pada pembaca), dan mengejar keduanya. Dua hal yang membedakannya dari sekadar "daftar kaidah":

- **Harness**: skrip pemeriksa otomatis (`scripts/periksa.py`) yang mendeteksi ratusan pola kesalahan secara deterministik, ditambah rubrik tinjauan sepuluh dimensi.
- **Loop**: alur kerja tulis → periksa → perbaiki → periksa lagi sampai laporan bersih dan rubrik lolos. Claude tidak menyerahkan teks sebelum melewati loop ini.

## Isi repositori

```
eyd/
├── SKILL.md                         # alur kerja, rubrik, kebijakan istilah, format keluaran
├── references/
│   ├── eyd-v-lengkap.md             # teks resmi EYD V (±13.000 kata) dari ejaan.kemendikdasmen.go.id
│   ├── eyd-v-ringkas.md             # kaidah yang paling sering dilanggar + perubahan dari PUEBI
│   ├── inventaris-kesalahan.md      # ±400 pola salah → benar dalam 12 kategori
│   ├── kalimat-efektif.md           # kalimat efektif, kohesi antarkalimat, koherensi antarparagraf
│   ├── kata-hubung.md               # konjungsi tiga tingkat, korelatif, pasangan yang sering tertukar
│   ├── menulis-baik.md              # sisi 'baik': kejelasan, kekonkretan, gaya, struktur per jenis tulisan
│   ├── aparat-karya-ilmiah.md       # pola paragraf, argumentasi, kutipan/sitasi, tabel-gambar, judul, notasi
│   └── istilah-dan-kbbi.md          # kebijakan istilah asing vs padanan KBBI + glosarium sains data
├── scripts/
│   └── periksa.py                   # pemeriksa otomatis (Python 3, tanpa dependensi)
└── evals/
    ├── evals.json                   # kasus uji untuk regresi skill
    ├── contoh-bermasalah.md         # harus menghasilkan banyak temuan
    ├── contoh-bersih.md             # harus 0 temuan
    ├── contoh-kapital-istilah.md
    ├── contoh-konjungsi.md
    ├── contoh-gaya.md
    └── contoh-latex.tex
```

## Cara memasang

**Claude.ai / aplikasi Claude**
1. Unduh `eyd.skill` dari halaman *Releases* (atau kemas sendiri, lihat bawah).
2. Buka *Settings → Capabilities → Skills*, lalu unggah berkas tersebut.

**Claude Code**
```bash
git clone https://github.com/madsyair/skil-eyd.git
mkdir -p ~/.claude/skills
cp -r skil-eyd/eyd ~/.claude/skills/eyd
```
Untuk satu proyek saja, salin ke `.claude/skills/eyd` di akar proyek.

**Mengemas ulang** setelah mengubah isi (memerlukan [skill-creator](https://github.com/anthropics/skills)):
```bash
python3 -m scripts.package_skill /path/ke/eyd     # dijalankan dari folder skill-creator
```

## Cara memakai

Skill terpicu otomatis setiap kali Claude diminta menulis, menyunting, memeriksa, atau menerjemahkan ke bahasa Indonesia — tidak perlu menyebut "EYD". Contoh permintaan:

- *Perbaiki bahasa abstrak ini dan beri catatan perubahan.*
- *Tulis surat pemberitahuan tracer study, ragam resmi.*
- *Mana yang benar, "di mana" atau "dimana"?*
- *Rapikan paragraf ini supaya lebih padu.*

Dalam mode menyunting, Claude mengembalikan teks hasil suntingan **dan** catatan perubahan berkode kategori. Kodenya: E ejaan, I imbuhan, D kata depan, G gabungan kata, P partikel, H kapital, S angka/singkatan, T tanda baca, K kalimat, M mubazir, L diksi, R ragam, dan A istilah. Contohnya sebagai berikut.

| Kode | Sebelum → Sesudah | Alasan |
|---|---|---|
| K1 | *Dalam penelitian ini membahas* → *Penelitian ini membahas* | subjek berkata depan |
| E1 | *analisa* → *analisis* | serapan *-is* |
| K3 | *Sehingga* di awal kalimat → digabung | konjungsi intrakalimat |

### Menjalankan pemeriksa sendiri

Skrip ini juga berguna tanpa Claude, misalnya sebagai pemeriksa pra-kirim (*pre-commit*) naskah:

```bash
python3 scripts/periksa.py naskah.md                  # laporan ke layar
python3 scripts/periksa.py naskah.tex                 # LaTeX diratakan: rumus → kata ganti, judul → §
python3 scripts/periksa.py naskah.docx                # lewat pandoc, bila terpasang
python3 scripts/periksa.py naskah.md --ragam populer  # longgarkan aturan ragam cakapan
python3 scripts/periksa.py naskah.md --fix keluar.md  # terapkan perbaikan yang aman, simpan ke berkas baru
python3 scripts/periksa.py naskah.md --json           # keluaran JSON untuk otomasi
```

Kode keluar `0` berarti tidak ada ERROR; `1` berarti ada. WARNING tidak memengaruhi kode keluar. Kategori `B-gaya` (pembuka klise, kata kabur, penguat kosong, penyangga bertumpuk, verba lemah, kalimat seragam) selalu WARNING karena menyangkut *baik*, bukan *benar*.

Contoh laporan:
```
== periksa.py — naskah.md ==
412 kata, 24 kalimat, rata-rata 17.2 kata/kalimat
ERROR: 3   WARNING: 2
  E-baku         1
  K-awal         1
  L-diksi        1
  T-koma         2

[ERROR  ] baris    5 E-baku       "analisa" → analisis
[ERROR  ] baris    9 K-awal       "Sehingga hasilnya dapat..." → konjungsi intrakalimat tidak mengawali kalimat; ...
[ERROR  ] baris   12 L-diksi      "terdiri dari" → terdiri atas
```

Perlu diingat: pemeriksa bekerja dengan pola, bukan pemahaman. **ERROR hampir selalu benar; WARNING perlu penilaian konteks** (*di mana* dalam kalimat tanya sah, *Ketiga* bisa numeralia, *jika–maka* boleh dalam teks matematis). Temuan pada teks miring diturunkan ke WARNING karena mungkin istilah asing atau judul. Baris yang memuat `→` atau `~~` dianggap catatan penyuntingan dan dilewati, sehingga dokumen yang *membahas* kesalahan tidak ditandai sebagai *melakukan* kesalahan.

## Kebijakan istilah asing dan KBBI

Padanan KBBI **tidak wajib dipakai** bila belum populer bagi pembaca sasaran, tetapi **selalu disertakan sebagai penjelasan** pada penyebutan pertama. Tiga kelas:

| Kelas | Kondisi | Pola | Contoh |
|---|---|---|---|
| A | padanan sudah umum | padanan saja | *unduh, daring, pencilan, pemangku kepentingan* |
| B | padanan dikenal, istilah asing masih lazim | padanan (*asing*) | *pembelajaran mesin (machine learning)* |
| C | padanan belum populer | *asing* (padanan) | **podcast* (siniar)*, **server* (peladen)* |

Setelah penyebutan pertama, satu konsep memakai satu istilah secara konsisten. Glosarium ±100 istilah statistika, sains data, dan komputasi ada di `references/istilah-dan-kbbi.md`.

## Menguji perubahan

Setiap kali mengubah `periksa.py` atau berkas rujukan, jalankan regresi:

```bash
python3 scripts/periksa.py evals/contoh-bersih.md        # harus: ERROR 0; WARNING hanya B-gaya
python3 scripts/periksa.py evals/contoh-gaya.md          # harus: ERROR 0; ≥10 WARNING B-gaya
python3 scripts/periksa.py evals/contoh-bermasalah.md    # harus: puluhan temuan
python3 scripts/periksa.py evals/contoh-latex.tex        # harus: tepat 2 ERROR (Sehingga di awal, terdiri dari)
```

`evals/evals.json` memuat enam prompt uji beserta keluaran yang diharapkan untuk menguji perilaku Claude, bukan hanya skripnya. Prinsip yang dipakai selama pengembangan: **menurunkan jumlah temuan tidak ada gunanya bila pemeriksa jadi buta** — setiap perubahan harus tetap menangkap kesalahan pada naskah uji.

## Berkontribusi

Laporan kesalahan yang paling berguna berbentuk satu kalimat contoh + apa yang diharapkan:

- *Temuan palsu*: kalimat yang benar, tetapi ditandai. Sertakan kalimatnya dan kaidah EYD V yang membenarkannya.
- *Kesalahan lolos*: kalimat salah yang tidak tertangkap. Sertakan bentuk benarnya.
- *Kaidah baru*: rujuk bab dan butir EYD V di `references/eyd-v-lengkap.md` atau sumber Badan Bahasa.

Tambahkan kasusnya ke `evals/` bila memungkinkan. Pola yang hanya benar dengan konteks sintaksis (misalnya kata berfungsi ganda) masuk sebagai WARNING, bukan ERROR.

## Sumber

- Badan Pengembangan dan Pembinaan Bahasa. 2022. *Ejaan Bahasa Indonesia yang Disempurnakan Edisi V*. Keputusan Kepala Badan Nomor 0424/I/BS.00.01/2022. https://ejaan.kemendikdasmen.go.id/eyd/
- Kamus Besar Bahasa Indonesia daring. https://kbbi.kemdikbud.go.id/
- Kajian kesalahan berbahasa pada artikel jurnal dan tugas akhir mahasiswa (kesalahan konjungsi, kohesi, dan koherensi), serta rubrik Bahasa Kompas dan Balai Bahasa Provinsi Jawa Barat untuk pasangan konjungsi yang sering tertukar.

## Lisensi

MIT. Teks EYD V adalah dokumen resmi pemerintah yang disalin untuk rujukan; hak atasnya tetap pada Badan Pengembangan dan Pembinaan Bahasa.

## Penulis

Achmad Syahrul Choir — Politeknik Statistika STIS. Dibangun bersama Claude dengan metode *harness engineering* dan *looping engineering*.
