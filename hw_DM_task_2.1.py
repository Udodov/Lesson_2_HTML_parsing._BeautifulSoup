import requests
from bs4 import BeautifulSoup
import json

# URL страницы
url = 'http://books.toscrape.com/catalogue/page-1.html'

# Выполняем запрос к странице с указанием кодировки utf-8
response = requests.get(url)
response.encoding = 'utf-8'
response.raise_for_status()  # Проверяем успешность запроса

# Создаем объект BeautifulSoup для парсинга HTML
soup = BeautifulSoup(response.text, 'html.parser')

# Функция для получения данных о книге
def get_book_data(book):
    title = book.h3.a['title']
    price = book.find('p', class_='price_color').text
    in_stock = book.find('p', class_='instock availability').text.strip()
    description = "No description available"  # В данном примере описание не извлекается

    # Преобразуем цену в float, удаляя символ валюты и пробелы
    price = float(price.replace('£', '').replace('Â', '').strip())

    # Преобразуем наличие в int
    in_stock = 1 if 'In stock' in in_stock else 0

    return {
        'title': title,
        'price': price,
        'in_stock': in_stock,
        'description': description
    }

# Находим все элементы книги на странице
books = soup.find_all('article', class_='product_pod')

# Извлекаем данные о книгах
books_data = [get_book_data(book) for book in books]

# Сохраняем данные в JSON файл
with open('books_data.json', 'w', encoding='utf-8') as f:
    json.dump(books_data, f, indent=4, ensure_ascii=False)

print("Данные успешно сохранены в books_data.json")
