// Copy to LLM functionality
// This script adds "Copy to LLM" buttons to code blocks and content sections
(function() {
  'use strict';

  // Helper function to format code for LLM consumption
  function formatCodeForLLM(codeElement, language) {
    const code = codeElement.textContent;
    const context = getPageContext();
    const siteName = getSiteName();

    const contextHeader = siteName ? `# Context from ${siteName}` : '# Context';

    return `${contextHeader}
Page: ${context.title}
Section: ${context.section}
URL: ${context.url}

\`\`\`${language}
${code}
\`\`\``;
  }

  // Helper function to format content section for LLM
  function formatSectionForLLM(sectionElement) {
    const context = getPageContext();
    const content = cleanContentForLLM(sectionElement);
    const siteName = getSiteName();

    const header = siteName ? `# ${siteName} Section` : '# Documentation Section';

    return `${header}
Page: ${context.title}
URL: ${context.url}

${content}`;
  }

  // Get site name from meta tag
  function getSiteName() {
    const metaSiteName = document.querySelector('meta[name="mkdocs-site-name"]');
    return metaSiteName ? metaSiteName.content : '';
  }

  // Check if analytics is enabled
  function isAnalyticsEnabled() {
    const metaAnalytics = document.querySelector('meta[name="mkdocs-copy-to-llm-analytics"]');
    return metaAnalytics && metaAnalytics.content === 'true';
  }


  // Track copy event to analytics
  function trackCopyEvent(eventType, contentLength) {
    // Only track if analytics is explicitly enabled via configuration
    if (!isAnalyticsEnabled()) {
      return;
    }

    // Check if Google Analytics is available
    if (typeof window.gtag === 'function') {
      try {
        window.gtag('event', 'copy_to_llm', {
          'event_category': 'engagement',
          'event_label': eventType,
          'value': contentLength
        });
      } catch (error) {
        console.error('Error tracking copy event:', error);
      }
    }

    // Support for other analytics platforms can be added here
    // For example: Plausible, Matomo, etc.
    if (typeof window.plausible === 'function') {
      try {
        window.plausible('Copy to LLM', { props: { type: eventType, length: contentLength } });
      } catch (error) {
        console.error('Error tracking copy event with Plausible:', error);
      }
    }
  }

  // Get current page context
  function getPageContext() {
    return {
      title: document.title,
      section: getCurrentSection(),
      url: window.location.href
    };
  }

  // Get the current section heading
  function getCurrentSection() {
    const headings = document.querySelectorAll('h1, h2, h3');
    for (let heading of headings) {
      if (heading.getBoundingClientRect().top > 0) {
        return heading.textContent.trim();
      }
    }
    return 'Main Content';
  }

  // Get the raw Markdown file URL
  function getMdFileUrl() {
    // Try to get the edit URL from MkDocs if available
    const editLink = document.querySelector('a[href*="edit/"]');
    if (editLink && editLink.href) {
      // Convert edit URL to raw URL
      // GitHub edit URL: https://github.com/owner/repo/edit/branch/path/to/file.md
      // Raw URL: https://raw.githubusercontent.com/owner/repo/branch/path/to/file.md
      const editUrl = editLink.href;
      try {
        const parsedUrl = new URL(editUrl);
        if (parsedUrl.hostname === 'github.com') {
          return editUrl
            .replace('github.com', 'raw.githubusercontent.com')
            .replace('/edit/', '/')
            .replace('/blob/', '/');
        }
      } catch (e) {
        // If URL parsing fails, fall through to fallback logic
      }
    }

    // Fallback: construct URL from current path
    const currentPath = window.location.pathname;

    // Remove the trailing slash if present
    let path = currentPath.endsWith('/') ? currentPath.slice(0, -1) : currentPath;

    // Handle root and index pages
    if (!path || path === '') {
      path = '/index';
    } else if (path.endsWith('/index')) {
      // Already ends with index, keep it
    } else if (!path.includes('.')) {
      // If path doesn't have an extension and doesn't end with index, it's likely a directory
      // MkDocs serves directory/index.md as directory/
      path = path + '/index';
    }

    // Try to get the repository URL from the page
    const repoLink = document.querySelector('a[href*="github.com"][href$="/tree/"]') ||
                     document.querySelector('a[href*="github.com"][href*="/tree/"]');

    let baseUrl = '';
    if (repoLink && repoLink.href) {
      // Extract base URL from repository link
      const match = repoLink.href.match(/github\.com\/([^\/]+\/[^\/]+)\/tree\/([^\/]+)/);
      if (match) {
        const [, repo, branch] = match;
        baseUrl = `https://raw.githubusercontent.com/${repo}/${branch}`;
      }
    }

    // Check for a configured base URL in meta tag or data attribute
    if (!baseUrl) {
      const metaRepo = document.querySelector('meta[name="mkdocs-copy-to-llm-repo-url"]');
      if (metaRepo && metaRepo.content) {
        baseUrl = metaRepo.content;
      }
    }

    // Fallback to a default (you might want to make this configurable)
    if (!baseUrl) {
      // This is a fallback - ideally this should be configurable
      console.warn('Copy to LLM: Could not determine repository URL. Using fallback.');
      baseUrl = 'https://raw.githubusercontent.com/polkadot-developers/polkadot-docs/refs/heads/master';
    }

    const mdPath = path + '.md';

    return baseUrl + mdPath;
  }

  // Remove front matter (metadata) from Markdown content
  function removeFrontMatter(content) {
    // Check if the content starts with ---
    if (!content.startsWith('---')) {
      return content;
    }

    // Find the second --- that closes the front matter
    const lines = content.split('\n');
    let endIndex = -1;

    // Start from line 1 (skip the first ---)
    for (let i = 1; i < lines.length; i++) {
      if (lines[i].trim() === '---') {
        endIndex = i;
        break;
      }
    }

    // If we found the closing ---, remove everything up to and including it
    if (endIndex > 0) {
      // Join the remaining lines after the front matter
      return lines.slice(endIndex + 1).join('\n').trim();
    }

    // If no closing --- found, return original content
    return content;
  }

  // Clean content for LLM (remove extra UI elements)
  function cleanContentForLLM(element) {
    const clone = element.cloneNode(true);

    // Remove buttons and UI elements
    clone.querySelectorAll('.md-clipboard, .copy-to-llm, .headerlink').forEach(el => el.remove());

    // Remove <script> and <style> tags and their content using DOM methods
    clone.querySelectorAll('script, style').forEach(el => el.remove());
    let html = clone.innerHTML;

    // Convert to markdown-like format
    let text = html
      .replace(/<h1[^>]*>(.*?)<\/h1>/gi, '# $1\n\n')
      .replace(/<h2[^>]*>(.*?)<\/h2>/gi, '## $1\n\n')
      .replace(/<h3[^>]*>(.*?)<\/h3>/gi, '### $1\n\n')
      .replace(/<h4[^>]*>(.*?)<\/h4>/gi, '#### $1\n\n')
      .replace(/<pre[^>]*><code[^>]*>(.*?)<\/code><\/pre>/gs, '```\n$1\n```\n\n')
      .replace(/<code[^>]*>(.*?)<\/code>/g, '`$1`')
      .replace(/<strong[^>]*>(.*?)<\/strong>/g, '**$1**')
      .replace(/<em[^>]*>(.*?)<\/em>/g, '*$1*')
      .replace(/<a[^>]*href="([^"]*)"[^>]*>(.*?)<\/a>/g, '[$2]($1)')
      .replace(/<li[^>]*>(.*?)<\/li>/g, '- $1\n')
      .replace(/<p[^>]*>(.*?)<\/p>/g, '$1\n\n')
      .replace(/<br[^>]*>/g, '\n')
      .replace(/<[^>]+>/g, '');

    // Clean up extra whitespace
    return text.replace(/\n{3,}/g, '\n\n').trim();
  }

  // Copy to clipboard with fallback
  async function copyToClipboard(text, button, eventType = 'unknown') {
    try {
      await navigator.clipboard.writeText(text);
      showCopySuccess(button);

      // Track the copy event
      trackCopyEvent(eventType, text.length);
    } catch (err) {
      // Fallback for older browsers
      const textarea = document.createElement('textarea');
      textarea.value = text;
      textarea.style.position = 'fixed';
      textarea.style.opacity = '0';
      document.body.appendChild(textarea);
      textarea.select();

      try {
        document.execCommand('copy');
        showCopySuccess(button);

        // Track the copy event
        trackCopyEvent(eventType, text.length);
      } catch (fallbackErr) {
        console.error('Failed to copy:', fallbackErr);
        showCopyError(button);
      }

      document.body.removeChild(textarea);
    }
  }

  // Show success feedback
  function showCopySuccess(button) {
    const originalTitle = button.title;
    const textElement = button.querySelector('.button-text');
    const originalText = textElement ? textElement.textContent : '';

    // Only change text for dropdown items, not the main copy button
    if (button.classList.contains('copy-to-llm-dropdown-item')) {
      button.classList.add('copy-success');
      button.title = 'Copied!';

      // If button has text, update it
      if (textElement) {
        textElement.textContent = 'Copied!';
      }

      setTimeout(() => {
        button.classList.remove('copy-success');
        button.title = originalTitle;
        if (textElement) {
          textElement.textContent = originalText;
        }
      }, 2000);
    }

    // Create and show toast notification
    const isMarkdownLink = button.classList.contains('copy-to-llm-dropdown-item') &&
                          button.dataset.action === 'copy-markdown-link';
    showToast(isMarkdownLink ? 'Link copied to clipboard!' : 'Content copied to clipboard!');
  }

  // Show toast notification
  function showToast(message) {
    // Remove any existing toast
    const existingToast = document.querySelector('.copy-to-llm-toast');
    if (existingToast) {
      existingToast.remove();
    }

    // Create toast element
    const toast = document.createElement('div');
    toast.className = 'copy-to-llm-toast';
    toast.textContent = message;

    // Add to body
    document.body.appendChild(toast);

    // Trigger animation
    setTimeout(() => {
      toast.classList.add('show');
    }, 10);

    // Remove after delay
    setTimeout(() => {
      toast.classList.remove('show');
      setTimeout(() => {
        toast.remove();
      }, 300);
    }, 2500);
  }

  // Show error feedback
  function showCopyError(button) {
    button.classList.add('copy-error');
    button.title = 'Copy failed';

    setTimeout(() => {
      button.classList.remove('copy-error');
      button.title = 'Copy to LLM';
    }, 2000);
  }

  // Create copy to LLM button for code blocks
  function createCodeCopyButton() {
    const button = document.createElement('button');
    button.className = 'md-clipboard md-icon copy-to-llm copy-to-llm-code';
    button.title = 'Copy to LLM';
    button.setAttribute('aria-label', 'Copy code to clipboard for LLM usage');
    button.setAttribute('role', 'button');
    button.innerHTML = `
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" aria-hidden="true">
        <path d="M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zM9 17H7v-7h2v7zm4 0h-2V7h2v10zm4 0h-2v-4h2v4z"/>
      </svg>
    `;

    // Add keyboard navigation
    button.addEventListener('keydown', (e) => {
      if (e.key === 'Enter' || e.key === ' ') {
        e.preventDefault();
        button.click();
      }
    });

    return button;
  }

  // Create a copy to LLM button for sections
  function createSectionCopyButton() {
    // Create container for split button
    const container = document.createElement('div');
    container.className = 'copy-to-llm-split-container';

    // Left button (copy)
    const copyButton = document.createElement('button');
    copyButton.className = 'copy-to-llm copy-to-llm-section copy-to-llm-left';
    copyButton.title = 'Copy entire page to LLM';
    copyButton.setAttribute('aria-label', 'Copy entire page content to clipboard for LLM usage');
    copyButton.setAttribute('role', 'button');
    copyButton.innerHTML = `
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" class="copy-icon" aria-hidden="true">
        <path d="M16 1H4c-1.1 0-2 .9-2 2v14h2V3h12V1zm3 4H8c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h11c1.1 0 2-.9 2-2V7c0-1.1-.9-2-2-2zm0 16H8V7h11v14z"/>
      </svg>
      <span class="button-text">Copy page</span>
    `;

    // Right button (dropdown)
    const dropdownButton = document.createElement('button');
    dropdownButton.className = 'copy-to-llm copy-to-llm-section copy-to-llm-right';
    dropdownButton.title = 'Copy options';
    dropdownButton.type = 'button'; // Explicitly set type
    dropdownButton.setAttribute('aria-label', 'Copy options menu');
    dropdownButton.setAttribute('aria-haspopup', 'true');
    dropdownButton.setAttribute('aria-expanded', 'false');
    dropdownButton.setAttribute('role', 'button');
    dropdownButton.innerHTML = `
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" class="chevron-icon" aria-hidden="true">
        <path d="M7 10l5 5 5-5z"/>
      </svg>
    `;

    // Create dropdown menu
    const dropdownMenu = document.createElement('div');
    dropdownMenu.className = 'copy-to-llm-dropdown';
    dropdownMenu.setAttribute('role', 'menu');
    dropdownMenu.setAttribute('aria-labelledby', 'dropdown-button');

    // Button visibility is controlled at build time
    let dropdownItems = [];

    // The following conditionals are modified during build based on config
    if (true) { // copy_markdown_link button
      dropdownItems.push(`
        <button class="copy-to-llm-dropdown-item" data-action="copy-markdown-link" role="menuitem" tabindex="-1">
          <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 1024 1024" aria-hidden="true">
            <path fill="currentColor" d="M295.664 732.448c6.256 6.256 14.432 9.376 22.624 9.376s16.368-3.12 22.624-9.376L728.576 341.76c12.496-12.496 12.496-32.752 0-45.248s-32.752-12.496-45.248 0L295.664 687.2c-12.512 12.496-12.512 32.752 0 45.248m180.208-68.143c10.576 46.624-.834 92.4-36.866 128.432L309.758 917.985c-27.2 27.184-63.36 42.16-101.824 42.16s-74.624-14.976-101.808-42.16c-56.144-56.16-56.144-147.536-.336-203.344l126.256-130.256c27.2-27.184 63.36-42.176 101.824-42.176c13.152 0 25.824 2.352 38.176 5.743L421.998 498c-27.872-13.024-57.952-19.792-88.128-19.792c-53.233 0-106.465 20.32-147.073 60.929L60.86 669.073c-81.216 81.216-81.216 212.912 0 294.16c40.608 40.624 93.84 60.912 147.073 60.912s106.465-20.288 147.073-60.912L483.95 838.289c62.128-62.128 75.568-148.72 42.656-224.72zM963.134 60.784C922.51 20.176 869.294-.145 816.077-.145c-53.248 0-106.496 20.32-147.088 60.929L540.061 185.728c-64.4 64.4-77.536 160.465-39.792 238.033l49.664-49.648c-14.704-49.104-3.408-104.336 35.056-142.832l129.248-125.248c27.216-27.184 63.344-42.176 101.84-42.176c38.431 0 74.624 14.992 101.808 42.176c56.128 56.16 56.128 147.536.32 203.344L788.957 438.625c-27.183 27.183-63.376 42.159-101.808 42.159c-9.808 0-18.431.992-27.84-.928l-50.975 51.008c25.471 10.592 51.632 13.935 78.815 13.935c53.216 0 106.432-20.303 147.056-60.927L963.15 354.928c81.2-81.216 81.2-212.896-.015-294.144z"/>
          </svg>
          Copy markdown link
        </button>
      `);
    }

    if (true) { // view_as_markdown button
      dropdownItems.push(`
        <button class="copy-to-llm-dropdown-item" data-action="view-markdown" role="menuitem" tabindex="-1">
          <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" aria-hidden="true">
            <path fill="currentColor" d="M22.27 19.385H1.73A1.73 1.73 0 0 1 0 17.655V6.345a1.73 1.73 0 0 1 1.73-1.73h20.54A1.73 1.73 0 0 1 24 6.345v11.308a1.73 1.73 0 0 1-1.73 1.731zM5.769 15.923v-4.5l2.308 2.885l2.307-2.885v4.5h2.308V8.078h-2.308l-2.307 2.885l-2.308-2.885H3.46v7.847zM21.232 12h-2.309V8.077h-2.307V12h-2.308l3.461 4.039z"/>
          </svg>
          <span>View as markdown</span>
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" class="external-icon" aria-hidden="true">
            <path d="M14 3v2h3.59l-9.83 9.83 1.41 1.41L19 6.41V10h2V3h-7z"/>
          </svg>
        </button>
      `);
    }

    if (true) { // open_in_chatgpt button
      dropdownItems.push(`
        <button class="copy-to-llm-dropdown-item" data-action="open-chatgpt" role="menuitem" tabindex="-1">
          <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" aria-hidden="true">
            <path fill="currentColor" d="M22.282 9.821a6 6 0 0 0-.516-4.91a6.05 6.05 0 0 0-6.51-2.9A6.065 6.065 0 0 0 4.981 4.18a6 6 0 0 0-3.998 2.9a6.05 6.05 0 0 0 .743 7.097a5.98 5.98 0 0 0 .51 4.911a6.05 6.05 0 0 0 6.515 2.9A6 6 0 0 0 13.26 24a6.06 6.06 0 0 0 5.772-4.206a6 6 0 0 0 3.997-2.9a6.06 6.06 0 0 0-.747-7.073M13.26 22.43a4.48 4.48 0 0 1-2.876-1.04l.141-.081l4.779-2.758a.8.8 0 0 0 .392-.681v-6.737l2.02 1.168a.07.07 0 0 1 .038.052v5.583a4.504 4.504 0 0 1-4.494 4.494M3.6 18.304a4.47 4.47 0 0 1-.535-3.014l.142.085l4.783 2.759a.77.77 0 0 0 .78 0l5.843-3.369v2.332a.08.08 0 0 1-.033.062L9.74 19.95a4.5 4.5 0 0 1-6.14-1.646M2.34 7.896a4.5 4.5 0 0 1 2.366-1.973V11.6a.77.77 0 0 0 .388.677l5.815 3.354l-2.02 1.168a.08.08 0 0 1-.071 0l-4.83-2.786A4.504 4.504 0 0 1 2.34 7.872zm16.597 3.855l-5.833-3.387L15.119 7.2a.08.08 0 0 1 .071 0l4.83 2.791a4.494 4.494 0 0 1-.676 8.105v-5.678a.79.79 0 0 0-.407-.667m2.01-3.023l-.141-.085l-4.774-2.782a.78.78 0 0 0-.785 0L9.409 9.23V6.897a.07.07 0 0 1 .028-.061l4.83-2.787a4.5 4.5 0 0 1 6.68 4.66zm-12.64 4.135l-2.02-1.164a.08.08 0 0 1-.038-.057V6.075a4.5 4.5 0 0 1 7.375-3.453l-.142.08L8.704 5.46a.8.8 0 0 0-.393.681zm1.097-2.365l2.602-1.5l2.607 1.5v2.999l-2.597 1.5l-2.607-1.5Z"/>
          </svg>
          <span>Open in ChatGPT</span>
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" class="external-icon" aria-hidden="true">
            <path d="M14 3v2h3.59l-9.83 9.83 1.41 1.41L19 6.41V10h2V3h-7z"/>
          </svg>
        </button>
      `);
    }

    if (true) { // open_in_claude button
      dropdownItems.push(`
        <button class="copy-to-llm-dropdown-item" data-action="open-claude" role="menuitem" tabindex="-1">
          <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" aria-hidden="true">
            <path fill="currentColor" d="M17.304 3.541h-3.672l6.696 16.918H24Zm-10.608 0L0 20.459h3.744l1.37-3.553h7.005l1.369 3.553h3.744L10.536 3.541Zm-.371 10.223L8.616 7.82l2.291 5.945Z"/>
          </svg>
          <span>Open in Claude</span>
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" class="external-icon" aria-hidden="true">
            <path d="M14 3v2h3.59l-9.83 9.83 1.41 1.41L19 6.41V10h2V3h-7z"/>
          </svg>
        </button>
      `);
    }

    const itemsHtml = dropdownItems.join('');
    if (!itemsHtml.trim()) {
      // No items to show; hide dropdown UI
      dropdownButton.style.display = 'none';
      dropdownMenu.remove();
    } else {
      dropdownMenu.innerHTML = itemsHtml;
    }

    container.appendChild(copyButton);
    container.appendChild(dropdownButton);
    container.appendChild(dropdownMenu);

    return { container, copyButton, dropdownButton, dropdownMenu };
  }

  // Add copy buttons to code blocks
  function addCodeCopyButtons() {
    const codeBlocks = document.querySelectorAll('.highlight');

    codeBlocks.forEach(block => {
      // Skip if the button already exists
      if (block.querySelector('.copy-to-llm-code')) return;

      const preElement = block.querySelector('pre');
      if (!preElement) return;

      // Get language from class
      const codeElement = preElement.querySelector('code');
      const language = getLanguageFromClass(codeElement) || 'text';

      // Create and add a button
      const button = createCodeCopyButton();
      button.addEventListener('click', (e) => {
        e.preventDefault();
        const formattedCode = formatCodeForLLM(codeElement, language);
        copyToClipboard(formattedCode, button, 'code_block');
      });

      // Insert after the existing copy button if it exists
      const existingCopyBtn = block.querySelector('.md-clipboard');
      if (existingCopyBtn) {
        existingCopyBtn.parentNode.insertBefore(button, existingCopyBtn.nextSibling);
      } else {
        // Otherwise add to the code block
        block.appendChild(button);
      }
    });
  }

  // Get language from a code element class
  function getLanguageFromClass(codeElement) {
    if (!codeElement || !codeElement.className) return null;

    const match = codeElement.className.match(/language-(\w+)/);
    return match ? match[1] : null;
  }

  // Add copy buttons to article sections
  function addSectionCopyButtons() {
    // Button visibility is controlled at build time
    // The following conditional is modified during build based on config
    if (false) { // copy_page button disabled check
      return;
    }

    // Only add to the main h1 title
    const mainTitle = document.querySelector('.md-content h1');
    if (mainTitle && !document.querySelector('.copy-to-llm-split-container')) {
      // Create a wrapper div for h1 and button
      const wrapper = document.createElement('div');
      wrapper.className = 'h1-copy-wrapper';

      // Insert wrapper before h1
      mainTitle.parentNode.insertBefore(wrapper, mainTitle);

      // Move h1 into wrapper
      wrapper.appendChild(mainTitle);

      // Create and add a split button
      const { container, copyButton, dropdownButton, dropdownMenu } = createSectionCopyButton();

      // Add keyboard navigation to buttons
      [copyButton, dropdownButton].forEach(button => {
        button.addEventListener('keydown', (e) => {
          if (e.key === 'Enter' || e.key === ' ') {
            e.preventDefault();
            button.click();
          }
        });
      });

      // Add keyboard navigation to dropdown menu
      dropdownMenu.addEventListener('keydown', (e) => {
        const items = Array.from(dropdownMenu.querySelectorAll('.copy-to-llm-dropdown-item'));
        const currentIndex = items.findIndex(item => item === document.activeElement);

        switch(e.key) {
          case 'ArrowDown':
            e.preventDefault();
            const nextIndex = currentIndex < items.length - 1 ? currentIndex + 1 : 0;
            items[nextIndex].tabIndex = 0;
            items[nextIndex].focus();
            if (currentIndex >= 0) items[currentIndex].tabIndex = -1;
            break;

          case 'ArrowUp':
            e.preventDefault();
            const prevIndex = currentIndex > 0 ? currentIndex - 1 : items.length - 1;
            items[prevIndex].tabIndex = 0;
            items[prevIndex].focus();
            if (currentIndex >= 0) items[currentIndex].tabIndex = -1;
            break;

          case 'Escape':
            e.preventDefault();
            dropdownMenu.classList.remove('show');
            dropdownButton.classList.remove('active');
            dropdownButton.setAttribute('aria-expanded', 'false');
            dropdownButton.focus();
            // Reset chevron
            const chevron = dropdownButton.querySelector('.chevron-icon');
            if (chevron) {
              chevron.style.transform = '';
            }
            break;

          case 'Home':
            e.preventDefault();
            if (items.length > 0) {
              items[0].tabIndex = 0;
              items[0].focus();
              if (currentIndex >= 0) items[currentIndex].tabIndex = -1;
            }
            break;

          case 'End':
            e.preventDefault();
            if (items.length > 0) {
              items[items.length - 1].tabIndex = 0;
              items[items.length - 1].focus();
              if (currentIndex >= 0) items[currentIndex].tabIndex = -1;
            }
            break;
        }
      });

      // Copy button click handler
      copyButton.addEventListener('click', async (e) => {
        e.preventDefault();

        // Save original icon HTML
        const copyIcon = copyButton.querySelector('.copy-icon');
        const originalIconHTML = copyIcon.outerHTML;

        // Replace icon with loading spinner
        copyIcon.outerHTML = `
          <svg class="copy-icon loading-spinner" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
            <circle cx="12" cy="12" r="10" stroke="currentColor" stroke-width="2" fill="none" stroke-dasharray="31.4" stroke-dashoffset="0">
              <animate attributeName="stroke-dashoffset" dur="1s" repeatCount="indefinite" from="0" to="62.8"/>
            </circle>
          </svg>
        `;

        try {
          // Fetch the raw Markdown content
          const mdUrl = getMdFileUrl();
          const response = await fetch(mdUrl);

          if (response.ok) {
            let markdownContent = await response.text();

            // Remove front matter (metadata) if present
            markdownContent = removeFrontMatter(markdownContent);

            await copyToClipboard(markdownContent, copyButton, 'markdown_content');

            // Change to check icon and make it green
            const checkIconSVG = `
              <svg class="copy-icon copy-success-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
                <path d="M9 16.17L4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41z"/>
              </svg>
            `;
            copyButton.querySelector('.copy-icon').outerHTML = checkIconSVG;

            // Restore the original icon after 3 seconds
            setTimeout(() => {
              copyButton.querySelector('.copy-icon').outerHTML = originalIconHTML;
            }, 3000);
          } else {
            // Fallback to formatted content if fetch fails
            const articleContent = document.querySelector('.md-content__inner .md-typeset');
            if (articleContent) {
              const formattedContent = formatSectionForLLM(articleContent);
              await copyToClipboard(formattedContent, copyButton, 'page_content');

              // Restore original icon
              copyButton.querySelector('.copy-icon').outerHTML = originalIconHTML;

              // Show success by making the icon green after a small delay to ensure DOM updates
              setTimeout(() => {
                copyButton.classList.add('copy-success-icon');
                setTimeout(() => {
                  copyButton.classList.remove('copy-success-icon');
                }, 3000);
              }, 50);
            }
          }
        } catch (error) {
          // Fallback to formatted content if fetch fails
          console.error('Failed to fetch markdown:', error);
          const articleContent = document.querySelector('.md-content__inner .md-typeset');
          if (articleContent) {
            const formattedContent = formatSectionForLLM(articleContent);
            await copyToClipboard(formattedContent, copyButton, 'page_content');

            // Change to check icon and make it green
            const checkIconSVG = `
              <svg class="copy-icon copy-success-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
                <path d="M9 16.17L4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41z"/>
              </svg>
            `;
            copyButton.querySelector('.copy-icon').outerHTML = checkIconSVG;

            // Restore the original icon after 3 seconds
            setTimeout(() => {
              copyButton.querySelector('.copy-icon').outerHTML = originalIconHTML;
            }, 3000);
          }
        }
      });

      // Dropdown button click handler
      dropdownButton.addEventListener('click', (e) => {
        e.preventDefault();
        e.stopPropagation();
        console.log('Dropdown clicked!'); // Debug log
        dropdownMenu.classList.toggle('show');

        // Toggle active state on button
        if (dropdownMenu.classList.contains('show')) {
          dropdownButton.classList.add('active');
          dropdownButton.setAttribute('aria-expanded', 'true');
          // Focus first menu item
          const firstItem = dropdownMenu.querySelector('.copy-to-llm-dropdown-item');
          if (firstItem) {
            firstItem.tabIndex = 0;
            firstItem.focus();
          }
        } else {
          dropdownButton.classList.remove('active');
          dropdownButton.setAttribute('aria-expanded', 'false');
        }

        // Toggle chevron rotation
        const chevron = dropdownButton.querySelector('.chevron-icon');
        if (chevron) {
          chevron.style.transform = dropdownMenu.classList.contains('show') ? 'rotate(180deg)' : '';
        }
      });

      // Dropdown menu item handlers
      dropdownMenu.addEventListener('click', (e) => {
        e.stopPropagation();
        const item = e.target.closest('.copy-to-llm-dropdown-item');
        if (!item) return;

        const action = item.dataset.action;
        const articleContent = document.querySelector('.md-content__inner .md-typeset');
        let contentToCopy = '';

        switch(action) {
          case 'copy-markdown-link':
            // Copy the raw Markdown file URL
            contentToCopy = getMdFileUrl();
            break;

          case 'view-markdown':
            // Open the raw Markdown file directly
            const mdUrl = getMdFileUrl();
            window.open(mdUrl, '_blank');
            dropdownMenu.classList.remove('show');
            dropdownButton.classList.remove('active');
            resetChevron();
            return; // Don't copy, just view

          case 'open-chatgpt':
            // Get the Markdown file URL
            const mdUrlForChatGPT = getMdFileUrl();
            const chatGPTPrompt = `Read ${mdUrlForChatGPT} so I can ask questions about it.`;
            const chatGPTUrl = `https://chatgpt.com/?hints=search&q=${encodeURIComponent(chatGPTPrompt)}`;
            window.open(chatGPTUrl, '_blank');
            dropdownMenu.classList.remove('show');
            dropdownButton.classList.remove('active');
            resetChevron();
            return; // Don't copy, just open

          case 'open-claude':
            // Get the Markdown file URL
            const mdUrlForClaude = getMdFileUrl();
            const claudePrompt = `Read ${mdUrlForClaude} so I can ask questions about it.`;
            const claudeUrl = `https://claude.ai/new?q=${encodeURIComponent(claudePrompt)}`;
            window.open(claudeUrl, '_blank');
            dropdownMenu.classList.remove('show');
            dropdownButton.classList.remove('active');
            resetChevron();
            return; // Don't copy, just open
        }

        if (contentToCopy) {
          copyToClipboard(contentToCopy, item, 'markdown_link');
          dropdownMenu.classList.remove('show');
          dropdownButton.classList.remove('active');
          resetChevron();
        }

        function resetChevron() {
          const chevron = dropdownButton.querySelector('.chevron-icon');
          if (chevron) {
            chevron.style.transform = '';
          }
        }
      });

      // Close dropdown when clicking outside
      document.addEventListener('click', (e) => {
        if (!container.contains(e.target)) {
          dropdownMenu.classList.remove('show');
          dropdownButton.classList.remove('active');
          // Reset chevron rotation
          const chevron = dropdownButton.querySelector('.chevron-icon');
          if (chevron) {
            chevron.style.transform = '';
          }
        }
      });

      wrapper.appendChild(container);
    }
  }

  // Get content of a section starting from a heading
  function getSectionContent(heading) {
    const content = document.createElement('div');
    content.appendChild(heading.cloneNode(true));

    let sibling = heading.nextElementSibling;
    while (sibling && !sibling.matches('h1, h2')) {
      content.appendChild(sibling.cloneNode(true));
      sibling = sibling.nextElementSibling;
    }

    return content;
  }

  // Initialize on DOM ready
  function initialize() {
    addCodeCopyButtons();
    addSectionCopyButtons();

    // Re-run when content changes (for dynamic content)
    const observer = new MutationObserver(() => {
      addCodeCopyButtons();
      addSectionCopyButtons();
    });

    const content = document.querySelector('.md-content');
    if (content) {
      observer.observe(content, {
        childList: true,
        subtree: true
      });
    }
  }

  // Wait for DOM to be ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initialize);
  } else {
    initialize();
  }

})();
