# Rollback & Deployment Procedures

## 🚨 Emergency Rollback Guide

### Quick Rollback Checklist

If you need to rollback immediately:

1. ✅ **Identify the deployment platform** (Railway backend, Vercel frontend)
2. ✅ **Locate the last known good commit/deployment**
3. ✅ **Execute rollback commands** (see below)
4. ✅ **Verify service health**
5. ✅ **Notify team and create incident report**

---

## Backend Rollback (Railway)

### Option 1: Railway Dashboard (Fastest)

1. Go to [Railway Dashboard](https://railway.app/dashboard)
2. Select your NBA Prediction API project
3. Click "Deployments" tab
4. Find the last successful deployment (marked with ✅)
5. Click "..." menu → "Redeploy"
6. Wait for deployment to complete (usually 2-3 minutes)
7. Verify: `curl https://nba-performance-prediction-production.up.railway.app/api/health`

### Option 2: Git Rollback

```bash
# 1. Find the last good commit
git log --oneline -10

# 2. Create a revert commit
git revert <bad-commit-hash>

# 3. Push to trigger auto-deployment
git push origin main

# 4. Monitor Railway deployment
# Railway auto-deploys from GitHub pushes
```

### Option 3: Docker Rollback (Local/Self-Hosted)

```bash
# 1. List recent images
docker images nba-api --format "table {{.Repository}}\t{{.Tag}}\t{{.CreatedAt}}"

# 2. Stop current container
docker stop nba-api
docker rm nba-api

# 3. Run previous version
docker run -d --name nba-api \
  -p 8000:8000 \
  --env-file .env \
  nba-api:<previous-tag>

# 4. Verify health
curl http://localhost:8000/api/health
```

---

## Frontend Rollback (Vercel)

### Option 1: Vercel Dashboard (Fastest)

1. Go to [Vercel Dashboard](https://vercel.com/dashboard)
2. Select NBA Performance Prediction project
3. Click "Deployments" tab
4. Find last successful deployment
5. Click "..." menu → "Promote to Production"
6. Verify: Visit https://nba-performance-prediction.vercel.app

### Option 2: Git Rollback

```bash
# 1. Rollback frontend code
cd frontend/
git revert <bad-commit-hash>
git push origin main

# Vercel auto-deploys from GitHub pushes
```

---

## Database Rollback (Alembic)

### Rollback Last Migration

```bash
# 1. Connect to production database (use READ REPLICA if available)
export DATABASE_URL="postgresql://user:pass@host:5432/nba_predictions"

# 2. Check current migration
alembic current

# 3. Rollback one migration
alembic downgrade -1

# 4. Verify database state
psql $DATABASE_URL -c "SELECT version_num FROM alembic_version;"
```

### Rollback to Specific Version

```bash
# Rollback to specific migration
alembic downgrade <revision-id>

# Example: Rollback to baseline
alembic downgrade base
```

⚠️ **WARNING**: Database rollbacks can cause data loss. Always:
- Create a backup before rolling back
- Test on staging first
- Coordinate with team during business hours

---

## Model Rollback

### Rollback to Previous Model Version

```bash
# 1. SSH into production server or Railway shell
railway run bash

# 2. List available models
ls -l models/

# 3. Update model symlinks or version in code
# Option A: Use environment variable
export MODEL_VERSION="v1.0.0"

# Option B: Swap model files
cd models/
mv game_logistic/v1/model.pkl game_logistic/v1/model.pkl.broken
mv game_logistic/v1/model.pkl.backup game_logistic/v1/model.pkl

# 3. Restart API
railway up
```

---

## Health Check Commands

### Backend Health

```bash
# Production
curl https://nba-performance-prediction-production.up.railway.app/api/health

# Expected response:
# {"status":"healthy","timestamp":"...","uptime_seconds":123,"models_loaded":6,"version":"1.0.0"}
```

### Frontend Health

```bash
# Production
curl -I https://nba-performance-prediction.vercel.app

# Expected: HTTP/2 200
```

### Database Health

```bash
# Check connection
psql $DATABASE_URL -c "SELECT NOW();"

# Check table counts
psql $DATABASE_URL -c "SELECT COUNT(*) FROM predictions;"
```

### Redis Cache Health

```bash
# Connect to Redis
redis-cli -h <redis-host> -p 6379

# Check connection
PING
# Expected: PONG

# Check stats
INFO stats
```

---

## Incident Response Workflow

### 1. Detection (0-5 minutes)

- Monitor alerts (Sentry, PagerDuty, uptime monitors)
- Check error logs
- Verify user reports

### 2. Assessment (5-10 minutes)

- **Severity Level**:
  - P0 (Critical): Complete outage, data loss
  - P1 (High): Partial outage, critical feature down
  - P2 (Medium): Performance degradation
  - P3 (Low): Minor bug, workaround available

- **Impact**:
  - How many users affected?
  - Which features are broken?
  - Is data at risk?

### 3. Decision (10-15 minutes)

**Should we rollback?**

✅ **YES, rollback if**:
- Complete service outage
- Data corruption/loss
- Security vulnerability
- No quick fix available

❌ **NO, forward fix if**:
- Minor bug with workaround
- Fix is simple and tested
- Rollback would cause more issues

### 4. Execution (15-25 minutes)

- Execute rollback (see procedures above)
- Monitor metrics during rollback
- Verify health checks pass

### 5. Communication (Throughout)

```
[INCIDENT] NBA API Rollback - P1

Status: IN PROGRESS
Impact: Predictions endpoint returning 500 errors
Action: Rolling back to deployment #234 (commit abc123)
ETA: 5 minutes

Updates:
- 14:32 - Incident detected
- 14:35 - Rollback initiated
- 14:40 - Rollback complete, verifying
- 14:45 - All systems healthy ✅

Root Cause: [To be determined in post-mortem]
```

### 6. Post-Mortem (Within 24 hours)

Create incident report:

```markdown
## Incident Report: [Date]

**Title**: [Brief description]
**Severity**: P1
**Duration**: 13 minutes (14:32 - 14:45 UTC)
**Impact**: 150 failed prediction requests

### Timeline
- 14:30 - Deployed v1.2.3 with new caching logic
- 14:32 - Error rate spike to 45%
- 14:35 - Rollback decision made
- 14:40 - Rollback completed
- 14:45 - Service fully recovered

### Root Cause
Redis connection timeout not handled gracefully in new code

### Resolution
Rolled back to v1.2.2

### Action Items
- [ ] Add Redis connection retry logic
- [ ] Improve staging test coverage
- [ ] Add Redis failover monitoring
- [ ] Update runbook with this case

### Lessons Learned
- Need better Redis error handling
- Staging didn't catch this (no Redis failures tested)
```

---

## Monitoring & Alerts

### Key Metrics to Watch

```bash
# Error rate
watch -n 5 'curl -s https://api.example.com/api/metrics | jq .errors_total'

# Response time
# Use your APM (Datadog, New Relic, etc.)

# Uptime
# Use external monitor (Pingdom, UptimeRobot)
```

### Set Up Alerts

1. **Error Rate Spike**: Errors > 5% of requests for 2 minutes
2. **Response Time**: P95 latency > 1000ms for 5 minutes
3. **Downtime**: Health check fails for 1 minute
4. **Database Connection**: Connection pool exhausted

---

## Pre-Deployment Checklist

Before ANY production deployment:

- [ ] Code reviewed and approved
- [ ] All tests pass (unit, integration, e2e)
- [ ] Tested on staging environment
- [ ] Database migrations tested
- [ ] Rollback plan documented
- [ ] Team notified of deployment window
- [ ] Monitoring dashboards open
- [ ] Backup of current production data
- [ ] Deployment during low-traffic window

---

## Emergency Contacts

**On-Call Rotation**: [Link to PagerDuty schedule]
**Incident Slack Channel**: #nba-api-incidents
**Status Page**: [status.example.com]

---

## Useful Commands

```bash
# Check recent deployments
gh api repos/yourusername/NBA-Performance-Prediction/deployments | jq '.[0:5]'

# View logs (Railway)
railway logs

# View logs (Docker)
docker logs -f --tail 100 nba-api

# Database backup
pg_dump $DATABASE_URL > backup_$(date +%Y%m%d_%H%M%S).sql

# Restore database
psql $DATABASE_URL < backup_20260206_143000.sql
```

---

## Testing Rollback Procedures

**Schedule quarterly rollback drills:**

1. Pick a random deployment from last week
2. Practice rolling back
3. Time how long it takes
4. Update procedures based on learnings
5. Ensure new team members practice too

**Remember**: The best time to test your rollback is BEFORE you need it!
