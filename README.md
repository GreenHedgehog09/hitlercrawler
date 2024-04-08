# Task #4. Hitler crawler (EN)
## Installation Guide
1. Install Python 3.11.4: https://www.python.org/downloads/release/python-3114/.
2. Open the console in the main project directory.
3. Create a virtual environment: Windows - python -m venv venv, Linux - python3 -m venv venv.
4. Activate the virtual environment: Windows - venv\Scripts\activate, Linux - source venv/bin/activate.
5. Install necessary modules: pip install -r requirements.txt
6. Run the program: Windows - python main.py, Linux - python3 main.py.

## Description
The program receives a Wikipedia article, scans it for links to other Wikipedia articles, opens them, and scans for links until it finds a link to the Wikipedia page about Hitler (maximum 6 redirects).

The program utilizes multiprocessing. If at any stage of the search there are more than 1 link on the page and the result has not been found yet, 2 new processes are launched for parallel search. The requests to the wiki pages themselves are executed asynchronously.

Input - URL, output - URL of the Wikipedia page about Hitler, execution time, or an error indicating that the page was not found.

Execution time: 6 hours 59 minutes.

# Task #4. Hitler crawler (UA)
## Інструкція з інсталяції
1. Встановити Python 3.11.4: https://www.python.org/downloads/release/python-3114/.
2. Відкрити консоль в головній директорії проєкту.
3. Створюємо віртуальне середовище: Windows - python -m venv venv, Linux - python3 -m venv venv.
4. Активуємо віртуальне середовище: Windows - venv\Scripts\activate, Linux - source venv/bin/activate.
5. Встановлюємо необхідні модулі: pip install -r requirements.txt
6. Запуск програми: Windows - python main.py, Linux - python3 main.py.

## Опис роботи
Програма отримує статтю Вікіпедії, сканує її на наявність посилань на інші статті Вікіпедії, відкриває їх і сканує посилання, поки не знайде посилання на сторінку Вікіпедії про Гітлера(макс 6 перенаправлень).

У програмі використовується багатопроцесорність. Якщо на якомусь із етапів пошуку на сторінці більше 1 посилання і результат ще не знайдено, то запускаються 2 нових процеси для паралельного пошуку. Самі запити до сторінок wiki виконуються асинхронно.

Вхід - URL, вихід - URL сторінки wiki про Гітлера, час виконання або помилка, що сторінку не знайдено.

Час виконання роботи: 6 год. 59 хв.