# GreenLife Foods Chatbot

GreenLife Foods Chatbot is an AI-powered solution designed to assist distributors and retailers of GreenLife Foods in streamlining their order capture process. This chatbot provides functionality for product inquiries, price checks, placing orders, and managing purchase history.

---

## Features

1. **Product Inquiry**
   - Users can ask for the list of available products.
   - If a user misspells a product name, the chatbot leverages the RapidFuzz library to suggest closely matching products.
   - Handles cases where multiple similar products exist (e.g., "almond" vs. "almond oil") by prompting the user for clarification.

2. **Price Check**
   - Users can inquire about the price of a specific product.
   - If the product is not available, the chatbot notifies the user.

3. **Order Placement**
   - Users can order single or multiple products in one query.
   - Handles quantity management:
     - If the requested quantity exceeds availability, the chatbot informs the user.
     - Successfully ordered products are deducted from the inventory.

4. **Order Completion**
   - Users can finalize their orders.
   - A receipt is generated, showing ordered products, their quantities, and the total cost.

5. **General Query Handling**
   - Answers user-specific historical queries, such as "What have I ordered in the past?".
   - Leverages conversation history to provide accurate responses.

---

## Workflow Overview

### 1. User Interaction
- The user interacts with the chatbot via a user-friendly Streamlit interface.
- Users can type queries like:
  - "What is the price of almond butter?"
  - "Order 2 units of quinoa and 1 unit of chia seeds."
  - "What products are available?"

### 2. Intent Identification
- The chatbot identifies the user’s intent from their query:
  - **`list_products`**: Listing all available products.
  - **`get_price`**: Checking the price of a product.
  - **`order_product`**: Placing an order for one or more products.
  - **`complete_order`**: Finalizing the order and generating a receipt.

### 3. JSON Response Processing
- The chatbot generates a JSON response for the user query.
- Based on the intent identified, specific functions handle the query:
  - **Price Check**: Returns the product price if available.
  - **Order Placement**: Adds items to the cart and updates inventory.
  - **General Queries**: Responds based on conversation history.

### 4. Inventory Management
- Ensures real-time updates to product quantities in the database.
- Prevents orders exceeding the available inventory.

### 5. RapidFuzz Integration
- Corrects spelling errors in product names using fuzzy matching.
- Suggests alternative products if multiple matches exist.

### 6. Multi-Intent Handling
- Supports queries with multiple intents, such as ordering products while requesting price details.

---

## Technical Details

### Stack
- **Frontend**: Streamlit
- **Backend**: Python with Google Gemini API
- **Libraries**: 
  - `rapidfuzz`: For fuzzy matching and product suggestion.
  - `google.generativeai`: For chatbot functionality.
  - `dotenv`: To securely load API keys.
  - `json`: For handling chatbot responses.

### Key Functionalities
- **Inventory Updates**: Deducts ordered quantities from stock.
- **Error Handling**: 
  - Notifies the user when a product or quantity is unavailable.
  - Handles malformed queries gracefully.
- **History Utilization**: Uses past interactions to answer general queries.

---

## Setup Instructions

### Prerequisites
1. Python 3.9+
2. An API key for Google Gemini API
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Environment Setup
1. Create a `.env` file:
   ```
   GEMINI_API_KEY=<your-api-key>
   ```
2. Ensure the `.env` file is in the project root directory.

### Run the Application
1. Start the chatbot using Streamlit:
   ```bash
   streamlit run app.py
   ```
2. Access the chatbot interface in your browser.

---

## Prompt Engineering
The chatbot uses carefully crafted prompts to:
1. I have say to remove the quantity unit of the product always give output in json
2. Ask it to handle like always return the intent mention in the prompt like if some user give cost then you should return intent get_price not give cost because we do not have give cost function although there meaning is same.
3. Also you return different intent



### Limitations
- Like there is problem in setting fuzzy ratio setting to low can lead to addition of the word which are not even related and adding adding can lead to ignorance of the item which i ordered like if i ordered wheat then organic_wheat is the name in our product list so setting high fuzz ratio wheat is not available.
- Sometime it give wrong output when you ask general question when you ask about the quantity. This may be due to context increasing. So we can improve it by my improving prompt

---

### You can check the output in the images that i have attached with this github repository.
