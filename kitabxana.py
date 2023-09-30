import sqlite3
from colorama import Fore, Style

class Kitab:
    def __init__(self, ad, muellif, janr, nesr_ili):
        self.ad = ad
        self.muellif = muellif
        self.janr = janr
        self.nesr_ili = nesr_ili

    def __str__(self):
        return f"Kitab adı: {self.ad}, Müəllif: {self.muellif}, Janr: {self.janr}, Nəşr İli: {self.nesr_ili}"

class Kitabxana:
    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS kitablar
                               (id INTEGER PRIMARY KEY AUTOINCREMENT,
                                ad TEXT,
                                muellif TEXT,
                                janr TEXT,
                                nesr_ili INTEGER)''')
        self.conn.commit()

    def baglanti_yarat(self):
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()

    def baglanti_kes(self):
        self.conn.close()

    def kitab_elave_et(self, kitab):
        self.cursor.execute("INSERT INTO kitablar (ad, muellif, janr, nesr_ili) VALUES (?, ?, ?, ?)",
                            (kitab.ad, kitab.muellif, kitab.janr, kitab.nesr_ili))
        self.conn.commit()

    def kitablari_goster(self):
        self.cursor.execute("SELECT * FROM kitablar")
        kitablar = self.cursor.fetchall()
        print(Fore.GREEN + "\nKitablar:")
        for kitab in kitablar:
            print(f"{kitab[0]}. {kitab[1]}")
        print(Style.RESET_ALL)

    def kitab_axtar(self, ad):
        self.cursor.execute("SELECT * FROM kitablar WHERE ad=?", (ad,))
        kitab = self.cursor.fetchone()
        if kitab:
            return Kitab(kitab[1], kitab[2], kitab[3], kitab[4])
        else:
            return None

    def kitab_sil(self, kitab_id):
        self.cursor.execute("DELETE FROM kitablar WHERE id=?", (kitab_id,))
        self.conn.commit()

def main():
    db_name = "kitabxana.db"
    kitabxana = Kitabxana(db_name)

    while True:
        print("\nKitabxana Komandaları:")
        print("1. Kitab əlavə et")
        print("2. Kitabları göstər")
        print("3. Kitab axtar")
        print("4. Kitab sil")
        print("5. Çıxış")

        secim = input("Seçiminizi daxil edin (1/2/3/4/5): ")

        if secim == "1":
            ad = input("Kitabın adını daxil edin: ")
            muellif = input("Müəllifin adını daxil edin: ")
            janr = input("Kitabın janrını daxil edin: ")
            nesr_ili = int(input("Kitabın nəşr ilini daxil edin: "))
            kitab = Kitab(ad, muellif, janr, nesr_ili)
            kitabxana.kitab_elave_et(kitab)
            print(Fore.GREEN + "Kitab əlavə edildi.")
            print(Style.RESET_ALL)

        elif secim == "2":
            kitabxana.kitablari_goster()

        elif secim == "3":
            ad = input("Axtarılacaq kitabın adını daxil edin: ")
            kitab = kitabxana.kitab_axtar(ad)
            if kitab:
                print(Fore.GREEN + "\nAxtarılacaq kitab:")
                print(kitab)
                print(Style.RESET_ALL)
            else:
                print(Fore.RED + "Kitab tapılmadı.")
                print(Style.RESET_ALL)

        elif secim == "4":
            kitab_id = int(input("Silinecek kitabın ID-ni daxil edin: "))
            kitabxana.kitab_sil(kitab_id)
            print(Fore.GREEN + "Kitab silindi.")
            print(Style.RESET_ALL)

        elif secim == "5":
            kitabxana.baglanti_kes()
            print(Fore.YELLOW + "Programdan çıxılır.")
            print(Style.RESET_ALL)
            break

        else:
            print(Fore.RED + "Yanlış seçim! 1, 2, 3, 4 və ya 5 seçin.")
            print(Style.RESET_ALL)

if __name__ == "__main__":
    main()
