const API_URL = "https://n9wz0wttxk.execute-api.us-east-1.amazonaws.com/prod";

// Function to fetch and display blog posts
async function fetchPosts() {
    try {
        const response = await fetch(`${API_URL}/posts`);

        if (!response.ok) throw new Error(`Error fetching posts: ${response.statusText}`);

        // Log raw response for debugging
        const jsonResponse = await response.json();
        console.log("Raw API Response:", jsonResponse);

        // Handle cases where the API response wraps the array inside a "body" field
        let posts = jsonResponse;

        if (jsonResponse.body) {
            try {
                posts = JSON.parse(jsonResponse.body);
            } catch (e) {
                console.error("Error parsing JSON body:", e);
            }
        }

        if (!Array.isArray(posts)) throw new Error("Invalid data format: Expected an array.");

        console.log("Final Posts Array:", posts);

        displayPosts(posts);
    } catch (error) {
        console.error("Error fetching posts:", error);
        document.getElementById("posts-container").innerHTML = `<p class="error">Failed to load posts. Please try again later.</p>`;
    }
}

// Function to display posts in the UI
function displayPosts(posts) {
    const postsContainer = document.getElementById("posts-container");
    postsContainer.innerHTML = ""; // Clear previous posts

    if (posts.length === 0) {
        postsContainer.innerHTML = `<p>No blog posts found.</p>`;
        return;
    }

    posts.forEach(post => {
        const postElement = document.createElement("div");
        postElement.classList.add("post");
        postElement.innerHTML = `
            <h3>${post.title}</h3>
            <p>${post.content}</p>
            <small>Posted on: ${new Date(post.createdAt).toLocaleString()}</small>
            
            <button onclick="toggleComments('${post.postId}')">View Comments</button>
            <div id="comments-${post.postId}" class="comments-section" style="display: none;"></div>

            <div class="comment-box">
                <input type="text" id="comment-input-${post.postId}" placeholder="Write a comment...">
                <button onclick="submitComment('${post.postId}')">Submit Comment</button>
            </div>
        `;
        postsContainer.appendChild(postElement);
    });
}

// Function to submit a new blog post
async function submitPost() {
    const title = document.getElementById("post-title").value.trim();
    const content = document.getElementById("post-content").value.trim();

    // Validate inputs
    if (!title || !content) {
        alert("Title and content cannot be empty.");
        return;
    }

    const requestBody = JSON.stringify({ title, content });

    console.log("Submitting Post:", requestBody);

    try {
        const response = await fetch(`${API_URL}/posts`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: requestBody
        });

        const jsonResponse = await response.json();
        console.log("API Response:", jsonResponse);

        if (!response.ok) throw new Error(jsonResponse.message || "Failed to submit post.");

        alert("Post submitted successfully!");
        document.getElementById("post-title").value = ""; // Clear input fields
        document.getElementById("post-content").value = "";
        fetchPosts(); // Refresh posts
    } catch (error) {
        console.error("Error submitting post:", error);
        alert(`Error submitting post: ${error.message}`);
    }
}

// Function to submit a new comment (Fix 1)
async function submitComment(postId) {
    const commentInput = document.getElementById(`comment-input-${postId}`);
    const commentText = commentInput.value.trim();

    if (!commentText) {
        alert("Comment cannot be empty.");
        return;
    }

    const requestBody = JSON.stringify({
        postId: postId,
        comment: commentText
    });

    try {
        const response = await fetch(`${API_URL}/comment`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: requestBody
        });

        const jsonResponse = await response.json();
        console.log("API Response:", jsonResponse);

        if (!response.ok) throw new Error(jsonResponse.message || "Failed to submit comment.");

        alert("Comment submitted successfully!");
        commentInput.value = ""; // Clear input field
        toggleComments(postId); // Refresh comments
    } catch (error) {
        console.error("Error submitting comment:", error);
        alert(`Error submitting comment: ${error.message}`);
    }
}

// Function to fetch and display comments 
async function toggleComments(postId) {
    const commentsSection = document.getElementById(`comments-${postId}`);
    if (commentsSection.style.display === "none") {
        commentsSection.style.display = "block";

        try {
            const response = await fetch(`${API_URL}/comment?postId=${postId}`);

            if (!response.ok) throw new Error(`Error fetching comments: ${response.statusText}`);

            const jsonResponse = await response.json();
            console.log("Fetched Comments:", jsonResponse);

            const comments = Array.isArray(jsonResponse) ? jsonResponse : [];

            if (!Array.isArray(comments)) throw new Error("Invalid data format: Expected an array.");
            comments.sort((a, b) => new Date(a.createdAt) - new Date(b.createdAt));

            commentsSection.innerHTML = comments.length
                ? comments.map(comment => `<p>${comment.comment} <small>(${new Date(comment.createdAt).toLocaleString()})</small></p>`).join("")
                : `<p>No comments yet.</p>`;
        } catch (error) {
            console.error("Error fetching comments:", error);
            commentsSection.innerHTML = `<p class="error">Failed to load comments. Please try again later.</p>`;
        }
    } else {
        commentsSection.style.display = "none";
    }
}

// Fetch all posts when page loads
window.onload = fetchPosts;
