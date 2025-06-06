PantryPal - Elegant Pantry Management Web Application
Welcome to PantryPal, a full-stack serverless web application designed to help users elegantly manage their household pantry inventory. This project features a dynamic, responsive frontend with a unique "fancy wedding invitation" aesthetic and a robust backend built on AWS.


Live Demo (S3 Hosted): http://my-pantry-items-jordon.s3-website-us-east-1.amazonaws.com

Note: This demo was initially hosted on a temporary AWS Learner Lab environment and may no longer be active if the lab session has expired. Please see the screenshots for a demonstration of the working application.


📋 Project Description
PantryPal is a user-friendly application that allows individuals to keep track of their pantry items with ease and style. Users can add items, specifying details such as name, quantity, category, and container type. The application provides a quick view of recent additions on the main page and a comprehensive, categorized list on a separate page for a full overview of the pantry stock. The design aims for an elegant and visually appealing experience.

This project was developed as a demonstration of full-stack serverless application development using AWS cloud services.

✨ Key Features
Dynamic Item Management: Add new pantry items with details including name, quantity, category, and container type.

Elegant User Interface: Custom-styled frontend with a "fancy wedding invitation" theme, utilizing specific fonts and a refined color palette.

Main Dashboard (Index.html):

Form for adding new pantry items.

Displays a sample of the most recently added items.

Link to view the complete pantry inventory.

Full Inventory Page (all_items.html):

Displays all pantry items fetched from the database.

Items are grouped by category for better organization.

Each item displays its name, quantity, and container type.

Two-column responsive layout for category display on wider screens, stacking to a single column on smaller screens.

Scrollable view within individual categories if the item list is long.

Navigation link back to the main dashboard.

Responsive Design: The user interface is designed to adapt to different screen sizes (desktop, tablet, mobile).

Serverless Backend: Utilizes AWS Lambda for compute, API Gateway for request handling, and DynamoDB for data storage, ensuring scalability and cost-effectiveness.

🛠️ Technologies Used
Cloud/Backend:

AWS Lambda: Python runtime for serverless functions (adding and retrieving items).

Amazon API Gateway: For creating and managing RESTful API endpoints.

Amazon DynamoDB: NoSQL database for storing pantry item data.

AWS S3 (Simple Storage Service): For hosting the static frontend web application (index.html, all_items.html).

AWS IAM (Identity and Access Management): For managing permissions and roles for AWS services.

Frontend:

HTML5: Structure of the web pages.

CSS3: Custom styling for the "fancy wedding invitation" theme, including Flexbox/Grid for layout, animations, and responsive design.

JavaScript (ES6+): For dynamic content rendering, API calls (fetch API), form handling, and DOM manipulation.

Fonts & Icons:

Google Fonts (Great Vibes, Playfair Display, EB Garamond).

Font Awesome (for icons).

🏗️ Architecture Overview
PantryPal follows a serverless, three-tier architecture:

Frontend (Client-Side):

Static HTML, CSS, and JavaScript files served from an AWS S3 bucket configured for static website hosting.

The JavaScript in the browser makes asynchronous API calls to Amazon API Gateway.

API Layer (Amazon API Gateway):

Provides RESTful HTTP endpoints (e.g., POST /items to add, GET /items to retrieve).

Handles request validation, CORS, and triggers the appropriate AWS Lambda functions based on the method and resource path.

Backend Logic & Data Tier (AWS Lambda & DynamoDB):

AWS Lambda Functions (Python):

addPantryItemFunction: Receives new item data from API Gateway, generates a unique ID, adds a timestamp, and stores the item in DynamoDB.

getPantryItemsFunction: Retrieves all items from the DynamoDB table and returns them.

Amazon DynamoDB:

A NoSQL table (PantryItems) stores each item with attributes like itemID (primary key), itemName, quantity, category, containerType, and dateAdded.

🚀 Setup & Running (Conceptual for Re-deployment)
This project was initially developed in an AWS Learner Lab environment. To re-deploy it in a personal AWS account:

Backend Setup:

Create a DynamoDB table (e.g., PantryItems) with a primary key (e.g., itemID as a String).

Create IAM roles with necessary permissions for Lambda functions to access DynamoDB and CloudWatch Logs.

Deploy the Python Lambda functions (addPantryItemFunction.py, getPantryItemsFunction.py). Configure environment variables (e.g., DYNAMODB_TABLE).

Set up an API Gateway REST API with appropriate resources (e.g., /items) and methods (GET, POST) configured for Lambda proxy integration, pointing to your Lambda functions. Enable CORS and deploy the API to a stage.

Frontend Setup:

Update the apiUrl constant in both index.html and all_items.html JavaScript sections with your new API Gateway Invoke URL.

Create an S3 bucket, enable static website hosting, and configure Index.html as the index document.

Upload index.html and all_items.html to the S3 bucket and ensure they have public read permissions.

Access the website via the S3 static website hosting endpoint.

🔮 Future Enhancements (Potential Next Steps)
Edit Item Functionality: Allow users to modify existing pantry items.

Delete Item Functionality: Allow users to remove items from the pantry.

Expiry Date Tracking: Add functionality to track item expiry dates and provide reminders.

Thank you for checking out PantryPal!
