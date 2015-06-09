#lang r5rs
(define (a) (list "def a = " "\ndef main = display (ref a 0); display \"[\"; write (ref a 0); display \" \"; write (ref a 1); display \"]\"; display (ref a 1)"))
(define (main) (display (list-ref (a) 0)) (display "[") (write (list-ref (a) 0)) (display " ") (write (list-ref (a) 1)) (display "]") (display (list-ref (a) 1)))
(main)