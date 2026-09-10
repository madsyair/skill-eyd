# Kebijakan Istilah: Padanan KBBI vs Istilah yang Sudah Populer

## Prinsip

Tujuan tulisan adalah dipahami. Padanan KBBI/Badan Bahasa **tidak wajib** dipakai jika belum populer di kalangan pembaca sasaran, tetapi padanan itu **tetap disertakan sebagai penjelasan** agar pembaca mengenalnya dan tulisan tetap "berbahasa Indonesia". Kaidahnya:

1. **Kelas A — padanan sudah populer**: pakai padanan Indonesia langsung, tanpa istilah asing. Contoh: *data, analisis, unduh, unggah, daring, luring, tautan, gawai, peramban, warganet, swafoto, penyintas, pemangku kepentingan, pindai, pemindai, tenggat, nirkabel, media sosial, aplikasi*.
2. **Kelas B — padanan dikenal tetapi istilah asing masih lebih lazim di bidangnya**: pakai padanan Indonesia, lalu istilah asing dalam kurung (miring) pada penyebutan **pertama**; selanjutnya padanan saja. Contoh: *pembelajaran mesin (machine learning)*, *mahadata (big data)*, *penambangan data (data mining)*, *kecerdasan buatan (artificial intelligence, AI)*.
3. **Kelas C — padanan KBBI belum populer / berisiko tidak dipahami**: pakai istilah asing (miring) sebagai istilah utama, lalu padanan KBBI dalam kurung pada penyebutan pertama sebagai penjelasan; selanjutnya istilah asing (miring) secara konsisten. Contoh: **podcast* (siniar)*, **mouse* (tetikus)*, **marketplace* (lokapasar)*, **overfitting* (kelewat pas)*.
4. **Nama diri, nama produk, merek, nama metode yang sudah jadi nama** tidak diterjemahkan dan tidak dimiringkan: *Python, R, Stan, Google, BPS*. Nama metode yang berupa frasa umum (*random forest*, *gradient boosting*) diperlakukan sebagai istilah asing Kelas C: miring, padanan dalam kurung pada penyebutan pertama, lalu konsisten.
5. **Konsistensi**: satu konsep, satu istilah, di seluruh naskah. Buat glosarium di awal/akhir dokumen panjang jika Kelas C banyak.
6. **Istilah asing selalu dimiringkan**; padanan Indonesia tidak. Singkatan asing (AI, ML, API, GPU) tidak dimiringkan.
7. **Jangan membentuk hibrida tidak baku**: ~~diupload, mengupload, di-upload-kan, ngeprint~~. Jika istilah asing terpaksa berimbuhan, pakai tanda hubung (*di-upgrade, me-recall*) — tetapi lebih baik gunakan padanan (*diunggah, memperbarui*).
8. **Penentuan kelas bergantung pada pembaca**: untuk artikel populer, kelas bisa naik/turun. Jika ragu, pilih Kelas B (padanan + kurung) — ini aman untuk hampir semua pembaca.
9. **Kata Indonesia yang keliru dianggap asing**: *data, statistik, komputer, internet, sistem, proses, fokus, target, valid, format* sudah diserap → tidak dimiringkan.

## Format penulisan pada penyebutan pertama

| Kelas | Pola | Contoh |
|---|---|---|
| A | padanan | *Data diunduh dari situs BPS.* |
| B | padanan (*asing*) | *Model pembelajaran mesin (*machine learning*) dilatih dengan ...* |
| C | *asing* (padanan) | *Materi dibagikan melalui *podcast* (siniar) mingguan.* |
| Singkatan | kepanjangan (SINGKATAN) | *kecerdasan buatan (*artificial intelligence*, AI)* |

Gunakan **kurung** untuk padanan/istilah, **petik tunggal** untuk makna: *outlier* (pencilan) 'nilai yang jauh dari sebaran'.

## Glosarium bidang statistika, sains data, dan komputasi

Kelas ditandai A/B/C sebagai default untuk pembaca akademik/instansi Indonesia; sesuaikan dengan pembaca.

| Istilah asing | Padanan (KBBI/Badan Bahasa) | Kelas |
|---|---|---|
| dataset | gugus data, set data | B |
| database | basis data, pangkalan data | A (basis data) |
| big data | mahadata | B |
| data mining | penambangan data | B |
| machine learning | pembelajaran mesin | B |
| deep learning | pembelajaran mendalam | B |
| artificial intelligence | kecerdasan buatan, kecerdasan artifisial | A/B |
| neural network | jaringan saraf tiruan | B |
| training / testing (data) | data latih / data uji | A |
| validation | validasi | A |
| overfitting / underfitting | kelewat pas / kurang pas | C |
| outlier | pencilan | A |
| missing value | nilai hilang, data hilang | A |
| imputation | imputasi | A |
| clustering | pengklasteran, penggerombolan | B |
| classification | klasifikasi | A |
| regression | regresi | A |
| variable | peubah, variabel | A (pilih satu, konsisten) |
| random variable | peubah acak | A |
| sampling | penarikan sampel, pencuplikan | A |
| sample / population | sampel / populasi | A |
| bias | bias | A |
| estimate / estimator | dugaan, penduga / estimasi, estimator | A (konsisten) |
| confidence interval | selang kepercayaan | A |
| credible interval | selang kredibel | B |
| prior / posterior | prior / posterior | C (istilah teknis; boleh tanpa padanan) |
| likelihood | kemungkinan, likelihood | C |
| p-value | nilai-p | A |
| hypothesis testing | pengujian hipotesis | A |
| benchmark | tolok ukur | A/B |
| baseline | garis dasar, acuan | B |
| pipeline | alur kerja, pipa data | B/C |
| preprocessing | prapemrosesan, praolah | B |
| feature (ML) | fitur, ciri | A |
| feature engineering | rekayasa fitur | B |
| hyperparameter | hiperparameter | A |
| tuning | penalaan | C |
| cross-validation | validasi silang | A |
| accuracy / precision / recall | akurasi / presisi / *recall* (perolehan) | A/A/C |
| dashboard | dasbor | B |
| server | peladen, server | C (peladen belum populer; *server* lazim) |
| cloud | komputasi awan | B |
| online / offline | daring / luring | A |
| download / upload | unduh / unggah | A |
| link | tautan, pranala | A (tautan) |
| browser | peramban | A |
| website | situs web, laman | A |
| email | surel, pos-el | B (surel) |
| software / hardware | perangkat lunak / perangkat keras | A |
| open source | sumber terbuka | A |
| repository | repositori | A |
| version control | kontrol versi | B |
| script | skrip | A |
| library / package (R, Python) | pustaka / paket | A |
| function | fungsi | A |
| output / input | luaran, keluaran / masukan | A |
| workflow | alur kerja | A |
| deadline | tenggat | A |
| stakeholder | pemangku kepentingan | A |
| survey | survei | A |
| questionnaire | kuesioner | A |
| respondent | responden | A |
| enumerator | pencacah, petugas lapangan | A |
| small area estimation | pendugaan area kecil | A/B |
| proxy | proksi | A |
| scoring | penskoran | A |
| ranking | pemeringkatan, peringkat | A |
| podcast | siniar | C |
| webinar | webinar, seminar web | A |
| marketplace | lokapasar | C |
| e-commerce | niaga elektronik, niaga-el | B |
| startup | perusahaan rintisan | B |
| fintech | tekfin, teknologi finansial | B |
| gadget | gawai | A |
| smartphone | ponsel pintar, gawai | A |
| selfie | swafoto | A |
| netizen | warganet | A |
| hoax | hoaks | A |
| viral | viral | A |
| update | pemutakhiran, memperbarui | A |
| upgrade | peningkatan, memperbarui | A |
| backup | cadangan, pencadangan | A |
| default | bawaan, baku | A |
| bug | kutu, galat program | C (bug lazim) |
| error | galat | A (statistika) |
| debugging | pengawakutuan | C |
| template | templat | A |
| brainstorming | curah pendapat | A |
| feedback | umpan balik | A |
| follow up | tindak lanjut | A |
| meeting | rapat, pertemuan | A |
| briefing | taklimat, pengarahan | A/B |
| review | tinjauan, ulasan, telaah | A |
| reviewer | penelaah, peninjau, mitra bestari (jurnal) | A |
| peer review | penelaahan sejawat | A |
| plagiarism | plagiarisme, plagiat | A |
| draft | draf | A |
| proofreading | penyuntingan naskah, pembacaan pruf | A |
| editing | penyuntingan | A |
| efficient / effective | sangkil, mangkus / efisien, efektif | A (efisien, efektif); *sangkil/mangkus* Kelas C |
| trend | tren | A |
| insight | wawasan, gagasan, pemahaman | A |
| impact | dampak | A |
| framework | kerangka kerja | A |
| roadmap | peta jalan | A |
| milestone | tonggak capaian | A |
| capacity building | peningkatan kapasitas | A |
| assessment | asesmen, penilaian | A |
| accreditation | akreditasi | A |
| tracer study | studi penelusuran (lulusan) | B |
| learning outcome | capaian pembelajaran | A |
| syllabus | silabus | A |
| lecture / lecturer | kuliah / dosen | A |

## Prosedur saat menemui istilah yang tidak ada di tabel
1. Cek KBBI daring (kbbi.kemdikbud.go.id) dan Pasti/Glosarium Badan Bahasa jika ada akses web; jika tidak, gunakan pengetahuan dengan hati-hati dan tandai `[cek KBBI]` bila ragu.
2. Tentukan kelas berdasarkan pembaca: apakah pembaca bidang ini sudah biasa dengan padanannya?
3. Terapkan pola penyebutan pertama; catat di glosarium naskah.
4. Konsistenkan seluruh naskah (cari-ganti).
