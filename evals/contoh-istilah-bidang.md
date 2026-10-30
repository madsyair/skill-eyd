# Contoh istilah bidang

Model dilatih dengan cross-validation sepuluh lipatan, lalu hiperparameter dipilih lewat proses penalaan. Model yang kelewat pas memberi galat latih kecil tetapi galat uji besar. Data juga mengandung derau sehingga kurva belajar tidak pernah mencapai nol. Estimasi bootstrap dibandingkan dengan holdout.

Kalimat berikut sudah benar. Model yang mengalami *overfitting* (kelewat pas) memberi galat latih kecil. Setiap *fold*-nya dipakai sekali sebagai data uji, dan galat *out-of-bag* dihitung dengan fungsi `bootstraps()` dari paket rsample. Uji Shapiro-Wilk tidak dimiringkan, dan singkatan MSE ditulis tegak.
