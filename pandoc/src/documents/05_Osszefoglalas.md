\pagebreak

\thispagestyle{semifancy} 

\pagestyle{fancy}
\rhead{Összefoglalás}  

# Összefoglalás

Dolgozatomban azt vizsgáltam, hogy zenei dalokat lehet-e sikeresen klaszterezni mindennemű metaadatot (előadó, album, album éve, stílus, stb)
nélkülözve, csupán a nyers frekvenciaadatokat felhasználva. 

Ehhez először összegyűjtöttem a tanulóhalmazomat, amit MP3 fájlokból állítottam elő. A zeneszámokat azonos formátumra hozás után
Fourier Transzformált segítségével frekvenciasávokra osztottam, majd azokból a releváns szeleteket PNG képként kiexportáltam.
Az adathalmaz képeit becsomagoltam egy Tensorflow specifikus protocol buffer fájlba. Az adathalmazban szereplő dalszeletek
hossza összegezve közel 5 napnyi zenét tesz ki.

A klaszterezés elvégzéséhez először Tensorflow segítségével megterveztem és a Google felhőszolgáltatásán betanítottam egy
konvolúciós autoencoder-t, mely segítségével a 800×20 pixel méretű spektrogram szeleteket egy 32-dimenziós látens térben
tudom elkódolni. A legnagyobb kihívást az autoencoder architektúrájának meghatározása, illetve a hiperparamétereinek finomhangolása
jelentette, mely egy hetekig tartó iteratív folyamat volt.

A betanított kész modell segítségével elkódoltam az adathalmazt, mely eredménye az összes dalszelet 32-dimenziós
koordinátáját tartalmazó csv fájl lett. Ezen látens térbeli koordinátákra alkalmaztam a t-SNE algoritmust, mely segítségével az adathalmazom
dimenzióját 32-ről 2-re csökkentettem. A 2-dimenziós pontokat stíluscímkékkel utólag visszacímkézve scatter ploton ábrázoltam. 
A kapott diagrammokon stílusokhoz tartozó klaszterek figyelhetőek meg. A klaszterek egymástól nem határolódnak el egyértelműen,
összeérnek, a klaszterhatároknál átmenet tapasztalható.

A sikeres vizualizációt követően megvizsgáltam, hogy a látens tér pontjai milyen relációban vannak szomszédaival, azoknak
stílusa hasonló-e a kiválasztott pont stílusához. A szomszédsági lekérdezések segítségével kísérleti jelleggel megterveztem egy algoritmust,
mely segítségével egy kiválasztott pontból indulva, tranzitív módon, a szomszédokon való lépegetésen keresztül lejátszási lista
generálható. Mind a szomszédsági lekérdezések, illetve a lejátszási listák készítése során mélyrehatóbban feltérképezhettem a 32-dimenziós
látens tér felépítését. Kísérletezéseim során felfedeztem, hogy a pontok stílusa tekintetében a látens tér bizonyos részei egybefüggőbbek, 
homogénebbek, alkalmasabbak lejátszási listák generálására, míg más részei vegyesebbek, olykor kifejezetten kaotikusak.

Összességében nézve úgy érzem sikerült a dolgozatomban kitűzött céljaimat teljesítenem. Egy autencoder segítségével megmutattam,
hogy frekvenciaadatok alapján is meglepő pontossággal lehet dalokat klaszterezni, majd pedig a modell által elkódolt dalszeletekhez
elkészítettem egy egyszerű, metaadatok használatát mellőző zenei ajánlórendszer alapjait. Ez az ajánlórendszer nem képes szofisztikált,
különböző alstílusok közötti különbségek felismerésére, viszont alapvetően képes különbséget tenni klasszikus, elektronikus, illetve metál
stílusú dalok között. Ez a rendszer nem alkalmas ipari használatra, ahhoz további kísérletezés, kutatás, szofisztikáltabb
architektúrájú neuronháló és több adat lenne szükséges.

## Továbbfejlesztési lehetőségek

Dolgozatom készítése során legnagyobb limitáló tényezőt az összegyűjthető adathalmaz mérete, illetve a tanítás ideje jelentették.
Ezen limitációk nélkül sokkal nagyobb adathalmazon tanítanám be a modellemet, további gyűjtőstílusokat definiálnék, mint például
pop, rap, s megnézném több gyűjtőstílus esetén hogyan viselkedne a modellem. Emellett szívesen kísérleteznék komplexebb
autoencoder architektúrákkal is. Dolgozatom készítése során sajnos
még nem volt széleskörűen elérhető a Google Cloud-on a Google TPU-ja, ami egy Tensorflow-ra optimalizált hardware, mely segítségével
gyorsabb számítási kapacitás érhető el, mint a GPU-kkal.

A legközelebbi szomszédok keresése, illetve lejátszási listák generálása során tapasztaltam, hogy a dalszeletek méretének kiválasztása
nem volt optimális. A látenstér alaposabb ismerete alapján úgy látom, hogy az eredeti 20 pixeles, azaz 3.7 másodperces szeletek
túl rövidnek bizonyultak: a modell túl könnyedén talált pár másodperces hasonlóságokat olyan dalok között is, melyek különböztek egymástól.
Emellett a 800 pixeles magasságot utólag túl magasnak ítélem, a releváns frekvenciaminták az alacsonyabb frekvenciasávokban találhatóak.
Másodszor nekikezdve 2 hatvány dimenziókat választanék, mint például 512×128 px.

A dalszeletek méretének szerencsésebb megválasztása mellett a percentilis szeletek aggregálásával is kísérleteznék.
Jelenleg egy dalhoz több percentilis tartozik, melyek különböző 32-dimenziós koordinátákkal rendelkeznek, ezáltal egy dal a látens tér több részén
is megtalálható. A dalok szétszórtsága hozzájárulhat a outlierek megjelenéséhez, ezt minimalizálandó, a pontokat
összegezném, vagy átlagolnám, s ezáltal egy pontként kezelném őket.