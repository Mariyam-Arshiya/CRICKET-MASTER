#!/usr/bin/env python3
"""
🏏 CRICKET MASTER - ONE-CLICK LAUNCHER
Fixes all errors and launches complete app
"""

import sys
import subprocess
import os
import time

def print_status(msg):
    print(f"📢 {msg}")

print("🏏 CRICKET MASTER - Complete Launcher Starting...")
print_status("Step 1: Installing core dependencies (Python 3.7 compatible)...")

# Install minimal deps (no pyarrow)
deps = [
    'requests==2.31.0',
    'pandas==1.3.5'
]
