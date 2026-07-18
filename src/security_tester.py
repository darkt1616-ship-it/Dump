"""
SISTEMA DI SICUREZZA - TEST CONTRO IL DUMP
"""

from pathlib import Path


class SecuritySystemTester:
    def __init__(self, dump_file="data/breach_dataset.txt"):
        self.dump_file = dump_file
        self.credential_cache = {}
        self.detection_stats = {
            'total_attempts': 0,
            'breach_detected': 0,
        }
    
    def load_credentials(self, num_credenziali=1000):
        """Carica credenziali dal dump"""
        print(f"📥 Carico {num_credenziali:,} credenziali...")

        if not Path(self.dump_file).exists():
            print(f"❌ File {self.dump_file} non trovato! Esegui prima 'generate'.")
            return

        with open(self.dump_file, 'r', encoding='utf-8') as f:
            for i, line in enumerate(f):
                if i >= num_credenziali:
                    break
                try:
                    email, password = line.strip().split(':', 1)
                    self.credential_cache[email] = password
                except ValueError:
                    continue
        
        print(f"✅ Caricate {len(self.credential_cache)} credenziali")
    
    def test_security_system(self):
        """Testa il sistema di sicurezza"""
        print("\n🛡️ TEST DEL SISTEMA DI SICUREZZA")
        print("=" * 50)
        
        for email, password in self.credential_cache.items():
            self.detection_stats['total_attempts'] += 1

            # 1. Controllo forza password
            if len(password) < 8:
                self.detection_stats['breach_detected'] += 1
                print(f"🔴 Password debole rilevata: {email}")

            # 2. Controllo pattern sospetti
            elif password.isdigit() or '123' in password:
                self.detection_stats['breach_detected'] += 1
                print(f"🔴 Pattern sospetto rilevato: {email}")

        self._print_results()
    
    def _print_results(self):
        """Stampa i risultati del test"""
        print("\n📊 RISULTATI TEST")
        print("=" * 50)
        print(f"🔄 Tentativi totali: {self.detection_stats['total_attempts']}")
        print(f"🔴 Breach rilevati: {self.detection_stats['breach_detected']}")

        if self.detection_stats['total_attempts'] > 0:
            detection_rate = self.detection_stats['breach_detected'] / self.detection_stats['total_attempts'] * 100
            print(f"📈 Tasso di rilevazione: {detection_rate:.1f}%")

def main():
    """Entry point per il comando breach-test"""
    tester = SecuritySystemTester()
    tester.load_credentials(1000)
    tester.test_security_system()


if __name__ == "__main__":
    main()