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
1. Always remove the quantity unit from the product and return the output in JSON format.
2. Ensure that the correct intent is returned as specified in the prompt. For example, if a user asks for the cost, the chatbot should return the get_price intent, not the give_cost intent, since the give_cost function does not exist, even though the meanings are similar.
3. Ensure that different intents are correctly returned based on user input



### Limitations
- Setting a low fuzzy matching ratio can result in the inclusion of unrelated words, while a high fuzzy ratio can cause relevant items to be overlooked. For example, if I search for "wheat," a high fuzzy ratio might not show "organic_wheat" from the product list, even though it's the correct match.
- Additionally, the system can give incorrect outputs when asked about specific details like quantity, likely due to increased context influencing the response. To improve the system's accuracy, enhancing the prompt could help address these issues.

---

### You can check the output in the images that i have attached with this github repository.
