import { test, expect } from '@playwright/test';

test.describe('NBA Predictions Flow', () => {
  test('should load homepage and display health status', async ({ page }) => {
    await page.goto('/');

    // Wait for health check to complete
    await page.waitForSelector('text=API Status', { timeout: 10000 });

    // Check that all health metrics are displayed
    await expect(page.locator('text=API Status')).toBeVisible();
    await expect(page.locator('text=Uptime')).toBeVisible();
    await expect(page.locator('text=Models Loaded')).toBeVisible();
    await expect(page.locator('text=Version')).toBeVisible();
  });

  test('should navigate to predictions page', async ({ page }) => {
    await page.goto('/');

    // Click on "Game Predictions" card
    await page.click('text=Game Predictions');

    // Wait for predictions page to load
    await expect(page).toHaveURL('/predictions');
    await expect(page.locator('h1:has-text("Game Predictions")')).toBeVisible();
  });

  test('should make a prediction', async ({ page }) => {
    await page.goto('/predictions');

    // Select home team (Boston Celtics)
    await page.selectOption('select >> nth=0', 'BOS');

    // Select away team (Los Angeles Lakers)
    await page.selectOption('select >> nth=1', 'LAL');

    // Click predict button
    await page.click('button:has-text("Get Prediction")');

    // Wait for loading to finish
    await page.waitForSelector('text=Fetching stats and predicting', { state: 'hidden', timeout: 15000 });

    // Check that prediction result is displayed
    await expect(page.locator('text=Wins with')).toBeVisible({ timeout: 10000 });
    await expect(page.locator('text=% confidence')).toBeVisible();

    // Check that probability chart is rendered
    await expect(page.locator('text=Win Probability')).toBeVisible();
  });

  test('should export predictions to CSV', async ({ page }) => {
    await page.goto('/predictions');

    // Make first prediction
    await page.selectOption('select >> nth=0', 'BOS');
    await page.selectOption('select >> nth=1', 'LAL');
    await page.click('button:has-text("Get Prediction")');
    await page.waitForSelector('text=Wins with', { timeout: 15000 });

    // Make second prediction
    await page.selectOption('select >> nth=0', 'GSW');
    await page.selectOption('select >> nth=1', 'MIA');
    await page.click('button:has-text("Get Prediction")');
    await page.waitForSelector('text=Wins with', { timeout: 15000 });

    // Check that export button appears
    await expect(page.locator('button:has-text("Export")')).toBeVisible();

    // Set up download handler
    const downloadPromise = page.waitForEvent('download');
    await page.click('button:has-text("Export")');
    const download = await downloadPromise;

    // Verify download
    expect(download.suggestedFilename()).toContain('predictions');
    expect(download.suggestedFilename()).toContain('.csv');
  });

  test('should display error for invalid prediction', async ({ page }) => {
    await page.goto('/predictions');

    // Try to predict with same team
    await page.selectOption('select >> nth=0', 'BOS');
    await page.selectOption('select >> nth=1', 'BOS');

    await page.click('button:has-text("Get Prediction")');

    // Should show error
    await expect(page.locator('text=Failed to get prediction')).toBeVisible({ timeout: 10000 });
  });

  test('should be responsive on mobile', async ({ page }) => {
    // Set mobile viewport
    await page.setViewportSize({ width: 375, height: 667 });

    await page.goto('/predictions');

    // Check that elements are visible and accessible
    await expect(page.locator('h1:has-text("Game Predictions")')).toBeVisible();
    await expect(page.locator('select').first()).toBeVisible();
    await expect(page.locator('button:has-text("Get Prediction")')).toBeVisible();
  });
});

test.describe('API Health and Navigation', () => {
  test('should navigate between pages', async ({ page }) => {
    await page.goto('/');

    // Navigate to each page
    const pages = [
      { link: 'Game Predictions', url: '/predictions' },
      { link: 'Player Analysis', url: '/players' },
      { link: 'Model Performance', url: '/performance' },
      { link: 'Data Explorer', url: '/explorer' },
    ];

    for (const { link, url } of pages) {
      await page.click(`text=${link}`);
      await expect(page).toHaveURL(url);
      await page.goBack();
    }
  });

  test('should handle API errors gracefully', async ({ page }) => {
    // Test with offline API (will timeout/error)
    await page.route('**/api/**', (route) => {
      route.abort();
    });

    await page.goto('/');

    // Should show error state or fallback
    await expect(
      page.locator('text=Failed to connect to API').or(page.locator('text=Failed to fetch health'))
    ).toBeVisible({ timeout: 10000 });
  });
});

test.describe('Accessibility', () => {
  test('should be keyboard navigable', async ({ page }) => {
    await page.goto('/predictions');

    // Tab through form elements
    await page.keyboard.press('Tab'); // First select
    await expect(page.locator('select').first()).toBeFocused();

    await page.keyboard.press('Tab'); // Second select
    await expect(page.locator('select').nth(1)).toBeFocused();

    await page.keyboard.press('Tab'); // Button
    await expect(page.locator('button:has-text("Get Prediction")')).toBeFocused();
  });

  test('should have proper ARIA labels', async ({ page }) => {
    await page.goto('/predictions');

    // Check for labels on form elements
    const homeLabel = page.locator('label:has-text("Home Team")');
    const awayLabel = page.locator('label:has-text("Away Team")');

    await expect(homeLabel).toBeVisible();
    await expect(awayLabel).toBeVisible();
  });
});
