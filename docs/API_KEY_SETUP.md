# NBA API Key Setup Guide

## Overview

This application uses the [balldontlie.io](https://www.balldontlie.io) NBA API to fetch real-time NBA data including player statistics, game results, and team information.

**An API key is required** to access NBA data. This guide walks you through obtaining and configuring your API key.

## Getting Your API Key

### Step 1: Create a Free Account

1. Visit [https://app.balldontlie.io](https://app.balldontlie.io)
2. Click "Sign Up" to create a free account
3. Verify your email address

### Step 2: Generate API Key

1. Log in to your balldontlie.io dashboard
2. Navigate to the API Keys section
3. Click "Create API Key"
4. Copy your API key (you'll need this for configuration)

### Step 3: Configure Your Application

Add your API key to the `.env` file in the project root:

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env and add your API key
BALLDONTLIE_API_KEY=your_actual_api_key_here
```

**Important:** Never commit your `.env` file to version control. The `.gitignore` file should already exclude it.

## API Key Tiers

balldontlie.io offers different API tiers:

| Tier      | Requests/Minute | Cost       | Best For                |
|-----------|-----------------|------------|-------------------------|
| Free      | 5               | $0/month   | Development & Testing   |
| ALL-STAR  | 60              | $9.99/mo   | Small Production Apps   |
| GOAT      | 600             | $39.99/mo  | High-Traffic Apps       |

The free tier is sufficient for development and small-scale use.

## Rate Limiting

Our application automatically handles rate limiting:

- **Free tier:** 5 requests per minute (12-second delay between requests)
- Requests are automatically spaced out to avoid hitting rate limits
- If you exceed the limit, you'll receive a clear error message

## Troubleshooting

### Error: "balldontlie.io API key is required"

**Cause:** No API key is configured

**Solution:**
1. Verify `BALLDONTLIE_API_KEY` is set in your `.env` file
2. Restart the API server after adding the key
3. Check that the `.env` file is in the project root directory

### Error: "Invalid API key for balldontlie.io"

**Cause:** The API key is incorrect or expired

**Solution:**
1. Log in to https://app.balldontlie.io
2. Verify your API key is active
3. Generate a new API key if needed
4. Update the `BALLDONTLIE_API_KEY` in your `.env` file

### Error: "Rate limit exceeded"

**Cause:** Too many requests in a short time

**Solution:**
- **Free tier:** Wait 1 minute before making more requests
- **Upgrade:** Consider upgrading to a higher tier for more requests
- The application will automatically retry after the rate limit resets

## Environment Variables Reference

```bash
# Required for NBA data access
BALLDONTLIE_API_KEY=your_api_key_here

# Optional: Override default base URL (advanced use only)
# BALLDONTLIE_BASE_URL=https://api.balldontlie.io/v1
```

## Testing Your API Key

You can test your API key configuration by running:

```bash
# From the project root
python -c "
import os
from dotenv import load_dotenv
from src.data_collection.player_data import PlayerDataCollector

load_dotenv()
api_key = os.getenv('BALLDONTLIE_API_KEY')

if not api_key:
    print('✗ API key not found in .env file')
else:
    print(f'✓ API key found: {api_key[:10]}...')
    try:
        collector = PlayerDataCollector(api_key=api_key)
        result = collector.search_players('LeBron James')
        if result['players']:
            print(f'✓ API key works! Found {len(result[\"players\"])} players')
        else:
            print('⚠ API key works but no results returned')
    except Exception as e:
        print(f'✗ API test failed: {e}')
"
```

Expected output for a valid API key:
```
✓ API key found: sk_abc1234...
✓ API key works! Found 1 players
```

## Security Best Practices

1. **Never commit API keys to version control**
   - The `.env` file is gitignored by default
   - Use `.env.example` for documentation

2. **Use environment variables in production**
   - Railway, Heroku, Vercel, etc. all support environment variables
   - Configure `BALLDONTLIE_API_KEY` in your deployment platform

3. **Rotate keys periodically**
   - Generate new API keys every 90 days
   - Revoke old keys after updating

4. **Monitor usage**
   - Check your balldontlie.io dashboard regularly
   - Set up alerts for unusual activity

## Support

- **balldontlie.io Documentation:** https://docs.balldontlie.io
- **API Status:** https://status.balldontlie.io
- **Support:** support@balldontlie.io

## Alternative Data Sources

If you need higher rate limits or different data, consider these alternatives:

- **NBA Stats API:** https://stats.nba.com (unofficial, no auth required)
- **SportsData.io:** https://sportsdata.io (premium, comprehensive)
- **RapidAPI NBA APIs:** https://rapidapi.com/hub/nba (multiple providers)

**Note:** This application is currently optimized for balldontlie.io. Using alternative APIs will require code modifications.
