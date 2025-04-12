# AI Workshop

Welcome to the AI Workshop project! This repository contains all the materials and code for our AI workshop.

## Table of Contents

- [Introduction](#introduction)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Introduction

In this workshop, we will explore various AI techniques and tools. The goal is to provide hands-on experience with AI development.

## Installation

To get started, clone the repository and install the necessary dependencies:

```bash
git clone https://github.com/yourusername/AI-Workshop.git
cd AI-Workshop
python -m venv venv
venv\Scripts\activate.bat
pip install -r requirements.txt
```
# Create a .env file and add OPENAI_API_KEY

# 🔑 Setting Up OAuth Credentials for Google Calendar API

Follow these steps to configure OAuth 2.0 authentication for the Google Calendar API.

## **1️⃣ Create a Google Cloud Project**

1. Go to [Google Cloud Console](https://console.cloud.google.com/).
2. Select an existing project or click **"Create Project"**.
3. Enter a project name (e.g., `Google Calendar Integration`) and click **Create**.

---

## **2️⃣ Enable Google Calendar API**

1. In **Google Cloud Console**, go to **APIs & Services > Library**.
2. Search for **Google Calendar API**.
3. Click **Enable**.

---

## **3️⃣ Create OAuth 2.0 Credentials**

1. Navigate to **APIs & Services > Credentials**.
2. Click **"Create Credentials"** and select **"OAuth client ID"**.
3. If prompted to set up an **OAuth consent screen**, follow these steps:

   - Click **Configure consent screen**.
   - Choose **External** (for testing) or **Internal** (for organization use).
   - Fill in the required fields (App Name, User Support Email, etc.).
   - Under **Scopes**, click **"Add or Remove Scopes"** and add:
     ```
     https://www.googleapis.com/auth/calendar
     https://www.googleapis.com/auth/calendar.events
     ```
   - Click **Save and Continue**.

4. Now, create OAuth credentials:
   - Select **Application Type: "Web App"**.
   - Enter a name (e.g., `Google Calendar App`).
   - Add redirect url: http://localhost:63275/
   - Click **Create**.
   - Download the `credentials.json` file.

---

## **4️⃣ Place `credentials.json` in Your Project**

1. Move the downloaded `credentials.json` to your project's root directory.
2. Ensure the file is accessible by your script.

## Usage

Follow the instructions in the workshop materials to run the examples and exercises. You can find the materials in the `materials` directory.

## Contributing

We welcome contributions! Please read our [contributing guidelines](CONTRIBUTING.md) for more details.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more information.
