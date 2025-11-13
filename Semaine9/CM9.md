---
jupytext:
  notebook_metadata_filter: rise
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
kernelspec:
  display_name: Python 3 (ipykernel)
  language: python
  name: python3
rise:
  auto_select: first
  autolaunch: false
  centered: false
  controls: false
  enable_chalkboard: true
  height: 100%
  margin: 0
  maxScale: 1
  minScale: 1
  overlay: "<div style='position: absolute; top: 0; left: 0'>Introduction \xE0 la\
    \ Science des Donn\xE9es, L1 Math-Info, Facult\xE9 des Sciences d'Orsay</div><div\
    \ style='position: absolute; top: 0; right: 0'><img src='media/logoParisSaclay.png'\
    \ width='150'></div>"
  scroll: true
  slideNumber: true
  start_slideshow_at: selected
  transition: none
  width: 90%
---

+++ {"editable": true, "slideshow": {"slide_type": "slide"}, "tags": []}

<center>

# Cours 9: Impact de la science des données et du numérique sur notre société

</center>

<br>

<center>Fanny Pouyet</center>

<center>L1 Informatique</center>

<center>Janvier - Avril 2024</center>

+++ {"editable": true, "slideshow": {"slide_type": "slide"}, "tags": []}

**Précédemment**

* Inititation à la science des données
* Initiation à l'apprentissage statistique
* Classification d'images

**Cette semaine**

* Science et société: l'impact de la science des données et du numérique sur notre société (sources: shift project, ADEME et gouvernement)

+++ {"editable": true, "slideshow": {"slide_type": "slide"}, "tags": []}

Numérique : réseaux de communications + terminaux + data centers 

**Comment maximiser l'impact positif du numérique et de la science des données en minimisant son impact négatif ?**


**Une question en apparence inutile mais aussi insoluble**

+++ {"editable": true, "slideshow": {"slide_type": "slide"}, "tags": []}

## Contexte : le numérique dans notre société

* Les énergies fossiles représentent 80% de la consommation d'énergie mondiale
* Elles sont responsables d'une grande partie des émissions de gaz à effet de serre.
* Ces émissions impactent notre climat et nos sociétés.
* Le numérique consomme de l'énergie mais permet aussi d'en réduire la consommation en permettant une certaine optimisation

+++ {"editable": true, "slideshow": {"slide_type": "slide"}, "tags": []}

### Impacts positifs


#### Le numérique pour limiter la consommation d'énergie

* utilisation plus efficace des ressources
* diminution des pertes (capteurs d'humidité,..)

Repose sur de l'analyse des données !

+++ {"editable": true, "slideshow": {"slide_type": "slide"}, "tags": []}

#### Développement économique et social
* augmentation de la productivité des entreprises, 
* création d'emplois, 
* commerce mondialisé

+++ {"editable": true, "slideshow": {"slide_type": "slide"}, "tags": []}

#### Science ouverte et utilisation critique des données publiques 

```{figure} https://www.oecd-ilibrary.org/sites/3a6a5d87-fr/images/images/3DPSS_FR/media/image2.png
---
alt: Données publiques (https://doi.org/10.1787/09ab162c-en.)
width: 1100px
align: center
---

```

+++ {"editable": true, "slideshow": {"slide_type": "slide"}, "tags": []}

Prenons l'exemple des données publiques de [data.gouv.fr](data.gouv.fr), site développé depuis une dizaine d'années:

**Ouverture des données**: le partage des données dont disposent les institutions (généralement, publiques, depuis la loi Cada 1978) implique:
* la gratuité, 
* des formats facilement traitables,
* et réutilisables.

+++ {"editable": true, "slideshow": {"slide_type": "slide"}, "tags": []}

**3 objectifs** :

1. améliorer le fonctionnement démocratique (transparence, concertation);
 
2. améliorer l'efficacité de l'action publique;
 
3. intégration des données dans de nouveaux services à forte valeur ajoutée économique ou sociale.

+++ {"editable": true, "slideshow": {"slide_type": "slide"}, "tags": []}

**Avantages** :

* simplification des systèmes d'informations par la création de nouvelles bases de données;
* accès facilité par internet aux documents administratifs.
* informations publiques réutilisables à d’autres fins que la mission de service public pour laquelle elles ont été produites ou reçues.

+++ {"editable": true, "slideshow": {"slide_type": "slide"}, "tags": []}

### Impacts négatifs

**Effet direct** Les TIC (technologies de l'information et de la communication) consomme de l'éléctricité...


```{figure} media/ICT.png
---
alt: 3 catégories de TIC (data center, devices, antennes)
width: 500px
align: center
---

```

+++ {"editable": true, "slideshow": {"slide_type": "slide"}, "tags": []}

**Effets indirects**
* Augmentation de l'utilisation des ressources informatiques par sa facilitation (smartphones vs. Nokia 3310)
* Le cycle de vie du produit pollue (fabrication, transport, utilisation (effet direct), absence de recylage) --> exemple de la production de matériel informatique (métaux rares, pollution loin de la France). Remarque: cours de Ligozat et Frenoux (master HCI) sur l'estimation du cout carbone du cycle de vie des outils informatiques

```{figure} media/incidences_geostrategiques.png
---
alt: media/incidences_geostrategiques.png
width: 1000px
align: center
---
```

+++ {"editable": true, "slideshow": {"slide_type": "slide"}, "tags": []}

## Consommation énergétique

* Etude de 2018 (projection à partir de cette date): 4 scénarios
* Consommation électrique en 2017 : 21000 TWh (augmentation d'1,5%/an)
* Consommation actuelle en Europe du coût energétique: [Electricity Map](https://app.electricitymaps.com/map)

```{figure} media/DEC.png
---
alt: media/DEC.png
width: 1000px
align: center
---
```

+++ {"editable": true, "slideshow": {"slide_type": "slide"}, "tags": []}

## Postes de consommation

10% de la consommation éléctrique en France vient des services numériques. Les objets individuels (ordinateurs, téléphones portables écrans etc.) sont ce qui consomme le plus à l'échelle du Pays (~70%)

```{figure} https://infos.ademe.fr/wp-content/uploads/2022/04/154-faits-et-chiffres-1.jpg
---
alt: Ademe (consommation services umériques)
width: 1000px
align: center
---
```

+++ {"editable": true, "slideshow": {"slide_type": "slide"}, "tags": []}

## Nombre de postes numériques par personne

```{figure} media/nb_equipement.png
---
alt: media/nb_equipement.png
width: 800px
align: center
---
```

+++ {"editable": true, "slideshow": {"slide_type": "slide"}, "tags": []}

## Empreinte carbone des calculs numériques

L'ADEME (Agence de l'Environnement et de la Maîtrise de l'Energie, **créée en 1991**) propose des moyens de calculer l'empreinte carbone de nos usages numériques (vie professionnelle ou personnelle)

```{figure} media/usage-numérique-pouyet.png
---
alt: Simulateur empreinte carbone du numérique
width: 500px
align: center
---
```

Pour calculer votre empreinte, utilisez le [simulateur Impact CO2 développé par l'ADEME](https://impactco2.fr/usagenumerique)

+++ {"editable": true, "slideshow": {"slide_type": "slide"}, "tags": []}

* **Empreinte carbone**: équivalent C02 qui prend en compte les différents gaz responsables du changement climatique.


* Prend en compte chaque étape du cycle de vie des équipements en incluant la fabrication, le transport, l'utilisation et la fin de vie.
* Bien que le calcul soit critiqué, il donne un *ordre de grandeur* tout à fait pertinent.

+++ {"editable": true, "slideshow": {"slide_type": "slide"}, "tags": []}

### Dans le secteur privé 

**Exemple d'estimation moyenne de l'empreinte carbone de l'accès à internet (au 01/01/2022):**

* Réseaux mobiles : 50 gCO2e/Go
* Réseaux fixes : 3,95 kgCO2e/mois/abonné. 
* L’utilisation des réseaux fixes est à privilégier dès que possible.

+++ {"editable": true, "slideshow": {"slide_type": "slide"}, "tags": []}

### Dans le monde de la recherche
* Estimer la consommation énergétique d'un entrainement d'un réseau de neurones n'est pas chose facile.
* Recherche active récente : exemple de calcul de vos émissions, [ML CO2 Impact](https://mlco2.github.io/impact/#home)

* Les émissions dépendent des **infrastructures** et de votre **code**.

+++ {"editable": true, "slideshow": {"slide_type": "slide"}, "tags": []}

- Une thèse en apprentissage statistique émet plusieurs tonnes de CO2. 
- Prenons l'exemple d'une thèse 2018-2022, qui a émis 2,9 tonnes de CO2 (source : doctorant du LISN)

```{figure} media/These_2p9TCO2.png
---
alt: media/These_2p9TCO2.png
width: 700px
align: center
---
```

+++ {"editable": true, "slideshow": {"slide_type": "slide"}, "tags": []}

**Ordre de grandeur et objectif des émissions en France**
```{figure} media/ordre_grandeur_CO2.png
---
alt: media/ordre_grandeur_CO2.png
width: 700px
align: center
---
```

+++ {"editable": true, "slideshow": {"slide_type": "slide"}, "tags": []}

## Impact du Deep learning sur notre consommation de ressources

### La consommation d'un ordinateur se répartit *grosso modo* comme suit:

```{figure} media/conso_ordi_perso.png
---
alt: media/conso_ordi_perso.png
width: 700px
align: center
---
```

+++ {"editable": true, "slideshow": {"slide_type": "slide"}, "tags": []}

### Les clusters de calculs sont utilisés quotidiennement
```{figure} media/nb_NN.png
---
alt: media/nb_NN.png
width: 700px
align: center
---
```

Le nombre de modèles développés augmente rapidement.
La nature du code joue un rôle important:

Par exemple, si on entraine un modèle d'apprentissage de langues la consommation varie d'un facteur 4 entre 
une utilisation GPU et CPU (Gay et Ligozat, séminaire 2023):

- GPU : 47KWh pour 150 heures
- CPU : 188KWh pour 6000 heures

+++ {"editable": true, "slideshow": {"slide_type": "slide"}, "tags": []}

Autre exemple :consommation en joule pour reconnaitre une image, ce qui revient à faire 50km de voitures pour reconnaitre $10^{12}$ images:
```{figure} media/GPU_joule_consumption.png
---
alt: media/GPU_joule_consumption.png
width: 400px
align: center
---
```

D'après Gay et Ligozat (séminaire 2023 de DataIA)

+++ {"editable": true, "slideshow": {"slide_type": "slide"}, "tags": []}

On cherche à maximiser la précision des modèles, mais n'oubliez pas que cela a un coût énergétique.

```{figure} media/cout_apprentissage.png
---
alt: media/cout_apprentissage.png
width: 700px
align: center
---
```

De plus de nombreux Joules sont perdus à cause d'erreurs professionnelles (Khan, 2019):

- Job crashing (erreurs de code)
- Optimisation lourde pour ne gagner que quelques % de précisions
- mauvaise utilisation des GPU

+++ {"editable": true, "slideshow": {"slide_type": "slide"}, "tags": []}

## Pour la fin de ce cours

**Projet n°2**

Soutenance entre le 03 et le 05 avril pour les IM et MI.

Vérifiez vos binômes et horaire de passage : https://codimd.math.cnrs.fr/m4cSohttSLyrAPl5Qoe5NQ

Organisation: 6 à 7 min de présentaiton en binome, suivi de quelques minutes de questions (1 question de cours et 1 sur la présentation par personne).

+++ {"editable": true, "slideshow": {"slide_type": "slide"}, "tags": []}

## Et pour la suite ? 

**L2 : Introduction à la science des données**
* Cours assuré par Yue Ma (MCU, LISN)
* Apprentissage supervisé (classification + régression)
* Apprentissage non supervisé
* Evaluations (cross-validation par exemple)
* Analyses statistiques (un peu plus de mathématiques même si ca restera léger)
* TP = utilisation de `sklearn`.
* Apprentissage par problème

**L3: Introduction à l'apprentissage statistique**
* Cours assuré par Francois Landes (MCU, LISN)
* Algorithme du gradient, du perceptron
* Les bases mathématiques de l'ACP, descente de gradient
* TD mais aussi TP  avec utilisation de `sklearn`.

**L3: Projet Optionnel de Bioinfo**
* Projet assuré par Fanny Pouyet (MCU, LISN)
* Science des données appliquée à une problématique liée au changement climatique
* Repose sur les données du GIEC

**M1: HCI Human Computer Interaction: Computer Science and Ecology**
* Cours assuré par Emmanuelle Frenoux et Anne-Laure Ligozat
* Estimation du cycle de vie d'objets numériques
* Analyse d'articles scientifiques

+++ {"editable": true, "slideshow": {"slide_type": "slide"}, "tags": []}

## Conclusions

* Cours d'initiation:
    * Observation n'est pas interprétation (l'observation est toujours possible! normalement elle ne devrait pas poser de problème)
    * identifier la question *précise* à laquelle on souhaite répondre c'est déjà une large partie du travail en science des données
    * Notions d'apprentissage statistiques, classificateurs, langage python
    * Recul sur l'importance du numérique et des données dans notre société

+++ {"editable": true, "slideshow": {"slide_type": "slide"}, "tags": []}

* Vous avez récupéré des images, les avez prétraitées, analysées leur composition et vous avez produit un classificateur en python. Auriez-vous pensé faire ca dès la L1 ? Bravo !

+++ {"editable": true, "slideshow": {"slide_type": "slide"}, "tags": []}

Maintenant: **QCM2**

Rangez vos affaires, ne gardez qu'un stylo, vos carte d'étudiant et du typex.

```{code-cell} ipython3
---
editable: true
slideshow:
  slide_type: ''
tags: []
---

```
