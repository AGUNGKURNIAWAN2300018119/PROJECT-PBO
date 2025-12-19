# === ABSTRAKSI ===
# Detail perhitungan nilai disembunyikan dalam fungsi

def hitung_nilai_akhir(tugas, uts, uas):
    # Struktur kontrol: operasi matematika
    return (tugas * 0.3) + (uts * 0.3) + (uas * 0.4)


def status_kelulusan(nilai_akhir):
    # Struktur kontrol: percabangan
    if nilai_akhir >= 60:
        return "LULUS"
    else:
        return "TIDAK LULUS"
