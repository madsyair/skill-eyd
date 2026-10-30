# Istilah Matematika, Statistika, dan *Machine Learning*

Berkas ini mengatur penulisan istilah teknis bidang matematika, statistika, sains data, dan *machine learning* (ML) dalam naskah berbahasa Indonesia. Aturannya lebih tegas daripada kebijakan umum di `istilah-dan-kbbi.md`: untuk istilah bidang, **tidak ada jalan tengah** berupa padanan yang belum dikenal pembaca. Istilah ditulis dalam bentuk yang benar-benar dipakai oleh komunitas bidangnya.

## 1. Aturan utama

1. **Padanan Indonesia sudah populer → pakai padanan Indonesia, tegak.** Ukurannya adalah pemakaian nyata di buku teks berbahasa Indonesia, jurnal nasional terakreditasi, publikasi resmi (mis. BPS), dan perkuliahan bidang itu. Contoh: *galat, varians, simpangan baku, selang kepercayaan, nilai-p, derajat bebas, regresi, validasi silang, data latih, data uji, hiperparameter, fitur, pencilan*.
2. **Padanan KBBI/Badan Bahasa ada tetapi belum populer → pakai istilah Inggris aslinya, bercetak miring.** Padanan KBBI boleh disebut sekali dalam kurung pada kemunculan pertama sebagai penjelasan, lalu istilah Inggris dipakai konsisten. Contoh: *overfitting* (kelewat pas), *tuning* (penalaan), *noise* (derau), *fold* (lipatan), *resampling* (penarikan sampel ulang), *bootstrap*, *holdout*, *learning curve* (kurva belajar).
3. **Tidak ada padanan sama sekali → pakai istilah Inggris, miring,** dan jelaskan maknanya dalam satu kalimat atau dalam petik tunggal saat pertama muncul: *out-of-bag* 'pengamatan yang tidak terambil ke sampel *bootstrap*'; *double descent*.
4. **Jangan mencipta padanan sendiri.** Bila istilah belum punya padanan yang lazim, pakai istilah Inggris. Terjemahan harfiah buatan penulis (*jendela geser* untuk *sliding window*, *ambang interpolasi* untuk *interpolation threshold*) menyulitkan pembaca mencari literatur.
5. **Ragu → istilah Inggris miring dengan padanan dalam kurung.** Pembaca bidang hampir selalu mengenali istilah Inggrisnya; kebalikannya belum tentu.
6. **Serapan yang sudah baku ditulis tegak dan tidak dianggap asing**: *algoritme, statistika, statistik, matriks, varians, estimasi, estimator, probabilitas, kalibrasi, optimisme, ekstrapolasi, iterasi, simulasi, parameter*. Tulis bentuk bakunya (*algoritme*, bukan *algoritma*; *hipotesis*, bukan *hipotesa*; *analisis*, bukan *analisa*).
7. **Konvensi lembaga atau naskah mengalahkan daftar bawaan**, asalkan konsisten. Catat setiap keputusan di glosarium naskah.

## 2. Satu konsep, satu istilah

- Setelah memilih bentuk (Indonesia atau Inggris), pakai bentuk itu di seluruh naskah, termasuk judul, keterangan gambar, tabel, dan latihan.
- Jangan berganti-ganti antara *fold* dan *lipatan*, atau antara *noise* dan *derau*, dalam satu naskah. Padanan dalam kurung pada kemunculan pertama bukan pergantian istilah.
- Pada naskah berbab, kemunculan pertama dihitung per naskah. Bab berikutnya boleh mengulang padanan dalam kurung bila bab itu dapat dibaca terpisah.

## 3. Cara menulis istilah Inggris dalam kalimat Indonesia

| Kasus | Kaidah | Contoh benar | Contoh salah |
|---|---|---|---|
| Istilah tunggal atau frasa | dicetak miring seluruhnya (EYD V, Huruf Miring, butir 3) | *cross-validation*, *grid search*, *random forest* | cross-validation, "grid search" |
| Frasa campuran | hanya unsur asingnya yang miring | galat *out-of-bag*, validasi silang *k-fold*, metode *grid search* | *galat out-of-bag* |
| Imbuhan atau partikel Indonesia | dirangkai dengan tanda hubung; hanya unsur asing yang miring (EYD V, Tanda Hubung, butir 7) | di-*tuning*, *bootstrap*-nya, *fold*-nya | dituning, tuningnya, *tuningnya* |
| Hibrida | hindari; susun ulang kalimat bila bisa | "proses *tuning*", "mengalami *overfitting*" | meng-*overfit*, ter-*overfitting* |
| Jamak | tulis bentuk tunggal; jamak dinyatakan kata bilangan atau konteks | sepuluh *fold*, beberapa *pipeline* | sepuluh *folds*, *pipelines* |
| Kata ulang | jangan mengulang istilah asing | setiap *fold*, semua *fold* | *fold*-*fold* |
| Singkatan | tegak, kepanjangan diberikan pada kemunculan pertama | *mean squared error* (MSE), *k-nearest neighbors* (k-NN), *area under the curve* (AUC) | *MSE*, mse |
| Nama diri, metode bernama orang, nama perangkat lunak | tegak, tidak diterjemahkan (EYD V, Huruf Miring, catatan a) | uji Shapiro-Wilk, metode Newton-Raphson, scikit-learn, tidymodels | *uji Shapiro-Wilk* |
| Nama fungsi, argumen, objek kode | format kode, tidak dimiringkan | `train_test_split()`, `strata = y` | *train_test_split* |
| Lambang matematika | format rumus, tidak dimiringkan sebagai istilah | $\mathrm{Err}_{\mathcal T}$, $k$ | |
| Judul dan subjudul | istilah asing tetap miring | ## Holdout berulang → ## *Holdout* berulang | |
| Petik | istilah asing tidak diapit petik; petik tunggal hanya untuk makna | *tie* 'jarak yang sama besar' | "tie" |

**Huruf kapital.** Istilah asing di tengah kalimat ditulis huruf kecil kecuali nama diri: *random forest*, bukan *Random Forest*; tetapi Bayes, Gauss, Monte Carlo tetap kapital (simulasi Monte Carlo, aturan Bayes).

**Istilah Indonesia dan Inggris dalam satu frasa.** Pilih salah satu sebagai inti frasa. Kata Indonesia di depan memberi konteks (*galat out-of-bag*, *data uji*), sedangkan istilah majemuk Inggris yang sudah satu konsep tidak dipecah (*k-fold cross-validation* atau validasi silang *k-fold*, bukan *k-fold* validasi silang).

## 4. Prosedur memutuskan satu istilah

1. **Nama diri?** Tegak, apa adanya.
2. **Sudah ada di glosarium naskah atau konvensi lembaga?** Ikuti.
3. **Serapan baku yang sudah lazim?** Tegak, bentuk baku KBBI.
4. **Ada padanan Indonesia?** Periksa pemakaiannya di tiga sumber: buku teks berbahasa Indonesia bidang itu, jurnal nasional, dan publikasi resmi. Bila dipakai luas, pakai padanan. Bila jarang atau hanya ada di kamus, pakai istilah Inggris miring dan padanan dalam kurung sekali.
5. **Tidak ada padanan?** Istilah Inggris miring dengan penjelasan makna.
6. **Catat keputusan** di glosarium naskah: istilah, bentuk yang dipakai, padanan untuk kurung, alasan.

Pemeriksa `periksa.py` kategori **A-bidang** memberi WARNING untuk (a) istilah bidang yang biasa ditulis dalam bahasa Inggris tetapi tidak dimiringkan, dan (b) padanan buatan yang belum populer yang dipakai sebagai istilah utama. Keduanya perlu ditinjau, bukan diganti otomatis.

## 5. Daftar bawaan untuk pembaca akademik Indonesia

Kolom **Bentuk** adalah pilihan bawaan. "Indonesia" berarti padanan dipakai tegak; "Inggris" berarti istilah Inggris miring, dengan padanan di kolom **Kurung** pada kemunculan pertama (kosong berarti tanpa padanan, cukup penjelasan makna).

### Matematika

| Konsep | Bentuk | Dipakai | Kurung |
|---|---|---|---|
| set | Indonesia | himpunan | |
| function / mapping | Indonesia | fungsi / pemetaan | |
| derivative, partial derivative | Indonesia | turunan, turunan parsial | |
| integral, limit | Indonesia | integral, limit | |
| matrix, transpose, inverse | Indonesia | matriks, transpos, invers | |
| eigenvalue, eigenvector | Indonesia | nilai eigen, vektor eigen | |
| trace | Inggris | *trace* | teras |
| rank (matrix) | Indonesia | pangkat (matriks) | |
| norm | Indonesia | norma | |
| gradient, Hessian | Indonesia | gradien, matriks Hessian | |
| convex | Indonesia | konveks | |
| theorem, lemma, corollary, proof | Indonesia | teorema, lema, akibat, bukti | |
| sequence, series | Indonesia | barisan, deret | |
| convergence | Indonesia | konvergensi | |
| indicator function | Indonesia | fungsi indikator | |
| closed form | Inggris | *closed form* | bentuk tertutup |

### Statistika

| Konsep | Bentuk | Dipakai | Kurung |
|---|---|---|---|
| error (model), standard error | Indonesia | galat, galat baku | |
| variance, covariance, correlation | Indonesia | varians, kovarians, korelasi | |
| standard deviation | Indonesia | simpangan baku | |
| expected value | Indonesia | nilai harapan | |
| estimator, estimate | Indonesia | estimator, estimasi (atau penduga, dugaan, sesuai lembaga) | |
| unbiased | Indonesia | tak bias | |
| confidence interval, p-value | Indonesia | selang kepercayaan, nilai-p | |
| degrees of freedom | Indonesia | derajat bebas | |
| hypothesis testing | Indonesia | uji hipotesis | |
| sampling, sample | Indonesia | penarikan sampel, sampel | |
| stratified, strata | Indonesia | terstratifikasi, strata | |
| outlier | Indonesia | pencilan | |
| residual | Indonesia | residual | |
| likelihood | Inggris | *likelihood* | kemungkinan |
| maximum likelihood estimation | Inggris | *maximum likelihood estimation* (MLE) | |
| prior, posterior | Inggris | *prior*, *posterior* | |
| credible interval | Indonesia | selang kredibel | |
| bootstrap | Inggris | *bootstrap* | |
| resampling | Inggris | *resampling* | penarikan sampel ulang |
| noise | Inggris | *noise* | derau |
| coverage (interval) | Inggris | *coverage* | cakupan |
| goodness of fit | Inggris | *goodness of fit* | kebaikan suai |
| tie | Inggris | *tie* | ikatan |
| fixed design | Inggris | *fixed design* | desain tetap |
| hat matrix | Inggris | *hat matrix* | matriks topi |
| smoother, linear smoother | Inggris | *smoother*, *linear smoother* | penghalus |
| Monte Carlo simulation | Indonesia | simulasi Monte Carlo | |
| mixture model | Inggris | *mixture model* | model campuran hingga |
| mixed model | Indonesia | model efek campuran | |

### *Machine learning* dan evaluasi model

| Konsep | Bentuk | Dipakai | Kurung |
|---|---|---|---|
| machine learning, deep learning | Inggris | *machine learning*, *deep learning* | pemelajaran mesin, pemelajaran mendalam |
| training set, validation set, test set | Indonesia | data latih, data validasi, data uji | |
| training error, test error, generalization error | Indonesia | galat latih, galat uji, galat generalisasi | |
| cross-validation, nested cross-validation | Indonesia | validasi silang, validasi silang bersarang | |
| fold | Inggris | *fold* | lipatan |
| holdout, repeated holdout | Inggris | *holdout*, *holdout* berulang | |
| three-way split | Inggris | *three-way split* | pembagian tiga arah |
| leave-one-out | Inggris | *leave-one-out* (LOO) | |
| out-of-bag | Inggris | *out-of-bag* | |
| overfitting, underfitting | Inggris | *overfitting*, *underfitting* | kelewat pas, kurang pas |
| bias–variance trade-off | Inggris | *bias–variance trade-off* | tarik-ulur bias–varians |
| bias–variance decomposition | Indonesia | dekomposisi bias–varians | |
| hyperparameter, tuning | campuran | hiperparameter, *tuning* | penalaan |
| grid search, random search | Inggris | *grid search*, *random search* | |
| feature, feature selection | Indonesia | fitur, seleksi fitur | |
| feature engineering | Inggris | *feature engineering* | rekayasa fitur |
| preprocessing | Indonesia | prapemrosesan | |
| pipeline, workflow (objek perangkat lunak) | Inggris | *pipeline*, *workflow* | |
| data leakage | Indonesia | kebocoran data | |
| learning curve | Inggris | *learning curve* | kurva belajar |
| loss function | Indonesia | fungsi kerugian | |
| learning rate, early stopping, epoch, batch | Inggris | *learning rate*, *early stopping*, *epoch*, *batch* | |
| k-nearest neighbors | Inggris | *k-nearest neighbors* (k-NN) | |
| random forest, gradient boosting, support vector machine | Inggris | *random forest*, *gradient boosting*, *support vector machine* (SVM) | |
| neural network | Inggris | *neural network* | jaringan saraf tiruan |
| clustering | Inggris | *clustering* | pengklasteran |
| class imbalance | Indonesia | ketidakseimbangan kelas | |
| precision, recall | campuran | presisi, *recall* | perolehan |
| calibration | Indonesia | kalibrasi | |
| in-sample error, extra-sample error | Inggris | *in-sample error*, *extra-sample error* | |
| apparent error rate | Inggris | *apparent error rate* | |
| double descent, interpolation threshold | Inggris | *double descent*, *interpolation threshold* | |
| deployment | Inggris | *deployment* | |
| refit | Indonesia | pelatihan ulang | |
| embedding, dropout | Inggris | *embedding*, *dropout* | |

Daftar ini bawaan, bukan putusan Badan Bahasa. Untuk pembaca populer, sebagian istilah Indonesia dapat dipilih lebih sering; untuk pembaca peneliti, istilah Inggris lebih aman.
