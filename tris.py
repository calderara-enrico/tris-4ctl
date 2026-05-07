import pymysql

# CONFIGURAZIONE DATABASE
DB_CONFIG = {
    "host": "0.0.0.0",                 # GENERICO
    "user": "NOME_UTENTE_DATABASE",    # GENERICO
    "password": "PASSWORD_DATABASE",   # GENERICO
    "database": "NOME_DATABASE",       # GENERICO
    "port": 0000,                      # GENERICO
    "cursorclass": pymysql.cursors.Cursor,
    "connect_timeout": 5,
}

def get_connection():
    return pymysql.connect(**DB_CONFIG)


# IMPORT DAL MODULO DB
from db import (
    get_or_create_player,
    save_game,
    get_top_players,
    get_player_stats
)


# FUNZIONI DI GIOCO
def stampa_scacchiera(s):
    print(f"\n {s[0]} | {s[1]} | {s[2]} ")
    print("-----------")
    print(f" {s[3]} | {s[4]} | {s[5]} ")
    print("-----------")
    print(f" {s[6]} | {s[7]} | {s[8]} \n")

def fai_mossa(s, pos, simbolo):
    if s[pos] != "_":
        print("Posizione occupata!")
        return False
    s[pos] = simbolo
    return True

def ha_vinto(s, simbolo):
    combinazioni = [
        [0,1,2],[3,4,5],[6,7,8],
        [0,3,6],[1,4,7],[2,5,8],
        [0,4,8],[2,4,6]
    ]
    return any(s[a] == s[b] == s[c] == simbolo for a,b,c in combinazioni)


# LOGICA PRINCIPALE DI GIOCO
def gioca(conn):
    print("=== BENVENUTI A TRIS ===")
    g1_nome = input("Nome Giocatore 1 (X): ")
    g2_nome = input("Nome Giocatore 2 (O): ")

    g1_id = get_or_create_player(conn, g1_nome)
    g2_id = get_or_create_player(conn, g2_nome)

    scacchiera = ["_"] * 9
    giocatore = g1_nome
    simbolo = "X"
    turni = 0

    while True:
        stampa_scacchiera(scacchiera)

        try:
            pos = int(input(f"{giocatore} ({simbolo}) scegli posizione (1-9): ")) - 1
            if pos < 0 or pos > 8:
                print("Numero non valido.")
                continue
        except:
            print("Inserisci un numero!")
            continue

        if not fai_mossa(scacchiera, pos, simbolo):
            continue

        turni += 1

        if ha_vinto(scacchiera, simbolo):
            stampa_scacchiera(scacchiera)
            print(f"VITTORIA di {giocatore}!")

            winner_id = g1_id if simbolo == "X" else g2_id
            save_game(conn, g1_id, g2_id, winner_id)
            break

        if turni == 9:
            stampa_scacchiera(scacchiera)
            print("Pareggio!")
            save_game(conn, g1_id, g2_id, None)
            break

        giocatore = g2_nome if giocatore == g1_nome else g1_nome
        simbolo = "O" if simbolo == "X" else "X"


# MENU PRINCIPALE
def main():
    conn = get_connection()

    while True:
        print("\n=== MENU ===")
        print("1) Gioca una partita")
        print("2) Top 5 giocatori")
        print("3) Statistiche giocatore")
        print("4) Esci")

        scelta = input("> ")

        if scelta == "1":
            gioca(conn)

        elif scelta == "2":
            top = get_top_players(conn)
            print("\n--- TOP 5 ---")
            for nome, vittorie in top:
                print(f"{nome}: {vittorie} vittorie")

        elif scelta == "3":
            nome = input("Inserisci nome giocatore: ")
            with conn.cursor() as cursor:
                cursor.execute("SELECT id FROM players WHERE name = %s", (nome,))
                row = cursor.fetchone()

            if not row:
                print("Giocatore non trovato.")
                continue

            pid = row[0]
            giocate, vinte, perse, winrate = get_player_stats(conn, pid)

            print(f"\nStatistiche di {nome}:")
            print(f"Partite giocate: {giocate}")
            print(f"Vinte: {vinte}")
            print(f"Perse: {perse}")
            print(f"Win rate: {winrate:.2f}%")

        elif scelta == "4":
            print("Arrivederci!")
            break

        else:
            print("Scelta non valida.")

    conn.close()


if __name__ == "__main__":
    main()
