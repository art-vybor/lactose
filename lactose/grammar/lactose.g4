grammar lactose;

import r5rs_token;

lactose_program: (function | function_call)*;

expression 
    : '(' expression ')' 
    | ('+'|'-') expression
    | ('not'|'~') expression
    | expression '**' expression
    | expression ('*'|'/'|'%'|'//') expression
    | expression ('+'|'-') expression
    | expression ('<<' | '>>') expression
    | expression '&' expression
    | expression '^' expression
    | expression '|' expression
    | expression 'and' expression
    | expression 'or' expression
    | expression ('<' | '<=' | '>' | '>=') expression
    | expression ('==' | '!=') expression
    | token
    ;

function_call: '(' token expression* ')';

function: token function_arguments function_body;
function_arguments: token*;
function_body: function_branch+;
function_branch: '|' expression '=' expression;

//NEWLINE: '\n' -> skip

COMMENT:  '--' ~( '\n' )* -> skip;
SPACES: [ \t\n]+ -> skip;