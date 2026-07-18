"""
Unit tests for generator module
"""

import pytest
from pathlib import Path

# Aggiungi src al path per i test
import sys
sys.path.append(str(Path(__file__).parent.parent))

from src.generator import (
    genera_email,
    genera_password,
    genera_batch,
    NOMI,
    COGNOMI,
    DOMINI,
    PAROLE_COMUNI,
    SQUADRE,
    SEQUENZE,
    TOP_PASSWORD,
)

class TestGenerator:
    """Test per il generatore di dataset"""
    
    def test_genera_email(self):
        """Test generazione email"""
        email = genera_email(1)
        
        # Verifica formato
        assert '@' in email
        assert '.' in email.split('@')[1]  # Dominio ha TLD
        
        # Verifica dominio valido
        dominio = email.split('@')[1]
        assert dominio in DOMINI

        # Ogni pattern contiene almeno il nome o il cognome per esteso
        assert any(nome in email for nome in NOMI) or any(cognome in email for cognome in COGNOMI)
    
    def test_genera_password(self):
        """Test generazione password"""
        password = genera_password(1)
        
        # Verifica non vuota
        assert len(password) > 0
        assert len(password) <= 64  # Limite ragionevole
        
        # Verifica caratteri validi
        import string
        valid_chars = string.ascii_letters + string.digits + "!@#$%&*?+"
        assert all(c in valid_chars for c in password)
    
    def test_genera_batch(self):
        """Test generazione batch"""
        batch_size = 10
        batch = genera_batch(0, batch_size)
        
        assert len(batch) == batch_size
        
        for line in batch:
            assert ':' in line
            email, password = line.strip().split(':', 1)
            assert '@' in email
            assert len(password) > 0
    
    def test_genera_batch_large(self):
        """Test batch grande"""
        batch_size = 1000
        batch = genera_batch(0, batch_size)
        assert len(batch) == batch_size
    
    def test_determinismo(self):
        """Test che la generazione sia deterministica"""
        # Due chiamate con lo stesso indice devono produrre lo stesso risultato
        email1 = genera_email(42)
        email2 = genera_email(42)
        assert email1 == email2

        password1 = genera_password(42)
        password2 = genera_password(42)
        assert password1 == password2

    def test_righe_uniche(self):
        """Nessuna riga (email:password) deve mai ripetersi identica, e le
        email devono essere tutte diverse (identificativo univoco in coda)."""
        n = 200000
        righe = {f"{genera_email(i)}:{genera_password(i)}" for i in range(n)}
        assert len(righe) == n, "trovate righe duplicate"
        emails = {genera_email(i) for i in range(n)}
        assert len(emails) == n, "trovate email duplicate"

    def test_password_coerente_con_email(self):
        """Una quota rilevante di password deve condividere nome o cognome con
        l'email della stessa riga (coerenza mail <-> password)."""
        campione = 3000
        coerenti = 0
        for i in range(campione):
            local = genera_email(i).split('@')[0]
            pwd = genera_password(i).lower()
            nome_mail = next((n for n in NOMI if n in local), None)
            cognome_mail = next((c for c in COGNOMI if c in local), None)
            if (nome_mail and nome_mail in pwd) or (cognome_mail and cognome_mail in pwd):
                coerenti += 1
        # la strategia "personale" pesa ~42%, con margine assumiamo almeno 30%
        assert coerenti / campione >= 0.30

    def test_password_realistica_wordlist_italiana(self):
        """Ogni password deve essere una sequenza nota oppure contenere una
        base italiana (nome, cognome, parola comune o squadra): niente
        stringhe casuali."""
        basi = set(NOMI) | set(COGNOMI) | set(PAROLE_COMUNI) | set(SQUADRE)
        note = set(SEQUENZE) | set(TOP_PASSWORD)
        for i in range(3000):
            pwd = genera_password(i).lower()
            if pwd in note:
                continue
            assert any(base in pwd for base in basi), f"password non riconosciuta: {pwd}"

    def test_password_valide_su_campione(self):
        """Char set e lunghezza validi su un ampio campione di indici."""
        import string
        validi = set(string.ascii_letters + string.digits + "!@#$%&*?+")
        for i in range(3000):
            pwd = genera_password(i)
            assert 0 < len(pwd) <= 64
            assert all(c in validi for c in pwd)

# Esegui i test se il file è eseguito direttamente
if __name__ == "__main__":
    pytest.main([__file__, "-v"])