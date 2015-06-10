#lang r5rs
(define (abs a) (if (>= a 0) a (- a)))
(define (main) (display (- abs 2)))
(main)