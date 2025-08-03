#!/usr/bin/env python3
"""
Debug script to check SQL parsing.
"""

import os

# Read schema script
script_dir = os.path.dirname(os.path.abspath(__file__))
schema_file = os.path.join(script_dir, 'database', 'schema.sql')

with open(schema_file, 'r', encoding='utf-8') as f:
    schema_sql = f.read()

# Split script into individual statements
statements = [stmt.strip() for stmt in schema_sql.split('GO') if stmt.strip()]

print(f"Found {len(statements)} SQL statements:")
print("=" * 50)

for i, statement in enumerate(statements, 1):
    print(f"\nStatement {i}:")
    print("-" * 20)
    if statement and not statement.startswith('--'):
        if statement.upper().startswith('PRINT'):
            print("PRINT statement (will be skipped)")
        else:
            print("SQL statement (will be executed)")
        print(f"Content: {statement[:100]}...")
    else:
        print("Empty or comment (will be skipped)")
