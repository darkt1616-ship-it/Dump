"""
ANALIZZATORE DATASET BREACH
Per analisi statistiche e report
"""

from collections import Counter, defaultdict
import re
from pathlib import Path

class BreachAnalyzer:
    def __init__(self, dump_file="data/breach_dataset.txt"):
        self.dump_file = dump_file
        self.stats = {
            'totale': 0,
            'domini': Counter(),
            'password_forza': {'debole': 0, 'media': 0, 'forte': 0},
            'password_comuni': Counter(),
            'pattern_breach': defaultdict(int),
            'email_patterns': Counter(),
            'lunghezza_passwords': []
        }
    
    def analizza(self, campione=10000):
        """Analizza il dataset"""
        print(f"🔍 Analizzo {campione:,} credenziali...")
        
        if not Path(self.dump_file).exists():
            print(f"❌ File {self.dump_file} non trovato!")
            return None
        
        with open(self.dump_file, 'r', encoding='utf-8') as f:
            for i, line in enumerate(f):
                if i >= campione:
                    break
                
                try:
                    email, password = line.strip().split(':', 1)
                    self.stats['totale'] += 1
                    
                    # Analisi dominio
                    dominio = email.split('@')[1] if '@' in email else 'unknown'
                    self.stats['domini'][dominio] += 1
                    
                    # Analisi password
                    self._analizza_password(password)
                    
                    # Pattern email
                    if re.search(r'\d{4,}', email):
                        self.stats['email_patterns']['con_anno'] += 1
                    
                    # Pattern breach
                    if len(password) <= 6:
                        self.stats['pattern_breach']['password_corte'] += 1
                    if password.isdigit():
                        self.stats['pattern_breach']['solo_numeri'] += 1
                    if '123' in password or 'abc' in password.lower():
                        self.stats['pattern_breach']['pattern_sequenziale'] += 1

                except ValueError:
                    continue
        
        return self.stats
    
    def _analizza_password(self, password):
        """Analizza forza password"""
        length = len(password)
        self.stats['lunghezza_passwords'].append(length)
        
        if length < 8:
            self.stats['password_forza']['debole'] += 1
        elif length < 12:
            self.stats['password_forza']['media'] += 1
        else:
            self.stats['password_forza']['forte'] += 1
        
        if password.lower() in ['password', '123456', 'qwerty', 'admin']:
            self.stats['password_comuni'][password] += 1
    
    def genera_report(self):
        """Genera report formattato"""
        if self.stats['totale'] == 0:
            return "❌ Nessun dato analizzato"
        
        total = self.stats['totale']
        
        report = f"""
╔══════════════════════════════════════════════════════════════╗
║     REPORT ANALISI DATASET BREACH                           ║
╚══════════════════════════════════════════════════════════════╝

📊 STATISTICHE GENERALI
───────────────────────────────────────────────
  Credenziali analizzate: {total:,}
  Lunghezza media password: {sum(self.stats['lunghezza_passwords'])/total:.1f} caratteri

📧 DOMINI PIU' COMPROMESSI (TOP 10)
───────────────────────────────────────────────"""
        
        for dominio, count in self.stats['domini'].most_common(10):
            pct = (count / total) * 100
            report += f"\n  {dominio:20} {count:>8,} ({pct:>5.1f}%)"
        
        report += f"""

🔐 FORZA PASSWORD
───────────────────────────────────────────────
  🟡 Debole (<8): {self.stats['password_forza']['debole']:,} ({self.stats['password_forza']['debole']/total*100:.1f}%)
  🟢 Media (8-11): {self.stats['password_forza']['media']:,} ({self.stats['password_forza']['media']/total*100:.1f}%)
  🔴 Forte (≥12): {self.stats['password_forza']['forte']:,} ({self.stats['password_forza']['forte']/total*100:.1f}%)

⚠️ PATTERN DI BREACH RILEVATI
───────────────────────────────────────────────
  Password corte: {self.stats['pattern_breach'].get('password_corte', 0):,}
  Solo numeri: {self.stats['pattern_breach'].get('solo_numeri', 0):,}
  Pattern sequenziali: {self.stats['pattern_breach'].get('pattern_sequenziale', 0):,}
  Email con anno/numero: {self.stats['email_patterns'].get('con_anno', 0):,}

🔑 PASSWORD PIU' COMUNI
───────────────────────────────────────────────"""
        
        for pwd, count in self.stats['password_comuni'].most_common(5):
            report += f"\n  {pwd:15} {count:>6} volte"
        
        report += """

🛡️ RACCOMANDAZIONI PER IL SISTEMA DI SICUREZZA
───────────────────────────────────────────────
  1. 📧 Monitorare domini ad alto rischio
  2. 🔐 Richiedere MFA per password deboli
  3. 🚫 Bloccare password comuni (top 100)
  4. 📊 Implementare rate limiting

╔══════════════════════════════════════════════════════════════╗
║  ANALISI COMPLETATA                                         ║
╚══════════════════════════════════════════════════════════════╝
"""
        return report

def main():
    """Entry point per il comando breach-analyze"""
    analyzer = BreachAnalyzer()
    analyzer.analizza(10000)
    print(analyzer.genera_report())


if __name__ == "__main__":
    main()