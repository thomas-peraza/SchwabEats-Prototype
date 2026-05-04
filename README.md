# Schwabeats Prototype – README

## Overview

This project contains a MVP system with two main portals:

* **Employee Portal**
* **Vendor Portal**

For testing purposes, please use the provided hard-coded credentials

---

## Login Credentials

### Employee Portal

* **Employee Name:** John Smith
* **Login ID:** `john-smith123`
* **Password:** `jsmith2026`

### Vendor Portal

* **Vendor ID:** `pasta_corner_dallas_vendor`
* **Password:** `PC2026`

---

## Running the Project

**Two** terminals are needed to run the frontend and backend

### 1. Start the Backend

In the first terminal, navigate to the backend directory and run:

```bash
python3 app.py
```

---

### 2. Start the Frontend

In a second terminal, navigate to the main project directory and run:

```bash
npm install
npm run dev
```

---

## Testing the Application

1. Open the `localhost` link you are provided after running  `npm run dev`. This will open the login portal in your browser

2. Choose a portal to log in:

   * Employee Portal → use employee credentials
   * Vendor Portal → use vendor credentials

3. Verify:

   * Successful login with correct credentials
   * Access to appropriate dashboard (Employee vs Vendor)
   * Any core features (menu viewing, recommendations, vendor actions, etc.)

