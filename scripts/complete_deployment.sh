#!/bin/bash
# NBA Performance Prediction - Complete Deployment Script
# This script completes the Railway deployment

set -e

echo "========================================="
echo "rocket.fill NBA Performance Prediction Deployment"
echo "========================================="
echo ""

PROJECT_ID="502c137a-1a48-4903-a396-6ecf23965758"
GITHUB_REPO="https://github.com/calebnewtonusc/NBA-Performance-Prediction"

echo "checkmark.circle.fill Already completed:"
echo "  - GitHub repository created: $GITHUB_REPO"
echo "  - Railway project created: insightful-heart"
echo "  - PostgreSQL database added"
echo "  - Redis cache added"
echo "  - Environment variables set"
echo ""

echo "🔄 Finding your API service..."
cd "$(dirname "$0")/.."

# Try to find and link to the main API service
echo "Linking to Railway project..."
railway link --project $PROJECT_ID 2>/dev/null || true

# List all services to find the API one
echo ""
echo "📋 Railway Services in your project:"
echo "(Looking for your API service - not Postgres or Redis)"
echo ""

# Generate domain for the API service
echo "exclamationmark.triangle.fill  MANUAL STEP REQUIRED:"
echo ""
echo "1. Open Railway dashboard: https://railway.com/project/$PROJECT_ID"
echo "2. Find your API service (the one with your code, NOT Postgres/Redis)"
echo "3. Click on the service"
echo "4. Go to Settings → Networking"
echo "5. Click 'Generate Domain'"
echo "6. Copy the generated URL"
echo ""
read -p "Enter your Railway API URL (e.g., nba-api-production.up.railway.app): " RAILWAY_URL

if [ -z "$RAILWAY_URL" ]; then
    echo "xmark.circle.fill No URL provided. Exiting."
    exit 1
fi

# Add https:// if not present
if [[ ! $RAILWAY_URL =~ ^https?:// ]]; then
    RAILWAY_URL="https://$RAILWAY_URL"
fi

echo ""
echo "checkmark.circle.fill Railway URL: $RAILWAY_URL"
echo ""

# Test the health endpoint
echo "🧪 Testing Railway API..."
sleep 2
if curl -f -s "$RAILWAY_URL/api/health" > /dev/null 2>&1; then
    echo "checkmark.circle.fill API is healthy!"
    curl -s "$RAILWAY_URL/api/health" | python3 -m json.tool
else
    echo "exclamationmark.triangle.fill  API not responding yet. This is normal if deployment is still in progress."
    echo "Wait 1-2 minutes and try: curl $RAILWAY_URL/api/health"
fi

echo ""
echo "========================================="
echo "pencil STREAMLIT CLOUD SETUP"
echo "========================================="
echo ""
echo "1. Open Streamlit Cloud: https://share.streamlit.io"
echo "2. Click 'New app'"
echo "3. Select repository: calebnewtonusc/NBA-Performance-Prediction"
echo "4. Branch: main"
echo "5. Main file: src/visualization/dashboard.py"
echo "6. Click 'Advanced settings...'"
echo "7. In Secrets section, paste this TOML:"
echo ""
echo "---"
cat << EOF
API_BASE_URL = "$RAILWAY_URL"
API_USERNAME = "admin"
API_PASSWORD = "G9.zs8FGHP1W_lx^5eP,}mU2"
EOF
echo "---"
echo ""
echo "8. Click 'Deploy!'"
echo "9. Wait 2-3 minutes for deployment"
echo ""
read -p "Enter your Streamlit URL (e.g., nba-dashboard.streamlit.app): " STREAMLIT_URL

if [ -z "$STREAMLIT_URL" ]; then
    echo "exclamationmark.triangle.fill  No Streamlit URL provided. Skipping CORS update."
    echo "   Update CORS later in Railway with:"
    echo "   railway variables set ALLOWED_ORIGINS=\"https://YOUR-APP.streamlit.app,http://localhost:8501\""
    exit 0
fi

# Add https:// if not present
if [[ ! $STREAMLIT_URL =~ ^https?:// ]]; then
    STREAMLIT_URL="https://$STREAMLIT_URL"
fi

echo ""
echo "checkmark.circle.fill Streamlit URL: $STREAMLIT_URL"
echo ""

# Update CORS in Railway
echo "🔄 Updating CORS in Railway..."
railway link --project $PROJECT_ID 2>/dev/null || true

# Find and link to the API service (not Postgres/Redis)
echo "Updating ALLOWED_ORIGINS..."
railway variables set ALLOWED_ORIGINS="$STREAMLIT_URL,http://localhost:8501" 2>/dev/null || {
    echo "exclamationmark.triangle.fill  Could not automatically update CORS."
    echo "   Please manually set in Railway:"
    echo "   ALLOWED_ORIGINS=$STREAMLIT_URL,http://localhost:8501"
}

echo ""
echo "========================================="
echo "party.popper.fill DEPLOYMENT COMPLETE!"
echo "========================================="
echo ""
echo "Your live URLs:"
echo "  chart.bar.fill Dashboard: $STREAMLIT_URL"
echo "  powerplug.fill API: $RAILWAY_URL"
echo "  book.fill API Docs: $RAILWAY_URL/api/docs"
echo "  heart.fill Health: $RAILWAY_URL/api/health"
echo "  laptopcomputer GitHub: $GITHUB_REPO"
echo ""
echo "========================================="
echo "🧪 FINAL TESTS"
echo "========================================="
echo ""
echo "Run these commands to verify everything works:"
echo ""
echo "# Test backend health"
echo "curl $RAILWAY_URL/api/health"
echo ""
echo "# Test backend login"
echo "curl -X POST $RAILWAY_URL/api/auth/login \\"
echo "  -H 'Content-Type: application/json' \\"
echo "  -d '{\"username\": \"admin\", \"password\": \"G9.zs8FGHP1W_lx^5eP,}mU2\"}'"
echo ""
echo "# Open dashboard"
echo "open $STREAMLIT_URL"
echo ""
echo "# Open API docs"
echo "open $RAILWAY_URL/api/docs"
echo ""
echo "========================================="
echo "🔐 SECURITY REMINDER"
echo "========================================="
echo ""
echo "DELETE these files now that deployment is complete:"
echo "  - DEPLOYMENT_SECRETS.txt"
echo "  - This setup script (optional)"
echo ""
echo "rm DEPLOYMENT_SECRETS.txt"
echo ""
echo "checkmark.circle.fill All done! Your NBA Prediction system is live!"
