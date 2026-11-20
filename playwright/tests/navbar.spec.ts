import { test, expect } from '@playwright/test';

test('login test user', async ({ page}) => {
  //-----------------------------------------------------------------------
  // Go to Home page
  //-----------------------------------------------------------------------
  await page.goto('http://127.0.0.1:8000/');
  // await page.goto('https://plants.fd8jte0qsatv2.us-east-1.cs.amazonlightsail.com/');
  let title = await page.title();
  expect(title).toContain('Gateway Gardens | Home');
  //-----------------------------------------------------------------------
  // Go to My Garden page
  //-----------------------------------------------------------------------
  await page.getByRole('link', { name: 'My Garden', exact: true }).click();
  title = await page.title();
  expect(title).toContain('Gateway Gardens | My Garden Summary');
  //-----------------------------------------------------------------------
  // Go to My Garden Plan page
  //-----------------------------------------------------------------------
  await page.getByRole('link', { name: 'My Garden Plan', exact: true }).click();
  title = await page.title();
  expect(title).toContain('Gateway Gardens | My Garden Plan');
  //-----------------------------------------------------------------------
  // Go to My ToDo's page
  //-----------------------------------------------------------------------
  await page.getByRole('link', { name: "My ToDo's", exact: true }).click();
  title = await page.title();
  expect(title).toContain("Gateway Gardens | My ToDo's");
  //-----------------------------------------------------------------------
  // Go to My Plants page
  //-----------------------------------------------------------------------
  await page.getByRole('link', { name: 'My Plants', exact: true }).click();
  title = await page.title();
  expect(title).toContain('Gateway Gardens | My Plants Summary');
  //-----------------------------------------------------------------------
  // Go to Plants page
  //-----------------------------------------------------------------------
  await page.getByRole('link', { name: 'Plants', exact: true }).click();
  title = await page.title();
  expect(title).toContain('Gateway Gardens | Plant Summary');
  //-----------------------------------------------------------------------
  // Go to Pests page
  //-----------------------------------------------------------------------
  await page.getByRole('link', { name: 'Pests', exact: true }).click();
  title = await page.title();
  expect(title).toContain('Gateway Gardens | Pest Summary');
  //-----------------------------------------------------------------------
  // Go to Glossary page
  //-----------------------------------------------------------------------
  await page.getByRole('link', { name: 'Glossary', exact: true }).click();
  title = await page.title();
  expect(title).toContain('Gateway Gardens | Glossary');
  //-----------------------------------------------------------------------
  // Go to Reference page
  //-----------------------------------------------------------------------
  await page.getByRole('link', { name: 'Reference', exact: true }).click();
  title = await page.title();
  expect(title).toContain('Gateway Gardens | Reference');
  //-----------------------------------------------------------------------
  // Go to About page
  //-----------------------------------------------------------------------
  await page.getByRole('link', { name: 'About', exact: true }).click();
  title = await page.title();
  expect(title).toContain('Gateway Gardens | About');
  //-----------------------------------------------------------------------

  // await page.pause()
  
});