#lang r5rs
(define (one) 1)
(define (gcd a b) (if (eq? b 0) a (gcd b (remainder a b))))
(define (abs a) (if (>= a 0) a (- a)))
(define (sqr x) (binpow x 2))
(define binpow (lambda (a n) (if (eq? n 0) 1 (if (eq? (remainder n 2) 1) (* (binpow a (- n 1)) a) (expt (binpow a (/ n 2)) 2)))))
(define (fib n) (/ (- (expt (/ (+ 1 (sqrt 5)) 2) n) (expt (/ (- 1 (sqrt 5)) 2) n)) (sqrt 5)))
(define (fact n) (if (eq? n 0) 1 (* n (fact (- n 1)))))
(define (print x) (display x) (newline))
(define (main) (print (one)) (print (gcd 2 8)) (print (fib 4)) (print (sqr 2)) (print (abs (- 5))) (print (fact 3)) (print (+ (+ (one) (sqr 2)) (abs (- 2)))) (print (binpow 2 3)))
(main)