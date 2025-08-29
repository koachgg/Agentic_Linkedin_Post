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
let useStreaming = true; // Re-enable streaming - issue was missing updateResultsCount function

// Event listeners
document.addEventListener('DOMContentLoaded', function() {
    console.log('🚀 DOM loaded, initializing...');
    
    // Check if all required elements exist
    if (!postForm) {
        console.error('❌ postForm element not found');
        return;
    }
    if (!generateBtn) {
        console.error('❌ generateBtn element not found');
        return;
    }
    if (!topicInput) {
        console.error('❌ topicInput element not found');
        return;
    }
    
    console.log('✅ All elements found, attaching listeners...');
    
    // Form submission
    postForm.addEventListener('submit', handleFormSubmit);
    
    // Backup: Handle button click directly
    generateBtn.addEventListener('click', function(event) {
        console.log('🔘 Generate button clicked directly');
        if (event.target.type === 'submit') {
            // Let the form handle it
            return;
        }
        handleFormSubmit(event);
    });
    
    // Real-time validation
    topicInput.addEventListener('input', validateForm);
    postCountInput.addEventListener('input', validatePostCount);
    
    // Clear errors on input
    topicInput.addEventListener('input', clearErrors);
    
    // Add keyboard shortcut for testing (Ctrl+Shift+T)
    document.addEventListener('keydown', function(event) {
        if (event.ctrlKey && event.shiftKey && event.key === 'T') {
            event.preventDefault();
            console.log('🧪 Running form submission test...');
            testFormSubmission();
        }
    });
    
    console.log('🚀 LinkedIn Post Generator loaded successfully');
    console.log('💡 Press Ctrl+Shift+T to test form submission');
    
    // Test API connectivity
    testAPIConnection();
});

/**
 * Handle form submission with streaming support
 */
async function handleFormSubmit(event) {
    console.log('🚀 Form submitted!', event);
    console.log('🚀 Event type:', event.type);
    console.log('🚀 Event target:', event.target);
    event.preventDefault();
    
    if (isGenerating) {
        console.log('⚠️ Already generating, skipping...');
        return;
    }
    
    if (!validateForm()) {
        console.log('❌ Form validation failed');
        showError('Please fill in all required fields correctly.');
        return;
    }
    
    console.log('✅ Form validation passed, starting generation...');
    
    try {
        setLoadingState(true);
        clearErrors();
        hideResults();
        
        const formData = getFormData();
        console.log('📤 Form data:', formData);
        
        if (useStreaming) {
            console.log('⚡ Using streaming API...');
            try {
                await generatePostsStreaming(formData);
            } catch (error) {
                console.error('❌ Streaming failed, falling back to regular API:', error);
                showError('Streaming failed, using regular generation...', 'warning');
                await generatePosts(formData);
            }
        } else {
            console.log('📡 Using regular API...');
            await generatePosts(formData);
        }
        
    } catch (error) {
        console.error('❌ Generation error:', error);
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
        
        const data = await response.json();
        
        console.log('📥 Received response:', data);
        
        if (!data || !data.posts) {
            throw new Error('Invalid response: missing posts data');
        }
        
        console.log('✅ Valid response received, displaying results...');
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
        console.log('⚡ Starting streaming generation...');
        
        // Clear previous results
        postsContainer.innerHTML = '';
        let currentPosts = [];
        
        // Show initial progress
        showStreamingProgress('Initializing...', 0);
        
        console.log('📤 Sending streaming request to /generate_posts_stream');
        const response = await fetch('/generate_posts_stream', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(formData)
        });
        
        console.log('📥 Streaming response received:', response.status, response.statusText);
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        if (!response.body) {
            throw new Error('Response body is null - streaming not supported');
        }
        
        const reader = response.body.getReader();
        const decoder = new TextDecoder();
        let buffer = '';
        
        console.log('📖 Starting to read stream...');
        
        let streamTimeout = setTimeout(() => {
            console.warn('⏰ Streaming timeout - no data received in 30 seconds');
            reader.cancel();
        }, 30000); // 30 second timeout
        
        while (true) {
            const { done, value } = await reader.read();
            if (done) {
                console.log('📥 Stream completed');
                clearTimeout(streamTimeout);
                break;
            }
            
            // Reset timeout on each chunk
            clearTimeout(streamTimeout);
            streamTimeout = setTimeout(() => {
                console.warn('⏰ Streaming timeout - no data received in 30 seconds');
                reader.cancel();
            }, 30000);
            
            const chunk = decoder.decode(value);
            console.log('📥 Received chunk:', chunk);
            
            // Add to buffer and process complete lines
            buffer += chunk;
            const lines = buffer.split('\n');
            
            // Keep the last incomplete line in buffer
            buffer = lines.pop() || '';
            
            for (const line of lines) {
                console.log('🔍 Processing line:', line);
                if (line.startsWith('data: ')) {
                    try {
                        const jsonData = line.slice(6);
                        console.log('📋 JSON data:', jsonData);
                        
                        if (jsonData.trim()) {
                            const data = JSON.parse(jsonData);
                            console.log('📦 Parsed data:', data);
                            await handleStreamingUpdate(data, currentPosts);
                        }
                    } catch (e) {
                        console.warn('❌ Failed to parse streaming data:', e, 'Line:', line);
                    }
                } else if (line.trim()) {
                    console.log('⚠️ Non-data line:', line);
                }
            }
        }
        
        // Process any remaining buffer
        if (buffer.trim()) {
            console.log('🔍 Processing final buffer:', buffer);
        }
        
    } catch (error) {
        console.error('❌ Streaming error:', error);
        hideStreamingProgress();
        throw error;
    }
}

/**
 * Handle individual streaming updates
 */
async function handleStreamingUpdate(data, currentPosts) {
    console.log('🔄 Handling streaming update:', data);
    
    if (data.status) {
        // Status update
        console.log('📊 Status update:', data.message, data.progress);
        showStreamingProgress(data.message, data.progress || 0);
    } else if (data.type === 'post') {
        // New post received
        console.log('📝 New post received:', data.data);
        currentPosts.push(data.data);
        
        // Store updated posts globally for copying
        window.currentPosts = currentPosts;
        
        addPostCard(data.data, data.index);
        updateResultsCount(currentPosts.length);
        showResults();
    } else if (data.type === 'metrics') {
        // Performance metrics
        console.log('📈 Metrics received:', data.data);
        showMetrics(data.data);
    } else if (data.type === 'complete') {
        // Generation complete
        console.log('✅ Generation complete:', data.message);
        
        // Ensure all posts are stored globally
        if (data.posts && data.posts.length > 0) {
            console.log('💾 Storing completed posts:', data.posts);
            window.currentPosts = data.posts;
        } else {
            console.log('💾 Using accumulated posts:', currentPosts);
            window.currentPosts = currentPosts;
        }
        
        hideStreamingProgress();
        showCompletionMessage(data.message);
        if (data.metrics) {
            showMetrics(data.metrics);
        }
    } else if (data.type === 'error') {
        // Error occurred
        console.log('❌ Streaming error:', data.message);
        hideStreamingProgress();
        throw new Error(data.message);
    } else {
        console.log('❓ Unknown streaming data type:', data);
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
    console.log('🎨 displayResults called with:', data);
    
    // Store posts data for copying
    setCurrentPosts(data);
    
    // Clear previous results and metrics
    postsContainer.innerHTML = '';
    
    // Remove any existing metrics
    const existingMetrics = document.querySelector('.performance-metrics');
    if (existingMetrics) {
        existingMetrics.remove();
    }
    
    const posts = data.posts;
    const metrics = data.metrics;
    
    console.log('📝 Posts to display:', posts.length);
    console.log('📊 Metrics:', metrics);
    
    // Update results count
    resultsCount.textContent = `${posts.length} post${posts.length !== 1 ? 's' : ''} generated`;
    
    // Create performance metrics display
    const metricsHtml = `
        <div class="performance-metrics">
            <div class="metrics-header">
                <svg viewBox="0 0 24 24">
                    <path d="M16,11.78L20.24,4.45L21.97,5.45L16.74,14.5L10.23,10.75L5.46,19H22V21H2V3H4V17.54L9.5,8L16,11.78Z"/>
                </svg>
                Generation Summary
            </div>
            <div class="metrics-content">
                <div class="metric-item">
                    <span class="metric-label">Generation Time:</span>
                    <span class="metric-value">${Math.round(metrics.total_latency * 10) / 10}s</span>
                </div>
                <div class="metric-item">
                    <span class="metric-label">Content Quality:</span>
                    <span class="metric-value">✅ AI Enhanced</span>
                </div>
                ${data.used_web_search ? `
                <div class="metric-item">
                    <span class="metric-label">Web Research:</span>
                    <span class="metric-value">${data.context_found ? '✅ Enhanced with latest data' : '⚠️ No recent data found'}</span>
                </div>
                ` : `
                <div class="metric-item">
                    <span class="metric-label">Source:</span>
                    <span class="metric-value">📚 AI Knowledge Base</span>
                </div>
                `}
                <div class="metric-item">
                    <span class="metric-label">Posts Generated:</span>
                    <span class="metric-value">${posts.length} unique posts</span>
                </div>
            </div>
        </div>
    `;
    
    // Insert metrics before posts container
    postsContainer.insertAdjacentHTML('beforebegin', metricsHtml);
    console.log('📊 Metrics inserted');
    
    // Create post cards
    console.log('🔨 Creating post cards...');
    posts.forEach((post, index) => {
        console.log(`📝 Creating post ${index + 1}:`, post);
        const postCard = createPostCard(post, index + 1);
        postsContainer.appendChild(postCard);
        console.log(`✅ Post ${index + 1} added to container`);
    });
    
    console.log('📦 Total posts in container:', postsContainer.children.length);
    
    // Show results section
    console.log('👁️ Showing results section...');
    showResults();
    
    // Scroll to results
    console.log('📜 Scrolling to results...');
    resultsSection.scrollIntoView({ 
        behavior: 'smooth', 
        block: 'start' 
    });
    
    console.log('✅ displayResults completed');
}

/**
 * Update the results count display
 */
function updateResultsCount(count) {
    if (resultsCount) {
        resultsCount.textContent = `${count} post${count !== 1 ? 's' : ''} generated`;
    }
}

/**
 * Show the results section
 */
function showResults() {
    if (resultsSection) {
        resultsSection.classList.add('show');
    }
}

/**
 * Hide the results section
 */
function hideResults() {
    if (resultsSection) {
        resultsSection.classList.remove('show');
    }
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
        console.log('📋 Attempting to copy post', postIndex);
        const posts = getCurrentPosts();
        console.log('📋 Available posts:', posts.length);
        
        const post = posts[postIndex];
        
        if (!post) {
            throw new Error(`Post ${postIndex} not found. Available: ${posts.length}`);
        }
        
        // Format the complete post
        const fullPost = `${post.post_text}\n\n${post.hashtags.join(' ')}\n\n${post.cta}`;
        console.log('📋 Formatted post:', fullPost.substring(0, 100) + '...');
        
        // Try modern clipboard API first
        if (navigator.clipboard && navigator.clipboard.writeText) {
            await navigator.clipboard.writeText(fullPost);
            console.log('✅ Copied using modern clipboard API');
        } else {
            // Fallback for older browsers
            const textArea = document.createElement('textarea');
            textArea.value = fullPost;
            textArea.style.position = 'fixed';
            textArea.style.opacity = '0';
            document.body.appendChild(textArea);
            textArea.select();
            document.execCommand('copy');
            document.body.removeChild(textArea);
            console.log('✅ Copied using fallback method');
        }
        
        // Visual feedback
        const copyBtn = document.querySelectorAll('.copy-btn')[postIndex];
        if (copyBtn) {
            const originalText = copyBtn.innerHTML;
            
            copyBtn.innerHTML = `
                <svg viewBox="0 0 24 24" width="16" height="16">
                    <path d="M9 16.2L4.8 12l-1.4 1.4L9 19 21 7l-1.4-1.4L9 16.2z"/>
                </svg>
                Copied!
            `;
            copyBtn.style.background = '#10B981';
            
            setTimeout(() => {
                copyBtn.innerHTML = originalText;
                copyBtn.style.background = '';
            }, 2000);
        }
        
        console.log('✅ Post copied to clipboard successfully');
        
    } catch (error) {
        console.error('❌ Failed to copy post:', error);
        
        // Error feedback
        const copyBtn = document.querySelectorAll('.copy-btn')[postIndex];
        if (copyBtn) {
            copyBtn.innerHTML = `
                <svg viewBox="0 0 24 24" width="16" height="16">
                    <path d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"/>
                </svg>
                Failed
            `;
            copyBtn.style.background = '#EF4444';
            
            setTimeout(() => {
                copyBtn.innerHTML = `
                    <svg viewBox="0 0 24 24" width="16" height="16">
                        <path d="M16 1H4c-1.1 0-2 .9-2 2v14h2V3h12V1zm3 4H8c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h11c1.1 0 2-.9 2-2V7c0-1.1-.9-2-2-2zm0 16H8V7h11v14z"/>
                    </svg>
                    Copy
                `;
                copyBtn.style.background = '';
            }, 2000);
        }
        
        // Show user-friendly error message
        showError(`Failed to copy post: ${error.message}`, 'error');
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
    console.log('🔍 getCurrentPosts called, window.currentPosts:', window.currentPosts);
    return window.currentPosts || [];
}

/**
 * Store current posts data
 */
function setCurrentPosts(data) {
    console.log('💾 setCurrentPosts called with:', data);
    window.currentPosts = data.posts || data; // Handle both old and new response formats
    window.currentData = data; // Store full response data
    console.log('💾 Stored posts:', window.currentPosts);
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
 * Show error or success message
 */
function showError(message, type = 'error') {
    errorText.textContent = message;
    
    // Apply different styling based on type
    if (type === 'success') {
        errorSection.style.background = 'rgba(16, 185, 129, 0.1)';
        errorSection.style.borderColor = '#10B981';
        errorSection.querySelector('svg path').setAttribute('d', 'M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z');
    } else {
        errorSection.style.background = 'rgba(239, 68, 68, 0.05)';
        errorSection.style.borderColor = '#EF4444';
        errorSection.querySelector('svg path').setAttribute('d', 'M1 21h22L12 2 1 21zm12-3h-2v-2h2v2zm0-4h-2v-4h2v4z');
    }
    
    errorSection.classList.add('show');
    
    // Scroll to message
    errorSection.scrollIntoView({ 
        behavior: 'smooth', 
        block: 'center' 
    });
    
    // Auto-hide success messages after 5 seconds
    if (type === 'success') {
        setTimeout(() => {
            clearErrors();
        }, 5000);
    }
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

/**
 * Test API connectivity on page load
 */
async function testAPIConnection() {
    try {
        console.log('🔍 Testing API connectivity...');
        const response = await fetch('/health');
        
        if (response.ok) {
            const data = await response.json();
            console.log('✅ API is healthy:', data);
        } else {
            console.warn('⚠️ API health check failed:', response.status);
        }
    } catch (error) {
        console.error('❌ API connectivity test failed:', error);
    }
}

/**
 * Test form submission with a simple endpoint
 */
async function testFormSubmission() {
    try {
        const formData = getFormData();
        console.log('🧪 Testing form submission with data:', formData);
        
        const response = await fetch('/test', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(formData)
        });
        
        if (response.ok) {
            const data = await response.json();
            console.log('✅ Test successful:', data);
            showError(`Test successful! Received: ${JSON.stringify(data.received_data)}`, 'success');
        } else {
            console.error('❌ Test failed:', response.status);
            showError(`Test failed: ${response.status} ${response.statusText}`);
        }
    } catch (error) {
        console.error('❌ Test error:', error);
        showError(`Test error: ${error.message}`);
    }
}

/**
 * Show metrics in a user-friendly way
 */
function showMetrics(metrics) {
    // Remove any existing metrics
    const existingMetrics = document.querySelector('.performance-metrics');
    if (existingMetrics) {
        existingMetrics.remove();
    }
    
    const metricsHtml = `
        <div class="performance-metrics">
            <div class="metrics-header">
                <svg viewBox="0 0 24 24">
                    <path d="M16,11.78L20.24,4.45L21.97,5.45L16.74,14.5L10.23,10.75L5.46,19H22V21H2V3H4V17.54L9.5,8L16,11.78Z"/>
                </svg>
                Generation Summary
            </div>
            <div class="metrics-content">
                <div class="metric-item">
                    <span class="metric-label">Generation Time:</span>
                    <span class="metric-value">${Math.round(metrics.total_latency * 10) / 10}s</span>
                </div>
                <div class="metric-item">
                    <span class="metric-label">Content Quality:</span>
                    <span class="metric-value">✅ AI Enhanced</span>
                </div>
                <div class="metric-item">
                    <span class="metric-label">Processing Status:</span>
                    <span class="metric-value">✅ Complete</span>
                </div>
            </div>
        </div>
    `;
    
    // Insert metrics before posts container
    postsContainer.insertAdjacentHTML('beforebegin', metricsHtml);
}

/**
 * Debug function to check current state (call from browser console)
 */
window.debugPosts = function() {
    console.log('=== DEBUG POSTS ===');
    console.log('window.currentPosts:', window.currentPosts);
    console.log('window.currentData:', window.currentData);
    console.log('Posts in DOM:', document.querySelectorAll('.post-card').length);
    console.log('Copy buttons in DOM:', document.querySelectorAll('.copy-btn').length);
    console.log('==================');
};
