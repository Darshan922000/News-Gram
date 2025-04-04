// API Configuration
const API_BASE_URL = 'http://localhost:8000';

// API endpoints
const ENDPOINTS = {
    NEWS_SEARCH: `${API_BASE_URL}/news_search`,
    HELP_SEARCH: `${API_BASE_URL}/help_search`
};

// DOM Elements
const newsSearchInput = document.getElementById('news-search');
const helpSearchInput = document.getElementById('help-search');
const newsSearchBtn = document.getElementById('news-search-btn');
const helpSearchBtn = document.getElementById('help-search-btn');
const newsResultsContent = document.getElementById('news-results-content');
const helpResultsContent = document.getElementById('help-results-content');
const themeToggle = document.querySelector('.theme-toggle');
const sunIcon = document.querySelector('.sun-icon');
const moonIcon = document.querySelector('.moon-icon');

// Templates
const loadingTemplate = document.getElementById('loading-template');

// Theme handling
function initializeTheme() {
    // Check for saved theme preference or use system preference
    const savedTheme = localStorage.getItem('theme');
    const systemPrefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    
    if (savedTheme) {
        document.documentElement.setAttribute('data-theme', savedTheme);
        updateThemeIcons(savedTheme);
    } else if (systemPrefersDark) {
        document.documentElement.setAttribute('data-theme', 'dark');
        updateThemeIcons('dark');
    }
}

function toggleTheme() {
    const currentTheme = document.documentElement.getAttribute('data-theme');
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
    
    document.documentElement.setAttribute('data-theme', newTheme);
    localStorage.setItem('theme', newTheme);
    updateThemeIcons(newTheme);
}

function updateThemeIcons(theme) {
    if (theme === 'dark') {
        sunIcon.style.display = 'none';
        moonIcon.style.display = 'block';
    } else {
        sunIcon.style.display = 'block';
        moonIcon.style.display = 'none';
    }
}

// Initialize the application
document.addEventListener('DOMContentLoaded', () => {
    initializeTheme();
    setupEventListeners();
    
    // Clear news data from local storage on page load
    localStorage.removeItem('newsData');
});

// Set up all event listeners
function setupEventListeners() {
    // Theme toggle
    themeToggle.addEventListener('click', toggleTheme);
    
    // Search button click events
    newsSearchBtn.addEventListener('click', () => handleNewsSearch(newsSearchInput.value));
    helpSearchBtn.addEventListener('click', () => handleHelpSearch(helpSearchInput.value));
    
    // Form submission (pressing Enter)
    newsSearchInput.closest('div.search-input-container').addEventListener('keydown', e => {
        if (e.key === 'Enter') {
            e.preventDefault();
            handleNewsSearch(newsSearchInput.value);
        }
    });
    
    helpSearchInput.closest('div.search-input-container').addEventListener('keydown', e => {
        if (e.key === 'Enter') {
            e.preventDefault();
            handleHelpSearch(helpSearchInput.value);
        }
    });
}

// Show loading indicator
function showLoading(container, type = 'news') {
    container.innerHTML = '';
    
    const loadingElement = loadingTemplate.content.cloneNode(true);
    const loadingIcon = loadingElement.querySelector('.loading-icon');
    const loadingMessage = loadingElement.querySelector('.loading-message');
    
    if (type === 'news') {
        loadingIcon.textContent = '🔍';
        loadingMessage.textContent = 'Searching';
    } else {
        loadingIcon.textContent = '💬';
        loadingMessage.textContent = 'Typing';
    }
    
    container.appendChild(loadingElement);
}

// Handler for news search
async function handleNewsSearch(query) {
    query = query.trim();
    
    if (!query) {
        return;
    }
    
    // Show loading indicator for news
    showLoading(newsResultsContent, 'news');
    
    try {
        const results = await fetchNewsResults(query);
        renderNewsResults(results);
        localStorage.setItem('newsData', results);
    } catch (error) {
        console.error('Error fetching news results:', error);
        showError(newsResultsContent, "I couldn't fetch results right now. Would you like me to try again or search another topic?");
    }
    
    // Clear the input field
    newsSearchInput.value = '';
}

// Handler for help search
async function handleHelpSearch(query) {
    query = query.trim();
    
    if (!query) {
        return;
    }
    
    // Show loading indicator for help
    showLoading(helpResultsContent, 'help');
    
    try {
        const results = await fetchHelpResults(query);
        renderHelpResults(results);
    } catch (error) {
        console.error('Error fetching help results:', error);
        showError(helpResultsContent, 'Failed to fetch help results. Please try again.');
    }
    
    // Clear the input field
    helpSearchInput.value = '';
}

// Fetch news search results from API
async function fetchNewsResults(query) {
    // Using POST request with JSON body as per FastAPI endpoint
    const response = await fetch(ENDPOINTS.NEWS_SEARCH, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            topic: query
        })
    });
    
    if (!response.ok) {
        throw new Error(`API request failed with status ${response.status}`);
    }
    
    const data = await response.json();
    return data.news || '';
}

// Fetch help search results from API
async function fetchHelpResults(query) {
    // Using POST request with JSON body as per FastAPI endpoint
    const response = await fetch(ENDPOINTS.HELP_SEARCH, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            query: query
        })
    });
    
    if (!response.ok) {
        throw new Error(`API request failed with status ${response.status}`);
    }
    
    const data = await response.json();
    return data.report || '';
}

// Render news search results
function renderNewsResults(results) {
    newsResultsContent.innerHTML = '';
    
    if (!results) {
        newsResultsContent.innerHTML = '<p class="placeholder-text">No news results found</p>';
        return;
    }
    
    // Configure marked options for better spacing
    marked.setOptions({
        breaks: true,
        gfm: true
    });
    
    // Split results by news items
    const newsItems = results.split('---');
    
    newsItems.forEach(item => {
        const trimmedItem = item.trim();
        if (trimmedItem) {
            const newsCard = document.createElement('div');
            newsCard.className = 'news-card';
            
            // Use marked library to convert markdown to HTML
            let htmlContent = marked.parse(trimmedItem);
            
            // Apply custom styling to source and time
            htmlContent = htmlContent
                .replace(/Source: (.*?) /g, '<span class="news-source">Source: $1</span> ')
                .replace(/Published: (.*?)$/gm, '<span class="news-time">Published: $1</span>')
                // Add special styling for conclusion sections
                .replace(/<p>Conclusion:/g, '<p class="conclusion">Conclusion:');
            
            // Replace news links with new tab links
            htmlContent = htmlContent.replace(/<a href="(.*?)"/g, '<a href="$1" target="_blank" rel="noopener noreferrer"');
            
            newsCard.innerHTML = htmlContent;
            newsResultsContent.appendChild(newsCard);
        }
    });
}

// Render help search results
function renderHelpResults(results) {
    helpResultsContent.innerHTML = '';
    
    if (!results) {
        helpResultsContent.innerHTML = '<p class="placeholder-text">No help results found</p>';
        return;
    }
    
    // Create a container for the answer content
    const answerContainer = document.createElement('div');
    answerContainer.className = 'answer-content';
    
    // Use marked library to convert markdown to HTML
    answerContainer.innerHTML = marked.parse(results);
    
    helpResultsContent.appendChild(answerContainer);
}

// Show error message
function showError(container, errorMessage) {
    container.innerHTML = `<div class="error-message">${errorMessage}</div>`;
}

// Utility function to debounce input events
function debounce(func, delay) {
    let timeoutId;
    return function(...args) {
        clearTimeout(timeoutId);
        timeoutId = setTimeout(() => {
            func.apply(this, args);
        }, delay);
    };
}

// Mock data for testing (will be replaced by actual API responses)
// Uncomment and use these while developing without a backend
/*
function fetchNewsSuggestions(query) {
    // Simulate API call
    return new Promise(resolve => {
        setTimeout(() => {
            const suggestions = [
                'Latest world news',
                'Technology trends 2025',
                'Sports updates',
                'Financial markets today',
                'Health news',
                'Politics latest',
                'Climate change report',
                'Entertainment news'
            ].filter(suggestion => 
                suggestion.toLowerCase().includes(query.toLowerCase())
            );
            resolve(suggestions);
        }, 300);
    });
}

function fetchHelpSuggestions(query) {
    // Simulate API call
    return new Promise(resolve => {
        setTimeout(() => {
            const suggestions = [
                'How to use News AI',
                'Setting up alerts',
                'Customizing news feed',
                'Saving articles',
                'Account settings',
                'Subscription plans',
                'Contact support',
                'Report an issue'
            ].filter(suggestion => 
                suggestion.toLowerCase().includes(query.toLowerCase())
            );
            resolve(suggestions);
        }, 300);
    });
}

function fetchNewsResults(query) {
    // Simulate API call
    return new Promise(resolve => {
        setTimeout(() => {
            resolve([
                {
                    id: '1',
                    title: 'Sample news article about ' + query,
                    snippet: 'This is a sample snippet that would typically contain a summary of the article related to ' + query + '...',
                    source: 'News Source',
                    url: 'https://example.com/news/1',
                    date: new Date().toLocaleDateString(),
                    imageUrl: 'https://picsum.photos/id/237/800/400',
                    category: 'Technology'
                },
                {
                    id: '2',
                    title: 'Another article related to ' + query,
                    snippet: 'Another sample snippet with information about ' + query + ' and related topics...',
                    source: 'Another Source',
                    url: 'https://example.com/news/2',
                    date: new Date().toLocaleDateString(),
                    category: 'Business'
                },
                {
                    id: '3',
                    title: 'Breaking news on ' + query,
                    snippet: 'The latest updates regarding ' + query + ' and how it affects current events...',
                    source: 'Breaking News',
                    url: 'https://example.com/news/3',
                    date: new Date().toLocaleDateString(),
                    imageUrl: 'https://picsum.photos/id/1005/800/400'
                }
            ]);
        }, 1000);
    });
}

function fetchHelpResults(query) {
    // Simulate API call
    return new Promise(resolve => {
        setTimeout(() => {
            resolve([
                {
                    id: '1',
                    title: 'Help article: ' + query,
                    snippet: 'This help article provides guidance on ' + query + ' and related functionalities...',
                    relatedTopics: ['Getting Started', 'Basics', 'Tutorial']
                },
                {
                    id: '2',
                    title: 'FAQ: ' + query,
                    snippet: 'Frequently asked questions about ' + query + ' and how to use this feature...',
                    relatedTopics: ['Common Questions', 'Troubleshooting']
                },
                {
                    id: '3',
                    title: 'Tutorial: Using ' + query,
                    snippet: 'Step-by-step guide to help you understand how to get the most out of ' + query + '...'
                }
            ]);
        }, 800);
    });
}
*/ 