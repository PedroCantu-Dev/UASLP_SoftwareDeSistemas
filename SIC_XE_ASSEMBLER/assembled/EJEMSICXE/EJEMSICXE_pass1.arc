0|EJEMSICXE|EJEMSICXE|000000|EJEMSICXE|START|0H|
1|EJEMSICXE|EJEMSICXE|000000||EXTDEF|TAM,SALTO|
2|EJEMSICXE|EJEMSICXE|000000||EXTREF|SIMBOLO|
3|EJEMSICXE|EJEMSICXE|000000||EXTDEF|COUNT|
4|EJEMSICXE|EJEMSICXE|000000|TABLA|RESW|3|
5|EJEMSICXE|EJEMSICXE|000009|NUM|EQU|19|
6|EJEMSICXE|EJEMSICXE|000009||BASE|SALTO|
7|EJEMSICXE|EJEMSICXE|000009|ETIQ|CLEAR|X|
8|EJEMSICXE|EJEMSICXE|00000B|MAX|EQU|SALTO+2|:ERROR:Sintaxis:variable inexistente en el ambito|
9|EJEMSICXE|EJEMSICXE|00000B|TAM|EQU|*|
10|EJEMSICXE|EJEMSICXE|00000B||+TIX|SIMBOLO|
11|EJEMSICXE|EJEMSICXE|00000F||LDA|#(TABLA-ETIQ+3)|
12|EJEMSICXE|EJEMSICXE|000012||ORG|3060H|
13|EJEMSICXE|EJEMSICXE|003060|SALTO|JLT|ETIQ|
14|EJEMSICXE|EJEMSICXE|003063||LDT|COUNT+4|
15|EJEMSICXE|EJEMSICXE|003066|COUNT|WORD|ETIQ-(TAM-TABLA)|
16|EJEMSICXE|EJEMSICXE|003069||WORD|2*(SALTO-TAM)|
17|EJEMSICXE|EJEMSICXE|00306C||RESB|86|
18|EJEMSICXE|EJEMSICXE|0030C2||WORD|4*(SALTO-TAMANO)|
19|EJEMSICXE|EJEMSICXE|0030C5||END|SALTO|
