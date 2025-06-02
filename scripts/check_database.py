#!/usr/bin/env python3
"""
Script για έλεγχο της SQLite database
"""
import sqlite3
import os

def check_database():
    db_path = 'data/processed/legal_text.db'
    
    if not os.path.exists(db_path):
        print(f"❌ Database not found at: {db_path}")
        return
    
    print(f"✅ Database found: {db_path}")
    print(f"📊 Size: {os.path.getsize(db_path) / 1024 / 1024:.2f} MB")
    
    # Σύνδεση με τη database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Λήψη όλων των tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    
    print(f"\n📋 Tables found: {len(tables)}")
    for table in tables:
        table_name = table[0]
        cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
        count = cursor.fetchone()[0]
        print(f"  - {table_name}: {count} rows")
        
        # Δείξε τα columns
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = cursor.fetchall()
        print(f"    Columns: {', '.join([col[1] for col in columns])}")
    
    conn.close()

if __name__ == "__main__":
    check_database()
