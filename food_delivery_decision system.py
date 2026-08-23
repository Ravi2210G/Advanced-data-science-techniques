
# Food Delivery Order Decision Automation System
#-------------------------------------------------
#Pure core-Python (no external libraries) rule-based engine that decides:
#    - Order Status (Accepted / Rejected / Manual Review)
#    - Delivery Charge
#    - Discount
#    - Priority Delivery status
#    - Cancellation Risk
#    - Restaurant Status
#    - Manual Review requirement
#    - Final Order Category
#   - Final Payable Amount
 
# Only if / elif / else / nested conditions / and / or are used for decisions.
#"""
 
 
# ---------------------------------------------------------------------
# 1. RESTAURANT STATUS
# ---------------------------------------------------------------------
def get_restaurant_status(restaurant_rating, preparation_time):
    if restaurant_rating < 2.5:
        status = "Suspended"
    elif restaurant_rating < 3.5 or preparation_time > 45:
        status = "Busy"
    elif restaurant_rating >= 4.5 and preparation_time <= 20:
        status = "Highly Active"
    else:
        status = "Active"
    return status
 
 
# ---------------------------------------------------------------------
# 2. CANCELLATION RISK
# ---------------------------------------------------------------------
def get_cancellation_risk(previous_cancellations, customer_rating, payment_method):
    if previous_cancellations >= 5 or customer_rating < 2.5:
        risk = "High"
    elif previous_cancellations >= 2 or customer_rating < 3.5:
        risk = "Medium"
    elif previous_cancellations == 0 and customer_rating >= 4.5:
        risk = "Very Low"
    else:
        risk = "Low"
 
    # COD orders carry slightly higher real-world risk -> bump one level
    if payment_method == "COD" and risk == "Medium":
        risk = "High"
    elif payment_method == "COD" and risk in ("Low", "Very Low"):
        risk = "Medium"
 
    return risk
 
 
# ---------------------------------------------------------------------
# 3. ORDER STATUS DECISION (Accepted / Rejected / Manual Review)
# ---------------------------------------------------------------------
def get_order_status(order_amount, delivery_distance, customer_type, restaurant_status,
                      cancellation_risk, payment_method, weather_condition,
                      demand_level, peak_hour):
 
    manual_review_required = "No"
 
    # --- Hard rejections first ---
    if order_amount <= 0:
        status = "Rejected"
    elif restaurant_status == "Suspended":
        status = "Rejected"
    elif weather_condition == "storm" and delivery_distance > 15:
        status = "Rejected"
    elif cancellation_risk == "High" and payment_method == "COD":
        status = "Rejected"
 
    # --- Manual review cases ---
    elif cancellation_risk == "High":
        status = "Manual Review"
        manual_review_required = "Yes"
    elif customer_type == "new" and order_amount > 5000:
        status = "Manual Review"
        manual_review_required = "Yes"
    elif weather_condition == "storm":
        status = "Manual Review"
        manual_review_required = "Yes"
    elif restaurant_status == "Busy" and demand_level == "high" and peak_hour:
        status = "Manual Review"
        manual_review_required = "Yes"
    elif delivery_distance > 25 and demand_level == "high":
        status = "Manual Review"
        manual_review_required = "Yes"
 
    # --- Otherwise accepted ---
    else:
        status = "Accepted"
 
    return status, manual_review_required
 
 
# ---------------------------------------------------------------------
# 4. DELIVERY CHARGE
# ---------------------------------------------------------------------
def get_delivery_charge(delivery_distance, weather_condition, peak_hour,
                         demand_level, customer_type, order_amount):
 
    charge = 20  # base charge
 
    # distance based charge (first 5 km free)
    if delivery_distance > 5:
        charge += (delivery_distance - 5) * 5
 
    # weather surcharge
    if weather_condition == "storm":
        charge += 25
    elif weather_condition == "rain":
        charge += 10
 
    # peak hour surcharge
    if peak_hour:
        charge += 15
 
    # demand surcharge
    if demand_level == "high":
        charge += 20
    elif demand_level == "medium":
        charge += 10
 
    # premium customer perk: free delivery on decent-sized orders
    if customer_type == "premium" and order_amount > 500:
        charge = 0
 
    return round(charge, 2)
 
 
# ---------------------------------------------------------------------
# 5. DISCOUNT
# ---------------------------------------------------------------------
def get_discount(order_amount, customer_type, previous_cancellations, customer_rating):
 
    discount_percent = 0
 
    if customer_type == "premium" and order_amount > 300:
        discount_percent = 15
    elif customer_type == "regular" and order_amount > 500:
        discount_percent = 5
    elif customer_type == "new" and order_amount > 200:
        discount_percent = 10
 
    # loyalty bonus: clean cancellation history + great rating
    if previous_cancellations == 0 and customer_rating >= 4.5:
        discount_percent += 5
 
    # cap discount at 25%
    if discount_percent > 25:
        discount_percent = 25
 
    discount_amount = round((discount_percent / 100) * order_amount, 2)
    return discount_percent, discount_amount
 
 
# ---------------------------------------------------------------------
# 6. PRIORITY DELIVERY
# ---------------------------------------------------------------------
def get_priority_status(customer_type, order_amount, peak_hour, demand_level, restaurant_status):
 
    if customer_type == "premium":
        priority = "Yes"
    elif order_amount > 1000 and restaurant_status in ("Active", "Highly Active"):
        priority = "Yes"
    else:
        priority = "No"
 
    # capacity override: system too busy to guarantee priority unless premium
    if priority == "Yes" and peak_hour and demand_level == "high" and customer_type != "premium":
        priority = "No"
 
    return priority
 
 
# ---------------------------------------------------------------------
# 7. FINAL ORDER CATEGORY
# ---------------------------------------------------------------------
def get_final_category(order_status, priority_status, cancellation_risk, restaurant_status):
 
    if order_status == "Rejected":
        category = "Rejected Order"
    elif order_status == "Manual Review":
        category = "Flagged / Risky Order"
    elif priority_status == "Yes" and restaurant_status == "Highly Active":
        category = "Express Priority"
    elif priority_status == "Yes":
        category = "Priority"
    elif cancellation_risk in ("Low", "Very Low") and restaurant_status in ("Active", "Highly Active"):
        category = "Standard"
    else:
        category = "Economy"
 
    return category
 
 
# ---------------------------------------------------------------------
# 8. MAIN DECISION ENGINE
# ---------------------------------------------------------------------
def process_order(order_amount, delivery_distance, customer_type, customer_rating,
                   restaurant_rating, preparation_time, payment_method,
                   weather_condition, demand_level, peak_hour, previous_cancellations):
 
    restaurant_status = get_restaurant_status(restaurant_rating, preparation_time)
 
    cancellation_risk = get_cancellation_risk(previous_cancellations, customer_rating, payment_method)
 
    order_status, manual_review_required = get_order_status(
        order_amount, delivery_distance, customer_type, restaurant_status,
        cancellation_risk, payment_method, weather_condition, demand_level, peak_hour
    )
 
    delivery_charge = get_delivery_charge(
        delivery_distance, weather_condition, peak_hour, demand_level, customer_type, order_amount
    )
 
    discount_percent, discount_amount = get_discount(
        order_amount, customer_type, previous_cancellations, customer_rating
    )
 
    priority_status = get_priority_status(
        customer_type, order_amount, peak_hour, demand_level, restaurant_status
    )
 
    final_category = get_final_category(
        order_status, priority_status, cancellation_risk, restaurant_status
    )
 
    # Final payable amount only makes sense if the order isn't rejected
    if order_status == "Rejected":
        final_payable = 0
    else:
        final_payable = round(order_amount - discount_amount + delivery_charge, 2)
 
    report = {
        "Order Status": order_status,
        "Delivery Charge": delivery_charge,
        "Discount (%)": discount_percent,
        "Discount (Amount)": discount_amount,
        "Priority Delivery": priority_status,
        "Cancellation Risk": cancellation_risk,
        "Restaurant Status": restaurant_status,
        "Manual Review Required": manual_review_required,
        "Final Order Category": final_category,
        "Final Payable Amount": final_payable,
    }
    return report
 
 
# ---------------------------------------------------------------------
# 9. PRETTY PRINT REPORT
# ---------------------------------------------------------------------
def print_report(report):
    print("\n" + "=" * 45)
    print("       FOOD DELIVERY ORDER REPORT")
    print("=" * 45)
    for key, value in report.items():
        print(f"{key:<25}: {value}")
    print("=" * 45)
 
 
# ---------------------------------------------------------------------
# 10. INTERACTIVE INPUT (run this file directly to use it live)
# ---------------------------------------------------------------------
def get_order_input():
    print("Enter order details:\n")
 
    order_amount = float(input("Order amount (Rs): "))
    delivery_distance = float(input("Delivery distance (km): "))
    customer_type = input("Customer type (new/regular/premium): ").strip().lower()
    customer_rating = float(input("Customer rating (1-5): "))
    restaurant_rating = float(input("Restaurant rating (1-5): "))
    preparation_time = float(input("Preparation time (minutes): "))
    payment_method = input("Payment method (COD/online): ").strip()
    weather_condition = input("Weather condition (clear/rain/storm): ").strip().lower()
    demand_level = input("Demand level (low/medium/high): ").strip().lower()
    peak_hour_input = input("Is it peak hour? (yes/no): ").strip().lower()
    peak_hour = True if peak_hour_input == "yes" else False
    previous_cancellations = int(input("Previous cancellations count: "))
 
    return (order_amount, delivery_distance, customer_type, customer_rating,
            restaurant_rating, preparation_time, payment_method,
            weather_condition, demand_level, peak_hour, previous_cancellations)
 
 
if __name__ == "__main__":
    print("FOOD DELIVERY ORDER DECISION SYSTEM")
    print("(Swiggy/Zomato-style rule engine — core Python only)\n")
 
    while True:
        inputs = get_order_input()
        result = process_order(*inputs)
        print_report(result)
 
        again = input("\nProcess another order? (yes/no): ").strip().lower()
        if again != "yes":
            print("\nExiting. Thank you!")
            break