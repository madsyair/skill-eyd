#!/usr/bin/env python3
"""
periksa.py — pemeriksa otomatis (harness) penulisan bahasa Indonesia sesuai EYD V.

Pemakaian:
  python3 periksa.py naskah.md                 # laporan ke layar
  python3 periksa.py naskah.md --json          # laporan JSON (untuk loop otomatis)
  python3 periksa.py naskah.md --fix keluar.md # terapkan perbaikan yang aman, simpan
  python3 periksa.py naskah.docx               # .docx dikonversi lewat pandoc bila ada
  python3 periksa.py naskah.tex                # LaTeX/Markdown diratakan: rumus → kata ganti, judul → §
  Baris yang memuat "→" atau "~~" dianggap catatan penyuntingan (contoh salah) dan dilewati.
  python3 periksa.py naskah.md --ragam populer # longgarkan aturan ragam cakapan

Kode keluar: 0 = tidak ada temuan ERROR, 1 = ada ERROR (WARNING tidak memengaruhi).
Temuan bukan vonis: pemeriksa tidak memahami konteks. Tinjau tiap temuan sebelum diterapkan.
"""
import re, sys, json, argparse, subprocess, os
from collections import Counter

# ---------- 1. Kamus kata tidak baku -> baku (aman untuk --fix) ----------
TIDAK_BAKU = {
 "aktifitas":"aktivitas","efektifitas":"efektivitas","produktifitas":"produktivitas","kreatifitas":"kreativitas",
 "komoditi":"komoditas","kwalitas":"kualitas","kwantitas":"kuantitas","kwitansi":"kuitansi","kwesioner":"kuesioner",
 "kuisioner":"kuesioner","frekwensi":"frekuensi","kwadrat":"kuadrat","analisa":"analisis","hipotesa":"hipotesis",
 "diagnosa":"diagnosis","sintesa":"sintesis","teoritis":"teoretis","praktek":"praktik","tehnik":"teknik","tekhnik":"teknik",
 "apotik":"apotek","atlit":"atlet","standarisasi":"standardisasi","sistim":"sistem","sistimatis":"sistematis",
 "obyek":"objek","subyek":"subjek","obyektif":"objektif","subyektif":"subjektif","komplek":"kompleks","ekstrim":"ekstrem",
 "elit":"elite","detil":"detail","trend":"tren","survey":"survei","resiko":"risiko","respon":"respons","karir":"karier",
 "esei":"esai","orisinil":"orisinal","otentik":"autentik","propinsi":"provinsi","pebruari":"Februari","nopember":"November",
 "jadual":"jadwal","jaman":"zaman","ijin":"izin","ijasah":"ijazah","azas":"asas","nasehat":"nasihat","hakekat":"hakikat",
 "faham":"paham","himbau":"imbau","menghimbau":"mengimbau","himbauan":"imbauan","handal":"andal","hutang":"utang",
 "hembus":"embus","hapal":"hafal","hadits":"hadis","adzan":"azan","sholat":"salat","ramadhan":"Ramadan","sekedar":"sekadar",
 "seksama":"saksama","silahkan":"silakan","terlanjur":"telanjur","terlantar":"telantar","nampak":"tampak","lembab":"lembap",
 "lobang":"lubang","mangkok":"mangkuk","coklat":"cokelat","cabe":"cabai","kedele":"kedelai","cengkeh":"cengkih",
 "nomer":"nomor","negri":"negeri","milyar":"miliar","trilyun":"triliun","jendral":"jenderal","sekertaris":"sekretaris",
 "konkrit":"konkret","aktip":"aktif","positip":"positif","negatip":"negatif","ustad":"ustaz","kuatir":"khawatir",
 "maghrib":"magrib","dzikir":"zikir","wudhu":"wudu","fardhu":"fardu","sorga":"surga","mesjid":"masjid","antri":"antre",
 "cidera":"cedera","cendikiawan":"cendekiawan","defenisi":"definisi","diskripsi":"deskripsi","faksimili":"faksimile",
 "hektar":"hektare","hirarki":"hierarki","intelejen":"intelijen","kharisma":"karisma","katagori":"kategori","komplit":"komplet",
 "konggres":"kongres","kwota":"kuota","managemen":"manajemen","manajement":"manajemen","metoda":"metode","musium":"museum",
 "notulen":"notula","panitya":"panitia","pinalti":"penalti","prosentase":"persentase","presentase":"persentase",
 "realita":"realitas","rejeki":"rezeki","standard":"standar","varitas":"varietas","photo":"foto","aktiv":"aktif",
 "dipungkiri":"dimungkiri","memungkiri":"memungkiri","mungkir":"mungkir","ekivalen":"ekuivalen","kompetensi":"kompetensi",
 # imbuhan (peluluhan)
 "mempengaruhi":"memengaruhi","dipengaruhi":"dipengaruhi","mentaati":"menaati","mensukseskan":"menyukseskan",
 "mentargetkan":"menargetkan","mensosialisasikan":"menyosialisasikan","mengkonsumsi":"mengonsumsi",
 "mengkoordinasi":"mengoordinasi","mengkoordinasikan":"mengoordinasikan","mengkonfirmasi":"mengonfirmasi",
 "mengkomunikasikan":"mengomunikasikan","mempesona":"memesona","memperdulikan":"memedulikan","mempedulikan":"memedulikan",
 "memparkir":"memarkir","mensurvei":"menyurvei","menyolok":"mencolok","mensortir":"menyortir","mempopulerkan":"memopulerkan",
 "mempublikasikan":"memublikasikan","mensubsidi":"menyubsidi","menterjemahkan":"menerjemahkan","mentertawakan":"menertawakan",
 "merubah":"mengubah","dirubah":"diubah","merubahnya":"mengubahnya","mentolerir":"menoleransi","memperbaharui":"memperbarui",
 "diperbaharui":"diperbarui","pembaharuan":"pembaruan","menyakinkan":"meyakinkan",
 # kata depan digabung
 "dimana":"di mana","disini":"di sini","disana":"di sana","diatas":"di atas","dibawah":"di bawah","didalam":"di dalam",
 "diluar":"di luar","diantara":"di antara","diantaranya":"di antaranya","disamping":"di samping","didepan":"di depan",
 "dibelakang":"di belakang","ditengah":"di tengah","disekitar":"di sekitar","diseluruh":"di seluruh","disetiap":"di setiap",
 "kesana":"ke sana","kesini":"ke sini","kemana":"ke mana","kedalam":"ke dalam","keatas":"ke atas","kebawah":"ke bawah",
 "dikarenakan":"karena",
 # gabungan kata
 "kerjasama":"kerja sama","tandatangan":"tanda tangan","tanggungjawab":"tanggung jawab","orangtua":"orang tua",
 "terimakasih":"terima kasih","sumberdaya":"sumber daya","budidaya":"budi daya","walikota":"wali kota","ibukota":"ibu kota",
 "sepakbola":"sepak bola","seringkali":"sering kali","acapkali":"acap kali","kadangkala":"kadang kala","ujicoba":"uji coba",
 "tatacara":"tata cara","tatakelola":"tata kelola","beritahu":"beri tahu","olah raga":"olahraga","mata hari":"matahari",
 "bea siswa":"beasiswa","dari pada":"daripada","suka rela":"sukarela","peri laku":"perilaku","sapu tangan":"saputangan",
 # partikel
 "apapun":"apa pun","siapapun":"siapa pun","kapanpun":"kapan pun","dimanapun":"di mana pun","walau pun":"walaupun",
 "meski pun":"meskipun","ada pun":"adapun","mau pun":"maupun","bagaimana pun":"bagaimanapun","biar pun":"biarpun",
 "kalau pun":"kalaupun","kendati pun":"kendatipun","atau pun":"ataupun","sungguh pun":"sungguhpun",
 # singkatan
 "s/d":"s.d.","a/n":"a.n.","u/p":"u.p.","d/a":"d.a.",
 # EYD V: maha + sifat/nama Tuhan ditulis terpisah
 "mahakuasa":"Maha Kuasa","mahaesa":"Maha Esa","mahasuci":"Maha Suci","mahapengasih":"Maha Pengasih",
 "mahapenyayang":"Maha Penyayang","mahatahu":"Maha Tahu","mahabijaksana":"Maha Bijaksana","mahaadil":"Maha Adil",
 "mahapengampun":"Maha Pengampun","mahapemurah":"Maha Pemurah",
 "undang-undang dasar":"Undang-Undang Dasar","alquran":"Al-Qur'an","al quran":"Al-Qur'an","al-quran":"Al-Qur'an",
}
BULAN_HARI=["januari","februari","maret","april","mei","juni","juli","agustus","september","oktober","november","desember",
            "senin","selasa","rabu","kamis","jumat","sabtu","minggu","idulfitri","iduladha","natal","nyepi","waisak","ramadan"]
BAHASA_BANGSA=["indonesia","inggris","jawa","sunda","arab","belanda","jepang","mandarin","melayu","bali","batak","bugis","minang","madura","prancis","jerman","korea","spanyol"]
# hapus entri yang tidak mengubah apa-apa (jaga-jaga)
TIDAK_BAKU = {k:v for k,v in TIDAK_BAKU.items() if k.lower()!=v.lower()}

RAGAM_CAKAPAN = {
 "tapi":"tetapi","nggak":"tidak","gak":"tidak","enggak":"tidak","ngga":"tidak","kayak":"seperti","banget":"sangat",
 "bilang":"mengatakan","gimana":"bagaimana","gitu":"begitu","gini":"begini","udah":"sudah","aja":"saja","emang":"memang",
 "doang":"saja","kalo":"kalau","ntar":"nanti","ngomong":"berbicara","ngasih":"memberi","nyari":"mencari","bikin":"membuat",
 "dapet":"mendapat","ketemu":"bertemu","ngerti":"mengerti","kayaknya":"tampaknya","makanya":"oleh karena itu",
 "soalnya":"karena","tau":"tahu","trus":"lalu","pake":"memakai","nanya":"bertanya","ngapain":"mengapa","oke":"baik",
 "sih":"","dong":"","deh":"","kok":"","lho":"","nih":"",
}

BENTUK_TERIKAT = ["antar","pasca","pra","sub","non","multi","ekstra","intra","inter","semi","tuna","swa","dwi","tri",
                  "purna","adi","nir","mono","poli","panca","anti","mikro","makro","bio","eko","sosio","tele","trans",
                  "ultra","super","hiper","infra","supra","kontra","maha"]

PLEONASME = [
 (r"\bagar supaya\b","agar / supaya (pilih satu)"),
 (r"\badalah merupakan\b","adalah / merupakan (pilih satu)"),
 (r"\bsangat \w+ sekali\b","sangat ... / ... sekali (pilih satu)"),
 (r"\bamat sangat\b","pilih satu"),
 (r"\bdemi untuk\b","untuk / demi"),
 (r"\bsejak dari\b","sejak"),
 (r"\bmulai sejak\b","sejak / mulai"),
 (r"\bseperti misalnya\b","seperti / misalnya"),
 (r"\bcontohnya seperti\b","contohnya / seperti"),
 (r"\bnaik ke atas\b","naik"),(r"\bturun ke bawah\b","turun"),(r"\bmaju ke depan\b","maju"),
 (r"\bmundur ke belakang\b","mundur"),(r"\bmasuk ke dalam\b","masuk ke / memasuki"),
 (r"\bpara hadirin\b","hadirin"),
 (r"\b(para|banyak|beberapa|semua|seluruh|sejumlah|berbagai)\s+(\w+)-\2\b","jamak sekali saja: \\1 \\2"),
 (r"\bsaling (\w+)-\1\b","saling \\1 / \\1-me\\1 (pilih satu)"),
 (r"\bdisebabkan karena\b","disebabkan oleh / karena"),
 (r"\bdikarenakan oleh\b","karena / disebabkan oleh"),
 (r"\bberbagai macam\b","berbagai / bermacam-macam"),
 (r"\bzaman dahulu kala\b","zaman dahulu / dahulu kala"),
 (r"\bkemudian setelah itu\b","kemudian / setelah itu"),
 (r"\blalu kemudian\b","lalu / kemudian"),
 (r"\bhanya (\w+ ){0,4}saja\b","hanya ... / ... saja (pilih satu)"),
 (r"\bsudah pernah\b","pernah"),(r"\bmasih belum\b","belum"),
 (r"\bakan tetapi namun\b","akan tetapi / namun"),
 (r"\bdapat mampu\b|\bmampu dapat\b","dapat / mampu"),
 (r"\blebih (\w+) dibandingkan daripada\b","lebih \\1 daripada / dibandingkan dengan"),
 (r"\bbahkan juga\b","bahkan / juga"),
 (r"\bmenyebabkan adanya\b","menyebabkan"),(r"\bterjadinya adanya\b","terjadinya"),
 (r"\bmelakukan (analisis|penelitian|pengujian|estimasi|evaluasi|pengamatan|perhitungan|pengukuran|penilaian|pemeriksaan|perbandingan|pengumpulan data|survei|observasi|wawancara|pengolahan)\b",
  "nominalisasi bertele-tele: menganalisis/meneliti/menguji/mengestimasi/... (jika cocok)"),
 (r"\bmemberikan (pengaruh|kontribusi|dampak|penjelasan|gambaran)\b","memengaruhi/berkontribusi/berdampak/menjelaskan/menggambarkan (jika cocok)"),
 (r"\bmemiliki (hubungan|perbedaan|kecenderungan|pengaruh)\b","berhubungan/berbeda/cenderung/berpengaruh (jika cocok)"),
 (r"\bdalam rangka\b","untuk (jika cocok)"),
 (r"\bsehubungan dengan hal tersebut\b","oleh karena itu"),
 (r"\btidak dapat dipungkiri bahwa\b|\bseperti (yang )?kita ketahui( bersama)?\b|\bperlu diketahui bahwa\b","kata pengantar hampa; pertimbangkan hapus"),
]

DIKSI = [
 (r"\bantara\b[^.,;:]{1,60}?\bdengan\b","antara ... dan (bukan 'dengan')","WARNING"),
 (r"\bterdiri dari\b","terdiri atas","ERROR"),
 (r"\btergantung (pada|kepada|dari)\b","bergantung pada","ERROR"),
 (r"\btergantung\b(?! (pada|kepada|dari))","bergantung (jika maksudnya 'depend'); 'tergantung' = digantung","WARNING"),
 (r"\bbaik\b[^.,;:]{1,60}?\bataupun\b","baik ... maupun","WARNING"),
 (r"\btidak\b[^.,;:]{1,40}?\bmelainkan\b","bukan ... melainkan / tidak ... tetapi","WARNING"),
 (r"\bjam (\d{1,2})[.:]\d{2}\b","pukul \\1.xx (jam = durasi)","ERROR"),
 (r"\bsesuatu (hal|masalah|metode|cara|model|pendekatan|faktor|kondisi)\b","suatu \\1","ERROR"),
 (r"\bmasing-masing (\w+)\b","setiap \\1 / \\1 masing-masing (masing-masing tidak diikuti nomina)","WARNING"),
 (r"\bdi tahun (\d{4})\b","pada tahun \\1","WARNING"),
 (r"\bdi (bulan|hari|abad|era|masa|saat|waktu)\b","pada \\1 (waktu memakai 'pada')","WARNING"),
 (r"\byang mana\b","hapus 'yang mana' (kalke 'which'); gunakan 'yang' atau ubah struktur","ERROR"),
 (r"\bdi mana\b(?![^.!?]*\?)","'di mana' sebagai penghubung relatif adalah kalke 'where'; ubah struktur (kecuali tanya/tempat)","WARNING"),
 (r"\bterkait (masalah|hal|isu|persoalan|kebijakan|rencana|program)\b","terkait dengan / mengenai \\1","WARNING"),
 (r"\bseputar\b","mengenai / tentang (ragam resmi)","WARNING"),
 (r"\bbertujuan untuk (mengetahui|melihat)\b","bertujuan mengetahui/menganalisis/mengukur (lebih tepat & hemat)","WARNING"),
 (r"\bhasil penelitian menyimpulkan\b","penelitian ini menyimpulkan / hasil penelitian menunjukkan","ERROR"),
 (r"\bwaktu dan tempat (kami|di)persilakan\b","Bapak/Ibu ... kami persilakan","ERROR"),
 (r"\bmempersingkat waktu\b","menghemat waktu","ERROR"),
 (r"\bdiupload\b|\bmengupload\b|\bdidownload\b|\bmendownload\b|\bdiinstall\b|\bmenginstall\b|\bdiprint\b|\bngeprint\b",
  "hibrida tidak baku: diunggah/mengunggah, diunduh/mengunduh, dipasang, dicetak","ERROR"),
 (r"\b(et al|dkk)\b(?!\.)","'et al.' (miring) / 'dkk.' dengan titik","ERROR"),
 (r"\bdi (upload|download|install|print|update|upgrade|share|submit|input|scan)\b","di-\\1 (dengan tanda hubung) atau lebih baik padanan: diunggah/diunduh/dipasang/dicetak/diperbarui/dibagikan/diajukan/dimasukkan/dipindai","ERROR"),
 (r"\b(pengaruh|hasil|dampak|tujuan|ketua|anggota|bagian|jumlah|manfaat|makna|arti|nilai|peran|fungsi|struktur|kualitas|tingkat|penyebab|akibat) dari\b","\\1 + nomina langsung (kalke 'of'), kecuali makna asal/sumber","WARNING"),
 (r"\bdipergunakan\b|\bmempergunakan\b","digunakan / menggunakan (lebih hemat)","WARNING"),
 (r"\bmengenai tentang\b|\btentang mengenai\b","mengenai / tentang (pilih satu)","ERROR"),
 # --- konjungsi (lihat kata-hubung.md) ---
 (r",\s*namun\b",", tetapi (namun = antarkalimat, dipakai di awal kalimat)","ERROR"),
 (r",\s*(akan tetapi|oleh karena itu|selain itu|dengan demikian|meskipun demikian)\b",", ... → konjungsi antarkalimat tidak dipakai di tengah kalimat; pecah kalimat atau ganti intrakalimat (tetapi/sehingga/dan)","WARNING"),
 (r"\bnamun demikian\b","Namun, / Meskipun demikian, (bentuk 'namun demikian' dipersoalkan)","WARNING"),
 (r"\bsehingga,","sehingga (tanpa koma sesudahnya)","ERROR"),
 (r"\bselain daripada itu\b","Selain itu","ERROR"),
 (r"\btidak hanya\b[^.;]{1,80}?\b(namun|melainkan) juga\b","tidak hanya ... tetapi juga","ERROR"),
 (r"\bbukan hanya\b[^.;]{1,80}?\btetapi juga\b","bukan hanya ... melainkan juga","ERROR"),
 (r"\bbukan\b[^.;,]{1,40}?, tetapi\b","bukan ... melainkan","WARNING"),
 (r"\bbaik\b[^.;]{1,60}?\b(dan|atau)\b(?![^.;]*\bmaupun\b)","baik ... maupun (jika korelatif)","WARNING"),
 (r"\bantara\b[^.;]{1,60}?\batau\b","antara ... dan","WARNING"),
 (r"\bsemakin\b[^.;]{1,40}?, maka semakin\b","semakin ..., semakin (tanpa maka)","ERROR"),
 (r"\b(oleh karena itu|dengan demikian|oleh sebab itu),?\s*maka\b","hapus 'maka' (ganda)","ERROR"),
 (r"\bdan lain sebagainya\b","dan sebagainya / dan lain-lain","ERROR"),
 (r"\bguna untuk\b","untuk / guna","ERROR"),
 (r"\badalah karena\b","'adalah' + 'karena' rancu: 'penyebabnya adalah X' atau 'hal ini terjadi karena X'","WARNING"),
 (r",\s*sementara itu\b",", sementara / , sedangkan ('sementara itu' = antarkalimat)","WARNING"),
 (r"\bmenurut [^,.]{2,60}? (mengatakan|menyatakan|menyebutkan|menjelaskan|berpendapat|mengemukakan)\b",
  "'Menurut X, ...' ATAU 'X mengatakan ...' (jangan keduanya)","ERROR"),
]

KONJ_ANTAR = ["Oleh karena itu","Oleh sebab itu","Namun","Akan tetapi","Selain itu","Di samping itu","Dengan demikian",
 "Jadi","Sebaliknya","Sementara itu","Meskipun demikian","Kendati demikian","Walaupun demikian","Di sisi lain","Lebih lanjut",
 "Selanjutnya","Akibatnya","Misalnya","Sebagai contoh","Pertama","Kedua","Ketiga","Keempat","Kelima","Terakhir","Dengan kata lain",
 "Singkatnya","Intinya","Secara keseluruhan","Sehubungan dengan itu","Berkaitan dengan itu","Lebih jauh","Bahkan","Karena itu",
 "Setelah itu","Kemudian","Sebelumnya","Pada akhirnya","Konsekuensinya","Sebagai akibatnya","Demikian pula","Sama halnya",
 "Serupa dengan itu","Terutama","Khususnya","Selain daripada itu"]
# Kata yang juga sah sebagai numeralia/subjek (Ketiga keluarga itu; Akibatnya tajam): hanya WARNING
KONJ_GANDA_FUNGSI={"Pertama","Kedua","Ketiga","Keempat","Kelima","Akibatnya","Konsekuensinya","Sebelumnya","Kemudian","Terakhir","Bahkan","Terutama","Khususnya","Misalnya"}
SISIPAN_KONJ=("lagi","pula","juga","sekali")

# ---------- 2. Alat bantu ----------
def ratakan_markup(teks, ext):
    """Ubah LaTeX/Markdown menjadi prosa polos. Rumus diganti kata ganti DI DALAM BARIS agar klausa
    sesudah rumus tampilan tetap satu kalimat dengan yang sebelumnya; spasi sebelum tanda baca dibersihkan."""
    if ext in (".tex",".ltx"):
        teks=re.sub(r"(?<!\\)%.*","",teks)
        if "\\begin{document}" in teks: teks=teks.split("\\begin{document}",1)[1]
        teks=teks.split("\\end{document}")[0]
        # rumus tampilan → kata ganti di dalam baris (gabungkan dengan baris sebelum/sesudah)
        teks=re.sub(r"\s*\\begin\{(equation|align|gather|multline|eqnarray|displaymath|flalign|alignat)\*?\}.*?\\end\{\1\*?\}\s*"," RUMUS ",teks,flags=re.S)
        teks=re.sub(r"\s*\\\[.*?\\\]\s*"," RUMUS ",teks,flags=re.S)
        teks=re.sub(r"\s*\$\$.*?\$\$\s*"," RUMUS ",teks,flags=re.S)
        teks=re.sub(r"\$[^$\n]+\$","SIMBOL",teks)
        # lingkungan non-prosa dibuang
        teks=re.sub(r"\\begin\{(figure|table|tabular|lstlisting|verbatim|algorithm|algorithmic|tikzpicture|thebibliography)\*?\}.*?\\end\{\1\*?\}","",teks,flags=re.S)
        teks=re.sub(r"\\(section|subsection|subsubsection|chapter|paragraph)\*?\{([^}]*)\}",r"\n§ \2\n",teks)
        teks=re.sub(r"\\(cite[tp]?|ref|eqref|label|autoref|cref|Cref|footnote|url|href)\*?(\[[^\]]*\])?\{[^}]*\}(\{[^}]*\})?","",teks)
        teks=re.sub(r"\\(emph|textit|textsl)\{([^}]*)\}",r"*\2*",teks)
        teks=re.sub(r"\\(textbf|texttt|textsc|underline|mbox|text)\{([^}]*)\}",r"\2",teks)
        teks=re.sub(r"\\item\s*","- ",teks)
        teks=re.sub(r"\\begin\{[^}]*\}(\[[^\]]*\])?|\\end\{[^}]*\}","",teks)
        teks=re.sub(r"\\[a-zA-Z]+\*?(\[[^\]]*\])?(\{[^}]*\})?","",teks)
        teks=teks.replace("~"," ").replace("\\\\","").replace("``",'"').replace("''",'"')
        teks=re.sub(r"[{}]","",teks)
    elif ext in (".md",".markdown"):
        teks=re.sub(r"\s*\$\$.*?\$\$\s*"," RUMUS ",teks,flags=re.S)
        teks=re.sub(r"\$[^$\n]+\$","SIMBOL",teks)
        teks=re.sub(r"`[^`\n]+`","KODE",teks)
        teks=re.sub(r"!\[[^\]]*\]\([^)]*\)","",teks)
        teks=re.sub(r"\[([^\]]+)\]\([^)]*\)",r"\1",teks)
    if ext in (".tex",".ltx"):
        # satu paragraf = satu baris (pemisah paragraf LaTeX adalah baris kosong); judul § tetap baris sendiri
        teks=re.sub(r"(?<!\n)\n(?!\n)(?!§)(?<!§)"," ",teks)
        teks=re.sub(r" +\n","\n",teks)
    teks=re.sub(r"[ \t]+([,.;:?!)])",r"\1",teks)   # spasi sebelum tanda baca akibat penggantian rumus
    teks=re.sub(r"[ \t]{2,}"," ",teks)
    return teks

def baca(path):
    ext=os.path.splitext(path)[1].lower()
    if ext in (".docx",".odt",".rtf",".html",".htm"):
        try:
            return subprocess.run(["pandoc",path,"-t","plain","--wrap=none"],capture_output=True,text=True,check=True).stdout
        except Exception as e:
            sys.exit(f"Gagal mengonversi {path} dengan pandoc: {e}")
    return ratakan_markup(open(path,encoding="utf8").read(),ext)

def kalimat_dari(teks):
    """Pisah kalimat kasar (abaikan singkatan umum)."""
    t=re.sub(r"\b(dll|dsb|dst|hlm|Yth|Bpk|Sdr|Dr|dr|Prof|Ir|No|Jl|Gd|Kec|Kel|Kab|Prov|a\.n|s\.d|u\.p|d\.a|et al|dkk|S\.ST|M\.Si|S\.Si|Ph\.D|M\.Sc|M\.A|S\.Kom|M\.Kom|M\.Stat|S\.Stat|S\.Tr\.Stat|M\.T|S\.T|S\.E|M\.M)\.", r"\1<TITIK>", teks)
    parts=re.split(r"(?<=[.!?])\s+(?=[A-Z\"“(])", t)
    return [p.replace("<TITIK>",".").strip() for p in parts if p.strip()]

def terlindung(baris):
    """Baris yang tidak perlu diperiksa: blok kode, URL, tabel, rumus, catatan penyuntingan (berisi → atau ~~)."""
    s=baris.strip()
    return s.startswith(("```","    ","$$","http","<","|---","---","![")) or "→" in s or "~~" in s

def judul(baris):
    """Judul/subjudul: bukan kalimat, aturan tingkat kalimat dilewati (ejaan tetap diperiksa)."""
    return baris.lstrip().startswith(("#","§"))

# ---------- 3. Pemeriksaan ----------
def periksa(teks, ragam="ilmiah"):
    temuan=[]  # dict(baris, kategori, tingkat, temuan, saran)
    def add(no,kat,tk,apa,saran): temuan.append(dict(baris=no,kategori=kat,tingkat=tk,temuan=apa,saran=saran))
    baris_list=teks.split("\n")
    dalam_kode=False
    for i,b in enumerate(baris_list,1):
        if b.strip().startswith("```"): dalam_kode=not dalam_kode; continue
        if dalam_kode or terlindung(b): continue
        # hapus kutipan miring/asing dari pemeriksaan kata baku? (istilah asing diizinkan) — tetap diperiksa, tetapi lewati URL & sitasi
        bb=re.sub(r"https?://\S+","",b)
        bb=re.sub(r"\([A-Z][^()]{0,60}\d{4}[^()]{0,20}\)","(SITASI)",bb)  # (Alwi, 2010)
        low=bb.lower()
        miring=[(m.start(),m.end()) for m in re.finditer(r"\*[^*\n]+\*|_[^_\n]+_",bb)]
        def dlm_miring(a,b2): return any(x<=a and b2<=y for x,y in miring)
        # E/I/D/G/P: kata tidak baku
        for salah,benar in TIDAK_BAKU.items():
            pola=r"(?<![\w-])"+re.escape(salah)+r"(?![\w-])"
            for m in re.finditer(pola,low):
                asli=bb[m.start():m.end()]
                sar=benar if asli[:1].islower() else benar[:1].upper()+benar[1:]
                if dlm_miring(m.start(),m.end()): add(i,"E-baku","WARNING",asli,sar+" — abaikan jika istilah asing/judul dalam teks miring")
                else: add(i,"E-baku","ERROR",asli,sar)
        # H: huruf kapital
        for nm in BULAN_HARI:
            for m in re.finditer(r"(?<![\w-])"+nm+r"(?![\w-])",bb):  # cocok hanya jika huruf kecil (bb asli)
                if nm=="minggu" and not re.search(r"\bhari minggu\b",low): continue  # 'minggu' = pekan sah
                add(i,"H-kapital","ERROR",m.group(),nm.capitalize()+" (nama bulan/hari/hari besar berhuruf kapital)")
        for nm in BAHASA_BANGSA:
            for m in re.finditer(r"\b(bahasa|bangsa|suku|orang|negara|pemerintah|republik|masyarakat|warga) "+nm+r"\b",bb):
                add(i,"H-kapital","ERROR",m.group(),m.group().split()[0]+" "+nm.capitalize())
        for m in re.finditer(r"\bUndang-undang\b|\bundang-undang (dasar|nomor|no\.)",bb):
            add(i,"H-kapital","ERROR",m.group(),"Undang-Undang (kedua unsur kapital pada nama resmi)")
        for m in re.finditer(r"\b(tuhan|allah)\b",bb):
            add(i,"H-kapital","ERROR",m.group(),m.group().capitalize())
        for m in re.finditer(r"\b(?:ibu|bapak|saudara) (kota|negara|pertiwi)\b",bb): pass
        # kata ulang dengan angka 2
        for m in re.finditer(r"\b([a-z]{3,})2\b",low): add(i,"G-ulang","ERROR",bb[m.start():m.end()],f"{m.group(1)}-{m.group(1)} (kata ulang pakai tanda hubung)")
        # D: bentuk terikat terpisah
        for bt in BENTUK_TERIKAT:
            for m in re.finditer(r"\b"+bt+r" ([a-z]{3,})\b",low):
                kata=m.group(1)
                if bt=="maha" and kata in ("esa","kuasa","suci","pengasih","penyayang","besar","tahu","bijaksana","adil","mulia","tinggi","agung","pemurah","pengampun","perkasa","melihat","mendengar"): continue
                if bt in ("anti","super","semi","inter","tele","trans","adi","tri","poli","mono","eko","bio","nir","sub","pra","non","multi","panca","dwi","swa","tuna","purna","kontra") and kata in ("dan","atau","yang","ini","itu","dari","untuk","adalah","juga","the","of"): continue
                if bt=="sub" and kata in ("total",): pass
                add(i,"D-terikat","WARNING",bb[m.start():m.end()],f"{bt}{kata} (bentuk terikat ditulis serangkai; abaikan bila '{bt}' kata bebas: 'pro dan kontra', 'super' nama merek)")
        # M: pleonasme
        for pola,saran in PLEONASME:
            for m in re.finditer(pola,low):
                add(i,"M-mubazir","WARNING",bb[m.start():m.end()],re.sub(r"\\(\d)",lambda g:m.group(int(g.group(1))) or "",saran) if "\\" in saran else saran)
        # L: diksi
        for pola,saran,tk in DIKSI:
            for m in re.finditer(pola,low):
                try: s=m.expand(saran) if "\\" in saran else saran
                except Exception: s=saran
                add(i,"L-diksi",tk,bb[m.start():m.end()],s)
        # R: ragam cakapan
        if ragam=="ilmiah":
            for salah,benar in RAGAM_CAKAPAN.items():
                for m in re.finditer(r"(?<![\w-])"+re.escape(salah)+r"(?![\w-])",low):
                    add(i,"R-ragam","ERROR",bb[m.start():m.end()],benar or "hapus (partikel cakapan)")
        # S/T: angka, singkatan, tanda baca
        for m in re.finditer(r"\bRp\s+\d",bb): add(i,"S-angka","ERROR",m.group(),"Rp tanpa spasi: Rp5.000")
        for m in re.finditer(r"\d\s+%",bb): add(i,"S-angka","ERROR",m.group(),"tanpa spasi: 5%")
        for m in re.finditer(r"\b\d{1,3},\d{3}\b(?!,\d)",bb): add(i,"S-angka","WARNING",m.group(),"pemisah ribuan pakai titik (10.000); koma untuk desimal")
        for m in re.finditer(r"\b\d+\.\d{1,2}\b(?!\.\d)",bb): add(i,"S-angka","WARNING",m.group(),"jika desimal → koma (3,5); jika pukul/nomor subbab abaikan")
        for m in re.finditer(r"\b(\d{4})\s?-\s?(\d{4})\b",bb): add(i,"T-pisah","WARNING",m.group(),f"rentang pakai tanda pisah: {m.group(1)}—{m.group(2)}")
        for m in re.finditer(r"\b(hlm\.|halaman|hal\.)\s*\d+\s?-\s?\d+",bb): add(i,"T-pisah","WARNING",m.group(),"rentang halaman pakai tanda pisah (–/—)")
        for m in re.finditer(r"\babad (\d{1,2})\b",bb): add(i,"S-angka","ERROR",m.group(),f"abad ke-{m.group(1)} / abad {m.group(1)} dalam angka Romawi")
        for m in re.finditer(r"\b(\d{4})an\b",bb): add(i,"S-angka","ERROR",m.group(),f"{m.group(1)}-an")
        for m in re.finditer(r"\bke (\d+)\b",bb): add(i,"S-angka","WARNING",m.group(),f"ke-{m.group(1)} jika bilangan bertingkat")
        for m in re.finditer(r"\b(dll|dsb|dst|hlm|yth|sdr|bpk|no|jl)\b(?!\.)",low):
            add(i,"S-singkatan","ERROR",bb[m.start():m.end()],bb[m.start():m.end()]+". (dengan titik)")
        for m in re.finditer(r"\bNIP\.",bb): add(i,"S-singkatan","ERROR",m.group(),"NIP (tanpa titik)")
        for m in re.finditer(r"\b(P\.T\.|C\.V\.)",bb): add(i,"S-singkatan","ERROR",m.group(),"PT / CV (tanpa titik)")
        for m in re.finditer(r"\s[,.;:?!]",bb):
            if not re.search(r"\d\s[.]",bb[max(0,m.start()-1):m.end()]): add(i,"T-spasi","ERROR",repr(m.group()),"tidak ada spasi sebelum tanda baca")
        for m in re.finditer(r"[,;:][A-Za-z]",bb): add(i,"T-spasi","ERROR",m.group(),"beri satu spasi setelah tanda baca")
        for m in re.finditer(r"\(\s|\s\)",bb): add(i,"T-spasi","ERROR",repr(m.group()),"tidak ada spasi di dalam kurung")
        if re.search(r"[^\s]  +[^\s]",bb): add(i,"T-spasi","WARNING","spasi ganda","satu spasi")
        for m in re.finditer(r"[?!]{2,}",bb): add(i,"T-baca","WARNING",m.group(),"satu tanda saja dalam ragam resmi")
        for m in re.finditer(r"\b(adalah|yaitu|yakni|meliputi|terdiri atas|antara lain|seperti|misalnya)\s*:",low):
            add(i,"T-titikdua","ERROR",bb[m.start():m.end()],"tanpa titik dua setelah kata ini")
        for m in re.finditer(r",\s*(bahwa)\b",low): add(i,"T-koma","ERROR",bb[m.start():m.end()],"tanpa koma sebelum 'bahwa'")
        for m in re.finditer(r"\b(\w+)\s+(tetapi|sedangkan|melainkan)\b",low):
            if m.group(1) not in ("akan",) and not bb[m.start():m.end()].startswith(","):
                # cek karakter sebelum konjungsi
                pre=low[:m.start(2)].rstrip()
                if not pre.endswith(","): add(i,"T-koma","ERROR",bb[m.start():m.end()],f"koma sebelum '{m.group(2)}'")
        for k in KONJ_ANTAR:
            for m in re.finditer(r"(^|(?<=[.!?]\s)|(?<=[.!?]\s\s))"+re.escape(k)+r"(?=\s[a-zA-Z\"“(])",bb):
                sisa=bb[m.end():].lstrip()
                kata1=sisa.split()[0] if sisa.split() else ""
                if kata1.rstrip(",") in SISIPAN_KONJ and kata1.endswith(","): continue   # "Lebih jauh lagi,"
                tk="WARNING" if k in KONJ_GANDA_FUNGSI else "ERROR"
                catatan=" (abaikan jika numeralia/subjek: 'Ketiga faktor itu', 'Akibatnya tajam')" if tk=="WARNING" else ""
                add(i,"T-koma",tk,m.group().strip(),f"'{k},' — koma setelah penghubung antarkalimat{catatan}")
        for m in re.finditer(r"\b(A|B|C|D|E)\b\s*,?\s*",bb): pass
        # T-daftar: "A, B dan C" tanpa koma sebelum dan
        for m in re.finditer(r"\b\w+, \w+(?: \w+)? (dan|atau|serta) \w+",low):
            seg=m.group()
            if re.search(r", \w+(?: \w+)? (dan|atau|serta)",seg) and not re.search(r", (dan|atau|serta)",seg):
                add(i,"T-koma","WARNING",bb[m.start():m.end()],"perincian ≥3 unsur: koma sebelum 'dan/atau' terakhir (A, B, dan C)")
        for m in re.finditer(r"\b(\d+) (kali|orang|responden|buah|unit|kabupaten|kota|provinsi|kecamatan|desa|peubah|variabel|model|tahap|faktor|kelompok|jenis)\b",bb):
            n=int(m.group(1))
            satu_kata={1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,100,1000,1000000}
            if n in satu_kata and not re.search(r"\d[.,]|\b(tabel|gambar|persamaan)\b",low[max(0,m.start()-25):m.start()]):
                add(i,"S-angka","WARNING",m.group(),"bilangan satu kata ditulis dengan huruf (tiga kali), kecuali dalam perincian/tabel")
    # K: pemeriksaan tingkat kalimat
    dalam_kode=False; no=0
    for i,b in enumerate(baris_list,1):
        if b.strip().startswith("```"): dalam_kode=not dalam_kode; continue
        if dalam_kode or terlindung(b) or judul(b) or not b.strip(): continue
        for no,kal in enumerate(kalimat_dari(b)):
            if kal.endswith("?"):  # kalimat tanya: 'Di mana ...?' sah, aturan pembuka dilewati
                continue
            kl=kal.lower(); kata=kal.split(); n=len(kata)
            if n>40: add(i,"K-panjang","WARNING",kal[:60]+"...",f"{n} kata; pecah kalimat")
            if re.match(r"^sementara (?!itu\b)",kl):
                add(i,"K-awal","WARNING",kal[:60],"'Sementara' = konjungsi waktu; untuk pertentangan antarkalimat pakai 'Sementara itu,' atau gabungkan dengan 'sedangkan'")
            if re.match(r"^yang (?!mana\b)",kl) and n>4:
                add(i,"K-awal","WARNING",kal[:60],"kalimat diawali 'Yang' sebagai penyambung; gabungkan dengan kalimat sebelumnya atau ulang nomina")
            if re.match(r"^(hal ini|hal tersebut|hal itu)\b",kl) and no==0:
                add(i,"K-acuan","WARNING",kal[:60],"'Hal ini' mengawali paragraf: pastikan acuannya jelas; lebih baik nomina eksplisit")
            if re.match(r"^(sehingga|sedangkan|tetapi|tapi|dan|dimana|di mana|yang mana|serta|atau|melainkan)\b",kl):
                add(i,"K-awal","ERROR",kal[:60],"konjungsi intrakalimat tidak mengawali kalimat; gabungkan atau ganti: Dengan demikian,/Sementara itu,/Namun,")
            if re.match(r"^(dalam|pada|di|bagi|untuk|menurut|berdasarkan|dari|mengenai|tentang|melalui|dengan|terhadap)\b",kl) and re.search(r"\b(menunjukkan|membahas|menjelaskan|menyatakan|mengatakan|menggambarkan|menghasilkan|menemukan|memaparkan|menguraikan|membuktikan|memperlihatkan|mengkaji|mengaji|meneliti|menganalisis|dibahas|dijelaskan|diketahui|diperoleh|dilakukan|dihasilkan)\b",kl):
                if not re.search(r"^(dalam|pada|di|bagi|untuk|menurut|berdasarkan|dari|mengenai|tentang|melalui|dengan|terhadap)\b[^,]{0,80},",kl):
                    add(i,"K-subjek","WARNING",kal[:70],"kemungkinan subjek berkata depan (subjek hilang): hapus kata depan di awal atau beri koma setelah keterangan")
            for a,c in [("meskipun|walaupun|kendati|sekalipun|biarpun|sungguhpun","tetapi|namun|tapi|akan tetapi"),
                        ("karena|oleh karena|berdasarkan|setelah|sesudah|jika|apabila|kalau|agar|supaya|dengan|untuk|mengingat|sehubungan","maka"),
                        ("setelah|sesudah","kemudian|lalu")]:
                if re.match(r"^("+a+r")\b",kl) and re.search(r",\s*("+c+r")\b",kl):
                    add(i,"K-konjganda","ERROR",kal[:70],"konjungsi ganda; hapus salah satu (dalam teks matematis 'jika–maka' boleh)")
            if re.match(r"^(karena|jika|apabila|meskipun|walaupun|agar|supaya|ketika|setelah|sebelum|sehingga|sedangkan|sementara)\b",kl) and "," not in kal and n<25:
                add(i,"K-buntung","WARNING",kal[:70],"kemungkinan anak kalimat tanpa induk; gabungkan dengan kalimat sekitar")
            for klausa in re.split(r"[;,]\s*(?:sedangkan|tetapi|melainkan|namun|dan|serta)\s+",kl):
                if "daripada" in klausa and not re.search(r"\b(lebih|kurang|dibanding|ketimbang|baik|buruk|besar|kecil|tinggi|rendah|banyak|sedikit|cepat|lambat)\b",klausa):
                    add(i,"L-diksi","WARNING",klausa[:60],"'daripada' hanya untuk perbandingan; untuk milik/asal hapus atau pakai 'dari'")
            if len(re.findall(r"\byang\b",kl))>=3: add(i,"K-yang","WARNING",kal[:60]+"...","'yang' ≥3 kali; pecah/ubah struktur")
            if len(re.findall(r"\btersebut\b",kl))>=2: add(i,"K-tersebut","WARNING",kal[:60]+"...","'tersebut' berulang; ganti dengan ini/itu atau hapus")
            if re.match(r"^\d",kal) and not re.match(r"^\d+([.)]|\s*[-–—])",kal):
                add(i,"S-angka","WARNING",kal[:40],"kalimat jangan diawali angka: 'Sebanyak 25 ...' atau ubah susunan")
    # Kepaduan: transisi berulang di awal paragraf & kalimat berturut-turut
    paras=[p for p in re.split(r"\n\s*\n",teks) if p.strip() and not terlindung(p) and not judul(p)]
    prev=None
    for idx,p in enumerate(paras,1):
        first=p.strip().split("\n")[0]
        m=re.match(r"^(Selain itu|Namun|Oleh karena itu|Di samping itu|Dengan demikian|Sementara itu|Selanjutnya|Selain daripada itu)\b",first)
        if m and prev==m.group(1):
            add(0,"P-kepaduan","WARNING",f"paragraf {idx}: '{m.group(1)}'","dua paragraf berturut-turut dibuka transisi yang sama; variasikan atau rangkai lewat kata kunci")
        prev=m.group(1) if m else None
        kal=kalimat_dari(p)
        if len(kal)==1 and len(p.split())>15: add(0,"P-kepaduan","WARNING",f"paragraf {idx}: satu kalimat","paragraf satu kalimat; kembangkan atau gabungkan")
        if len(p.split())>280: add(0,"P-kepaduan","WARNING",f"paragraf {idx}: {len(p.split())} kata","paragraf terlalu panjang; kemungkinan >1 gagasan → pecah")
        # transisi sama pada kalimat berturut-turut
        awal=[re.match(r"^(\w+( itu)?)",k.lower()).group(1) for k in kal if re.match(r"^(\w+( itu)?)",k.lower())]
        for a,b2 in zip(awal,awal[1:]):
            if a==b2 and a in ("selain itu","namun","oleh karena itu","dengan demikian","hal ini","penelitian ini","selanjutnya"):
                add(0,"P-kepaduan","WARNING",f"paragraf {idx}: kalimat berturut-turut diawali '{a}'","variasikan pembuka kalimat")
    # Istilah asing: konsistensi sederhana (dua varian dalam satu naskah)
    pasangan=[("dataset","gugus data"),("machine learning","pembelajaran mesin"),("big data","mahadata"),("outlier","pencilan"),
              ("variabel","peubah"),("error","galat"),("download","unduh"),("upload","unggah"),("online","daring"),("offline","luring"),
              ("stakeholder","pemangku kepentingan"),("deadline","tenggat"),("feedback","umpan balik"),("survey","survei"),("database","basis data")]
    low_all=teks.lower()
    for a,b2 in pasangan:  # pola "padanan (*asing*)" atau "*asing* (padanan)" pada penyebutan pertama sah
        low_all=re.sub(r"\b"+b2+r"\s*\(\*?"+a+r"\*?[^)]*\)","",low_all)
        low_all=re.sub(r"\*?\b"+a+r"\b\*?\s*\("+b2+r"[^)]*\)","",low_all)
        if re.search(r"\b"+a+r"\b",low_all) and re.search(r"\b"+b2+r"\b",low_all):
            add(0,"A-istilah","WARNING",f"'{a}' dan '{b2}' dipakai bergantian","satu konsep, satu istilah; pilih satu (lihat istilah-dan-kbbi.md)")
    return temuan

def perbaiki(teks):
    """Terapkan hanya penggantian yang aman (kata tidak baku, kata depan digabung, gabungan kata, partikel, singkatan)."""
    out=[]; dalam_kode=False; jumlah=Counter()
    for b in teks.split("\n"):
        if b.strip().startswith("```"): dalam_kode=not dalam_kode; out.append(b); continue
        if dalam_kode or terlindung(b): out.append(b); continue
        # pisahkan teks miring (*...* / _..._) agar istilah asing tidak ikut diganti
        segmen=re.split(r"(\*[^*\n]+\*|_[^_\n]+_)",b)
        for si,seg in enumerate(segmen):
            if si%2==1: continue
            for salah,benar in TIDAK_BAKU.items():
                def rep(m):
                    w=m.group(0); jumlah[salah]+=1
                    return benar[:1].upper()+benar[1:] if w[:1].isupper() else benar
                seg=re.sub(r"(?<![\w-])"+re.escape(salah)+r"(?![\w-])",rep,seg,flags=re.I)
            segmen[si]=seg
        b="".join(segmen)
        b=re.sub(r"\bRp\s+(\d)",r"Rp\1",b); b=re.sub(r"(\d)\s+%",r"\1%",b); b=re.sub(r"\b(\d{4})an\b",r"\1-an",b)
        b=re.sub(r"\bNIP\.",r"NIP",b)
        out.append(b)
    return "\n".join(out),jumlah

# ---------- 4. Laporan ----------
def main():
    ap=argparse.ArgumentParser(description=__doc__,formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("berkas"); ap.add_argument("--json",action="store_true"); ap.add_argument("--fix",metavar="KELUAR")
    ap.add_argument("--ragam",choices=["ilmiah","populer"],default="ilmiah")
    a=ap.parse_args()
    teks=baca(a.berkas)
    if a.fix:
        teks2,jml=perbaiki(teks); open(a.fix,"w",encoding="utf8").write(teks2)
        print(f"Perbaikan aman diterapkan: {sum(jml.values())} penggantian → {a.fix}")
        for k,v in jml.most_common(): print(f"  {k} → {TIDAK_BAKU.get(k,'')} ({v}x)")
        teks=teks2
    temuan=periksa(teks,a.ragam)
    temuan.sort(key=lambda t:(t["baris"],t["kategori"]))
    n_err=sum(1 for t in temuan if t["tingkat"]=="ERROR"); n_warn=len(temuan)-n_err
    kata=len(teks.split()); kal=sum(len(kalimat_dari(p)) for p in teks.split("\n") if p.strip())
    ringkas=dict(berkas=a.berkas,kata=kata,kalimat=kal,rata_kata_per_kalimat=round(kata/max(kal,1),1),error=n_err,warning=n_warn,
                 per_kategori=dict(Counter(t["kategori"] for t in temuan)))
    if a.json:
        print(json.dumps(dict(ringkasan=ringkas,temuan=temuan),ensure_ascii=False,indent=1)); sys.exit(1 if n_err else 0)
    print(f"== periksa.py — {a.berkas} ==\n{kata} kata, {kal} kalimat, rata-rata {ringkas['rata_kata_per_kalimat']} kata/kalimat")
    print(f"ERROR: {n_err}   WARNING: {n_warn}")
    for k,v in sorted(ringkas["per_kategori"].items()): print(f"  {k:14s} {v}")
    print()
    for t in temuan:
        print(f"[{t['tingkat']:7s}] baris {t['baris']:>4} {t['kategori']:12s} \"{t['temuan']}\" → {t['saran']}")
    if not temuan: print("Tidak ada temuan. Lanjutkan ke tinjauan manual (rubrik di SKILL.md).")
    sys.exit(1 if n_err else 0)

if __name__=="__main__": main()
