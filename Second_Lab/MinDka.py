from sys import stdin

#funkcija za uklanjanje nedohvatljivih stanja
def ukloni_nedohvatljiva(dohvatljiva_stanja, mapa_prijelaza, abeceda):

    promjena = True
    while promjena:
        promjena = False
        nova_stanja = set()
        for stanje in dohvatljiva_stanja:
            if stanje in mapa_prijelaza:
                for znak in abeceda:
                    if znak in mapa_prijelaza[stanje]:
                        nova_stanja.add((mapa_prijelaza[stanje])[znak])
        for stanje in nova_stanja:
            if stanje not in dohvatljiva_stanja:
                dohvatljiva_stanja.add(stanje)
                promjena = True
    return dohvatljiva_stanja

#funkcija za oznacavanje istovjetnih stanja u donjoj trokutastoj matrici
def oznaci_istovjetna(dohvatljiva_stanja, prihvatljiva_stanja, abeceda):

    istovjetna_stanja = [[True for x in range(len(dohvatljiva_stanja) - 1)] for y in range(len(dohvatljiva_stanja) - 1)]
    promjena = True

    for i in range(len(dohvatljiva_stanja) - 1):
        for j in range(i + 1):
            if (istovjetna_stanja[i][j] == True):
                if (dohvatljiva_stanja[i+1] in prihvatljiva_stanja and dohvatljiva_stanja[j] not in prihvatljiva_stanja) or (dohvatljiva_stanja[i+1] not in prihvatljiva_stanja and dohvatljiva_stanja[j] in prihvatljiva_stanja):
                    istovjetna_stanja[i][j] = False

    while (promjena):
        promjena = False
        for i in range(len(dohvatljiva_stanja)-1):
            for j in range(i+1):
                if (istovjetna_stanja[i][j] == True):
                    for znak in abeceda:
                        prvo_stanje = (mapa_prijelaza[dohvatljiva_stanja[i+1]])[znak]
                        drugo_stanje = (mapa_prijelaza[dohvatljiva_stanja[j]])[znak]
                        index_prvog = dohvatljiva_stanja.index(prvo_stanje)
                        index_drugog = dohvatljiva_stanja.index(drugo_stanje)
                        if index_prvog == index_drugog:
                            continue
                        if index_prvog < index_drugog:
                            swap = index_prvog
                            index_prvog = index_drugog
                            index_drugog = swap
                        if istovjetna_stanja[index_prvog - 1][index_drugog] == False:
                            istovjetna_stanja[i][j] = False
                            promjena = True
                            break

    return istovjetna_stanja

#glavni program
if __name__ == '__main__':

    #parsiranje ulaznog dokumenta

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
        drugi_dio = parsirana_linija[1]
        (mapa_prijelaza[prvi_dio[0]])[prvi_dio[1]] = drugi_dio

    #uklanjanje nedohvatljivih stanja

    dohvatljiva_stanja = {pocetno_stanje}
    dohvatljiva_stanja = sorted(ukloni_nedohvatljiva(dohvatljiva_stanja, mapa_prijelaza, abeceda))

    stanja_za_obrisati = []

    for kljuc in mapa_prijelaza.keys():
        if kljuc not in dohvatljiva_stanja:
            stanja_za_obrisati.append(kljuc)

    for stanje in stanja_za_obrisati:
        del mapa_prijelaza[stanje]
        if stanje in prihvatljiva_stanja:
            prihvatljiva_stanja.remove(stanje)

    #odredivanje istovjetnih stanja
    istovjetna_stanja = oznaci_istovjetna(dohvatljiva_stanja, prihvatljiva_stanja, abeceda)

    rjecnik_istovjetnih = {}
    for stanje in dohvatljiva_stanja:
        rjecnik_istovjetnih[stanje] = []

    for i in range(len(dohvatljiva_stanja)-1):
        for j in range(i+1):
            if istovjetna_stanja[i][j] == True:
                prvo_stanje = dohvatljiva_stanja[i+1]
                drugo_stanje = dohvatljiva_stanja[j]
                if prvo_stanje > drugo_stanje:
                    swap = prvo_stanje
                    prvo_stanje = drugo_stanje
                    drugo_stanje = swap
                rjecnik_istovjetnih[prvo_stanje].append(drugo_stanje)

    #uredivanje zapisa
    for lista in rjecnik_istovjetnih.values():
        for stanje in lista:
            if stanje in prihvatljiva_stanja:
                prihvatljiva_stanja.remove(stanje)
            if stanje in dohvatljiva_stanja:
                dohvatljiva_stanja.remove(stanje)
            if stanje in mapa_prijelaza:
                del mapa_prijelaza[stanje]

    promjena = True
    while(promjena):
        promjena = False
        for mapa in mapa_prijelaza.values():
            for znak, slj_stanje in mapa.items():
                for gl_stanje, lista in rjecnik_istovjetnih.items():
                    if slj_stanje in lista:
                        mapa[znak] = gl_stanje
                        promjena = True
                    if pocetno_stanje in lista:
                        pocetno_stanje = gl_stanje

    #ispis
    print(','.join(dohvatljiva_stanja))
    print(','.join(abeceda))
    print(','.join(prihvatljiva_stanja))
    print(pocetno_stanje)

    for poc_stanje,mapa in mapa_prijelaza.items():
        ispis = poc_stanje
        for znak,slj_stanje in mapa.items():
            ispis += ("," + znak)
            ispis += ("->" + slj_stanje)
            print(ispis)
            ispis = poc_stanje