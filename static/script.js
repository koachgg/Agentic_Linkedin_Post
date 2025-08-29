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

// Streaming support
let useStreaming = true; // Toggle for streaming vs regular API calls

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
 * Handle form submission (original non-streaming version)
 */
async function handleFormSubmitOriginal(event) {
    event.preventDefault();
    
    if (isGenerating) return;
    
    if (!validateForm()) {
        showError('Please fill in all required fields correctly.');
        return;
    }
    
    try {
        setLoadingState(true);
        clearErrors();
        hideResults();
        
        const formData = getFormData();
        
        if (useStreaming) {
            await generatePostsStreaming(formData);
        } else {
            await generatePosts(formData);
        }
        
    } catch (error) {
        console.error('Generation error:', error);
        showError(error.message || 'An unexpected error occurred. Please try again.');
    } finally {
        setLoadingState(false);
    }
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
 * Generate posts using streaming API
 */
async function generatePostsStreaming(formData) {
    try {
        // Clear previous results
        postsContainer.innerHTML = '';
        let currentPosts = [];
        
        // Show initial progress
        showStreamingProgress('Initializing...', 0);
        
        const response = await fetch('/generate_posts_stream', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(formData)
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const reader = response.body.getReader();
        const decoder = new TextDecoder();
        
        while (true) {
            const { done, value } = await reader.read();
            if (done) break;
            
            const chunk = decoder.decode(value);
            const lines = chunk.split('\n');
            
            for (const line of lines) {
                if (line.startsWith('data: ')) {
                    try {
                        const data = JSON.parse(line.slice(6));
                        await handleStreamingUpdate(data, currentPosts);
                    } catch (e) {
                        console.warn('Failed to parse streaming data:', e);
                    }
                }
            }
        }
        
    } catch (error) {
        console.error('Streaming error:', error);
        throw error;
    }
}

/**
 * Handle individual streaming updates
 */
async function handleStreamingUpdate(data, currentPosts) {
    if (data.status) {
        // Status update
        showStreamingProgress(data.message, data.progress || 0);
    } else if (data.type === 'post') {
        // New post received
        currentPosts.push(data.data);
        addPostCard(data.data, data.index);
        updateResultsCount(currentPosts.length);
        showResults();
    } else if (data.type === 'metrics') {
        // Performance metrics
        showMetrics(data.data);
    } else if (data.type === 'complete') {
        // Generation complete
        hideStreamingProgress();
        showCompletionMessage(data.message);
        if (data.metrics) {
            showMetrics(data.metrics);
        }
    } else if (data.type === 'error') {
        // Error occurred
        hideStreamingProgress();
        throw new Error(data.message);
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
 * Create a post card element with feedback buttons
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
                <svg viewBox="0 0 24 24" width="16" height="16">
                    <path d="M16 1H4c-1.1 0-2 .9-2 2v14h2V3h12V1zm3 4H8c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h11c1.1 0 2-.9 2-2V7c0-1.1-.9-2-2-2zm0 16H8V7h11v14z"/>
                </svg>
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
            
            <div class="post-feedback">
                <span style="color: #6B7280; font-size: 0.875rem; font-weight: 500;">Was this helpful?</span>
                <button class="feedback-btn" onclick="submitFeedback(${postNumber - 1}, 'positive')">
                    <svg viewBox="0 0 24 24" width="16" height="16">
                        <path d="M1 21h4V9H1v12zm22-11c0-1.1-.9-2-2-2h-6.31l.95-4.57.03-.32c0-.41-.17-.79-.44-1.06L14.17 1 7.59 7.59C7.22 7.95 7 8.45 7 9v10c0 1.1.9 2 2 2h9c.83 0 1.54-.5 1.84-1.22l3.02-7.05c.09-.23.14-.47.14-.73v-1.91l-.01-.01L23 10z"/>
                    </svg>
                    <span>Helpful</span>
                </button>
                <button class="feedback-btn" onclick="submitFeedback(${postNumber - 1}, 'negative')">
                    <svg viewBox="0 0 24 24" width="16" height="16">
                        <path d="M15 3H6c-.83 0-1.54.5-1.84 1.22l-3.02 7.05c-.09.23-.14.47-.14.73v1.91l.01.01L1 14c0 1.1.9 2 2 2h6.31l-.95 4.57-.03.32c0 .41.17.79.44 1.06L9.83 23l6.59-6.59c.36-.36.58-.86.58-1.41V5c0-1.1-.9-2-2-2zm4 0v12h4V3h-4z"/>
                    </svg>
                    <span>Not helpful</span>
                </button>
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
 * Submit user feedback for a post
 */
async function submitFeedback(postIndex, rating) {
    try {
        const posts = getCurrentPosts();
        const post = posts[postIndex];
        
        if (!post) {
            throw new Error('Post not found');
        }
        
        // Prepare feedback data
        const feedbackData = {
            post_index: postIndex,
            rating: rating,
            post_preview: post.post_text.substring(0, 50) + '...',
            timestamp: new Date().toISOString()
        };
        
        // Send feedback to server
        const response = await fetch('/feedback', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(feedbackData)
        });
        
        if (!response.ok) {
            throw new Error(`Failed to submit feedback: ${response.statusText}`);
        }
        
        const result = await response.json();
        
        // Update UI to show feedback was submitted
        const feedbackButtons = document.querySelectorAll(`.post-card:nth-child(${postIndex + 1}) .feedback-btn`);
        feedbackButtons.forEach(btn => {
            btn.disabled = true;
            btn.style.opacity = '0.5';
        });
        
        // Highlight the selected feedback button
        const selectedButton = document.querySelector(
            `.post-card:nth-child(${postIndex + 1}) .feedback-btn[onclick*="${rating}"]`
        );
        if (selectedButton) {
            selectedButton.classList.add('active');
            selectedButton.style.opacity = '1';
        }
        
        console.log('📝 Feedback submitted:', result.message);
        
        // Optional: Show a brief success message
        showFeedbackConfirmation(rating);
        
    } catch (error) {
        console.error('❌ Failed to submit feedback:', error);
        // Could show an error message to the user
    }
}

/**
 * Show feedback confirmation message
 */
function showFeedbackConfirmation(rating) {
    // Create a temporary success message
    const message = document.createElement('div');
    message.className = 'feedback-confirmation';
    message.textContent = `Thank you for your ${rating} feedback!`;
    message.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: #10B981;
        color: white;
        padding: 12px 20px;
        border-radius: 8px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
        z-index: 1000;
        font-size: 0.875rem;
        font-weight: 500;
        animation: slideInRight 0.3s ease;
    `;
    
    document.body.appendChild(message);
    
    // Remove after 3 seconds
    setTimeout(() => {
        message.style.animation = 'slideOutRight 0.3s ease';
        setTimeout(() => {
            document.body.removeChild(message);
        }, 300);
    }, 3000);
}

/**
 * Add a single post card (for streaming)
 */
function addPostCard(post, index) {
    const postCard = createPostCard(post, index + 1);
    postsContainer.appendChild(postCard);
    
    // Add animation
    setTimeout(() => {
        postCard.style.opacity = '1';
        postCard.style.transform = 'translateY(0)';
    }, 100);
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

/**
 * Show streaming progress indicator
 */
function showStreamingProgress(message, progress) {
    // Create or update progress indicator
    let progressElement = document.getElementById('streamingProgress');
    if (!progressElement) {
        progressElement = document.createElement('div');
        progressElement.id = 'streamingProgress';
        progressElement.className = 'streaming-progress';
        progressElement.innerHTML = `
            <div class="progress-message"></div>
            <div class="progress-bar">
                <div class="progress-fill"></div>
            </div>
            <div class="progress-percentage"></div>
        `;
        
        // Insert before results section
        resultsSection.parentNode.insertBefore(progressElement, resultsSection);
    }
    
    progressElement.querySelector('.progress-message').textContent = message;
    progressElement.querySelector('.progress-fill').style.width = `${progress}%`;
    progressElement.querySelector('.progress-percentage').textContent = `${Math.round(progress)}%`;
    progressElement.style.display = 'block';
}

/**
 * Hide streaming progress indicator
 */
function hideStreamingProgress() {
    const progressElement = document.getElementById('streamingProgress');
    if (progressElement) {
        progressElement.style.display = 'none';
    }
}

/**
 * Show completion message
 */
function showCompletionMessage(message) {
    // Could show a toast or update UI to indicate completion
    console.log('✅ Generation complete:', message);
}
