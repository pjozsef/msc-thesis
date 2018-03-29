\pagebreak

\thispagestyle{semifancy} 

\pagestyle{fancy}
\rhead{Elméleti háttérismeretek}  

# Elméleti háttérismeretek

## Zeneelméleti alapok

### Hanghullám
A hang, fizikai tekintetben, valamilyen közegben terjedő rezgéshullám. A hangszeren egy húrt megpendítve,
vagy amikor beszélünk, a hangszálainkkal a levegő részecskéit mozgásba hozzuk. Ezen részecskék tranzitív
módon a velük érintkező részecskéket is mozgásba hozzák. Így terjed a hang.[@url_hangtan]

### Hang frekvenciája
A hang frekvenciája hanghullám másodpercenkénti rezgésszámát határozza meg. Ez a periódusidő reciproka, 
mértékegysége a Hertz (Hz). Az alacsonyabb frekvenciájú hangokat mélynek, a magasabb frekvenciájú hangokat
pedig magasabb hangként érzékeljük.[@url_hangtan]
    
### Alaphang, felhang
Az általunk érzékelt hang több részhangnak az együtteséből áll. A legmélyebb részhangot nevezzük alaphangnak.
A további részhangokat felhangoknak nevezzük. Egy tetszőleges $f$ frekvencia esetén az alaphang frekvenciája $f$,
a rákövetkező $n$ darab felhang frekvenciái pedig rendre $i*f$, ahol $i \in [2,n]$[@url_hangtan]

### Hang amplitúdója
A hang amplitudója, a hanghullám maximális eltérése az x tengelytől. 
Az alacsony amplitudójú hanghullámot halknak, a nagyobb amplitúdójút pedig hangosabbnak halljuk.[@url_hangtan]

### Hangszín
Ugyanazt a frekvenciájú hangot zongorán és gitáron lejátszva egyértelműen el tudjuk dönteni, 
hogy épp melyik hangszert halljuk. A különbség a zongora és a gitár húrjainak fizikai tulajdonságában rejlik. 
Mindkettő más jelalakú (szinusz, háromszög, fűrészfog, négyszög, stb.) hanghullámot gerjeszt, 
melyekben a felhangok más mértékben vannak jelen. A hang magasságát az alaphang frekvenciája, 
a hangszínét pedig a felhangok erősségének a variációja határozza meg.
   
### Hallható hangtartomány
Hallható hangtartomány alatt a 20Hz és 20 kHz közötti frekvenciatartományt értjük.

## Jelfeldolgozás

### Analóg jelből digitális jel
Ahhoz, hogy a számítógépen hangfájlokkal dolgozhassunk, a folytonos analóg jelet digitalizálnunk kell. Digitalizálás során 
a jelből azonos időközönként mintavételezünk, s ezzel a diszkretizációval próbáljuk közelíteni az eredeti jelet.

Sample rate-nek (mintavételezési ráta) nevezzük azt a mennyiséget, ahányszor másodpercenként mintavételezünk, mértékegysége a Hz. 
CD formátum esetén a mintavételezési frekvencia 44100 Hz, azaz 44.1 kHz.

A bit depth (bitmélység) segítségével adjuk meg, hogy hány biten ábrázoljuk az adott mintát. A bitmélység tipikusan 8,
16, 32 bit szokott lenni. 

### MP3 formátum
Az MP3 formátum egy veszteséges tömörítés.
A tömörítés minősége a bit rate-től (bitráta) függ, mely azt határozza meg, hogy egy másodpercnyi digitális jelet hány biten tárolunk el.
Minél nagyobb a bitráta, annál jobban és részletesebben tudjuk eltárolni az adott jelet, viszont annál
több tárhelyet is foglal a fájl. Minél kisebb a bitmélység, a mintavételezett hangfájl annál kevesebbet foglal, viszont
a minőség is annál rosszabb az eredeti jelhez viszonyítva. A bitrátát célszerű az adott feladathoz viszonítva megválasztani.
Az emberi beszéd például alacsonyabb bitráta mellett is elkódolható, míg zeneszámok esetében célszerű magasabb rátával dolgozni.
Néhány elterjedtebb bitráta:
* 64 Kbps - emberi hang
* 96 Kbps - emberi hang
* 128 Kbps - zene
* 256 Kbps - zene
* 320 Kbps - zene

### MP3 tag
MP3 tag-ek, azaz címkék segítségével metaadatokat rendelhetünk az MP3-as dalokhoz. Ezek közül a leggyakoribb címkék a dal címe,
előadója, albuma, album éve, dal stílusa.

### Fourier Transzformált
Ditigális jelfeldolgozás szemszögéből nézve a (Diszkrét) Fourier Transzformált nem más, mint egy eszköz, mely segítségével a diszkretizált
mintavételeinket szétbonthatjuk alkotórészeire, azaz különálló frekvenciákra.
Ezt egyfajta leképezésnek is tekinthetjük, mely során a digitális jelet az idő domain-ből a frekvencia domain-be képezzük le. 
Az Inverz Fourier Transzformált segítségével pedig fordítva, a frekvencia domain-ből tudjuk visszaalakítani az eredeti digitális jelet.

A Fourier Transzformáltat a következőképp kapjuk:
\begin{equation}\label{fouriertransform}
\begin{split}
    X(k) = \sum\limits_{n=0}^{N-1}x(n)W_N^{kn}, \qquad & 0 \leqslant k \leqslant N-1 \\
    & W^j_n=e^{-j2\pi/n}
\end{split}
\end{equation}
Gyakorlati alkalmazáskor a Gyors Fourier Transzformáltat használjuk, melynek futási ideje O(n^2) helyett csupán O(n log n)
[@guide_to_digital_signal_processing][@algterv]

### Nyquist-Shannon-féle mintavételezési tétel
A Nyquist-Shannon tétel kimondja, hogy veszteségmentes digitalizáshoz az analóg jel maximális frekvenciájának legalább kétszeresével
kell a mintavételezést másodpercenként elvégeznünk.[@nyquist]

Ezen tétel miatt lett a CD formátum mintavételezési frekvenciája 44.1 kHz, mely kicsivel több, mint az emberi hallás felső küszöbe
(20 kHz).

## Gépi tanulás

A gépi tanulás a mesterséges intelligenciának egy olyan ága, mely során az algoritmsnak az úgy nevezett
tanítási fázisban példaadatokat mutatunk, s elvárjuk hogy a bemenetekre adott
kimenete és a ténylegesen elvárt kimenet közötti különbség minimális legyen. [@book_deeplearning]

### Felügyelt tanulás
Angolul supervised learning. Felügyelt tanulásról akkor beszélünk, ha megcímkézett adathalmazzal dolgozunk.
Ilyen esetben tanulás során a modellnek megadjuk a bemenetet, s a modell kimenetét összevetjük a bemenő adathoz
tartozó eredeti címkével. Felügyelt tanulás például az osztályozás, illetve a regresszió.
  
### Felügyelet nélküli tanulás
Angolul unsupervised learning. Felügyelet nélküli tanulás esetén csupán a nyers adathalmazzal dolgozunk,
nem áll rendelkezésünkre címke az adott elemekhez. Felügyelet nélküli tanulás körébe tartozik például a 
klaszterezés, dimenzió csökkentés és az anomália detektálás is.
  
### Hibafüggvény
Hibafüggvénynek nevezzük azt a függvényt, mely az elvárt és kapott kimeneteket egy valós számra
képezi le.
\begin{center}
     $C:Y \times \hat{Y} \rightarrow \mathbb{R}$, ahol 
     \newline $Y$ az elvárt kimenetek halmaza, 
     \newline $\hat{Y}$ pedig a modell által adott kimenetek halmaza.
\end{center}
Tanulás során a hibafüggvény minimalizálása a cél.
  
### Négyzetes hibafüggvény
Angolul quadratic loss function, gyakran használt hibafüggvény:
\begin{equation}
     C(y, \hat{y})= (y-\hat{y})^2 \text{, ahol } y \in Y, \, \hat{y} \in \hat{Y}.
\end{equation}

### Hiperparaméter
Egy adott algoritmusnak több olyan "paramétere" lehet, melyek nem közvetlenül, hanem közvetve
befolyásolják a teljesítményét. Ezen paramétereket nevezzük az algoritmus hiperparamétereinek. 
Hiperparaméter például, hogy az algoritmust hány iteráción keresztül tanítjuk. Random forest esetén
hiperparaméternek tekinthetjük a döntési fák számát, illetve azok mélységét. Support Vector Machine (SVM) esetén
pedig a modell által használt kernel is hiperparaméter. 
  
### Alulilleszkedés
Angolul underfitting. Egy modell alulilleszkedik, ha nem képes rendesen modellezni a tanuló halmazt,
illetve nem generalizál jól új adatra sem. Ilyen esetben a modell hibája nagy mind a tanuló halmazra, 
mind az ismeretlen adatokra egyaránt. Alulilleszkedés esetén célszerű erőteljesebb gépi tanulási 
algoritmust használni, vagy a meglévő algoritmus hiperparaméterein finomhangolni, illetve a több ideig tanítani a modellt.
  
### Túlilleszkedés
Angolul overfitting. Egy modell túlilleszkedik, ha a tanuló halmazt nagyon jól modellezi, azaz hibája alacsony,
viszont a túlilleszkedés miatt nem generalizál jól, ezért új adatok esetén nagy a hibája. Túlilleszkedés esetén
célszerű regularizációt használni, a modell paramétereinek számát csökkenteni, illetve a tanulóhalmaz méretét növelni.
  
![Alulilleszkedés és túlilleszkedés szemléltetése](src/images/overfit-underfit.png)
  
### Tanuló halmaz
Angolul training set. Az az adathalmaz melyen az algoritmust betanítjuk.

### Ellenőrző halmaz
Angolul test set. Ezen az adathalmazon értékeljük ki a végleges modellünk teljesítményét. Ennek a halmaznak
az elemeivel a modell nem találkozott a tanítás során.

### Keresztellenőrző halmaz
Angolul crossvalidation set. Tanítás során ezt az adathalmazt használjuk arra, hogy a modellünk 
hiperparamétereit finomhangoljuk. Azért használunk erre a célra egy külön halmazt, nem pedig az 
ellenőrző halmazt, mert ahogy a modell paraméterei túlilleszkedhetnek a tanulóhalmazra, 
úgy a hiperparaméterei is túlilleszkedhetnek az ellenőrző halmaz elemeire.

## Neuronhálók

### Perceptron
A perceptron egy bináris mesterséges neuron, melyet az 1950-es, 60-as években dolgozott ki Frank Rosenblatt[@perceptron_rosenblatt].
Manapság csupán historikus jelentősége van, viszont a perceptronon keresztül könnyű szemléltetni magának
a neuronhálónak, illetve a modern neuron típusoknak a működését is.\newline
A perceptron bemenetül egy tetszőleges $n$ hosszúságú bináris $x \in \mathbb{B}^n$ vektort vár. Minden perceptronnak 
rendelkezik egy saját $w \in \mathbb{R}^n$ súlyvektorral, melyek az egyes bemenetek "fontosságát" határozzák meg.
A neuron $a \in \mathbb{B}$ bináris kimenete attól függően 1, vagy 0, hogy a bemeneti vektor és a súlyvektor skalárszorzata egy adott 
$t \in \mathbb{R}$ küszöbértéknél nagyobb-e vagy sem.[@nn_and_deeplearning] Matematikailag formalizálva:
\begin{equation}\label{perceptron1}
  a =
  \begin{cases}
    0 & \text{ha } \sum\limits_{j=1}^{n} x_jw_j \leqslant t \\
    1 & \text{ha } \sum\limits_{j=1}^{n} x_jw_j > t
  \end{cases}
\end{equation}
  
![Példa egy három bemenetet váró perceptronra. Forrás:[@nn_and_deeplearning]](src/images/perceptron.png){width=50%}

### Bias
A \ref{perceptron1}. egyenlet könnyebb kezelhetősége érdekében vezessük be a bias fogalmát, mely definíció szerint
$b \equiv -1 * t, b \in \mathbb{R}$. A bias azt jelöli, hogy a perceptron mennyire könnyen tud aktiválódni.
Negatív, kicsi bias esetén a perceptron ritkábban; pozitív, nagy bias esetén sűrűbben aktiválódik. A \ref{perceptron1}.
egyenletet egyszerűsítve, s a bias-t bevezetve a következő egyenletet kapjuk:
\begin{equation}
    a =
    \begin{cases}
      0 & \text{ha } x \cdot w + b \leqslant 0 \\
      1 & \text{ha } x \cdot w + b > 0
    \end{cases}
\end{equation}
    
### Sigmoid neuron
Egy neuronháló betanítása során azt szeretnénk, hogy a súlyokban, illetve bias-okban történő kis változás a neuronháló
kimenetében is csupán kis változást okozzon. Perceptronok esetében ez nem teljesül, hiszen a kimenetük diszkrét érték.
A sigmoid neuron kimenete ezzel ellentétben egy 0 és 1 közötti valós szám: $a \in \mathbb{R}|_{0 \, \leqslant \, a \, \leqslant \, 1}$.
A perceptronhoz hasonlóan, a sigmoid neuron is rendelkezik súlyokkal és bias értékkel, viszont a kimenet számítása az
alábbiak szerint változik:
\begin{equation}\label{sigmoid-neuron}
      a = \sigma(x \cdot w + b)
\end{equation}
A klasszikus sigmoid neuron esetén $\sigma$-t sigmoid függvénynek hívjuk:
\begin{equation}
      \sigma(z) \equiv \frac{1}{1+e^{-z}}
\end{equation}
Megfigyelhető, hogy $\sigma$-t a fentebbi lépcsős függvénynek választva visszakapjuk a perceptron neuront. Az $a$ értéket
kimenet mellett szokás még a neuron aktivációjának is nevezni.

### Aktivációs függvény
A sigmoid neuron felfedezése óta sok előrelépés történt a neuronhálók területén, s a sigmoid függvénynél optimálisabb aktivációs 
függvények terjedtek el. Ezek közül néhány:

#### Tanh
A közismert hiberbolikus tangens függvény az x tengelyre szimmetrikus, s a [-1, 1] intervallumon vesz fel értékeket. 
Ez a tulajdonság azért szerencsés, mert így nagyobb eséllyel kapunk 0-hoz közeli értéket, 
ami a rákövetkező réteg inputjaként fog szolgálni. A 0-hoz közeli input gyorsabb konvergenciához vezet.[@efficient_backprop]
\begin{equation}
      tanh(x) = \frac{e^{2x}-1}{e^{2x}+1}
\end{equation}

#### RELU
A sigmoid, tanh aktivációs függvények esetén fenn áll a probléma, hogy nagyon nagy bemenetre a derivált
értéke a 0-hoz közelít. A [[Gradient Descent]] és [[Backpropagation]] szekciónál látni fogjuk, hogy a neuronháló annál
gyorsabban tanul, minél nagyobb a gradiens. Nullához közeli gradiens esetén a háló szinte semmit sem fog tanulni. Ezt a problémát Vanishing
Gradient problémának nevezik.

A RELU (Rectified Linear Unit) aktivációs függvény ezt a problémát hivatott megoldani:
\begin{equation}
  relu(x) = max(0, x)
\end{equation}

#### ELU
Az ELU (Exponential Linear Unit) aktivációs függvény a RELU továbbfejlesztése. RELU esetén, mint ahogy a sigmoid függvénynél is láttuk,
a függvény átlagos értéke nincs közel a 0-hoz. Az ELU függvény segítségével, átlagosan nézve, a 0-hoz közelebbi értékeket kapunk.[@elu]
\begin{equation}
  elu(\alpha, x) =
  \begin{cases}
    \alpha(e^x -1) & \text{ha } x < 0 \\
    x & \text{ha } x \geqslant 0
  \end{cases}
\end{equation}
  
![Aktivációs függvények a [-10, +10] intervallumon ábrázolva.](src/images/activations.png)
  
### Súlyozott bemenet
Angolul weighted input. A neuron súlyozott bemenete nem más, mint a (\ref{sigmoid-neuron}) egyenlet azon része, 
melyet $\sigma$-nak paraméterül átadunk, azaz:
\begin{equation}
      z \equiv x \cdot w + b
\end{equation}

### Neuronháló
A neuronháló, intuitív módon megfogalmazva, nem más mint egy nemlieáris függvény approximátor. A neuronháló egy bemeneti, 
egy kimeneti és közöttük tetszőletes számú rejtett régetből áll. Egy réteg tetszőleges számú neuronból állhat. Több 
réteg esetén az első réteg aktivációja szolgál a rákövetkező réteg bemeneteként.

Matematikai oldalról tekintve egy neuronháló nem más, mint mátrix szorzások, vektor összeadások és aktivációs függvény
hívások sorozata. (\ref{sigmoid-neuron}) alapján, a neuronháló $l$-edik rétegének $a^l$ aktivációja a következőképp
számolható ki:
\begin{equation}
      a^l = \sigma(a^{l-1} \times W^l + b^l)
\end{equation}
, ahol $a^{l-1} \in \mathbb{R}^m$, $W^l \in \mathbb{R}^{m \times n}$, $b^l \in \mathbb{R}^n$ és $a^l \in \mathbb{R}^n$

![Példa egy rejtett réteget tartalmazó neuronhálóra. Forrás:[@nn_and_deeplearning]](src/images/nn.png){width=75%}

### Neuronháló hiperparaméterei
Egy neuronhálónak rengeteg hiperparamétere lehet:
* Hány epoch-on keresztül tanítjuk a hálót.
* Mekkora learning rate-tel.
* Milyen hibafüggvényt használunk.
* Rétegek száma a neuronhálóban.
* Egyes rétegek hány neuronból állnak.
* Használunk-e regularizációt. És ha igen, akkor milyen mértékben.
* Milyen aktivációs függvényeket használunk.
* A kezdeti súlyokat hogyan inicializáljuk.

### Regularizáció
A regularizáció a túlilleszkedés ellen nyújt hatékony megoldást. Alkalmazásával a hibafüggvény mellé további megkötéseket 
tehetünk a neuronhálóra, például büntetjük a nagyon nagy súlyokat, mely segítségével a hálót a generalizálás irányába tereljük,
mintsem afelé, hogy a különálló bemenetek zajaira illeszkedjen. Egy súlyt csak akkor tud nagyra nőni, ha a regularizáció büntetést
ellenére is nagy mértékben javít a modell pontosságán.

#### L2 regularizáció
L2 regularizáció esetén a súlyok ($w \in \mathbb{R}$) négyzetnét összegezzük. A bias-okat nem regularizáljuk.
\begin{equation}
      C_{reg} = C(y, \hat{y}) + \lambda \sum\limits_w w^2
\end{equation}
, ahol $\lambda \in \mathbb{R}, \lambda > 0$ a regularizációs paraméter.[@nn_and_deeplearning]

#### L1 regularizáció
L1 regularizáció esetén a súlyok ($w \in \mathbb{R}$) abszolútértékét összegezzük. A bias-okat nem regularizáljuk.
\begin{equation}
      C_{reg} = C(y, \hat{y}) + \lambda \sum\limits_w |w|
\end{equation}
, ahol $\lambda \in \mathbb{R}, \lambda > 0$ a regularizációs paraméter.[@nn_and_deeplearning]

#### Dropout
Dropout esetén nem a súlyokat regularizáljuk, hanem tanítás alatt magát a neuronhálót módosítjuk, pontosabban véve
azt, ahogyon a $\hat{y}$ kimenetet megkapjuk. A tanítás során, minden példa adat esetén véletlenszerűen "kikapcsoljuk"
a neuronháló rejtett rétegeiben lévő neuronok bizonyos részét. A 0.5 például tipikus dropout érték[@hinton_dropout], mely azt
jelenti, hogy 50% eséllyel hagyjuk csak meg az adott neuront. A "kikapcsolt" neuronok aktivációját 0-nak tekintjük.

A dropout segítségével a neuronhálóból kikényszerítjük, hogy fele annyi neuronnal rendelkezve, előbb az adathalmaz legrobosztusabb
tulajdonságait tanulja meg modellezni, azaz kikényszerítjük, hogy a generalizáljon. Másik oldalról nézve, a neuronok 
folyamatos ki-be kapcsolgatásával úgy is tekinthetjük, hogy nem egy, hanem több, különböző neuronokkal rendelkező hálót tanítunk be, 
melyek nagy eséllyel az adathalmaz más és más részhalmazaira fognak túlilleszkedni, így a neuronhálót egészben nézve, a túlilleszkedés
kevésbé lesz számottevő.[@nn_and_deeplearning][@understanding_dropout]

![Neuronháló dropout regularizáció nélkül, illetve dropout regularizációval. Forrás:[@nn_and_deeplearning]](src/images/dropout.png){width=75%}

### Deep learning
A Deep Learning alapvető elgondolása az, hogy összetett koncepciókat egyszerűbb koncepciók hierarchiájával
tudunk lemodellezni. Deep learningről tipikusan neurális hálók kapcsán beszélhetünk. Ilyenkor azt értjük alatta,
hogy több egyrétegű neuronhálót egymás mellé helyezünk, az egyik  réteg kimenete a következő réteg bemenete.
Több réteg, egymás utáni nemlinearitás segítségével erőteljesebb modellt kapunk, mintha egyetlen, több neuronból álló
réteggel dolgoznánk.[@book_deeplearning]

### Fully connected réteg
Fully connected réteg alatt egy klasszikus neuronháló réteget értjük, melynél minden előző réteg beli neuron össze van kötve
minden rákövetkező réteg beli neuronnal.

### Konvolúciós neuronháló
Konvolúciós neuronhálókat főleg kép, illetve hangfeldolgozásnál használnak.
Egy konvolúciós háló tipikusan konvolúciós, pooling, majd pedig végül fully connected rétegekből épül fel.
 
#### Konvolúciós réteg
A konvolúciós réteg neuronjai, a megszokott, klasszikus neuronhálókéval ellentétben, egy 3 dimenziós térben helyezkednek el
egymáshoz képest, szélesség, magasság és mélység szerint. Ennek megfelelően a konvolúciós réteg bemenete is 3 dimenziós
kell legyen. Egy 800*600-as fekete-fehér, RGB és RGBA csatornákkal rendelkező bemeneti kép mérete rendre 800*600*1, 800*600*3, illetve
800*600*4.

Konvolúciós rétegnél egy fix méretű kernelt (kerneleket) csúsztatunk végig a bemeneten $s$ stride-dal (lépésközzel). A kernelt
szokás még filternek is nevezni. Egy konvolúciós réteg 4 dimenziós: kernel szélesség * kernelmagasság 
* bemeneti csatornák száma * kimeneti csatornák száma.[@cs231n]

#### Konvolúció stride
A stride segítségével definiáljuk, hogy mekkora ugrásokkal csúsztatjuk a kernelünket a bemeneten. Ha a stride 1, akkor
a kernelt mindig egy egységgel toljuk el.[@cs231n]

#### Konvolúció padding
2 dimenziós esetben, egy 10*10-es képen végigcsúsztatva egy 2*2-es kernelt 2*2es stride-dal, a kimenetünk mérete 
5*5-ös lesz. Sokszor előnyös számunkra, ha az adat mérete nem változik a konvolúció során. Padding használata esetén
a kimenet körvonalát annyi nullával rakjuk körbe, hogy megőrizzük az eredeti méretét.[@cs231n]

#### Pooling réteg
A pooling rétegek használata gyakori konvolúciós hálókban. Segítségükkel a konvolúciós réteg aktivációjának méretét tudjuk csökkenteni.
A pooling réteg tipikusan egy 2*2 filter, 2*2 stride-dal.
Max pooling esetén a filter kimenete a 2*2-es terület maximuma, míg Average pooling esetén a terület átlaga.
A pooling a csatornák számát nem csökkenti, csupán csatornánként a szélességet, magasságot.


Pooling réteg használatával, ugyanúgy csúszóablakos módon, csökkenteni tudjuk a neuronhálón áthaladó adat méretét. Pooling
Nagy méretű bemenet esetén szükséges lehet a bemeneti adat méretén csökkenteni, ahogyan haladunk rétegről rétegre. A pooling
réteg, a konvolúciós réteghez hasonlóan.[@cs231n]

### Autoencoder
Az autoencoderek a neuronhálók egy speciális csoportját alkotják. Egy autoencoderrel az egységfüggvényt próbáljuk meg approximálni.
Ezt önmagában triviális feladatot azzal a megszorítással nehezítjük, hogy az autoencoder belső, rejtett rétegeinek dimenziója 
kisebb kell legyen a bemenet dimenziójánál. Ezáltal a háló egyik fele egyfajta tömörítést, dimenzió csökkentést hajt
végre a bemeneti adaton, s a háló másik felének a feladata, hogy ebből a csökkentett méretű köztes reprezentációból
visszaállítsa az eredeti bemenetet. Az adat köztes reprezentációját szokás encoding-nak, illetve code-nak is nevezni.
Ezzel a tömörítéssel-visszaállítással a célunk, hogy az autoencoder megtanuljon egy szemantikailag értelmes 
reprezentációt az adatról, amit más célokra felhasználhatunk, például klaszterezésre.[@hinton_semantic_hashing][@hinton_autoencoder_image_retrieval] 

![Példa egy egyszerű autoencoder-re. Forrás:[@stanford_autoencoders]](src/images/autoencoder.png){height=50%}

### Gradient Descent
A Gradient Descent egy iteratív optimalizáló algoritmus, mely az optimalizálandó célfüggvénynek (egy potenciálisan lokális) minimumát
keresi meg a célfüggvény gradiensének segítségével. A step size, vagy learning rate, $\alpha \in \mathbb{R}, \alpha > 0$ 
a Gradient Descent egy paramétere, mely azt mondja meg, hogy minden egyes iterációban mekkora lépést tegyen az 
algoritmus a gradienssel ellentétes irányba.[@cs231n][@coursera_ng_machine_learning] Adott $\alpha$ learning rate és
$f$ differenciálható célfüggvény esetén az algoritmus $i$-k lépése a következőképp néz ki:
\begin{equation}
        x_{i+1} := x_i - \alpha * \nabla f
\end{equation}

### Backpropagation
A Backpropagation algoritmus segítségével a neuronháló súlyaihoz, bias-aihoz meg tudjuk feleltetni a megfelelő
parciális deriváltakat, ezáltal a Gradient Descent optimalizáló algoritmust neuronhálókra is tudjuk alkalmazni.
Eredetileg 1970-ben mutatták be, viszont igazán csak 1986-ban lett népszerű David Rumelhart, Geoffrey Hinton, és
Ronald Williams cikkje[@article_backprop] révén.

Az algoritmus ismertetése előtt két feltételezést kell tennünk a hibafüggvényről:

1. A hibafüggvény felírható kell legyen a különálló bemenetekhez tartozó hibafüggvények értékének az átlagaként. 
Erre azért van szükségünk, mert a backpropagation segítségével csupán a különálló $x$ bemenetekhez tartozó parciális 
deriváltakat ($\partial C_x / \partial w, \partial C_x / \partial b$) tudjuk kiszámolni. 
A $\partial C / \partial w$ és $\partial C / \partial b$ kiszámolásához átlagoljuk az egyes tanulóadatokhoz tartozó hibát.
\begin{equation}
          C= \frac{1}{n}\sum\limits_{x=1}^{n}C_x\text{, ahol $n$ a tanulóadatok száma.}
\end{equation}
2. A hibafüggvény csakis a neuronháló kimenetétől függ. Természetesen a hiba függ az elvárt $y$ kimenettől is, 
viszont mivel az $x$ bemenetet kötött paraméternek tekintjük, ezért az elvárt $y$ is az.

Egy neuronra tekinthetünk függvényként, egy neuronhálóra pedig összetett függvényként. A Backpropagation algoritmus,
a láncszabály alkalmazásával a hibafüggvény parciális deriváltjai határozza meg a súly/bias paraméterek szerint. 
A parciális deriváltak alapján pedig a súlyokat, bias-okat oly módon tudjuk módosítani, 
hogy adott bemenetre a hibafüggvény értéke csökkenjen.

Első lépésben definiáljuk a kimeneti $L$-edik réteg $j$-edik neuronjához tartozó hibát:
\begin{equation}
  \delta_j^L = \frac{\partial C}{\partial a_j^L} * \sigma '(z_j^L)
\end{equation}

Vektorizált formában, a kimeneti $L$-edik réteg hibája:
\begin{equation}\label{BP2}
  \delta^L = \nabla_a C \odot \sigma '(z^L)
\end{equation}
, ahol $\odot$ jelölje két vektor Hadamard-szorzatát (elemenként vett szorzatát).

Második lépésben definiáljuk egy tetszőleges $l$-edik réteg hibáját a rákövetkező réteg hibájának függvényében:
\begin{equation}\label{BP2}
  \delta^l = ((w^{l+1})^T \delta^{l+1}) \odot \sigma '(z^L)
\end{equation}

(\ref{BP1}) és (\ref{BP2}) kombinálásával a neuronháló minden rétegének a hibáját ki tudjuk számítani.

A hibafüggvény parciális deriváltja adott $l$ réteg $j$-edik neuronjának bias-a szerint:
\begin{equation}\label{BP3}
  \frac{\partial C}{\partial b_j^l} = \delta_j^l
\end{equation}

A hibafüggvény parciális deriváltja adott $l$ réteg $j$-edik neuronjának súlyvektorának $k$-adik eleme szerint:
\begin{equation}\label{BP4}
  \frac{\partial C}{\partial w_{jk}^l} = a_k^{l-1}\delta_j^l
\end{equation}

A (\ref{BP3}) és (\ref{BP4}) egyenletek birtokában a neuronháló bármely paramétere szerinti parciális deriváltat fel tudjuk
írni, ezáltal a Gradient Descent algoritmust tudjuk alkalmazni.[@nn_and_deeplearning]