grammar lactose;

import r5rs_token;

parse: (function_define | scheme_block)*;

expression 
    : arithmetic_expression
    | lambda_function
    | list_expression
    ;

arithmetic_expression
    : arithmetic_expression '**' arithmetic_expression
    | arithmetic_expression ('*'|'/'|'%'|'//') arithmetic_expression
    | arithmetic_expression ('+'|'-') arithmetic_expression
    | arithmetic_expression ('<<' | '>>') arithmetic_expression
    | arithmetic_expression '&' arithmetic_expression
    | arithmetic_expression '^' arithmetic_expression
    | arithmetic_expression '|' arithmetic_expression
    | arithmetic_expression 'and' arithmetic_expression
    | arithmetic_expression 'or' arithmetic_expression
    | arithmetic_expression ('<' | '<=' | '>' | '>=') arithmetic_expression
    | arithmetic_expression ('==' | '!=') arithmetic_expression
    | ('+'|'-') arithmetic_expression
    | ('not'|'~') arithmetic_expression
    | if_condition
    | token
    | IDENTIFIER
    | function_call
    | lambda_function_call    
    | '(' arithmetic_expression ')'
    ;

list_expression: '[' expression* ']';

if_condition: 'if' expression 'then' expression 'else' expression;

function_define: 'def' IDENTIFIER function_arguments '=' (function_body | '{' function_body '}');
function_body: function_body_token (';' function_body_token)*;
function_body_token: function_define | expression;
function_arguments: IDENTIFIER*;

lambda_function: '\\' function_arguments '->' function_body;

function_call: IDENTIFIER expression*;
lambda_function_call: '(' lambda_function ')' expression*;

scheme_block: SCHEME_BLOCK_BODY 'export' IDENTIFIER function_arguments;
SCHEME_BLOCK_BODY: '{{' ~[}]* '}}';

COMMENT:  '--' ~( [\n] )* -> skip;
SPACES: [ \t\n]+ -> skip;