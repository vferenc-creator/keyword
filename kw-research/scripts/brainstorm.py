#!/usr/bin/env python3
"""Saját bővítési lista (brainstorm) a Kulcsszótervezőhöz – az Autocomplete helyett.

Kategória × módosító × márka mátrix vásárlói nyelvezettel. Keresésszámot NEM tartalmaz:
minden sor "brainstorm" forrású, validálatlan, amíg a Kulcsszótervező CSV vissza nem jön.

Futtatás (a kw-research/ mappából):
    python3 scripts/brainstorm.py -o 02_brainstorm.csv
"""
import argparse
import csv
from pathlib import Path

# Fő termékcsoportok -> fejkifejezések. Ezek kapják a teljes vásárlási módosítókészletet.
HEADS = {
    "Horgászbot": ["horgászbot", "horgászbotok", "pontyozó bot", "feeder bot", "method feeder bot",
                   "picker bot", "pergető bot", "match bot", "bojlis bot", "teleszkópos bot",
                   "rakós bot", "harcsázó bot", "spinning bot", "úszós bot", "bolognai bot",
                   "horgászbot szett", "gyerek horgászbot", "utazó horgászbot", "ultralight bot",
                   "süllőző bot", "csukázó bot", "heavy feeder bot", "spod bot", "marker bot"],
    "Orsó": ["horgász orsó", "horgászorsó", "nyeletőfékes orsó", "pontyozó orsó", "feeder orsó",
             "pergető orsó", "elsőfékes orsó", "hátsófékes orsó", "harcsázó orsó", "bojlis orsó",
             "big pit orsó", "match orsó", "multiplikátor orsó", "dobóorsó", "tengeri orsó"],
    "Zsinór": ["horgászzsinór", "fonott zsinór", "monofil zsinór", "fluorocarbon zsinór",
               "feeder zsinór", "pontyozó zsinór", "pergető zsinór", "harcsázó zsinór",
               "dobóelőke zsinór", "előkezsinór", "leadcore", "süllyedő zsinór"],
    "Előke, horog, aprócikk": ["kötött előke", "horgász előke", "bojlis előke", "feeder előke",
                               "horgász horog", "pontyozó horog", "feeder horog", "harcsázó horog",
                               "szakáll nélküli horog", "hármashorog", "forgó kapocs",
                               "gyorskapocs", "csali tű", "pva háló", "pva zsák", "gumi ütköző",
                               "hajszálelőke"],
    "Kosár, ólom, úszó": ["feeder kosár", "method kosár", "etetőkosár", "horgász ólom", "bojlis ólom",
                          "fülesólom", "csúszó ólom", "horgász úszó", "waggler úszó", "markerúszó",
                          "világító úszó", "spomb"],
    "Etetőanyag, csali": ["etetőanyag", "feeder etetőanyag", "pontyozó etetőanyag", "method mix",
                          "bojli", "oldódó bojli", "pop up bojli", "wafter", "horgász pellet", "etető pellet",
                          "method pellet", "csali pellet", "horgász aroma", "folyékony aroma", "bojli dip",
                          "bojli booster", "horgász csali", "horgász kukorica", "tigrismogyoró",
                          "kendermag", "gumi kukorica", "mű kukorica", "partikkel", "horgász melasz",
                          "etetőanyag adalék", "csonti", "szúnyoglárva", "csalikeverék"],
    "Műcsali": ["műcsali", "wobbler", "gumihal", "villantó", "támolygó villantó", "körforgó villantó",
                "popper műcsali", "twister csali", "jigfej", "spinnerbait", "pilker", "kuttyogató",
                "csukázó wobbler", "süllőző gumihal", "harcsázó műcsali", "balinozó wobbler",
                "műcsali szett", "gumihal szett", "wobbler szett"],
    "Kapásjelzés": ["kapásjelző", "elektromos kapásjelző", "kapásjelző szett", "vevős kapásjelző",
                    "swinger", "kapásjelző swinger", "horgász csengő"],
    "Botállvány, rod pod": ["botállvány", "rod pod", "horgász leszúró", "bottartó", "feeder botállvány",
                            "botartó fej", "feeder kar"],
    "Szák, pontymatrac": ["merítőszák", "pontyozó merítőszák", "merítőszák nyél", "merítőfej",
                          "haltartó szák", "pontymatrac", "pontybölcső", "mérlegelő zsák",
                          "halmérleg", "ponty fertőtlenítő"],
    "Szék, ágy, sátor, ernyő": ["horgászszék", "karfás horgászszék", "horgászágy", "horgászsátor",
                                "bivvy", "horgászernyő", "ernyősátor", "horgász hálózsák",
                                "sátor horgász 2 személyes"],
    "Láda, táska, doboz": ["horgászláda", "versenyláda", "feeder láda", "ülőláda", "horgásztáska",
                           "bottáska", "bottartó táska", "szerelékes doboz", "aprócikkes doboz",
                           "csalis doboz", "horgász hűtőtáska", "horgász vödör", "etetőanyag vödör"],
    "Ruházat": ["horgász ruházat", "horgászruha", "waders", "melles csizma", "combcsizma",
                "horgász bakancs", "horgász kabát", "horgász thermo ruha", "horgász esőruha",
                "horgász sapka", "horgász kesztyű", "horgász napszemüveg", "horgász póló",
                "horgász pulóver", "horgász mellény", "horgász nadrág"],
    "Etetőhajó, csónak, elektronika": ["etetőhajó", "gps etetőhajó", "horgászcsónak", "gumicsónak",
                                       "elektromos csónakmotor", "csónakmotor", "echolot",
                                       "halradar", "parti halradar", "horgász fejlámpa",
                                       "sátorlámpa", "horgász powerbank"],
    "Szett, felszerelés": ["horgászfelszerelés", "horgász felszerelés", "horgász kellékek",
                           "horgászcikk", "pontyozó felszerelés", "harcsázó felszerelés",
                           "feeder felszerelés", "pergető felszerelés", "csukázó felszerelés",
                           "süllőző felszerelés", "horgász szett", "horgász kezdő csomag",
                           "horgász ajándék", "horgász webshop", "horgász bolt", "horgászbolt",
                           "horgász webáruház", "horgász akció", "horgász nagyker"],
}

# Vásárlási / összehasonlító módosítók.
MODS_FULL = ["ár", "akció", "olcsó", "webshop", "vásárlás", "eladó", "használt", "legjobb",
             "vélemény", "teszt", "szett", "kezdőknek"]
MODS_LIGHT = ["ár", "akció", "olcsó", "legjobb", "vélemény"]
# Fogyóeszközöknél a "használt", "teszt", "kezdőknek" nem értelmes.
MODS_CONSUMABLE = ["ár", "akció", "olcsó", "webshop", "legjobb", "vélemény"]
CONSUMABLE_GROUPS = {"Zsinór", "Előke, horog, aprócikk", "Kosár, ólom, úszó", "Etetőanyag, csali"}
# A bolt-jellegű fejkifejezésekre ezek nem értelmesek.
NO_MODS = {"horgász webshop", "horgász bolt", "horgászbolt", "horgász webáruház", "horgász akció",
           "horgász nagyker", "horgász ajándék", "horgászbotok"}
# Az első N fejkifejezés kategóriánként kapja a teljes módosítókészletet, a többi a könnyűt.
FULL_PER_GROUP = 5

# Technikák / célhalak: vásárlói kombinációk.
TECHNIQUES = {
    "pontyhorgászat": ["pontyozó szerelék", "pontyozó bot és orsó", "pontyhorgász felszerelés",
                       "pontyozó készlet"],
    "harcsázás": ["harcsázó szerelék", "harcsázó csali", "harcsázó kuttyogató", "harcsázó bot és orsó",
                  "harcsázó készlet"],
    "csukázás": ["csukázó szerelék", "csukázó csali", "csukázó előke", "csukázó villantó",
                 "csukázó gumihal"],
    "süllőzés": ["süllőző szerelék", "süllőző csali", "süllőző wobbler", "süllőző jigfej"],
    "feederezés": ["feeder szerelék", "feeder szett", "feeder horgász készlet", "feeder kezdő szett"],
    "pergetés": ["pergető szett", "pergető készlet", "pergető műcsali", "pergető csali"],
    "fenekezés": ["fenekező bot", "fenekező szerelék", "fenekező készlet"],
    "egyéb": ["method feeder", "method feeder szerelék", "bojlis horgászat felszerelés",
              "úszós horgászat felszerelés", "keszegező bot", "balinozó műcsali", "pisztrángozó bot",
              "pisztráng csali", "amur csali", "jeges horgászat felszerelés", "téli horgászat ruha"],
}

# Márka × termékcsoport (csak ahol a márka ténylegesen jelen van az adott csoportban).
BRANDS = {
    ("shimano", "daiwa", "okuma", "penn", "abu garcia", "mitchell", "ryobi", "dam", "jaxon",
     "cormoran", "spro", "sänger"): ["bot", "orsó", "feeder bot", "pergető bot", "nyeletőfékes orsó"],
    ("fox", "korda", "nash", "trakker", "avid carp", "prologic", "gardner", "solar", "carp zoom",
     "carp expert", "carp academy", "mivardi", "delphin", "carp spirit", "nevis", "energoteam",
     "cralusso"): ["bot", "orsó", "kapásjelző", "rod pod", "szék", "sátor"],
    ("matrix", "preston", "guru", "browning", "korum", "by döme"): ["feeder bot", "orsó", "láda",
                                                                    "method kosár"],
    ("haldorádó", "sensas", "dynamite baits", "mainline", "starbaits", "ccmoore", "top mix",
     "timár mix", "benzar mix", "maros mix", "dovit", "carp zoom", "by döme"):
        ["etetőanyag", "bojli", "pellet", "aroma", "method mix"],
    ("rapala", "savage gear", "berkley", "salmo", "mepps", "westin"): ["wobbler", "gumihal",
                                                                       "villantó", "műcsali"],
    ("deeper", "lowrance", "garmin", "humminbird"): ["halradar", "echolot"],
    ("gamakatsu", "owner"): ["horog"],
    ("sufix",): ["fonott zsinór", "zsinór"],
}
# Puszta márkanév + "akció" csak az egyértelműen horgász márkáknál (pl. "shimano" = kerékpár is,
# "fox", "garmin", "ryobi" stb. más piacon is él); a többinél csak "<márka> horgász".
UNAMBIGUOUS_BRANDS = {"daiwa", "okuma", "abu garcia", "carp zoom", "carp expert", "carp academy",
                      "mivardi", "nevis", "energoteam", "cralusso", "jaxon", "by döme", "haldorádó",
                      "sensas", "dynamite baits", "mainline", "starbaits", "ccmoore", "timár mix",
                      "benzar mix", "maros mix", "avid carp", "prologic", "korum", "rapala",
                      "savage gear", "mepps", "westin", "cormoran", "gamakatsu", "sufix",
                      "carp spirit", "humminbird"}


def build() -> list[tuple[str, str]]:
    rows: dict[str, str] = {}

    def add(kw: str, group: str) -> None:
        kw = " ".join(kw.split()).lower()
        rows.setdefault(kw, group)

    for group, heads in HEADS.items():
        for i, h in enumerate(heads):
            add(h, group)
            if h in NO_MODS:
                continue
            if i >= FULL_PER_GROUP:
                mods = MODS_LIGHT
            elif group in CONSUMABLE_GROUPS:
                mods = MODS_CONSUMABLE
            else:
                mods = MODS_FULL
            for m in mods:
                add(f"{h} {m}", group)
    for tech, combos in TECHNIQUES.items():
        if tech != "egyéb":
            add(tech, "Technika")
            add(f"{tech} felszerelés", "Technika")
        for c in combos:
            add(c, "Technika")
    for brands, cats in BRANDS.items():
        for b in brands:
            add(f"{b} horgász", "Márka")
            if b in UNAMBIGUOUS_BRANDS:
                add(b, "Márka")
                add(f"{b} akció", "Márka")
            for c in cats:
                add(f"{b} {c}", "Márka")
    return sorted(rows.items(), key=lambda kv: (kv[1], kv[0]))


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("-o", "--output", default="02_brainstorm.csv")
    args = ap.parse_args()
    rows = build()
    with Path(args.output).open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f)
        w.writerow(["keyword", "sources", "product_group"])
        for kw, group in rows:
            w.writerow([kw, "brainstorm", group])
    print(f"{len(rows)} kulcsszó -> {args.output}")


if __name__ == "__main__":
    main()
