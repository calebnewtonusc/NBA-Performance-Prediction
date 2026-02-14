#!/usr/bin/env python3
"""
Generate Secure Secrets for Production Deployment

Usage:
    python scripts/generate_secrets.py

This script generates cryptographically secure random strings for:
- SECRET_KEY (JWT token signing)
- API_PASSWORD (API authentication)
- Database passwords
- Redis passwords
"""

import secrets
import string


def generate_secret_key(length: int = 32) -> str:
    """Generate a URL-safe secret key"""
    return secrets.token_urlsafe(length)


def generate_password(length: int = 24, use_special: bool = True) -> str:
    """Generate a secure password with letters, numbers, and optional special characters"""
    alphabet = string.ascii_letters + string.digits
    if use_special:
        alphabet += "!@#$%^&*()-_=+[]{}|;:,.<>?"

    # Ensure at least one character from each category
    password = [
        secrets.choice(string.ascii_lowercase),
        secrets.choice(string.ascii_uppercase),
        secrets.choice(string.digits),
    ]

    if use_special:
        password.append(secrets.choice("!@#$%^&*()-_=+"))

    # Fill the rest randomly
    password.extend(secrets.choice(alphabet) for _ in range(length - len(password)))

    # Shuffle to avoid predictable patterns
    secrets.SystemRandom().shuffle(password)

    return ''.join(password)


def main():
    """Generate and display all required secrets"""
    print("=" * 70)
    print("[lock.shield.fill] NBA Performance Prediction - Production Secrets Generator")
    print("=" * 70)
    print()
    print("Copy these values to your environment variables:")
    print()
    print("-" * 70)
    print("# Railway Backend Environment Variables")
    print("-" * 70)
    print()

    # API Secrets
    print(f"SECRET_KEY={generate_secret_key(32)}")
    print(f"API_PASSWORD={generate_password(24)}")
    print()

    # Database
    print("# PostgreSQL (Railway will auto-generate DATABASE_URL)")
    print(f"POSTGRES_PASSWORD={generate_password(24, use_special=False)}")
    print()

    # Redis
    print("# Redis (Railway will auto-configure connection)")
    print(f"REDIS_PASSWORD={generate_password(24, use_special=False)}")
    print()

    print("-" * 70)
    print("# Streamlit Cloud Secrets")
    print("-" * 70)
    print()
    print("# Add to Streamlit Cloud > App Settings > Secrets")
    print("API_BASE_URL = \"https://your-railway-app.up.railway.app\"")
    print("API_USERNAME = \"admin\"")
    print(f"API_PASSWORD = \"{generate_password(24)}\"")
    print()

    print("-" * 70)
    print("# Docker Compose .env file (Local Development)")
    print("-" * 70)
    print()
    print(f"SECRET_KEY={generate_secret_key(32)}")
    print(f"API_PASSWORD={generate_password(24)}")
    print(f"POSTGRES_PASSWORD={generate_password(24, use_special=False)}")
    print(f"REDIS_PASSWORD={generate_password(24, use_special=False)}")
    print()

    print("=" * 70)
    print("[exclamationmark.triangle]  IMPORTANT SECURITY NOTES:")
    print("=" * 70)
    print("1. Store these secrets securely (use a password manager)")
    print("2. Never commit secrets to version control")
    print("3. Use different secrets for dev, staging, and production")
    print("4. Rotate secrets periodically")
    print("5. Share secrets only through secure channels (not email/Slack)")
    print("=" * 70)


if __name__ == "__main__":
    main()
