#lang r5rs

(define (print_sqr x) (display (expt x 2)))
(define (main) (display (car (list 1 2 3))) (newline) (print_sqr 3) (newline))
(main)