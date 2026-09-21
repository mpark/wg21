document.addEventListener('DOMContentLoaded', () => {
  const toc = document.querySelector('[role="doc-toc"]');
  if (!toc) return;

  const sourceList = toc.querySelector(':scope > ul');
  const chrome = toc.querySelector(':scope > .toc-chrome');
  if (!sourceList || !chrome) return;

  if (!sourceList.id) {
    sourceList.id = (toc.id || 'toc') + '-outline';
  }

  const expandToggle = chrome.querySelector('.toc-expand-toggle');
  const progressBar = chrome.querySelector('.toc-progress-bar');
  if (!expandToggle || !progressBar) return;

  expandToggle.setAttribute('aria-label', 'Expand table of contents');
  expandToggle.setAttribute('aria-controls', sourceList.id);

  const entries = Array.from(toc.querySelectorAll('a[href^="#"]'))
    .map(link => ({
      link,
      target: document.getElementById(
        decodeURIComponent(link.getAttribute('href')).slice(1))
    }))
    .filter(e => e.target);
  if (entries.length === 0) return;

  let active = null;
  let sidebar = false;
  let readingLine = 1;
  const mobileBar = document.querySelector('.toc-mobile-bar');
  const mobileDialog = document.querySelector('.toc-dialog');
  const mobileTrigger = document.querySelector('.toc-mobile-trigger');
  const closeButton = document.querySelector('.toc-dialog-close');
  const dialogNav = document.querySelector('.toc-dialog-nav');
  let mobileLinks = [];
  let expansionPreference = null;

  const hasNestedSections = Boolean(sourceList.querySelector('li > ul'));
  expandToggle.hidden = !hasNestedSections;

  function measureLayout() {
    sidebar = getComputedStyle(toc).position === 'fixed';
    readingLine =
      (parseFloat(getComputedStyle(entries[0].target).scrollMarginTop) || 0) + 1;
  }

  function setExpanded(expanded) {
    toc.classList.toggle('toc-expanded', expanded);
    expandToggle.textContent = expanded ? 'Collapse' : 'Expand';
    expandToggle.setAttribute('aria-expanded', String(expanded));
    expandToggle.setAttribute(
      'aria-label',
      expanded
        ? 'Collapse table of contents'
        : 'Expand table of contents'
    );
    if (active) {
      requestAnimationFrame(() => keepActiveEntryVisible(active.link));
    }
  }

  // Prefer the complete outline whenever it fits without adding an inner
  // scrollbar. This naturally accounts for viewport height and wrapping.
  function updateDefaultExpansion() {
    if (expansionPreference !== null || !sidebar || !hasNestedSections) {
      return;
    }

    toc.classList.add('toc-expanded');
    const expandedFits = toc.scrollHeight <= toc.clientHeight + 2;
    setExpanded(expandedFits);
  }

  expandToggle.addEventListener('click', () => {
    expansionPreference = !toc.classList.contains('toc-expanded');
    setExpanded(expansionPreference);
  });

  function syncMobileActive(scrollToActive = false) {
    const activeHref = active?.link.getAttribute('href');
    let mobileActive = null;

    for (const link of mobileLinks) {
      const isActive = link.getAttribute('href') === activeHref;
      link.classList.toggle('active', isActive);
      if (isActive) {
        link.setAttribute('aria-current', 'location');
        mobileActive = link;
      } else {
        link.removeAttribute('aria-current');
      }
    }

    if (scrollToActive && mobileActive) {
      requestAnimationFrame(() => {
        mobileActive.scrollIntoView({ block: 'center', behavior: 'auto' });
      });
    }
  }

  function markMobileDialogClosed() {
    document.body.classList.remove('toc-menu-open');
    if (mobileTrigger) mobileTrigger.setAttribute('aria-expanded', 'false');
  }

  function closeMobileDialog() {
    if (!mobileDialog?.open) return;
    if (typeof mobileDialog.close === 'function') {
      mobileDialog.close();
    } else {
      mobileDialog.removeAttribute('open');
      markMobileDialogClosed();
    }
  }

  if (mobileBar && mobileDialog && mobileTrigger && closeButton && dialogNav) {
    const mobileList = sourceList.cloneNode(true);
    mobileList.removeAttribute('id');
    for (const element of mobileList.querySelectorAll('[id]')) {
      element.removeAttribute('id');
    }
    dialogNav.appendChild(mobileList);
    mobileLinks = Array.from(dialogNav.querySelectorAll('a[href^="#"]'));

    document.body.classList.add('toc-ready');

    mobileTrigger.addEventListener('click', () => {
      syncMobileActive();
      document.body.classList.add('toc-menu-open');
      mobileTrigger.setAttribute('aria-expanded', 'true');
      if (typeof mobileDialog.showModal === 'function') {
        mobileDialog.showModal();
      } else {
        mobileDialog.setAttribute('open', '');
      }
      syncMobileActive(true);
    });
    closeButton.addEventListener('click', closeMobileDialog);
    mobileDialog.addEventListener('close', markMobileDialogClosed);
    mobileDialog.addEventListener('click', event => {
      if (event.target === mobileDialog) closeMobileDialog();
    });
    dialogNav.addEventListener('click', event => {
      const link = event.target.closest('a[href^="#"]');
      if (!link) return;

      const target = document.getElementById(
        decodeURIComponent(link.getAttribute('href')).slice(1));
      if (!target) return;

      event.preventDefault();
      closeMobileDialog();
      const href = link.getAttribute('href');
      requestAnimationFrame(() => requestAnimationFrame(() => {
        history.pushState(null, '', href);
        target.scrollIntoView();
      }));
    });
  }

  function keepActiveEntryVisible(link) {
    if (!sidebar) return;

    const tocRect = toc.getBoundingClientRect();
    const linkRect = link.getBoundingClientRect();
    const top = tocRect.top + chrome.offsetHeight + 8;
    const bottom = tocRect.bottom - 8;

    if (linkRect.top < top) {
      toc.scrollBy({
        top: linkRect.top - top
      });
    } else if (linkRect.bottom > bottom) {
      toc.scrollBy({
        top: linkRect.bottom - bottom
      });
    }
  }

  function update() {
    const scrollable = document.documentElement.scrollHeight - window.innerHeight;
    const fraction = scrollable > 0
      ? Math.max(0, Math.min(1, window.scrollY / scrollable))
      : 0;
    progressBar.style.transform = 'scaleX(' + fraction + ')';

    let current = entries[0];
    for (const e of entries) {
      // TOC entries are in document order, so stop at the first
      // heading below the reading line.
      if (e.target.getBoundingClientRect().top > readingLine) break;
      current = e;
    }
    if (current === active) {
      if (active) keepActiveEntryVisible(active.link);
      return;
    }

    if (active) {
      active.link.classList.remove('active');
      active.link.removeAttribute('aria-current');
    }
    active = current;
    if (active) {
      active.link.classList.add('active');
      active.link.setAttribute('aria-current', 'location');

      const stalePath = new Set(toc.querySelectorAll('li.active-path'));
      for (let n = active.link.parentElement; n && n !== toc; n = n.parentElement) {
        if (n.tagName === 'LI') {
          n.classList.add('active-path');
          stalePath.delete(n);
        }
      }
      for (const li of stalePath) li.classList.remove('active-path');
      keepActiveEntryVisible(active.link);
      syncMobileActive();
    }
  }

  let queued = false;
  function onScroll() {
    if (queued) return;
    queued = true;
    requestAnimationFrame(() => { queued = false; update(); });
  }

  let expansionQueued = false;
  function onResize() {
    measureLayout();
    if (sidebar) closeMobileDialog();
    onScroll();
    if (expansionPreference !== null || expansionQueued) return;
    expansionQueued = true;
    requestAnimationFrame(() => {
      expansionQueued = false;
      updateDefaultExpansion();
    });
  }

  window.addEventListener('scroll', onScroll, { passive: true });
  window.addEventListener('resize', onResize, { passive: true });
  // Late layout shifts (images, MathJax, mermaid) move the headings.
  window.addEventListener('load', () => {
    measureLayout();
    update();
    updateDefaultExpansion();
  });
  measureLayout();
  update();
  updateDefaultExpansion();
});
