0|PROGB|PROGB|000000|PROGB|CSECT||
1|PROGB|PROGB|000000||EXTDEF|LISTB,ENDB|
2|PROGB|PROGB|000000||EXTREF|LISTA,ENDA,LISTC,ENDC|
3|PROGB|PROGB|000000||ORG|36h|
4|PROGB|PROGB|000036|REF1|+LDA|LISTA|
5|PROGB|PROGB|00003A|REF2|LDT|LISTB+4|
6|PROGB|PROGB|00003D|REF3|+LDX|#ENDA-LISTA|
7|PROGB|PROGB|000041||ORG|60h|
8|PROGB|PROGB|000060|LISTB|EQU|*|
9|PROGB|PROGB|000060||ORG|70H|
10|PROGB|PROGB|000070|ENDB|EQU|*|
11|PROGB|PROGB|000070|REF4|WORD|ENDA-LISTA+LISTC|
12|PROGB|PROGB|000073|REF5|WORD|ENDC-LISTC-10|
13|PROGB|PROGB|000076|REF6|WORD|ENDC-LISTC+LISTA-1|
14|PROGB|PROGB|000079|REF7|WORD|ENDA-LISTA-(ENDB-LISTB)|
15|PROGB|PROGB|00007C|REF8|WORD|LISTB-LISTA|
