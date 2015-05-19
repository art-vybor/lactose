grammar lactose;

lactose_program
    : token+
    ;

// function_declare
//     : NAME arguments function_body
//     ;

// function_body
//     : (OR function_branch NL)+
//     ;

// function_branch
//     : condition EQ INT
//     ;

// condition
//     : NAME (LESS | MR | EQUAL) INT
//     ;

// arguments: NAME+;

// NAME: [a-zA-Z]+;

// INT: '-'?[0-9]+;

// EQ: '=';

// OR: '|';

// NL: '\n';

// MR: '>';

// LESS: '<';

// EQUAL: '==';

WS :   [ \t]+ -> skip;

// NUMBER

// token: identifier | BOOLEAN | number | character | string;
token: BOOLEAN | number;


number: NUM_2 | NUM_8 | NUM_10 | NUM_16;

NUM_2: PREFIX_2 COMPLEX_2;
fragment COMPLEX_2: REAL_2 | REAL_2 '@' REAL_2 
                  | REAL_2 '+' UREAL_2 'i' | REAL_2 '-' UREAL_2 'i' 
                  | REAL_2 '+' 'i' | REAL_2 '-' 'i'
                  | '+' UREAL_2 'i' | '-' UREAL_2 'i' | '+' 'i' | '-' 'i';
fragment REAL_2: SIGN UREAL_2;
fragment UREAL_2: UINTEGER_2 | UINTEGER_2 '/' UINTEGER_2 | DECIMAL_10;
fragment UINTEGER_2: DIGIT_2+ '#'*;
fragment PREFIX_2: RADIX_2 EXACTNESS | EXACTNESS RADIX_2;

NUM_8: PREFIX_8 COMPLEX_8;
fragment COMPLEX_8: REAL_8 | REAL_8 '@' REAL_8 
                  | REAL_8 '+' UREAL_8 'i' | REAL_8 '-' UREAL_8 'i' 
                  | REAL_8 '+' 'i' | REAL_8 '-' 'i'
                  | '+' UREAL_8 'i' | '-' UREAL_8 'i' | '+' 'i' | '-' 'i';
fragment REAL_8: SIGN UREAL_8;
fragment UREAL_8: UINTEGER_8 | UINTEGER_8 '/' UINTEGER_8 | DECIMAL_10;
fragment UINTEGER_8: DIGIT_8+ '#'*;
fragment PREFIX_8: RADIX_8 EXACTNESS | EXACTNESS RADIX_8;


NUM_10: PREFIX_10 COMPLEX_10;
fragment COMPLEX_10: REAL_10 | REAL_10 '@' REAL_10 
                  | REAL_10 '+' UREAL_10 'i' | REAL_10 '-' UREAL_10 'i' 
                  | REAL_10 '+' 'i' | REAL_10 '-' 'i'
                  | '+' UREAL_10 'i' | '-' UREAL_10 'i' | '+' 'i' | '-' 'i';
fragment REAL_10: SIGN UREAL_10;
fragment UREAL_10: UINTEGER_10 | UINTEGER_10 '/' UINTEGER_10 | DECIMAL_10;
fragment UINTEGER_10: DIGIT_10+ '#'*;
fragment PREFIX_10: RADIX_10 EXACTNESS | EXACTNESS RADIX_10;

NUM_16: PREFIX_16 COMPLEX_16;
fragment COMPLEX_16: REAL_16 | REAL_16 '@' REAL_16 
                  | REAL_16 '+' UREAL_16 'i' | REAL_16 '-' UREAL_16 'i' 
                  | REAL_16 '+' 'i' | REAL_16 '-' 'i'
                  | '+' UREAL_16 'i' | '-' UREAL_16 'i' | '+' 'i' | '-' 'i';
fragment REAL_16: SIGN UREAL_16;
fragment UREAL_16: UINTEGER_16 | UINTEGER_16 '/' UINTEGER_16 | DECIMAL_10;
fragment UINTEGER_16: DIGIT_16+ '#'*;
fragment PREFIX_16: RADIX_16 EXACTNESS | EXACTNESS RADIX_16;

fragment DECIMAL_10: UINTEGER_10 SUFFIX
                   | '.' DIGIT_10+ '#'* SUFFIX 
                   | DIGIT_10+ '.' DIGIT_10* '#'* SUFFIX 
                   | DIGIT_10+ '#'+ . '#'* SUFFIX;

fragment SUFFIX: (EXPONENT_MARKER SIGN DIGIT_10)?;
fragment EXPONENT_MARKER: [esfdl];
fragment SIGN: [+-]?;
fragment EXACTNESS: ('#i' | '#e')?;
fragment RADIX_2: '#b';
fragment RADIX_8: '#o';
fragment RADIX_10: ('#d')?;
fragment RADIX_16: '#x';
fragment DIGIT_2: [0-1];
fragment DIGIT_8: [0-7];
fragment DIGIT_10: [0-9];
fragment DIGIT_16: [0-9a-f];

BOOLEAN: '#t' | '#f';

// json:   object_
//     |   array
//     ;

// object_
//     :   '{' pair (',' pair)* '}'
//     |   '{' '}' // empty object
//     ;
    
// pair:   STRING ':' value ;

// array
//     :   '[' value (',' value)* ']'
//     |   '[' ']' // empty array
//     ;

// value
//     :   STRING
//     |   NUMBER
//     |   object_  // recursion
//     |   array   // recursion
//     |   'true'  // keywords
//     |   'false'
//     |   'null'
//     ;

// STRING :  '"' (ESC | ~["\\])* '"' ;
// fragment ESC :   '\\' (["\\/bfnrt] | UNICODE) ;
// fragment UNICODE : 'u' HEX HEX HEX HEX ;
// fragment HEX : [0-9a-fA-F] ;
// NUMBER
//     :   '-'? INT '.' [0-9]+ EXP? // 1.35, 1.35E-9, 0.3, -4.5
//     |   '-'? INT EXP             // 1e10 -3e4
//     |   '-'? INT                 // -3, 45
//     ;
// fragment INT :   '0' | [1-9] [0-9]* ; // no leading zeros
// fragment EXP :   [Ee] [+\-]? INT ; // \- since - means "range" inside [...]
