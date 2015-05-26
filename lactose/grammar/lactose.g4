grammar lactose;

import r5rs_token;

lactose_program: function_define*;

expression 
    : '(' expression ')' 
    | if_condition
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
    | function_call
    | lambda_function_call
    ;

if_condition: 'if' expression expression expression;

function_define: IDENTIFIER '=' lambda_function
               | IDENTIFIER function_arguments '=' function_body;

lambda_function: '(' lambda_function ')' | '\\' function_arguments '->' function_body;

function_body: function_body_token (';' function_body_token)*;
function_body_token: function_define | expression;
function_arguments: IDENTIFIER*;

function_call: IDENTIFIER expression*;
lambda_function_call: lambda_function expression*;

COMMENT:  '--' ~( '\n' )* -> skip;
SPACES: [ \t\n]+ -> skip;