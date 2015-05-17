grammar lactose;

lactose_program
    : function_declare
    ;

function_declare
    : NAME arguments function_body
    ;

function_body
    : (OR function_branch NL)+
    ;

function_branch
    : condition EQ INT
    ;

condition
    : NAME (LESS | MR | EQUAL) INT
    ;

arguments: NAME+;

NAME: [a-zA-Z]+;

INT: '-'?[0-9]+;

EQ: '=';

OR: '|';

NL: '\n';

MR: '>';

LESS: '<';

EQUAL: '==';

WS :   [ \t]+ -> skip;


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
