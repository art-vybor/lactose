grammar lactose;
r  : 'hellow' t;         // match keyword hello followed by an identifier
t  : ID E q;
q  : ID Q;
E  : 'E';
Q  : 'Q';
ID : [a-z]+ ;             // match lower-case identifiers
WS : [ \t\r\n]+ -> skip ; // skip spaces, tabs, newlines

