import streamlit as st
import os
import google.generativeai as genai
import json
from rapidfuzz import process, fuzz
from dotenv import load_dotenv  # Import dotenv

# Load environment variables from .env file
load_dotenv()  # This will load the environment variables from .env file

#Configure the Gemini API using environment variables
API_KEY = os.getenv("GEMINI_API_KEY")  # Ensure you set this environment variable
if not API_KEY:
    st.error("Please set the GEMINI_API_KEY environment variable.")
    st.stop()

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

if "chatbot" not in st.session_state:
    st.session_state.chatbot = []  # Use session state for persistence in Streamlit

chatbot = st.session_state.chatbot

def handle_user_query(msg,chatbot):
    chatbot+=[[msg,None]]
    return chatbot

def generate_chatbot(chatbot):
    q="""You are GreenLife Foods Chatbot. Your job is to assist users with tasks related to product availability, "
                "pricing, ordering, and listing products. You also have access to the user's interaction history within the "
                "chat and should use this history to answer any general or history-based questions, such as cumulative orders.\n\n"
                "### General Behavior:\n"
                "1. Always use the user's history provided in the conversation to respond to context-specific queries.\n"
                "   For example, if the user asks, 'How much total quantity of cashews have I ordered?', calculate the cumulative "
                "quantity of cashews ordered based on the history provided.\n"
                "2. If the history contains incomplete information, respond with an appropriate message such as:\n"
                "   'Based on the provided history, you have ordered X units of cashews.'\n"
                "3. Do not say 'I do not have access to your history.' Always use the history provided in the conversation.\n\n"
                "### Guidelines for Intent Mapping:\n"
                "- Use the exact intents listed below when responding:\n"
                "  - 'get_price': When the user asks for the price or cost of a product.\n"
                "  - 'order_product': When the user wants to order a product.\n"
                "  - 'list_products': When the user requests a list of all products.\n"
                "  - 'complete_order': When the user wants to finalize their order.\n"
                "  - 'unknown': If the query is unclear or cannot be categorized under the above intents.\n\n"
                "- If a query uses synonyms or phrases with the same meaning as an intent, map it to the exact intent name.\n\n"
                "### Guidelines for Quantity Parsing:\n"
                "- Always extract numeric values for quantities and exclude units (e.g., '2 kg' should be returned as '2').\n"
                "- If the quantity is specified incrementally (e.g., 'add 1 more kg'), calculate the cumulative total based on the history.\n"
                "- Examples:\n"
                "  - Query: 'Order 3 kg of cashews and add 2 more kg.'\n"
                "    Response: {\n"
                "       \"intent\": \"order_product\",\n"
                "       \"product_name\": \"cashews\",\n"
                "       \"quantity\": 5\n"
                "    }\n\n"
                "### Examples:\n"
                "- User Query: 'How much total quantity of cashews have I ordered?'\n"
                "  History: Query 1: Order 2 kg of cashews, Query 2: Add 1 more kg.\n"
                "  Response: {\n"
                "     \"intent\": \"unknown\",\n"
                "     \"message\": \"Based on the provided history, you have ordered 3 units of cashews.\"\n"
                "  }\n\n"
                "- User Query: 'What is the price of cashews?'\n"
                "  Response: {\n"
                "     \"intent\": \"get_price\",\n"
                "     \"product_name\": \"cashews\"\n"
                "  }\n\n"
                "- User Query: 'List all products and give the price of almonds.'\n"
                "  Response: [\n"
                "     {\n"
                "         \"intent\": \"list_products\"\n"
                "     },\n"
                "     {\n"
                "         \"intent\": \"get_price\",\n"
                "         \"product_name\": \"almonds\"\n"
                "     }\n"
                "  ]"""
    formatted_chatbot=[ {
            "role": "model",
            "parts": q
        }]
    if len(chatbot)==0:
        return formatted_chatbot


    i=1
    p="This is what users asked had asked to the chatbot model in different sequential queries. So it is basically user's history with interaction with chatbot model so model can used it for  giving general question answer which are not intent specific . History of user given below in every query and the chatbot response to the query"
    for query, response in chatbot:
        p+=f" Query {i}:"+query+" "+"Chatbot response "+response+"\n"
        i=i+1
    
    formatted_chatbot=[]
    q=q+"\n\n"+p
    formatted_chatbot.append({"role":"model","parts":q})
    return formatted_chatbot



# Secondary chatbot for restructuring unstructured JSON
secondary_chat = model.start_chat(
    history=[
        {
            "role": "user",
            "parts": (
                """You are a JSON validation assistant. Your job is to restructure and validate unstructured JSON responses. "
                "If you receive malformed JSON, fix it and return valid JSON. Do not include any code blocks or extra text, just "
                "the corrected JSON structure.\n\n"
                "Examples:\n"
                "Unstructured Input:\n"
                "```json\n{\n  \"intent\": \"get_price\",\n  \"product_name\": \"cashews\",\n}\n```\n"
                "Structured Output:\n"
                "{\n  \"intent\": \"get_price\",\n  \"product_name\": \"cashews\"\n}\n\n"
                "Unstructured Input:\n"
                "```json\n[\n  {\n    \"intent\": \"get_price\",\n    \"product_name\": \"quinoa\"\n  },\n  {\n    \"intent\": \"list_products\",\n  }\n]\n```\n"
                "Structured Output:\n"
                "[\n  {\n    \"intent\": \"get_price\",\n    \"product_name\": \"quinoa\"\n  },\n  {\n    \"intent\": \"list_products\"\n  }\n]"""
            )
        }
    ]
)

# Product database
products = {
    "organic_rice": {"price": 50, "quantity": 10},
    "almond_butter": {"price": 150, "quantity": 5},
    "organic_wheat": {"price": 40, "quantity": 20},
    "quinoa": {"price": 120, "quantity": 8},
    "chia_seeds": {"price": 90, "quantity": 15},
    "organic_honey": {"price": 200, "quantity": 7},
    "almonds": {"price": 300, "quantity": 12},
    "cashews": {"price": 400, "quantity": 10},
    "peanut_butter": {"price": 150, "quantity": 6},
    "oats": {"price": 100, "quantity": 15},
    "wheat_flour": {"price": 30, "quantity": 25},
    "almond_flour": {"price": 150, "quantity": 10},
    "coconut_oil": {"price": 250, "quantity": 10},
    "olive_oil": {"price": 300, "quantity": 5},
    "black_salt":{"price":30,"quantity":10},
    "white_salt":{"price":36,"quantitiy":20}
}

# Helper functions
def find_closest_product(query, products, threshold=60):
    matches = process.extract(query, list(products.keys()), scorer=fuzz.ratio)
    return [match for match in matches if match[1] >= threshold]

def process_response(response_text, cart):
    try:
        # Debug: Print the raw response for better visibility
        print("Raw Response Text:", repr(response_text))
        
        # Clean up the response text by removing code block markers
        if response_text.startswith("```json"):
            response_text = response_text.replace("```json", "").replace("```", "").strip()

        # Debug: Print the cleaned response text
        print("Cleaned Response Text:", response_text)

        # Parse the cleaned JSON response
        response = json.loads(response_text)

        # Handle different cases: single or multiple intents
        if isinstance(response, dict) and response.get("intent") == "unknown":
            return response.get("message", "Unknown query.")
        elif isinstance(response, list):
            messages = []
            for intent_data in response:
                messages.append(handle_intent(intent_data, cart))
            return "\n".join(messages)
        else:
            return handle_intent(response, cart)
    except json.JSONDecodeError as e:
        print(response_text)
        return response_text


def handle_intent(intent_data, cart):
    intent = intent_data.get("intent")
    product_name = intent_data.get("product_name")
    quantity = intent_data.get("quantity", 0)
    close_product=find_closest_product(product_name,products)

    if intent == "get_price":
        if (product_name in products) :
            return f"The price of {product_name.replace('_', ' ')} is {products[product_name]['price']} per unit."
        elif len(close_product)==1:
            return f"The price of {close_product[0][0]} is {close_product[0][0]} per unit."
        elif len(close_product)>1:
            s=f"There are {len(close_product)} {product_name}  that are "
            p=""
            for x in close_product:
                 p=p+","+x[0]
            p=p[1:]
            s=s+p+" whose price do you want"
            return s
        return f"We do not manufacture {product_name.replace('_', ' ')}."
        

    elif intent == "order_product":
        if product_name in products and products[product_name]["quantity"] < quantity:
            return f"We do not have {quantity} units of {product_name.replace('_', ' ')} available."
        elif product_name in products:
            products[product_name]["quantity"] -= quantity
            cart.append({"name": product_name.replace('_', ' '), "quantity": quantity, "price": products[product_name]["price"]})
            return f"Added {quantity} units of {product_name.replace('_', ' ')} to your cart."
        elif len(close_product)==1:
            if products[close_product[0][0]]["quantity"] < quantity:
                return f"We do not have {quantity} units of {close_product[0][0].replace('_', ' ')} available."
            else:
                products[close_product[0][0]]["quantity"] -= quantity
                cart.append({"name": product_name.replace('_', ' '), "quantity": quantity, "price": products[close_product[0][0]]["price"]})
                return f"Added {quantity} units of {close_product[0][0].replace('_', ' ')} to your cart."
        else:
            if len(close_product)>1:
                s=f"There are {len(close_product)} {product_name}  that are "
                p=""
                for x in close_product:
                    p=p+","+x[0]
                p=p[1:]
                s=s+p+" what product do you want to ordered"
                return s
            return f"We do not manufacture {product_name.replace('_', ' ')}."

    elif intent == "list_products":
        return "Available products: " + ", ".join(products.keys())

    elif intent == "complete_order":
        if not cart:
            return "Your cart is empty."
        total = sum(item["quantity"] * item["price"] for item in cart)
        receipt = "\n".join([f"{item['name']}: {item['quantity']} at {item['price']} each" for item in cart])
        cart.clear()
        return f"Order complete. Total: {total}\nReceipt:\n{receipt}"

    return "Unknown intent."

# Streamlit interface
st.title("GreenLife Foods Chatbot")
st.markdown("Welcome to the GreenLife Foods Chatbot. Ask me anything about our products!")

user_query = st.text_input("Your Query:")
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "cart" not in st.session_state:
    st.session_state.cart = []

if user_query:
    print("hi 1")
    chatbot=handle_user_query(user_query,chatbot)
    print("printed chatbot start")
    print(chatbot)
    print("printed chatbot end")
    print("hi 2")
    formated_history=generate_chatbot(chatbot[:-1])
    print("hi 3")
    print("formatted history start")
    print(formated_history)
    print("formated_history end")
    main_chat=model.start_chat(history=formated_history)
    print("hi 4")
    response = main_chat.send_message(user_query).text
    chat_response = process_response(response, st.session_state.cart)
    chatbot[-1][1]=response
    st.session_state.chatbot = chatbot
    print("response is ",response)
    print("history is ",main_chat.history)
    st.session_state.chat_history.append((user_query, chat_response))

if st.session_state.chat_history:
    st.markdown("### Chat History")
    for user, bot in st.session_state.chat_history:
        st.markdown(f"**You:** {user}")
        st.markdown(f"**Chatbot:** {bot}")
