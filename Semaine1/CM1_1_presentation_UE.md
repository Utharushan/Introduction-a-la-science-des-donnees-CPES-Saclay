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
  scroll: true
  slideNumber: true
  start_slideshow_at: selected
  transition: none
  width: 90%
---

+++ {"editable": true, "slideshow": {"slide_type": "slide"}, "tags": []}

<center>

# Cours: Initiation à la Science des données

</center>

<center>Fanny Pouyet</center>

<center>L1 Informatique</center>

<center>Semestre 2 - 2024</center>


```{image} media/logoParisSaclay.png
:alt: logo Université
:class: bg-primary
:width: 150px
:align: center
```

+++ {"slideshow": {"slide_type": "slide"}}

<center>

## Présentation de l'UE ISD

</center>

### Sommaire

1. Les enseignantes et enseignants
2. Qu'est-ce que la science des données ?
3. Objectifs de l'UE
3. Liens utiles
4. Organisation, dates importantes et modalités d'évaluation

+++ {"slideshow": {"slide_type": "slide"}}

### Les enseignantes et enseignants

Responsable du cours:

* Fanny Pouyet, maitresse de conférences en bioinformatique

Chargées et chargés de TP:

* Sarah Antier, astronome à l'Observatoire de la Cote d'Azur
* Thomas Gerald, maitre de conférences en NLP
* Chiara Marmo, ingénieure de recherche en analyse de données 
* Solal Nathan, doctorant en apprentissage automatique 
* Clémence Sebe, doctorante en bioinformatique
* Nicolas Thiéry, professeur en combinatoire

+++ {"slideshow": {"slide_type": "slide"}}

### Les enseignantes et enseignants en CPES

Chargé de cours:

* Bryan Brancotte, ingénieur de recherche en informatique

Chargée et chargé de TP:

* Bryan Brancotte, ingénieur de recherche en informatique
* Clémence Sebe, doctorante en bioinformatique

+++ {"slideshow": {"slide_type": "slide"}}

### Qu'est-ce que la science des données

#### La science des données, une spécialité interdisciplinaire


Selon vous, qu'est-ce que la science des données ? https://app.wooclap.com/DBJNEA

+++ {"slideshow": {"slide_type": "slide"}}

#### Les expertises en science des données

La science des données correspond à la récupération, l'analyse et l'interprétation de données.
Les données doivent etre transformées et préparées (c'est ce qui prend le plus de temps).


```{image} media/dataScience.svg
:alt: logo Université
:class: bg-primary
:width: 500px
:align: center
```

+++ {"slideshow": {"slide_type": "slide"}}

#### Qu'est ce que sont «les données» ?
Les données sont diverses. Tout est "données". Généralement, elles prendront la forme d'une table avec en colonne des *attributs* et en ligne des *instances*.

**Exemple**: L'administration rend disponible de plus en plus de données comme la liste des prénoms donnés à Paris entre 2004 et aujourd'hui (disponible ici: [opendata](https://opendata.paris.fr/explore/dataset/liste_des_prenoms))

```{image} media/prenoms.png
:alt: tableau de prénoms
:class: bg-primary
:width: 500px
:align: center
```

- Comment obtenir et traiter ce genre de données? (voir ci-après)
- Une fois qu'on a cette table, que peut-on en dire ? (voir le 1er TP)

```{code-cell}
---
slideshow:
  slide_type: slide
---
#Obtention de la table en Python
## 1. Téléchargement de la liste des prénoms si ce n'est déjà fait

!if [ ! -f liste_des_prenoms.csv ]; then  \
    curl --http1.1 https://opendata.paris.fr/explore/dataset/liste_des_prenoms/download/\?format\=csv\&timezone\=Europe/Berlin\&lang\=fr\&use_labels_for_header\=true\&csv_separator\=%3B -o liste_des_prenoms.csv; \
fi

## 2. Importation des librairies: pandas pour manipuler des données
import pandas as pd

## 3. Chargement de la table en Python
prenoms = pd.read_csv('liste_des_prenoms.csv', sep=';')
prenoms.head(7)
```

+++ {"heading_collapsed": true, "slideshow": {"slide_type": "slide"}}

### Objectifs de l'UE

* *Compréhension*

On verra que la science des données est omni-présente dans nos
vies. On apprendra aussi à utiliser des outils d'apprentissage
statistique (*machine learning*).

* *Raisonnement* 

Être capable de lire une figure/une infographie dans les médias. Être capable de différencier: l'observation (qu'est ce que je vois?) et l'interprétation (qu'est ce que cela veut dire?). 

*  *Technicité* 

Faire de l'analyse de données **en Python** : l'analyse de tables et
la classification d'objets par apprentissage statistique

+++ {"slideshow": {"slide_type": "slide"}}

### Liens utiles

1. [Page web](http://nicolas.thiery.name/Enseignement/IntroScienceDonnees/):
   cours, sujets de TP, ...

2. [Espace e-Campus](https://ecampus.paris-saclay.fr/course/view.php?id=81000):
   - [Forum d'aide](https://ecampus.paris-saclay.fr/enrol/index.php?id=81000)
   - Salles de TP et horaires
   - Annales de QCM
   - Environnement Jupyter

3. Pb de code ? Quelqu'un a surement déjà eu le meme problème, n'hésitez pas a glaner des infos sur chatgpt, stackoverflow ou openclassrooms 

4. Si vous avez une question concernant les TP, utilisez **exclusivement** le forum d'aide

5. Mon mail: fanny.pouyet@universite-paris-saclay.fr

+++ {"slideshow": {"slide_type": "slide"}}

### Organisation de l'UE

- 9 semaines avec 1h à 1h30 de CM et 2h de TP + un oral (semaine du 29 avril - 3 mai)
- TP = apprentissage pratique + technicité (attention: on ne redéfinira pas les notions vues en CM!)
- CM = mise en contexte + présentation des notions

#### Modalités d'évaluation

- les rendus de TP (15% de la note finale)
- 1 TP en binome noté (15% de la note finale)
- 2 projets en binôme (15% + 25% de la note finale)
- 2 QCM (30% de la note finale) sur papier

Y a t il des questions ?

#### Infrastructure du cours

L'infrastructure est *presque identique* à celle du cours Introduction à la
Programmation Impérative:

- Salles de TP virtuelle: [MyDocker-VD](https://mydocker-vd.centralesupelec.fr/shell/join/RGNnWFxxFhTLVkMlqizu)
- Salles de TP en 336
- Forge logicielle [GitLab](https://gitlab.dsi.universite-paris-saclay.fr/)
- Gestion de devoirs avec l'outil [travo](https://gitlab.info.uqam.ca/travo/travo)

+++ {"slideshow": {"slide_type": "slide"}}

### Calendrier

* Semaine 1 : tutoriels et analyses de données
* Semaine 2 : TP analyse de données **en binôme**
* Semaine 3 : chaine complète en science des données 
* Semaine 4 et 5 : Projet 1 **en binôme** 
* *VACANCES de Février*
* Semaine 6 : Traitement des données
* Semaine 7 à 9 : Projet 2 **en binôme**
* Semaine 10 : Soutenances **en binôme**

+++ {"slideshow": {"slide_type": "slide"}}

### Rendus des TPs et Projets

**Avant le mardi 23h59** avec le tableau de bord (mis en place lors du TP1)
