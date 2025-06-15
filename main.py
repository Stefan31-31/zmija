import pygame
import random
import sys
import os

pygame.init()
pygame.mixer.init()

# Učitaj muziku odmah nakon inicijalizacije
pygame.mixer.music.load("muzika/muzika.mp3")
pygame.mixer.music.set_volume(0.5)

sirina, visina = 600, 600
background_slika = pygame.transform.scale(pygame.image.load("meni/background_slika.png"), (sirina, visina))
velicina_bloka = 20
prozor = pygame.display.set_mode((sirina, visina))
pygame.display.set_caption("Zmija")

BIJELA = (255, 255, 255)
TAMNOZELENA = (0, 51, 0)
SIVA = (100, 100, 100)
SVETLOZELENA_POZADINA = (50, 150, 50)  # Pozadina za rezultat

prostor_za_tekst = 60  # visina prostora za rezultat na vrhu

# Ucitaj slike
slike_glava = {
    "GORE": pygame.transform.scale(pygame.image.load("tijelo/glava_gore.png"), (velicina_bloka, velicina_bloka)),
    "DOLJE": pygame.transform.scale(pygame.image.load("tijelo/glava_dolje.png"), (velicina_bloka, velicina_bloka)),
    "LIJEVO": pygame.transform.scale(pygame.image.load("tijelo/glava_lijevo.png"), (velicina_bloka, velicina_bloka)),
    "DESNO": pygame.transform.scale(pygame.image.load("tijelo/glava_desno.png"), (velicina_bloka, velicina_bloka))
}

slike_tijelo = {
    "GORE": pygame.transform.scale(pygame.image.load("tijelo/tijelo_gore.png"), (velicina_bloka, velicina_bloka)),
    "DOLJE": pygame.transform.scale(pygame.image.load("tijelo/tijelo_dolje.png"), (velicina_bloka, velicina_bloka)),
    "LIJEVO": pygame.transform.scale(pygame.image.load("tijelo/tijelo_lijevo.png"), (velicina_bloka, velicina_bloka)),
    "DESNO": pygame.transform.scale(pygame.image.load("tijelo/tijelo_desno.png"), (velicina_bloka, velicina_bloka))
}

slike_rep = {
    "GORE": pygame.transform.scale(pygame.image.load("tijelo/rep_gore.png"), (velicina_bloka, velicina_bloka)),
    "DOLJE": pygame.transform.scale(pygame.image.load("tijelo/rep_dolje.png"), (velicina_bloka, velicina_bloka)),
    "LIJEVO": pygame.transform.scale(pygame.image.load("tijelo/rep_lijevo.png"), (velicina_bloka, velicina_bloka)),
    "DESNO": pygame.transform.scale(pygame.image.load("tijelo/rep_desno.png"), (velicina_bloka, velicina_bloka))
}

slika_hrana = pygame.transform.scale(pygame.image.load("hrana/hrana.png"), (velicina_bloka, velicina_bloka))
slika_pecurka = pygame.transform.scale(pygame.image.load("hrana/pecurka.png"), (velicina_bloka, velicina_bloka))

font = pygame.font.SysFont("Courier", 24, bold=True)
sat = pygame.time.Clock()
fps = 10

putanja_top10 = "top10.txt"

def ucitaj_top10():
    if not os.path.exists(putanja_top10):
        return [{"ime": "Niko", "rezultat": 0} for _ in range(10)]
    top_lista = []
    with open(putanja_top10, "r", encoding="utf-8") as f:
        for linija in f:
            delovi = linija.strip().split(" ")
            if len(delovi) >= 2:
                ime = " ".join(delovi[:-1])
                try:
                    rezultat = int(delovi[-1])
                except:
                    rezultat = 0
                top_lista.append({"ime": ime, "rezultat": rezultat})
    while len(top_lista) < 10:
        top_lista.append({"ime": "Niko", "rezultat": 0})
    return top_lista[:10]

def sacuvaj_top10(ime, rezultat):
    top_lista = ucitaj_top10()
    vec_postoji = False
    for zapis in top_lista:
        if zapis["ime"] == ime:
            vec_postoji = True
            if rezultat > zapis["rezultat"]:
                zapis["rezultat"] = rezultat
            break
    if not vec_postoji:
        top_lista.append({"ime": ime, "rezultat": rezultat})
    top_lista.sort(key=lambda x: x["rezultat"], reverse=True)
    top_lista = top_lista[:10]
    with open(putanja_top10, "w", encoding="utf-8") as f:
        for zapis in top_lista:
            f.write(f"{zapis['ime']} {zapis['rezultat']}\n")

def nova_hrana(zmija):
    while True:
        x = random.randint(0, (sirina - velicina_bloka) // velicina_bloka) * velicina_bloka
        y = random.randint(prostor_za_tekst // velicina_bloka, (visina - velicina_bloka) // velicina_bloka) * velicina_bloka
        if [x, y] not in zmija:
            return [x, y]

def nova_pecurka(zmija, hrana):
    while True:
        x = random.randint(0, (sirina - velicina_bloka) // velicina_bloka) * velicina_bloka
        y = random.randint(prostor_za_tekst // velicina_bloka, (visina - velicina_bloka) // velicina_bloka) * velicina_bloka
        if [x, y] not in zmija and [x, y] != hrana:
            return [x, y]

def prikazi_tekst(tekst, y, boja=BIJELA):
    prikaz = font.render(tekst, True, boja)
    rect = prikaz.get_rect(center=(sirina // 2, y))
    prozor.blit(prikaz, rect)

def dugme_tekst(poruka, x, y, sir, vis):
    pygame.draw.rect(prozor, SIVA, (x, y, sir, vis))
    tekst = font.render(poruka, True, BIJELA)
    tekst_rect = tekst.get_rect(center=(x + sir // 2, y + vis // 2))
    prozor.blit(tekst, tekst_rect)

def smjer_izmedju(pocetak, kraj):
    if kraj[0] > pocetak[0]: return "DESNO"
    if kraj[0] < pocetak[0]: return "LIJEVO"
    if kraj[1] > pocetak[1]: return "DOLJE"
    return "GORE"

def prikazi_poraz(ime_igraca, rezultat):
    pygame.mixer.music.stop()
    while True:
        #prozor.fill((0, 0, 0))
        prozor.blit(background_slika, (0, 0))
        prikazi_tekst("Izgubili ste! Pokusajte opet.", 200)
        dugme_tekst("Pokusaj opet", 180, 300, 240, 60)
        dugme_tekst("Povratak na meni", 180, 380, 240, 60)
        pygame.display.flip()
        for dogadjaj in pygame.event.get():
            if dogadjaj.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if dogadjaj.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if 180 < x < 420 and 300 < y < 360:
                    igra(ime_igraca)
                    return
                if 180 < x < 420 and 380 < y < 440:
                    return

def igra(ime_igraca):
    pygame.mixer.music.play(-1)
    zmija = [[300, 300]]
    smjer = "GORE"
    hrana = nova_hrana(zmija)
    rezultat = 0
    global fps
    fps = 10

    # Varijable za pečurku
    pecurka = None
    pecurka_efekat = None
    vrijeme_efekta = 0
    vrijeme_poruke = 0
    tekst_poruke = ""

    top_lista = ucitaj_top10()
    najbolji = top_lista[0] if top_lista else {"ime": "Niko", "rezultat": 0}

    while True:
        sledeci_smjer = smjer
        for dogadjaj in pygame.event.get():
            if dogadjaj.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if dogadjaj.type == pygame.KEYDOWN:
                if dogadjaj.key == pygame.K_w and smjer != "DOLJE":
                    sledeci_smjer = "GORE"
                elif dogadjaj.key == pygame.K_s and smjer != "GORE":
                    sledeci_smjer = "DOLJE"
                elif dogadjaj.key == pygame.K_a and smjer != "DESNO":
                    sledeci_smjer = "LIJEVO"
                elif dogadjaj.key == pygame.K_d and smjer != "LIJEVO":
                    sledeci_smjer = "DESNO"
                elif dogadjaj.key == pygame.K_ESCAPE:
                    pauza_meni()
        smjer = sledeci_smjer

        glava = list(zmija[0])
        if smjer == "GORE":
            glava[1] -= velicina_bloka
            if glava[1] < prostor_za_tekst:
                glava[1] = visina - velicina_bloka
        elif smjer == "DOLJE":
            glava[1] += velicina_bloka
            if glava[1] >= visina:
                glava[1] = prostor_za_tekst
        elif smjer == "LIJEVO":
            glava[0] -= velicina_bloka
            if glava[0] < 0:
                glava[0] = sirina - velicina_bloka
        elif smjer == "DESNO":
            glava[0] += velicina_bloka
            if glava[0] >= sirina:
                glava[0] = 0

        if glava in zmija:
            sacuvaj_top10(ime_igraca, rezultat)
            prikazi_poraz(ime_igraca, rezultat)
            return

        zmija.insert(0, glava)

        trenutno = pygame.time.get_ticks()

        # Pojedenje hrane
        if glava == hrana:
            dodaj = 20 if pecurka_efekat == "dupli_poeni" else 10
            rezultat += dodaj
            hrana = nova_hrana(zmija)
            fps += 0.2
            if pecurka_efekat == "dupli_poeni":
                zmija.insert(0, list(zmija[0]))
            if pecurka is None and random.random() < 0.07:
                pecurka = nova_pecurka(zmija, hrana)
        else:
            zmija.pop()

        # Pojedenje pečurke
        if pecurka and glava == pecurka:
            efekat = random.choice(["brzina", "dupli_poeni"])
            pecurka_efekat = efekat
            vrijeme_efekta = trenutno
            vrijeme_poruke = trenutno
            tekst_poruke = "Efekat: Ubrzanje trajanje 20sek!" if efekat == "brzina" else "Efekat: Dupli poeni trajanje 20sek!"
            if efekat == "brzina":
                fps *= 1.17
            pecurka = None

        # Kraj trajanja efekta
        if pecurka_efekat and trenutno - vrijeme_efekta > 20000:
            if pecurka_efekat == "brzina":
                fps /= 1.17
            pecurka_efekat = None

        prozor.fill(TAMNOZELENA)
        pygame.draw.rect(prozor, SVETLOZELENA_POZADINA, (0, 0, sirina, prostor_za_tekst))
        tekst_rez = f"Rezultat: {rezultat}    Najbolji: {najbolji['ime']} {najbolji['rezultat']}"
        prikazi_tekst(tekst_rez, prostor_za_tekst // 2)

        for i in range(len(zmija)):
            if i == 0:
                s = smjer_izmedju(zmija[1], zmija[0]) if len(zmija) > 1 else smjer
                prozor.blit(slike_glava[s], zmija[i])
            elif i == len(zmija) - 1:
                s = smjer_izmedju(zmija[-1], zmija[-2])
                prozor.blit(slike_rep[s], zmija[i])
            else:
                s = smjer_izmedju(zmija[i + 1], zmija[i])
                prozor.blit(slike_tijelo[s], zmija[i])

        prozor.blit(slika_hrana, hrana)
        if pecurka:
            prozor.blit(slika_pecurka, pecurka)
        if tekst_poruke and trenutno - vrijeme_poruke < 6000:
            prikazi_tekst(tekst_poruke, prostor_za_tekst + 30, (255, 255, 0))

        pygame.display.flip()
        sat.tick(fps)

def prikazi_top10():
    top_lista = ucitaj_top10()
    while True:
        #prozor.fill((0, 0, 0))
        prozor.blit(background_slika, (0, 0))
        prikazi_tekst("TOP 10 REZULTATA", 50)
        y = 100
        for i, zapis in enumerate(top_lista):
            prikazi_tekst(f"{i+1}. {zapis['ime']} - {zapis['rezultat']}", y)
            y += 30
        dugme_tekst("Povratak na meni", 180, 500, 240, 60)
        pygame.display.flip()
        for dogadjaj in pygame.event.get():
            if dogadjaj.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if dogadjaj.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if 180 < x < 420 and 500 < y < 560:
                    return

def unos_imena():
    ime = ""
    aktivno = True
    while aktivno:
        #prozor.fill((0, 0, 0))
        prozor.blit(background_slika, (0, 0))
        prikazi_tekst("Unesite korisnicko ime:", 200)
        tekst_ime = font.render(ime, True, BIJELA)
        prozor.blit(tekst_ime, tekst_ime.get_rect(center=(sirina // 2, 300)))
        dugme_tekst("Pocni igru", 180, 400, 240, 60)
        pygame.display.flip()
        for dogadjaj in pygame.event.get():
            if dogadjaj.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if dogadjaj.type == pygame.KEYDOWN:
                if dogadjaj.key == pygame.K_RETURN and ime:
                    aktivno = False
                elif dogadjaj.key == pygame.K_BACKSPACE:
                    ime = ime[:-1]
                elif dogadjaj.unicode.isprintable() and len(ime) < 15:
                    ime += dogadjaj.unicode
            if dogadjaj.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if 180 < x < 420 and 400 < y < 460 and ime:
                    aktivno = False
    return ime
def pauza_meni():
    pauza_aktivna = True
    while pauza_aktivna:
        prozor.blit(background_slika, (0, 0))
        prikazi_tekst("PAUZA", 150)
        dugme_tekst("Nastavi igru", 180, 250, 240, 60)
        dugme_tekst("Povratak na meni", 180, 330, 240, 60)
        pygame.display.flip()

        for dogadjaj in pygame.event.get():
            if dogadjaj.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if dogadjaj.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if 180 < x < 420 and 250 < y < 310:
                    pauza_aktivna = False  # Nastavi igru
                elif 180 < x < 420 and 330 < y < 390:
                    meni()  # Povratak na meni
                    return
            if dogadjaj.type == pygame.KEYDOWN:
                if dogadjaj.key == pygame.K_ESCAPE:
                    pauza_aktivna = False  # Nastavi igru ako opet pritisne ESC

def meni():
    while True:
        #prozor.fill((0, 0, 0))
        prozor.blit(background_slika, (0, 0))
        prikazi_tekst("ZMIJA", 150)
        dugme_tekst("Nova igra", 180, 250, 240, 60)
        dugme_tekst("Top 10", 180, 330, 240, 60)
        dugme_tekst("Izlaz", 180, 410, 240, 60)
        pygame.display.flip()
        for dogadjaj in pygame.event.get():
            if dogadjaj.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if dogadjaj.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if 180 < x < 420 and 250 < y < 310:
                    ime = unos_imena()
                    if ime:
                        igra(ime)
                elif 180 < x < 420 and 330 < y < 390:
                    prikazi_top10()
                elif 180 < x < 420 and 410 < y < 470:
                    pygame.quit()
                    sys.exit()

meni()