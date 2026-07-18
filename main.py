#!/usr/bin/env python3
"""
BREACH RESEARCH - Main Entry Point
Per Ricerca Accademica sulla Cybersecurity
"""

import click

from src.generator import genera_dataset
from src.analyzer import BreachAnalyzer
from src.security_tester import SecuritySystemTester

@click.group()
def cli():
    """Breach Research - Strumenti per la ricerca sul credential stuffing"""
    pass

@cli.command()
@click.option('--righe', default=1000000, help='Numero di righe da generare')
def generate(righe):
    """Genera il dataset di breach"""
    genera_dataset(num_righe=righe)

@cli.command()
@click.option('--campione', default=10000, help='Numero di righe da analizzare')
def analyze(campione):
    """Analizza il dataset generato"""
    analyzer = BreachAnalyzer()
    analyzer.analizza(campione)
    print(analyzer.genera_report())

@cli.command()
@click.option('--credenziali', default=1000, help='Numero di credenziali da testare')
def test(credenziali):
    """Testa il sistema di sicurezza"""
    tester = SecuritySystemTester()
    tester.load_credentials(credenziali)
    tester.test_security_system()

@cli.command()
def full():
    """Esegui l'intero workflow"""
    print("🔐 AVVIO WORKFLOW COMPLETO")
    print("=" * 50)
    
    # 1. Genera
    print("\n[1/3] Generazione dataset...")
    generate.callback(righe=100000)
    
    # 2. Analizza
    print("\n[2/3] Analisi dataset...")
    analyze.callback(campione=10000)
    
    # 3. Test
    print("\n[3/3] Test sistema sicurezza...")
    test.callback(credenziali=1000)

if __name__ == "__main__":
    cli()