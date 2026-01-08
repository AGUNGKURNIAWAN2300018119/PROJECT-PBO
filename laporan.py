from datetime import datetime
from mahasiswa import Mahasiswa
from nilai import Nilai
from typing import Optional

class Laporan:
    """Class untuk generate laporan nilai mahasiswa"""
    
    @staticmethod
    def cetak_laporan_mahasiswa(nim: str) -> Optional[str]:
        """Generate laporan nilai untuk satu mahasiswa"""
        # Cari data mahasiswa
        mhs = Mahasiswa.cari_by_nim(nim)
        if not mhs:
            return None
        
        # Ambil nilai mahasiswa
        nilai_list = Nilai.get_by_nim(nim)
        
        # Ambil statistik
        ipk, total_sks, jumlah_lulus = Nilai.get_statistik_mahasiswa(nim)
        
        # Generate laporan
        laporan = []
        laporan.append("=" * 80)
        laporan.append("LAPORAN NILAI MAHASISWA".center(80))
        laporan.append("=" * 80)
        laporan.append(f"Tanggal Cetak: {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}")
        laporan.append("")
        laporan.append("DATA MAHASISWA")
        laporan.append("-" * 80)
        laporan.append(f"NIM        : {mhs.nim}")
        laporan.append(f"Nama       : {mhs.nama}")
        laporan.append(f"Jurusan    : {mhs.jurusan}")
        laporan.append(f"Angkatan   : {mhs.angkatan}")
        laporan.append("")
        laporan.append("DAFTAR NILAI")
        laporan.append("-" * 80)
        
        if nilai_list:
            # Header tabel
            laporan.append(f"{'Kode MK':<12} {'Nama Mata Kuliah':<25} {'Tugas':>8} {'UTS':>8} {'UAS':>8} {'N.Akhir':>8} {'Grade':>6} {'Status':<12}")
            laporan.append("-" * 80)
            
            # Data nilai
            for data in nilai_list:
                nim, nama, kode_mk, nama_mk, tugas, uts, uas, nilai_akhir, grade, status = data
                laporan.append(f"{kode_mk:<12} {nama_mk:<25} {tugas:>8.2f} {uts:>8.2f} {uas:>8.2f} {nilai_akhir:>8.2f} {grade:>6} {status:<12}")
        else:
            laporan.append("Tidak ada data nilai.")
        
        laporan.append("-" * 80)
        laporan.append("")
        laporan.append("STATISTIK")
        laporan.append("-" * 80)
        laporan.append(f"IPK                : {ipk:.2f}")
        laporan.append(f"Total SKS          : {total_sks}")
        laporan.append(f"Mata Kuliah Lulus  : {jumlah_lulus}")
        laporan.append("=" * 80)
        
        return "\n".join(laporan)
    
    @staticmethod
    def cetak_laporan_semua() -> str:
        """Generate laporan nilai untuk semua mahasiswa"""
        mahasiswa_list = Mahasiswa.get_all()
        
        laporan = []
        laporan.append("=" * 100)
        laporan.append("LAPORAN NILAI SEMUA MAHASISWA".center(100))
        laporan.append("=" * 100)
        laporan.append(f"Tanggal Cetak: {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}")
        laporan.append("")
        
        if mahasiswa_list:
            # Header tabel
            laporan.append(f"{'NIM':<15} {'Nama':<25} {'Jurusan':<20} {'IPK':>8} {'Total SKS':>10} {'MK Lulus':>10}")
            laporan.append("-" * 100)
            
            # Data per mahasiswa
            for mhs_data in mahasiswa_list:
                nim, nama, jurusan, angkatan = mhs_data
                ipk, total_sks, jumlah_lulus = Nilai.get_statistik_mahasiswa(nim)
                laporan.append(f"{nim:<15} {nama:<25} {jurusan:<20} {ipk:>8.2f} {total_sks:>10} {jumlah_lulus:>10}")
        else:
            laporan.append("Tidak ada data mahasiswa.")
        
        laporan.append("=" * 100)
        
        return "\n".join(laporan)
    
    @staticmethod
    def simpan_laporan(nim: str, filename: str = None) -> bool:
        """Simpan laporan ke file"""
        try:
            laporan = Laporan.cetak_laporan_mahasiswa(nim)
            if not laporan:
                return False
            
            if not filename:
                filename = f"laporan_{nim}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(laporan)
            
            return True
        except Exception as e:
            print(f"Error saving report: {e}")
            return False
    
    @staticmethod
    def simpan_laporan_semua(filename: str = None) -> bool:
        """Simpan laporan semua mahasiswa ke file"""
        try:
            laporan = Laporan.cetak_laporan_semua()
            
            if not filename:
                filename = f"laporan_semua_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(laporan)
            
            return True
        except Exception as e:
            print(f"Error saving report: {e}")
            return False