# === OOP & ENKAPSULASI ===
# Class digunakan untuk merepresentasikan objek Mahasiswa

class Mahasiswa:
    def __init__(self, nim, nama, mata_kuliah, tugas, uts, uas):
        # Enkapsulasi: data mahasiswa disimpan dalam satu objek
        self.nim = nim              
        self.nama = nama            
        self.mata_kuliah = mata_kuliah
        self.tugas = tugas
        self.uts = uts
        self.uas = uas

        # Nilai ini dihitung di file lain (abstraksi)
        self.nilai_akhir = 0
        self.status = ""
