# Mini-Marché 3D

Application Android du jeu **Mini-Marché 3D**, créée avec Capacitor.

## Construire et télécharger l’APK

1. Ouvrir l’onglet **Actions** du dépôt.
2. Si GitHub affiche un bouton pour autoriser les workflows, l’activer.
3. Ouvrir **Construire APK Android**.
4. Appuyer sur **Run workflow**, choisir la branche `main`, puis confirmer.
5. Quand la compilation devient verte, ouvrir son résultat.
6. Dans **Artifacts**, télécharger **Mini-Marche-3D-APK**.
7. Décompresser le ZIP, puis installer `Mini-Marche-3D.apk` sur Android.

## Fonctionnement

Le jeu HTML est conservé sous forme compactée dans `source/template-parts/`. Le workflow le restaure, réintègre les modèles 3D Kenney, ajoute le conteneur Android Capacitor, puis produit automatiquement un APK installable.

## Identité Android

- Nom : `Mini-Marché 3D`
- Package : `com.tikowikofamily.minimarche`
