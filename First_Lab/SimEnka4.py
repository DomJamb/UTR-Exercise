from sys import stdin

#funkcija za dodavanje stanja epsilon okoline u skup trenutnih stanja
#ako je na kraju prosirivanja skup trenutnih stanja prazan, u skup se dodaje oznaka #
def prosiriEpsilonOkolinu(trenutna_stanja, mapa_prijelaza):

    nova_stanja = set()
    promjena = True

    while promjena:
        promjena = False
        for stanje in trenutna_stanja:
            if stanje in mapa_prijelaza:
                if ("$" in mapa_prijelaza[stanje]):
                    for novo_stanje in (mapa_prijelaza[stanje])['$']:
                        if novo_stanje not in nova_stanja:
                            nova_stanja.add(novo_stanje)
        for novo_stanje in nova_stanja:
            if (novo_stanje not in trenutna_stanja):
                trenutna_stanja.add(novo_stanje)
                promjena = True

    if len(trenutna_stanja) == 0:
        trenutna_stanja.add('#')

    nova_stanja.clear()

#funkcija za pretvorbu skupa trenutnih stanja u string kako bi se ostvario laksi ispis
def pripremiIspis(trenutna_stanja):

    ispis = ""
    for stanje in trenutna_stanja:
        ispis += (stanje + ",")

    ispis = ispis[0:len(ispis) - 1]

    return ispis

#glavni program
if __name__ == '__main__':

    #parsiranje ulaznog dokumenta
    line = input()
    ulazni_nizovi = line.split("|")

    line = input()
    moguca_stanja = line.split(",")

    line = input()
    abeceda = line.split(",")

    line = input()
    prihvatljiva_stanja = line.split(",")

    pocetno_stanje = input()

    #kreiranje mape prijelaza
    mapa_prijelaza = {}

    for stanje in moguca_stanja:
        mapa = {}
        mapa_prijelaza[stanje] = mapa

    for line in stdin:
        line = line.strip()
        parsirana_linija = line.split("->")
        prvi_dio = parsirana_linija[0].split(",")
        drugi_dio = parsirana_linija[1].split(",")
        if ("#" not in drugi_dio):
            (mapa_prijelaza[prvi_dio[0]])[prvi_dio[1]] = drugi_dio

    #simuliranje rada e-nka
    for niz in ulazni_nizovi:

        trenutni_niz = niz.split(",")
        trenutna_stanja = {pocetno_stanje}
        nova_stanja = set()

        for znak in trenutni_niz:

            prosiriEpsilonOkolinu(trenutna_stanja, mapa_prijelaza)

            ispis = pripremiIspis(sorted(trenutna_stanja))
            print(ispis + "|", end = "")

            for stanje in trenutna_stanja:
                if stanje in mapa_prijelaza:
                    if znak in mapa_prijelaza[stanje]:
                        for novo_stanje in (mapa_prijelaza[stanje])[znak]:
                            if novo_stanje not in nova_stanja:
                                nova_stanja.add(novo_stanje)

            trenutna_stanja.clear()
            trenutna_stanja.update(nova_stanja)
            if len(trenutna_stanja) == 0:
                trenutna_stanja.add('#')

            nova_stanja.clear()

            prosiriEpsilonOkolinu(trenutna_stanja, mapa_prijelaza)

        ispis = pripremiIspis(sorted(trenutna_stanja))
        print(ispis)

        trenutna_stanja.clear()