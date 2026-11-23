import { test as setup, expect } from '@playwright/test';
import path from 'path';

const authFile = path.join(__dirname, '../playwright/.auth/user.json');

setup('authenticate', async ({ page }) => {

    const username = process.env.TEST_USERNAME;
    const password = process.env.TEST_PASSWORD;

    if (!username || !password) {
        throw new Error('TEST_USERNAME and TEST_PASSWORD must be set in .env');
    }
    //-----------------------------------------------------------------------
    // Go to Home page (uses baseURL from playwright.config.ts)
    //-----------------------------------------------------------------------
    await page.goto('/');
    //-----------------------------------------------------------------------
    // Perform authentication steps
    //-----------------------------------------------------------------------
    // Open the 'Account drop-down menu'
    await page.getByRole('button', { name: 'Account' }).hover();
    // Open the login modal
    await page.getByRole('button', { name: 'Login' }).click();
    // Assert that the login modal is visible
    const loginModal = page.locator('#login_modal');
    await expect(loginModal).toBeVisible();
    // Fill in the username and password
    await page.getByLabel('Username').fill(username);
    await page.getByLabel('Password').fill(password);
    // Log in the user
    await page.locator('#id_login_button').click();
    // Assert that the login modal is hidden
    await expect(loginModal).toBeHidden();
    
    //
    await page.context().storageState({ path: authFile });

    // await page.pause();
});