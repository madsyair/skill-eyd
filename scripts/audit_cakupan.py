#!/usr/bin/env python3
"""audit_cakupan.py — memeriksa apakah setiap butir kaidah EYD V sudah dipetakan di skill.

Harness untuk merawat skill ini (bukan untuk memeriksa naskah):
  1. Struktur: bab dan subbab di references/eyd-v-lengkap.md dibandingkan dengan daftar
     subbab resmi EYD V (situs ejaan.kemendikdasmen.go.id). Subbab yang hilang = ERROR.
  2. Jumlah butir: untuk subbab yang jumlah butirnya sudah dicocokkan dengan situs resmi,
     selisih jumlah = ERROR.
  3. Cakupan: setiap butir (mis. I.F.3, II.B.1c, III.E.6) harus ada di tabel
     references/peta-cakupan-eyd.md dengan status ✓ (dicakup), ◐ (sebagian), atau ✗ (belum).
     Butir tanpa baris = ERROR; status ✗ = WARNING; status ◐ dilaporkan.
  4. Rujukan: setiap berkas yang disebut di kolom "Di skill" harus ada.

Pemakaian:
  python3 scripts/audit_cakupan.py            # laporan ringkas
  python3 scripts/audit_cakupan.py --rinci    # tampilkan semua butir ◐/✗
  python3 scripts/audit_cakupan.py --daftar   # cetak semua ID butir dari teks resmi
Kode keluar 1 jika ada ERROR.
"""
import os, re, sys, argparse
from collections import Counter, OrderedDict

AKAR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LENGKAP = os.path.join(AKAR, "references", "eyd-v-lengkap.md")
PETA = os.path.join(AKAR, "references", "peta-cakupan-eyd.md")

# Subbab resmi EYD V (dicocokkan dengan situs resmi, 10 November 2026)
SUBBAB_RESMI = OrderedDict([
    ("I",   "ABCDEFGH"),          # Huruf abjad ... huruf tebal
    ("II",  "ABCDEFGHI"),         # Kata dasar ... kata sandang
    ("III", "ABCDEFGHIJKLMNO"),   # Titik ... apostrof
    ("IV",  "AB"),                # Serapan umum, serapan khusus
])
# Jumlah butir yang sudah dicocokkan satu per satu dengan situs resmi
JUMLAH_RESMI = {
    "I.F": 23,    # huruf kapital
    "II.B": 12,   # kata turunan: 1a–1e, 2a–2b, 3a–3e
    "II.C": 14,   # pemenggalan: 1a–1g, 2a–2d, 3, 4, 5
    "II.F": 9,    # singkatan: 1, 2, 3, 4a, 4b, 4c, 5, 6, 7
    "II.G": 13,   # angka: 1–7, 8a, 8b, 9–12
    "III.B": 14,  # koma
    "III.E": 9,   # tanda hubung
    "III.L": 4,   # tanda kurung
}

ROMAWI = {"I", "II", "III", "IV"}


def butir_resmi(path=LENGKAP):
    """Kembalikan OrderedDict id -> judul butir, serta dict subbab -> judul."""
    bab = None; sub = None; induk = None
    butir = OrderedDict(); subbab = OrderedDict()
    anak = Counter()
    for baris in open(path, encoding="utf8"):
        s = baris.rstrip("\n")
        m = re.match(r"^# (I|II|III|IV)\. (.+)$", s)
        if m and (m.group(1) in ROMAWI and (m.group(2).isupper() or m.group(1) == "IV" and "Serapan" in m.group(2) and not m.group(2).startswith(("Penulisan Unsur Serapan Umum", "Penulisan Unsur Serapan Khusus")))):
            bab = m.group(1); sub = None; induk = None
            continue
        m = re.match(r"^# ([A-O])\. (.+)$", s)
        if m and bab:
            sub = f"{bab}.{m.group(1)}"; induk = None
            subbab[sub] = m.group(2).strip()
            continue
        if not sub:
            continue
        m = re.match(r"^#### (\d+)\.?([a-g])? ?(.*)$", s)
        if m:
            no, huruf, judul = m.group(1), m.group(2), m.group(3).strip()
            induk = f"{sub}.{no}"
            butir[f"{induk}{huruf or ''}"] = judul
            continue
        m = re.match(r"^###### ([a-g])\. (.*)$", s)
        if m and induk:
            butir[f"{induk}{m.group(1)}"] = m.group(2).strip()
            anak[induk] += 1
    # induk yang punya anak (1. Kata Berimbuhan → 1a, 1b, ...) diwakili anaknya
    for i in list(anak):
        butir.pop(i, None)
    # subbab tanpa butir bernomor diwakili subbab itu sendiri
    for s, j in subbab.items():
        if not any(k.startswith(s + ".") for k in butir):
            butir[s] = j
    urut = OrderedDict(sorted(butir.items(), key=lambda kv: kunci(kv[0])))
    return urut, subbab


def kunci(i):
    bab, sub, *rest = i.split(".")
    no = rest[0] if rest else ""
    m = re.match(r"(\d*)([a-g]?)", no)
    return (["I", "II", "III", "IV"].index(bab), sub, int(m.group(1) or 0), m.group(2))


def uraikan_id(sel):
    """'II.C.1a-1g' → [II.C.1a, ..., II.C.1g]; 'IV.A.1-95' → 95 id; 'I.F.3' → [I.F.3]."""
    sel = sel.strip().strip("`").replace("–", "-")
    m = re.match(r"^(I|II|III|IV)\.([A-O])(?:\.(\d+)([a-g]?)(?:-(\d+)?([a-g]?))?)?$", sel)
    if not m:
        return []
    bab, sub, n1, h1, n2, h2 = m.groups()
    dasar = f"{bab}.{sub}"
    if n1 is None:
        return [dasar]
    if n2 is None and not h2:
        return [f"{dasar}.{n1}{h1}"]
    if h1 and h2 and (n2 is None or n2 == n1):
        return [f"{dasar}.{n1}{chr(c)}" for c in range(ord(h1), ord(h2) + 1)]
    return [f"{dasar}.{k}" for k in range(int(n1), int(n2) + 1)]


def baca_peta(path=PETA):
    peta = {}; rujukan = set(); dobel = []
    for no, baris in enumerate(open(path, encoding="utf8"), 1):
        if not baris.startswith("|") or baris.startswith("|---") or "Butir" in baris[:12]:
            continue
        kol = [k.strip() for k in baris.strip().strip("|").split("|")]
        if len(kol) < 4:
            continue
        ids = [x for bag in kol[0].split(",") for x in uraikan_id(bag)]
        status = kol[2][:1]
        for i in ids:
            if i in peta:
                dobel.append(i)
            peta[i] = dict(status=status, kaidah=kol[1], di_skill=kol[3], baris=no)
        for f in re.findall(r"`([\w./-]+\.(?:md|py))", kol[3]):
            rujukan.add(f)
    return peta, rujukan, dobel


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--rinci", action="store_true")
    ap.add_argument("--daftar", action="store_true")
    a = ap.parse_args()
    butir, subbab = butir_resmi()
    if a.daftar:
        for i, j in butir.items():
            print(f"{i:10s} {j[:90]}")
        return 0
    err = []; warn = []
    # 1. struktur
    for bab, huruf in SUBBAB_RESMI.items():
        for h in huruf:
            if f"{bab}.{h}" not in subbab:
                err.append(f"subbab resmi {bab}.{h} tidak ada di eyd-v-lengkap.md")
    for s in subbab:
        bab, h = s.split(".")
        if h not in SUBBAB_RESMI.get(bab, ""):
            warn.append(f"subbab {s} di eyd-v-lengkap.md tidak dikenal dalam daftar resmi")
    # 2. jumlah butir
    for s, n in JUMLAH_RESMI.items():
        ada = sum(1 for k in butir if k.startswith(s + "."))
        if ada != n:
            err.append(f"{s} ({subbab.get(s, '?')}): {ada} butir di salinan, {n} butir di situs resmi")
    # 3. cakupan
    peta, rujukan, dobel = baca_peta()
    for d in sorted(set(dobel), key=kunci):
        warn.append(f"{d} dipetakan lebih dari sekali")
    st = Counter()
    for i, j in butir.items():
        if i not in peta:
            err.append(f"{i} belum dipetakan: {j[:70]}")
            st["tanpa baris"] += 1
            continue
        s = peta[i]["status"]
        st[s] += 1
        if s == "✗":
            warn.append(f"{i} belum dicakup: {j[:70]}")
        elif s not in "✓◐":
            err.append(f"{i}: status '{s}' tidak dikenal (pakai ✓, ◐, ✗)")
    for i in peta:
        if i not in butir:
            warn.append(f"{i} ada di peta, tetapi tidak ada di teks resmi")
    # 4. rujukan berkas
    for f in sorted(rujukan):
        if not os.path.exists(os.path.join(AKAR, "references", f)) and not os.path.exists(os.path.join(AKAR, "scripts", f)) and not os.path.exists(os.path.join(AKAR, f)):
            err.append(f"rujukan berkas tidak ditemukan: {f}")
    total = len(butir)
    print(f"== audit_cakupan.py — {total} butir kaidah EYD V ==")
    print(f"✓ dicakup: {st['✓']}   ◐ sebagian: {st['◐']}   ✗ belum: {st['✗']}   tanpa baris: {st['tanpa baris']}")
    print(f"Cakupan penuh: {100 * st['✓'] / max(total, 1):.1f}%   penuh + sebagian: {100 * (st['✓'] + st['◐']) / max(total, 1):.1f}%")
    for bab in SUBBAB_RESMI:
        ids = [i for i in butir if i.split(".")[0] == bab]
        c = Counter(peta.get(i, {}).get("status", "-") for i in ids)
        print(f"  Bab {bab:3s}: {len(ids):3d} butir — ✓ {c['✓']}  ◐ {c['◐']}  ✗ {c['✗']}  tanpa baris {c['-']}")
    print(f"ERROR: {len(err)}   WARNING: {len(warn)}")
    for e in err:
        print(f"[ERROR  ] {e}")
    for w in warn:
        print(f"[WARNING] {w}")
    if a.rinci:
        for i, d in sorted(peta.items(), key=lambda kv: kunci(kv[0])):
            if d["status"] != "✓" and i in butir:
                print(f"[{d['status']}] {i}: {butir[i][:70]} — {d['di_skill']}")
    return 1 if err else 0


if __name__ == "__main__":
    sys.exit(main())
