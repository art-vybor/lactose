grammar lactose;

import r5rs_token;

parse: function_define*;

expression 
    : '(' expression ')' 
    | if_condition
    //| ('+'|'-') expression
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
    | function_call
    | lambda_function_call
    | token
    
    ;
function_call: IDENTIFIER expression*;
lambda_function_call: lambda_function expression*;

if_condition: 'if' expression expression expression;

function_define: 'def' (function_define_by_lambda | function_define_default);
function_define_by_lambda: IDENTIFIER '=' lambda_function;
function_define_default: IDENTIFIER function_arguments '=' function_body;

lambda_function: '(' lambda_function ')' | '\\' function_arguments '->' function_body;

function_body: function_body_token (';' function_body_token)*;
function_body_token: function_define | expression;
function_arguments: IDENTIFIER*;

COMMENT:  '--' ~( '\n' )* -> skip;
SPACES: [ \t\n]+ -> skip;