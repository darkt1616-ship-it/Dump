"""
BREACH DATASET GENERATOR
Per Ricerca Accademica sulla Cybersecurity
"""

import os
import time
from pathlib import Path
from multiprocessing import cpu_count
from concurrent.futures import ProcessPoolExecutor
from tqdm import tqdm

# Configurazione (i valori runtime vengono letti dentro genera_dataset)
NUM_PROCESSI = max(1, cpu_count() - 1)

# Database nomi e cognomi (ISTAT)
NOMI = [
    "marco", "giuseppe", "antonio", "giovanni", "francesco", "andrea",
    "luca", "alessandro", "roberto", "paolo", "luigi", "mario",
    "anna", "maria", "giulia", "laura", "francesca", "elena",
    "silvia", "alessandra", "claudia", "roberta", "paola", "carla",
    "matteo", "lorenzo", "davide", "enrico", "salvatore", "vincenzo",
    "simone", "stefano", "riccardo", "gabriele", "federico", "giacomo"
]

COGNOMI = [
    "rossi", "bianchi", "verdi", "russo", "ferrari", "esposito",
    "romano", "colombo", "ricci", "marino", "greco", "bruno",
    "gallo", "conti", "moretti", "mancini", "costa", "giordano",
    "lombardi", "barbieri", "fontana", "santoro", "manca", "piras",
    "marchetti", "gentile", "serra", "cattaneo", "bartolini", "bianco"
]

# Domini email con distribuzione realistica
DOMINI = {
    'gmail.com': 30,
    'yahoo.com': 15,
    'hotmail.com': 10,
    'outlook.com': 8,
    'alice.it': 10,
    'libero.it': 8,
    'virgilio.it': 5,
    'tiscali.it': 4,
    'icloud.com': 5,
    'protonmail.com': 3,
    'aol.com': 2
}

# Pattern email realistici
PATTERNS_EMAIL = [
    "{nome}.{cognome}@{dominio}",
    "{nome}{cognome}@{dominio}",
    "{nome}_{cognome}@{dominio}",
    "{nome}{cognome}{anno}@{dominio}",
    "{nome}.{cognome}{anno}@{dominio}",
    "{nome}{cognome}_{numero}@{dominio}",
    "{nome}{numero}@{dominio}",
    "{nome}{cognome}{numero}@{dominio}"
]

# ---------------------------------------------------------------------------
# Wordlist italiane per password realistiche.
# Basi ricorrenti nei breach di utenti italiani: parole comuni, squadre di
# calcio, termini affettivi e sequenze da tastiera. Solo caratteri ASCII.
# ---------------------------------------------------------------------------
PAROLE_COMUNI = [
    "password", "passwordit", "ciao", "ciaociao", "amore", "amoremio",
    "tiamo", "tesoro", "cuore", "principessa", "bellezza", "stella",
    "sole", "mare", "estate", "primavera", "vacanza", "montagna",
    "casa", "famiglia", "liberta", "felicita", "segreto", "italia",
    "vespa", "ferrari", "campione", "calcio", "pizza", "gelato",
    "gatto", "gattino", "cane", "pippo", "pluto", "topolino",
]

# Squadre di calcio: tra le basi piu' frequenti nelle password italiane
SQUADRE = [
    "juventus", "juve", "forzajuve", "milan", "acmilan", "inter",
    "napoli", "forzanapoli", "roma", "asroma", "lazio", "fiorentina",
    "torino", "atalanta", "bologna", "genoa", "sampdoria", "palermo",
]

# Sequenze da tastiera / numeriche molto diffuse
SEQUENZE = [
    "123456", "1234567", "12345678", "123456789", "12345",
    "qwerty", "qwertyuiop", "asdasd", "abc123", "111111",
    "000000", "123123", "654321",
]

SIMBOLI = ['!', '@', '#', '$', '%', '&', '*', '?', '+']

# Strategie di generazione password con probabilita' (somma = 100).
# "personale" deriva dai dati della mail (nome/cognome/anno): la password e'
# quindi COERENTE con l'indirizzo email della stessa riga.
STRATEGIE_PASSWORD = [
    ("personale", 42),
    ("parola", 30),
    ("squadra", 13),
    ("sequenza", 10),
    ("comune_pura", 5),
]

# Password "personali" (coerenti con la mail)
PATTERNS_PERSONALI = [
    "{nome}{anno}",
    "{Nome}{anno}",
    "{nome}{anno2}",
    "{Nome}{anno2}",
    "{cognome}{anno}",
    "{Cognome}{anno}",
    "{nome}{cognome}",
    "{Nome}{Cognome}",
    "{nome}{numero}",
    "{Nome}{anno}{simbolo}",
    "{nome}{simbolo}{anno}",
    "{cognome}{anno2}{simbolo}",
]

# Password basate su una parola comune
PATTERNS_PAROLA = [
    "{parola}{numero}",
    "{parola}{anno}",
    "{parola}{anno2}",
    "{Parola}{anno}",
    "{parola}{simbolo}",
    "{parola}{simbolo}{numero}",
    "{parola}{parola2}",
    "{Parola}{numero}{simbolo}",
    "{parola}",
]

# Password a tema calcistico
PATTERNS_SQUADRA = [
    "{squadra}{anno}",
    "{squadra}{anno2}",
    "{squadra}{numero}",
    "{Squadra}{anno}",
    "{squadra}{simbolo}",
    "{squadra}1",
]


def _hash(index, salt=0):
    """Hash deterministico dell'indice, distribuito su [0, 10^6)."""
    return (index * 2654435761 + 987654 + salt) % 1000000


def _persona(index):
    """Dati anagrafici deterministici associati a un indice.

    Condivisi da mail e password, cosi' la password puo' risultare coerente
    con l'indirizzo (stesso nome, cognome e anno di nascita).
    """
    h = _hash(index)
    nome = NOMI[h % len(NOMI)]
    cognome = COGNOMI[(h * 7) % len(COGNOMI)]
    anno = 1960 + (h % 50)          # anno di nascita plausibile: 1960-2009
    numero = 1 + (h % 9999)
    return nome, cognome, anno, numero


def _scelta_pesata(coppie, valore):
    """Sceglie un elemento da una lista di (elemento, peso) in modo
    deterministico a partire da un valore intero."""
    totale = sum(peso for _, peso in coppie)
    v = valore % totale
    cum = 0
    for elemento, peso in coppie:
        cum += peso
        if v < cum:
            return elemento
    return coppie[-1][0]


def genera_email(index):
    """Genera un'email realistica in modo deterministico."""
    nome, cognome, anno, numero = _persona(index)
    h = _hash(index)

    # Seleziona il dominio in modo deterministico, rispettando i pesi
    totale_pesi = sum(DOMINI.values())
    scelta = h % totale_pesi
    cum_peso = 0
    dominio = next(iter(DOMINI))
    for d, peso in DOMINI.items():
        cum_peso += peso
        if scelta < cum_peso:
            dominio = d
            break

    pattern = PATTERNS_EMAIL[h % len(PATTERNS_EMAIL)]
    email = pattern.format(
        nome=nome,
        cognome=cognome,
        dominio=dominio,
        anno=anno,
        numero=numero,
    )
    return email.lower()


def genera_password(index):
    """Genera una password realistica basata su wordlist italiane e coerente
    con la mail generata per lo stesso indice, in modo deterministico.

    Nel ~42% dei casi la password deriva dai dati della persona (nome,
    cognome, anno di nascita) presenti anche nell'email; negli altri casi usa
    parole comuni, squadre di calcio o sequenze tipiche dei breach italiani.
    """
    nome, cognome, anno, _ = _persona(index)
    h = _hash(index, 999999)

    parola = PAROLE_COMUNI[h % len(PAROLE_COMUNI)]
    squadra = SQUADRE[(h * 13) % len(SQUADRE)]
    campi = {
        "nome": nome,
        "Nome": nome.capitalize(),
        "cognome": cognome,
        "Cognome": cognome.capitalize(),
        "anno": anno,
        "anno2": str(anno)[-2:],
        "numero": 1 + (h % 999),
        "simbolo": SIMBOLI[(h * 17) % len(SIMBOLI)],
        "parola": parola,
        "Parola": parola.capitalize(),
        "parola2": PAROLE_COMUNI[(h * 11 + 7) % len(PAROLE_COMUNI)],
        "squadra": squadra,
        "Squadra": squadra.capitalize(),
    }

    strategia = _scelta_pesata(STRATEGIE_PASSWORD, h)

    if strategia == "personale":
        return PATTERNS_PERSONALI[(h // 7) % len(PATTERNS_PERSONALI)].format(**campi)
    if strategia == "parola":
        return PATTERNS_PAROLA[(h // 7) % len(PATTERNS_PAROLA)].format(**campi)
    if strategia == "squadra":
        return PATTERNS_SQUADRA[(h // 7) % len(PATTERNS_SQUADRA)].format(**campi)
    if strategia == "sequenza":
        return SEQUENZE[(h // 7) % len(SEQUENZE)]
    # comune_pura
    return PAROLE_COMUNI[(h // 7) % len(PAROLE_COMUNI)]

def genera_batch(start_idx, batch_size):
    """Genera un batch di righe"""
    batch = []
    for offset in range(batch_size):
        i = start_idx + offset
        email = genera_email(i)
        password = genera_password(i)
        batch.append(f"{email}:{password}\n")
    return batch

def genera_dataset(num_righe=None):
    """Genera il dataset completo.

    I parametri vengono letti al momento della chiamata (non all'import) cosi'
    l'opzione --righe della CLI e le variabili d'ambiente hanno sempre effetto.
    """
    # Leggi la configurazione al momento della chiamata
    num_righe = num_righe if num_righe is not None else int(os.environ.get("NUM_RIGHE", "1000000"))
    buffer_size = int(os.environ.get("BUFFER_SIZE", "100000"))
    nome_file = os.environ.get("OUTPUT_FILE", "data/breach_dataset.txt")

    # Crea la directory di output (gestisce anche OUTPUT_FILE con sottocartelle)
    Path(nome_file).parent.mkdir(parents=True, exist_ok=True)

    print("=" * 70)
    print("🔐 GENERAZIONE DATASET BREACH - RICERCA ACCADEMICA")
    print("=" * 70)
    print(f"📊 Righe da generare: {num_righe:,}")
    print(f"💻 CPU disponibili: {cpu_count()}")
    print(f"⚡ Processi in parallelo: {NUM_PROCESSI}")
    print(f"📦 Buffer size: {buffer_size:,}")
    print("=" * 70)

    start_time = time.time()

    # Rimuovi file esistente
    if Path(nome_file).exists():
        Path(nome_file).unlink()

    # Calcola batch size ottimale
    batch_size = min(50_000, max(5_000, num_righe // (NUM_PROCESSI * 2)))
    num_batch = (num_righe + batch_size - 1) // batch_size

    print(f"📦 Generazione di {num_batch:,} batch...\n")

    # Generazione parallela
    with ProcessPoolExecutor(max_workers=NUM_PROCESSI) as executor:
        futures = []
        for batch_id in range(num_batch):
            start_idx = batch_id * batch_size
            current_size = min(batch_size, num_righe - start_idx)
            if current_size <= 0:
                break
            future = executor.submit(genera_batch, start_idx, current_size)
            futures.append((future, batch_id))

        # Scrittura ottimizzata
        with open(nome_file, 'w', encoding='utf-8') as f:
            buffer = []
            righe_scritte = 0

            with tqdm(total=num_righe, desc="Generazione", unit="righe") as pbar:
                for future, batch_id in futures:
                    try:
                        batch = future.result(timeout=120)
                        buffer.extend(batch)
                        righe_scritte += len(batch)
                        pbar.update(len(batch))

                        if len(buffer) >= buffer_size:
                            f.writelines(buffer)
                            buffer.clear()

                    except Exception as e:
                        print(f"⚠️ Errore batch {batch_id}: {e}")

                if buffer:
                    f.writelines(buffer)

    elapsed = time.time() - start_time
    velocita = righe_scritte / elapsed if elapsed > 0 else 0
    file_size = Path(nome_file).stat().st_size if Path(nome_file).exists() else 0

    print("\n" + "=" * 70)
    print("✅ GENERAZIONE COMPLETATA!")
    print("=" * 70)
    print(f"📁 File: {nome_file}")
    print(f"📊 Righe scritte: {righe_scritte:,}")
    print(f"💾 Dimensione: {file_size / (1024**3):.2f} GB")
    print(f"⏱️ Tempo: {elapsed/60:.2f} minuti")
    print(f"⚡ Velocità: {velocita:,.0f} righe/secondo")
    print("=" * 70)

if __name__ == "__main__":
    genera_dataset()