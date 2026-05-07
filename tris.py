# --- FASE DI LOGIN ---
print("=== BENVENUTI A TRIS ===")
g1_nome = input("Inserisci il nome utente del Giocatore 1 (Userà le X): ")
g2_nome = input("Inserisci il nome utente del Giocatore 2 (Userà le O): ")
print(f"\nPerfetto! {g1_nome} vs {g2_nome}. Iniziamo!\n")

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

def gioca():
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
            break

        # Controllo Pareggio
        if turni == 9:
            stampa_scacchiera(scacchiera)
            print(" Pareggio! La scacchiera è piena.")
            break

        # Cambio Giocatore
        if giocatore_attuale == g1_nome:
            giocatore_attuale = g2_nome
            simbolo_attuale = "O"
        else:
            giocatore_attuale = g1_nome
            simbolo_attuale = "X"

# Avvio del gioco
gioca()
