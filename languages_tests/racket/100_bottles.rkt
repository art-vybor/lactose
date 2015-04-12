#! /usr/bin/racket

#lang r5rs

(define get_ending (lambda (n)
    (if (member n '(11 12 13 14))
        "ок"     
        (case (remainder n 10)
            ((1) "ка")
            ((2 3 4) "ки")
            ((5 6 7 8 9 0) "ок")
        )
    )    
  )
)

(define bottles (lambda (n) 
    (map display (list
        (number->string n) " бутыл" (get_ending n) " на столе.\nОдна упала...\n"
      )
    )

    (cond ((> n 1) (bottles (- n 1))))
  )
)

(bottles 100)