#!/bin/bash
# Quick reference for common populate_db commands

# Full database reset with default data
python scripts/populate_db.py --clear --seed 42

# Minimal test data (good for development)
python scripts/populate_db.py --clear --seed 42 --courses 1 --students-per-course 4

# Medium dataset for testing
python scripts/populate_db.py --clear --seed 42 --courses 2 --students-per-course 8

# Large dataset for performance testing
python scripts/populate_db.py --clear --seed 42 --courses 5 --students-per-course 20

# Add more data without clearing (appends to existing data)
python scripts/populate_db.py --courses 2 --students-per-course 5

# Quick check - just create/verify tables without adding data
# (use the script without --clear and with 0 count - currently not supported, use minimal dataset instead)
