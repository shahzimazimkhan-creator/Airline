import gradio as gr
import random
import time
from datetime import datetime, timedelta

# Mock AI response function (would connect to a real AI model in production)
def get_ai_response(message, history):
    # Convert history to a string context
    history_text = "\n".join([f"User: {h[0]}\nAssistant: {h[1]}" for h in history])
    
    # Simple rule-based responses for demo purposes
    message_lower = message.lower()
    
    if any(word in message_lower for word in ["hello", "hi", "hey", "greetings"]):
        return "Hello! Welcome to SkyWay Airlines. How can I assist you with your travel plans today?"
    
    elif any(word in message_lower for word in ["flight", "booking", "reservation"]):
        return "I can help you with flight bookings. Please provide your departure city, destination, and travel dates."
    
    elif any(word in message_lower for word in ["status", "track", "where"]):
        flight = random.choice(["SW425", "SW318", "SW201", "SW562"])
        status = random.choice(["On Time", "Delayed by 15 mins", "Boarding", "Departed"])
        return f"Flight {flight} is currently {status}. Would you like more specific details?"
    
    elif any(word in message_lower for word in ["baggage", "luggage", "bag"]):
        return "Our baggage policy allows one carry-on (up to 7kg) and one personal item. Checked bags can be up to 23kg. Would you like to add baggage to your booking?"
    
    elif any(word in message_lower for word in ["check-in", "check in"]):
        return "You can check in online 24 hours before your flight or at the airport counter. Would you like me to send you a check-in link?"
    
    elif any(word in message_lower for word in ["cancel", "refund", "change"]):
        return "I can help you with flight changes or cancellations. Please provide your booking reference number."
    
    elif any(word in message_lower for word in ["seat", "preference"]):
        return "Window, aisle, and extra-legroom seats are available. Would you like me to show you the seat map?"
    
    elif any(word in message_lower for word in ["food", "meal", "dietary"]):
        return "We offer vegetarian, vegan, gluten-free, and standard meal options. You can pre-order meals up to 24 hours before your flight."
    
    elif any(word in message_lower for word in ["thanks", "thank", "appreciate"]):
        return "You're welcome! Is there anything else I can help you with today?"
    
    elif any(word in message_lower for word in ["bye", "goodbye", "see you"]):
        return "Thank you for choosing SkyWay Airlines. Have a pleasant journey!"
    
    else:
        return "I'm here to help with your airline needs. You can ask me about flights, bookings, baggage, check-in, or any other travel-related questions."

# Function to simulate flight search
def search_flights(from_city, to_city, depart_date, return_date, passengers):
    depart_date_obj = datetime.strptime(depart_date, "%Y-%m-%d")
    return_date_obj = datetime.strptime(return_date, "%Y-%m-%d") if return_date else None
    
    # Generate some mock flight options
    flights = []
    airlines = ["SkyWay Airlines", "SkyJet", "AirExpress", "Global Airways"]
    prices = [299, 349, 399, 449, 499, 549]
    
    for i in range(3):
        depart_time = f"{random.randint(6, 20)}:{random.choice(['00', '15', '30', '45'])}"
        arrive_time = f"{random.randint(8, 22)}:{random.choice(['00', '15', '30', '45'])}"
        duration = f"{random.randint(1, 4)}h {random.randint(0, 55)}m"
        
        flight_data = {
            "airline": random.choice(airlines),
            "flight_no": f"SW{random.randint(100, 999)}",
            "departure": f"{from_city} at {depart_time}",
            "arrival": f"{to_city} at {arrive_time}",
            "duration": duration,
            "price": f"${random.choice(prices)}",
            "stops": random.choice(["Non-stop", "1 stop", "2 stops"])
        }
        flights.append(flight_data)
    
    # Sort by price
    flights.sort(key=lambda x: int(x["price"][1:]))
    
    return flights

# Function to format flight results
def format_flight_results(flights):
    if not flights:
        return "No flights found for your criteria. Please try different dates or cities."
    
    result = "### Available Flights\n\n"
    for i, flight in enumerate(flights, 1):
        result += f"**Option {i}:** {flight['airline']} ({flight['flight_no']})\n"
        result += f"- Depart: {flight['departure']}\n"
        result += f"- Arrive: {flight['arrival']}\n"
        result += f"- Duration: {flight['duration']} ({flight['stops']})\n"
        result += f"- Price: {flight['price']}\n\n"
    
    result += "Would you like to book any of these flights?"
    return result

# Function to handle flight search
def handle_flight_search(from_city, to_city, depart_date, return_date, passengers):
    if not from_city or not to_city or not depart_date:
        return "Please fill in all required fields: departure city, destination city, and departure date."
    
    flights = search_flights(from_city, to_city, depart_date, return_date, passengers)
    return format_flight_results(flights)

# Function to check flight status
def check_flight_status(flight_number):
    if not flight_number:
        return "Please enter a flight number."
    
    statuses = ["On Time", "Delayed by 15 mins", "Delayed by 30 mins", "Boarding", "Departed", "Arrived"]
    gates = ["A12", "B7", "C3", "D21", "E15"]
    
    status = random.choice(statuses)
    gate = random.choice(gates)
    
    return f"Flight {flight_number} is currently **{status}**. Departure gate: {gate}"

# Create the Gradio interface
with gr.Blocks(title="SkyWay Airlines AI Assistant", theme=gr.themes.Soft()) as demo:
    gr.HTML("""
    <div style="text-align: center; padding: 20px; background: linear-gradient(135deg, #1e40af, #3b82f6); color: white; border-radius: 10px;">
        <h1 style="margin: 0;">SkyWay Airlines ✈️</h1>
        <p style="margin: 5px 0 0;">AI-Powered Customer Assistant</p>
    </div>
    """)
    
    with gr.Tab("Chat Assistant"):
        gr.Markdown("### How can I help you with your travel plans today?")
        chatbot = gr.Chatbot(label="Conversation", height=400)
        msg = gr.Textbox(label="Your message", placeholder="Type your question here...")
        clear = gr.Button("Clear Chat")
        
        def respond(message, chat_history):
            bot_message = get_ai_response(message, chat_history)
            chat_history.append((message, bot_message))
            time.sleep(1)  # Simulate processing time
            return "", chat_history
        
        msg.submit(respond, [msg, chatbot], [msg, chatbot])
        clear.click(lambda: None, None, chatbot, queue=False)
    
    with gr.Tab("Flight Search"):
        gr.Markdown("### Find the best flights for your journey")
        
        with gr.Row():
            with gr.Column():
                from_city = gr.Textbox(label="From", placeholder="Departure city")
                to_city = gr.Textbox(label="To", placeholder="Destination city")
                depart_date = gr.Textbox(label="Departure Date", placeholder="YYYY-MM-DD")
            
            with gr.Column():
                return_date = gr.Textbox(label="Return Date (optional)", placeholder="YYYY-MM-DD")
                passengers = gr.Dropdown(choices=["1", "2", "3", "4", "5+"], label="Passengers", value="1")
                search_btn = gr.Button("Search Flights", variant="primary")
        
        results = gr.Markdown(label="Search Results")
        
        search_btn.click(
            handle_flight_search, 
            [from_city, to_city, depart_date, return_date, passengers], 
            results
        )
    
    with gr.Tab("Flight Status"):
        gr.Markdown("### Check your flight status")
        flight_number = gr.Textbox(label="Flight Number", placeholder="e.g., SW425")
        status_btn = gr.Button("Check Status", variant="primary")
        status_result = gr.Markdown()
        
        status_btn.click(check_flight_status, flight_number, status_result)
    
    with gr.Tab("Manage Booking"):
        gr.Markdown("### Manage your existing booking")
        booking_ref = gr.Textbox(label="Booking Reference", placeholder="6-character code")
        last_name = gr.Textbox(label="Last Name", placeholder="As on booking")
        manage_btn = gr.Button("Retrieve Booking", variant="primary")
        
        gr.Markdown("### Once retrieved, you can:")
        gr.Markdown("- Change your flight dates")
        gr.Markdown("- Select seats")
        gr.Markdown("- Add baggage")
        gr.Markdown("- Request special meals")
        gr.Markdown("- Cancel your booking")
        
        manage_result = gr.Markdown()
        
        def retrieve_booking(ref, name):
            if not ref or not name:
                return "Please enter both your booking reference and last name."
            return f"Booking **{ref}** for **{name}** found! What would you like to do with your booking?"
        
        manage_btn.click(retrieve_booking, [booking_ref, last_name], manage_result)
    
    with gr.Tab("Information"):
        gr.Markdown("### Airline Information")
        
        with gr.Accordion("Baggage Policy", open=False):
            gr.Markdown("""
            - **Carry-on**: 1 bag up to 7kg + 1 personal item
            - **Checked baggage**: Up to 23kg for economy, 32kg for business class
            - **Additional bags**: $50 per bag (up to 2 additional)
            - **Special items**: Sports equipment and musical instruments accepted with prior notice
            """)
        
        with gr.Accordion("Check-in Options", open=False):
            gr.Markdown("""
            - **Online check-in**: Available 24h to 1h before flight
            - **Mobile boarding pass**: Sent to your email after check-in
            - **Airport kiosks**: Available at all our destinations
            - **Counter check-in**: Opens 3h before departure, closes 45min before
            """)
        
        with gr.Accordion("Special Assistance", open=False):
            gr.Markdown("""
            We provide assistance for:
            - Passengers with reduced mobility
            - Unaccompanied minors
            - Medical conditions
            - Elderly passengers
            
            Please contact us at least 48 hours before your flight.
            """)
        
        with gr.Accordion("Contact Information", open=False):
            gr.Markdown("""
            - **Customer Service**: 1-800-SKY-WAY (1-800-759-929)
            - **Email**: support@skywayairlines.com
            - **Twitter**: @SkyWaySupport
            - **Emergency**: 1-800-759-911 (24/7)
            """)

if __name__ == "__main__":
    demo.launch()