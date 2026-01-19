#!/usr/bin/env python3
"""Verify that all dependencies are installed correctly."""

import sys

def check_import(module_name, package_name=None):
    """Check if a module can be imported."""
    if package_name is None:
        package_name = module_name

    try:
        __import__(module_name)
        print(f"✅ {package_name} - installed")
        return True
    except ImportError:
        print(f"❌ {package_name} - NOT installed")
        return False

print("=" * 60)
print("LinkedIn Post Generator - Setup Verification")
print("=" * 60)
print()

print(f"Python Version: {sys.version}")
print(f"Python Path: {sys.executable}")
print()

print("Checking dependencies...")
print("-" * 60)

all_good = True
all_good &= check_import("click")
all_good &= check_import("rich")
all_good &= check_import("crewai")
all_good &= check_import("anthropic")
all_good &= check_import("duckduckgo_search", "duckduckgo-search")
all_good &= check_import("dotenv", "python-dotenv")
all_good &= check_import("pydantic")
all_good &= check_import("langchain")
all_good &= check_import("langchain_anthropic", "langchain-anthropic")

print("-" * 60)
print()

if all_good:
    print("✅ All dependencies installed successfully!")
    print()
    print("Next steps:")
    print("1. Copy .env.example to .env")
    print("2. Add your Anthropic API key to .env")
    print("3. Run: python main.py generate --topic 'Your topic'")
else:
    print("❌ Some dependencies are missing!")
    print()
    print("Fix:")
    print("  pip install -r requirements.txt")

print()
print("=" * 60)
