import { test, expect } from '@playwright/test';

test('login test user', async ({ page}) => {
    //-----------------------------------------------------------------------
    // Go to Home page (uses baseURL from playwright.config.ts)
    //-----------------------------------------------------------------------
    // Development server
    await page.goto('/');

    // Production server
    // await page.goto('https://plants.fd8jte0qsatv2.us-east-1.cs.amazonlightsail.com/');
    
    await expect(page).toHaveURL('/');
    await expect(page).toHaveTitle('Gateway Gardens | Home')
    //-----------------------------------------------------------------------
    // Go to My Garden page
    //-----------------------------------------------------------------------
    await page.getByRole('link', { name: 'My Garden', exact: true }).click();
    await expect(page).toHaveURL('mygarden_summary/');
    await expect(page).toHaveTitle('Gateway Gardens | My Garden Summary')
    //-----------------------------------------------------------------------
    // Go to My Garden Plan page
    //-----------------------------------------------------------------------
    await page.getByRole('link', { name: 'My Garden Plan', exact: true }).click();
    await expect(page).toHaveURL('mygarden_plan/');
    await expect(page).toHaveTitle('Gateway Gardens | My Garden Plan')
    //-----------------------------------------------------------------------
    // Go to My ToDo's page
    //-----------------------------------------------------------------------
    await page.getByRole('link', { name: "My ToDo's", exact: true }).click();
    await expect(page).toHaveURL('mygarden_todo/');
    await expect(page).toHaveTitle('Gateway Gardens | My ToDo\'s')
    //-----------------------------------------------------------------------
    // Go to My Plants page
    //-----------------------------------------------------------------------
    await page.getByRole('link', { name: 'My Plants', exact: true }).click();
    await expect(page).toHaveURL('myplants_summary/');
    await expect(page).toHaveTitle('Gateway Gardens | My Plants Summary')
    //-----------------------------------------------------------------------
    // Go to Plants page
    //-----------------------------------------------------------------------
    await page.getByRole('link', { name: 'Plants', exact: true }).click();
    await expect(page).toHaveURL('plants_summary/');
    await expect(page).toHaveTitle('Gateway Gardens | Plant Summary')
    //-----------------------------------------------------------------------
    // Go to Pests page
    //-----------------------------------------------------------------------
    await page.getByRole('link', { name: 'Pests', exact: true }).click();
    await expect(page).toHaveURL('pest_summary/');
    await expect(page).toHaveTitle('Gateway Gardens | Pest Summary')
    //-----------------------------------------------------------------------
    // Go to Glossary page
    //-----------------------------------------------------------------------
    await page.getByRole('link', { name: 'Glossary', exact: true }).click();
    await expect(page).toHaveURL('glossary/');
    await expect(page).toHaveTitle('Gateway Gardens | Glossary')
    //-----------------------------------------------------------------------
    // Go to Reference page
    //-----------------------------------------------------------------------
    await page.getByRole('link', { name: 'Reference', exact: true }).click();
    await expect(page).toHaveURL('reference/');
    await expect(page).toHaveTitle('Gateway Gardens | Reference')
    //-----------------------------------------------------------------------
    // Go to About page
    //-----------------------------------------------------------------------
    await page.getByRole('link', { name: 'About', exact: true }).click();
    await expect(page).toHaveURL('about/');
    await expect(page).toHaveTitle('Gateway Gardens | About')
    //-----------------------------------------------------------------------

    // await page.pause()
  
});