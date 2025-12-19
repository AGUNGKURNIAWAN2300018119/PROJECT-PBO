from data import tambah_mahasiswa, tampilkan_mahasiswa, cari_mahasiswa, hapus_mahasiswa
from laporan import cetak_laporan

# === STRUKTUR KONTROL ===
def menu():
    while True:   # perulangan agar program terus berjalan
        print("1. Tambah")
        print("2. Tampil")
        print("3. Cari")
        print("4. Hapus")
        print("5. Laporan")
        print("6. Keluar")

        pilih = input("Pilih: ")

        if pilih == "1":
            tambah_mahasiswa()
        elif pilih == "2":
            tampilkan_mahasiswa()
        elif pilih == "3":
            cari_mahasiswa()
        elif pilih == "4":
            hapus_mahasiswa()
        elif pilih == "5":
            cetak_laporan()
        elif pilih == "6":
            break


menu()  
