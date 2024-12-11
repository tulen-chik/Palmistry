import pandas as pd
from sklearn.model_selection import train_test_split
from transformers import BertTokenizer, BertForSequenceClassification, Trainer, TrainingArguments
import torch
from data import data

# Преобразование в DataFrame
df = pd.DataFrame(data)

# Кодирование меток
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


df['label'] = df['label'].map(label_map)

# Разделение на обучающую и тестовую выборки
train_texts, test_texts, train_labels, test_labels = train_test_split(df['text'], df['label'], test_size=0.2)

# Загрузка токенизатора и модели
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertForSequenceClassification.from_pretrained('bert-base-uncased', num_labels=len(label_map))

# Токенизация
train_encodings = tokenizer(train_texts.tolist(), truncation=True, padding=True)
test_encodings = tokenizer(test_texts.tolist(), truncation=True, padding=True)

# Создание Dataset
class NewsDataset(torch.utils.data.Dataset):
    def __init__(self, encodings, labels):
        self.encodings = encodings
        self.labels = labels

    def __getitem__(self, idx):
        item = {key: torch.tensor(val[idx]) for key, val in self.encodings.items()}
        item['labels'] = torch.tensor(self.labels[idx])
        return item

    def __len__(self):
        return len(self.labels)

train_dataset = NewsDataset(train_encodings, train_labels.tolist())
test_dataset = NewsDataset(test_encodings, test_labels.tolist())

training_args = TrainingArguments(
    output_dir='./results',
    num_train_epochs=12,  # Увеличьте до 10-15 при необходимости
    per_device_train_batch_size=16,  # Попробуйте 32, если память позволяет
    per_device_eval_batch_size=16,
    warmup_steps=500,
    weight_decay=0.01,  # Регуляризация
    logging_dir='./logs',
    logging_steps=10,
    eval_strategy="epoch",  # Оценка на каждой эпохе
    save_strategy="epoch",  # Сохранение лучшей модели
    load_best_model_at_end=True,  # Загрузка лучшей модели
    fp16=True,  # Использование смешанной точности (если поддерживается)
)

# Обучение
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=test_dataset,
)

trainer.train()

# Оценка
trainer.evaluate()

model.save_pretrained('./fine_tuned_model')
tokenizer.save_pretrained('./fine_tuned_model')
