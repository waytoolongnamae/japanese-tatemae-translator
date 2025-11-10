/**
 * Japanese Hedging Translator - Web App
 * Mobile-friendly translation interface
 */

// State
let currentLevel = 'business';
let lastTranslation = null;

// DOM Elements
const inputText = document.getElementById('input-text');
const charCount = document.getElementById('char-count');
const translateBtn = document.getElementById('translate-btn');
const outputSection = document.getElementById('output-section');
const outputText = document.getElementById('output-text');
const copyBtn = document.getElementById('copy-btn');
const shareBtn = document.getElementById('share-btn');
const levelButtons = document.querySelectorAll('.level-btn');
const examplesContainer = document.getElementById('examples-container');
const intentEl = document.getElementById('intent');
const confidenceEl = document.getElementById('confidence');
const languageEl = document.getElementById('language');
const btnText = translateBtn.querySelector('.btn-text');
const btnLoader = translateBtn.querySelector('.btn-loader');

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    loadExamples();
    setupEventListeners();
});

// Event Listeners
function setupEventListeners() {
    // Input text changes
    inputText.addEventListener('input', () => {
        updateCharCount();
        updateTranslateButton();
    });

    // Level selection
    levelButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            selectLevel(btn.dataset.level);
        });
    });

    // Translate button
    translateBtn.addEventListener('click', handleTranslate);

    // Copy button
    copyBtn.addEventListener('click', handleCopy);

    // Share button
    shareBtn.addEventListener('click', handleShare);

    // Note: Enter key adds newline naturally (no auto-submit)
    // Users must click the translate button to submit
}

// Update character count
function updateCharCount() {
    const count = inputText.value.length;
    charCount.textContent = count;

    if (count > 4500) {
        charCount.style.color = 'var(--secondary-color)';
    } else {
        charCount.style.color = 'var(--text-secondary)';
    }
}

// Update translate button state
function updateTranslateButton() {
    const hasText = inputText.value.trim().length > 0;
    translateBtn.disabled = !hasText;
}

// Select politeness level
function selectLevel(level) {
    currentLevel = level;
    levelButtons.forEach(btn => {
        if (btn.dataset.level === level) {
            btn.classList.add('active');
        } else {
            btn.classList.remove('active');
        }
    });
}

// Handle translation
async function handleTranslate() {
    const text = inputText.value.trim();
    if (!text) return;

    // Show loading state
    setLoadingState(true);

    try {
        const response = await fetch('/api/translate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                text: text,
                level: currentLevel
            })
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Translation failed');
        }

        const result = await response.json();
        displayResult(result);
        lastTranslation = result;

    } catch (error) {
        console.error('Translation error:', error);
        showToast('❌ Translation failed: ' + error.message);
    } finally {
        setLoadingState(false);
    }
}

// Display translation result
function displayResult(result) {
    outputText.textContent = result.tatemae_text;
    intentEl.textContent = result.intent;
    confidenceEl.textContent = (result.confidence * 100).toFixed(0) + '%';
    languageEl.textContent = result.detected_language.toUpperCase();

    // Show output section with animation
    outputSection.style.display = 'block';

    // Scroll to result
    setTimeout(() => {
        outputSection.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }, 100);

    showToast('✅ Translation complete!');
}

// Set loading state
function setLoadingState(isLoading) {
    if (isLoading) {
        translateBtn.disabled = true;
        btnText.style.display = 'none';
        btnLoader.style.display = 'inline';
        inputText.disabled = true;
    } else {
        translateBtn.disabled = false;
        btnText.style.display = 'inline';
        btnLoader.style.display = 'none';
        inputText.disabled = false;
    }
}

// Handle copy to clipboard
async function handleCopy() {
    if (!lastTranslation) return;

    const textToCopy = lastTranslation.tatemae_text;

    try {
        // Try modern Clipboard API first
        if (navigator.clipboard && navigator.clipboard.writeText) {
            await navigator.clipboard.writeText(textToCopy);
            showToast('📋 Copied to clipboard!');

            // Visual feedback
            copyBtn.textContent = '✓';
            setTimeout(() => {
                copyBtn.textContent = '📋';
            }, 1500);
        } else {
            // Fallback for older browsers or non-HTTPS contexts
            const textArea = document.createElement('textarea');
            textArea.value = textToCopy;
            textArea.style.position = 'fixed';
            textArea.style.left = '-999999px';
            textArea.style.top = '-999999px';
            document.body.appendChild(textArea);
            textArea.focus();
            textArea.select();

            try {
                const successful = document.execCommand('copy');
                if (successful) {
                    showToast('📋 Copied to clipboard!');

                    // Visual feedback
                    copyBtn.textContent = '✓';
                    setTimeout(() => {
                        copyBtn.textContent = '📋';
                    }, 1500);
                } else {
                    throw new Error('execCommand failed');
                }
            } finally {
                document.body.removeChild(textArea);
            }
        }
    } catch (error) {
        console.error('Copy failed:', error);
        showToast('❌ Copy failed - try selecting and copying manually');
    }
}

// Handle share
async function handleShare() {
    if (!lastTranslation) return;

    const shareData = {
        title: '建前 Translation',
        text: lastTranslation.tatemae_text,
        url: window.location.href
    };

    try {
        // Try Web Share API first (mobile)
        if (navigator.share) {
            await navigator.share(shareData);
            showToast('📤 Shared successfully!');
        } else {
            // Fallback: copy to clipboard
            await navigator.clipboard.writeText(
                `${shareData.text}\n\n📱 Translated with 建前 Translator: ${shareData.url}`
            );
            showToast('📋 Share text copied to clipboard!');
        }
    } catch (error) {
        if (error.name !== 'AbortError') {
            console.error('Share failed:', error);
            showToast('❌ Share failed');
        }
    }
}

// Load examples
async function loadExamples() {
    try {
        const response = await fetch('/api/examples');
        const data = await response.json();

        examplesContainer.innerHTML = data.examples
            .map(example => `
                <div class="example-card" data-text="${example.input.replace(/"/g, '&quot;')}">
                    <div class="example-text">"${example.input}"</div>
                    <div class="example-meta">
                        <span class="example-intent">${example.intent}</span>
                        <span>${example.description}</span>
                    </div>
                </div>
            `)
            .join('');

        // Add click handlers
        document.querySelectorAll('.example-card').forEach(card => {
            card.addEventListener('click', () => {
                inputText.value = card.dataset.text;
                updateCharCount();
                updateTranslateButton();
                inputText.focus();

                // Scroll to input
                inputText.scrollIntoView({ behavior: 'smooth', block: 'center' });
            });
        });
    } catch (error) {
        console.error('Failed to load examples:', error);
    }
}

// Show toast notification
function showToast(message) {
    const toast = document.getElementById('toast');
    toast.textContent = message;
    toast.style.display = 'block';

    setTimeout(() => {
        toast.style.display = 'none';
    }, 3000);
}

// PWA: Service Worker Registration
if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
        navigator.serviceWorker.register('/static/sw.js').catch(err => {
            console.log('Service worker registration failed:', err);
        });
    });
}
