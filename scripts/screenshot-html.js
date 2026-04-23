#!/usr/bin/env node
/**
 * Screenshot HTML files using puppeteer-core + system Chrome.
 * Usage: node scripts/screenshot-html.js [html_file_or_dir] [output_dir]
 */
const puppeteer = require('puppeteer-core');
const path = require('path');
const fs = require('fs');

const CHROME_PATH = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';

async function screenshot(htmlPath, outputDir) {
  const absHtml = path.resolve(htmlPath);
  const basename = path.basename(htmlPath, '.html');
  const outFile = path.join(outputDir, `${basename}.png`);

  const browser = await puppeteer.launch({
    executablePath: CHROME_PATH,
    headless: 'new',
    args: ['--no-sandbox', '--disable-setuid-sandbox'],
  });

  const page = await browser.newPage();
  await page.setViewport({ width: 1280, height: 900 });
  await page.goto(`file://${absHtml}`, { waitUntil: 'networkidle0', timeout: 30000 });
  
  // Wait a bit for any JS rendering
  await new Promise(r => setTimeout(r, 1000));

  await page.screenshot({ path: outFile, fullPage: true });
  await browser.close();

  console.log(`  ✅ ${basename}.png (${(fs.statSync(outFile).size / 1024).toFixed(0)} KB)`);
  return outFile;
}

async function main() {
  const input = process.argv[2] || 'features/assessment-admin/pad';
  const outputDir = process.argv[3] || 'screenshots';

  fs.mkdirSync(outputDir, { recursive: true });

  let files = [];
  if (fs.statSync(input).isDirectory()) {
    files = fs.readdirSync(input)
      .filter(f => f.endsWith('.html'))
      .map(f => path.join(input, f));
  } else {
    files = [input];
  }

  console.log(`Screenshotting ${files.length} files → ${outputDir}/`);
  const results = [];
  for (const f of files) {
    const out = await screenshot(f, outputDir);
    results.push(out);
  }
  console.log(`\nDone: ${results.length} screenshots`);
}

main().catch(e => { console.error(e); process.exit(1); });
