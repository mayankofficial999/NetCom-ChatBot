import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import tkinter as tk
from transformers import logging
logging.set_verbosity_warning()

# Load pre-trained BERT model and tokenizer
model_name = "bert-base-uncased"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name)

# Define possible product categories
product_categories = ["switches", "machines", "india"]

# Define possible questions and their corresponding answers
data = {
    "What products does your company sell?": 
        "We sell software, hardware, and services.",
    "Can you tell me more about your software products?": 
        "Our software products include network management software, security software, and cloud computing software.",
    "What hardware products do you offer?": 
        "We offer network routers, switches, firewalls, and other networking hardware products.",
    "What kind of services do you provide?": 
        "We provide consulting, implementation, and maintenance services for our products.",
    "How can I purchase your products?": 
        "You can purchase our products through our website or authorized resellers.",
    "Do you offer any discounts or promotions?": 
        "Yes, we occasionally offer discounts and promotions. Please check our website for current offers.",
    "Can you provide technical support for your products?": 
        "Yes, we offer technical support for all our products. Please contact our support team for assistance.",
    "What is your company's mission?": 
        "Our mission is to provide high-quality networking solutions to our customers worldwide."
}

# Define a function to generate responses
def generate_response(text):
    # Classify text into one of the product categories
    inputs = tokenizer(text, return_tensors="pt")
    outputs = model(**inputs)
    _, predicted_class = torch.max(outputs.logits, dim=1)
    category = product_categories[predicted_class]
    
    # Check if text matches any of the pre-defined questions
    for question, answer in data.items():
        if text.lower() == question.lower():
            return answer
    
    # If not, generate a generic response based on the product category
    if category == "switches":
        return "Our software products include network management software, security software, and cloud computing software."
    elif category == "machines":
        return "We offer network routers, switches, firewalls, and other networking hardware products."
    elif category == "india":
        return "We provide consulting, implementation, and maintenance services for our products."
    
    return "I'm sorry, I didn't understand your question."

# Define a function to handle user input
def get_response():
    text = user_input.get()
    response = generate_response(text)
    chat_history.insert(tk.END, "You: " + text + "\n")
    chat_history.insert(tk.END, "Chatbot: " + response + "\n\n")
    user_input.delete(0, tk.END)

# Create a simple GUI
root = tk.Tk()
root.title("Networking Company Chatbot")

# Add a chat history display
chat_history = tk.Text(root, height=20, width=60)
chat_history.configure(state="disabled")
chat_history.pack(side=tk.TOP, padx=10, pady=10)

# Add a user input field
user_input = tk.Entry(root, width=50)
user_input.pack(side=tk.LEFT, padx=10, pady=10)

# Add a "send" button to submit user input
send_button = tk.Button(root, text="Send", command=get_response)
send_button.pack(side=tk.LEFT, padx=10, pady=10)