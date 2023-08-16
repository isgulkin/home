[![Open in Visual Studio Code](https://classroom.github.com/assets/open-in-vscode-f059dc9a6f8d3a56e377f745f24479a46679e63a5d9fe6f495e02850cd0d8118.svg)](https://classroom.github.com/online_ide?assignment_repo_id=5751947&assignment_repo_type=AssignmentRepo)
# Кодирование длин серий
Упрощённый вариант Кодирования длин серий. Повторяющиеся буквы заменяются на число повторов + одну букву. В исходной строке цифры встречаться не могут. Пример: строка "WWWWWWWWWBBBWWWWWWWWWWWWWWWWWWWWWWWBWWWWWWWWWWWWWW" сожмётся до "12W3B24WB14W".

Подробнее этот способ сжатия информации описан в https://ru.wikipedia.org/wiki/Кодирование_длин_серий. Основное отличие: если символ встречается один раз, `1` не дописывается.