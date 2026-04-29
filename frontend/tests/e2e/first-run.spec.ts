import { test, expect } from "@playwright/test";

test("first run: chat -> ask -> see citations", async ({ page }) => {
  await page.goto("/");
  await expect(page.getByText(/Vakeel for India/i)).toBeVisible();

  // Pick a starter prompt.
  await page.getByRole("button", { name: /landlord/i }).first().click();

  // Wait for any rendered citation pill.
  await expect(page.locator(".cite-pill").first()).toBeVisible({ timeout: 10_000 });

  // Confidence badge present.
  await expect(page.getByRole("status")).toBeVisible();
});

test("persona persists across reload", async ({ page }) => {
  await page.goto("/");
  await page.getByRole("button", { name: /^founder$/i }).click();
  await page.reload();
  await expect(page.getByText(/Mode: Founder/i)).toBeVisible();
});

test("company KB upload flow", async ({ page }) => {
  await page.goto("/company");
  await expect(page.getByRole("heading", { name: /Company Knowledge Base/i })).toBeVisible();
  // Upload control present.
  await expect(page.getByText(/Choose file/i)).toBeVisible();
});
