# Modul za automatizaciju online školice za život
# Napisao Jurek Runtas <runtas.j@gmail.com>
# Copyright (C) 2020 Jurica Runtas

# Motivacijski hashtagovi
# #naprednoObjektnoProgramiranje
# #naprednoKorištenjeSustavaLinux
# #ovoVŠkoliciNebušNavčil

# TODO: napravit grafičko sučelje (jesi zadovoljan prokletniče Leo Budin?)

import time
import random
import os
import shutil
import sys
import requests
import zipfile
import stat
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

def download_driver():
  if not os.path.isfile("chromedriver"):
    if sys.platform == "win32": url = "https://chromedriver.storage.googleapis.com/87.0.4280.88/chromedriver_win32.zip"
    elif sys.platform == "linux": url = "https://chromedriver.storage.googleapis.com/87.0.4280.88/chromedriver_linux64.zip"
    elif sys.platform == "darwin": url = "https://chromedriver.storage.googleapis.com/87.0.4280.88/chromedriver_mac64.zip"
    download_driver = requests.get(url, stream=True)
    if download_driver.ok:
      with open("chromedriver_zip", "wb") as driver:
        shutil.copyfileobj(download_driver.raw, driver)
      
      with zipfile.ZipFile("chromedriver_zip", "r") as chromedriver_zip:
        chromedriver_zip.extractall("chromedriver_extracted")
      
      shutil.move(os.path.join("chromedriver_extracted", "chromedriver"), os.path.abspath(os.path.dirname(__file__)))
      os.rmdir("chromedriver_extracted")
      os.remove("chromedriver_zip")
      st = os.stat('chromedriver')
      os.chmod('chromedriver', st.st_mode | stat.S_IEXEC)

class PitajDrazena:
  def __init__(self, predmet, faktor_ocajnosti=0.5, drazen_na_wappu="Dražen Šarić"):
    self.predmeti = {"Sklopovska oprema računala": ["sklopovsku", "koscicu"],
                     "Dijagnostika i održavanje": ["dijagnostiku"],
                     "Sustavna programska potpora": ["spp", "sustavnu"],
                     "Elektronička instrumentacija": ["dudeka", "instrumentaciju"],
                     "Matematika": ["matisu", "majdu"],
                     "Hrvatski jezik": ["hrvatski"],
                     "Digitalna elektronika": ["galeta", "digitalnu"],
                     "Politika i gospodarstvo": ["politku"],
                     "Engleski jezik": ["engleski"],
                     "Radioničke vježbe": ["vlanica", "radionicke"],
                     "Pametne kuće": ["za pametne kuće", "vlainica"],
                     "Automatsko vođenje procesa": ["avp", "cuksa"],
                     "Fizika": ["siksa", "fiziku"]}
    assert predmet in self.predmeti.keys(), "Kaje to predmet?"
    self.predmet = self.predmeti[predmet]
    self.faktor_ocajnosti = faktor_ocajnosti
    self.drazen_na_wappu = drazen_na_wappu

  def stvori_pitanje(self):
    if self.faktor_ocajnosti <= 0.25:
      pitanje1 = "E daj mi posalji %s kad napises" % random.choice(self.predmet)
      pitanje2 = "E si mozda %s napiso?" % random.choice(self.predmet)
      pitanje3 = "Jesi kojim slucajem sklepal %s" % random.choice(self.predmet)
      pitanje4 = "Posaljes %s" % random.choice(self.predmet)
    elif self.faktor_ocajnosti > 0.25 and self.faktor_ocajnosti <= 0.5:
      pitanje1 = "Kaj mi mozes poslat %s kad napises?" % random.choice(self.predmet)
      pitanje2 = "Kaj bi mi mogo poslat %s?" % random.choice(self.predmet)
      pitanje3 = "Jel mi mozes poslat %s?" % random.choice(self.predmet)
      pitanje4 = "E kaj si napiso %s? Kaj mi mozes poslat ak jesi" % random.choice(self.predmet)
    elif self.faktor_ocajnosti > 0.5:
      pitanje1 = "Kaj mi mozes molim te poslat %s kad napises?" % random.choice(self.predmet)
      pitanje2 = "E jesi napiso %s? Fakat nezz kak to ide" % random.choice(self.predmet)
      pitanje3 = "E daj mi pls posalji %s" % random.choice(self.predmet)
      pitanje4 = "Jel mi mozes molim te poslat %s ak si napiso" % random.choice(self.predmet)
    
    pitanje = random.choice([pitanje1, pitanje2, pitanje3, pitanje4])
    return pitanje+"*"

  def pitaj_drazena(self):
    search_bar = "/html/body/div[1]/div/div/div[3]/div/div[1]/div/label/div/div[2]" 
    drazen_element = "/html/body/div[1]/div/div/div[3]/div/div[2]/div[1]/div/div/div[1]/div/div/div[2]/div[1]/div[1]/span/span"
    type_a_message_bar = "/html/body/div[1]/div/div/div[4]/div/footer/div[1]/div[2]/div/div[2]"
    
    driver_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), "chromedriver")
    driver = webdriver.Chrome(executable_path=driver_path)
    driver.get("https://web.whatsapp.com")
    print("Daj skeniraj QR kod buraz")
    
    # searchaj drazena
    search = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, search_bar)))
    search.click()
    time.sleep(2)
    search.send_keys(self.drazen_na_wappu)
    time.sleep(2)
    
    # napravi pitanje i odi na drazena
    #pitanje = self.stvori_pitanje()
    pitanje = "Fakada*"
    drazen = driver.find_element_by_xpath(drazen_element)
    time.sleep(2)
    drazen.click() 
    
    # posalji poruku
    input_box = driver.find_element_by_xpath(type_a_message_bar)
    time.sleep(2)
    input_box.send_keys(pitanje + Keys.ENTER)
    time.sleep(2) 
    
    driver.quit()

if __name__ == "__main__":
  assert len(sys.argv) > 2, "Moje najdublje isprike. Potrebno je unijeti ime predmeta i faktor očajnosti."
  predmet = " ".join(sys.argv[1:-1])
  faktor_ocajnosti = float(sys.argv[-1])
  download_driver()
  drazen = PitajDrazena(predmet, faktor_ocajnosti)
  drazen.pitaj_drazena()
