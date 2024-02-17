document.getElementById('send-btn').addEventListener('click', function() {
    const userInput = document.getElementById('user-input').value;
    if (userInput.trim() !== '') {
        displayMessage(userInput, 'user');
        fetchResponse(userInput);
        document.getElementById('user-input').value = ''; // Clear the input field after sending
    }
});

function displayMessage(message, sender) {
    const messageElement = document.createElement('div');
    messageElement.classList.add('message', sender);
    messageElement.textContent = message;
    document.getElementById('chat-window').appendChild(messageElement);
    document.getElementById('chat-window').scrollTop = document.getElementById('chat-window').scrollHeight; // Scroll to the latest message
}

async function fetchResponse(query) {
    try {
        const response = await fetch('/ask', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ query: query }),
        });

        if (response.ok) {
            const data = await response.json();
            displayMessage(data.response, 'bot');
        } else {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
    } catch (error) {
        console.error("Fetch error: " + error);
        displayMessage("Sorry, I couldn't fetch the response. Please try again later.", 'bot');
    }
}
