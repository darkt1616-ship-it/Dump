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

# Configurazione
NUM_RIGHE = int(os.environ.get("NUM_RIGHE", "1000000"))
BUFFER_SIZE = int(os.environ.get("BUFFER_SIZE", "100000"))
NUM_PROCESSI = max(1, cpu_count() - 1)
NOME_FILE = os.environ.get("OUTPUT_FILE", "data/breach_dataset.txt")

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

# Password pattern e wordlist
PAROLE_COMUNI = [
    "password", "admin", "welcome", "login", "qwerty", "letmein",
    "monkey", "dragon", "baseball", "football", "iloveyou", "princess",
    "sunshine", "mustang", "passw0rd", "shadow", "ashley", "trustno1",
    "hello", "freedom", "whatever", "cookie", "summer", "winter",
    "spring", "autumn", "starwars", "batman", "superman", "matrix"
]

SIMBOLI = ['!', '@', '#', '$', '%', '&', '*', '?', '+']

PASSWORD_PATTERNS = [
    ("{parola}{numero}", 25),
    ("{parola}{simbolo}{numero}", 15),
    ("{parola}{anno}", 12),
    ("{parola}{parola}{numero}", 10),
    ("{parola}{simbolo}", 8),
    ("{parola}", 7),
    ("{numero}", 5),
    ("{parola}{numero}{simbolo}", 5),
    ("{parola}{parola}{anno}", 4),
]

def genera_email(index):
    """Genera email realistica in modo deterministico"""
    hash_val = (index * 2654435761 + 987654) % 1000000
    
    nome = NOMI[hash_val % len(NOMI)]
    cognome = COGNOMI[(hash_val * 7) % len(COGNOMI)]
    
    # Seleziona dominio in modo deterministico (rispettando i pesi)
    totale_pesi = sum(DOMINI.values())
    scelta = hash_val % totale_pesi
    cum_peso = 0
    dominio = next(iter(DOMINI))
    for d, peso in DOMINI.items():
        cum_peso += peso
        if scelta < cum_peso:
            dominio = d
            break

    pattern = PATTERNS_EMAIL[hash_val % len(PATTERNS_EMAIL)]
    anno = 1970 + (hash_val % 36)
    numero = 1 + (hash_val % 9999)
    
    email = pattern.format(
        nome=nome,
        cognome=cognome,
        dominio=dominio,
        anno=anno,
        numero=numero
    )
    
    return email.lower()

def genera_password(index):
    """Genera password realistica in modo deterministico"""
    hash_val = (index * 2654435761 + 987654 + 999999) % 1000000
    
    # Seleziona pattern
    rand_val = hash_val % 100
    cum_prob = 0
    pattern_scelto = PASSWORD_PATTERNS[0][0]
    
    for pattern, peso in PASSWORD_PATTERNS:
        cum_prob += peso
        if rand_val < cum_prob:
            pattern_scelto = pattern
            break
    
    # Genera componenti
    parola1 = PAROLE_COMUNI[hash_val % len(PAROLE_COMUNI)]
    parola2 = PAROLE_COMUNI[(hash_val * 11) % len(PAROLE_COMUNI)]
    numero = 1 + (hash_val % 9999)
    simbolo = SIMBOLI[(hash_val * 17) % len(SIMBOLI)]
    anno = 1970 + (hash_val % 36)
    
    password = pattern_scelto.format(
        parola=parola1,
        parola2=parola2,
        numero=numero,
        simbolo=simbolo,
        anno=anno
    )
    
    # Variazioni
    if hash_val % 3 == 0:
        password = password.capitalize()
    
    return password

def genera_batch(start_idx, batch_size):
    """Genera un batch di righe"""
    batch = []
    for offset in range(batch_size):
        i = start_idx + offset
        email = genera_email(i)
        password = genera_password(i)
        batch.append(f"{email}:{password}\n")
    return batch

def crea_directory():
    """Crea la directory per i dati"""
    Path("data").mkdir(exist_ok=True)

def genera_dataset(num_righe=None):
    """Genera il dataset completo.

    I parametri vengono letti al momento della chiamata (non all'import) cosi'
    l'opzione --righe della CLI e le variabili d'ambiente hanno sempre effetto.
    """
    crea_directory()

    # Leggi la configurazione al momento della chiamata
    num_righe = num_righe if num_righe is not None else int(os.environ.get("NUM_RIGHE", "1000000"))
    buffer_size = int(os.environ.get("BUFFER_SIZE", "100000"))
    nome_file = os.environ.get("OUTPUT_FILE", "data/breach_dataset.txt")

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
    velocita = num_righe / elapsed if elapsed > 0 else 0
    file_size = Path(nome_file).stat().st_size if Path(nome_file).exists() else 0

    print("\n" + "=" * 70)
    print("✅ GENERAZIONE COMPLETATA!")
    print("=" * 70)
    print(f"📁 File: {nome_file}")
    print(f"📊 Righe: {num_righe:,}")
    print(f"💾 Dimensione: {file_size / (1024**3):.2f} GB")
    print(f"⏱️ Tempo: {elapsed/60:.2f} minuti")
    print(f"⚡ Velocità: {velocita:,.0f} righe/secondo")
    print("=" * 70)

if __name__ == "__main__":
    genera_dataset()