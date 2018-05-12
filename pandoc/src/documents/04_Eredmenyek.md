\pagebreak

\thispagestyle{semifancy} 

\pagestyle{fancy}
\rhead{Eredmények}  

# Eredmények

## Látens tér elemzése

Az eredmények ismertetését a modell közvetlen kimenetével, a látens tér elemzésével kezdem. Első lépésként box plotok segítségével
vizualizáltam a dimenziók eloszlását a látens tér egészére, illetve külön külön stílusokra nézve is. A diagrammokon 
egyértelműen látszik, hogy a modell stílustól függően más eloszlást rendel az adott dimenziókhoz, mely az első jele annak, 
hogy a modell, frekvenciaértékek alapján képes volt különbséget tenni a zenestílusok között.

![Boxplot diagram a teljes látens térre nézve](src/images/latent_space_boxplot.png)

![Boxplot diagram, klasszikus stílusra szűrve](src/images/latent_space_boxplot_classical.png)

![Boxplot diagram, elektronikus stílusra szűrve](src/images/latent_space_boxplot_electronic.png)

![Boxplot diagram, metál stílusra szűrve](src/images/latent_space_boxplot_metal.png)

A box plotokat követően elkészítettem egy scatter plot mátrixot (\ref{scatterplot}. ábra) is a teljes adathalmazra, mely 
megmutatja a látens dimenziók
páronkénti kapcsolatát. A diagram átlójában az adott látens dimenzió becsült sűrűségfüggvénye látható.
A mátrixban több helyen is felfedezhetőek átlós alakú scatter plotok (\ref{scatterplot_zoom}. ábra), melyek az adott dimenziók 
közötti korrelációkról árulkodnak.
Kettő látens változó közötti erős korreláció esetén az egyik változót, minimális hiba mellett, 
elő tudjuk állítani a másik változó segítségével.
A látens tér tekintetében ez azt jelenti, hogy a probléma kevesebb dimenziójú térben is modellezhető, a jelenlegi látens tér 
redundáns, azaz eldobható dimenziókat tartalmaz, melyek a többi dimenzó segítségével kifejezhetőek.
Nagyobb adathalmazon történő tanítás esetén ez a fajta redundancia valószínűleg nem állna fenn.

\begin{figure}[H]
\centering
\includegraphics[width=0.9\textwidth]{src/images/latent_space_scatter_plot_matrix.png}
\caption{Scatter plot mátrix a teljes látens térre}\label{scatterplot}
\end{figure}

\begin{figure}[H]
\centering
\includegraphics[width=0.5\textwidth]{src/images/latent_space_scatter_plot_matrix_zoomed.png}
\caption{A scatter plot mátrix egy részlete, melyben a középső plot pozitív korrelációt mutat két látensdimenzió között}\label{scatterplot_zoom}
\end{figure}

A látens tér statisztikai elemzését követően a különálló dalok vizualizációjával is foglalkoztam. Jelölje $m_{a, s, p} \in \mathbb{R}^{32}$
látens térbeli vektor az $a$ előadó $s$ dalának $p$. percentilisét. Továbbá legyen:
\begin{equation}
        m_{a,s} := \sum\limits_{p=50, \; 5|p}^{100} m_{a,s,p} \in \mathbb{R}^{32}
\end{equation}
vektor az $a$ előadó $s$ dalának releváns, azaz 50. és afölötti percentiliseit
összegző vektor. Ezen $m$ vektorokat elkészítettem minden dalhoz, majd radar chart segítségével 
grafikusan ábrázoltam őket. Fontosnak tartom kiemelni, hogy a diagramon látható értékek normalizálva vannak 0 és 1 közé. A 
normalizálás során a dalok között elveszik a nagysági reláció, ezáltal előfordulhat, hogy kettő dal diagrammja hasonlít egymásra,
viszont ennek ellenére azok teljesen más intervallumok között mozognak.
Azért döntöttem a normalizálás mellett, mert számomra elsődlegesen a dalok azonos skálán történő ábrázolása volt a cél, 
hogy a diagramjuk alakját össze tudjam hasonlítani egymással.

![Klasszikus stílus alá tartozó dalok vizualizálva, a dalok rendre: 
Itzhak Perlman - Concerto No.1 in E, RV 269 'Sprint', 
Jeremy Soule - Reign of the Septims,
John Williams - The Imperial March,
Nox Arcana - Castle Dracula,
Walter Klien - Fantasy for Piano No. 3 in D Minor\label{img_cl}](src/images/sample_classical.png)

![Elektronikus stílus alá tartozó dalok vizualizálva, a dalok rendre:
Angelspit - 100%, 
Crystal Castles - Crimewave,
Mind.in.a.box - Walking,
Skrillex - Scary Monsters and Nice Sprites,
The Prodigy - Voodoo People (Pendulum remix)\label{img_el}](src/images/sample_electronic.png)

![Metál stílus alá tartozó dalok vizualizálva, a dalok rendre:
ASP - Krabat,
Dalriada - Téli Ének,
Eluveitie - Inis Mona,
In Flames - Come Clarity,
SlipKnot - Duality\label{img_me}](src/images/sample_metal.png)

A radar chartokon észrevehetőek ismétlődő minták, melyek egy-egy stílus esetén megjelennek. Adott stílusokra tipikusan
mindig ugyanazok a dimenziók a "legaktívabbak". Klasszikus daloknál a 6-10., 13-14. és 16-17. dimenziók között figyelhetünk meg 
aktivitást, elektronikus daloknál jellemzően a 0. és 16. dimenziók által meghatározott tengely mentén
az aktivitás határozott hiánya látható, míg metál stílusú dalok esetén többnyire a 3., 12., 15., 18., 26. és 28-30. dimenziókban 
találhatunk nagyobb értékeket.

Ahhoz, hogy mélyebb betekintést nyerhessek a modell működésébe, kiexportáltam az összes dal radar chart-ját,
majd a képeket stílusok szerint szétválogattam, s átlagoltam őket. Ezáltal láthatóvá vált, hogy a stílusok a látens
tér mely dimenzióiban veszik fel a legnagyobb értékeket. A \ref{img_avg}. ábra alapján látható, hogy a modell alapvetően megtanult
különbséget tenni a különböző gyűjtőstílusok között.

![A teljes adathalmaz radar chartjainak átlagolása stílusok szerint\label{img_avg}](src/images/songs_average.png)

A látens tér elemzését néhány érdekesebb diagrammal szeretném zárni, ahol a dalokhoz azok élő, akusztikus vagy épp remix változatait
társítottam, hogy lássuk a különböző variánsok mennyire hasonlítanak egymásra.

![Apocalyptica - Bittersweet című száma különféle verziókban. Megfigyelhető a hasonlóság az
eredeti és az akusztikus dal között. Az instrmentális dal képe különbözik, hiszen nincs benne vokál, 
viszont bizonyos dimenziók értéke ennek ellenére is változatlan marad.](src/images/img_apocalyptica_bittersweet.png)

![The Prodigy - Spitfire című száma különféle verziókban. Az élő és a 2005-ös verzió is
hasonlóságot mutat az eredetire.](src/images/img_prodigy_spitfire.png)

![Skrillex - Scary Monsters and Nice Sprites című száma különféle verziókban](src/images/img_skrillex_scary.png)

## t-SNE

A t-SNE algoritmus alkalmas magasabb dimenziójú ponthalmazok 2-dimenziós ábrázolására. A vizualizáció segítségével átfogóbb képet kaphatunk
a 32-dimenziós tér struktúrájáról. Érdemes megemlíteni, hogy a 32-ről 2-dimenzióra történő csökkentés torzulással jár, az eredeti
adathalmaznak csupán az "árnyékát" láthatjuk.
Emiatt a t-SNE algoritmus eredménye sokszor félrevezető lehet, az eredmény csupán a pontok közötti relatív viszonyokat mutatja meg.
A címkézett adatok birtokában viszont viszonyítási alapunk van arra, hogy a t-SNE eredményeképp egymáshoz közel rendelt pontok
és azok stílusai között érdemi kapcsolat van-e.

![t-SNE futtatása stílusonként 3000 pontra 50-100 percentilisekre\label{tsne_50}](src/images/tsne_real_50perc_9k.png)

![t-SNE futtatása stílusonként 3000 pontra 75-100 percentilisekre\label{tsne_75}](src/images/tsne_real_75perc_9k.png)

A \ref{tsne_50}. és \ref{tsne_75}. ábrák különböző percentilis intervallumokon futtatott t-SNE futási eredményeket mutatnak.
Mivel az algoritmus futási ideje nagyon hosszú lenne a teljes adathalmazra nézve, ezért mindkét esetben stílusonként 3000
pontot mintavételezve, tehát összesen 9000 pontra végeztem el a vizualizációt.

A diagrammokon látható, ahogyan a stílusok jobbára elkülönülnek, néhol összemosódnak egymással. 
Mivel a zenei stílusokra nem diszkrét, hanem inkább fuzzy halmazokként tekinthetünk, elfogadhatónak tartom, 
hogy a stílusokhoz tartozó klaszterek egymáshoz közel helyezkednek el, s azok között átfedések, átmenetek fedezhetőek fel.

A diagrammokat alaposabban szemlélve észrevehetjük, hogy outlier pontok fel-felbukkannak a képeken. Ez egyrészt betudható
a modell tényleges hibájának, másrészről lehetséges, hogy egy félrecímkézett pontról van szó. Mivel címkézés során egy album
összes dalához egységesen rendeltem stíluscímkét, ezért előfordulhat, hogy egy metál album szimfonikus intro és outro dala is metál címkét
kapott, miközben helyesen klasszikus címkét kellett volna kapjanak. Az algoritmus nem néz címkéket, így ezek a helytelenül metál 
stílusúnak címkézett dalok hangzásuk alapján helyesen a klasszikus klaszterbe kerülhettek. Amennyiben egy nem klasszikusnak címkézett
albumban találhatóak olyan dalok, melyekben tradícionális hangszerek vannak túlnyomó többségben, azok ugyanúgy a klasszikus
klaszterhez kerülhetnek a diagrammokon. Hasonlóképp, amennyiben egy nem elektronikusnak címkézett album tartalmaz remix dalokat,
azok nagy valószínűséggel az elektronikus klaszter közelében fognak elhelyezkedni, attól függetlenül, hogy a címkéjük mást mond.

Gépi tanulási algoritmusok esetén, főképp osztályozásnál, bevett szokás vizsgálni, hogy a modell mennyivel teljesít jobban
a véletlenszerű találgatásnál. Ezt a megközelítést kíséreltem meg alkalmazni saját modellem kapcsán is, melyhez az 
alábbi kérdést tettem fel: "Vajon a modellem megbízhatóbban működik-e, mintha véletlen vektorokat generálnék és azokat 
rendelném hozzá az adott dalokhoz?" A kérdés megválaszolásához az adathalmazhoz elkészítettem annak véletlenszerű
koordinátákkal feltöltött változatát. Az eredeti adathalmazhoz tartozó sorokat szétválasztottam stílusok szerint,
majd mindegyik stílushoz kiszámoltam, hogy annak dimenziói rendre mekkora minimum és maximum értékeket vesznek fel. Ezt követően
minden dalhoz egyenletes eloszlással hozzárendeltem egy dimenzióértéket a stílus adott dimenziójának minimum és maximum értékei között.

A véletlenszerű adatokkal feltöltött csv fájlra is lefuttattam a vizualizációt, hogy megnézzem, a t-SNE véletlenszerűen
előállított adathalmaz esetén is képes-e hasonló struktúrák "felfedezésére". A \ref{tsne_random}. ábrán látható, hogy
a hamis adathalmaz esetén a t-SNE nem mutatott ki semmilyen szabályszerűséget.

Mindezek alapján, a t-SNE 2-dimenziós megjelenítése megerősítette, hogy a modell képes volt alapvető különbségeket tenni
a gyűjtőstílusok között. Továbbá, a vizualizáció alapján sejthető, hogy a 32-dimenziós látens tér bizonyos részei, a klaszterek belső
területei homogénebbek,
míg a stílusok határainál inhomogén területekkel találkozhatunk.

![t-SNE futtatása hamis, véletlenszerűen generált adatokra\label{tsne_random}](src/images/tsne_random.png)

## k-legközelebbi szomszéd

A modell egyik gyakorlati alkalmazása a percentilisekhez generált kódok szomszédainak lekérdezése, mely során láthatjuk, 
hogy az adott dalszelet közelébe a modell mely másik szeleteket helyezi. Távolságfüggvénynek a megszokott euklideszi
távolságot használtam. 

A példákon látható, hogy az eredményt nagyban befolyásolja, hogy a látens tér mely részéből indulunk ki. Ha a kiindulási
pont a látens tér homogén tartományába esik, a szomszédok egyöntetűen ugyanazzal a stíluscímkével rendelkeznek. Amennyiben
inhomogén területhez tartozó pont szomszédait vesszük, például kettő stílus határáról, a szomszédsági lista a két stílus határához
tartozó dalokból fog vegyesen tartalmazni.

A lekérdezések során outlier-ek is felfedezhetőek voltak. Ezek olyan dalok, melyek hangzásra egyáltalán nem hasonlítanak az eredeti,
kiindulási dalhoz. A modell 3.7 másodperces dalszeleteknek megfelelő képekből generálja a 32-dimenziós kódokat, s előfordulhat,
hogy két dalból kiragadott pár másodperces szelet hasonlít egymásra, míg a teljes 3-5 perces dalok
összességében tekintve egymástól nagyon különbözőek lehetnek.

Az "outlier-ek" másik csoportját a félrecímkézett dalok alkották, melyek természetesen nem igazi outlier-ek. 
Érdekes volt számomra látni, hogy a modell egy klasszikus
címkéjű dal szomszédai közé sorolt egy metál címkével ellátott dalt, mivel az egy metál album szimfonikus intermezzoja volt.

A táblázatok 0. sora a kiindulási pont, $k$-adik legközelebbi szomszéda a $k$-adik sorbeli dal.

\footnotesize\csvautolongtable[
  table head={
    \hline \rowcolor{black!15} \# & Stílus & Előadó & Dal & Percentilis \\\hline
    \endfirsthead
    \hline
    \caption{Midnight Syndicate előadó Forgotten Path című dalának legközelebbi szomszédai ugyanazon dal további szeletei}
    \endfoot
  },
  respect all
]{src/tables/01_classical_midnight.csv}\normalsize

\footnotesize\csvautolongtable[
  table head={
    \hline \rowcolor{black!15} \# & Stílus & Előadó & Dal & Perc. \\\hline
    \endfirsthead
    \hline
    \caption{A kiindulási dalszelet egy Bach mű (BWV Anh.125) Christfried Bickenbach előadásában.
    A szelet legközelebbi szomszédai további Bach művek ugyanarról az albumról.}
    \endfoot
  },
  respect all
]{src/tables/02_classical_bach.csv}\normalsize

\footnotesize\csvautolongtable[
  table head={
    \hline \rowcolor{black!15} \# & Stílus & Előadó & Dal & Percentilis \\\hline
    \endfirsthead
    \hline
    \caption{ASP előadó Ich Will Brennen dalának átdolgozásának legközelebbi szomszédai 
    ugyanazon dal további, illetve az eredeti dal szeletei.}
    \endfoot
  },
  respect all
]{src/tables/03_metal_asp.csv}\normalsize

\footnotesize\csvautolongtable[
  table head={
    \hline \rowcolor{black!15} \# & Stílus & Előadó & Dal & Percentilis \\\hline
    \endfirsthead
    \hline
    \caption{A kiindulási pont legközelebbi szomszédai között van ugyanazon dal 60. percentiliséhez
    tartozó szelete, illetve egy másik dal is ugyanattól az előadótól.}
    \endfoot
  },
  respect all
]{src/tables/04_metal_mixed.csv}\normalsize

\footnotesize\csvautolongtable[
  table head={
    \hline \rowcolor{black!15} \# & Stílus & Előadó & Dal & Percentilis \\\hline
    \endfirsthead
    \hline
    \caption{Egy outlier megjelenése a 3. sorban, mely stilisztikailag nem illik a kiindulási ponthoz.}
    \endfoot
  },
  respect all
]{src/tables/05_classical_outliers.csv}\normalsize

\pagebreak
\footnotesize\csvautolongtable[
  table head={
    \hline \rowcolor{black!15} \# & Stílus & Előadó & Dal & Percentilis \\\hline
    \endfirsthead
    \hline
    \caption{Egy teljes mértékben véletlenszerűnek tekinthető szomszédsági lekérdezés eredménye,
    valószínűsíthetőleg a dalszeletek rövidségének következtében.}
    \endfoot
  },
  respect all
]{src/tables/06_outlier_too_short_slices.csv}\normalsize

\footnotesize\csvautolongtable[
  table head={
    \hline \rowcolor{black!15} \# & Stílus & Előadó & Dal & Percentilis \\\hline
    \endfirsthead
    \hline
    \caption{A kiindulási pont egy instrumentális dalszelet. A metál címkéjű dalok ismeretében belátható, hogy ezek a dalok
    szimfonikus/akusztikus dalok metál albumokból.}\label{table_mislabeled}
    \endfoot
  },
  respect all
]{src/tables/07_mislabeled_metal.csv}\normalsize

\footnotesize\csvautolongtable[
  table head={
    \hline \rowcolor{black!15} \# & Stílus & Előadó & Dal & Percentilis \\\hline
    \endfirsthead
    \hline
    \caption{A kezdeti dal egy metál album szimfonikus intermezzo dala, a \ref{table_mislabeled}. táblázathoz
    hasonlóan, ez a szomszédsági lekérdezés helyes.}
    \endfoot
  },
  respect all
]{src/tables/09_classical_metal_intermezzo.csv}\normalsize

## Lejátszási lista generálás

A generált lejátszási listák vizsgálata során is hasonlóakat tapasztaltam mint a szomszédsági lekérdezéseknél:
inhomogén területről indított algoritmus esetén, a generált lejátszási lista alternált a stílusok között. 
Ez nem is meglepő, hiszen a lejátszási lista 
készítő algoritmus szomszédsági lekérdezések révén fűzi a dalokat egymás után. Emiatt természetesen a szomszédsági lekérdezéseknél
megfigyelt outiler-ek itt is előfordultak.

Másik észrevételem, hogy a modell megfelelően generalizál amennyiben
csupán a három gyűjtőstílust vesszük figyelembe, viszont a modell nem tesz érdemi különbséget például két elektronikus
dal között, azok hiába tartoznak eltérő alstílusba.

\footnotesize\csvautolongtable[
  table head={
    \hline \rowcolor{black!15} \# & Stílus & Előadó & Dal & Percentilis \\\hline
    \endfirsthead
    \hline
    \caption{Lejátszási lista generálása a látens tér egyik homogén részéből indítva. A lejátszási lista metál stíluson
    belül marad. Az előadók többször szerepelnek, az algoritmus vissza-visszatér hozzájuk.}
    \endfoot
  },
  respect all
]{src/tables/playlist_01_metal.csv}\normalsize

\footnotesize\csvautolongtable[
  table head={
    \hline \rowcolor{black!15} \# & Stílus & Előadó & Dal & Percentilis \\\hline
    \endfirsthead
    \hline
    \caption{A kiindulási pont a látens tér elektronikus-metál határához közel helyezkedhetett el. Emiatt tapasztalható,
     hogy a lejátszási lista a két stílus közötti alternál.}
    \endfoot
  },
  respect all
]{src/tables/playlist_02_alternates.csv}\normalsize

\footnotesize\csvautolongtable[
  table head={
    \hline \rowcolor{black!15} \# & Stílus & Előadó & Dal & Percentilis \\\hline
    \endfirsthead
    \hline
    \caption{Egy elektronikus dalokat tartalmazó lejátszási lista. A lista dalait szemlélve észrevehető, hogy a modell
    nem tesz különbséget az alstílusok között. A lejátszási listában vegyesen megtalálhatóak EBM, Aggrotech, Dance, Psychedelic Trance,
    és Future pop stílusú dalok is.}
    \endfoot
  },
  respect all
]{src/tables/playlist_03_electronic.csv}\normalsize

\footnotesize\csvautolongtable[
  table head={
    \hline \rowcolor{black!15} \# & Stílus & Előadó & Dal & Percentilis \\\hline
    \endfirsthead
    \hline
    \caption{Egy teljes mértékben véletlenszerűnek tekinthető lejátszási lista, mely betekintést nyújt a látens tér kaotikusabb területeire.}
    \endfoot
  },
  respect all
]{src/tables/playlist_04_outliers.csv}\normalsize

\footnotesize\csvautolongtable[
  table head={
    \hline \rowcolor{black!15} \# & Stílus & Előadó & Dal & Percentilis \\\hline
    \endfirsthead
    \hline
    \caption{Az alábbi klasszikus stílusú dalokat tartalmazó lejátszási lista érdekessége a 10. sorban található dal,
    mely egy tajvani metálbanda népi hangszeres intermezzo-ja. A dalban egy erhu nevű hangszeren játszanak, ami egy kéthúros kínai 
    tradicionális vonós hangszer.}
    \endfoot
  },
  respect all
]{src/tables/playlist_05_misclassified.csv}\normalsize