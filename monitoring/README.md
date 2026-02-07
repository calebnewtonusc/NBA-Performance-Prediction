# NBA Prediction API Monitoring

Complete monitoring stack using Prometheus and Grafana.

## Overview

This monitoring setup provides:
- **Prometheus**: Metrics collection and time-series database
- **Grafana**: Visualization dashboards
- **Redis Exporter**: Redis cache metrics
- **PostgreSQL Exporter**: Database metrics
- **Node Exporter**: System-level metrics

## Quick Start

### 1. Start Monitoring Stack

```bash
cd monitoring
docker-compose -f docker-compose.monitoring.yml up -d
```

### 2. Access Dashboards

- **Grafana**: http://localhost:3000
  - Username: `admin`
  - Password: `admin` (change in production!)

- **Prometheus**: http://localhost:9090

### 3. Configure API Token

Update `prometheus.yml` with your API authentication token:

```yaml
scrape_configs:
  - job_name: 'nba-api'
    bearer_token: 'YOUR_ACTUAL_TOKEN_HERE'
```

Then restart Prometheus:

```bash
docker-compose -f docker-compose.monitoring.yml restart prometheus
```

## Metrics Exposed

### API Metrics (`/api/v1/metrics`)

- `api_requests_total` - Total API requests
- `api_errors_total` - Total API errors
- `api_request_duration_seconds` - Request duration histogram
- `predictions_total` - Total predictions made
- `cache_hits_total` - Cache hit count
- `cache_misses_total` - Cache miss count
- `models_loaded_total` - Number of loaded models

### Model Performance Metrics

- `model_accuracy` - Current model accuracy
- `model_drift_score` - Data drift score
- `model_predictions_correct` - Correct predictions count
- `model_predictions_incorrect` - Incorrect predictions count

### Infrastructure Metrics

- **Redis**: Connection stats, memory usage, commands/sec
- **PostgreSQL**: Active connections, queries, cache hit ratio
- **System**: CPU, memory, disk usage, network I/O

## Alerts

Configured alerts in `alert_rules.yml`:

### Critical Alerts
- `APIDown` - API is unreachable for >2 minutes
- `DatabaseConnectionFailed` - >5 DB connection failures in 5 minutes

### Warning Alerts
- `HighErrorRate` - Error rate >0.1 errors/sec for 5 minutes
- `HighResponseTime` - Average response time >2s for 5 minutes
- `ModelAccuracyDrop` - Accuracy <60% for 10 minutes
- `CacheUnavailable` - Redis unavailable for >2 minutes
- `HighMemoryUsage` - Available memory <10%
- `DiskSpaceLow` - Available disk space <10%

## Dashboard Panels

The Grafana dashboard (`grafana-dashboard.json`) includes:

1. **API Request Rate** - Requests per second over time
2. **Prediction Accuracy** - Model accuracy trend
3. **Response Time (p95)** - 95th percentile latency
4. **Error Rate** - Errors per second
5. **Cache Hit Rate** - Percentage of cache hits
6. **Models Loaded** - Number of active models
7. **Database Connections** - Active vs idle connections
8. **Model Drift Score** - Data drift detection

## Customization

### Add Custom Metrics

In your API code:

```python
from prometheus_client import Counter, Histogram, Gauge

# Define custom metrics
custom_counter = Counter('custom_metric_total', 'Description')
custom_histogram = Histogram('custom_duration_seconds', 'Description')
custom_gauge = Gauge('custom_value', 'Description')

# Use in code
custom_counter.inc()
custom_histogram.observe(1.5)
custom_gauge.set(42)
```

### Add Custom Alerts

Edit `alert_rules.yml`:

```yaml
- alert: CustomAlert
  expr: custom_metric_total > 100
  for: 5m
  labels:
    severity: warning
  annotations:
    summary: "Custom alert triggered"
    description: "Custom metric exceeded threshold."
```

### Modify Dashboard

1. Access Grafana at http://localhost:3000
2. Navigate to Dashboards → NBA Prediction API Monitoring
3. Click "Edit" to modify panels
4. Save and export JSON to `grafana-dashboard.json`

## Production Deployment

### Security

1. **Change default passwords**:
   ```yaml
   # docker-compose.monitoring.yml
   environment:
     - GF_SECURITY_ADMIN_PASSWORD=YOUR_SECURE_PASSWORD
   ```

2. **Enable HTTPS** for Grafana:
   ```yaml
   environment:
     - GF_SERVER_PROTOCOL=https
     - GF_SERVER_CERT_FILE=/path/to/cert.pem
     - GF_SERVER_CERT_KEY=/path/to/key.pem
   ```

3. **Restrict access** with firewall rules

### Data Retention

Configure Prometheus retention in `docker-compose.monitoring.yml`:

```yaml
command:
  - '--storage.tsdb.retention.time=30d'  # Keep 30 days
  - '--storage.tsdb.retention.size=10GB'  # Max 10GB
```

### Backup

Backup Prometheus data:

```bash
docker run --rm -v prometheus-data:/data -v $(pwd):/backup \
  alpine tar czf /backup/prometheus-backup.tar.gz /data
```

Backup Grafana dashboards:

```bash
docker run --rm -v grafana-data:/data -v $(pwd):/backup \
  alpine tar czf /backup/grafana-backup.tar.gz /data
```

## Troubleshooting

### Prometheus not scraping API

1. Check API is accessible from Prometheus container
2. Verify bearer token is correct
3. Check Prometheus logs:
   ```bash
   docker logs nba-prometheus
   ```

### Grafana dashboard empty

1. Verify Prometheus is running and has data
2. Check Grafana data source configuration
3. Ensure time range is appropriate

### High memory usage

Reduce Prometheus retention or increase container memory:

```yaml
deploy:
  resources:
    limits:
      memory: 2G
```

## Monitoring Stack Commands

```bash
# Start all services
docker-compose -f docker-compose.monitoring.yml up -d

# View logs
docker-compose -f docker-compose.monitoring.yml logs -f

# Stop all services
docker-compose -f docker-compose.monitoring.yml down

# Stop and remove volumes (WARNING: deletes all metrics data)
docker-compose -f docker-compose.monitoring.yml down -v

# Restart specific service
docker-compose -f docker-compose.monitoring.yml restart prometheus

# View service status
docker-compose -f docker-compose.monitoring.yml ps
```

## Integration with Alertmanager

For production alerting (email, Slack, PagerDuty):

1. Add Alertmanager service to `docker-compose.monitoring.yml`
2. Configure alert routing in `alertmanager.yml`
3. Update `prometheus.yml` with Alertmanager target

Example Slack integration:

```yaml
# alertmanager.yml
receivers:
  - name: 'slack'
    slack_configs:
      - api_url: 'YOUR_SLACK_WEBHOOK_URL'
        channel: '#alerts'
        text: '{{ range .Alerts }}{{ .Annotations.description }}{{ end }}'
```

## Resources

- [Prometheus Documentation](https://prometheus.io/docs/)
- [Grafana Documentation](https://grafana.com/docs/)
- [PromQL Query Language](https://prometheus.io/docs/prometheus/latest/querying/basics/)

## Support

For issues or questions about the monitoring setup, check:
1. Service logs with `docker-compose logs`
2. Prometheus targets at http://localhost:9090/targets
3. Grafana data sources at http://localhost:3000/datasources
