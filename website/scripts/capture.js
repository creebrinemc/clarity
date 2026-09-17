import puppeteer from 'puppeteer-core';
import { spawn } from 'node:child_process';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const websiteDir = path.resolve(__dirname, '..');
const CHROME_PATH = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
const PORT = 4175;
const BASE_URL = `http://localhost:${PORT}`;

const ROUTES = [
  { route: '/', filename: 'home.png', title: 'Homepage' },
  { route: '/docs', filename: 'docs.png', title: 'Docs Hub' },
  { route: '/docs/getting-started', filename: 'getting-started.png', title: 'Docs: Getting Started' },
  { route: '/docs/language', filename: 'language.png', title: 'Docs: Language Guide' },
  { route: '/docs/standard-library', filename: 'standard-library.png', title: 'Docs: Standard Library' },
  { route: '/docs/examples', filename: 'examples-docs.png', title: 'Docs: Examples Walkthrough' },
  { route: '/docs/ecosystem', filename: 'ecosystem.png', title: 'Docs: Ecosystem Architecture' },
  { route: '/docs/spec', filename: 'spec.png', title: 'Docs: Formal Specification' },
  { route: '/examples', filename: 'examples.png', title: 'Examples Showcase' },
  { route: '/install', filename: 'install.png', title: 'Installation Guide' },
  { route: '/roadmap', filename: 'roadmap.png', title: 'Project Roadmap' },
  { route: '/this-does-not-exist', filename: 'not-found.png', title: '404 Not Found State' },
];

const outputDirs = [
  path.resolve(websiteDir, 'visual-qa', 'desktop'),
  path.resolve(websiteDir, 'visual-qa', 'mobile'),
  path.resolve(websiteDir, 'public', 'visual-qa', 'desktop'),
  path.resolve(websiteDir, 'public', 'visual-qa', 'mobile'),
];

for (const dir of outputDirs) {
  fs.mkdirSync(dir, { recursive: true });
}

async function startServer() {
  return new Promise((resolve, reject) => {
    console.log(`Starting Vite preview server on port ${PORT}...`);
    const server = spawn('npx', ['vite', 'preview', '--port', String(PORT)], {
      cwd: websiteDir,
      stdio: ['ignore', 'pipe', 'pipe'],
    });

    let started = false;
    server.stdout.on('data', (data) => {
      const msg = data.toString();
      if (msg.includes('http://localhost') && !started) {
        started = true;
        console.log('Preview server ready.');
        resolve(server);
      }
    });

    server.stderr.on('data', (data) => {
      console.error('Server error:', data.toString());
    });

    server.on('error', reject);

    setTimeout(() => {
      if (!started) {
        started = true;
        resolve(server);
      }
    }, 4000);
  });
}

async function captureAll() {
  const server = await startServer();
  let browser;

  try {
    console.log('Launching Chrome from:', CHROME_PATH);
    browser = await puppeteer.launch({
      executablePath: CHROME_PATH,
      headless: true,
      args: ['--no-sandbox', '--disable-setuid-sandbox', '--disable-gpu'],
    });

    const page = await browser.newPage();

    // 1. Desktop captures
    console.log('\n--- Capturing Desktop Screenshots (1440x1000) ---');
    await page.setViewport({
      width: 1440,
      height: 1000,
      deviceScaleFactor: 2,
    });

    for (const item of ROUTES) {
      const targetUrl = `${BASE_URL}${item.route}`;
      console.log(`Capturing Desktop [${item.filename}]: ${targetUrl}`);
      await page.goto(targetUrl, { waitUntil: 'networkidle0', timeout: 15000 });
      await page.evaluate(() => document.fonts.ready);
      await new Promise((r) => setTimeout(r, 400));

      const targetPath1 = path.resolve(websiteDir, 'visual-qa', 'desktop', item.filename);
      const targetPath2 = path.resolve(websiteDir, 'public', 'visual-qa', 'desktop', item.filename);
      
      const buffer = await page.screenshot({ fullPage: false });
      fs.writeFileSync(targetPath1, buffer);
      fs.writeFileSync(targetPath2, buffer);
    }

    // 2. Mobile captures
    console.log('\n--- Capturing Mobile Screenshots (390x844) ---');
    await page.setViewport({
      width: 390,
      height: 844,
      deviceScaleFactor: 2,
      isMobile: true,
      hasTouch: true,
    });

    for (const item of ROUTES) {
      const targetUrl = `${BASE_URL}${item.route}`;
      console.log(`Capturing Mobile [${item.filename}]: ${targetUrl}`);
      await page.goto(targetUrl, { waitUntil: 'networkidle0', timeout: 15000 });
      await page.evaluate(() => document.fonts.ready);
      await new Promise((r) => setTimeout(r, 400));

      const targetPath1 = path.resolve(websiteDir, 'visual-qa', 'mobile', item.filename);
      const targetPath2 = path.resolve(websiteDir, 'public', 'visual-qa', 'mobile', item.filename);
      
      const buffer = await page.screenshot({ fullPage: false });
      fs.writeFileSync(targetPath1, buffer);
      fs.writeFileSync(targetPath2, buffer);
    }

    console.log('\nAll screenshots captured successfully!');
  } finally {
    if (browser) {
      await browser.close();
    }
    if (server) {
      server.kill('SIGTERM');
    }
  }
}

captureAll().catch((err) => {
  console.error('Fatal capture error:', err);
  process.exit(1);
});
