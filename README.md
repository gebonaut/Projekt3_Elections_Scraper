# PROJEKT 3 - Elections Scraper

## Popis projektu
Programu slouží ke stažení dat z webu [**volby.cz**](https://volby.cz/), konkrétně z parlamentních voleb 2017 - [**
ukázka**](https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=2&xnumnuts=2101).

## Požadavky
Všechny potřebné knihovny jsou k dispozici v souboru [**requirements.txt**](https://github.com/gebonaut/Projekt3_Elections_Scraper/blob/master/requirements.txt)

## Instalace knihoven

1. Ověření verze manažeru 


    pip3 --version

2. Instalace knihoven ze souboru [**requirements.txt**](https://github.com/gebonaut/Projekt3_Elections_Scraper/blob/master/requirements.txt)

    
    pip3 install -r requirements.txt


## Spuštění programu
Spuštění programu příkazem v příkazové řádce vyžaduje dva povinné argumenty:

    python election-scraper.py "odkaz územního celku" "název výstupního souboru"

Program se spustí a vypisuje průběh stahování dat. 
Následně vygeneruje soubor s daty ve formátu '.csv'.

### Příklad spuštění:

1. První argument (odkaz):

    
    "https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=11&xnumnuts=6204"

2. Druhý argument (název výstupního souboru):


    "vysledky_breclav.csv"

3. Zadání: 

    
    python election-scraper.py "https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=11&xnumnuts=6204" "vysledky_breclav.csv"

4. Průběh stahování:

         Připojeno: kód 200, pokračuji ve stahování dat...
         Stahuju data z odkazu č. 0 pro obec Babice
               ✓ Úspěšně staženo
         --------------------------------------------------
         Stahuju data z odkazu č. 1 pro obec Bánov
         - Stahuju data jednotlivých okrsků obce č. 1 Bánov:
             • Stahuju data okrsku č. 1
               ✓ Úspěšně staženo
             • Stahuju data okrsku č. 2
               ✓ Úspěšně staženo
         --------------------------------------------------




