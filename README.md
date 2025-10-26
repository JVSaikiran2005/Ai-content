# AI Content Generator

Unleash the power of the Gemini API to generate content on various topics. This simple web application allows users to input a prompt and receive AI-generated text content, such as stories, articles, or explanations.

## 🚀 Features

* **AI-Powered Generation:** Leverages the **Gemini 2.0 Flash** model via the Gemini API for fast, high-quality content generation.
* **Simple Interface:** A clean, responsive design built with **Tailwind CSS**.
* **Loading and Error Handling:** Provides clear visual feedback during content generation and displays informative error messages on failure.
* **Dynamic Styling:** Generated content is rendered with basic **prose styling** for improved readability.

## 🛠️ Technology Stack

* **Frontend:** HTML5, CSS (via Tailwind CSS CDN)
* **JavaScript:** Vanilla JavaScript for DOM manipulation and API calls.
* **API:** Google Gemini API (`gemini-2.0-flash` model).

## 📋 Prerequisites

Before running this project, you will need:

1.  A **Google AI API Key**.
2.  A way to serve the `index.html` file (e.g., a local web server, or simply opening the file in your browser).

## ⚙️ Setup and Installation

### 1. Get Your API Key

The provided `index.html` file includes an API key, but for a production-ready application, **you should replace this with a secure method of handling your key.**

For local testing, you can modify the `index.html` file:

1.  Open `index.html`.
2.  Find the following lines in the `<script>` block:

    ```javascript
    // API key (empty string as Canvas provides it at runtime for gemini-2.0-flash)
    const apiKey = "your api key"; // <-- REPLACE THIS
    ```

3.  Replace the placeholder value with your actual Google AI API Key.

### 2. Run the Application

Since this is a client-side application, you can run it in two ways:

1.  **Directly:** Simply open the `index.html` file in your web browser.
2.  **Using a Local Server (Recommended):** Use a tool like **Live Server** (VS Code Extension) or run a simple Python server:
    ```bash
    # In the project directory
    python -m http.server 8000
    ```
    Then, navigate to `http://localhost:8000` in your browser.

## 💻 Usage

1.  Open the application in your browser.
2.  Enter your desired topic or prompt into the **Your Topic** text area (e.g., *Write a short story about a futuristic city powered by renewable energy.*).
3.  Click the **Generate Content** button.
4.  The button will change to a loading state, and once the AI responds, the generated text will appear in the **Generated Content** section below.

## 📁 File Structure
