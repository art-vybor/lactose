#lang r5rs
(define (fact n) (define (loop i) (if (< i n) (* i (loop (+ i 1))) n)) (loop 1))
(define (main) (display (fact 5)))
(main)