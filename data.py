from pyDatalog import pyDatalog

pyDatalog.create_terms('X,Y,Z')
pyDatalog.create_terms('zupa,pierwsze_danie,danie_glowne,danie_glowneZ,dodatek_danie_glowne,surowka_danie_glowne,drugie_danie,ciasto,lody,deser,woda,sok,napoj_bezalkoholowy,napoj_alkoholowy,cena,zupa_wegetarianska,pierwsze_danie_wegetarianskie,danie_glowne_wegetarianskie')

+ zupa('rosól')
+ zupa('pomidorowa')
+ zupa('krem z dyni')
+ zupa('ogórkowa')
+ zupa('chłodnik')

pierwsze_danie(X) <= zupa(X)

+ danie_glowne('spaghetti po bolońsku')
+ danie_glowne('naleśniki z serem')

+ danie_glowneZ('kotlet schabowy')
+ danie_glowneZ('ryba')
+ danie_glowneZ('gołąbki w sosie pomidorowym')
+ danie_glowneZ('krokiety z mięsem')

+ dodatek_danie_glowne('ziemniaki gotowane')
+ dodatek_danie_glowne('puree ziemniaczane')
+ dodatek_danie_glowne('frytki')
+ dodatek_danie_glowne('ryż')

+ surowka_danie_glowne('surówka z marchewki')
+ surowka_danie_glowne('surówka z kiszonej kapusty')
+ surowka_danie_glowne('surówka z białej rzodkiewki')

drugie_danie(X) <= danie_glowne(X)
drugie_danie(X,Y) <= danie_glowneZ(X) & dodatek_danie_glowne(Y)
drugie_danie(X,Y) <= dodatek_danie_glowne(X) & surowka_danie_glowne(Y)
drugie_danie(X,Y,Z) <= danie_glowneZ(X) & dodatek_danie_glowne(Y) & surowka_danie_glowne(Z)

+ ciasto('ciasto czekoladowe')
+ ciasto('sernik')
+ ciasto('ciasto pistacjowe')

+ lody('lody waniliowe')
+ lody('lody smietankowe')
+ lody('lody truskawkowe')
+ lody('lody czekoladowe')
+ lody('lody pistacjowe')

deser(X) <= ciasto(X)
deser(X) <= lody(X)

+ woda('woda niegazowana')
+ woda('woda gazowana')
+ sok('sok pomarańczowy')
+ sok('sok jabłkowy')
+ sok('sok wiśniowy')

napoj_bezalkoholowy(X) <= woda(X)
napoj_bezalkoholowy(X) <= sok(X)

+ napoj_alkoholowy('wino białe')
+ napoj_alkoholowy('wino czerwone')
+ napoj_alkoholowy('piwo')

+ zupa_wegetarianska('pomidorowa')
+ zupa_wegetarianska('krem z dyni')
+ zupa_wegetarianska('ogórkowa')
+ zupa_wegetarianska('chłodnik')

pierwsze_danie_wegetarianskie(X) <= zupa(X)

+ danie_glowne_wegetarianskie('naleśniki z serem')

+ cena('rosól', 5.00)
+ cena('pomidorowa', 4.00)
+ cena('krem z dyni', 4.50)
+ cena('ogórkowa', 4.00)
+ cena('chłodnik', 4.50)

+ cena('spagetti po bolońsku', 11.00)
+ cena('naleśniki z serem', 10.00)

+ cena('kotlet schabowy', 7.50)
+ cena('ryba', 8.00)
+ cena('gołąbki w sosie pomidorowym', 7.00)
+ cena('krokiety z mięsem', 7.50)

+ cena('ziemniaki gotowane', 3.00)
+ cena('puree ziemniaczane', 3.50)
+ cena('frytki', 4.00)
+ cena('ryż', 3.00)

+ cena('surówka z marchewki', 2.50)
+ cena('surówka z kiszonej kapusty', 2.50)
+ cena('surówka z białej rzodkiewki', 2.50)

+ cena('ciasto czekoladowe', 5.00)
+ cena('sernik', 4.50)
+ cena('ciasto pistacjowe', 6.00)

+ cena('lody waniliowe', 6.00)
+ cena('lody smietankowe', 5.00)
+ cena('lody truskawkowe', 6.00)
+ cena('lody czekoladowe', 6.00)
+ cena('lody pistacjowe', 6.00)

+ cena('woda niegazowana', 2.00)
+ cena('woda gazowana', 2.00)
+ cena('sok pomarańczowy', 5.00)
+ cena('sok jabłkowy', 4.00)
+ cena('sok wiśniowy', 5.00)

+ cena('wino białe', 7.00)
+ cena('wino czerwone', 8.00)
+ cena('piwo', 5.00)
