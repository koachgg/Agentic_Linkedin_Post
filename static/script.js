/**
 * LinkedIn Post Generator - Frontend JavaScript
 */

// DOM elements
const postForm = document.getElementById('postForm');
const generateBtn = document.getElementById('generateBtn');
const loadingSpinner = document.getElementById('loadingSpinner');
const resultsSection = document.getElementById('resultsSection');
const postsContainer = document.getElementById('postsContainer');
const resultsCount = document.getElementById('resultsCount');
const errorSection = document.getElementById('errorSection');
const errorText = document.getElementById('errorText');

// Form fields
const topicInput = document.getElementById('topic');
const toneSelect = document.getElementById('tone');
const audienceInput = document.getElementById('audience');
const postCountInput = document.getElementById('postCount');
const useWebSearchCheckbox = document.getElementById('useWebSearch');

// State management
let isGenerating = false;

// Event listeners
document.addEventListener('DOMContentLoaded', function() {
    // Form submission
    postForm.addEventListener('submit', handleFormSubmit);
    
    // Real-time validation
    topicInput.addEventListener('input', validateForm);
    postCountInput.addEventListener('input', validatePostCount);
    
    // Clear errors on input
    topicInput.addEventListener('input', clearErrors);
    
    console.log('🚀 LinkedIn Post Generator loaded');
});

/**
 * Handle form submission
 */
async function handleFormSubmit(event) {
    event.preventDefault();
    
    if (isGenerating) return;
    
    if (!validateForm()) {
        showError('Please fill in all required fields correctly.');
        return;
    }
    
    const formData = getFormData();
    await generatePosts(formData);
}

/**
 * Validate form inputs
 */
function validateForm() {
    const topic = topicInput.value.trim();
    const postCount = parseInt(postCountInput.value);
    
    if (!topic) {
        topicInput.focus();
        return false;
    }
    
    if (postCount < 1 || postCount > 10) {
        postCountInput.focus();
        return false;
    }
    
    return true;
}

/**
 * Validate post count input
 */
function validatePostCount() {
    const postCount = parseInt(postCountInput.value);
    
    if (postCount < 1) {
        postCountInput.value = 1;
    } else if (postCount > 10) {
        postCountInput.value = 10;
    }
}

/**
 * Get form data
 */
function getFormData() {
    return {
        topic: topicInput.value.trim(),
        tone: toneSelect.value || null,
        audience: audienceInput.value.trim() || null,
        post_count: parseInt(postCountInput.value),
        use_web_search: useWebSearchCheckbox.checked
    };
}

/**
 * Generate posts by calling the API
 */
async function generatePosts(formData) {
    try {
        setLoadingState(true);
        clearErrors();
        hideResults();
        
        console.log('📤 Sending request:', formData);
        
        const response = await fetch('/generate_posts', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(formData)
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            const errorData = await response.json();
            let errorMessage = errorData.detail || `HTTP ${response.status}: ${response.statusText}`;
            
            // Handle specific error types
            if (response.status === 502) {
                errorMessage = "AI service is temporarily unavailable. Please try again in a few moments.";
            } else if (response.status === 400) {
                errorMessage = `Invalid request: ${errorData.detail}`;
            }
            
            throw new Error(errorMessage);
        }
        
        console.log('📥 Received response:', data);
        
        displayResults(data);
        
    } catch (error) {
        console.error('❌ Error generating posts:', error);
        
        // Show specific error message from server
        let displayMessage = error.message;
        
        // Handle network errors
        if (error.name === 'TypeError' && error.message.includes('fetch')) {
            displayMessage = 'Unable to connect to the server. Please check your internet connection.';
        }
        
        showError(displayMessage);
    } finally {
        setLoadingState(false);
    }
}

/**
 * Set loading state
 */
function setLoadingState(loading) {
    isGenerating = loading;
    generateBtn.disabled = loading;
    
    if (loading) {
        generateBtn.classList.add('loading');
    } else {
        generateBtn.classList.remove('loading');
    }
}

/**
 * Display generated posts
 */
function displayResults(data) {
    // Clear previous results and metrics
    postsContainer.innerHTML = '';
    
    // Remove any existing metrics
    const existingMetrics = document.querySelector('.performance-metrics');
    if (existingMetrics) {
        existingMetrics.remove();
    }
    
    const posts = data.posts;
    const metrics = data.metrics;
    
    // Update results count
    resultsCount.textContent = `${posts.length} post${posts.length !== 1 ? 's' : ''} generated`;
    
    // Create performance metrics display
    const metricsHtml = `
        <div class="performance-metrics">
            <div class="metrics-header">
                <i class="fas fa-chart-line"></i>
                Performance Metrics
            </div>
            <div class="metrics-content">
                <div class="metric-item">
                    <span class="metric-label">Generation Time:</span>
                    <span class="metric-value">${metrics.total_latency}s</span>
                </div>
                <div class="metric-item">
                    <span class="metric-label">Tokens Used:</span>
                    <span class="metric-value">${metrics.total_tokens.toLocaleString()}</span>
                </div>
                <div class="metric-item">
                    <span class="metric-label">API Calls:</span>
                    <span class="metric-value">${metrics.call_count}</span>
                </div>
                ${data.used_web_search ? `
                <div class="metric-item">
                    <span class="metric-label">Web Search:</span>
                    <span class="metric-value">${data.context_found ? '✅ Enhanced' : '⚠️ No results'}</span>
                </div>
                ` : ''}
            </div>
        </div>
    `;
    
    // Insert metrics before posts container
    postsContainer.insertAdjacentHTML('beforebegin', metricsHtml);
    
    // Create post cards
    posts.forEach((post, index) => {
        const postCard = createPostCard(post, index + 1);
        postsContainer.appendChild(postCard);
    });
    
    // Show results section
    showResults();
    
    // Scroll to results
    resultsSection.scrollIntoView({ 
        behavior: 'smooth', 
        block: 'start' 
    });
}

/**
 * Create a post card element
 */
function createPostCard(post, postNumber) {
    const card = document.createElement('div');
    card.className = 'post-card';
    
    // Format hashtags
    const hashtagsHtml = post.hashtags.map(tag => 
        `<span class="hashtag">${tag}</span>`
    ).join('');
    
    card.innerHTML = `
        <div class="post-header">
            <span class="post-number">Post ${postNumber}</span>
            <button class="copy-btn" onclick="copyPost(${postNumber - 1})">
                <i class="fas fa-copy"></i>
                Copy
            </button>
        </div>
        
        <div class="post-text">${escapeHtml(post.post_text)}</div>
        
        <div class="post-meta">
            <div class="hashtags">
                ${hashtagsHtml}
            </div>
            
            <div class="cta-section">
                <div class="cta-label">Call to Action:</div>
                <div class="cta-text">${escapeHtml(post.cta)}</div>
            </div>
        </div>
    `;
    
    return card;
}

/**
 * Copy post content to clipboard
 */
async function copyPost(postIndex) {
    try {
        const posts = getCurrentPosts();
        const post = posts[postIndex];
        
        if (!post) {
            throw new Error('Post not found');
        }
        
        // Format the complete post
        const fullPost = `${post.post_text}\n\n${post.hashtags.join(' ')}\n\n${post.cta}`;
        
        await navigator.clipboard.writeText(fullPost);
        
        // Visual feedback
        const copyBtn = document.querySelectorAll('.copy-btn')[postIndex];
        const originalText = copyBtn.innerHTML;
        
        copyBtn.innerHTML = '<i class="fas fa-check"></i> Copied!';
        copyBtn.style.background = '#28a745';
        
        setTimeout(() => {
            copyBtn.innerHTML = originalText;
            copyBtn.style.background = '';
        }, 2000);
        
        console.log('📋 Post copied to clipboard');
        
    } catch (error) {
        console.error('❌ Failed to copy post:', error);
        
        // Fallback for older browsers
        const copyBtn = document.querySelectorAll('.copy-btn')[postIndex];
        copyBtn.innerHTML = '<i class="fas fa-times"></i> Failed';
        copyBtn.style.background = '#dc3545';
        
        setTimeout(() => {
            copyBtn.innerHTML = '<i class="fas fa-copy"></i> Copy';
            copyBtn.style.background = '';
        }, 2000);
    }
}

/**
 * Get current posts data
 */
function getCurrentPosts() {
    // This is a simple way to store the current posts
    // In a real application, you might want to use a more robust state management solution
    return window.currentPosts || [];
}

/**
 * Store current posts data
 */
function setCurrentPosts(data) {
    window.currentPosts = data.posts || data; // Handle both old and new response formats
    window.currentData = data; // Store full response data
}

/**
 * Show results section
 */
function showResults() {
    resultsSection.classList.add('show');
}

/**
 * Hide results section
 */
function hideResults() {
    resultsSection.classList.remove('show');
}

/**
 * Show error message
 */
function showError(message) {
    errorText.textContent = message;
    errorSection.classList.add('show');
    
    // Scroll to error
    errorSection.scrollIntoView({ 
        behavior: 'smooth', 
        block: 'center' 
    });
}

/**
 * Clear error messages
 */
function clearErrors() {
    errorSection.classList.remove('show');
}

/**
 * Escape HTML to prevent XSS
 */
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

/**
 * Update results with current posts
 */
function updateDisplayedPosts() {
    const posts = getCurrentPosts();
    if (posts && posts.length > 0) {
        displayResults(posts);
    }
}

// Make copyPost function globally available
window.copyPost = copyPost;

// Store posts when displaying results
const originalDisplayResults = displayResults;
displayResults = function(data) {
    setCurrentPosts(data);
    originalDisplayResults(data);
};

// Health check on page load
document.addEventListener('DOMContentLoaded', async function() {
    try {
        const response = await fetch('/health');
        const health = await response.json();
        
        if (health.status === 'healthy') {
            console.log('✅ API is healthy');
            if (!health.api_configured) {
                console.warn('⚠️ API key not configured - will use mock responses');
            }
        }
    } catch (error) {
        console.error('❌ Health check failed:', error);
        showError('Unable to connect to the API. Please check if the server is running.');
    }
});
