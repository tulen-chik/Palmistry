from handlers.place_handler import get_places, send_places

def handle_location(message):
    user_id = message.chat.id
    latitude = message.location.latitude
    longitude = message.location.longitude

    places = get_places(user_id, latitude, longitude)
    send_places(user_id, places)