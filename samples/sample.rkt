#lang r5rs
(define (main) (display ((lambda (f) (f 3)) (lambda (x) (expt x 2)))) (newline))
(main)