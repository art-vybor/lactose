#lang r5rs
(define (main) (display (program)) (write (program)) (newline))
(define (program) "def main = display program; write program; newline\ndef program = ")
(main)