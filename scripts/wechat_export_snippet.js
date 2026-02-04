// Paste into the WeChat MP article list page console to export URLs.
// It collects visible article links on the page.
(() => {
  const links = new Set();
  document.querySelectorAll('a').forEach((a) => {
    if (!a.href) return;
    if (a.href.includes('mp.weixin.qq.com/s/')) {
      links.add(a.href.split('#')[0]);
    }
  });
  const output = [...links].join('\n');
  console.log(output);
  if (output) {
    try {
      navigator.clipboard.writeText(output);
      console.log('Copied to clipboard');
    } catch (e) {
      console.log('Clipboard copy failed, please copy from console output.');
    }
  } else {
    console.log('No links found on this page. Scroll/load more and retry.');
  }
})();
