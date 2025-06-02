#!/usr/bin/env python3
"""
Explore the legal_text.db SQLite database
Εξερεύνηση της βάσης δεδομένων legal_text.db
"""

import sqlite3
import pandas as pd
import os
from pathlib import Path

def explore_database():
    """Εξερεύνηση της SQLite database"""
    
    # Paths to check
    db_paths = [
        Path("data/processed/legal_text.db"),
        Path("data/raw/legal_text.db"),
        Path("data/legal_text.db"),
    ]
    
    # Find the database
    db_path = None
    for path in db_paths:
        if path.exists():
            db_path = path
            print(f"✓ Βρέθηκε database: {path}")
            break
    
    if not db_path:
        print("❌ Δεν βρέθηκε η database!")
        print("Searched paths:", [str(p) for p in db_paths])
        return
    
    # Connect to database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    print(f"\n📊 Database Info:")
    print(f"Size: {os.path.getsize(db_path) / 1024 / 1024:.2f} MB")
    
    # Get all tables
    tables = pd.read_sql_query(
        "SELECT name FROM sqlite_master WHERE type='table';", 
        conn
    )
    print(f"\n📋 Tables found: {len(tables)}")
    for table in tables['name']:
        print(f"  - {table}")
    
    # For each table, show schema and sample data
    for table in tables['name']:
        print(f"\n{'='*50}")
        print(f"📌 Table: {table}")
        print(f"{'='*50}")
        
        # Get schema
        schema = pd.read_sql_query(f"PRAGMA table_info({table})", conn)
        print("\n🔧 Schema:")
        print(schema[['name', 'type', 'notnull', 'pk']])
        
        # Count rows
        count = pd.read_sql_query(f"SELECT COUNT(*) as count FROM {table}", conn)
        print(f"\n📊 Total rows: {count['count'][0]:,}")
        
        # Show sample data
        print("\n📄 Sample data (first 3 rows):")
        sample = pd.read_sql_query(f"SELECT * FROM {table} LIMIT 3", conn)
        print(sample)
        
        # Show column statistics if numeric
        numeric_cols = schema[schema['type'].str.contains('INT|REAL|NUMERIC', case=False)]['name'].tolist()
        if numeric_cols:
            print(f"\n📈 Numeric column statistics:")
            stats = pd.read_sql_query(
                f"SELECT {', '.join([f'MIN({col}) as min_{col}, MAX({col}) as max_{col}, AVG({col}) as avg_{col}' for col in numeric_cols])} FROM {table}", 
                conn
            )
            print(stats.T)
    
    conn.close()
    print("\n✅ Database exploration complete!")

if __name__ == "__main__":
    explore_database()
