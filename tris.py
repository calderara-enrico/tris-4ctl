import pymysql

# --- CONFIGURAZIONE DATABASE ---
DB_CONFIG = {
    "host": "0.0.0.0",
    "user": "NOME_UTENTE",
    "password": "PASSWORD",
    "database": "NOME_DATABASE",
    "port": 5000,
    "cursorclass": pymysql.cursors.Cursor,
    "connect_timeout": 5,
}

def get_connection():
    return pymysql.connect(**DB_CONFIG)

# --- FUNZIONI SQL ---
def get_or_create_player(conn, name):
    with conn.cursor() as cursor:
        cursor.execute("SELECT id FROM players WHERE name = %s", (name,))
        row = cursor.fetchone()
        if row:
            return row[0]

        cursor.execute("INSERT INTO players (name) VALUES (%s)", (name,))
        conn.commit()
        return cursor.lastrowid

def save_game(conn, player_x_id, player_o_id, winner_id):
    with conn.cursor() as cursor:
        cursor.execute(
            "INSERT INTO games (player_x_id, player_o_id, winner_id) VALUES (%s, %s, %s)",
            (player_x_id, player_o_id, winner_id)
        )
    conn.commit()

def get_top5_full_stats(conn):
    with conn.cursor() as cursor:
        cursor.execute("""
            SELECT 
                p.id,
                p.name,
                (SELECT COUNT(*) FROM games WHERE winner_id = p.id) AS vinte,
                (SELECT COUNT(*) FROM games WHERE player_x_id = p.id OR player_o_id = p.id) AS giocate
            FROM players p
            ORDER BY vinte DESC
            LIMIT 5;
        """)
        rows = cursor.fetchall()

        top5 = []
        for pid, nome, vinte, giocate in rows:
            winrate = (vinte / giocate * 100) if giocate > 0 else 0
            top5.append((nome, vinte, giocate, winrate))

        return top5

def get_player_stats(conn, player_id):
    with conn.cursor() as cursor:
        cursor.execute("""
            SELECT 
                (SELECT COUNT(*) FROM games WHERE player_x_id = %s OR player_o_id = %s),
                (SELECT COUNT(*) FROM games WHERE winner_id = %s),
                (SELECT COUNT(*) FROM games 
                 WHERE (player_x_id = %s OR player_o_id = %s) 
                 AND winner_id <> %s AND winner_id <> -1)
        """, (player_id, player_id, player_id, player_id, player_id, player_id))

        giocate, vinte, perse = cursor.fetchone()
        winrate = (vinte / giocate * 100) if giocate > 0 else 0
        return giocate, vinte, perse, winrate

# --- FUNZIONI DI INTERFACCIA ---
def stampa_top5(conn):
    print("\n=== TOP 5 GIOCATORI ===")
    top = get_top5_full_stats(conn)

    print(f"\n{'Giocatore':<20} {'Vittorie':<10} {'Giocate':<10} {'Winrate (%)':<12}")
    print("-" * 55)

    for nome, vinte, giocate, winrate in top:
        print(f"{nome:<20} {vinte:<10} {giocate:<10} {winrate:>10.2f}")

def stampa_scacchiera(scacchiera):
    print(f"\n {scacchiera[0]} | {scacchiera[1]} | {scacchiera[2]} ")
    print("-----------")
    print(f" {scacchiera[3]} | {scacchiera[4]} | {scacchiera[5]} ")
    print("-----------")
    print(f" {scacchiera[6]} | {scacchiera[7]} | {scacchiera[8]} \n")

def fai_mossa(scacchiera, posizione, simbolo):
    if scacchiera[posizione] != "_":
        print(" ATTENZIONE: Posizione già occupata! Scegline un'altra.")
        return False
    else:
        scacchiera[posizione] = simbolo
        return True

def ha_vinto(scacchiera, simbolo):
    combinazioni_vincenti = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Orizzontali
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Verticali
        [0, 4, 8], [2, 4, 6]              # Diagonali
    ]
    for c in combinazioni_vincenti:
        if scacchiera[c[0]] == scacchiera[c[1]] == scacchiera[c[2]] == simbolo:
            return True
    return False

# --- LOGICA DI GIOCO ---
def gioca():
    conn = get_connection()
    
    print("=== BENVENUTI A TRIS ===")
    g1_nome = input("Inserisci il nome utente del Giocatore 1 (Userà le X): ")
    g2_nome = input("Inserisci il nome utente del Giocatore 2 (Userà le O): ")
    print(f"\nPerfetto! {g1_nome} vs {g2_nome}. Iniziamo!\n")

    g1_id = get_or_create_player(conn, g1_nome)
    g2_id = get_or_create_player(conn, g2_nome)

    scacchiera = ["_"] * 9
    giocatore_attuale = g1_nome
    simbolo_attuale = "X"
    turni = 0

    while True:
        stampa_scacchiera(scacchiera)

        mossa_completata = False
        while not mossa_completata:
            try:
                scelta = input(f"Turno di {giocatore_attuale} ({simbolo_attuale}). Inserisci posizione (1-9): ")
                pos = int(scelta) - 1

                if 0 <= pos <= 8:
                    if fai_mossa(scacchiera, pos, simbolo_attuale):
                        mossa_completata = True
                        turni += 1
                else:
                    print(" Errore: il numero deve essere tra 1 e 9.")
            except ValueError:
                print(" Errore: Inserisci solo numeri interi.")

        # Controllo Vittoria
        if ha_vinto(scacchiera, simbolo_attuale):
            stampa_scacchiera(scacchiera)
            print("="*40)
            print(f" VITTORIA! {giocatore_attuale}, hai vinto!")
            print("="*40)
            
            winner_id = g1_id if simbolo_attuale == "X" else g2_id
            save_game(conn, g1_id, g2_id, winner_id)
            break

        if turni == 9:
            stampa_scacchiera(scacchiera)
            print(" Pareggio! La scacchiera è piena.")
            print(" Il pareggio vale come doppia sconfitta!")
            save_game(conn, g1_id, g2_id, -1)
            break

        # Cambio Giocatore
        if giocatore_attuale == g1_nome:
            giocatore_attuale = g2_nome
            simbolo_attuale = "O"
        else:
            giocatore_attuale = g1_nome
            simbolo_attuale = "X"

    stampa_top5(conn)
    conn.close()

if __name__ == "__main__":
    gioca()
