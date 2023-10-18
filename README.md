# OgameBot


## Google API

### Compte de service
- Pour utiliser les API Google, il faut créer un compte de service.
- Pour cela, rendez-vous sur [cette page](https://console.cloud.google.com/iam-admin/serviceaccounts) et sélectionnez le projet que vous voulez utiliser, ou créez-en un nouveau.
- Puis cliquez sur `Créer des identifiants` puis `Compte de service`.
- Vous pouvez ensuite choisir le nom du compte de service.
- Cliquez ensuite sur `Créer et continuer`.
- Sur la page suivante, vous pouvez choisir les rôles du compte de service.
- Pour ce projet, il faut choisir `Projet` puis `Propriétaire`, `Editeur` et `Lecteur`.
- Cliquez ensuite sur `Continuer`.


### credentials.json
- Pour obtenir une clé, qui sera sous un fichier .json, rendez-vous dans l'interface du compte de service que vous voudrez utiliser.
- Allez ensuite dans `Clés` dans la barre supérieure, puis `Ajouter une clé` et enfin `Créer une clé`.
- Vous choisirez ensuite `JSON` comme type de clé, et vous obtiendrez un fichier .json.
- Placer ensuite ce fichier dans le dossier `bot_config` qui se trouve dans la racine du projet, puis renommez-le en `credentials.json`.


### Google Sheet
- Pour utiliser les API Google Sheet, il faudra préalablement créer un fichier Google Sheet.
- Pour cela, rendez-vous sur [cette page](https://docs.google.com/spreadsheets/u/0/) et cliquez sur `Nouveau` puis `Google Sheets`.
- Vous pouvez ensuite choisir le nom du fichier.
- Récupérer l'adresse mail du compte de service que vous avez créé précédemment, dans l'interface du compte de service.
- Allez ensuite dans le fichier Google Sheet que vous avez créé, et cliquez sur `Partager` en haut à droite.
- Collez l'adresse mail du compte de service dans la barre de recherche, et sélectionnez les droits appropriés.
- Vous pouvez ensuite récupérer l'ID du fichier Google Sheet dans l'URL du fichier. Il s'agit de la suite de caractères après `/d/` et avant `/edit`.
- Vous pouvez ensuite placer l'ID du fichier dans le fichier `bot_config/sheet.json`.

