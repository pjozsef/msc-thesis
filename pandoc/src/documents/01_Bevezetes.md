\pagebreak

\thispagestyle{semifancy} 

\pagestyle{fancy}
\rhead{Bevezetés}

# Bevezetés

## Motiváció

Az okostelefonok és a széleskörűen elérhető mobilinternet korában szinte már elképzelhetetlen, hogy az ember ne tudjon 
on-demand zenét hallgatni, legyen akár otthon, úton a munkahelyére, vagy épp egy külföldi országban.
Az emberek mindennapi életének részévé vált a zeneszolgáltatások, mint például 
a Spotify[@url_spotify_home] vagy a Google Play Music[@url_playmusic_home] használata, ahol több tízezer dal közül választhatnak.

Egy zeneszolgáltatás sikere nem csupán az elérhető zenekatalógus méretétől függ. Ugyanennyire fontos az is, hogy mennyire képes
új dalokat ajánlani a felhasználóknak, amik várhatóan tetszeni is fognak neki. Ajánlórendszerek közül az egyik legelterjedtebb módszer
a Collaborative Filtering, mely a felhasználók viselkedése alapján egy profilt épít fel róluk és a felhasználónak a vele
hasonló érdeklődéssel rendelkező felhasználók közül ajánl kedvelt dalokat. Egy ilyen profil több részből állhat,
a rendszer figyelheti, hogy a felhasználó melyik dalokat értékelte pozitívan, mely dalokat hallgatja sűrűn, melyeket
mentette le egy lejátszási listába.

Mivel a Collaborative Filtering erőteljesen támaszkodik arra a feltételezésre, hogy a felhasználónak nagy eséllyel tetszeni fognak
azok a dalok, melyeket a hozzá hasonló ízlésű felhasználók is szeretnek, ezért sokszor pontatlan ajánlásokat tud tenni.
Elképzelhető, hogy a címkék alapján egy eredetileg metál stílusú dal elektronikus remixét ajánlja egy olyan felhasználónak,
aki nem hallgat elektronikus zenéket, illetve attól, hogy a felhasználóhoz hasonló érdeklődésű felhasználók hallgatnak egy előadót, 
az még lehet teljesen irreleváns a felhasználó számára.

Ezt orvosolandó, elterjedtek a hibrid ajánlórendszer megoldások, melyek a Collaborative Filteringet  más módszerekkel
igyekeznek kiegészíteni, hogy javítsák az ajánlások minőségét. A Spotify például gépi nyelvfeldolgozással és a nyers hanganyag elemzésével igyekszik
pontosítani.[@url_spotify_discover_weekly][@url_spotify_discover_weekly_slides]

## Célkitűzés 

Célom a zeneajánlás témakörének egy másik oldalról történő megközelítése. A bevezetésben említett módszerek címkézett adatokon dolgoznak,
dolgozatomban azt szeretném megvizsgálni, hogy címkék (előadó, album, stílus, stb) nélkül, csupán a zeneszámok nyers bináris adatai
alkothatják-e egy ajánlórendszer alapját. Arra szeretnék választ kapni, hogy egy ilyen rendszer képes-e hasonlóságok, összefüggések, 
belső struktúrák felfedezésére, hasonló stílusú dalokat azonos klaszterekbe helyezni.

Célom eléréséhez a magas dimenziójú frekvenciaszeleteket egy autoencodernek nevezett speciális neurális háló architektúra segítségével,
felügyelet nélküli gépi tanulás révén egy alacsonyabb dimenziós térben fogom elkódolni. Ezt követően, ebben az alacsonyabb
dimenziójú látens térben fogok relációkat keresni az adathalmazban, megvizsgálni, hogy hasonló zeneszámok egymáshoz közel kerülnek-e.
Emellett, végső validációként a látens teret 2 dimenzióba ágyazva, grafikusan ábrázolni fogom. A pontokat utólag vissza fogom címkézni, 
a diagramon stílus szerint színezve, s azt fogom vizsgálni hogy a diagramon a különböző stílusú pontok valamiféle struktúrát alkotnak-e, 
vagy teljesen véletlenszerűen helyezkednek el.

A vizuális megjelenítés mellett, a gyakorlatban is tesztelni szeretném a rendszert. Egy részről az alacsony dimenziós 
adathalmaz pontjait a szomszédaival fogom összehasonlítani, másrészt a szomszédsági relációk alapján, 
kísérleti jelleggel, egy pontból kiindulva, s annak a szomszédai mentén lépdelve, lejátszási lista
generálásával is kísérletezni fogok

## Kapcsolódó kutatások

Szükségesnek érzem megemlíteni azokat a kutatásokat, melyek részben kapcsolódnak saját témámhoz, illetve azokat is, melyek inspirációt nyújtottak
az elgondolásomhoz.

### Spotify - Discover Weekly

A Spotify zeneajánló megoldása piacvezetőnek tekinthető a hasonló szolgáltatások körében. 
Szolgáltatásukban ötvözik a Collaborative Filtering-et olyan modern technológiákkal, mint a nyelvfeldolgozás (Natural Language Processing), 
illetve a gépi mély tanulás (Deep Learning). A Spotify mérnökeinek azzal az ördögi körrel kellett megküzdeniük, 
hogy a Collaborative Filtering nem alkalmazható új, ismeretlen dalokra, viszont pont ezek azok a dalok, amiket igazán
ajánlani szerettek volna, hogy az emberek megismerhessék. Ez egy ismert probléma, melyet Cold Start problémának hívnak.

A Cold Start problémát végül a Deep Learning segítségével orvosolták: betanítottak egy regressziós modelt, mely képes volt az adatokat
a Collaborative Filtering model látens terébe képezni. Ezt a modellt a meglévő adatok alapján tanították be, s ezután
sikerrel használták új, eddig ismeretlen dalok esetén is.

Saját témám abban különbözik a Spotify megoldásától, hogy én felügyelet nélküli tanulással szeretném megvizsgálni,
hogy a modell milyen struktúrát képes felfedezni a címkézetlen adathalmazon, míg a Spotify esetében felügyelt,
regressziós mélyhálóról beszélhetünk.[@url_spotify_deep_learning]

### Music Information Retrieval

A Music Information Retrieval (MIR) egy feltörőben lévő kutatási terület, mely hanganyagokból, dalokból nyer ki különböző
adatokat, például a zenei stílust, tempót, hangszereket, zenei struktúrát. A MIR témakörébe sorolható mind a nyers hanganyagok 
elemzése, mind pedig a szimbolikus adatok, mint például kották értelmezése is. Másik érdekes témája a "query by humming",
azaz zeneszámok keresése dúdolás alapján.[@mir][@mir_2]

### Shazam - Audio search
A Music Information Retrieval talán egyik legnagyobb eredményének tekinthetjük a Shazam algoritmusát, mely segítségével 
emberek milliói azonosíthatják a rádióban szóló dalt a telefonjukon lévő alkalmazás segítésével.[@url_shazam_home]
Az algoritmus fő gondolata, hogy a nyers spektrogram adatot időszeletekre bontva, mindegyik időszelethez társítható egy
leíró vektor, mely a meghatározott frekvenciasávok legnagyobb értékeit tartalmazza.

Az algoritmus első lépésea nyers spektrogram szeletek legjellemzőbb pontjainak a detektálása. Ehhez venni kell az 
adott frekvenciasávokban lévő legnagyobb megnitúdóju frekvenciát. Az ilyen módon kiválasztott frekvenciákból kapott vektort
fingerprint-nek nevezzük. A zenei kereső adatbázist ilyen fingerprintekkel töltjük fel.
Az adatbázisban való kereséshez csupán az éppen szóló dal fingerprint-jét kell összevetnünk az adatbázisban lévőkkel, s
nagy valószínűséggel a legtöbb egyezést mutató dal lesz az, ami épp szól a rádióban.[@wang2003industrial]

Érdekesnek tartom, hogy csupán címke nélküli nyers adattal dolgozva is mennyire megbízható és jól működő rendszert lehet
készíteni. Részben a Shazam példája inspirált arra, hogy saját témámon keresztül is azt vizsgáljam, mi mindent lehet 
még címkézetlen nyers adatokból kinyerni. 