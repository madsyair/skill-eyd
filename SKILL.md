---
name: eyd
description: Pedoman menulis dan menyunting teks berbahasa Indonesia yang baik dan benar sesuai EYD Edisi V (2022), kalimat efektif (hemat, cermat, logis), dan paragraf yang padu. Gunakan skill ini SETIAP KALI menulis, menyunting, memeriksa, memperbaiki, atau menerjemahkan ke bahasa Indonesia apa pun bentuknya — artikel ilmiah, skripsi/tesis, abstrak, laporan, surat dinas, dokumen akreditasi, RPS, modul ajar, proposal, notula, siaran pers, artikel populer, takarir media sosial, atau sekadar satu paragraf — meskipun pengguna tidak menyebut "EYD", "ejaan", atau "kalimat efektif". Juga gunakan saat pengguna bertanya tentang kata baku, tanda baca, huruf kapital, penulisan angka/singkatan, padanan istilah asing (KBBI), atau menyuruh "rapikan", "perbaiki bahasanya", "koreksi", "proofread", "buat lebih formal/efektif". Skill ini memuat teks resmi EYD V, inventaris kesalahan umum, panduan kepaduan antarkalimat/antarparagraf, kebijakan istilah asing vs padanan KBBI, dan skrip pemeriksa otomatis.
---

# Menulis Bahasa Indonesia yang Baik dan Benar (EYD V)

Tulisan yang **benar** mengikuti EYD V dan tata bahasa baku. Tulisan yang **baik** jelas, konkret, bertenaga, terstruktur sesuai jenisnya, dan berpihak pada pembaca — benar saja tidak cukup. Skill ini mengejar keduanya dengan dua mekanisme: **harness** (pemeriksa otomatis + rubrik tetap) dan **loop** (tulis → periksa → perbaiki → periksa lagi sampai bersih). Jangan pernah menyerahkan teks Indonesia tanpa melewati loop ini minimal sekali.

## Berkas dalam skill ini

| Berkas | Isi | Kapan dibaca |
|---|---|---|
| `references/eyd-v-ringkas.md` | Kaidah EYD V yang paling sering dilanggar + apa yang berubah dari PUEBI | **Selalu**, sebelum menulis/menyunting |
| `references/inventaris-kesalahan.md` | Peta ranjau: ratusan pola salah → benar (ejaan, imbuhan, kata depan, gabungan kata, partikel, angka, tanda baca, struktur kalimat, pleonasme, diksi, ragam, istilah) | Saat menyunting; saat harness melaporkan kategori tertentu |
| `references/kalimat-efektif.md` | Enam syarat kalimat efektif; alat kohesi antarkalimat; anatomi paragraf dan cara menjahit antarparagraf; daftar periksa kepaduan | Teks > 1 paragraf |
| `references/menulis-baik.md` | Sisi *baik*: tiga pertanyaan pra-tulis, kejelasan, kekonkretan, tenaga dan irama, struktur per jenis tulisan (abstrak, pendahuluan, surat dinas, laporan, modul, opini), pembuka/penutup, tanda tulisan mesin, daftar periksa | **Selalu** saat menulis naskah baru; iterasi terakhir saat menyunting |
| `references/kata-hubung.md` | Konjungsi tiga tingkat (intrakalimat, antarkalimat, antarparagraf), pasangan korelatif, 30+ pasangan yang sering tertukar (*tetapi/namun, sedangkan/sementara, dengan demikian/oleh karena itu*), daftar periksa | Teks > 1 paragraf; saat harness melaporkan K-awal, K-konj, T-koma, P-kepaduan |
| `references/istilah-dan-kbbi.md` | Kebijakan istilah asing vs padanan KBBI (Kelas A/B/C) + glosarium statistika/sains data/komputasi | Teks mengandung istilah asing atau teknis |
| `references/eyd-v-lengkap.md` | Teks resmi EYD V (±13.000 kata) dengan daftar isi | Hanya jika ringkasan tidak menjawab; cari dengan `grep -n` pada judul bab |
| `evals/` | Contoh naskah bermasalah/bersih + `evals.json` untuk menguji ulang skill setelah diubah | Saat memperbaiki skill ini |
| `scripts/periksa.py` | Pemeriksa otomatis (harness). `--fix` menerapkan perbaikan aman; `--json` untuk loop; `--ragam populer` melonggarkan aturan cakapan | Setiap iterasi loop |

## Alur kerja (harness + loop)

### Langkah 0 — Tentukan mode dan ragam (10 detik)
- **Mode**: (a) menulis baru, (b) menyunting teks pengguna, (c) memeriksa/menjelaskan kaidah saja, (d) menerjemahkan ke Indonesia.
- **Ragam**: *ilmiah* (skripsi, artikel jurnal, laporan penelitian), *resmi* (surat dinas, dokumen instansi, akreditasi, RPS), atau *populer* (blog, media sosial, buku populer). Jika tidak jelas, tebak dari konteks; tanyakan hanya jika pilihan ragam mengubah hasil secara drastis.
- **Pembaca**: menentukan Kelas istilah (A/B/C) — lihat `istilah-dan-kbbi.md`.
- Baca `references/eyd-v-ringkas.md` sekarang. Untuk teks > 1 paragraf, baca juga `references/kalimat-efektif.md` dan `references/kata-hubung.md`.

### Langkah 1 — Tulis atau terima draf
Mode menulis: jawab dahulu tiga pertanyaan `menulis-baik.md` §1 (siapa pembacanya, apa yang harus mereka ketahui/lakukan, apa pesan intinya — satu kalimat), pilih struktur menurut jenis tulisan (§5), susun kerangka (gagasan per paragraf), lalu tulis. Pesan inti harus muncul di 30 detik pertama membaca. Terapkan sejak awal: subjek–predikat jelas, satu paragraf satu gagasan, kalimat 15–25 kata, istilah konsisten, transisi antarkalimat diikuti koma.
Mode menyunting: pertahankan makna dan gaya penulis; ubah hanya yang salah atau tidak efektif. Jangan menulis ulang total kecuali diminta.
Simpan draf ke berkas, misalnya `/home/claude/draf.md` (harness membaca berkas).

### Langkah 2 — Jalankan harness otomatis
```bash
python3 scripts/periksa.py /home/claude/draf.md            # ragam ilmiah/resmi
python3 scripts/periksa.py /home/claude/draf.md --ragam populer
python3 scripts/periksa.py /home/claude/draf.md --fix /home/claude/draf2.md   # terapkan perbaikan aman dahulu
```
Kategori laporan: E (baku), I (imbuhan), D (kata depan/terikat), G (gabungan/ulang), P (partikel), H (kapital), S (angka/singkatan), T (tanda baca), K (kalimat), M (mubazir), L (diksi), R (ragam), A (istilah), P-kepaduan. Temuan pada teks miring diturunkan ke WARNING karena mungkin istilah asing/judul.
Berkas `.tex` dan `.md` diratakan lebih dulu (rumus → kata ganti di dalam baris, judul → `§`, komentar/preambel/sitasi dibuang, baris dalam satu paragraf digabung), sehingga naskah LaTeX dapat diperiksa langsung. Judul dan kalimat tanya dikecualikan dari aturan tingkat kalimat. Kata yang berfungsi ganda (*Pertama, Ketiga, Akibatnya, Kemudian*) hanya WARNING karena bisa numeralia/subjek.
**Konvensi kutipan contoh salah**: baris yang memuat `→` atau `~~` dianggap catatan penyuntingan dan dilewati. Saat menulis catatan perubahan, tulis contoh salah dengan pola `*salah* → *benar*` agar tidak ditandai sebagai kesalahan; prosa naskah tetap diperiksa terpisah dari catatannya.
Bacalah laporan sebagai **petunjuk, bukan vonis**: skrip tidak memahami konteks. Contoh yang harus dinilai sendiri: `di mana` dalam kalimat tanya sah; `antar dan` bukan bentuk terikat; `tergantung` sebagai 'digantung' sah; `3 kabupaten` dalam perincian boleh angka; `jika ..., maka` dalam teks matematis boleh. ERROR hampir selalu benar; WARNING perlu penilaian.

### Langkah 3 — Tinjauan manual dengan rubrik tetap
Harness hanya menangkap pola permukaan. Periksa sendiri sepuluh dimensi berikut, satu per satu, sambil membaca teks sekali lagi:

1. **Ejaan & kata baku** — semua kata sesuai KBBI/EYD V (serapan: *-itas, -is, -ik, v/f, k/c*).
2. **Imbuhan** — peluluhan k/t/s/p; *mengubah*; gabungan kata berimbuhan (awalan saja → sebagian; awalan+akhiran → serangkai).
3. **Kata depan & bentuk terikat** — *di/ke* terpisah untuk tempat; *antar-, pasca-, sub-, non-* serangkai; *Maha* + sifat Tuhan terpisah.
4. **Huruf kapital & miring** — nama diri, lembaga, jabatan+nama, geografi vs nama jenis; istilah asing miring; judul karya miring.
5. **Angka, singkatan, satuan** — satu kata → huruf; ukuran/uang/persen → angka; *Rp5.000*; *s.d., dll.*; tanda pisah untuk rentang; kalimat tidak diawali angka.
6. **Tanda baca** — koma sebelum *tetapi/sedangkan/melainkan*; koma setelah anak kalimat di depan dan setelah penghubung antarkalimat; tanpa koma sebelum *bahwa*; titik dua hanya setelah pernyataan lengkap; titik koma untuk perincian berkoma.
7. **Struktur kalimat** — tiap kalimat punya S dan P; tidak ada subjek berkata depan; tidak ada konjungsi ganda; tidak ada kalimat diawali *Sehingga/Sedangkan/Dimana/Yang mana*; paralel; ≤40 kata.
8. **Kehematan & kecermatan** — tidak ada pleonasme; nominalisasi bertele-tele diganti verba; *terdiri atas, bergantung pada, antara ... dan, pukul/jam, suatu/sesuatu, setiap/masing-masing*; kata ganti mengacu jelas.
9. **Kepaduan & kata hubung** — konjungsi tepat tingkatnya (*tetapi* di dalam kalimat, *Namun,* antarkalimat; *sedangkan* pertentangan, *sementara* waktu; *dengan demikian* simpulan, *oleh karena itu* akibat); korelatif lengkap; kata tunjuk beracuan jelas; tiap paragraf satu kalimat topik; kalimat pertama paragraf terhubung ke paragraf sebelumnya (kata kunci/transisi/pengacuan); transisi bervariasi; *tersebut/ini/itu* mengacu jelas; urutan logis dipertahankan; penutup memantulkan tujuan.
10. **Istilah** — satu konsep satu istilah; penyebutan pertama memakai pola Kelas A/B/C; istilah asing miring; padanan KBBI hadir sebagai penjelasan bila istilah asing dipertahankan.
11. **Kejelasan & kekonkretan** — pesan inti tampak di awal; klaim didukung angka/contoh; tidak ada kata kabur (*berbagai, cukup, pihak terkait, signifikan* nonstatistik) tanpa penjelasan; verba bekerja (*terdapat/adanya/melakukan + nomina* diperiksa); kata tunjuk beracuan jelas.
12. **Gaya & struktur** — panjang kalimat bervariasi; tidak ada pembuka klise, penguat kosong, penyangga bertumpuk, rangkaian sinonim, transisi berulang; struktur sesuai jenis tulisan; pembuka mengait, penutup memberi implikasi; tidak terbaca sebagai tulisan mesin (`menulis-baik.md` §7).

### Langkah 4 — Perbaiki, lalu ulangi Langkah 2–3
Kriteria berhenti: (a) harness melaporkan **0 ERROR** dan setiap WARNING yang tersisa sudah dinilai sah, **dan** (b) sepuluh dimensi rubrik lolos. Biasanya butuh 2 iterasi; batasi maksimum 4. Pada iterasi terakhir, baca teks sekali lagi dari atas ke bawah untuk kepaduan dan gaya (dimensi 9, 11, 12) — ini yang paling sering luput karena perbaikan lokal bisa memutus alur. Uji terakhir: baca hanya kalimat pertama tiap paragraf; alur argumen harus masih terbaca.

### Langkah 5 — Serahkan
- **Mode menulis**: berikan teks final. Jika pengguna meminta berkas, tulis ke `/mnt/user-data/outputs/` dan tampilkan dengan `present_files`. Sebutkan singkat pilihan istilah Kelas C (istilah asing yang dipertahankan beserta padanan KBBI-nya) jika ada.
- **Mode menyunting**: tanyakan dalam hati seberapa jauh boleh mengubah. Jika pengguna hanya minta "perbaiki"/"koreksi", sunting kaidah dan kejelasan tanpa mengubah struktur; jika minta "buat lebih baik"/"tulis ulang"/"perbaiki alurnya", terapkan juga dimensi 11–12 termasuk menyusun ulang paragraf. Berikan (1) teks hasil suntingan, dan (2) **catatan perubahan** ringkas berkelompok per kategori (kode E/I/D/G/P/S/T/K/M/L/R/A) dengan contoh sebelum → sesudah dan alasan satu baris. Jangan mendaftar setiap perubahan sepele; kelompokkan. Jika teks panjang, catatan cukup 5–12 butir yang paling berpengaruh. Format tabel cocok untuk ini.
- **Mode memeriksa**: sebutkan kaidah EYD V yang berlaku (nama bab/butir), bentuk benar, dan alasan; kutip contoh dari `eyd-v-ringkas.md` atau `eyd-v-lengkap.md`.
- Tulis dalam bahasa Indonesia yang juga mematuhi kaidah ini — jawaban tentang EYD yang sendiri melanggar EYD tidak dapat dipercaya.

## Kebijakan istilah asing dan KBBI (ringkas)
Padanan KBBI **tidak wajib dipakai** bila belum populer bagi pembaca sasaran, tetapi **wajib disertakan sebagai penjelasan** pada penyebutan pertama. Tiga kelas:
- **A** (padanan sudah umum): pakai padanan saja — *unduh, daring, tautan, pemangku kepentingan, pencilan, peubah*.
- **B** (dikenal, tetapi istilah asing masih lazim di bidangnya): padanan (*asing*) — *pembelajaran mesin (machine learning)*, *mahadata (big data)*.
- **C** (padanan belum populer): *asing* (padanan) — **podcast* (siniar)*, **server* (peladen)*, **overfitting* (kelewat pas)*.
Setelah penyebutan pertama, gunakan satu bentuk secara konsisten. Istilah asing selalu miring; jangan bentuk hibrida (*diupload* → *diunggah*). Rinciannya dan glosarium bidang statistika/sains data ada di `istilah-dan-kbbi.md`.

## Prinsip penyuntingan yang sering dilupakan
- Perbaikan lokal jangan merusak alur: setelah menghapus *Sehingga* di awal kalimat, pastikan hubungan sebab-akibatnya tetap tersampaikan (*Dengan demikian,* atau gabungkan kalimat).
- *Hemat* bukan berarti *pendek*: kalimat boleh panjang jika setiap kata bekerja; kalimat pendek beruntun tanpa penghubung justru tidak padu.
- Ragam populer tetap harus benar ejaannya; yang boleh longgar hanya pilihan kata (*tapi, oke*) dan panjang kalimat.
- Nama diri (orang, lembaga, produk, judul resmi) tidak diubah ejaannya meskipun tidak sesuai EYD (*Soekarno, Universitas Airlangga, Jalan Panglima Polim*).
- Kutipan langsung tidak disunting; kesalahan dalam kutipan ditandai *[sic]* bila perlu.
- Konvensi bidang (notasi statistik, *p-value* → nilai-*p*, *et al.* dalam sitasi) dihormati; konsistenkan dengan gaya selingkung jurnal/lembaga jika pengguna menyebutnya.
- Jika suatu kaidah tidak ditemukan di berkas skill dan tidak yakin, katakan tidak yakin dan tandai `[cek KBBI]` — jangan mengarang kaidah. Bila akses web tersedia, KBBI daring (kbbi.kemdikbud.go.id) dan situs EYD (ejaan.kemendikdasmen.go.id) adalah rujukan utama.

## Contoh singkat mode menyunting

Masukan pengguna:
> Dalam penelitian ini membahas analisa kemiskinan dimana data yang digunakan adalah Susenas. Sehingga hasilnya dapat dipergunakan pemda. Meskipun sampel kecil, tetapi hasilnya sangat baik sekali.

Keluaran:
> **Hasil suntingan**
> Penelitian ini menganalisis kemiskinan dengan data Susenas sehingga hasilnya dapat digunakan pemerintah daerah. Meskipun sampelnya kecil, hasilnya baik.
>
> **Catatan perubahan**
> | Kode | Sebelum → Sesudah | Alasan |
> |---|---|---|
> | K1 | *Dalam penelitian ini membahas* → *Penelitian ini menganalisis* | subjek berkata depan; nominalisasi diganti verba |
> | E1 | *analisa* → *analisis* | serapan *-is* (EYD V, unsur serapan) |
> | K9 | *dimana* → dihapus | 'di mana' bukan penghubung relatif; struktur diubah |
> | K3 | *Sehingga* di awal kalimat → digabung | konjungsi intrakalimat tidak mengawali kalimat |
> | K2 | *Meskipun ..., tetapi* → *Meskipun ...,* | konjungsi ganda |
> | M | *sangat baik sekali* → *baik* | pleonasme; klaim tanpa bukti dilemahkan |
