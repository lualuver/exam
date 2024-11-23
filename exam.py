import requests
from bs4 import BeautifulSoup


class SiteManager:
    def __init__(self):
        self.sites = []

    def add_site(self, url):
        """Добавить сайт в список"""
        if url not in self.sites:
            self.sites.append(url)
            print(f"Сайт {url} добавлен.")
        else:
            print(f"Сайт {url} уже в списке.")

    def get_sites(self):
        """Получить список всех добавленных сайтов"""
        return self.sites


class SiteParser:
    def __init__(self):
        pass

    def search_on_site(self, url, query):
        """Поиск по сайту: возвращает количество совпадений"""
        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.content, 'html.parser')
            text = soup.get_text().lower()
            query = query.lower()
            matches = text.count(query)
            return matches
        except Exception as e:
            print(f"Ошибка при парсинге сайта {url}: {e}")
            return 0


class UserInterface:
    def __init__(self, app):
        self.app = app

    def display_menu(self):
        """Отображает меню для пользователя"""
        print("1. Добавить сайт")
        print("2. Поиск по сайтам")
        print("3. Выход")

    def get_user_choice(self):
        """Получить выбор пользователя"""
        return input("Введите номер действия: ")

    def get_url(self):
        """Получить URL от пользователя"""
        return input("Введите URL сайта: ")

    def get_search_query(self):
        """Получить запрос для поиска"""
        return input("Введите запрос для поиска: ")

    def handle_user_input(self):
        """Обрабатывает выбор пользователя"""
        while True:
            self.display_menu()
            choice = self.get_user_choice()

            if choice == '1':
                url = self.get_url()
                self.app.add_site(url)

            elif choice == '2':
                query = self.get_search_query()
                self.app.search(query)

            elif choice == '3':
                print("Выход из программы...")
                break

            else:
                print("Неверный выбор. Попробуйте снова.")


class SearchApp:
    def __init__(self):
        self.site_manager = SiteManager()
        self.site_parser = SiteParser()
        self.ui = UserInterface(self)

    def add_site(self, url):
        """Добавить сайт в список"""
        self.site_manager.add_site(url)

    def search(self, query):
        """Поиск по добавленным сайтам"""
        sites = self.site_manager.get_sites()
        results = []

        for site in sites:
            matches = self.site_parser.search_on_site(site, query)
            if matches > 0:
                results.append((site, matches))

        for i in range(len(results)):
            for j in range(i + 1, len(results)):
                if results[i][1] < results[j][1]:
                    results[i], results[j] = results[j], results[i]

        if results:
            print(f"Найдено {len(results)} сайта(ов):")
            for site, matches in results:
                print(f"{site} - {matches} совпадений")
        else:
            print("Совпадений не найдено.")


if __name__ == "__main__":
    app = SearchApp()
    app.ui.handle_user_input()
