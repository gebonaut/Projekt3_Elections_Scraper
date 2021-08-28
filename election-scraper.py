import sys
import requests
from bs4 import BeautifulSoup
import pandas as pd

# -----------------------------------------------------------------------------
def oddelovac(sign="-"):
  """Klasický oddělovač"""
  print(sign*50)
# -----------------------------------------------------------------------------
def prevedeni_textu_na_cislo(text_k_prevedeni:str) -> int:
  """Kontroluje a převádí text na číslo ve správném formátu, protože se občas vyskytne chyba kódování..."""
  try:
    return int(text_k_prevedeni)
  except:
    return int(text_k_prevedeni[0] + text_k_prevedeni[-3:])
# -----------------------------------------------------------------------------
def stazeni_seznamu_obci(URL:str):
  """Kontroluje platnost URL a stahuje seznam obcí ve zvoleném okrese"""
  try:
    test_url = "https://volby.cz/pls/ps2017nss/"
    r = requests.get(URL)
    status = r.status_code
    if status == 200 and test_url in URL:
      oddelovac(sign='*')
      print(f'Připojeno: kód {status}, pokračuji ve stahování dat...')
      oddelovac(sign='*')
      html = r.text
      soup = BeautifulSoup(html, "html.parser")
      rows = soup.find_all('tr')[2:]
      dataset = list()
      for row in rows:
        try:
          cislo = row.find_all('td')[0].text
          obec = row.find_all('td')[1].text
          odkaz = f"https://volby.cz/pls/ps2017nss/{row.find_all('td')[2].a['href']}"
          dataset.append({'Kod obce':cislo, 'Název':obec, 'Odkaz':odkaz})
        except:
          continue
      konecny_list = dataset.copy()
      return konecny_list
    else:
      print(f'Nepřipojeno: kód {status}, ukončuji program.')
      exit()
  except:
    print(f"Neplatná adresa: {URL}")
    exit()
# -----------------------------------------------------------------------------
def scitani_stran(soup, obec):
  # data všech stran
  strany_data = soup.find_all('table')[1].find_all('tr')[2:] + soup.find_all('table')[2].find_all('tr')[2:]
  for strana in strany_data:
    nazev_strany = strana.find_all('td')[1].text
    # kontrola, že strana je platná a převede hlasy na číslo
    if nazev_strany != '-':
      pocet_hlasu = prevedeni_textu_na_cislo(strana.find_all('td')[2].text)
      # přičtení hlasů strany
      if nazev_strany in obec.keys():
        obec[nazev_strany] += pocet_hlasu
      else:
        obec[nazev_strany] = pocet_hlasu
    else:
      print('Neplatná strana')
# -----------------------------------------------------------------------------
def stazeni_dat_obci(seznam_obci):
  """Stahuje data ze seznamu obcí a jejich okrsků"""
  ok = 0
  nok = 0
  for cislo_obce, obec in enumerate(seznam_obci):
    print(f"Stahuju data z odkazu č. {cislo_obce} pro obec {obec['Název']}")
    r2 = requests.get(obec['Odkaz'])
    html2 = r2.text
    soup2 = BeautifulSoup(html2, "html.parser")
    if soup2.find('th').text != 'Okrsek':
      try:
        obec['Volici'] = prevedeni_textu_na_cislo(soup2.find_all('td')[3].text)
        obec['Vydané obálky'] = prevedeni_textu_na_cislo(soup2.find_all('td')[4].text)
        obec['Platné hlasy'] = prevedeni_textu_na_cislo(soup2.find_all('td')[7].text)

        # Sčítání hlasů stran pro obec bez okrsků
        scitani_stran(soup2, obec)
        print(f"      ✓ Úspěšně staženo")
        ok += 1
      except:
        print('✗ Chyba formátu webu, nebo špatné URL.')
        nok += 1
      finally:
        oddelovac()
    else:
      # Obec má okrsky
      print(f"- Stahuju data jednotlivých okrsků obce č. {cislo_obce} {obec['Název']}:")
      okrsky = soup2.find_all('td')
      try:
        for cislo_okrsku, okrsek in enumerate(okrsky):
          # vygeneruje odkaz okrsku
          odkaz_okrsku = f"https://volby.cz/pls/ps2017nss/{soup2.find_all('td')[cislo_okrsku].a['href']}"
          print(f"    • Stahuju data okrsku č. {cislo_okrsku+1}")
          # Stahuje data jednotlivých okrsků dle vygenerovaných odkazů
          r3 = requests.get(odkaz_okrsku)
          html3 = r3.text
          soup3 = BeautifulSoup(html3, "html.parser")
          # data volici
          volici = prevedeni_textu_na_cislo(soup3.find_all('td')[0].text)
          vydane_obalky = prevedeni_textu_na_cislo(soup3.find_all('td')[1].text)
          platne_hlasy = prevedeni_textu_na_cislo(soup3.find_all('td')[4].text)
          if 'Volici' in obec.keys():
            # pokud Volici existují, přičti
            obec['Volici'] += volici
            obec['Vydané obálky'] += vydane_obalky
            obec['Platné hlasy'] += platne_hlasy
          else:
            # pokud Volici neexistují, vytvoř
            obec['Volici'] = volici
            obec['Vydané obálky'] = vydane_obalky
            obec['Platné hlasy'] = platne_hlasy

          # Sčítání hlasů stran pro obec s okrsky
          scitani_stran(soup3, obec)
          print(f"      ✓ Úspěšně staženo")
          ok += 1
      except:
        print(f"✗ Neplatný formát následujícího okrsku")
        continue
      finally:
        oddelovac()
  oddelovac(sign="*")
  print(
    f'Stažení dat KOMPLETNÍ!\n'
    f'Úspěšně: {ok}\n'
    f'Chyb: {nok}'
  )
  oddelovac(sign="*")
  oddelovac()
  return seznam_obci
# -----------------------------------------------------------------------------
def zpracovani_vystupu(dataframe):
  upravena_data = pd.DataFrame(dataframe)
  upravena_data.drop(columns='Odkaz', inplace=True)
  upravena_data.rename(
    columns={
      'Kod obce': 'Kód obce',
      'Název': 'Název obce',
      'Volici': 'Voliči v seznamu'
    },
    inplace=True
  )
  return upravena_data
# -----------------------------------------------------------------------------
def vystup_do_csv(data_k_vystupu,nazev_souboru):
  data_k_vystupu.to_csv(nazev_souboru, index=False, encoding='utf8')
  oddelovac(sign='*')
  print(f'Soubor {nazev_souboru} byl úspěšně vygenerován.')
  print(f'Ukončuji program Election scraper.')
  oddelovac(sign='*')
# -----------------------------------------------------------------------------
def kontrola_nazvu_souboru(nazev_souboru):
  """Kontroluje, jestli název souboru zadaný uživatelem má správnou příponu, popřípadě ji přidá a pokračuje."""
  try:
    if nazev_souboru[-4:] == '.csv':
      return nazev_souboru.lower()
    else:
      nazev_souboru = nazev_souboru + '.csv'
      oddelovac()
      print(f"Název souboru musí obsahovat příponu '.csv' - nový název: {nazev_souboru}")
      oddelovac()
      return nazev_souboru.lower()
  except:
    oddelovac()
    print('Neplatné zadání názvu souboru. Ukončuji program.')
    oddelovac()
    exit()
# -----------------------------------------------------------------------------
def main():
  URL = str(sys.argv[1])
  nazev_souboru = kontrola_nazvu_souboru(sys.argv[2])
  seznam_obci = stazeni_seznamu_obci(URL)
  dataframe = stazeni_dat_obci(seznam_obci)
  upravena_data = zpracovani_vystupu(dataframe)
  vystup_do_csv(upravena_data, nazev_souboru)
# -----------------------------------------------------------------------------
if __name__ == '__main__':
  main()