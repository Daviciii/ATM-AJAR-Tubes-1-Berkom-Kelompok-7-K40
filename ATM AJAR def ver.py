import random
import tkinter as tk
from datetime import datetime
from tkinter import messagebox

# Config & Data Utama
NAMA_BANK = "BANK AJAR"
MAKS_SALAH_PIN = 3
SALDO_MINIMAL = 50_000
BATAS_TARIK = 2_500_000
KELIPATAN_TARIK = 50_000
BIAYA_ANTARBANK = 6_500
BIAYA_ADMIN = 2_500

akun = {
    "nama": "BUDI SANTOSO",
    "no_rekening": "1234567890",
    "pin": "123456",
    "saldo": 5_000_000,
    "salah_pin": 0,
}

DAFTAR_BANK = ["BCA", "BNI", "BRI", "MANDIRI", "CIMB NIAGA", "PERMATA"]
NOMINAL_PULSA = [10_000, 25_000, 50_000, 100_000]
NOMINAL_TOKEN = [20_000, 50_000, 100_000, 200_000, 500_000]
E_WALLET = ["GOPAY", "OVO", "DANA", "SHOPEEPAY", "LINKAJA"]
NOMINAL_EWALLET = [20_000, 50_000, 100_000, 200_000]
DAFTAR_ASURANSI = ["AJAR Life", "Prudential", "Allianz", "AXA Mandiri"]

# Warna & font UI
WARNA_BG = "#0b2a4a"
WARNA_KARTU = "#ffffff"
WARNA_BIRU = "#1e6fd9"
WARNA_HIJAU = "#2e9d5b"
WARNA_MERAH = "#d64545"
WARNA_ABU = "#5c6b7a"
FONT = ("Arial", 12)
FONT_BOLD = ("Arial", 12, "bold")
FONT_JUDUL = ("Arial", 18, "bold")


# Helper functions
def rupiah(angka):
    return "Rp" + f"{angka:,}".replace(",", ".")


def tagihan_acak(rendah, tinggi):
    return random.randrange(rendah, tinggi, 100)


def kolom(label, panjang_min, panjang_maks=None, rahasia=False):
    return (label, panjang_min, panjang_maks or panjang_min, rahasia)


# App Main Class
class AplikasiATM(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(f"{NAMA_BANK} - Simulasi ATM")
        self.geometry("560x760")
        self.configure(bg=WARNA_BG)

        self.isi = tk.Frame(self, bg=WARNA_BG)
        self.isi.pack(fill="both", expand=True, padx=25, pady=15)

        self.riwayat = []
        self.tampil_login()

    # Helper UI Component
    def bersihkan(self, judul_teks):
        for widget in self.isi.winfo_children():
            widget.destroy()
        tk.Label(self.isi, text=NAMA_BANK, font=FONT_JUDUL,
                 bg=WARNA_BG, fg="#f2c94c").pack(pady=(5, 0))
        tk.Label(self.isi, text=judul_teks, font=FONT_BOLD,
                 bg=WARNA_BG, fg="white").pack(pady=(0, 15))

    def tombol(self, induk, teks, perintah, warna=WARNA_BIRU, samping=None):
        tombol = tk.Button(induk, text=teks, command=perintah, font=FONT_BOLD,
                           bg=warna, fg="white", activebackground=warna,
                           relief="flat", cursor="hand2", pady=8)
        if samping:
            tombol.pack(side=samping, expand=True, fill="x", padx=3)
        else:
            tombol.pack(fill="x", pady=4)
        return tombol

    def tombol_bawah(self):
        baris = tk.Frame(self.isi, bg=WARNA_BG)
        baris.pack(fill="x", pady=(20, 0))
        self.tombol(baris, "Menu Utama", self.tampil_menu_utama, WARNA_ABU, "left")
        self.tombol(baris, "Batal (ke PIN)", self.tampil_login, WARNA_MERAH, "left")

    def layar_menu(self, judul_teks, pilihan, bawah=True):
        self.bersihkan(judul_teks)
        for teks, fungsi in pilihan:
            self.tombol(self.isi, teks, fungsi)
        if bawah:
            self.tombol_bawah()

    def layar_form(self, judul_teks, daftar_kolom, lanjut, petunjuk="", bawah=True):
        self.bersihkan(judul_teks)
        if petunjuk:
            tk.Label(self.isi, text=petunjuk, font=FONT, bg=WARNA_BG,
                     fg="#cbd5e1", wraplength=480).pack(pady=(0, 5))

        daftar_entry = []
        for label, _, _, rahasia in daftar_kolom:
            tk.Label(self.isi, text=label, font=FONT, bg=WARNA_BG,
                     fg="white").pack(anchor="w", pady=(10, 2))
            entry = tk.Entry(self.isi, font=("Arial", 14), justify="center",
                             show="*" if rahasia else "")
            entry.pack(fill="x", ipady=6)
            daftar_entry.append(entry)

        def kirim(event=None):
            isian = []
            for entry, (label, pmin, pmaks, _) in zip(daftar_entry, daftar_kolom):
                teks = entry.get().strip()
                if not (teks.isascii() and teks.isdigit()):
                    messagebox.showwarning("Input tidak valid",
                                           f"{label}\n\nHanya boleh angka 0-9.")
                    return
                if not pmin <= len(teks) <= pmaks:
                    syarat = f"{pmin} digit" if pmin == pmaks else f"{pmin}-{pmaks} digit"
                    messagebox.showwarning("Input tidak valid",
                                           f"{label}\n\nHarus {syarat}.")
                    return
                isian.append(teks)
            lanjut(*isian)

        for entry in daftar_entry:
            entry.bind("<Return>", kirim)
        daftar_entry[0].focus()

        self.tombol(self.isi, "Lanjut", kirim, WARNA_HIJAU).pack_configure(pady=(20, 4))
        if bawah:
            self.tombol_bawah()

    def layar_pesan(self, judul_teks, pesan, warna=WARNA_HIJAU):
        self.bersihkan(judul_teks)
        tk.Label(self.isi, text=pesan, font=FONT_BOLD, bg=WARNA_BG, fg=warna,
                 wraplength=480, justify="center").pack(pady=30)
        self.tombol_akhir()

    def tombol_akhir(self):
        baris = tk.Frame(self.isi, bg=WARNA_BG)
        baris.pack(fill="x", pady=(20, 0))
        self.tombol(baris, "Transaksi Lain", self.tampil_login, WARNA_BIRU, "left")
        self.tombol(baris, "Selesai", self.tampil_selesai, WARNA_MERAH, "left")

    def pilih_nominal(self, judul_teks, daftar_nominal, lanjut):
        pilihan = [(rupiah(n), lambda n=n: lanjut(n)) for n in daftar_nominal]
        self.layar_menu(judul_teks, pilihan)

    # Autentikasi PIN
    def periksa_pin(self, pin):
        if pin == akun["pin"]:
            akun["salah_pin"] = 0
            return True

        akun["salah_pin"] += 1
        sisa = MAKS_SALAH_PIN - akun["salah_pin"]
        if sisa <= 0:
            self.tampil_blokir()
        else:
            messagebox.showerror("PIN Salah", f"PIN salah. Sisa percobaan: {sisa}")
        return False

    # Login & Menu Utama
    def tampil_login(self):
        def cek(pin):
            if self.periksa_pin(pin):
                self.tampil_menu_utama()

        self.layar_form("SELAMAT DATANG", [kolom("Masukkan PIN (6 digit)", 6, rahasia=True)],
                        cek, "Silakan masukkan kartu ATM Anda... (simulasi)", bawah=False)

    def tampil_menu_utama(self):
        self.layar_menu(f"MENU UTAMA - Halo, {akun['nama']}", [
            ("1. Transfer", self.menu_transfer),
            ("2. Penarikan Tunai", self.menu_tarik_tunai),
            ("3. Ganti PIN", self.menu_ganti_pin),
            ("4. Bayar / Beli", self.menu_bayar_beli),
            ("5. Informasi Saldo", self.tampil_saldo),
        ], bawah=False)
        self.tombol(self.isi, "Batal (ke PIN)", self.tampil_login, WARNA_MERAH).pack_configure(pady=(20, 4))

    # Logika dasar transaksi
    def transaksi(self, jenis, rincian, jumlah, biaya=0, setelah=None):
        total = jumlah + biaya
        if akun["saldo"] - total < SALDO_MINIMAL:
            self.layar_pesan("TRANSAKSI GAGAL",
                             f"Saldo tidak cukup.\nSaldo minimal yang harus mengendap "
                             f"{rupiah(SALDO_MINIMAL)}.", WARNA_MERAH)
            return

        self.bersihkan("KONFIRMASI TRANSAKSI")
        kartu = tk.Frame(self.isi, bg=WARNA_KARTU, padx=15, pady=15)
        kartu.pack(fill="x")

        baris = [("Jenis", jenis)] + rincian + [("Jumlah", rupiah(jumlah))]
        if biaya:
            baris.append(("Biaya", rupiah(biaya)))
        baris.append(("TOTAL", rupiah(total)))

        for i, (kunci, nilai) in enumerate(baris):
            tebal = FONT_BOLD if kunci == "TOTAL" else FONT
            tk.Label(kartu, text=kunci, font=tebal, bg=WARNA_KARTU,
                     anchor="w").grid(row=i, column=0, sticky="w", pady=3)
            tk.Label(kartu, text=f": {nilai}", font=tebal, bg=WARNA_KARTU,
                     anchor="w").grid(row=i, column=1, sticky="w", pady=3)

        tk.Label(self.isi, text="Apakah data di atas sudah benar\ndan transaksi akan dilanjutkan?",
                 font=FONT_BOLD, bg=WARNA_BG, fg="white").pack(pady=20)

        baris_tombol = tk.Frame(self.isi, bg=WARNA_BG)
        baris_tombol.pack(fill="x")
        self.tombol(baris_tombol, "Ya, Lanjutkan",
                    lambda: self.minta_pin(jenis, rincian, jumlah, biaya, setelah),
                    WARNA_HIJAU, "left")
        self.tombol(baris_tombol, "Tidak",
                    lambda: self.layar_pesan("TRANSAKSI DIBATALKAN",
                                             "Transaksi tidak dilanjutkan.", WARNA_MERAH),
                    WARNA_MERAH, "left")

    def minta_pin(self, jenis, rincian, jumlah, biaya, setelah):
        def cek(pin):
            if not self.periksa_pin(pin):
                return
            akun["saldo"] -= jumlah + biaya
            tambahan = setelah() if setelah else ""
            self.tampil_struk(jenis, rincian, jumlah, biaya, tambahan)

        self.layar_form("KONFIRMASI PIN", [kolom("Masukkan PIN (6 digit)", 6, rahasia=True)],
                        cek, "Masukkan PIN untuk menyelesaikan transaksi.")

    def tampil_struk(self, jenis, rincian, jumlah, biaya, tambahan=""):
        waktu = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        no_ref = "".join(random.choices("0123456789", k=12))
        total = jumlah + biaya
        self.riwayat.append((waktu, jenis, total))

        self.bersihkan("TRANSAKSI BERHASIL")
        kartu = tk.Frame(self.isi, bg=WARNA_KARTU, padx=15, pady=15)
        kartu.pack(fill="x")

        baris = [("Waktu", waktu), ("No. Ref", no_ref),
                 ("Rekening", akun["no_rekening"]), ("Jenis", jenis)] + rincian
        baris.append(("Jumlah", rupiah(jumlah)))
        if biaya:
            baris.append(("Biaya", rupiah(biaya)))
        baris.append(("Total", rupiah(total)))
        baris.append(("Sisa Saldo", rupiah(akun["saldo"])))

        for i, (kunci, nilai) in enumerate(baris):
            tk.Label(kartu, text=kunci, font=FONT, bg=WARNA_KARTU).grid(
                row=i, column=0, sticky="w", pady=2)
            tk.Label(kartu, text=f": {nilai}", font=FONT, bg=WARNA_KARTU).grid(
                row=i, column=1, sticky="w", pady=2)

        if tambahan:
            tk.Label(self.isi, text=tambahan, font=FONT_BOLD, bg=WARNA_BG,
                     fg="#f2c94c", wraplength=480).pack(pady=12)
        self.tombol_akhir()

    # Feature 1: Transfer
    def menu_transfer(self):
        self.layar_menu("TRANSFER", [
            ("Antarbank", self.pilih_bank),
            ("Antar Rekening AJAR", self.form_antar_rekening),
        ])

    def pilih_bank(self):
        pilihan = [(bank, lambda b=bank: self.form_antarbank(b)) for bank in DAFTAR_BANK]
        self.layar_menu("PILIH BANK TUJUAN", pilihan)

    def form_antarbank(self, bank):
        def lanjut(no_rek, nominal):
            nominal = int(nominal)
            if nominal < 10_000:
                messagebox.showwarning("Nominal", f"Minimal transfer {rupiah(10_000)}.")
                return
            self.transaksi("Transfer Antarbank",
                           [("Bank", bank), ("Rek. Tujuan", no_rek)],
                           nominal, BIAYA_ANTARBANK)

        self.layar_form(f"TRANSFER KE {bank}", [
            kolom("No. rekening tujuan (10-16 digit)", 10, 16),
            kolom("Nominal transfer (Rp)", 1, 12),
        ], lanjut)

    def form_antar_rekening(self):
        def lanjut(no_rek, nominal):
            nominal = int(nominal)
            if no_rek == akun["no_rekening"]:
                messagebox.showwarning("Rekening", "Tidak bisa transfer ke rekening sendiri.")
                return
            if nominal < 10_000:
                messagebox.showwarning("Nominal", f"Minimal transfer {rupiah(10_000)}.")
                return
            self.transaksi("Transfer Antar Rekening AJAR",
                           [("Rek. Tujuan", no_rek)], nominal)

        self.layar_form("TRANSFER ANTAR REKENING AJAR", [
            kolom("No. rekening tujuan (10 digit)", 10),
            kolom("Nominal transfer (Rp)", 1, 12),
        ], lanjut)

    # Feature 2: Penarikan Tunai
    def menu_tarik_tunai(self):
        self.layar_menu("PENARIKAN TUNAI", [
            ("Rp50.000", lambda: self.tarik(50_000)),
            ("Rp100.000", lambda: self.tarik(100_000)),
            ("Rp200.000", lambda: self.tarik(200_000)),
            ("Jumlah Lain", self.form_tarik_lain),
        ])

    def form_tarik_lain(self):
        def lanjut(nominal):
            nominal = int(nominal)
            if nominal < KELIPATAN_TARIK or nominal % KELIPATAN_TARIK != 0:
                messagebox.showwarning("Nominal", f"Harus kelipatan {rupiah(KELIPATAN_TARIK)}.")
                return
            if nominal > BATAS_TARIK:
                messagebox.showwarning("Nominal", f"Maksimal {rupiah(BATAS_TARIK)} per transaksi.")
                return
            self.tarik(nominal)

        self.layar_form("JUMLAH LAIN", [kolom("Jumlah penarikan (Rp)", 1, 12)], lanjut,
                        f"Kelipatan {rupiah(KELIPATAN_TARIK)}, maksimal {rupiah(BATAS_TARIK)}.")

    def tarik(self, nominal):
        self.transaksi("Penarikan Tunai", [], nominal,
                       setelah=lambda: "Silakan ambil uang Anda... (simulasi)")

    # Feature 3: Ganti PIN
    def menu_ganti_pin(self):
        def proses(lama, baru, ulang):
            if not self.periksa_pin(lama):
                return
            if baru == akun["pin"]:
                messagebox.showwarning("PIN", "PIN baru tidak boleh sama dengan PIN lama.")
                return
            if len(set(baru)) == 1 or baru in ("123456", "654321"):
                messagebox.showwarning("PIN", "PIN terlalu mudah ditebak.")
                return
            if ulang != baru:
                messagebox.showwarning("PIN", "PIN konfirmasi tidak cocok.")
                return
            akun["pin"] = baru
            self.layar_pesan("GANTI PIN", "PIN berhasil diganti.")

        self.layar_form("GANTI PIN", [
            kolom("PIN lama (6 digit)", 6, rahasia=True),
            kolom("PIN baru (6 digit)", 6, rahasia=True),
            kolom("Ulangi PIN baru", 6, rahasia=True),
        ], proses)

    # Feature 4: Bayar / Beli
    def menu_bayar_beli(self):
        self.layar_menu("BAYAR / BELI", [
            ("Telepon / HP", self.menu_telepon),
            ("Listrik / Gas", self.menu_listrik_gas),
            ("BPJS", self.menu_bpjs),
            ("Asuransi", self.menu_asuransi),
            ("E-Wallet", self.menu_ewallet),
        ])

    # Telepon / HP
    def menu_telepon(self):
        self.layar_menu("TELEPON / HP", [
            ("Prabayar (Pulsa)", lambda: self.form_hp(prabayar=True)),
            ("Pascabayar", lambda: self.form_hp(prabayar=False)),
        ])

    def form_hp(self, prabayar):
        def lanjut(no_hp):
            if not no_hp.startswith("08"):
                messagebox.showwarning("No. HP", "Nomor HP harus diawali 08.")
                return
            if prabayar:
                self.pilih_nominal(
                    "NOMINAL PULSA", NOMINAL_PULSA,
                    lambda n: self.transaksi("Beli Pulsa Prabayar",
                                             [("No. HP", no_hp)], n, 1_500))
            else:
                tagihan = tagihan_acak(80_000, 400_000)
                self.transaksi("Bayar Telepon Pascabayar",
                               [("No. HP", no_hp)], tagihan, BIAYA_ADMIN)

        self.layar_form("NOMOR HP", [kolom("No. HP (10-13 digit, mis. 0812xxxxxxx)", 10, 13)], lanjut)

    # Listrik / Gas
    def menu_listrik_gas(self):
        self.layar_menu("LISTRIK / GAS", [
            ("PGN", self.form_pgn),
            ("PLN Prabayar (Token)", self.form_pln_prabayar),
            ("PLN Pascabayar", self.form_pln_pascabayar),
        ])

    def form_pgn(self):
        def lanjut(no_pel):
            tagihan = tagihan_acak(50_000, 300_000)
            self.transaksi("Bayar Tagihan PGN", [("No. Pel.", no_pel)], tagihan, BIAYA_ADMIN)

        self.layar_form("PGN", [kolom("No. pelanggan PGN (10 digit)", 10)], lanjut)

    def form_pln_prabayar(self):
        def buat_token():
            kelompok = ["".join(random.choices("0123456789", k=4)) for _ in range(5)]
            return "Token listrik Anda:\n" + "-".join(kelompok)

        def lanjut(no_meter):
            self.pilih_nominal(
                "NOMINAL TOKEN LISTRIK", NOMINAL_TOKEN,
                lambda n: self.transaksi("Beli Token PLN Prabayar",
                                         [("No. Meter", no_meter)], n, BIAYA_ADMIN,
                                         setelah=buat_token))

        self.layar_form("PLN PRABAYAR", [kolom("No. meter / ID pelanggan (11-12 digit)", 11, 12)], lanjut)

    def form_pln_pascabayar(self):
        def lanjut(id_pel):
            tagihan = tagihan_acak(100_000, 900_000)
            self.transaksi("Bayar Tagihan PLN Pascabayar",
                           [("ID Pel.", id_pel)], tagihan, BIAYA_ADMIN)

        self.layar_form("PLN PASCABAYAR", [kolom("ID pelanggan (11-12 digit)", 11, 12)], lanjut)

    # BPJS
    def menu_bpjs(self):
        self.layar_menu("BPJS", [
            ("BPJS Ketenagakerjaan", lambda: self.form_bpjs("BPJS Ketenagakerjaan", 11)),
            ("BPJS Kesehatan", lambda: self.form_bpjs("BPJS Kesehatan", 16)),
        ])

    def form_bpjs(self, nama, panjang):
        def lanjut(no_peserta):
            if nama == "BPJS Ketenagakerjaan":
                tagihan = tagihan_acak(16_800, 200_000)
            else:
                tagihan = random.choice([42_000, 100_000, 150_000]) * random.randint(1, 4)
            self.transaksi(f"Bayar {nama}", [("No. Peserta", no_peserta)], tagihan, BIAYA_ADMIN)

        self.layar_form(nama.upper(), [kolom(f"No. peserta ({panjang} digit)", panjang)], lanjut)

    # Asuransi
    def menu_asuransi(self):
        pilihan = [(nama, lambda n=nama: self.form_asuransi(n)) for nama in DAFTAR_ASURANSI]
        self.layar_menu("PILIH ASURANSI", pilihan)

    def form_asuransi(self, perusahaan):
        def lanjut(no_polis):
            premi = tagihan_acak(150_000, 1_500_000)
            self.transaksi(f"Bayar Premi {perusahaan}", [("No. Polis", no_polis)],
                           premi, BIAYA_ADMIN)

        self.layar_form(perusahaan.upper(), [kolom("No. polis (10 digit)", 10)], lanjut)

    # E-Wallet
    def menu_ewallet(self):
        pilihan = [(nama, lambda n=nama: self.form_ewallet(n)) for nama in E_WALLET]
        self.layar_menu("PILIH E-WALLET", pilihan)

    def form_ewallet(self, nama):
        def lanjut(no_hp):
            self.pilih_nominal(
                "NOMINAL TOP UP", NOMINAL_EWALLET,
                lambda n: self.transaksi(f"Top Up {nama}", [("No. HP", no_hp)], n, 1_000))

        self.layar_form(f"TOP UP {nama}", [kolom("No. HP terdaftar (10-13 digit)", 10, 13)], lanjut)

    # Feature 5: Informasi Saldo
    def tampil_saldo(self):
        self.bersihkan("INFORMASI SALDO")
        kartu = tk.Frame(self.isi, bg=WARNA_KARTU, padx=15, pady=15)
        kartu.pack(fill="x")
        data = [("Nama", akun["nama"]),
                ("No. Rekening", akun["no_rekening"]),
                ("Saldo", rupiah(akun["saldo"])),
                ("Waktu", datetime.now().strftime("%d/%m/%Y %H:%M:%S"))]
        for i, (kunci, nilai) in enumerate(data):
            tk.Label(kartu, text=kunci, font=FONT, bg=WARNA_KARTU).grid(
                row=i, column=0, sticky="w", pady=3)
            tk.Label(kartu, text=f": {nilai}", font=FONT, bg=WARNA_KARTU).grid(
                row=i, column=1, sticky="w", pady=3)
        self.tombol_akhir()

    # Layar Akhir
    def tampil_selesai(self):
        self.bersihkan("TRANSAKSI SELESAI")
        if self.riwayat:
            tk.Label(self.isi, text="Ringkasan transaksi sesi ini:", font=FONT_BOLD,
                     bg=WARNA_BG, fg="white").pack(anchor="w")
            for waktu, jenis, total in self.riwayat:
                tk.Label(self.isi, text=f"{waktu}  {jenis}  {rupiah(total)}",
                         font=("Arial", 10), bg=WARNA_BG, fg="#cbd5e1",
                         anchor="w").pack(fill="x")
        tk.Label(self.isi, text=f"\nSaldo akhir: {rupiah(akun['saldo'])}",
                 font=FONT_BOLD, bg=WARNA_BG, fg="#f2c94c").pack()
        tk.Label(self.isi, text=f"\nSilakan ambil kartu Anda.\n"
                                f"Terima kasih telah menggunakan {NAMA_BANK}.",
                 font=FONT, bg=WARNA_BG, fg="white").pack(pady=10)
        self.tombol(self.isi, "Tutup", self.destroy, WARNA_MERAH)

    def tampil_blokir(self):
        self.bersihkan("KARTU DIBLOKIR")
        tk.Label(self.isi, text=f"Kartu DIBLOKIR karena salah PIN {MAKS_SALAH_PIN} kali.\n"
                                "Hubungi bank terdekat.",
                 font=FONT_BOLD, bg=WARNA_BG, fg=WARNA_MERAH,
                 wraplength=480).pack(pady=30)
        self.tombol(self.isi, "Tutup", self.destroy, WARNA_MERAH)


# Main
if __name__ == "__main__":
    AplikasiATM().mainloop()