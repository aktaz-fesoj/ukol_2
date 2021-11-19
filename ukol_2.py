import csv
import datetime

def OdecetDni(d,m,r,presah):
    """Vrací datum formátu datetime, které nastalo před "presah" dnů od data "d.m.r".
    Parameters:
                    d (int): Den z data od kterého bude odečítáno
                    m (int): Měsíc z data od kterého bude odečítáno
                    r (int): Rok z data od kterého bude odečítáno
                    presah(int): Počet dní o které se bude datum posouvat zpět
            Returns:
                    vysledek (): Binary string of the sum of a and b
    """

    datum = datetime.date(r, m, d)
    presah_dni = datetime.timedelta(presah-1)
    vysledek = datum - presah_dni
    return(vysledek)

def PlatneCislice(a, pocet_platnych):
    """Vrací číslo zaokrouhlené na daný počet platných číslic

    Keyword arguments:
    a -- 
    """
    a = round(a, pocet_platnych)
    vys = "{:.4f}".format(a)
    return(vys)
    

def TydenniPrumery(vstupni_data, vystup):
    with open(vstupni_data, encoding = "utf-8") as tyden_vstup,\
        open(vystup, "w", encoding = "utf-8") as tyden_vystup:
        reader = csv.reader(tyden_vstup)
        zapis_tyden  = csv.writer(tyden_vystup, lineterminator='\r')
        soucet = 0
        i = 0
        for row in reader:
            i += 1
            if i % 7 == 1 or i == 1:
                vypis_radek = [row[0], row[1], row[2], row[3], row[4]]
            soucet += float(row[5])
            if i % 7 == 0:
                prumer_hotovy = PlatneCislice(soucet/7, 4)
                vypis_radek.append(prumer_hotovy)
                zapis_tyden.writerow(vypis_radek)
                soucet = 0
                vypis_radek.clear
            dat = row
        a = OdecetDni(int(dat[4]), int(dat[3]), int(dat[2]), i % 7)
        prumer_posledni = PlatneCislice(soucet / (i % 7),  4)
        zapis_tyden.writerow([dat[0], dat[1], a.year, a.month, a.day, prumer_posledni])
    return()

def RocniPrumery(vstupni_data, vystup):
    with open(vstupni_data, encoding = "utf-8") as rok_vstup,\
        open(vystup, "w", encoding = "utf-8") as rok_vystup:
        reader = csv.reader(rok_vstup)
        zapis_rok  = csv.writer(rok_vystup, lineterminator='\r')
        i = 0
        rok = 0
        soucet = 0
        for row in reader:
            if rok == 0:
                vypis_radek = [row[0], row[1], row[2], row[3], row[4]]
            if rok != int(row[2]) and rok !=0:
                prumer_hotovy = PlatneCislice(soucet/i, 4)
                vypis_radek.append(prumer_hotovy)
                zapis_rok.writerow(vypis_radek)
                soucet = 0
                i = 0
                vypis_radek.clear
                vypis_radek = [row[0], row[1], row[2], row[3], row[4]]
            i += 1
            dat = row
            soucet += float(row[5])
            rok = int(row[2])
        a = OdecetDni(int(dat[4]), int(dat[3]), int(dat[2]), i)
        prumer_posledni = PlatneCislice(soucet/i,  4)
        zapis_rok.writerow([dat[0], dat[1], a.year, a.month, a.day, prumer_posledni])
    return()    


def KontrolaDat(vstupni_data):
    with open(vstupni_data, encoding = "utf-8") as vstup:
        reader = csv.reader(vstup)
        i = 0
        chyba = False
        delka = 0
        for row in reader:
            i += 1
            try:
                if int(row[3]) < 1 or int(row[3]) > 12:
                    print(f"Chyba v datech, řádek {i}, neplatný měsíc.")
                    chyba = True

                if int(row[3]) == 1 or int(row[3]) == 3 or int(row[3]) == 5 or int(row[3]) == 7 or int(row[3]) == 8 or int(row[3]) == 10 or int(row[3]) == 12:
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
                print(f"Chyba ve vstupních datech, den, měsíc či rok v neplatném formátu(desetinné číslo, text, prázdné pole). Identifikováno na řádku {i}.")
                chyba = True
            try:
                float(row[5])
            except ValueError:
                print(f"Chyba ve vstupních datech. Průtok na řádku {i} není číslo.")
                chyba = True
        if chyba == True:
            print("Prosím, opravte vstupní data a zkuste to ještě jednou.")
            exit()


KontrolaDat("vstup.csv")
TydenniPrumery("vstup.csv", "vystup_7dni.csv")
RocniPrumery("vstup.csv", "vystup_rok.csv")
print("Program úspěšně proběhl.") 

OdecetDni()