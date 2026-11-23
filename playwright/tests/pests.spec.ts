import { test, expect } from '@playwright/test';

test('pests page', async ({ page}) => {
  //-----------------------------------------------------------------------
  // Go to Home page (uses baseURL from playwright.config.ts)
  //-----------------------------------------------------------------------
  await page.goto('/');
  //-----------------------------------------------------------------------
  // Go to Pests page
  //-----------------------------------------------------------------------
  await page.getByRole('link', { name: 'Pests', exact: true }).click();
  await expect(page).toHaveURL('pest_summary/');
  await expect(page).toHaveTitle('Gateway Gardens | Pest Summary')
  //-----------------------------------------------------------------------
  // Go to Add Pest page
  //-----------------------------------------------------------------------
  // Open the 'Pest' drop-down menu
  await page.getByRole('button', { name: 'menu', exact: true }).hover();
  // Open the 'Add Pest' page and check that it was navigated to
  await page.getByRole('link', { name: 'Add Pest', exact: true }).click();

  // await expect(page).toHaveURL(^[^/]+/pest_edit/\d+/$);
  
  await expect(page).toHaveTitle('Gateway Gardens | Pest Edit');
  // Populate the input fields

  //-----------------------------------------------------------------------

  // await page.pause();
  
});