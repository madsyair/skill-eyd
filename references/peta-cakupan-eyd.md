# Peta Cakupan EYD V dalam Skill Ini

Peta ini menghubungkan setiap butir kaidah EYD V dengan tempat butir itu dicakup di skill: ringkasan, rujukan, dan kategori pemeriksa otomatis. Gunakan peta ini untuk (1) mengecek apakah suatu kaidah sudah tercakup sebelum menjawab pertanyaan kaidah dan (2) merawat skill. Setiap kali `eyd-v-lengkap.md`, ringkasan, atau pemeriksa diubah, jalankan:

```bash
python3 scripts/audit_cakupan.py            # wajib 0 ERROR
python3 scripts/audit_cakupan.py --rinci    # daftar butir ◐/✗
```

Audit memeriksa empat hal. (1) Setiap subbab resmi EYD V ada di `eyd-v-lengkap.md`. (2) Jumlah butir subbab yang sudah dicocokkan sama dengan situs resmi. (3) Setiap butir punya baris di tabel ini. (4) Berkas yang dirujuk memang ada.

Status: **✓** dicakup di ringkasan atau rujukan khusus; **◐** dicakup sebagian, sisanya hanya di `eyd-v-lengkap.md`; **✗** belum dicakup. Kolom *Butir* boleh berisi rentang (`II.C.1a-1g`, `IV.A.1-95`). "Ringkas" berarti `eyd-v-ringkas.md`; "Inv" berarti `inventaris-kesalahan.md`.

**Hasil kajian 10 November 2026.** Teks resmi diambil dari ejaan.kemendikdasmen.go.id. Ditemukan lima celah. (1) Bab I.A Huruf Abjad, I.C Huruf Konsonan, dan I.E Gabungan Huruf Konsonan tidak ada di salinan teks resmi; sekarang sudah ditambahkan. (2) Butir yang tidak tercakup di ringkasan: I.F.3, I.F.5, I.F.9, II.B.2b, II.G.8, II.G.12, II.H.2, II.I.2, III.A.2, III.A.5, III.A.6, III.D.4, III.D.7, III.E.3, III.E.6–9, III.G, III.H, III.I, III.L.3, III.M.2, III.N.3, dan IV.B. (3) Tiga klaim ringkasan tidak sesuai EYD V: huruf tebal untuk lema kamus, titik dalam daftar pustaka, dan koma sebelum *yaitu* sebagai butir tersendiri. (4) Singkatan dan kepanjangannya belum punya rujukan tersendiri, dan pemeriksa hanya menangkap lima pola singkatan. (5) Kaidah rumus tampilan sebagai bagian paragraf belum ada. Semua celah sudah ditutup.

| Butir | Kaidah | Status | Di skill | Pemeriksa |
|---|---|---|---|---|
| I.A | Abjad 26 huruf; nama dan pengucapan huruf | ✓ | Ringkas §0b; `singkatan-akronim.md` §2 | — |
| I.B | Lima huruf vokal; diakritik *ê* untuk *e* pepet | ✓ | Ringkas §0, §0b | — |
| I.C | 21 huruf konsonan; *q* dan *x* untuk nama diri/bidang tertentu | ✓ | Ringkas §0, §0b | — |
| I.D.1-2 | Monoftong *eu*; diftong *ai, au, ei, oi* | ✓ | Ringkas §0, §0b; `pemenggalan-kata.md` | N-penggal |
| I.E | Gabungan konsonan *kh, ng, ny, sy* | ✓ | Ringkas §0b; `pemenggalan-kata.md` | N-penggal |
| I.F.1 | Kapital awal kalimat | ✓ | Ringkas §1; `singkatan-akronim.md` §2 | — |
| I.F.2 | Kapital nama orang dan julukan | ✓ | Ringkas §1 | — |
| I.F.3 | Nama orang sebagai nama jenis/satuan tidak kapital | ✓ | Ringkas §1 | — |
| I.F.4 | Nama orang pada teori, hukum, rumus | ✓ | Ringkas §0, §1 | — |
| I.F.5 | *bin, binti, boru, van* tidak kapital | ✓ | Ringkas §1 | — |
| I.F.6 | Kapital awal petikan langsung | ✓ | Ringkas §1 | — |
| I.F.7 | Nama agama, kitab suci, Tuhan, kata ganti Tuhan | ✓ | Ringkas §1 | H-kapital |
| I.F.8 | Gelar diikuti nama orang; gelar akademik sesudah nama | ✓ | Ringkas §1 | — |
| I.F.9 | Gelar, profesi, jabatan sebagai sapaan | ✓ | Ringkas §1 | — |
| I.F.10 | Jabatan dan pangkat diikuti nama/pengganti nama | ✓ | Ringkas §1 | — |
| I.F.11 | Nama bangsa, suku, bahasa, aksara | ✓ | Ringkas §1 | H-kapital |
| I.F.12 | Bentuk turunan nama bangsa/bahasa tidak kapital | ✓ | Ringkas §1 | — |
| I.F.13 | Nama tahun, bulan, hari, hari besar | ✓ | Ringkas §1 | H-kapital |
| I.F.14-15 | Peristiwa sejarah; bukan nama → nonkapital | ✓ | Ringkas §1 | — |
| I.F.16-19 | Nama geografi; unsur tanpa nama diri; nama jenis; asal daerah | ✓ | Ringkas §1 | — |
| I.F.20 | Nama negara, lembaga, organisasi, dokumen | ✓ | Ringkas §1, §3f; `singkatan-akronim.md` §3b | H-kapital, S-singkatan |
| I.F.21 | Judul buku, karangan, media massa | ✓ | Ringkas §1; `aparat-karya-ilmiah.md` §6 | — |
| I.F.22 | Singkatan gelar dan pangkat | ✓ | Ringkas §1, §3f; `singkatan-akronim.md` §2 | S-singkatan |
| I.F.23 | Kata kekerabatan sebagai sapaan | ✓ | Ringkas §1 | — |
| I.G.1-3 | Huruf miring: judul, penegasan, bahasa daerah/asing | ✓ | Ringkas §2; `istilah-dan-kbbi.md` | E-baku (teks miring diturunkan ke WARNING), A-istilah |
| I.H.1-2 | Huruf tebal: penegasan dalam teks miring; bab/subbab | ✓ | Ringkas §2 | — |
| II.A | Kata dasar ditulis mandiri | ✓ | Ringkas §3 | — |
| II.B.1a | Kata berimbuhan serangkai | ✓ | Ringkas §3; Inv I | E-baku |
| II.B.1b | Bentuk terikat serangkai | ✓ | Ringkas §3a; Inv D | D-terikat |
| II.B.1c | Bentuk terikat + huruf kapital → tanda hubung | ✓ | Ringkas §3a, §3f; `singkatan-akronim.md` §2 | S-singkatan |
| II.B.1d | Bentuk terikat + kata miring → tanda hubung | ✓ | Ringkas §3a, §4 (tanda hubung) | — |
| II.B.1e | *maha-* + nama/sifat Tuhan terpisah | ✓ | Ringkas §0, §3a | E-baku |
| II.B.2a | Bentuk ulang dengan tanda hubung | ✓ | Ringkas §3c | G-ulang |
| II.B.2b | Bentuk ulang gabungan kata: ulang unsur pertama | ✓ | Ringkas §3c | — |
| II.B.3a-3e | Gabungan kata: terpisah, hubung, serangkai | ✓ | Ringkas §3b; Inv G | E-baku |
| II.C.1a-1g | Pemenggalan kata dasar | ✓ | Ringkas §3i; `pemenggalan-kata.md` | N-penggal; `penggal.py` |
| II.C.2a-2d | Pemenggalan kata berimbuhan | ✓ | Ringkas §3i; `pemenggalan-kata.md` | N-penggal; `penggal.py` |
| II.C.3-5 | Unsur gabungan, nama orang, singkatan tidak dipenggal | ✓ | Ringkas §3i; `pemenggalan-kata.md`; `singkatan-akronim.md` §2 | N-penggal |
| II.D | Kata depan terpisah | ✓ | Ringkas §3d; Inv D | E-baku |
| II.E.1-4 | Partikel *-lah, -kah, -tah, pun, per* | ✓ | Ringkas §3e; Inv P | E-baku |
| II.F.1-3, II.F.4a-4c, II.F.5-7 | Singkatan dan akronim (gelar, inisial, huruf awal, umum, alamat, satuan, akronim) | ✓ | Ringkas §3f; `singkatan-akronim.md` §1; Inv S | S-singkatan |
| II.G.1 | Angka Arab dan Romawi | ✓ | Ringkas §3g | — |
| II.G.2 | Bilangan satu kata ditulis dengan huruf | ✓ | Ringkas §0, §3g | S-angka |
| II.G.3 | Angka untuk ukuran dan nilai | ✓ | Ringkas §3g | S-angka |
| II.G.4 | Angka di awal kalimat | ✓ | Ringkas §3g | S-angka |
| II.G.5 | Bilangan besar sebagian huruf | ✓ | Ringkas §3g | — |
| II.G.6-7 | Angka pada alamat; penomoran karangan/kitab suci | ✓ | Ringkas §3g | — |
| II.G.8a-8b | Bilangan dengan huruf: utuh mandiri; pecahan dengan *per-* | ✓ | Ringkas §3g | — |
| II.G.9 | Bilangan tingkat | ✓ | Ringkas §3g | S-angka |
| II.G.10 | Angka + *-an* dengan tanda hubung | ✓ | Ringkas §3g | S-angka |
| II.G.11 | Angka diikuti huruf dalam dokumen resmi | ✓ | Ringkas §3g | — |
| II.G.12 | Bilangan dalam nama geografi serangkai | ✓ | Ringkas §3g | — |
| II.H.1-2 | Kata ganti *ku-, kau-, -ku, -mu, -nya*; *kau* bebas terpisah | ✓ | Ringkas §3h | — |
| II.I.1-2 | *si* dan *sang*; *Sang* untuk nama Tuhan | ✓ | Ringkas §3h | — |
| III.A.1-2 | Titik akhir kalimat; pernyataan lengkap + perincian baru | ✓ | Ringkas §4 | — |
| III.A.3-6 | Titik dalam daftar, deret nomor, perincian berkurung, judul tabel/gambar | ✓ | Ringkas §4; `aparat-karya-ilmiah.md` §5–6 | — |
| III.A.7 | Titik pemisah jam, menit, detik | ✓ | Ringkas §0, §4 | S-angka |
| III.A.8-9 | Titik ribuan untuk jumlah; bukan untuk tahun/nomor | ✓ | Ringkas §3g, §4 | S-angka |
| III.A.10-11 | Tanpa titik pada judul, alamat penerima, tanggal surat | ✓ | Ringkas §4; Inv T14 | — |
| III.B.1-14 | Tanda koma | ✓ | Ringkas §4; `kata-hubung.md`; Inv T | T-koma |
| III.C.1-4 | Tanda titik koma | ✓ | Ringkas §0, §4 | — |
| III.D.1-2 | Titik dua sesudah pernyataan lengkap; tidak bila perincian bagian kalimat | ✓ | Ringkas §4 | T-titikdua |
| III.D.3-7 | Titik dua: pemerian, drama, jilid/halaman, jam, rasio | ✓ | Ringkas §4 | — |
| III.E.1 | Tanda hubung pemenggalan | ✓ | Ringkas §3i; `pemenggalan-kata.md` | N-penggal |
| III.E.2 | Tanda hubung bentuk ulang | ✓ | Ringkas §3c, §4 | G-ulang |
| III.E.3-4 | Tanggal berangka, ejaan huruf, skor; memperjelas hubungan | ✓ | Ringkas §4 | — |
| III.E.5 | Kapital + nonkapital, huruf + angka | ✓ | Ringkas §3f, §4; `singkatan-akronim.md` §2 | S-singkatan |
| III.E.6 | Tanpa hubung bila angka = jumlah huruf (*P3K*) | ✓ | Ringkas §0, §3f, §4; `singkatan-akronim.md` §2 | S-singkatan |
| III.E.7-9 | Unsur daerah/asing/slang; imbuhan sebagai objek bahasan; dua unsur satu kesatuan | ✓ | Ringkas §4 | — |
| III.F.1-3 | Tanda pisah: sisipan, rentang | ✓ | Ringkas §3g, §4 | T-pisah |
| III.G.1-2 | Tanda tanya; (?) untuk hal yang diragukan | ✓ | Ringkas §4 | T-baca |
| III.H | Tanda seru | ✓ | Ringkas §4; Inv T17 | T-baca |
| III.I.1-4 | Tanda elipsis | ✓ | Ringkas §4 | — |
| III.J.1-3 | Tanda petik | ✓ | Ringkas §4; Inv T13 | — |
| III.K.1-2 | Tanda petik tunggal | ✓ | Ringkas §4; Inv T18 | — |
| III.L.1 | Kurung untuk singkatan dan padanan asing | ✓ | Ringkas §3f, §4; `singkatan-akronim.md` §3; `istilah-dan-kbbi.md` | S-singkatan |
| III.L.2-4 | Kurung: penjelasan, kata opsional, penanda perincian | ✓ | Ringkas §4 | T-spasi |
| III.M.1-2 | Kurung siku: koreksi; keterangan di dalam kurung | ✓ | Ringkas §4 | — |
| III.N.1-3 | Garis miring: nomor, pengganti *dan/atau/setiap*, koreksi | ✓ | Ringkas §4; Inv S | E-baku (*s/d, a/n*) |
| III.O | Apostrof | ✓ | Ringkas §4 | — |
| IV.A.1-95 | Serapan umum (95 butir) | ◐ | Ringkas §5 (kaidah tersering dan daftar kata baku); sisanya `eyd-v-lengkap.md` | E-baku (daftar kata tidak baku) |
| IV.B.1-2 | Deret konsonan akhir kata Arab | ◐ | Ringkas §5 (sebutan); contoh di `eyd-v-lengkap.md` | — |
| IV.B.3-4 | Konsonan ganda → tunggal; serapan lazim tidak diubah | ✓ | Ringkas §5 | — |

## Di luar EYD V, tetapi dicakup skill
Kaidah ini bukan butir EYD V, melainkan kaidah tata bahasa, penulisan ilmiah, atau penyuntingan. Rujukannya ada di berkas masing-masing.

| Topik | Di skill | Pemeriksa |
|---|---|---|
| Kalimat efektif, kepaduan, konjungsi | `kalimat-efektif.md`, `kata-hubung.md` | K-*, P-kepaduan |
| Kepanjangan singkatan: urutan, kapital, konsistensi | `singkatan-akronim.md` §3 | S-singkatan |
| Rumus tampilan bagian kalimat; lanjutan tanpa indentasi | `aparat-karya-ilmiah.md` §7 | A-rumus |
| Notasi, sitasi, tabel, gambar | `aparat-karya-ilmiah.md` | A-aparat |
| Istilah asing vs KBBI | `istilah-dan-kbbi.md` | A-istilah |
| Gaya dan kejelasan | `menulis-baik.md` | B-gaya |
