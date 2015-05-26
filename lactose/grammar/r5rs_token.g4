grammar r5rs_token;
//lisp token parser according to the r5rs standart


//token: IDENTIFIER | BOOLEAN | number | CHARACTER | STRING;
token: IDENTIFIER | BOOLEAN | NUMBER | CHARACTER | STRING;

IDENTIFIER: INITIAL SUBSEQUENT*;
fragment INITIAL: LETTER | SPECIAL_INITIAL;
fragment LETTER: [a-zA-Z];
fragment SPECIAL_INITIAL: [$:?_];
fragment SUBSEQUENT: INITIAL | DIGIT_10; //| SPECIAL_SUBSEQUENT;
fragment SPECIAL_SUBSEQUENT: [+-.@];

CHARACTER: '#\\' . | '#\\' CHARACTER_NAME ;
fragment CHARACTER_NAME: S P A C E | N E W L I N E;

STRING: '"' STRING_ELEMENT* '"';
fragment STRING_ELEMENT: ~('"' | '\\') | '\\"' | '\\\\';

NUMBER: NUM_2 | NUM_8 | NUM_10 | NUM_16;
fragment NUM_2: PREFIX_2 COMPLEX_2;
fragment COMPLEX_2: REAL_2 | REAL_2 '@' REAL_2 | REAL_2 '+' UREAL_2 I | REAL_2 '-' UREAL_2 I | REAL_2 '+' I
                  | REAL_2 '-' I | '+' UREAL_2 I | '-' UREAL_2 I | '+' I | '-' I;
fragment REAL_2:  UREAL_2;
fragment UREAL_2: UINTEGER_2 | UINTEGER_2 '/' UINTEGER_2;
fragment UINTEGER_2: DIGIT_2+ '#'*;
fragment PREFIX_2: RADIX_2 EXACTNESS | EXACTNESS RADIX_2;
fragment NUM_8: PREFIX_8 COMPLEX_8;
fragment COMPLEX_8: REAL_8 | REAL_8 '@' REAL_8 | REAL_8 '+' UREAL_8 I | REAL_8 '-' UREAL_8 I | REAL_8 '+' I 
                  | REAL_8 '-' I | '+' UREAL_8 I | '-' UREAL_8 I | '+' I | '-' I;
fragment REAL_8:  UREAL_8;
fragment UREAL_8: UINTEGER_8 | UINTEGER_8 '/' UINTEGER_8;
fragment UINTEGER_8: DIGIT_8+ '#'*;
fragment PREFIX_8: RADIX_8 EXACTNESS | EXACTNESS RADIX_8;
fragment NUM_10: PREFIX_10 COMPLEX_10;
fragment COMPLEX_10: REAL_10 | REAL_10 '@' REAL_10 | REAL_10 '+' UREAL_10 I | REAL_10 '-' UREAL_10 I 
                  | REAL_10 '+' I | REAL_10 '-' I | '+' UREAL_10 I | '-' UREAL_10 I | '+' I | '-' I;
fragment REAL_10:  UREAL_10;
fragment UREAL_10: UINTEGER_10 | UINTEGER_10 '/' UINTEGER_10 | DECIMAL_10;
fragment UINTEGER_10: DIGIT_10+ '#'*;
fragment PREFIX_10: RADIX_10 EXACTNESS | EXACTNESS RADIX_10;
fragment NUM_16: PREFIX_16 COMPLEX_16;
fragment COMPLEX_16: REAL_16 | REAL_16 '@' REAL_16 | REAL_16 '+' UREAL_16 I | REAL_16 '-' UREAL_16 I 
                   | REAL_16 '+' I | REAL_16 '-' I | '+' UREAL_16 I | '-' UREAL_16 I | '+' I | '-' I;
fragment REAL_16:  UREAL_16;
fragment UREAL_16: UINTEGER_16 | UINTEGER_16 '/' UINTEGER_16;
fragment UINTEGER_16: DIGIT_16+ '#'*;
fragment PREFIX_16: RADIX_16 EXACTNESS | EXACTNESS RADIX_16;
fragment DECIMAL_10: UINTEGER_10 SUFFIX | '.' DIGIT_10+ '#'* SUFFIX | DIGIT_10+ '.' DIGIT_10* '#'* SUFFIX 
                   | DIGIT_10+ '#'+ . '#'* SUFFIX;
fragment SUFFIX: (EXPONENT_MARKER SIGN DIGIT_10)?;
fragment EXPONENT_MARKER: E|S|F|D|L;
fragment SIGN: [+-]?;
fragment EXACTNESS: ('#'I | '#'E)?;
fragment RADIX_2: '#'B;
fragment RADIX_8: '#'O;
fragment RADIX_10: ('#'D)?;
fragment RADIX_16: '#'X;
fragment DIGIT_2: [0-1];
fragment DIGIT_8: [0-7];
fragment DIGIT_10: [0-9];
fragment DIGIT_16: [0-9a-fA-F];

BOOLEAN: '#'T | '#'F;

fragment A: 'A' | 'a';
fragment B: 'B' | 'b';
fragment C: 'C' | 'c';
fragment D: 'D' | 'd';
fragment E: 'E' | 'e';
fragment F: 'F' | 'f';
fragment G: 'G' | 'g';
fragment H: 'H' | 'h';
fragment I: 'I' | 'i';
fragment J: 'J' | 'j';
fragment K: 'K' | 'k';
fragment L: 'L' | 'l';
fragment M: 'M' | 'm';
fragment N: 'N' | 'n';
fragment O: 'O' | 'o';
fragment P: 'P' | 'p';
fragment Q: 'Q' | 'q';
fragment R: 'R' | 'r';
fragment S: 'S' | 's';
fragment T: 'T' | 't';
fragment U: 'U' | 'u';
fragment V: 'V' | 'v';
fragment W: 'W' | 'w';
fragment X: 'X' | 'x';
fragment Y: 'Y' | 'y';
fragment Z: 'Z' | 'z';
