from pyDatalog import pyDatalog

pyDatalog.create_terms('X,Y,Z')
pyDatalog.create_terms('produkt,zupa,pierwsze_danie,danie_glowne,danie_glowneZ,dodatek_danie_glowne,surowka_danie_glowne,drugie_danie,ciasto,lody,deser,woda,sok,napoj_bezalkoholowy,napoj_alkoholowy,cena,zupa_wegetarianska,pierwsze_danie_wegetarianskie,danie_glowne_wegetarianskie')

+ zupa('rosol')
+ zupa('zupa pomidorowa')
+ zupa('krem z dyni')
+ zupa('zupa ogorkowa')
+ zupa('chlodnik')

+ danie_glowne('spaghetti po bolonsku')

+ danie_glowneZ('kotlet schabowy')
+ danie_glowneZ('ryba')
+ danie_glowneZ('golabki w sosie pomidorowym')
+ danie_glowneZ('krokiety z miesem')

+ dodatek_danie_glowne('ziemniaki gotowane')
+ dodatek_danie_glowne('puree ziemniaczane')
+ dodatek_danie_glowne('frytki')
+ dodatek_danie_glowne('ryz')

+ surowka_danie_glowne('surowka z marchewki')
+ surowka_danie_glowne('surowka z kiszonej kapusty')

+ ciasto('ciasto czekoladowe')
+ ciasto('sernik')
+ ciasto('ciasto pistacjowe')

+ lody('lody waniliowe')
+ lody('lody truskawkowe')

+ woda('woda')
+ sok('sok pomaranczowy')
+ sok('sok wisniowy')

napoj_bezalkoholowy(X) <= woda(X)
napoj_bezalkoholowy(X) <= sok(X)

+ napoj_alkoholowy('wino czerwone')
+ napoj_alkoholowy('piwo')

+ cena('rosol', 5.00)
+ cena('zupa pomidorowa', 4.00)
+ cena('krem z dyni', 4.50)
+ cena('zupa ogorkowa', 4.00)
+ cena('chlodnik', 4.50)

+ cena('spaghetti po bolonsku', 11.00)

+ cena('kotlet schabowy', 7.50)
+ cena('ryba', 8.00)
+ cena('golabki w sosie pomidorowym', 7.00)
+ cena('krokiety z miesem', 7.50)

+ cena('ziemniaki gotowane', 3.00)
+ cena('puree ziemniaczane', 3.50)
+ cena('frytki', 4.00)
+ cena('ryz', 3.00)

+ cena('surowka z marchewki', 2.50)
+ cena('surowka z kiszonej kapusty', 2.50)

+ cena('ciasto czekoladowe', 5.00)
+ cena('sernik', 4.50)
+ cena('ciasto pistacjowe', 6.00)

+ cena('lody waniliowe', 6.00)
+ cena('lody truskawkowe', 6.00)

+ cena('woda', 2.00)
+ cena('sok pomaranczowy', 5.00)
+ cena('sok wisniowy', 5.00)

+ cena('wino czerwone', 8.00)
+ cena('piwo', 5.00)

produkt(X) <= zupa(X)
produkt(X) <= danie_glowne(X)
produkt(X) <= danie_glowneZ(X)
produkt(X) <= dodatek_danie_glowne(X)
produkt(X) <= surowka_danie_glowne(X)
produkt(X) <= ciasto(X)
produkt(X) <= lody(X)
produkt(X) <= napoj_bezalkoholowy(X)
produkt(X) <= napoj_alkoholowy(X)