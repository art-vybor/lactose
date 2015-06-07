#lang r5rs
(define (factorial) ((lambda (f) (lambda (x) (f f x))) (lambda (fact x) (if (= x 0) 1 (* x (fact fact (- x 1)))))))
(define (main) (display ((factorial) 5)) (display ((lambda (f) (lambda (x) (f f x))) (lambda (fact x) (if (= x 0) 1 (* x (fact fact (- x 1))))) 5)) (newline))
(main)