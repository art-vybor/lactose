#! /usr/bin/racket

#lang r5rs

; for each pair in l:
;   if not: swap
; #f


(define (swapper l)

    #f
)

(define (sort l)    
    (if (swapper l)
        (sort (swapper l))
        l
    )    
)

(display (sort (list 3 2 1 4)))
(newline)