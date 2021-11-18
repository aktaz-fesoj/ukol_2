import csv
import datetime

def datum_posledni(d,m,r,presah):
    datum = datetime.date(r, m, d)
    presah_dni = datetime.timedelta(presah-1)
    vysledek = datum - presah_dni
    return(vysledek)

def tydenni_prumery(vstupni_data, vystup):
    with open(vstupni_data, encoding = "utf-8") as tyden_vstup,\
        open(vystup, "w", encoding = "utf-8") as tyden_vystup:
        reader = csv.reader(tyden_vstup)
        zapis_tyden  = csv.writer(tyden_vystup)
        soucet = 0
        i = 0
        for row in reader:
            i += 1
            if i % 7 == 1 or i == 1:
                vypis_radek = [row[0], row[1], row[2], row[3], row[4]]
            soucet += float(row[5])
            if i % 7 == 0:
                vypis_radek.append(round(soucet/7, 4))
                zapis_tyden.writerow(vypis_radek)
                soucet = 0
                vypis_radek.clear
            dat = row
        a = datum_posledni(int(dat[4]), int(dat[3]), int(dat[2]), i % 7)
        zapis_tyden.writerow([dat[0], dat[1], a.year, a.month, a.day, round(soucet / (i % 7),4)])
    return()

def kontrola_dat(vstupni_data):
    with open(vstupni_data, encoding = "utf-8") as vstup:
        reader = csv.reader(vstup)
        i = 0
        chyba = False
        delka = 0
        for row in reader:
            i += i
            try:
                if int(row[3]) < 1 or int(row[3]) > 12:
                    print(f"Chyba v datech, řádek {i}, neplatný měsíc.")
                    chyba = True
                if int(row[3]) == 1 or 3 or 5 or 7 or 8 or 10 or 12:
                    delka = 31
                elif int(row[3]) == 2 and int(row[2]) % 4 == 0:
                        delka = 29
                elif int(row[3]) == 2 and int(row[2]) % 4 != 0:
                        delka = 28
                else:
                    delka = 30
                if int(row[4]) < 1 or int(row[4]) > delka:
                    print(f"Chyba v datech, řádek {i}, neplatný den.")
                    chyba = True
            except ValueError:
                print("Chyba ve vstupních datech, den, měsíc či rok v desetinném čísle.")
                chyba = True
        if chyba == True:
            print("Prosím, opravte vstupní data a zkuste to ještě jednou.")
            exit()





kontrola_dat("vstup.csv")
tydenni_prumery("vstup.csv", "vystup_7dni.csv")
print("Program úspěšně proběhl.")