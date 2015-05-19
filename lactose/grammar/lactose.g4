grammar lactose;

import r5rs_token;

lactose_program: token*;

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

SPACES: [ \t]+ -> skip;