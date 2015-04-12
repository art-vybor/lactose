#! /usr/bin/racket

#lang r5rs

(define bottles (lambda (n) 
    (case n
        (1 (display 8))
    )

    (display n)
    (newline)
    (cond ((> n 0) (bottles (- n 1))))
  )
)

(bottles 5)