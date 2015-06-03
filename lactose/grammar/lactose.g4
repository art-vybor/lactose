grammar lactose;

import r5rs_token;

parse: function_define*;

expression 
    : expression '**' expression
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
    | ('+'|'-') expression
    | ('not'|'~') expression
    | if_condition
    | token
    | IDENTIFIER
    | lambda_function
    | function_call
    | lambda_function_call    
    | '(' expression ')' 
    ;

if_condition: 'if' expression 'then' expression 'else' expression;

function_define: 'def' IDENTIFIER function_arguments '=' function_body; 

function_body: expression (';' expression)*;
//function_body_token: function_define | expression;
function_arguments: IDENTIFIER*;

lambda_function: '\\' function_arguments '->' function_body;

function_call: IDENTIFIER expression*;
lambda_function_call: '(' lambda_function ')' expression*;

COMMENT:  '--' ~( [\n] )* -> skip;
SPACES: [ \t\n]+ -> skip;