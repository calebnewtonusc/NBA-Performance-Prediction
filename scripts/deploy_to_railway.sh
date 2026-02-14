#!/bin/bash
# Deploy NBA Prediction API to Railway via CLI

set -e

PROJECT_ID="502c137a-1a48-4903-a396-6ecf23965758"

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "rocket.fill Deploying to Railway"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

cd "$(dirname "$0")/.."

echo "1️⃣  Linking to Railway project..."
railway link --project $PROJECT_ID --environment production 2>&1 | grep -i "success\|linked" || echo "Already linked"

echo ""
echo "2️⃣  Uploading code to Railway service 'nba-api'..."
echo "    (This will take 2-3 minutes)"
echo ""

railway up --service nba-api --detach

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "checkmark.circle.fill Upload Complete!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Railway is now building your Docker image."
echo "This takes ~2-3 minutes."
echo ""
echo "Next steps:"
echo "1. Go to: https://railway.com/project/$PROJECT_ID"
echo "2. Click on 'nba-api' service"
echo "3. Go to 'Deployments' tab"
echo "4. Wait for 'SUCCESS' status"
echo "5. Go to 'Settings' → 'Networking'"
echo "6. Click 'Generate Domain'"
echo "7. Copy your API URL"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
read -p "Press Enter to open Railway dashboard..."

open "https://railway.com/project/$PROJECT_ID" 2>/dev/null || \
  echo "Open: https://railway.com/project/$PROJECT_ID"

echo ""
echo "checkmark.circle.fill Deployment initiated!"
