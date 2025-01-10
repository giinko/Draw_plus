# README - Draw++

## Introduction
Draw++ est un langage de programmation conçu pour créer des dessins et animations sur un écran. Ce projet permet de manipuler des curseurs, de dessiner des formes géométriques, de créer des animations, et d'utiliser des structures de contrôle comme des boucles ou des conditions.

Ce document a pour objectif d’expliquer comment utiliser Draw++ et son IDE, ainsi que de fournir une documentation détaillée pour maîtriser toutes les fonctionnalités du langage.

---

## Table des Matières
1. [Installation](#installation)
2. [Fonctionnalités principales](#fonctionnalités-principales)
3. [Guide d'utilisation](#guide-dutilisation)
4. [Syntaxe du langage](#syntaxe-du-langage)
    - Instructions élémentaires
    - Instructions avancées
5. [Fonctionnalités de l'IDE](#fonctionnalités-de-lide)
6. [FAQ](#faq)
7. [Contributeurs](#contributeurs)

---

## Installation
### Prérequis
- Python 3.8+
- SDL2 et SDL2_gfx (pour les fonctions de dessin en C)
- Bibliothèques Python : tkinter, re, subprocess

### Étapes d'installation
1. Clonez le dépôt Git :
    ```bash
    git clone https://github.com/nom_utilisateur/drawplusplus.git
    ```
2. Installez tkinter :
    ```bash
    pip install tk
    ```
3. Installez SDL2 sur votre système :
    - **Linux (Ubuntu/Debian)** :
      ```bash
      sudo apt-get install libsdl2-dev libsdl2-gfx-dev
      ```
    - **Windows** : Téléchargez SDL2 depuis [SDL.org](https://www.libsdl.org/) et ajoutez-le à votre PATH.
4. Lancez l'application :
    ```bash
    python UI.py
    ```

---

## Fonctionnalités principales
### 1. Dessins avec curseurs
- Créez des curseurs positionnés à des coordonnées spécifiques.
- Déplacez et tournez ces curseurs pour dessiner des formes.

### 2. Formes supportées
- Cercle
- Carré
- Rectangle
- Ligne
- Arc
- Point

### 3. Structures de contrôle
- Conditions : `if`, `else`
- Boucles : `for`, `while`

### 4. Génération de code intermédiaire
- Compilez le code Draw++ en C pour l'exécuter en SDL2.

### 5. IDE intégré
- Créez, modifiez, sauvegardez, exécutez et déboguez vos fichiers Draw++ dans une interface intuitive.

---

## Guide d'utilisation

### 1. Lancer l'IDE
1. Ouvrez l'application avec : `python UI.py`
2. Vous arrivez sur une interface divisée en trois parties :
    - **Explorateur de fichiers** : à gauche.
    - **Zone de code** : au centre.
    - **Canvas de dessin** : à droite.

### 2. Créer un fichier Draw++
1. Cliquez sur `Fichier > New File`.
2. Saisissez un nom et commencez à écrire votre code dans la zone de texte.

### 3. Exécuter un fichier
1. Écrivez le code Draw++ dans la zone de texte.
2. Cliquez sur le bouton **Lancer**.
3. Le résultat apparaît sur le canvas.

### 4. Compiler en C
1. Une fois votre code Draw++ prêt, cliquez sur `Fichier > Compile File`.
2. Un fichier `output.c` est généré dans le répertoire courant.

---

## Syntaxe du langage

### Instructions élémentaires
#### Créer un curseur
```
CREATE_CURSOR(name, x, y, color, thickness);
```
- **Exemple** :
    ```
    CREATE_CURSOR(c1, 0, 0, red, 2);
    ```

#### Déplacer un curseur
```
MOOV(cursor, distance);
```
- **Exemple** :
    ```
    MOOV(c1, 100);
    ```

#### Tourner un curseur
``` 
ROTATE(cursor, angle);
```
- **Exemple** :
    ```
    ROTATE(c1, 90);
    ```

#### Dessiner une forme
``` 
DRAW(cursor, shape, size[, additional_info]);
```
- **Formes supportées** : `circle`, `square`, `rectangle`, `line`, `arc`
- **Exemple** :
    ```
    DRAW(c1, circle, 50);
    DRAW(c1, rectangle, 50, 100);
    ```

### Instructions avancées
#### Conditions
``` 
if (condition) {
    // instructions
} else {
    // instructions
}
```
- **Exemple** :
    ```
    if (c1.x > 50) {
        ROTATE(c1, 90);
    } else {
        DRAW(c1, line, 30);
    }
    ```

#### Boucles
**While** :
``` 
while (condition) {
    // instructions
}
```
**For** :
``` 
for (var in range(start, end)) {
    // instructions
}
```
- **Exemple** :
    ```
    for (i in range(0, 10)) {
        DRAW(c1, circle, i * 10);
    }
    ```

---

## Fonctionnalités de l'IDE
### Menu "Fichier"
- **New File** : Crée un nouveau fichier Draw++.
- **Open Folder** : Ouvre un dossier pour naviguer dans les fichiers existants.
- **Save** : Sauvegarde le fichier en cours.
- **Compile File** : Génère un fichier C et un éxécutable à partir du code Draw++.

### Canvas
- **Zoom in/out** : Modifie la taille du dessin.
- **Animate** : Lance une animation pour visualiser les instructions pas à pas.
- **Sélection de dessin** : Sélectionnez des parties du dessin pour les manipuler (rotation, déplacement, etc.).

### Debugging
- Les erreurs sont affichées dans une zone dédiée.
- Les erreurs syntaxiques sont surlignées.

---

## FAQ
**Q : Pourquoi mon curseur ne s'affiche-t-il pas ?**
- Vérifiez que le curseur a bien été créé avec `CREATE_CURSOR`.

**Q : Comment corriger les erreurs de compilation ?**
- Les erreurs sont surlignées en rouge dans l'IDE avec des messages explicatifs.

**Q : Peut-on dessiner plusieurs formes avec un seul curseur ?**
- Oui, utilisez plusieurs commandes `DRAW` avec le même curseur.

---

## Contributeurs
- **Balit Ilian**
- **Clément Maxime**
- **Sait Nahel**
- **Zerrouki Abbes**



