from database import Database
from typing import List, Optional

class Mahasiswa:
    """Class untuk mengelola data mahasiswa"""
    
    def __init__(self, nim: str, nama: str, jurusan: str, angkatan: int):
        self.nim = nim
        self.nama = nama
        self.jurusan = jurusan
        self.angkatan = angkatan
        self.db = Database()
    
    def tambah(self) -> bool:
        """Menambah data mahasiswa ke database"""
        query = "INSERT INTO mahasiswa (nim, nama, jurusan, angkatan) VALUES (?, ?, ?, ?)"
        return self.db.execute_query(query, (self.nim, self.nama, self.jurusan, self.angkatan))
    
    def update(self) -> bool:
        """Update data mahasiswa"""
        query = "UPDATE mahasiswa SET nama=?, jurusan=?, angkatan=? WHERE nim=?"
        return self.db.execute_query(query, (self.nama, self.jurusan, self.angkatan, self.nim))
    
    @staticmethod
    def hapus(nim: str) -> bool:
        """Hapus data mahasiswa berdasarkan NIM"""
        db = Database()
        query = "DELETE FROM mahasiswa WHERE nim=?"
        return db.execute_query(query, (nim,))
    
    @staticmethod
    def cari_by_nim(nim: str) -> Optional['Mahasiswa']:
        """Cari mahasiswa berdasarkan NIM"""
        db = Database()
        query = "SELECT * FROM mahasiswa WHERE nim=?"
        result = db.fetch_one(query, (nim,))
        
        if result:
            return Mahasiswa(result[0], result[1], result[2], result[3])
        return None
    
    @staticmethod
    def cari_by_nama(nama: str) -> List[tuple]:
        """Cari mahasiswa berdasarkan nama (pencarian partial)"""
        db = Database()
        query = "SELECT * FROM mahasiswa WHERE nama LIKE ?"
        return db.fetch_all(query, (f"%{nama}%",))
    
    @staticmethod
    def get_all() -> List[tuple]:
        """Ambil semua data mahasiswa"""
        db = Database()
        query = "SELECT * FROM mahasiswa ORDER BY nim"
        return db.fetch_all(query)
    
    @staticmethod
    def is_nim_exists(nim: str) -> bool:
        """Cek apakah NIM sudah ada di database"""
        db = Database()
        query = "SELECT nim FROM mahasiswa WHERE nim=?"
        result = db.fetch_one(query, (nim,))
        return result is not None
    
    def __str__(self):
        return f"Mahasiswa(NIM: {self.nim}, Nama: {self.nama}, Jurusan: {self.jurusan}, Angkatan: {self.angkatan})"