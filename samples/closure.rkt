#lang r5rs
(define (make_adder n) (lambda (x) (+ x n)))
(define (inc) (make_adder 1))
(define (dec) (make_adder (- 1)))
(define (main) (display ((inc) 0)) (newline) (display ((dec) 3)) (newline))
(main)