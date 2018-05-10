\pagebreak

\thispagestyle{semifancy} 

\pagestyle{fancy}
\rhead{Elméleti háttérismeretek}  

# Elméleti háttérismeretek

## Zeneelméleti alapok

### Hanghullám
A hang, fizikai tekintetben nézve, valamilyen közegben terjedő rezgéshullám. A hangszeren egy húrt megpendítve,
vagy amikor beszélünk, a hangszálainkkal a levegő részecskéit mozgásba hozzuk. Ezen részecskék tranzitív
módon a velük érintkező részecskéket is mozgásba hozzák, így terjed a hang.[@url_hangtan]

### Hang frekvenciája
A hang frekvenciája a hanghullám másodpercenkénti rezgésszámát határozza meg, mértékegysége a Hertz (Hz). 
Az alacsonyabb frekvenciájú hangokat mélynek, a magasabb frekvenciájú hangokat
pedig magasabb hangként érzékeljük.[@url_hangtan]
    
### Alaphang, felhang
Az általunk érzékelt hang több részhangnak az együtteséből áll. A legmélyebb részhangot nevezzük alaphangnak.
A további részhangokat felhangoknak nevezzük. Egy tetszőleges $f$ frekvencia esetén az alaphang frekvenciája $f$,
a rákövetkező $n$ darab felhang frekvenciái pedig rendre $i×f$, ahol $i \in [2,n]$. [@url_hangtan]

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

### Mintavételezési ráta
Mintavételezési rátának, angolul sample rate-nek  nevezzük a másodpercenkénti mintavételezések számát, mértékegysége a Hz. 
CD formátum esetén a mintavételezési frekvencia 44100 Hz, azaz 44.1 kHz.

### Bitmélység
A bitmélység, angolul bit depth adja meg, hogy hány biten ábrázoljuk az adott mintát. A bitmélység tipikusan 8,
16, 32 bit szokott lenni. 

### Nyquist--Shannon-féle mintavételezési tétel
A Nyquist-Shannon tétel kimondja, az analóg jel maximális frekvenciájának legalább kétszeresével
kell a mintavételezést másodpercenként elvégeznünk annak érdekében, hogy a digitális jel veszteségmentesen visszaalakítható
legyen analóg jellé.[@nyquist]

Ezen tétel miatt lett a CD formátum mintavételezési frekvenciája 44.1 kHz, mely kicsivel több, mint az emberi hallás felső küszöbének
(20 kHz) a kétszerese.

### MP3 formátum
Az MP3 formátum egy veszteséges tömörítés.
A tömörítés minősége a bit rate-től (bitráta) függ, mely azt határozza meg, hogy egy másodpercnyi digitális jelet hány biten tárolunk el.
Minél nagyobb a bitráta, annál jobb minőségben és részletgazdagabban tudjuk eltárolni az adott jelet, viszont annál
több tárhelyet is foglal a fájl. Minél kisebb a bitráta, a mintavételezett hangfájl annál kevesebbet foglal, viszont
a minőség is annál rosszabb az eredeti jelhez viszonyítva. A bitrátát célszerű az adott feladathoz mérten megválasztani.
Az emberi beszéd például alacsonyabb bitráta mellett is elkódolható, míg zeneszámok esetében célszerű magasabb rátával dolgozni.
Néhány elterjedtebb bitráta:

* 64 Kbps - emberi hang
* 96 Kbps - emberi hang
* 128 Kbps - zene
* 256 Kbps - zene
* 320 Kbps - zene

### MP3 tag
MP3 tag-ek, azaz címkék segítségével metaadatokat rendelhetünk az MP3-as dalokhoz. Leggyakoribb címkék közé tartozik a dal címe,
előadója, albuma, album éve és a stílusa.

### Fourier Transzformált
Ditigális jelfeldolgozás szemszögéből nézve a (Diszkrét) Fourier Transzformált nem más, mint egy módszer, mely segítségével a diszkretizált
mintavételeinket szétbonthatjuk alkotórészeire, különálló frekvenciákra.
Ez a leképezés a digitális jelet az idő domain-ből a frekvencia domain-be képezi le. 
Az Inverz Fourier Transzformált segítségével pedig fordítva, a frekvencia domain-ből idő domain-be tudjuk visszaalakítani a digitális jelet.

A Fourier Transzformáltat a következőképp kapjuk:
\begin{equation}\label{fouriertransform}
\begin{split}
    X(k) = \sum\limits_{n=0}^{N-1}x(n)W_N^{kn}, \qquad & 0 \leqslant k \leqslant N-1 \\
    & W^j_n=e^{-j2\pi/n}
\end{split}
\end{equation}
Gyakorlati alkalmazáskor a Gyors Fourier Transzformáltat (FFT) használjuk, melynek futási ideje O($n^2$) helyett csupán O(n log n)
[@guide_to_digital_signal_processing][@algterv]

## Gépi tanulás

### Felügyelt tanulás
Felügyelt tanulásról (supervised learning) akkor beszélünk, ha megcímkézett adathalmazzal dolgozunk.
Ilyen esetben tanulás során a modellnek megadjuk a bemenetet, s a modell kimenetét összevetjük a bemenő adathoz
tartozó eredeti címkével. Célunk, hogy a modell kimenete megközelítse az elvárt kimenetet.
Felügyelt tanulás például az osztályozás, illetve a regresszió.

### Felügyelet nélküli tanulás
Felügyelet nélküli tanulás (unsupervised learning) esetén csupán a nyers adathalmazzal dolgozunk,
nem áll rendelkezésünkre címke az adott elemekhez. Felügyelet nélküli tanulás körébe tartozik például a 
klaszterezés, dimenzió csökkentés és az anomália detektálás is.
  
### Hibafüggvény
Hibafüggvénynek nevezzük azt a függvényt, mely az elvárt és kapott kimenetet egy valós számra
képezi le.
\begin{center}
     $C:Y \times \hat{Y} \rightarrow \mathbb{R}$, ahol 
     \newline $Y$ az elvárt kimenetek halmaza, 
     \newline $\hat{Y}$ pedig a modell által adott kimenetek halmaza.
\end{center}
Tanulás során a hibafüggvény minimalizálása a cél.
  
### Négyzetes hibafüggvény
Egy gyakran használt hibafüggvény, angolul quadratic loss function-nek hívják.
\begin{equation}
     C(y, \hat{y})= (y-\hat{y})^2 \text{, ahol } y \in Y, \, \hat{y} \in \hat{Y}.
\end{equation}

### Hiperparaméter
Egy adott algoritmusnak több olyan "paramétere" lehet, mely nem közvetlenül, hanem közvetve
befolyásola a teljesítményét. Ezen paramétereket nevezzük az algoritmus hiperparamétereinek. 
Hiperparaméter például, hogy az algoritmust hány iteráción keresztül tanítjuk. Random forest esetén
hiperparaméternek tekinthetjük a döntési fák számát, illetve azok mélységét. Support Vector Machine (SVM) esetén
pedig a modell által használt kernel is hiperparaméter. 
  
### Alulilleszkedés
Egy modell alulilleszkedik (underfitting), ha nem képes rendesen modellezni a tanuló halmazt,
illetve nem generalizál jól új adatra sem. Ilyen esetben a modell hibája nagy mind a tanuló halmazra, 
mind az ismeretlen adatokra egyaránt. Alulilleszkedés esetén célszerű erőteljesebb gépi tanulási 
algoritmust használni, vagy a meglévő algoritmus hiperparaméterein finomhangolni, illetve több ideig tanítani a modellt.
  
### Túlilleszkedés
Egy modell túlilleszkedik (overfitting), ha a tanuló halmazt nagyon jól modellezi, azaz hibája alacsony,
viszont a túlilleszkedés miatt nem generalizál jól, ezért új adatok esetén nagy a hibája. Túlilleszkedés esetén
célszerű regularizációt használni, a modell paramétereinek számát csökkenteni, illetve a tanulóhalmaz méretét növelni.
  
![Alulilleszkedés és túlilleszkedés szemléltetése](src/images/overfit-underfit.png)
  
### Tanuló halmaz
Az az adathalmaz melyen az algoritmust betanítjuk. Angolul training set-nek nevezzük.

### Ellenőrző halmaz
Ezen az adathalmazon értékeljük ki a végleges modellünk teljesítményét. Ennek a halmaznak
az elemeivel a modell nem találkozott a tanítás során. Angolul test set-nek nevezzük.

### Keresztellenőrző halmaz
Tanítás során ezt az adathalmazt használjuk arra, hogy a modellünk 
hiperparamétereit finomhangoljuk. Angolul crossvalidation set-nek nevezzük. Azért használunk erre a célra egy külön halmazt, nem pedig az 
ellenőrző halmazt, mert ahogy a modell paraméterei túlilleszkedhetnek a tanulóhalmazra, 
úgy a hiperparaméterei is túlilleszkedhetnek az ellenőrző halmaz elemeire.

### t-SNE
A t-SNE (t-Distributed Stochastic Neighbor Embedding) egy dimenziócsökkentő algoritmus, mely segítségével 2- illetve
3-dimenzióban tudunk magas dimenziójú adatokat vizualizálni. Az algoritmus oly módon csökkenti a bemeneti adathalmaz dimenzióját,
hogy eközben az adatpontok közötti távolsági relációkat megőrzi. Két pont, melyek az eredeti adathalmazban
távol álltak egymástól, dimenziócsökkentés után is távol fognak elhelyezkedni, míg két közeli pont az algoritmus futtatása
után is közel lesz egymáshoz. A perplexity érték a t-SNE algoritmus fontos paramétere, segítségével szabályozhatjuk, hogy
az algoritmus a lokális, vagy inkább a globális struktúrákat vegye jobban figyelembe. Az értéke tipikusan 5 és 50 között
mozog.[@tsne][@tsne_github]

### Tenzor
A tenzor nem más, mint a vektorok és mátrixok általánosítása. A tenzor rendje az egymástól függetelen dimeziók számát jelöli.
Nulladrendű tenzorok a skalárok, elsőrendűek a vektorok, másodrendűek a mátrixok. Fejlesztés során a tenzorokat n-dimenziós
tömbökként kezeljük.[@tensor_definition]

\begin{figure}[H]
\centering
\includegraphics{src/images/tensor.png}
\caption{Példa egy nullad-, első-, másod- és harmadrangú tenzorra.}
\end{figure}

## Neuronhálók

### Perceptron
A perceptron egy bináris mesterséges neuron, melyet az 1950-es, 60-as években dolgozott ki Frank Rosenblatt[@perceptron_rosenblatt].
Manapság csupán historikus jelentősége van, viszont a perceptronon keresztül könnyű szemléltetni magának
a neuronhálónak, illetve a modern neuron típusoknak a működését is.\newline
A perceptron bemenetül egy tetszőleges $n$ hosszúságú bináris $x \in \mathbb{B}^n$ vektort vár. Minden perceptron 
rendelkezik egy saját $w \in \mathbb{R}^n$ súlyvektorral, mely elemei a neuron adott bemeneteinek a "fontosságát" határozzák meg.
A neuron $a \in \mathbb{B}$ bináris kimenete attól függően 1, vagy 0, hogy a bemeneti vektor és a súlyvektor skalárszorzata egy adott 
$t \in \mathbb{R}$ küszöbértéknél nagyobb-e vagy sem.[@nn_and_deeplearning] Matematikailag formalizálva:
\begin{equation}\label{perceptron1}
  a =
  \begin{cases}
    0 & \text{ha } \sum\limits_{j=1}^{n} x_jw_j \leqslant t \\
    1 & \text{ha } \sum\limits_{j=1}^{n} x_jw_j > t
  \end{cases}
\end{equation}
  
![Példa egy három bemenettel rendelkező perceptronra. Forrás:[@nn_and_deeplearning]](src/images/perceptron.png){width=50%}

### Bias
A (\ref{perceptron1}). egyenlet könnyebb kezelhetősége érdekében vezessük be a bias fogalmát, mely definíció szerint
$b \equiv -1 × t,\; b \in \mathbb{R}$. A bias azt jelöli, hogy a perceptron mennyire könnyen tud aktiválódni.
Negatív, kicsi bias esetén a perceptron ritkábban; pozitív, nagy bias esetén sűrűbben aktiválódik. A (\ref{perceptron1}).
egyenletet egyszerűsítve, s a bias-t használva a következő egyenletet kapjuk:
\begin{equation}
    a =
    \begin{cases}
      0 & \text{ha } x \cdot w + b \leqslant 0 \\
      1 & \text{ha } x \cdot w + b > 0
    \end{cases}
\end{equation}
    
### Sigmoid neuron
Egy neuronháló betanítása során a célunk, hogy a súlyokban, illetve bias-okban történő kis változás a neuronháló
kimenetében is csupán kis változást okozzon. Perceptronok esetében ez nem teljesül, hiszen a kimenetük diszkrét érték.
A sigmoid neuron kimenete ezzel ellentétben egy 0 és 1 közötti valós szám: $a \in [0,1]$.
A perceptronhoz hasonlóan, a sigmoid neuron is rendelkezik súlyvektorokkal és bias értékkel, viszont a kimenet kiszámítása az
alábbiak szerint változik:
\begin{equation}\label{sigmoid-neuron}
      a = \sigma(x \cdot w + b)
\end{equation}
A klasszikus sigmoid neuron esetén $\sigma$-t sigmoid függvénynek hívjuk:
\begin{equation}
      \sigma(z) \equiv \frac{1}{1+e^{-z}}
\end{equation}
Megfigyelhető, hogy $\sigma$-t egy 0 és 1 közötti lépcsős függvénynek választva visszakapjuk az eredeti perceptron neuront. Az $a$ értéket
kimenet mellett szokás még a neuron aktivációjának is nevezni.

### Aktivációs függvény
A sigmoid neuron felfedezése óta sok előrelépés történt a neuronhálók területén, s a sigmoid függvénynél optimálisabb aktivációs 
függvények terjedtek el. Ezek közül néhány:

#### Tanh
A közismert tangens hiberbolikusz függvény, mely a $[-1, 1]$ intervallumon vesz fel értékeket. 
Ez a tulajdonság azért szerencsés, mert így nagyobb eséllyel kapunk 0-hoz közeli értéket, 
ami a rákövetkező réteg inputjaként fog szolgálni. A 0-hoz közeli input gyorsabb konvergenciához vezet.[@efficient_backprop]
\begin{equation}
      \text{tanh}(x) = \frac{e^{2x}-1}{e^{2x}+1}
\end{equation}

#### RELU
A sigmoid és tanh aktivációs függvények esetén fennáll a probléma, hogy nagyon nagy bemenetre a derivált
értéke a 0-hoz közelít. A [[Gradient Descent]] és [[Backpropagation]] szekciónál látni fogjuk, hogy a neuronháló annál
gyorsabban tanul, minél nagyobb a gradiens. Nullához közeli gradiens esetén a háló szinte semmit sem fog tanulni. Ezt a problémát Vanishing
Gradient problémának nevezik.

A RELU (Rectified Linear Unit) aktivációs függvény ezt a problémát hivatott megoldani:
\begin{equation}
  \text{relu}(x) = max(0, x)
\end{equation}

#### ELU
Az ELU (Exponential Linear Unit) aktivációs függvény a RELU továbbfejlesztése. RELU esetén, mint ahogy a sigmoid függvénynél is láttuk,
a függvény átlagos értéke nincs közel a 0-hoz. Az ELU függvény segítségével, átlagosan nézve, a 0-hoz közelebbi értékeket kapunk.[@elu]
\begin{equation}
  \text{elu}(\alpha, x) =
  \begin{cases}
    \alpha(e^x -1) & \text{ha } x < 0 \\
    x & \text{ha } x \geqslant 0
  \end{cases}
\end{equation}
  
![Aktivációs függvények a [-10, +10] intervallumon ábrázolva.](src/images/activations.png)
  
### Súlyozott bemenet
A neuron súlyozott bemenete (weighted input) nem más, mint az (\ref{sigmoid-neuron}) egyenlet azon része, 
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
      a^l = \sigma(a^{l-1} \times W^l + b^l),
\end{equation}
ahol $a^{l-1} \in \mathbb{R}^m$, $W^l \in \mathbb{R}^{m \times n}$, $b^l \in \mathbb{R}^n$ és $a^l \in \mathbb{R}^n$

![Példa egy rejtett réteget tartalmazó neuronhálóra. Forrás:[@nn_and_deeplearning]](src/images/nn.png){width=75%}

### Neuronháló hiperparaméterei
Egy neuronhálónak számos hiperparaméterrel rendelkezik:

* Hány epoch-on keresztül tanítjuk a hálót
* Mekkora learning rate-et használunk
* Milyen hibafüggvényt használunk
* Hány réteg van a neuronhálóban
* Az egyes rétegek hány neuronból állnak
* Használunk-e regularizációt, és ha igen, akkor milyen mértékben
* Milyen aktivációs függvényeket használunk
* A kezdeti súlyokat hogyan inicializáljuk

### Regularizáció
A regularizáció a túlilleszkedés ellen nyújt hatékony megoldást. Alkalmazásával a hibafüggvény mellé további megkötéseket 
tehetünk a neuronhálóra, például büntethetjük a nagyon nagy súlyokat, mely segítségével a hálót a generalizálás irányába tereljük,
mintsem afelé, hogy a különálló bemenetek zajaira illeszkedjen. Egy súly csak akkor tud nagyra nőni, ha a regularizációs büntetés
ellenére is nagy mértékben javít a modell pontosságán.

#### L2 regularizáció
L2 regularizáció esetén a súlyok ($w \in \mathbb{R}$) négyzetét összegezzük. A bias-okat nem regularizáljuk.
\begin{equation}
      C_{reg} = C(y, \hat{y}) + \lambda \sum\limits_w w^2,
\end{equation}
ahol $\lambda \in \mathbb{R}, \lambda > 0$ a regularizációs paraméter.[@nn_and_deeplearning]

#### L1 regularizáció
L1 regularizáció esetén a súlyok ($w \in \mathbb{R}$) abszolútértékét összegezzük. A bias-okat nem regularizáljuk.
\begin{equation}
      C_{reg} = C(y, \hat{y}) + \lambda \sum\limits_w |w|,
\end{equation}
ahol $\lambda \in \mathbb{R}, \lambda > 0$ a regularizációs paraméter.[@nn_and_deeplearning]

#### Dropout
Dropout esetén nem a súlyokat regularizáljuk, hanem tanítás alatt magát a neuronhálót módosítjuk, pontosabban véve
azt, ahogyan az $\hat{y}$ kimenetet megkapjuk. A tanítás során, minden példa adat esetén véletlenszerűen "kikapcsoljuk"
a neuronháló rejtett rétegeiben lévő neuronok bizonyos részét. A 0.5 például tipikus dropout érték[@hinton_dropout], mely azt
jelenti, hogy csupán 50% eséllyel hagyjuk "aktívan" az adott neuront. A "kikapcsolt" neuronok aktivációját 0-nak tekintjük.

A dropout segítségével a neuronhálóból kikényszerítjük, hogy (0.5-ös esetben) fele annyi neuronnal rendelkezve, előbb az adathalmaz legrobosztusabb
tulajdonságait tanulja meg, azaz kikényszerítjük, hogy a generalizáljon. Másik oldalról nézve, a neuronok 
folyamatos ki-be kapcsolgatásával úgy is tekinthetjük, hogy nem egy, hanem több, különböző neuronokkal rendelkező hálót tanítunk be, 
melyek nagy eséllyel az adathalmaz más és más részhalmazaira fognak túlilleszkedni, így a neuronháló egészét nézve, a túlilleszkedés
kevésbé lesz számottevő.[@nn_and_deeplearning][@understanding_dropout]

![Neuronháló dropout regularizáció nélkül, illetve dropout regularizációval. Forrás:[@nn_and_deeplearning]](src/images/dropout.png){width=75%}

### Deep learning
A Deep Learning mögötti elgondolás az, hogy összetett koncepciókat egyszerűbb koncepciók tetszőleges hierarchiájával
is képesek vagyunk modellezni. Deep learningről tipikusan neurális hálók kapcsán beszélhetünk. Ilyenkor azt értjük alatta,
hogy több egyrétegű neuronhálót egymás mellé helyezünk, az egyik  réteg kimenete a következő réteg bemenete.
Több rétegnyi nemlinearitás segítségével erőteljesebb modellt kapunk, mintha egyetlen, ámbátor nagyságrendekkel több 
neuronból álló réteggel dolgoznánk.[@book_deeplearning]

### Fully connected réteg
Fully connected réteg alatt egy klasszikus neuronháló réteget értünk, melynél minden előző rétegbeli neuron össze van kötve
minden rákövetkező rétegbeli neuronnal.

### Konvolúciós neuronháló
Konvolúciós neuronhálókat főleg kép, illetve hangfeldolgozásnál használnak.
Egy konvolúciós háló tipikusan konvolúciós, pooling, végül pedig fully connected rétegekből épül fel.
 
#### Konvolúciós réteg
A konvolúciós réteg neuronjai, a megszokott, klasszikus neuronhálókéval ellentétben, egy 3 dimenziós térben helyezkednek el
egymáshoz képest, szélesség, magasság és mélység szerint. Ennek megfelelően a konvolúciós réteg bemenete is 3 dimenziós
kell legyen. Egy 800×600-as fekete-fehér, RGB és RGBA csatornákkal rendelkező bemeneti kép mérete rendre 800×600×1, 800×600×3, illetve
800×600×4.

Konvolúciós rétegnél egy, vagy több fix méretű kernelt csúsztatunk végig a bemeneten $s$ stride-dal (lépésközzel). A kernelt
szokás még filternek is nevezni. Egy konvolúciós kernel negyedrangú tenzor: kernel magasság × kernel szélesség 
× bemeneti csatornák száma × kimeneti csatornák száma.[@cs231n]

#### Konvolúció stride
A stride segítségével definiáljuk, hogy mekkora lépésközzel csúsztatjuk a kernelünket a bemeneten. $m$×$n$-es stride esetén
a kernelt $m$ egységgel léptetjük vertikálisan és $n$ egységgel horizontálisan.[@cs231n]

#### Konvolúció padding
2 dimenziós esetben, egy 10×10-es képen egy 2×2-es kernelt 2×2-es stride-dal végigléptetve, a kimenetünk mérete 
5×5-ös lesz, ezt "Valid padding"-nek nevezzük. Sokszor előnyös számunkra, ha az adat mérete nem változik a konvolúció során. 
Padding használata esetén a kimenetet annyi nullával rakjuk körbe, hogy visszakapjuk az eredeti méretet. 
Ezt "Same padding"-nak nevezzük [@cs231n]

#### Pooling réteg
A pooling rétegek használata gyakori konvolúciós hálókban. Segítségükkel a konvolúciós réteg aktivációjának méretét tudjuk csökkenteni.
A pooling réteg tipikusan egy 2×2-es filter, 2×2-es stride-dal.
Max pooling esetén a filter kimenete a 2×2-es terület maximuma, míg average pooling esetén a terület átlaga.
A pooling a csatornák számát nem csökkenti, csupán csatornánként a szélességet, magasságot.[@cs231n]

### Autoencoder
Az autoencoderek a neuronhálók egy speciális csoportját alkotják. Egy autoencoderrel az egységfüggvényt próbáljuk approximálni.
Ezt az önmagában triviális feladatot azzal a megszorítással végezzük, hogy az autoencoder belső, rejtett rétegeinek dimenziója 
kisebb kell legyen a bemenet dimenziójánál. Ezáltal a háló első fele egyfajta tömörítést, dimenzió csökkentést hajt
végre a bemeneti adaton, s a háló másik felének a feladata, hogy ebből a csökkentett méretű köztes reprezentációból
visszaállítsa az eredeti bemenetet. Az adat köztes reprezentációját szokás encoding-nak, illetve code-nak is nevezni.
Ezzel a tömörítéssel-visszaállítással a célunk, hogy az autoencoder egy szemantikailag értelmes 
reprezentációt tanuljon meg az adatról, amit a továbbiakban más célokra felhasználhatunk, például klaszterezésre.[@coursera_hinton_neural_networks] 

![Példa egy egyszerű autoencoder-re. Forrás:[@stanford_autoencoders]](src/images/autoencoder.png){height=50%}

### Gradient Descent
A Gradient Descent egy iteratív optimalizáló algoritmus, mely az optimalizálandó célfüggvénynek (egy potenciálisan lokális) minimumát
keresi meg a célfüggvény gradiensének segítségével. A step size, vagy learning rate, $\alpha \in \mathbb{R}^+$ 
a Gradient Descent egy paramétere, mely azt mondja meg, hogy minden egyes iterációban mekkora lépést tegyen az 
algoritmus a gradienssel ellentétes irányba.[@cs231n][@coursera_ng_machine_learning] Adott $\alpha$ learning rate és
$f$ differenciálható célfüggvény esetén az algoritmus $i$-k lépése a következőképp néz ki:
\begin{equation}
        x_{i+1} := x_i - \alpha * \nabla f,
\end{equation}
ahol $\nabla f$ fejlölje $f$ gradiensét.

### Backpropagation
A Backpropagation algoritmus segítségével a neuronháló súlyaihoz, bias-aihoz meg tudjuk feleltetni a megfelelő
parciális deriváltakat, ezáltal a Gradient Descent optimalizáló algoritmust neuronhálókra is tudjuk alkalmazni.
Eredetileg 1970-ben mutatták be, viszont igazán csak 1986-ban lett népszerű David Rumelhart, Geoffrey Hinton, és
Ronald Williams cikkje[@article_backprop] révén.

Az algoritmus ismertetése előtt két feltételezést kell tennünk a hibafüggvényről:

1. A hibafüggvény felírható kell legyen a különálló bemenetekhez tartozó hibafüggvények értékének az átlagaként. 
Erre azért van szükségünk, mert a backpropagation segítségével csupán a különálló $x$ bemenetekhez tartozó parciális 
deriváltakat ($\partial C_x / \partial w, \partial C_x / \partial b$) tudjuk kiszámolni. 
A $\partial C / \partial w$ és $\partial C / \partial b$ kiszámolásához átlagoljuk az egyes tanulóadatokhoz tartozó hibát:
\begin{equation}
          C= \frac{1}{n}\sum\limits_{x=1}^{n}C_x\text{, ahol $n$ a tanulóadatok száma.}
\end{equation}
2. A hibafüggvény csakis a neuronháló kimenetétől függ. Természetesen a hiba függ az elvárt $y$ kimenettől is, 
viszont mivel az $x$ bemenetet kötött paraméternek tekintjük, ezért az elvárt $y$ is az.

Egy neuronra tekinthetünk függvényként, egy neuronhálóra pedig összetett függvényként. A Backpropagation algoritmus,
a láncszabály alkalmazásával a hibafüggvény parciális deriváltjai határozza meg a súly/bias paraméterek szerint. 
A parciális deriváltak alapján pedig a súlyokat, bias-okat oly módon tudjuk módosítani, 
hogy adott bemenetre a hibafüggvény értéke csökkenjen.

Első lépésben definiáljuk a kimeneti, $L$-edik réteg $j$-edik neuronjához tartozó hibát:
\begin{equation}\label{BP1}
  \delta_j^L = \frac{\partial C}{\partial a_j^L} * \sigma '(z_j^L).
\end{equation}

Vektorizált formában, a kimeneti $L$-edik réteg hibája:
\begin{equation}\label{BP2}
  \delta^L = \nabla_a C \odot \sigma '(z^L),
\end{equation}
ahol $\odot$ jelölje két vektor Hadamard-szorzatát (elemenként vett szorzatát).

Második lépésben definiáljuk egy tetszőleges $l$-edik réteg hibáját a rákövetkező réteg hibájának függvényében:
\begin{equation}\label{BP2}
  \delta^l = ((w^{l+1})^T \delta^{l+1}) \odot \sigma '(z^L).
\end{equation}

(\ref{BP1}) és (\ref{BP2}) kombinálásával a neuronháló minden rétegének a hibáját ki tudjuk számítani.
Ezt követően definiálhatjuk a paraméterek szerinti parciális deriváltakat.

A hibafüggvény parciális deriváltja adott $l$ réteg $j$-edik neuronjának bias-a szerint:
\begin{equation}\label{BP3}
  \frac{\partial C}{\partial b_j^l} = \delta_j^l.
\end{equation}

A hibafüggvény parciális deriváltja adott $l$ réteg $j$-edik neuronjának súlyvektorának $k$-adik eleme szerint:
\begin{equation}\label{BP4}
  \frac{\partial C}{\partial w_{jk}^l} = a_k^{l-1}\delta_j^l.
\end{equation}

A (\ref{BP3}) és (\ref{BP4}) egyenletek birtokában a neuronháló bármely paramétere szerinti parciális deriváltat fel tudjuk
írni, ezáltal a Gradient Descent algoritmust tudjuk alkalmazni.[@nn_and_deeplearning]
