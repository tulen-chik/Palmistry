from transformers import BertTokenizer, BertForSequenceClassification
from transformers import pipeline

label_map = {
    "Ночные клубы": 0,
    "Спортивные клубы": 1,
    "Киберспортивные арены": 2,
    "Кафе": 3,
    "Танцевальные студии": 4,
    "Туристические агентства": 5,
    "Волонтерские организации": 6,
    "Библиотеки": 7,
    "Книжные магазины": 8,
    "Игровые кафе": 9,
    "Мастерские": 10,
    "Парки": 11,
    "Студии йоги": 12,
    "Музеи": 13,
    "Квест-комнаты": 14,
    "Книжные клубы": 15,
    "Концертные залы": 16,
    "Киберспортивные турниры": 17,
    "Пикниковые зоны": 18,
    "Мастер-классы": 19
}


def initAI():
    model = BertForSequenceClassification.from_pretrained("./fine_tuned_model")
    tokenizer = BertTokenizer.from_pretrained("./fine_tuned_model")
    global text_classification
    text_classification = pipeline("text-classification", model=model, tokenizer=tokenizer)

def generateCategory(user_input: str):
    result = text_classification(user_input)
    category = list(label_map.keys())[list(label_map.values()).index(int(result[0]['label'][-1]))]
    return category
