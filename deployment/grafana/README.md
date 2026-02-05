# Grafana Configuration

This directory contains Grafana configuration files for the NBA Prediction API monitoring stack.

## Directory Structure

- `dashboards/` - Dashboard JSON files (currently empty - configure manually)
- `datasources/` - Datasource YAML files (currently empty - configure manually)

## Setup Instructions

### Option 1: Manual Configuration (Recommended for Learning)

1. Start the stack: `docker-compose up -d`
2. Access Grafana at http://localhost:3000
3. Login with default credentials:
   - Username: `admin`
   - Password: See `docker-compose.yml` (default: `admin_password_change_in_production`)
4. Add Prometheus datasource manually:
   - URL: `http://prometheus:9090`
5. Create custom dashboards for your metrics

### Option 2: Pre-configured Dashboards (Coming Soon)

Pre-configured dashboards for the NBA Prediction API will be added in a future release.

## Metrics Available

The API exposes the following metrics at `/api/metrics`:

- `predictions_total` - Total number of predictions made
- `errors_total` - Total number of errors
- `cache_hits` - Cache hit count (when Redis is integrated)
- `cache_misses` - Cache miss count (when Redis is integrated)
- `cache_hit_rate` - Calculated cache hit rate
- `models_loaded` - Number of models currently loaded
- `uptime_seconds` - API uptime

## Common Queries

```promql
# Requests per second
rate(predictions_total[5m])

# Error rate
rate(errors_total[5m]) / rate(predictions_total[5m])

# P95 latency (when histogram metrics added)
histogram_quantile(0.95, rate(request_duration_seconds_bucket[5m]))
```

## Resources

- [Grafana Documentation](https://grafana.com/docs/)
- [Prometheus Query Examples](https://prometheus.io/docs/prometheus/latest/querying/examples/)
