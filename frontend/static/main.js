// Define the global variable to store the current post ID
var currentPostId = null;

// Function that runs once the window is fully loaded
window.onload = function() {
    // Attempt to retrieve the API base URL from the local storage
    var savedBaseUrl = localStorage.getItem('apiBaseUrl');
    // If a base URL is found in local storage, load the posts
    if (savedBaseUrl) {
        document.getElementById('api-base-url').value = savedBaseUrl;
        loadPosts();
    }
}

// Function to fetch all the posts from the API and display them on the page
function loadPosts() {
    // Retrieve the base URL from the input field and save it to local storage
    var baseUrl = document.getElementById('api-base-url').value;
    localStorage.setItem('apiBaseUrl', baseUrl);

    // Use the Fetch API to send a GET request to the /posts endpoint
    fetch(baseUrl + '/posts')
        .then(response => response.json())  // Parse the JSON data from the response
        .then(data => {  // Once the data is ready, we can use it
            // Clear out the post container first
            const postContainer = document.getElementById('post-container');
            postContainer.innerHTML = '';

            // For each post in the response, create a new post element and add it to the page
            data.forEach(post => {
                const postDiv = document.createElement('div');
                postDiv.className = 'post';
                postDiv.id = `post-${post.id}`;
                postDiv.innerHTML = `<h2>${post.title}</h2>
                <p><small>By: <strong>${post.author}</strong> on ${post.post_date}</small></p>
                <p>${post.content}</p>
                <div class="button-container">
                        <button id="delete-post-${post.id}" class="delete" onclick="deletePost(${post.id})">Delete</button>
                        <button id="update-post-${post.id}" class="update" onclick="prepareUpdate(${post.id}, '${post.title}', '${post.content}', '${post.author}')">Update</button>
                </div>`;
            postContainer.appendChild(postDiv);
            });
        })
        .catch(error => console.error('Error:', error));  // If an error occurs, log it to the console
}

// Function to prepare for updating a post
function prepareUpdate(postId, title, content, author) {
    currentPostId = postId;
    document.getElementById('post-title').value = title;
    document.getElementById('post-content').value = content;
    document.getElementById('post-author').value = author;
    document.getElementById('add-post-btn').style.display = 'none';
    document.getElementById('update-post-btn').style.display = 'inline';
    window.scrollTo(0,0)
}

// Function to send a POST request to the API to add a new post
function addPost() {
    // Retrieve the values from the input fields
    var baseUrl = document.getElementById('api-base-url').value;
    var postTitle = document.getElementById('post-title').value;
    var postContent = document.getElementById('post-content').value;
    var postAuthor = document.getElementById('post-author').value || 'Anonymous';
    var postDate = new Date().toISOString().split('T')[0];  // Formats the date as 'YYYY-MM-DD'

    // Use the Fetch API to send a POST request to the /posts endpoint
    fetch(baseUrl + '/posts', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            title: postTitle,
            content: postContent,
            author: postAuthor,
            post_date: postDate })
    })
    .then(response => response.json())  // Parse the JSON data from the response
    .then(post => {
        console.log('Post added:', post);
        loadPosts(); // Reload the posts after adding a new one
    })
    .catch(error => console.error('Error:', error));  // If an error occurs, log it to the console
}

// Function to clear input fields
function clearInputs() {
    console.log("Hahaha")
    document.getElementById('post-title').value = '';
    document.getElementById('post-content').value = '';
    document.getElementById('post-author').value = '';
    document.getElementById('add-post-btn').style.display = 'inline';
    document.getElementById('update-post-btn').style.display = 'none';
}

// Function to send a DELETE request to the API to delete a post
function deletePost(postId) {
    var baseUrl = document.getElementById('api-base-url').value;

    // Use the Fetch API to send a DELETE request to the specific post's endpoint
    fetch(baseUrl + '/posts/' + postId, {
        method: 'DELETE'
    })
    .then(response => {
        console.log('Post deleted:', postId);
        loadPosts(); // Reload the posts after deleting one
    })
    .catch(error => console.error('Error:', error));  // If an error occurs, log it to the console
}

// Function to send a PUT request to update a post
function updateExistingPost() {
    const baseUrl = document.getElementById('api-base-url').value;
    const postTitle = document.getElementById('post-title').value;
    const postContent = document.getElementById('post-content').value;
    const postAuthor = document.getElementById('post-author').value || 'Anonymous';

    fetch(`${baseUrl}/posts/${currentPostId}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            title: postTitle,
            content: postContent,
            author: postAuthor
        })
    })
    .then(response => response.json())  // Parse the JSON data from the response
    .then(post => {
        console.log('Post added:', post);
        console.log('post-'+ post.post_id)
        const targetDiv = document.getElementById('post-'+ post.post_id)
        targetDiv.scrollIntoView()
        clearInputs();
        loadPosts(); // Reload the posts after adding a new one
    })

    .catch(error => console.error('Error updating post:', error));
}
