#lang r5rs
(define (f x) 1)
(define (main x) (f ((lambda (x y) 1))) (define (g x) 1))
(main)