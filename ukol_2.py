import csv
import datetime

def OdecetDni(d,m,r,presah):
    """Vrací datum ve formátu datetime, které nastalo před "presah" dnů od data "d.m.r".

        Parameters:
                    d (int): Den z data od kterého bude odečítáno
                    m (int): Měsíc z data od kterého bude odečítáno
                    r (int): Rok z data od kterého bude odečítáno
                    presah(int): Počet dní o které se bude datum posouvat zpět
        Returns:
                    vysledek(date): Výsledné datum ve formátu datetime.date, lze z něj volat day, month, year
    """
    datum = datetime.date(r, m, d)              #Vstupní datum
    presah_dni = datetime.timedelta(presah)   #Počet odčítaných dní
    vysledek = datum - presah_dni
    return(vysledek)

def PlatneCislice(a, pocet_platnych):
    """Vrací číslo zaokrouhlené na daný počet platných číslic za desetinnou čárkou.

        Parameters:
                    a (float): Číslo, které bude upraveno
                    pocet_platnych(int): Počet požadovaných platných číslic za desetinnou čárkou
        Returns:
                    vys(float): číslo zaokrouhlené na daný počet platných číslic za desetinnou čárkou
    """
    a = round(a, pocet_platnych)    #Zaokrouhlí číslo na místa za desetinnou čárkou 
    vys = "{:.4f}".format(a)        #Docílí toho, aby byly vypsány všechny 4 číslice, i když jsou poslední z nich nuly
    return(vys)

def TydenniPrumery(vstupni_data, vystup):
    """Funkce zpracovává data o sedmidenních průtocích z csv souboru.
    
    Funkce zpracovává vstupní csv soubor s daty o denních průtocích a vrací nový csv soubor, ve kterém \
    jsou uloženy sedmidenní průměry průtoku spojené s prvním dnem daného sedmidenního úseku. \
    Pokud není počet sledovaných dní dělitelný sedmi, jsou zbylá data na konci vstupního souboru zpracovány.

        Parameters:
                    vstupni_data(str): Relativní či absolutní cesta ke vstupnímu csv souboru
                    vystup(str): Relativní či absolutní cesta k výstupnímu csv souboru
    """
    with open(vstupni_data, encoding = "utf-8") as tyden_vstup,\
        open(vystup, "w", encoding = "utf-8") as tyden_vystup:              #Otevírá vstupní a výstupní csv soubory
        reader = csv.reader(tyden_vstup)
        zapis_tyden  = csv.writer(tyden_vystup, lineterminator='\r')
        soucet = 0
        i = 0
        for row in reader:
            i += 1                                                          #Počítá dny, při každém opakování se zvýší o 1
            if i % 7 == 1:                                                  #Je-li zbytek po i/7 roven 1, znamená to, že začal nový týden
                vypis_radek = [row[0], row[1], row[2], row[3], row[4]]      #Uložím tedy do seznamu informace, které mají být vypsány o prvním dni sledovaného období
            soucet += float(row[5])                                         #Při každém opakování přičtu průtok daného dne
            if i % 7 == 0:                                                  #Je li i dělitelné beze zbytku sedmi, jde o poslední den týdne
                prumer_hotovy = PlatneCislice(soucet/7, 4)                  #Spočtu tedy průměr průtoků z sedm dní, který pomocí fce PlatneCislice upravím na 4 platné číslice
                vypis_radek.append(prumer_hotovy)                           #Přidám ho do seznamu k údajům z prvního dne sedmidenního období
                zapis_tyden.writerow(vypis_radek)                           #Celý seznam vypíši jako řádek do nového csv souboru
                soucet = 0                                                  #Proměnnou soucet vynuluji, aby se do ní mohlo sčítat opět od 0 pro další úsek dní
                vypis_radek.clear                                           #Stejně tak vyčistím i seznam vypis_radek
            dat = row                                                       #Do proměnné dat si uložím daný řádek, využiji ji u posledního řádku ze souboru
        if i % 7 != 0:                                                       #Pokud zbyly dny tzn. sedmi nelze dělit beze zbytku
            a = OdecetDni(int(dat[4]), int(dat[3]), int(dat[2]), i % 7 - 1)     #Proběhne-li předchozí cyklus na počtu řádků neceločíselně dělitelných sedmi, pomocí fce OdecetDni odečtu i%7 dní od data posledního dne ze souboru (i%7 vrátí počet dní, které byly "navíc" od posledního konce sedmidenního období)
            prumer_posledni = PlatneCislice(soucet / (i % 7),  4)               #Spočítám průměr posledního období a pomocí fce PlatneCislice upravím (zaokrouhlím na čtyři platné číslice za desetinnou čárkou)
            zapis_tyden.writerow([dat[0], dat[1], a.year, a.month, a.day, prumer_posledni]) #Vypíši řádek o posledním období. Proměnná a vznikla výpočtem fcí OdecetDni, odkazuje na první datum daného období, o kterém vypisuji informace
    return()

def RocniPrumery(vstupni_data, vystup):
    """Funkce zpracovává data o ročních průtocích z csv souboru.
    
    Funkce zpracovává vstupní csv soubor s daty o denních průtocích a vrací nový csv soubor, ve kterém \
    jsou uloženy roční průměry průtoku spojené s prvním dnem daného roku se zaznamenanou informací o průtoku.

        Parameters:
                    vstupni_data(str): Relativní či absolutní cesta ke vstupnímu csv souboru
                    vystup(str): Relativní či absolutní cesta k výstupnímu csv souboru
    """
    with open(vstupni_data, encoding = "utf-8") as rok_vstup,\
        open(vystup, "w", encoding = "utf-8") as rok_vystup:                #Otevírá vstupní a výstupní csv soubory
        reader = csv.reader(rok_vstup)
        zapis_rok  = csv.writer(rok_vystup, lineterminator='\r')            #Definování lineiteretoru (oddělovače řádků) jako \r zajistí, aby nevznikal prázdný řádek mezi každými dvěma řádky
        i = 0
        rok = 0
        soucet = 0
        for row in reader:
            if rok == 0:                                                    #Uloží informace o prvním roce do seznamu vypis_radek
                vypis_radek = [row[0], row[1], row[2], row[3], row[4]]      
            if rok != int(row[2]) and rok !=0:                              #Vždy když dojde ke změně roku, vypíše průměrný průtok spolu s informacemi o prvním dni období, podobně jako fce TydenniPrumery
                prumer_hotovy = PlatneCislice(soucet/i, 4)                  #Spočítá průměr a upraví ho do požadovaného formátu. Proměnná i uchovává počet sčítaných průtoků - dní v období.
                vypis_radek.append(prumer_hotovy)                           #Přidá výsledný průměr do seznamu k informacím z prvního dne daného období
                zapis_rok.writerow(vypis_radek)                             #Vypíše všechny tyto informace jako řádek do výstupního souboru
                soucet = 0                                                  #Vynuluje soucet, tak aby pro nový rok byl počítán znovu od nuly
                i = 0                                                       #Vynuluje i, tedy proměnnou uchovávající počet sečtených průtoků v daném období
                vypis_radek.clear                                           #Vyčistí seznam, který byl již vypsán
                vypis_radek = [row[0], row[1], row[2], row[3], row[4]]      #Uloží informace o prvním dni nového roku
            i += 1                                                          #Počítá počet dní, respektive započítaných průtoků
            soucet += float(row[5])                                         #Sčítání průtoků
            rok = int(row[2])                                               #Ukládá do proměnné rok letopočet z daného řádku, tak aby mohl být v dalším opakování porovnán s novým letopočtem
        if i != 0:                                                           
            prumer_posledni = PlatneCislice(soucet/i,  4)                    #Spočítá průměr pro poslední rok
            vypis_radek.append(prumer_posledni)                              #Přidá poslední průměr do seznamu k informací z prvního dne roku
            zapis_rok.writerow(vypis_radek)                                  #Vypíše informace o posledním ze sledovaných roků
    return()    

def KontrolaDat(vstupni_data):
    """Funkce kontroluje koreknost vstupních dat.

        Kontroluje se korektnost čísla dnea měsíce, dat o průtoku, přístupnost csv souboru, to jestli není prázdný.

        Parameters:
                    vstupni_data(str): Relativní či absolutní cesta ke vstupnímu csv souboru
    """
    try:
        with open(vstupni_data, encoding = "utf-8") as vstup:
            reader = csv.reader(vstup)
            i = 0
            chyba = False
            delka = 0
            prutok_cislo = 1
            for row in reader:
                i += 1              #Počítadlo řádků
                try:
                    if int(row[3]) < 1 or int(row[3]) > 12: #Číslo měsíce nemůže být větší než 12 ani menší než 0
                        print(f"Chyba v datech, řádek {i}, neplatný měsíc.")
                        chyba = True
                    if int(row[3]) == 1 or int(row[3]) == 3 or int(row[3]) == 5 or int(row[3]) == 7 or int(row[3]) == 8 or int(row[3]) == 10 or int(row[3]) == 12:      #Měsíce s délkou 31 dní
                        delka = 31
                    elif int(row[3]) == 2 and int(row[2]) % 4 == 0:      #Přestupné roky, únor má 29 dní. Existuje výjimka, ale poslední nastala v roce 1900 a další nastane až v roce 2100, nepředpokládám taková vstupní data. 
                            delka = 29
                    elif int(row[3]) == 2 and int(row[2]) % 4 != 0:      #Nepřestupné roky, únor má 28 dní
                            delka = 28
                    else:
                        delka = 30              #Ostatní měsíce mají 30 dní
                    if int(row[4]) < 1 or int(row[4]) > delka:      # Číslo dne nemůže být menší než 0 ani větší něž počet dní v daném měsíci
                        print(f"Chyba v datech, řádek {i}, neplatný den.")
                        chyba = True
                except ValueError:          #V případě neceločíselných dat den, měsíc, rok se jedná o chybná data
                    print(f"Chyba ve vstupních datech, den, měsíc či rok v neplatném formátu(desetinné číslo, text, prázdné pole). Identifikováno na řádku {i}.")
                    chyba = True
                try:                    #Kontrola dat průtoků
                    float(row[5])
                except ValueError:
                    print(f"Chyba ve vstupních datech. Průtok na řádku {i} není číslo.")
                    chyba = True
                    prutok_cislo = 0
                if prutok_cislo != 0:
                    if float(row[5]) <= 0:
                        print(f"Nulový, nebo záporný průtok na řádku {i}, dne {row[4]}. {row[3]}. {row[2]}.")
            if i == 0:
                print("Vstupní soubor je prázdný.")         #Je-li vstupní soubor prázdný, neprovede se žádná iterace -> i = 0
                chyba = True
            if chyba == True:                               #Identifikovala-li fce chybu v datech, vypíše hlášku a ukončí běh programu.
                print("Prosím, opravte vstupní data a zkuste to ještě jednou.")
                exit()
                
    except FileNotFoundError:
        print("Soubor vstup.csv nebyl nalezen ve stejné složce, z jaké spouštíte tento program. Přejmenujte, případně přesuňte csv soubor.")
        exit()  
    except PermissionError:
        print("Program nemá oprávnění číst soubor vstup.csv.")
        print("Prosím, opravte vstupní data a zkuste to ještě jednou.")
        exit()
    except IndexError:
        print("Byla nelezena chyba ve struktuře dat. Přečtěte si prosím uživatelskou dokumentaci.")
        print("Prosím, opravte vstupní data a zkuste to ještě jednou.")
    return(print("Prvotní kontrola dat v souboru proběhla úspěšně."))

def MaxMinPrutok(vstupni_data):
    """Funkce vrací maximální a minimální průtok spolu s dalšími údaji.

        Funkce vypíše do konzole maximální a minimální průtok spolu s údaji o dni ve kterém bylo maximum a minimum naměřeno.

        Parameters:
                    vstupni_data(str): Relativní či absolutní cesta ke vstupnímu csv souboru
    """
    with open(vstupni_data, encoding = "utf-8") as vstup:
        reader = csv.reader(vstup)
        i=0
        for row in reader:
            i += 1
            if i == 1:
                max = float(row[5])
                max_info = [i, row[2], row[3], row[4]]
                min = float(row[5])
                min_info = [i, row[2], row[3], row[4]]
            if float(row[5]) > max:
                max = float(row[5])
                max_info = [i, row[2], row[3], row[4]]
            if float(row[5]) < min:
                min = float(row[5])
                min_info = [i, row[2], row[3], row[4]]
        
        print(f"Maximální průtok detekován na řádku {max_info[0]}, datum: {max_info[3]}. {max_info[2]}. {max_info[1]}, průtok: {max}.")
        print(f"Maximální průtok detekován na řádku {min_info[0]}, datum: {min_info[3]}. {min_info[2]}. {min_info[1]}, průtok: {min}.")
        return(max, min, max_info, min_info)

def ChybejiciDny(vstupni_data):
    """Funkce vypíše dny chybějící v datech.

        Funkce vypíše data chybějící mezi dtem na prvním řádku a datem posledním v datech

        Parameters:
                    vstupni_data(str): Relativní či absolutní cesta ke vstupnímu csv souboru
    """
    with open(vstupni_data, encoding = "utf-8") as vstup:
            reader = csv.reader(vstup)
            i = 0
            predchozi = datetime.date(1,1,1)
            for row in reader:
                i += 1
                aktualni = datetime.date(int(row[2]), int(row[3]), int(row[4]))                 #Proměnná aktualni uloží datum právě zpracovávaného řádku
                if OdecetDni(int(row[4]), int(row[3]), int(row[2]), 1) != predchozi and i != 1: #Fce odecet dni vratí datum předcházejícího dne. Pokud se toto datum nerovná datu uloženému v proměnné predchozi, den(nebo dny) v datech chybí. Speciálním případem je 1. průběh cyklu, tehdy není s čím srovnávat, proto je uvedena podmínka i != 1
                    mezera = aktualni - predchozi                                               #mezera je počet dní chybějících mezi dnem v aktuálním cyklu a dnem v předchozím cyklu
                    for dira in range (1,int(mezera.days),1):                                   #Cyklus, který vypíše chybějící dny, z mezera volám rozdíl dnů
                        den = OdecetDni(aktualni.day, aktualni.month, aktualni.year, dira)      #Odečítám pomocí funkce OdecetDni od aktuálního dne postupně dira až do počtu chybějících dní
                        print(f"Chybí den {den.day}. {den.month}. {den.year}")
                predchozi = datetime.date(int(row[2]), int(row[3]), int(row[4]))                #Ukládá datum z aktuální iterace pro porovnání v iteraci příští



KontrolaDat("vstup.csv")
ChybejiciDny("vstup.csv")
TydenniPrumery("vstup.csv", "vystup_7dni.csv")
RocniPrumery("vstup.csv", "vystup_rok.csv")
MaxMinPrutok("vstup.csv")
print("Program úspěšně proběhl.")