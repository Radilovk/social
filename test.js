const fs = require('fs');
const { JSDOM, VirtualConsole } = require('jsdom');
let html = fs.readFileSync('index.html', 'utf-8');
html = html.replace(/<link[^>]*fonts\.googleapis[^>]*>/g, '');
html = html.replace(/<script src="bookData.js"><\/script>/, '');
const dataScript = fs.readFileSync('bookData.js', 'utf-8');
html = html.replace('</body>', `<script>${dataScript}</script></body>`);
const vConsole = new VirtualConsole();
vConsole.sendTo(console);
const dom = new JSDOM(html, { runScripts: 'dangerously', resources: 'usable', url: 'http://localhost', pretendToBeVisual: true, virtualConsole: vConsole });
dom.window.scrollTo = () => {};
dom.window.addEventListener('load', () => {
  const navList = dom.window.document.getElementById('nav-list-container');
  const navItems = navList ? navList.querySelectorAll('li').length : 0;
  console.log('Nav items:', navItems);
  const continueBtn = dom.window.document.querySelector('#continue-reading-btn');
  console.log('Continue button:', continueBtn?.textContent.trim());
});
