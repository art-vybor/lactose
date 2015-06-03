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
объявление функций внутри функции
добавить тесты на все виды выражений
регистронезависимость в проверке видимости символов.