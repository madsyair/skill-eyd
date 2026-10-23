#!/usr/bin/env python3
"""
penggal.py — pemenggalan kata bahasa Indonesia menurut EYD V (Bab II.C Pemenggalan Kata).

Pemakaian:
  python3 penggal.py berjalan makan+an per+ingat+an intro+speksi
  python3 penggal.py --tex ber+jalan makan+an          # keluaran \\hyphenation{...} untuk LaTeX
  python3 penggal.py --json kata1 kata2
  python3 penggal.py --berkas daftar.txt               # satu kata per baris

Penanda pada masukan (hanya untuk memberi tahu skrip; tidak ikut dicetak):
  +   batas morfem: awalan/akhiran/partikel/bentuk terikat/unsur gabungan
      (ber+jalan, makan+an, di+per+jual+beli+kan, pasca+sarjana, bio+grafi, apa+kah).
      JANGAN beri + bila bentuk dasar luluh (menutup, penyapu, mengunci): kaidah 2b
      menyuruh memenggalnya seperti kata dasar (me-nu-tup, pe-nya-pu, me-ngun-ci).
  .   paksa batas suku kata (ma.in, mu.se.um)
  _   larang pemenggalan di antara dua huruf (se_udati → monoftong eu; sa_udara → diftong au)

Yang dikerjakan skrip (kaidah EYD V):
  1a vokal berurutan dipenggal di antaranya   1b monoftong eu tidak dipenggal
  1c diftong ai, au, ei, oi tidak dipenggal   1d satu konsonan di antara vokal → sebelum konsonan
  1e dua konsonan → di antaranya               1f tiga konsonan atau lebih → sesudah konsonan pertama
  1g kh, ng, ny, sy tidak dipenggal            2a batas imbuhan (dari penanda +)
  2d tidak menyisakan satu huruf di awal/akhir baris   3 batas unsur gabungan (dari penanda +)
  5 singkatan/akronim huruf kapital, angka, dan lambang tidak dipenggal.
Yang TIDAK dapat diketahui skrip: batas morfem (pakai +), apakah ai/au/ei/oi/eu itu diftong
atau dua vokal (skrip menebak dan menandai [cek KBBI]), dan nama orang (kaidah 4: hanya di antara kata).
"""
import re, sys, json, argparse

VOKAL = set("aiueoéèê")
DIGRAF = ("kh", "ng", "ny", "sy")          # gabungan konsonan satu bunyi (1g)
DIFTONG = ("ai", "au", "ei", "oi")         # 1c
MONOFTONG = ("eu",)                        # 1b

def _satuan(seg):
    """Pecah segmen huruf menjadi satuan bunyi: digraf konsonan dihitung satu satuan."""
    out, i = [], 0
    while i < len(seg):
        if seg[i:i+2].lower() in DIGRAF:
            out.append(seg[i:i+2]); i += 2
        else:
            out.append(seg[i]); i += 1
    return out

def _vokal(u): return u.lower() in VOKAL

def _penggal_segmen(seg, catatan):
    """Kembalikan daftar suku untuk satu morfem (kata dasar) menurut kaidah 1a–1g.
    seg boleh memuat '.' (paksa batas) dan '_' (larang batas)."""
    # titik paksa: penggal tiap bagian sendiri-sendiri
    if "." in seg:
        hasil = []
        for bag in seg.split("."):
            if bag: hasil += _penggal_segmen(bag, catatan)
        return hasil
    larang = set()
    bersih = ""
    for ch in seg:
        if ch == "_": larang.add(len(bersih))      # larang batas sebelum huruf ke-n
        else: bersih += ch
    u = _satuan(bersih)
    # posisi huruf awal tiap satuan
    pos, p = [], 0
    for x in u: pos.append(p); p += len(x)
    vok = [i for i, x in enumerate(u) if _vokal(x)]
    if len(vok) <= 1: return [bersih]
    # inti suku = rentang [awal, akhir] satuan vokal; vokal berurutan digabung bila diftong/monoftong
    inti = []
    for i in vok:
        if inti and inti[-1][1] == i - 1 and inti[-1][0] == inti[-1][1]:
            a, b = inti[-1][1], i
            pas = (u[a] + u[b]).lower()
            unit = False
            if pos[b] in larang:
                unit = True
            elif pas in MONOFTONG:
                catatan.append(f"'{u[a]}{u[b]}' dianggap dua vokal (mu-se-um); bila monoftong eu (seu-da-ti), tulis e_u [cek KBBI]")
            elif pas in DIFTONG:
                akhir_kata = (b == len(u) - 1)
                ada_vokal_sebelum = any(j < a for j in vok)
                diikuti_suku_terbuka = (b + 2 < len(u) and not _vokal(u[b+1]) and any(j > b + 1 for j in vok))
                unit = (akhir_kata and ada_vokal_sebelum) or diikuti_suku_terbuka
                bentuk = "diftong" if unit else "dua vokal"
                catatan.append(f"'{u[a]}{u[b]}' ditebak {bentuk} [cek KBBI; paksa dengan . atau _]")
            if unit:
                inti[-1] = (a, b); continue
        inti.append((i, i))
    if len(inti) <= 1: return [bersih]
    batas = []  # indeks satuan tempat suku baru dimulai
    for (_, a), (b, _) in zip(inti, inti[1:]):
        n = b - a - 1  # jumlah satuan konsonan di antara dua inti
        if n == 0: batas.append(b)             # 1a
        elif n == 1: batas.append(a + 1)       # 1d
        else: batas.append(a + 2)              # 1e (dua) dan 1f (tiga atau lebih): sesudah konsonan pertama
    # buang batas yang dilarang
    batas = [i for i in batas if pos[i] not in larang]
    suku, mulai = [], 0
    for i in batas:
        suku.append("".join(u[mulai:i])); mulai = i
    suku.append("".join(u[mulai:]))
    return suku

def penggal(token):
    """Penggal satu token. Kembalikan dict: kata, penggalan (str dengan '-'), suku (list), catatan (list)."""
    catatan = []
    polos = re.sub(r"[+._]", "", token)
    # kaidah 5 dan lambang: singkatan kapital, mengandung angka, atau bukan huruf
    if re.search(r"\d", polos) or re.search(r"[^A-Za-zÀ-ÿ\-']", polos):
        return dict(kata=polos, penggalan=polos, suku=[polos], catatan=["mengandung angka/lambang: tidak dipenggal"])
    if len(polos) > 1 and polos.isupper():
        return dict(kata=polos, penggalan=polos, suku=[polos], catatan=["singkatan/akronim kapital: tidak dipenggal (kaidah 5)"])
    if re.search(r"[A-Z].*[A-Z]", polos) and not polos.isupper():
        catatan.append("campuran kapital (KTP-el, di-PHK?): bagian berhuruf kapital tidak dipenggal")
    komponen = token.split("-")  # tanda hubung yang sudah ada (kata ulang, non-Indonesia) = titik penggal
    hasil_komp = []
    for komp in komponen:
        if not komp: continue
        kp = re.sub(r"[+._]", "", komp)
        if len(kp) > 1 and kp.isupper():
            hasil_komp.append([kp]); continue
        morfem = [m for m in komp.split("+") if m]
        suku = []
        for m in morfem:
            suku += _penggal_segmen(m, catatan)
        # kaidah 2d: tidak menyisakan satu huruf di awal/akhir baris
        while len(suku) > 1 and len(suku[0]) < 2:
            suku[1] = suku[0] + suku[1]; suku.pop(0)
        while len(suku) > 1 and len(suku[-1]) < 2:
            suku[-2] = suku[-2] + suku[-1]; suku.pop()
        hasil_komp.append(suku)
    # petunjuk batas morfem bila tidak ada penanda +
    if "+" not in token and len(komponen) == 1:
        low = polos.lower()
        m = re.match(r"^(keber|keter|memper|diper|ber|ter|per|meng|peng)(?=[aiueo])", low)
        if m and len(low) - len(m.group(1)) >= 3:
            catatan.append(f"awalan {m.group(1)}- + bentuk dasar berawal vokal? Bila ya, tulis {m.group(1)}+{low[len(m.group(1)):]} "
                           f"(kaidah 2a); bila bentuk dasarnya luluh (me+ngukur dari kukur) atau ini kata dasar, biarkan")
        if len(low) >= 7 and re.search(r"[^aiueo]an$", low):
            catatan.append("akhiran -an pada bentuk dasar berakhir konsonan? Bila ya, tandai + (makan+an → ma-kan-an, bukan ma-ka-nan)")
        if re.match(r"^(me|di|ter|ber|pe)", low) and re.search(r"[^aiueo]i$", low) and len(low) >= 7:
            catatan.append("akhiran -i? Bila ya, tandai + (meng+akhir+i → meng-a-khiri, bukan meng-a-khi-ri)")
    penggalan = "-".join("-".join(s) for s in hasil_komp)
    semua = [x for s in hasil_komp for x in s]
    return dict(kata=polos, penggalan=penggalan, suku=semua, catatan=list(dict.fromkeys(catatan)))

# ---------- Validasi penggalan buatan orang (dipakai periksa.py) ----------
def nilai_penggalan(bagian_kiri, bagian_kanan):
    """Nilai satu titik penggal: kiri|kanan adalah potongan kata di akhir dan awal baris.
    Kembalikan daftar (tingkat, pesan). Hanya pelanggaran yang pasti → ERROR; dugaan → WARNING."""
    out = []
    kiri = re.sub(r"[^A-Za-zÀ-ÿ]", "", bagian_kiri)    # seluruh potongan di akhir baris
    kanan = re.sub(r"[^A-Za-zÀ-ÿ]", "", bagian_kanan)  # seluruh potongan di awal baris
    kata = kiri + kanan
    if not kiri or not kanan: return out
    if len(kata) > 1 and kiri.isupper() and kanan.isupper():
        out.append(("ERROR", f"singkatan/akronim '{kata}' tidak dipenggal (EYD V II.C.5)"))
        return out
    if len(kiri) < 2:
        out.append(("ERROR", f"'{kiri}-' menyisakan satu huruf di akhir baris (EYD V II.C.2d)"))
    if len(kanan) < 2:
        out.append(("ERROR", f"'-{kanan}' menyisakan satu huruf di awal baris (EYD V II.C.2d)"))
    sambung = (kiri[-1] + kanan[0]).lower()
    if sambung in DIGRAF:
        # n|g, k|h, n|y, s|y: hampir selalu salah (an-gin, pen-yakit), kecuali batas morfem sungguhan
        out.append(("WARNING", f"'{kiri}-{kanan}': gabungan huruf '{sambung}' melambangkan satu bunyi dan tidak dipenggal (II.C.1g), "
                               f"kecuali memang batas morfem"))
    if sambung in DIFTONG or sambung in MONOFTONG:
        out.append(("WARNING", f"'{kiri}-{kanan}': bila '{sambung}' diftong/monoftong, tidak boleh dipenggal (II.C.1b–c) [cek KBBI]"))
    return out

def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("kata", nargs="*")
    ap.add_argument("--berkas", help="berkas berisi satu kata per baris")
    ap.add_argument("--tex", action="store_true", help="cetak \\hyphenation{...} untuk preambel LaTeX")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    kata = list(a.kata)
    if a.berkas:
        kata += [w.strip() for w in open(a.berkas, encoding="utf8") if w.strip() and not w.startswith("#")]
    if not kata: ap.print_help(); sys.exit(0)
    hasil = [penggal(k) for k in kata]
    if a.json:
        print(json.dumps(hasil, ensure_ascii=False, indent=1)); return
    if a.tex:
        isi = [h["penggalan"] for h in hasil if "-" in h["penggalan"] and re.fullmatch(r"[a-z\-]+", h["penggalan"])]
        print("\\hyphenation{" + " ".join(isi) + "}")
        lain = [h["kata"] for h in hasil if h not in [x for x in hasil if x["penggalan"] in isi]]
        if lain: print("% tidak dimasukkan (kapital/tak terpenggal): " + ", ".join(lain), file=sys.stderr)
        return
    lebar = max(len(h["kata"]) for h in hasil)
    for h in hasil:
        print(f"{h['kata']:<{lebar}}  {h['penggalan']}")
        for c in h["catatan"]: print(f"{'':<{lebar}}    · {c}")

if __name__ == "__main__":
    main()
