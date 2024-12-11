from config import user_profiles

def update_profile(user_id, personality_choice):
    if user_id not in user_profiles:
        user_profiles[user_id] = {
            'personality': personality_choice,
            'preferences': {
                'places_rated': 0,
                'favorite_places': [],
                'past_choices': []
            }
        }
    else:
        user_profiles[user_id]['personality'] = personality_choice
    user_profiles[user_id]['preferences']['past_choices'].append(personality_choice)

def update_favorite_places(user_id, place_name):
    user_profiles[user_id]['preferences']['favorite_places'].append(place_name)