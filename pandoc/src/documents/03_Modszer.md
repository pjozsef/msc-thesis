\pagebreak

\thispagestyle{semifancy} 

\pagestyle{fancy}
\rhead{Módszer ismertetése}  

# Módszer ismertetése

\begin{wrapfigure}[25]{r}{0.3\textwidth}
  \begin{center}
    \includegraphics[width=0.29\textwidth]{src/images/workflow1_portrait.png}
  \end{center}
  \caption{Nyers MP3 fájloktól a kész modellig}
\end{wrapfigure}
Elgondolásomat az az intuíció vezérelte, hogy egy autoencoder segítségével oly módon lehet dimenziócsökkentést végezni
magasabb dimenzióból alacsonyabb dimenzióba, hogy eközben a bemeneti adatok közötti szemantikai relációk, hasonlóságok a látens térben
is megmaradjanak. Ehhez felhasználtam az autoencoderek azon tulajdonságát, hogy az egymáshoz közeli bemenetek a látens térben is
közel kerülnek egymáshoz.[@hinton_semantic_hashing][@hinton_autoencoder_image_retrieval] Az autoencoder látens terében elhelyezett kódok
felhasználhatóak többek között klaszterezésre, szomszédsági lekérdezésekre, melyek egy zenei ajánlórendszer alapját képezhetik.

## Adathalmaz elkészítése
A teljes adathalmaz alapját MP3 fájlok alkotják. Pontosabban fogalmazva olyan MP3 fájlok, melyeknél az **artist**, **album** és
**song** MP3 tag-ek ki vannak töltve. Ezek a metaadatok nem közvetlenül a neuronháló betanításához szükségesek, 
mivel a módszer felügyelet nélküli tanuláson alapul. A metaadatok azért szükségesek, hogy az autoencoder betanítását
követően a látens térben elkódolt bemenetek visszacímkézésével a modell teljesítményét pontosabban ki lehessen értékelni.

A megfelelő MP3 fájlok kiválogatása után a fájlokat közös formátumra kell hozni, hiszen elképzelhető, hogy a fájlok
különböző bitrátával rendelkeznek, illetve az egyik fájl hangosabb, vagy épp halkabb. FFmpeg[@url_ffmpeg_home] segítségével az MP3 fájlokat
WAV fájlokká konvertálom, melyek sample rate-je 44100 Hz, bitmélysége 16 bit, s egy csatornával rendelkeznek (mono). Loudnormalization-t
is alkalmazok, mely során minden fájl hangereje normalizálva lesz, azonos skálára kerülnek.

Ezek a WAV fájlok már alkalmasak arra, hogy Fourier transzformáció segítségével spektrogramot készítsünk belőlük. 
Eredetileg 0.2 másodperces, azaz $44100/5=8820$ mintavételt tartalmazó szeletekből terveztem a frekvencia értékeket
elkészíteni. Mivel az általam használt FFT programcsomag $2^n$ méretű bemenetet fogad el, ezért végül $2^{13}=8192$ méretű
szeletekkel dolgoztam, melyek $8192/44100=0.1857$ másodperces időszeleteknek felelnek meg. Amennyiben az eredeti, nyers
mintavételeket tartalmazó tömb $N$ hosszú volt, a Fourier transzformáció elvégzése után kapott spektrogram egy 
$\lfloor N/8192\rfloor\times 8192$ méretű mátrix, mely $\lfloor N/8192\rfloor$ darab Fourier transzformáltat tartalmaz.
A Fourier transzformáció eredményéül kapott tömb 4096 komplex számból áll, mely implementációs szinten egy 8196 
elemű valós--imaginárius számpárokat tartalmazó tömb. Ez a komplex tömb 4096 frekvenciasávot határoz meg.

A kapott spektrogram mérete túl nagy ahhoz, hogy egy az egyben bemenete lehessen a neuronhálónak. Emellett másik probléma, 
hogy különböző hosszúságú daloknak a spektrogramjai is különböző hosszúságúak lesznek, viszont a neuronháló kötött méretű
bemenetet vár el. Emiatt a spektrogramot azonos szélességű és magasságú szeletekre kell vágni. A választásom a 800×20-as
méretű spektrogramszeletekre esett.

Mindenképpen szerettem volna, ha a spektrogramszeletek 0 Hz-től legalább a zongora magas C hangjáig (C8) terjedő intervallumot lefedik.
Mivel tudjuk, hogy az eredeti 44100 Hz-es mintavételezési ráta mellett a visszaalakítható maximális frekvencia ennek a fele, 
azaz 22050 Hz, illetve, hogy a Fourier transzformált 4096 darab frekvenciasávra osztja a bemeneti mintavételeket, kiszámítható
hogy egy frekvenciasáv 22050/4096 ~ 5.38 Hz-nyi tartományt fed le. A zongora C8 hangjának a frekvenciája 4186 Hz, melyből 
adódik hogy ez a frekvencia a $4186/5.38=779.0669$, azaz közelítőleg a 779. frekvenciasávban helyezkedik el. A kettővel való
többszörös oszthatóság érdekében választottam végül a 800-at.\newline
A spektrogramszelet szélességét azért választottam 20-nak, hogy a neuronháló bemenete ne legyen túlságosan nagy.
Mivel a spektrogramban egy oszlop 0,1857 másodpercnek felel meg, így a spektrogramszelet $20*0.1857=3.714$ másodpercet fed le.

A spektrogramszeletek méretének definiálása mellett azt is meg kell határozni, hogy az adott szeletet a dal mely részéből
válasszuk ki, hogy minél inkább releváns és reprezentatív szeletekkel dolgozhassunk. Egy halk intro/outro nem mond sokat a dalról, pont ugyanúgy
mint a dal közepébe ékelt fél perces halk intermezzo sem. Mivel a legalkalmasabb dalszelet dalonként
változik, nem egy szeletet választottam a dalból, hanem többet. Első lépésként, a spektrogramon egy 20 egység széles ablakot 
végigcsúsztva mindegyik ablakhoz kiszámoltam a benne található frekvenciasávokhoz tartozó magnitúdók összegét, mely nem más, mint a komplex számok
hosszának az összege. Ez az érték jó indikátora az adott ablakban zajló aktivitásnak, s ez alapján az ablakokat sorbarendezve
kiválasztottam közülük minden $k$-adik percentilishez tartozó ablakot, ahol $k \in [15..100]$ és $5 \, | \, k$. Egy dalból
összesen 18 spektrogramszeletet választok ki ily módon.

A percentilisekhez tartozó spektrogramszeleteket normalizáltam $[0..1]$ közé, majd kiexportáltam őket 800×20 pixel méretű 
fekete fehér PNG képként. Ezt követően Tensorflow specifikus, tfrecords-nak nevezett bináris protocol buffer fájlokba
csomagoltam a képeket. A protocol buffer a Google saját nyelv- és platformfüggetlen bináris adatszerializáló formátuma.
Stílusonként 3 tfrecords fájlt készítettem el, külön a train, test és crossvalidation halmazoknak megfelelően. 
A képek halmazát 60:20:20 arányban osztottam meg a train, test és crossvalidation halmazok között.

## Adathalmaz

Számtalan stílusú zene létezik, egy dal több stílus alá is tartozhat, s különböző emberek ugyanazt a dalt
különböző stílus alá is besorolhatják. Ebből fakadóan, egy zeneszám stílusának meghatározása nem egzakt, hanem 
szubjektív folyamat. Annak érdekében, hogy a lehetőségekhez mérten minél objektívabb módon határozhassam 
meg az előadókhoz a stílus címkéket, a Last.fm[@lastfm_api] publikus REST API-ján keresztül elérhető
zenei adatbázist hívtam segítségül. A lekérdezéseket követően 
48 különböző stílust sikerült összegyűjtenem. Mivel ez a szám túlságosan nagy, a könnyebb kezelhetőség érdekében a stílusokat
besoroltam 3 gyűjtőstílus alá, melyek rendre klasszikus, elektronikus és metál stílusok lettek.

Fontosnak tartom megemlíteni, hogy a dalok 3 osztályba sorolása nagy mértékű általánosítással jár. A "klasszikus" kategória
alá például nem csak komolyzenei klasszikusok (Mozart, Beethoven, stb) kerültek, hanem kortárs film-, illetve videójátékzeneszerzők, 
neoklasszikus, instrumentális és akusztikus előadók is besorolásra kerültek. Az elektronikus és metál gyűjtőstílus esetén is több, egymástól
különböző stílusról beszélhetünk, melyek alapvetően mind mégis az adott gyűjtőstílusba sorolhatóak.
Legjobb próbálkozásom ellenére, a gyűjtőstílusok között találhatóak átfedések, például szimfonikus elemeket alkalmazó metál zene, 
vagy olyan elektronikus zene mely metálosabb, nyersebb hangzásra épít. Ilyen esetekben az adott előadót a számára legrelevánsabb
stílusba soroltam.

\csvautolongtable[
  table head={
    \hline \rowcolor{black!15} \# & Klasszikus & Elektronikus & Metál \\\hline
    \endfirsthead
    \hline
    \caption{Stílusokhoz tartozó 5 leggyakoribb alstílus Last.fm alapján}\label{table_styles}
    \endfoot
  },
  respect all
]{src/tables/subgenres.csv}

![Az előadók, albumok és dalok számának eloszlása stílusonként](src/images/dataset_stats.png)

Az adathalmaz elkészítéséhez összesen 262 előadó 639 albumának 6192 zeneszámát használtam fel.
Mivel dalonként 18 kép került exportálásra, az adathalmaz összesen $6192*18=111 456$ db képből áll.
A képek önmagukban 1.23 GB tárhelyet foglalnak, a belőlük készített tfrecords fájlok pedig 3.68 GB-ot.
Ez a mennyiségű adat $111456*3,714$, azaz 413 947 másodpercnyi zenét takar, ami 4,79 napnak felel meg.

Az adathalmazban előfordulnak félrecímkézett stílusú dalok, mint például egy metál album akusztikus intro-ja, outro-ja. 
Emellett, metál album esetén az albumok végén található elektronikus remixek is metál címkét kaptak. Mivel az algoritmus maga nem használja ezeket a címkéket,
azok csupán utólagos validálásra szolgálnak, a közelítőleg 6200 dal megcímkézésének gyorsítása végett a stílusba sorolást előadónként,
indokolt esetben albumonként végeztem, nem pedig dalonként. 

\footnotesize\csvautolongtable[
  table head={
    \hline \rowcolor{black!15} \#& Összesítve& Klasszikus& Elektronikus& Metál \\\hline
    \endfirsthead
    \hline
    \caption{Top 5 előadó összesítve, illetve stílusonként tekintve}
    \endfoot
  },
  respect all
]{src/tables/topk_artists.csv}\normalsize

## Modell
A modellem egy konvolúciós autoencoder, mely encoder és decoder részekből áll. Az encoder kezdeti rétegeiben 
több konvolúciós és pooling réteg váltakozik. Az encoder bemenete egy harmadrendű tenzor, melynek
mérete 800×20×1 (magasság×szélesség×csatornák száma). A konvolúciós neuronhálók esetén kialakult konvenciót követve, 
a pooling rétegek révén rétegről rétegre
csökkentettem a tenzor szélességét és magasságát, míg a konvolúciós rétegekkel a csatornák számát növeltem.
Miután a tenzort így kellőképp "elkeskenyítettem", elsőrendű tenzorrá lapítottam, s fully connected rétegeken 
keresztül csökkentettem tovább a dimenzióját a látens tér dimenziójáig.

\begin{figure}[H]
\centering
\includegraphics{src/images/data_dimension_change.png}
\caption{A bemeneti adat méretének transzformálása konvolúciós és poolig rétegek segítségével egy leegyszerűsített példa hálózaton.}
\end{figure}

A modell decoder része az encoder szemantikai tükörképe. Egy
$N$ bemenettel és $M$ kimenettel rendelkező fully connected réteg inverze egy $M$ bemenettel és $N$ kimenettel rendelkező 
fully connected réteg. 
Egy $H$×$W$×$I$×$O$ méretű kernellel rendelkező konvolúciós réteg inverze a $H$×$W$×$O$×$I$ méretű kernellel 
rendelkező dekonvolúciós/transzponált konvolúciós réteg, ahol $H$ a kernel magassága, $W$ a kernel szélessége, $I$ a bemeneti
csatornák száma, $O$ a kimeneti csatornák száma. 
A pooling rétegnek az upsampling réteg az inverze, 
mely annyival növeli a bemenet méretét, amennyivel a vele megfelelő pooling réteg azt csökkentette. Az upsampling réteg
Nearest Neighbor interpolációval végzi a bemenet felskálázását. A decoder háló az encoder háló
súlytenzorainak transzponáltját használja fel, ezáltal közel megfelezve a teljes háló paraméterszámát. 
A kevesebb paraméter előnyös, mert így csökken az esély, hogy a háló túlilleszkedjen a tanuló adathalmazra. A decoder
háló az encoder bias változóit nem használja fel, csupán a súlyait, ezért nem beszélhetünk a paraméterek pontos felezéséről.

Az encoder kimenete megegyezik a látens tér dimenziójával. Gépi tanulási problémák esetén elterjedt gyakorlat 2 hatványú dimenziókkal
dolgozni. A választásom csupán kísérleti jelleggel esett a 32-re, az intuícióm azt súgta, hogy a feladat komplexitásához
egy ekkora dimenziójú látens tér elégéséges lehet.

\begin{figure}[H]
\centering
\includegraphics{src/images/modell_structure_landscape.png}
\caption{A modell sematikus szerkezete}\label{modell_structure}
\end{figure}

\footnotesize\csvautolongtable[
  table head={
    \hline \rowcolor{black!15} \#&Réteg&Bemenet&Kernel méret&Stride&Padding&Kimenet&Paraméterek\\\hline
    \endfirsthead
    \hline
    \caption{A modell rétegei. A paraméterek oszlop 'súly paraméterek+bias paraméterek' formátumú.}
    \endfoot
  },
  respect all
]{src/tables/model_parameters.csv}\normalsize

\footnotesize\csvautolongtable[
  table head={
    \hline \rowcolor{black!15} Réteg& Rétegek száma& Encoder/Decoder& Súly paraméterek& Bias paraméterek \\\hline
    \endfirsthead
    \hline
    \caption{Rétegek számszerűsítve}
    \endfoot
  },
  respect all
]{src/tables/model_layer_stats.csv}\normalsize

## Modell használata
A modell sikeres betanítását követően elsődleges dolgunk egy adatbázis feltöltése a frekvenciaszeletek encodingjaival.
Mivel az encodingok csupán 32 darab double értékből állnak, ezért nagyságrendekkel kevesebbet foglalnak a nekik megfelelő,
PNG képként kiexportált frekvenciaszelethez képest. Esetemben, a nagyságrendileg 100 000-es darabszámú képmennyiség esetén is
kezelhető maradt az encoding halmaz mérete, ezért nem adatbázist használtam, csupán egy csv fájlban tároltam az adatokat. 
A teljes adathalmaz elkódolása megközelítőleg egy 50 MB méretű csv fájlt eredményezett, mely könnyedén betölthető a
memóriába is. Lényegesen nagyobb adathalmaz esetén célszerű olyan adatbázist választani, mely támogatást nyújt szomszédság
alapú lekérdezésekre.
\begin{figure}[H]
\centering
\includegraphics[width=0.6\textwidth]{src/images/workflow2_portrait.png}
\caption{A kész modell alkalmazásai}
\end{figure}

A látens térben elhelyezett pontok könnyebb átláthatósága végett első lépésben t-SNE segítségével 2-dimenzióban vizualizáltam
az adathalmazt. A t-SNE futási ideje a pontok számától függően akár több órán keresztül is eltarthat, ezért a teljes adathalmaz
helyett az adathalmazból csupán mintavételezett pontokra alkalmaztam a vizualizációt. Az algoritmus által kapott 2-dimenziós
pontokat utólag, a stílusadatokkal visszacímkézve scatter ploton ábrázoltam.
\begin{figure}[H]
\centering
\includegraphics[width=0.6\textwidth]{src/images/tsne_example.png}
\caption{Példa diagram a t-SNE alkalmazására az adathalmazon. A klasszikus, elektronikus és metál stílusokhoz tartozó pontok rendre kék, sárga és fekete színűek}
\end{figure}

Az adathalmaz 2-dimenziós ábrázolását követően, a globális struktúra után a lokális részletekre is kíváncsi voltam. Ehhez
véletlenszerűen kiválasztottam adatpontokat, majd azok 5-10 legközelebbi szomszédját (Nearest Neighbour) vizsgálva megnéztem, azok mennyire
hasonlóak a kiválasztott ponthoz képest. 

\scriptsize\csvautolongtable[
  table head={
    \hline \rowcolor{black!15} \#& Stílus& Előadó& Dal& Percentilis& Távolság \\\hline
    \endfirsthead
    \hline
    \caption{Példa egy Nearest Neighbor lekérdezésre}
    \endfoot
  },
  respect all
]{src/tables/topk_5_01.csv}\normalsize

A legközelebbi szomszédok ötletét továbbvezetve, a modell által generált 32-dimenziós pontok halmazán lejátszási
lista generálásával is megpróbálkoztam. A lista elkészítésére az alábbi nemdeterminisztikus algoritmust dolgoztam ki:

1) Az algoritmus egy tetszőlegesen kiválasztott pontból indul, ez lesz a lejátszási lista első dala
2) Vesszük az aktuális pont legközelebbi **K** szomszédját
3) A szomszédokhoz valószínűségeket rendelünk, s a valószínűségek alapján kiválasztjuk a következő dalt.
4) A kiválasztott dalhoz tartozó összes percentilist töröljük a halmazból, hogy a dal a lejátszási listában ne fordulhasson elő kétszer.
5) A kiválasztott dalt hozzáadjuk a lejátszási listához, s a kiválasztott dal lesz az aktuális dal.
6) Visszaugrunk a 2-es pontra mindaddig, amíg a legjátszási lista **L** hosszúságú nem lesz.

Az algoritmus implementációja során az aktuális pont szomszédainak kiválasztási valószínűségét a pontok távolságával tettem
fordítottan arányossá. $K=2$ esetén, ha az aktuális pontnak vesszük két szomszédját, melyek rendre 1 és 2 távolságra vannak tőle,
a szomszédok kiválasztási esélye rendre 0.66 és 0.33 lesz. Formalizálva:
\begin{equation}
      p(x_i) = \frac{\frac{1}{x_i}}{\sum\limits_{j=1}^{n} \frac{1}{x_j}},
\end{equation}
ahol $(x_1, x_2, ..., x_n) \in \mathbb{R}^n$ a szomszédok távolságai az aktuális ponttól, $p(x_i) \in \mathbb{R}$ az $i$-edik szomszéd kiválasztásának
az esélye. Az algoritmus nemdeterminisztikussága változatosabb lejátszási listák készítését garantálja, azonos pontból kiindulva
mindig más és más listát kapunk. 

Az algoritmus 3 fontos paramétere a lejátszási lista hossza, a legközelebbi K szomszéd száma, illetve, hogy
mely percentilisekhez tartozó pontok közül keresgéljen az algoritmus. A percentilisek filterezésére azért van szükség, mert
alacsonyabb percentilisek esetén a zaj számottevőbb. Használat során úgy tapasztaltam, hogy az 50 és 100 közé eső 
percentilisekre való szűréssel adta az algoritmus a legjobb eredményeket.

## Használt technológiák

Kotlin
  ~ A Kotlin[@kotlin] egy nyílt forráskódú, statikusan típusos modern JVM nyelv, melyet a JetBrains fejleszt. Széleskörűen elterjedt
    mind backend és frontend fejlesztés körében. A 2017-es Google IO óta[@kotlin_android] a Google is hivatalosan támogatja
    Androidon.

Python
  ~ A Python[@python] egy dinamikusan típusos script nyelv. Kényelmes és hasznos nyelvi elemei, egyszerű szintaxisa és az
   elérhető adatelemzési, gépi tanulási programcsomagok miatt az egyik legelterjedtebb nyelv Data Science, 
   illetve Machine Learning terén.

Google Cloud ML Engine
  ~ A Cloud Machine Learning Engine a Google Cloud egyik szolgáltatása, mely segítségével könnyedén lehet Tensorflow 
  modelleket tanítani a felhőben. A szolgáltatás révén könnyű hozzáférésünk jut a Google szerverparkjában lévő GPU-khoz,
  melyek elengedhetetlenek a valós életbeli modellek betanításához. A Google saját gépi tanulási modelljeit (Google
  Photos, Google Cloud Speach) is ezen a platformon tanítja be.[@google_cloud_ml]

FFmpeg
  ~ Az FFmpeg[@url_ffmpeg_home] egy nyílt forráskódú, parancssori multimédiás keretrendszer, mely segítségével hangfájlokat,
  videó fájlokat konvertálhatunk különböző formátumokba, különböző filtereket futtathatunk rajtuk. Az FFmpeg crossplatform,
  elérhető Linuxra, OS X-re, Windows-ra is. Az FFmpeg-et a különböző hangerővel, bitrátával rendelkező MP3 fájlok azonos
  WAV formátumra hozásánál használtam.

mp3agic
  ~ Nyíilt forráskódú Java programkönyvtár, MP3 tag-ek írásása, olvasására használható. Az MP3 fájlok metaadatainak (előadó, album, dalcím) 
  kinyerésére használtam.

JTransforms
  ~ Nyílt forráskódú Java programkönyvtár, mely segítségével a Gyors Fourier Transzformáltat számítottam ki a nyers WAV adatokból.

NumPy
  ~ Nyílt forráskódú Python programkönyvtár, mely segítségével könnyedén tudunk N-dimenziós tömböket kezelni. Emellett rengeteg lineáris algebrai,
  illetve statisztikai műveletet, függvényt is tartalmaz.

Pandas
  ~ Nyílt forráskódú Python programkönyvtár, mely 2-dimenziós adattáblák létrehozását, kezelését, elemzését támogatja.

TensorFlow
  ~ Nyílt forráskódú, alacsony szintű gépi tanulási keretrendszer Python-hoz, mellyel többek között neuronháló modelleket
  tudunk létrehozni, betanítani és a tanítást követően használni. A Tensorflow-t használva készítettem el a saját modellemet is.

scikit-learn
  ~ Nyílt forráskódú gépi tanulási programkönyvtár Python-hoz. A scikit-learn számtalan, adatbányászati, adatelemzési és 
  gépi tanulási algoritmusot tartalmaz, mint például regresszió, osztályozás, klaszterezés, dimenziócsökkentés.
  A modellem által kapott, 32-dimenziós térben elkódolt pontok szomszédsági lekérdezéseit, illetve a t-SNE-vel történő
  vizualizációt is a scikit-learn segítségével végeztem.

## Módszer alkalmazása saját adathalmazra
Az alábbi fejezetben bemutatom a szükséges technikai lépéseket, hogy a módszerem tetszőleges MP3 adathalmazzal
megismételhető lehessen.
A parancsok futtatáshoz az alábbiakra lesz szükség:

* MP3 fájlok, a megfelelő artist, album, song tag-ekkel kitöltve
* Java 8
* Python 3.6
* FFmpeg [@url_ffmpeg_home]
* Pipenv [@url_pipenv_home]

### Tanulóadatok elkészítése
1. Stílusonként helyezzük külön mappákba az MP3 fájlokat.
2. Navigáljunk a projekt gyökérkönyvtárába.
3. Készítsük el a futtatható jar fájlt.
\begin{verbatim}./gradlew dsp:shadowJar\end{verbatim}
4. Minden stílushoz készítsük el az MP3 listát, melyből a frekvenciaszeleteket exportálni fogjuk. 
\begin{verbatim}java -jar dsp/build/libs/dsp-all.jar list [mp3Mappa] \\end{verbatim}
\begin{verbatim}     -i --path > [mp3Lista.txt] 2> [hiba.txt]\end{verbatim}
Azon **mp3Mappában** 
lévő mp3 fájlok útvonalai, melyek rendelkeznek a megfelelő tag-ekkel, az **mp3Lista.txt** 
fájlba fognak kerülni. A program a hibákat, mint például a hiányzó tag-eket
a **hiba.txt** fájlba fogja logolni.
5. Minden stílushoz készítsük el a frekvenciaszeleteket tartalmazó mappát
\begin{verbatim}mkdir [stílusMappa]\end{verbatim}
6. Minden stílushoz generáljuk le a frekvenciaszeleteket.
\begin{verbatim}java -jar dsp/build/libs/dsp-all.jar exportlist \\end{verbatim}
\begin{verbatim}     --style [stílus] \\end{verbatim}
\begin{verbatim}     -o [stílusMappa] \\end{verbatim}
\begin{verbatim}     [mp3Lista.txt]\end{verbatim}
7. Navigáljunk a **model** mappába.
\begin{verbatim}cd model\end{verbatim}
8. Telepítsük **pipenv**-en keresztül a szükséges függőségeket
\begin{verbatim}pipenv install\end{verbatim}
9. Minden stílushoz partícionáljuk a kiexportált frekvenciaszeleteket train, test és crossvalidation halmazokba. 
\begin{verbatim}pipenv run python src/data/partition.py \\end{verbatim}
\begin{verbatim}    --source "[stílusMappa]/*.png" \\end{verbatim}
\begin{verbatim}    --output-file [stílusRecord]\end{verbatim}
Az alábbi három
fájl fog létrejönni: **stílusRecord_train.txt**, **stílusRecord_test.txt**, **stílusRecord_cv.txt**.
10. Minden stílushoz készítsük el a **train**, **test** és **cv** tfrecord kiterjesztésű tanuló fájlokat, melyekből a Tensorflow modell tanulni fog.
\begin{verbatim}pipenv run python src/data/create-tfrecord.py \\end{verbatim}
\begin{verbatim}    --source [stílusRecord]_train.txt \\end{verbatim}
\begin{verbatim}    --result [tfRecordMappa]/[stílus]_train.tfrecords\end{verbatim}
\begin{verbatim}pipenv run python src/data/create-tfrecord.py \\end{verbatim}
\begin{verbatim}    --source [stílusRecord]_test.txt \\end{verbatim}
\begin{verbatim}    --result [tfRecordMappa]/[stílus]_test.tfrecords\end{verbatim}
\begin{verbatim}pipenv run python src/data/create-tfrecord.py \\end{verbatim}
\begin{verbatim}    --source [stílusRecord]_cv.txt \\end{verbatim}
\begin{verbatim}    --result [tfRecordMappa]/[stílus]_cv.tfrecords\end{verbatim}
11. A fenti lépések végrehajtása után, amennyiben 3 stílussal dolgozunk (klasszikus, elektronikus, metál), a **tfRecorddMappában** 9
fájlt kell találjunk:
    * **klasszikus_train.tfrecords**
    * **klasszikus_test.tfrecords**
    * **klasszikus_cv.tfrecords**
    * **elektronikus_train.tfrecords**
    * **elektronikus_test.tfrecords**
    * **elektronikus_cv.tfrecords**
    * **metál_train.tfrecords**
    * **metál_test.tfrecords**
    * **metál_cv.tfrecords**

### Modell betanítása
A megfelelő **tfrecord** fájlok birtokában képesek vagyunk betanítani a modellünket. A fenti 3 stílusnál maradva 
(klasszikus, elektronikus, metál), a modellt **X** epoch-on keresztül tanítva, a parancsunk az alábbiként fog kinézni:
\begin{verbatim}pipenv run python -m src.train.trainer \\end{verbatim}
\begin{verbatim}    --epoch [X] \\end{verbatim}
\begin{verbatim}    --job-dir [trainMappa] \\end{verbatim}
\begin{verbatim}    --train-data-root [tfRecorddMappa] \\end{verbatim}
\begin{verbatim}    --train-data-records [klasszikus_train.tfrecords] \\end{verbatim}
\begin{verbatim}                         [elektronikus_train.tfrecords] \\end{verbatim}
\begin{verbatim}                         [metál_train.tfrecords] \\end{verbatim}
\begin{verbatim}    --cv-data-root [tfRecorddMappa] \\end{verbatim}
\begin{verbatim}    --cv-data-records [klasszikus_cv.tfrecords] \\end{verbatim}
\begin{verbatim}                      [elektronikus_cv.tfrecords] \\end{verbatim}
\begin{verbatim}                      [metál_cv.tfrecords] \\end{verbatim}
\begin{verbatim}    --test-data-root [tfRecorddMappa] \\end{verbatim}
\begin{verbatim}    --test-data-records [klasszikus_test.tfrecords] \\end{verbatim}
\begin{verbatim}                        [elektronikus_test.tfrecords] \\end{verbatim}
\begin{verbatim}                        [metál_test.tfrecords] \end{verbatim}

A tanítás végeztével a kész modellünk a **trainMappa/final_model** mappába lesz elmentve.

### Modell használata
Első lépésként, az elkészült modell segítségével kódoljuk el a frekvenciaszeleteket egy **codes.csv** nevű fájlba. 
A rákövetkező lépések mindegyike ezt a csv fájlt fogja használni.
\begin{verbatim}pipenv run python src/infer/infer.py \\end{verbatim}
\begin{verbatim}    --data-glob "[frekvenciaSzeletek]/*.png" \\end{verbatim}
\begin{verbatim}    --model [trainMappa]/final_model \\end{verbatim}
\begin{verbatim}    --export [codes].csv\end{verbatim}

Az elkészült csv fájl az alábbi adatokat tartalmazza mindegyik frekvenciaszeletről:

* stílus
* előadó
* album
* dalcím
* percentilis
* látens térbeli 32-dimenziós vektorérték (0-31)

#### t-SNE vizualizáció
Az alábbi paranccsal tudjuk 2-dimenzióban vizualizálni a 32-dimenzióban elhelyezett pontjainkat:
\begin{verbatim}pipenv run python src/infer/tsne.py \\end{verbatim}
\begin{verbatim}    --input [codes].csv \\end{verbatim}
\begin{verbatim}    --title "Elkódolt zeneszámok vizualizációja t-SNE segítségével" \\end{verbatim}
\begin{verbatim}    --retry [X] \\end{verbatim}
\begin{verbatim}    --percentiles 50-100\end{verbatim}

A vizualizáció elkészítése nagyon sok pont esetén több órát is igénybe vehet. A sebességen javíthatunk, s a zajt is
csökkenthetjük, ha nem az összes pontot vizsgáljuk, hanem csupán bizonyos percentilis intervallumokhoz tartozó pontokat,
például 50-100, vagy 75-100.\newline
Mivel a t-SNE algoritmus is Gradient Descent révén tanul, ezért nem garantált, hogy első futásra a legoptimálisabb eredményt kapjuk.
A **retry** paraméterrel megadhatjuk, hogy hányszor szeretnénk lefuttatni a ponthalmazra a t-SNE algoritmust, s ezek közül
a legjobbat fogjuk majd megtartani.\newline
Amennyiben túl nagy adathalmazzal van dolgunk, a t-SNE algoritmus futása napokig is eltarthat. A **sample** paraméterrel
megadható, hogy stílusonként hány véletlenszerűen kiválasztott pontra fusson az algoritmus. Amennyiben percentilis szűrést
is alkalmazunk, a mintavételezés a megfelelő percentilisek kiválogatása után fog megtörténni.

#### Közeli szomszédok keresése
Az alábbi paranccsal tudjuk egy véletlenszerűen kiválasztott pont szomszédait kilistázni:
\begin{verbatim}pipenv run python -m src.infer.neighbours \\end{verbatim}
\begin{verbatim}    --input [codes].csv \\end{verbatim}
\begin{verbatim}    --topk [K] \\end{verbatim}
\begin{verbatim}    --percentiles 50-100 \end{verbatim}

A **topk** paraméter segítségével megadhatjuk, hogy a pontnak hány darab legközelebbi szomszédját szeretnénk kilistázni.\newline
A **percentiles** paraméterrel megadhatjuk, hogy a kereséshez mely percentilisekhez tartozó pontokat vegyük figyelembe.\newline
Opcionálisan megadható egy **start-index** paraméter is, ez esetben az adott indexű pont szomszédait fogja a program kilistázni.
Az index 0-tól kezdődik és a csv fájl megfelelő sorát jelöli.

#### Lejátszási lista generálása
Az alábbi paranccsal tudunk egy véletlenszerűen kiválasztott pontból kiindulva lejátszási listát generálni:
\begin{verbatim}pipenv run python -m src.infer.suggest \\end{verbatim}
\begin{verbatim}    --input [codes].csv \\end{verbatim}
\begin{verbatim}    --topk [K] \\end{verbatim}
\begin{verbatim}    --length [L] \\end{verbatim}
\begin{verbatim}    --percentiles 50-100 \end{verbatim}

A **topk** paraméter segítségével megadhatjuk, hogy hány darab legközelebbi szomszéd közül válasszuk ki az aktuális
dal után következő dalt.\newline
A **percentiles** paraméterrel megadhatjuk, hogy a generáláshoz mely percentilisekhez tartozó pontokat vegyük figyelembe.\newline
A **length** paraméterrel meghatározhatjuk, hogy a generált lejátszási lista milyen hosszú legyen.\newline
Opcionálisan megadható egy **start-index** paraméter is, ez esetben a lejátszási lista az adott indexű pontból fog kiindulni.
Az index 0-tól kezdődik és a csv fájl megfelelő sorát jelöli.\newline
Opcionálisan megadható egy **seed** paraméter is, amivel a véletlengenerátor seed-jét inicializálni lehet.