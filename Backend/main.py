from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from datetime import datetime
from zoneinfo import ZoneInfo  # Python 3.9+ timezone support

import Db_helper
import generic_helper
from zoneinfo import ZoneInfo

app = FastAPI()
inprogress_orders = {}

@app.get("/")
async def home():
    return {"message": "FastAPI webhook is live."}

# Shop open hours (Monday to Friday, 10 AM to 10 PM)
def is_shop_open():
    sg_time = datetime.now(ZoneInfo("Asia/Singapore"))
    return sg_time.weekday() < 5 and 10 <= sg_time.hour < 22

@app.post("/")
async def handle_request(request: Request):
    payload = await request.json()

    intent = payload['queryResult']['intent']['displayName']
    parameters = payload['queryResult']['parameters']
    output_contexts = payload['queryResult']['outputContexts']
    session_id = generic_helper.extract_session_id(output_contexts[0]["name"])
    
    if intent == "new.order":
        if session_id:
            Db_helper.clear_order_session(session_id)
            inprogress_orders.pop(session_id, None)
        return {"fulfillmentText": "Sure! Let's start fresh. What would you like to order?"}

    if not is_shop_open():
        return {"fulfillmentText": "Our shop is currently closed. We are open Monday to Friday from 10 AM to 10 PM."}
    
    intent_handler_dict = {
       'order.add - Context: ongoing-order': add_to_order,
       'order.remove - context: ongoing-order': remove_from_order,
       'order.complete - context: ongoing-order': complete_order,
       'track.order - context: ongoing-tracking': track_order
    }

    return intent_handler_dict[intent](parameters, session_id)


# ✅ Track existing order
def track_order(parameters: dict):
    order_id = int(parameters.get("number", 0))

    if not order_id:
        return JSONResponse(content={"fulfillmentText": "Please provide an order ID to track."})

    status = Db_helper.get_order_status(order_id)

    if status:
        return JSONResponse(content={"fulfillmentText": f"Your order {order_id} is currently: {status}."})
    else:
        return JSONResponse(content={"fulfillmentText": f"No order found with ID {order_id}."})
    

def save_to_db(order: dict):
    next_order_id = Db_helper.get_next_order_id()

    # Insert individual items along with quantity in orders table
    for food_item, quantity in order.items():
        rcode = Db_helper.insert_order_item(
            food_item,
            quantity,
            next_order_id
        )

        if rcode == -1:
            return -1
    return next_order_id


# ✅ Remove items from cart
def remove_from_order(parameters: dict, session_id: str):
    if session_id not in inprogress_orders:
        return JSONResponse(content={"fulfillmentText": "I couldn't find your current order. Please start a new one."})

    food_items = parameters["food-item"]
    current_order = inprogress_orders[session_id]
    removed_items, missing_items = [], []
    fulfillment_text = ""

    for item in food_items:
        if item in current_order:
            del current_order[item]
            removed_items.append(item)
        else:
            missing_items.append(item)

    if removed_items:
        fulfillment_text += f"Removed {', '.join(removed_items)} from your order. "

    if missing_items:
        fulfillment_text += f"{', '.join(missing_items)} were not in your order. "

    if not current_order:
        fulfillment_text += "Your order is now empty."
    else:
        order_str = generic_helper.get_str_from_food_dict(current_order)
        fulfillment_text += f" Remaining items: {order_str}"

    return JSONResponse(content={"fulfillmentText": fulfillment_text})

# ✅ Complete and save order
def complete_order(parameters: dict, session_id: str):
    if session_id not in inprogress_orders:
        # fallback: pull from outputContext
        food_items = []
        quantities = []

        # pull from last context
        for ctx in parameters.get("outputContexts", []):
            if "ongoing-order" in ctx["name"]:
                food_items = ctx["parameters"].get("food-item", [])
                quantities = ctx["parameters"].get("number", [])

        if not food_items or not quantities:
            return JSONResponse(content={"fulfillmentText": "I couldn't find your order. Please start again."})

        order = dict(zip(food_items, quantities))
    else:
        order = inprogress_orders[session_id]

    order_id = save_to_db(order)
    if order_id == -1:
        fulfillment_text = "Sorry, there was a problem saving your order. Please try again."
    else:
        total = Db_helper.get_total_order_price(order_id)
        fulfillment_text = (
            f"Order placed successfully! Your order ID is #{order_id}. "
            f"Total is ₹{total}. Please pay at the time of delivery."
        )

    if session_id in inprogress_orders:
        del inprogress_orders[session_id]

    return JSONResponse(content={"fulfillmentText": fulfillment_text})

# ✅ Add items to cart
def add_to_order(parameters: dict, session_id: str):
    food_items = parameters["food-item"]
    quantities = parameters["number"]

    if len(food_items) != len(quantities):
        fulfillment_text = "Sorry I didn't understand. Can you please specify food items and quantities clearly?"
    else:
        new_food_dict = dict(zip(food_items, quantities))

        if session_id in inprogress_orders:
            current_food_dict = inprogress_orders[session_id]
            current_food_dict.update(new_food_dict)
            inprogress_orders[session_id] = current_food_dict
        else:
            inprogress_orders[session_id] = new_food_dict

        order_str = generic_helper.get_str_from_food_dict(inprogress_orders[session_id])
        fulfillment_text = f"So far you have: {order_str}. Do you need anything else?"

    return JSONResponse(content={
        "fulfillmentText": fulfillment_text
    })





# # ✅ Save order to database
# def save_to_db(order: dict):
#     order_id = Db_helper.get_next_order_id()
#     for item_name, qty in order.items():
#         item_id = Db_helper.get_item_id_by_name(item_name)
#         if not item_id:
#             print(f"[ERROR] Item not found: {item_name}")
#             return -1
#         result = Db_helper.insert_order_item(item_id, qty, order_id)
#         if result == -1:
#             return -1

#     Db_helper.insert_order_tracking(order_id, "in progress")
#     return order_id
