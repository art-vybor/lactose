# lactose
Syntax sugar for Scheme.

## installation
Before lactose installation you should install antlr4 for python:
`pip install antlr4-python2-runtime`

To lactose installation you should use `make install` with optional PREFIX.
Example: `PREFIX=~/.local make install`

To use print_to_pdf functionality graphviz package should be installed.
Debian example: `sudo apt-get install graphviz`

## description
All tokens must satisfy the constraints of R5RS standart, so they are case insensitive.
Python ariphmetic syntax are used. 
Priorities:
    1. not, ~
    2. *, /, %, //, **
    3. + -
    4. <<, >>
    5. &
    6. ^
    7. |
    8. and
    9. or
    10. <, <=, >, >=
    11. ==, !=


##books
R5RS standart: http://www.schemers.org/Documents/Standards/R5RS/r5rs.pdf

##error
регистронезависимость в проверке видимости символов.
протестить gitstats

тело функции в {}
Списки [a b c]

В отличие от Scheme локальные определения соответствуют let и letrec

заместо входного языка исходный язык

Scheme задать как целевой

Области видимости символов

удобство использования

Какой алгоритм использует antlr.
Скорее всего механизм возвратов.
Преобразование строки byte в строку символов Unicode имеет сложность O(n), n - длина символа.

Компилятор реализован как препроцессор кscheme. Таким образом образом целевым языком является Scheme

Язык и компилятор получили название lactose (лактоза). Лактоза - молочный сахар (молочный - отсылка к первоначальному обучению программированию, сахар - отсылка к синтаксическому сахару).

про замыкания и определении функций и анонимных функциях, переписать видимость символов.

Разработка через ... (assert)

во введение напомнить про ML и в особенности haskell (многое от scheme унаследовал: управляющие конструкции, связывание имён со значениями и так далее)
добавить литературу ссылка на Haskell 2010 report