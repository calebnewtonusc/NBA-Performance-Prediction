# Security Guide

## Security Improvements (v2.1)

This document outlines all security measures implemented in the NBA Prediction API.

---

## ✅ Fixed Security Issues

### 1. Environment Variable Configuration

**Problem**: Hardcoded secrets in source code
**Solution**: All sensitive configuration moved to environment variables

```bash
# Copy and customize .env.example
cp .env.example .env

# Generate secure SECRET_KEY
python3 -c "import secrets; print(secrets.token_urlsafe(32))"

# Edit .env with your secure values
```

**Required Variables**:
- `SECRET_KEY`: JWT signing key (generate with secrets.token_urlsafe(32))
- `API_USERNAME`: API authentication username
- `API_PASSWORD`: API authentication password
- `ALLOWED_ORIGINS`: Comma-separated CORS origins

### 2. CORS Restrictions

**Problem**: CORS allowed all origins (`allow_origins=["*"]`)
**Solution**: Restricted to specific origins via environment variable

```bash
# Production example
ALLOWED_ORIGINS=https://api.yourdomain.com,https://app.yourdomain.com

# Development example  
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8000
```

### 3. Non-Root Docker Container

**Problem**: Container ran as root user (security risk)
**Solution**: Added dedicated `nbaapi` user with UID 1000

```dockerfile
# Create non-root user
RUN groupadd -r nbaapi && useradd -r -g nbaapi -u 1000 nbaapi

# Switch to non-root user
USER nbaapi
```

**Benefits**:
- Container breakout doesn't give root access
- Follows principle of least privilege
- Production security best practice

### 4. Thread Safety

**Problem**: Global state not thread-safe with multiple workers
**Solution**: Added threading.RLock() for all shared resources

```python
# Thread-safe model loading
with models_lock:
    loaded_models[key] = model

# Thread-safe metrics
with metrics_lock:
    api_metrics["predictions_total"] += 1
```

### 5. Metrics Tracking

**Problem**: Metrics endpoints returned hardcoded zeros
**Solution**: Implemented actual thread-safe counters

**Tracked Metrics**:
- `predictions_total`: Total predictions made
- `cache_hits`: Cache hit count
- `cache_misses`: Cache miss count
- `errors_total`: Total errors
- `cache_hit_rate`: Calculated hit rate percentage

---

## Security Checklist

### Development

- [x] Use `.env` for configuration (never commit `.env`)
- [x] Generate strong `SECRET_KEY`
- [x] Use environment-specific credentials
- [x] Enable CORS only for trusted origins
- [x] Run containers as non-root user
- [x] Use thread-safe data structures

### Production

- [ ] **CRITICAL**: Change all default passwords
- [ ] **CRITICAL**: Generate production `SECRET_KEY`
- [ ] **CRITICAL**: Set strong `API_PASSWORD`
- [ ] Configure HTTPS/TLS (reverse proxy)
- [ ] Restrict CORS to production domains
- [ ] Enable rate limiting per user (not just IP)
- [ ] Set up database backups
- [ ] Configure monitoring and alerting
- [ ] Use secrets management (AWS Secrets Manager, Vault, etc.)
- [ ] Enable audit logging
- [ ] Regular security updates

---

## Generating Secure Credentials

### SECRET_KEY (JWT Signing)

```bash
# Python (recommended)
python3 -c "import secrets; print(secrets.token_urlsafe(32))"

# OpenSSL
openssl rand -hex 32

# Output example:
# XK7jP4mR9sT2wN8vL3cH6qY5aE1dF0gB
```

### Passwords

```bash
# Generate strong password
python3 -c "import secrets; import string; chars = string.ascii_letters + string.digits + string.punctuation; print(''.join(secrets.choice(chars) for _ in range(32)))"
```

---

## HTTPS/TLS Configuration

### Using NGINX Reverse Proxy

```nginx
server {
    listen 443 ssl http2;
    server_name api.yourdomain.com;

    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### Using Caddy (Automatic HTTPS)

```
api.yourdomain.com {
    reverse_proxy localhost:8000
}
```

---

## Rate Limiting

Current rate limits (per IP address):

| Endpoint | Limit |
|----------|-------|
| `/api/predict` | 100/minute |
| `/api/predict/batch` | 20/minute |
| `/api/health` | 60/minute |
| `/api/metrics` | 30/minute |
| Other endpoints | 30/minute |

### Production Recommendations

1. **Per-User Limits**: Track by user ID instead of IP
2. **Different Tiers**: Free vs paid users
3. **Burst Handling**: Allow temporary bursts
4. **Redis Backend**: Use Redis for distributed rate limiting

---

## Database Security

### Connection Security

```python
# Use SSL for database connections
DATABASE_URL = "postgresql://user:pass@host:5432/db?sslmode=require"
```

### Best Practices

- [x] Use SQLAlchemy ORM (prevents SQL injection)
- [ ] Enable SSL/TLS for database connections
- [ ] Use read-only credentials for read operations
- [ ] Regular backups with encryption
- [ ] Network isolation (private subnet)
- [ ] Audit logging for sensitive queries

---

## Monitoring & Alerts

### Security Events to Monitor

1. **Failed Authentication**: Track in `api_metrics["errors_total"]`
2. **Rate Limit Violations**: Log excessive requests
3. **Unusual Patterns**: Spike in errors or predictions
4. **Database Errors**: Connection failures, slow queries

### Recommended Tools

- **Sentry**: Error tracking and monitoring
- **Prometheus + Grafana**: Metrics and dashboards
- **AWS CloudWatch**: Cloud-based monitoring
- **Datadog**: All-in-one monitoring

---

## Vulnerability Scanning

### Scan Dependencies

```bash
# Install safety
pip install safety

# Scan for known vulnerabilities
safety check -r requirements-api.txt
```

### Scan Docker Images

```bash
# Using Trivy
trivy image nba-prediction:latest

# Using Grype
grype nba-prediction:latest
```

---

## Incident Response

### If Secrets are Compromised

1. **Immediately**:
   - Rotate `SECRET_KEY` (invalidates all JWTs)
   - Change `API_PASSWORD`
   - Update database passwords
   - Rotate Redis password

2. **Investigate**:
   - Check logs for unauthorized access
   - Review recent API calls
   - Identify affected users

3. **Notify**:
   - Inform users if data was accessed
   - Document the incident
   - Update security procedures

---

## Security Updates

### Stay Updated

```bash
# Update dependencies regularly
pip install --upgrade -r requirements-api.txt

# Check for security updates
pip list --outdated

# Update base Docker image
docker pull python:3.11-slim
docker build -t nba-prediction:latest -f Dockerfile.api .
```

---

## Reporting Security Issues

If you discover a security vulnerability:

1. **DO NOT** create a public GitHub issue
2. Email security@yourdomain.com (set up dedicated email)
3. Include:
   - Description of vulnerability
   - Steps to reproduce
   - Potential impact
   - Suggested fix (if any)

We aim to respond within 24 hours.

---

## Security Best Practices Summary

### ✅ Implemented

- Environment variable configuration
- Restricted CORS origins
- Non-root Docker user
- Thread-safe operations
- JWT authentication
- Rate limiting
- Input validation (Pydantic)
- SQL injection prevention (SQLAlchemy ORM)

### 🔄 Recommended for Production

- HTTPS/TLS termination
- Database connection SSL
- Per-user rate limiting
- Audit logging
- Secrets management service
- Automated security scanning
- Backup and disaster recovery
- Penetration testing

---

## Additional Resources

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [FastAPI Security](https://fastapi.tiangolo.com/tutorial/security/)
- [Docker Security Best Practices](https://docs.docker.com/develop/security-best-practices/)
- [PostgreSQL Security](https://www.postgresql.org/docs/current/security.html)

---

**Last Updated**: February 5, 2026
**Security Version**: 2.1
