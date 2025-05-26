import re
from urllib.request import urlopen
from urllib.error import URLError, HTTPError

def fetch_malware_hashes():
    """Получаем свежие хеши вредоносных программ"""
    source_url = "https://bazaar.abuse.ch/export/txt/sha256/recent/"
    
    try:
        with urlopen(source_url) as response:
            content = response.read().decode('utf-8')
            print('Хеши успешно загружены из источника')
            return content
            
    except (URLError, HTTPError) as error:
        print(f"Ошибка при получении данных: {error}")
        return None

def clean_hash_data(raw_hashes):
    """Очищаем данные от комментариев и лишних символов"""
    if not raw_hashes:
        return []
    
    # Удаляем комментарии и пустые строки
    cleaned = [line for line in raw_hashes.split('\n') 
              if line and not line.startswith('#')]
    return cleaned

def save_hashes_to_file(hash_list, filename='malware_hashes.txt'):
    """Сохраняем хеши в текстовый файл"""
    try:
        with open(filename, 'w') as output_file:
            output_file.write('\n'.join(hash_list))
        print(f"Хеши сохранены в файл {filename}")
    except IOError as e:
        print(f"Ошибка записи в файл: {e}")

def execute_hash_processing():
    """Основной процесс обработки хешей"""
    raw_content = fetch_malware_hashes()
    if raw_content:
        processed_hashes = clean_hash_data(raw_content)
        save_hashes_to_file(processed_hashes)

if __name__ == "__main__":
    execute_hash_processing()
