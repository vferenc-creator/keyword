# Kulcsszótervező – letöltési útmutató

Ebben a mappában ezek a fájlok vannak:

| Fájl | Mire való |
|---|---|
| `01_volumen_lista_1.txt` | 2413 kulcsszó (ábécérendben az első fele). **Keresési volumen** kell hozzá (A rész). |
| `01_volumen_lista_2.txt` | 2413 kulcsszó (a második fele). Ugyanígy, **külön futtatásban** (A rész). |
| `02_felfedezes_seedcsoportok.txt` | 8 seed-csoport **új ötletekhez** (B rész, nem kötelező). |

A 4826 kulcsszó forrása: 78 seed, Google Autocomplete-javaslatok (base és commercial mód
minden seed-re, letters mód a 10 legfontosabbra), plusz egy saját termékcsoport × módosító ×
márka mátrix. A nem horgászatos találatokat már kiszűrtem (lásd `../negatives.txt`).
Minden visszakapott CSV-t a merge egyesít, és kiszűri a duplikációkat.

Letöltés GitHubról: nyisd meg a fájlt a `claude/zealous-lamport-oajv6j` ágon, és kattints a
**Raw** gombra (vagy a letöltés ikonra).

---

## A) Keresési volumen és előrejelzések (kötelező)

1. Nyisd meg az ads.google.com oldalt, és válts **Szakértői módra**, ha a fiók Smart módban van.
2. **Eszközök** (csavarkulcs ikon) → **Tervezés** → **Kulcsszótervező**.
3. Válaszd ezt: **Keresési volumen és előrejelzések lekérése**.
4. Másold be a `01_volumen_lista_1.txt` teljes tartalmát, vagy a **Fájl feltöltése** opcióval töltsd
   fel magát a fájlt. Kattints a **Kezdés** gombra.
5. A találati oldal tetején állítsd be:
   - **Helyek:** Magyarország (minden más helyet törölj, alapból lehet több is).
   - **Nyelv:** magyar.
   - **Keresési hálózat:** **Google** (ne a „Google és keresési partnerek”).
   - **Időszak:** az utolsó 24 teljes hónap, azaz **2024. okt. – 2026. szept.** (az aktuális,
     félig eltelt hónapot ne vedd bele).
6. Válts az **Előzménymutatók** fülre (nem az „Előrejelzés” fülre).
7. Kattints a **Letöltés** ikonra (lefelé mutató nyíl) → **Előzménymutatók tervezése** /
   **.csv** formátum. Ne Google Táblázatként töltsd le.
8. A fájlt ne nyisd meg és ne mentsd újra Excelben (UTF-16 kódolású, az Excel elronthatja).
   Átnevezni szabad, pl. `kt_volumen_1.csv`.
9. Ismételd meg a 3–8. lépést a `01_volumen_lista_2.txt` fájllal is (`kt_volumen_2.csv`).
   Ellenőrizd, hogy a beállítások (hely, nyelv, hálózat, időszak) ugyanazok maradtak.

> Ha a fiókban kevés a hirdetési költés, a volumen sávosan jelenik meg (pl. „1 E – 10 E”).
> Ez nem hiba, a feldolgozás kezeli; a riportban jelezni fogom, hol sávos az adat.

## B) Új kulcsszavak felfedezése (ajánlott)

Csoportonként egyszer (8 futtatás):

1. **Kulcsszótervező** → **Új kulcsszavak felfedezése** → **Kezdés kulcsszavakkal**.
2. Másold be a `02_felfedezes_seedcsoportok.txt` egy csoportjának sorát (a vesszővel elválasztott
   kifejezéseket; a `#` kezdetű sort ne).
3. A webhely mezőt hagyd üresen. **Eredmények megjelenítése**.
4. Ugyanazok a beállítások, mint fent: Magyarország, magyar, **Google** hálózat, utolsó 24 hónap.
5. **Kulcsszóötletek letöltése** → **.csv**. Nevezd el sorszámmal: `kt_otletek_1.csv` …
   `kt_otletek_8.csv`.

Az Autocomplete már lefedte a valós long-tail kereséseket, ezért ez a rész most opcionális.
Ha időd engedi, legalább az 1–3. csoportot (botok, orsók, zsinór/előke/etetőanyag) futtasd le.

## Feltöltés GitHubra

1. A GitHubon nyisd meg a repót, és válts a **`claude/zealous-lamport-oajv6j`** ágra.
2. Lépj be a `kw-research/input/` mappába → **Add file** → **Upload files**.
3. Húzd be az összes CSV-t, és commitold közvetlenül erre az ágra.
4. Szólj nekem: lehúzom őket (`git pull`), és folytatom a 6. lépéssel (egyesítés, szándék,
   klaszterezés, pontozás, riport).
