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
    DOMINI
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
        
        # Verifica nome/cognome presenti
        assert any(nome in email for nome in NOMI)
        assert any(cognome in email for cognome in COGNOMI)
    
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

# Esegui i test se il file è eseguito direttamente
if __name__ == "__main__":
    pytest.main([__file__, "-v"])