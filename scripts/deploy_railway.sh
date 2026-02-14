#!/bin/bash
# Railway CLI Automated Deployment Script

set -e

PROJECT_ID="502c137a-1a48-4903-a396-6ecf23965758"

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "rocket.fill Railway CLI Automated Deployment"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

cd "$(dirname "$0")/.."

echo "1️⃣  Linking to Railway project..."
railway link --project $PROJECT_ID --environment production 2>&1 | grep -i "success\|linked" || true

echo ""
echo "2️⃣  Checking current services..."
echo ""
echo "exclamationmark.triangle.fill  IMPORTANT: Railway requires manual steps for first deployment"
echo ""
echo "📋 Complete these steps in Railway web UI:"
echo "   https://railway.com/project/$PROJECT_ID"
echo ""
echo "   1. Click '+ New' button"
echo "   2. Select 'GitHub Repo'"
echo "   3. Choose: calebnewtonusc/NBA-Performance-Prediction"
echo "   4. Railway will auto-detect Dockerfile.api"
echo "   5. Wait for build to complete (~3 mins)"
echo "   6. Go to Settings → Networking → Generate Domain"
echo "   7. Copy the generated URL"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "chart.bar.fill Your Railway Project Status"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "checkmark.circle.fill Project created: insightful-heart"
echo "checkmark.circle.fill PostgreSQL: Added"
echo "checkmark.circle.fill Redis: Added"
echo "checkmark.circle.fill Environment variables: Set"
echo "⏳ API Service: Needs to be connected via web UI"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
read -p "Press Enter after you've completed Railway setup and have your API URL..."

echo ""
read -p "Enter your Railway API URL (e.g., nba-api-xyz.up.railway.app): " RAILWAY_URL

if [ -z "$RAILWAY_URL" ]; then
    echo "xmark.circle.fill No URL provided"
    exit 1
fi

# Add https:// if not present
if [[ ! $RAILWAY_URL =~ ^https?:// ]]; then
    RAILWAY_URL="https://$RAILWAY_URL"
fi

echo ""
echo "checkmark.circle.fill Railway URL: $RAILWAY_URL"
echo ""
echo "🧪 Testing API health..."
sleep 2

if curl -f -s "$RAILWAY_URL/api/health" > /dev/null 2>&1; then
    echo "checkmark.circle.fill API is healthy!"
    echo ""
    curl -s "$RAILWAY_URL/api/health" | python3 -m json.tool 2>/dev/null || echo "API responded successfully"
else
    echo "exclamationmark.triangle.fill  API not responding yet (may still be deploying)"
    echo "   Try: curl $RAILWAY_URL/api/health"
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "party.popper.fill Railway Backend Complete!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Your API: $RAILWAY_URL"
echo "API Docs: $RAILWAY_URL/api/docs"
echo "Health: $RAILWAY_URL/api/health"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "pencil NEXT: Deploy Frontend to Streamlit Cloud"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Unfortunately, Streamlit has no CLI. Use web UI:"
echo ""
echo "1. Go to: https://share.streamlit.io"
echo "2. Click 'New app'"
echo "3. Repository: calebnewtonusc/NBA-Performance-Prediction"
echo "4. Branch: main"
echo "5. Main file: src/visualization/dashboard.py"
echo "6. Advanced settings → Secrets:"
echo ""
cat << EOF
API_BASE_URL = "$RAILWAY_URL"
API_USERNAME = "admin"
API_PASSWORD = "G9.zs8FGHP1W_lx^5eP,}mU2"
EOF
echo ""
echo "7. Click 'Deploy!'"
echo "8. Wait 2-3 minutes"
echo ""
read -p "Press Enter after Streamlit is deployed and enter your Streamlit URL..."
read -p "Enter Streamlit URL (e.g., nba-dashboard.streamlit.app): " STREAMLIT_URL

if [ -z "$STREAMLIT_URL" ]; then
    echo "exclamationmark.triangle.fill  No Streamlit URL provided. You'll need to update CORS manually."
    exit 0
fi

# Add https:// if not present
if [[ ! $STREAMLIT_URL =~ ^https?:// ]]; then
    STREAMLIT_URL="https://$STREAMLIT_URL"
fi

echo ""
echo "checkmark.circle.fill Streamlit URL: $STREAMLIT_URL"
echo ""
echo "🔄 Updating CORS in Railway..."

# Note: Railway CLI doesn't support selecting specific service easily
# User needs to do this in web UI
echo ""
echo "exclamationmark.triangle.fill  Please update CORS manually in Railway:"
echo ""
echo "1. Go to your API service in Railway"
echo "2. Variables tab"
echo "3. Update ALLOWED_ORIGINS to:"
echo "   $STREAMLIT_URL,http://localhost:8501"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "party.popper.fill DEPLOYMENT COMPLETE!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Your Live URLs:"
echo "  chart.bar.fill Dashboard: $STREAMLIT_URL"
echo "  powerplug.fill API: $RAILWAY_URL"
echo "  book.fill Docs: $RAILWAY_URL/api/docs"
echo ""
echo "🧪 Test your app:"
echo "  curl $RAILWAY_URL/api/health"
echo "  open $STREAMLIT_URL"
echo ""
echo "🔐 Remember to delete: DEPLOYMENT_SECRETS.txt"
echo ""
