# 🍔 Char Food Delivery Chatbot

A smart, end-to-end food ordering chatbot built using **Dialogflow**, **FastAPI**, and **MySQL** — with a floating chatbot interface embedded into a custom website.

---

## 🔍 Project Overview

This chatbot allows users to interact in natural language to:
- Place new food orders
- Add/remove items from their cart
- Track existing orders
- Complete and save orders

The project integrates:
- **Dialogflow CX** for natural language understanding
- **FastAPI** to handle webhook fulfillment
- **MySQL** for backend order management
- **HTML/CSS** for chatbot UI with a floating iframe

---

## 🧠 Features

- 🗣️ Conversational ordering via Dialogflow
- 🍱 Add/remove food items
- 📦 Track orders by ID
- 💾 Save and complete orders to MySQL
- ⏱️ Business logic for shop timings (Weekdays 10 AM–10 PM)
- 🧼 Session clearing with “new order” intent
- 🖼️ Embedded chatbot UI with floating iframe

---

## ⚙️ Tech Stack

| Layer         | Tool            |
|---------------|------------------|
| NLP Chatbot   | Dialogflow       |
| Backend       | FastAPI (Python) |
| Database      | MySQL            |
| Frontend      | HTML/CSS         |
| Hosting       | GitHub Pages / Localhost (Dev) |

---

## 🛠️ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/CharanyaMadhan/char-food-chatbot.git
cd char-food-chatbot
2. Install Dependencies
bash
Copy
Edit
pip install fastapi uvicorn mysql-connector-python
3. Run FastAPI Server
bash
Copy
Edit
uvicorn main:app --reload
4. Access the Webpage
Open home.html in your browser to see the chatbot floating in the bottom right corner.

🧪 Dialogflow Setup
Intents: order.add, order.remove, order.complete, track.order, new.order

Contexts used for maintaining conversation flow

Fulfillment URL points to FastAPI server (/ endpoint)



SOURCE OF LEARNING:

🧾 Credit
Tutorial Source:
🎓 Codebasics - End-to-End Chatbot Project
