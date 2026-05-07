# 🧩 Progetto Tris — Python + MySQL

Questo progetto implementa il gioco del **Tris (Tic‑Tac‑Toe)** in Python, con salvataggio delle partite e statistiche tramite **database MySQL**.

Il programma permette di:

- giocare una partita tra due utenti  
- salvare automaticamente i giocatori e i risultati nel database  
- visualizzare la **top 5** dei giocatori con più vittorie  
- mostrare le statistiche di un singolo giocatore  

---

## 🚀 Come avviare il progetto

Segui attentamente questi passaggi per far funzionare correttamente il gioco.

---

## 1️⃣ Esegui lo script SQL

Importa nel tuo database il file:

```
tris.sql
```

Questo creerà le tabelle:

- `players`
- `games`

---

## 2️⃣ Apri il tunnel SSH

Se stai usando il server della scuola, apri il tunnel SSH con:

```
ssh -N -L 3307:localhost:3306 [nome_utente_server]@lab.alberghetti.cloud
```

> Sostituisci **[nome_utente_server]** con il tuo username del server.

Il tunnel rimane attivo finché tieni aperto il terminale.

---

## 3️⃣ Modifica i parametri del database nel file Python

Apri il file Python principale e cerca questa sezione:

```python
DB_CONFIG = {
    "host": "0.0.0.0",        # GENERICO
    "user": "NOME_UTENTE_DATABASE",   # GENERICO
    "password": "PASSWORD_DATABASE",  # GENERICO
    "database": "NOME_DATABASE",      # GENERICO
    "port": 0000,                     # GENERICO
}
```

Sostituisci **tutti i valori segnati come GENERICO** con:

- host del database  
- nome utente  
- password  
- nome del database  
- porta (es. 3307 se usi il tunnel SSH)

---

## 4️⃣ Avvia il gioco

Esegui il file Python:

```
python3 main.py
```

Comparirà il menu:

- Giocare una partita  
- Vedere la top 5  
- Consultare le statistiche di un giocatore  

---

## 🎉 Divertiti!

Ora puoi giocare, salvare le partite e consultare le statistiche direttamente dal terminale.
