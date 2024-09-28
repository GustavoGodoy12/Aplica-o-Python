import os
import shutil
from datetime import datetime
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / 'data'
BACKUP_DIR = BASE_DIR / 'backups'
EXPORT_DIR = BASE_DIR / 'exports'
DB_PATH = DATA_DIR / 'livraria.db'

# Criar diretórios se não existirem
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(BACKUP_DIR, exist_ok=True)
os.makedirs(EXPORT_DIR, exist_ok=True)

def fazer_backup():
    data_atual = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    backup_path = BACKUP_DIR / f"backup_livraria_{data_atual}.db"
    shutil.copy(DB_PATH, backup_path)
    print(f"Backup criado: {backup_path}")

def limpar_backups_antigos():
    backups = sorted(BACKUP_DIR.glob("backup_livraria_*.db"), key=os.path.getmtime, reverse=True)
    for backup in backups[5:]:
        os.remove(backup)
        print(f"Backup antigo removido: {backup}")
