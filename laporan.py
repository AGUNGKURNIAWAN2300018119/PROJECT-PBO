from data import data_mahasiswa

# === MODULAR ===


def cetak_laporan():
    for mhs in data_mahasiswa:
        print(f"{mhs.nim} | {mhs.nama} | {mhs.nilai_akhir} | {mhs.status}")
