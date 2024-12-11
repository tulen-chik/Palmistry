
from transformers import BertTokenizer, BertForSequenceClassification, Trainer, TrainingArguments
from datasets import Dataset
from data import data

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

texts = [item["text"] for item in data]
labels = [label_map[item["label"]] for item in data]

# Создание датасета
dataset = Dataset.from_dict({"text": texts, "label": labels})

# Токенизация данных
tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")
tokenized_dataset = dataset.map(lambda x: tokenizer(x["text"], padding="max_length", truncation=True), batched=True)

# Обучение модели
model = BertForSequenceClassification.from_pretrained("bert-base-uncased", num_labels=20)
training_args = TrainingArguments(output_dir="./results", num_train_epochs=20, per_device_train_batch_size=4)
trainer = Trainer(model=model, args=training_args, train_dataset=tokenized_dataset)
trainer.train()

model.save_pretrained("./my_model")
tokenizer.save_pretrained("./my_model")
