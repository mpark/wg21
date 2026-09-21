(() => {
  const root = document.documentElement;
  const darkStyles = document.getElementById('dark-theme-styles');
  const storageKey = 'mpark-wg21-theme';
  const themes = new Set(['system', 'light', 'dark']);

  let theme = 'system';
  try {
    const stored = localStorage.getItem(storageKey);
    if (themes.has(stored)) theme = stored;
  } catch (_) {
    // Local storage may be unavailable for local files or restricted contexts.
  }

  function applyTheme(value, persist) {
    theme = value;
    root.dataset.theme = value;
    darkStyles.media = value === 'dark'
      ? 'screen'
      : value === 'light' ? 'not all' : 'screen and (prefers-color-scheme: dark)';

    for (const button of document.querySelectorAll('button[data-theme-value]')) {
      button.setAttribute('aria-pressed', String(button.dataset.themeValue === value));
    }

    if (!persist) return;
    try {
      if (value === 'system') {
        localStorage.removeItem(storageKey);
      } else {
        localStorage.setItem(storageKey, value);
      }
    } catch (_) {
      // The selected theme still applies for this page.
    }
  }

  applyTheme(theme, false);
  document.addEventListener('DOMContentLoaded', () => {
    applyTheme(theme, false);
    for (const button of document.querySelectorAll('button[data-theme-value]')) {
      button.addEventListener('click', () => applyTheme(button.dataset.themeValue, true));
    }
  });
})();
