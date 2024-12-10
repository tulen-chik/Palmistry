from handlers.place_handler import get_places, send_places

def handle_location(message):
    user_id = message.chat.id
    coordinates = user_profiles[user_id]['coordinates']

    places = get_places(user_id, coordinates.lat, coordinates.lon)
    send_places(user_id, places)