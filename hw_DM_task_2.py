import requests
from bs4 import BeautifulSoup
import json

# Базовый URL сайта
base_url = 'http://books.toscrape.com/catalogue/'

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

# Функция для получения данных со всех страниц
def scrape_all_pages(base_url):
    page_number = 1
    books_data = []

    while True:
        # Формируем URL для текущей страницы
        url = f'{base_url}page-{page_number}.html'
        
        # Выполняем запрос к странице с указанием кодировки utf-8
        response = requests.get(url)
        response.encoding = 'utf-8'
        
        # Если страница не существует (404 ошибка), выходим из цикла
        if response.status_code == 404:
            break
        
        response.raise_for_status()  # Проверяем успешность запроса

        # Создаем объект BeautifulSoup для парсинга HTML
        soup = BeautifulSoup(response.text, 'html.parser')

        # Находим все элементы книги на странице
        books = soup.find_all('article', class_='product_pod')

        # Извлекаем данные о книгах и добавляем их в общий список
        for book in books:
            book_data = get_book_data(book)
            books_data.append(book_data)

        print(f"Собраны данные со страницы {page_number}")
        
        # Переходим к следующей странице
        page_number += 1

    return books_data

# Собираем данные со всех страниц
all_books_data = scrape_all_pages(base_url)

# Сохраняем данные в JSON файл
with open('all_books_data.json', 'w', encoding='utf-8') as f:
    json.dump(all_books_data, f, indent=4, ensure_ascii=False)

print("Данные успешно сохранены в all_books_data.json")
