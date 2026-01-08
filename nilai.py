from database import Database
from typing import List, Optional, Tuple

class Nilai:
    """Class untuk mengelola data nilai mahasiswa"""
    
    def __init__(self, nim: str, kode_mk: str, tugas: float = 0, uts: float = 0, uas: float = 0):
        self.nim = nim
        self.kode_mk = kode_mk
        self.tugas = tugas
        self.uts = uts
        self.uas = uas
        self.nilai_akhir = self.hitung_nilai_akhir()
        self.grade = self.hitung_grade()
        self.status = self.hitung_status()
        self.db = Database()
    
    def hitung_nilai_akhir(self) -> float:
        """Hitung nilai akhir dengan bobot: Tugas 30%, UTS 30%, UAS 40%"""
        return round((self.tugas * 0.3) + (self.uts * 0.3) + (self.uas * 0.4), 2)
    
    def hitung_grade(self) -> str:
        """Hitung grade berdasarkan nilai akhir"""
        if self.nilai_akhir >= 85:
            return 'A'
        elif self.nilai_akhir >= 80:
            return 'A-'
        elif self.nilai_akhir >= 75:
            return 'B+'
        elif self.nilai_akhir >= 70:
            return 'B'
        elif self.nilai_akhir >= 65:
            return 'B-'
        elif self.nilai_akhir >= 60:
            return 'C+'
        elif self.nilai_akhir >= 55:
            return 'C'
        elif self.nilai_akhir >= 50:
            return 'D'
        else:
            return 'E'
    
    def hitung_status(self) -> str:
        """Hitung status kelulusan (Lulus jika nilai >= 55)"""
        return "Lulus" if self.nilai_akhir >= 55 else "Tidak Lulus"
    
    def tambah(self) -> bool:
        """Menambah data nilai ke database"""
        query = """INSERT INTO nilai (nim, kode_mk, tugas, uts, uas, nilai_akhir, grade, status) 
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?)"""
        params = (self.nim, self.kode_mk, self.tugas, self.uts, self.uas, 
                  self.nilai_akhir, self.grade, self.status)
        return self.db.execute_query(query, params)
    
    def update(self) -> bool:
        """Update data nilai"""
        # Recalculate nilai akhir, grade, dan status
        self.nilai_akhir = self.hitung_nilai_akhir()
        self.grade = self.hitung_grade()
        self.status = self.hitung_status()
        
        query = """UPDATE nilai SET tugas=?, uts=?, uas=?, nilai_akhir=?, grade=?, status=? 
                   WHERE nim=? AND kode_mk=?"""
        params = (self.tugas, self.uts, self.uas, self.nilai_akhir, 
                  self.grade, self.status, self.nim, self.kode_mk)
        return self.db.execute_query(query, params)
    
    @staticmethod
    def hapus(nim: str, kode_mk: str) -> bool:
        """Hapus data nilai"""
        db = Database()
        query = "DELETE FROM nilai WHERE nim=? AND kode_mk=?"
        return db.execute_query(query, (nim, kode_mk))
    
    @staticmethod
    def get_by_nim_and_kode(nim: str, kode_mk: str) -> Optional['Nilai']:
        """Ambil data nilai berdasarkan NIM dan Kode MK"""
        db = Database()
        query = "SELECT nim, kode_mk, tugas, uts, uas FROM nilai WHERE nim=? AND kode_mk=?"
        result = db.fetch_one(query, (nim, kode_mk))
        
        if result:
            return Nilai(result[0], result[1], result[2], result[3], result[4])
        return None
    
    @staticmethod
    def get_by_nim(nim: str) -> List[tuple]:
        """Ambil semua nilai mahasiswa berdasarkan NIM"""
        db = Database()
        query = """
            SELECT n.nim, m.nama, n.kode_mk, mk.nama_mk, 
                   n.tugas, n.uts, n.uas, n.nilai_akhir, n.grade, n.status
            FROM nilai n
            JOIN mahasiswa m ON n.nim = m.nim
            JOIN mata_kuliah mk ON n.kode_mk = mk.kode_mk
            WHERE n.nim = ?
            ORDER BY n.kode_mk
        """
        return db.fetch_all(query, (nim,))
    
    @staticmethod
    def get_all() -> List[tuple]:
        """Ambil semua data nilai"""
        db = Database()
        query = """
            SELECT n.nim, m.nama, n.kode_mk, mk.nama_mk, 
                   n.tugas, n.uts, n.uas, n.nilai_akhir, n.grade, n.status
            FROM nilai n
            JOIN mahasiswa m ON n.nim = m.nim
            JOIN mata_kuliah mk ON n.kode_mk = mk.kode_mk
            ORDER BY n.nim, n.kode_mk
        """
        return db.fetch_all(query)
    
    @staticmethod
    def is_nilai_exists(nim: str, kode_mk: str) -> bool:
        """Cek apakah nilai sudah ada untuk mahasiswa dan mata kuliah tertentu"""
        db = Database()
        query = "SELECT id FROM nilai WHERE nim=? AND kode_mk=?"
        result = db.fetch_one(query, (nim, kode_mk))
        return result is not None
    
    @staticmethod
    def get_statistik_mahasiswa(nim: str) -> Tuple[float, int, int]:
        """Ambil statistik nilai mahasiswa: IPK, Total SKS, Jumlah MK Lulus"""
        db = Database()
        
        # Ambil nilai dan SKS
        query = """
            SELECT n.nilai_akhir, mk.sks, n.status
            FROM nilai n
            JOIN mata_kuliah mk ON n.kode_mk = mk.kode_mk
            WHERE n.nim = ?
        """
        results = db.fetch_all(query, (nim,))
        
        if not results:
            return 0.0, 0, 0
        
        total_bobot = 0
        total_sks = 0
        jumlah_lulus = 0
        
        for nilai_akhir, sks, status in results:
            # Konversi nilai ke bobot
            if nilai_akhir >= 85:
                bobot = 4.0
            elif nilai_akhir >= 80:
                bobot = 3.7
            elif nilai_akhir >= 75:
                bobot = 3.3
            elif nilai_akhir >= 70:
                bobot = 3.0
            elif nilai_akhir >= 65:
                bobot = 2.7
            elif nilai_akhir >= 60:
                bobot = 2.3
            elif nilai_akhir >= 55:
                bobot = 2.0
            elif nilai_akhir >= 50:
                bobot = 1.0
            else:
                bobot = 0.0
            
            total_bobot += bobot * sks
            total_sks += sks
            
            if status == "Lulus":
                jumlah_lulus += 1
        
        ipk = round(total_bobot / total_sks, 2) if total_sks > 0 else 0.0
        
        return ipk, total_sks, jumlah_lulus
    
    def __str__(self):
        return (f"Nilai(NIM: {self.nim}, Kode MK: {self.kode_mk}, "
                f"Tugas: {self.tugas}, UTS: {self.uts}, UAS: {self.uas}, "
                f"Nilai Akhir: {self.nilai_akhir}, Grade: {self.grade}, Status: {self.status})")