import requests
import csv
from bs4 import BeautifulSoup


SUB_LINK = 'https://skv.pl'
PAGE_LINK = '&page='
link_result = {}
BASE_URL = input('Введите ссылку на категорию, ссылку брать обязательно с EN версии сайта! ').strip()
path = input('Введи название категории которую хотите спарсить ')


def get_html(BASE_URL):
    page = requests.get(BASE_URL)
    return page


def parser(page):
    soup = BeautifulSoup(page.text, 'lxml')
    container = soup.find('div', id='contentDiv')
    for links in container.find_all('a', attrs='href', class_='flex-column item-info'):
        link_result.setdefault(links.find().text, SUB_LINK + links['href'])
    return link_result


def write_result(path, link_result):
    with open('Out_' + path + '.csv', 'w', newline='', encoding='utf-8') as csv_write:
        writer = csv.writer(csv_write, delimiter=';')
        writer.writerow(('Stock Reference', 'Links'))
        for key, val in link_result.items():
            writer.writerow((key, val))
        print('Парсинг окончен, файл успешно записан')


def page_count(page):
    soup = BeautifulSoup(page.text, 'lxml')
    total_pages = soup.find('span', class_='totalPages').text
    return int(total_pages)


def main():
    page = get_html(BASE_URL)
    count = page_count(page)
    for page in range(1, count):
        parser(get_html(BASE_URL + PAGE_LINK + str(page)))
        print('Всего страниц {}, спарсено {}'.format(count, page))

    write_result(path, link_result)


if __name__ == '__main__':
    main()
