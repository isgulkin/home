[![Open in Visual Studio Code](https://classroom.github.com/assets/open-in-vscode-f059dc9a6f8d3a56e377f745f24479a46679e63a5d9fe6f495e02850cd0d8118.svg)](https://classroom.github.com/online_ide?assignment_repo_id=5994021&assignment_repo_type=AssignmentRepo)
# k ближайших чисел
Задача: найти `k` чисел, ближайших к заданному значению, в *упорядоченном* массиве. Само значение может не встретиться в массиве.

Пример:
```python3
assert closest([1,4,8,10], target=2, count=3) == [1, 4, 8]
```

Решение должно иметь сложность O(log(n) + k).

Будьте внимательны с тестом `range`: в нём очень большой массив, который может и в память не влезть при попытке копирования.

Использовать модуль `bisect` в этом задании запрещено. Вспоминайте первую лекцию и реализуйте поиск самостоятельно.