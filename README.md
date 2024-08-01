# BobcatCLAWS

BobcatCLAWS (Cost-effective Living and Academic Wellness Solutions) is a web application designed to aid college students in finding cost-effective essentials. The application integrates product comparison features, provides an intuitive user interface, and implements seamless navigation to enhance the online shopping experience for students.

## Table of Contents

- [Description](#description)
- [Features](#features)
- [Technologies](#technologies)
- [Installation](#installation)

## Description

BobcatCLAWS is a user-centric web application developed to help college students save money on essential items. The application aggregates data from multiple retail stores, allowing users to compare prices and find the best deals. It features a clean and intuitive interface with maroon and gold themes, seamless navigation, and robust backend support.

## Features

- Product search and comparison
- User-friendly interface with maroon and gold themes
- Seamless navigation
- Integration with multiple retail APIs
- Backend support for data storage and retrieval

## Technologies

- **Frontend**: React, HTML, CSS, JavaScript
- **Backend**: Node.js, MongoDB, MySQL, Flask, Django
- **APIs**: Various retail store APIs
- **Data Analysis**: Python scripts for data aggregation and comparison

## Installation

Follow these steps to set up and run BobcatCLAWS locally:

```bash
# Clone the repository
git clone https://github.com/yourusername/bobcatclaws.git

# Navigate to the project directory
cd bobcatclaws

# Install frontend dependencies
cd frontend
npm install

# Install backend dependencies
cd ../backend
npm install

# Set up environment variables
cp .env.example .env

# Start the backend server
npm start

# In a new terminal window, start the frontend server
cd ../frontend
npm start
