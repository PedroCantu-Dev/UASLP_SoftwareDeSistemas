0|BLOQUES|BLOQUES|000000|BLOQUES|START|0|
1|BLOQUES|BLOQUES|000000||STL|RETADR|172019|
2|BLOQUES|BLOQUES|000003|CLOOP|JSUB|RDREC|4B2007|
3|BLOQUES|BLOQUES|000006||+COMP|#MAXLEN|29101000|
4|BLOQUES|BLOQUES|00000A|FIRST|LDA|LENGTH|032012|
5|BLOQUES|CDATA|000000||USE|CDATA|
6|BLOQUES|CDATA|000000|RETADR|RESW|1|
7|BLOQUES|CDATA|000003|LENGTH|RESW|1|
8|BLOQUES|CBLKS|000000||USE|CBLKS|
9|BLOQUES|CBLKS|000000|BUFFER|RESB|4096|
10|BLOQUES|CBLKS|001000|NUM|EQU|18|
11|BLOQUES|CBLKS|001000|BUFFEND|EQU|*|
12|BLOQUES|CBLKS|001000|MAXLEN|EQU|BUFFEND-BUFFER|
13|BLOQUES|CBLKS|001000|RES|EQU|(MAXLEN*NUM-500H)/2|
14|BLOQUES|BLOQUES|00000D||USE||
15|BLOQUES|BLOQUES|00000D|RDREC|CLEAR|X|B410|
16|BLOQUES|BLOQUES|00000F||+LDT|#INIC|75101025*R|
17|BLOQUES|CDATA|000006||USE|CDATA|
18|BLOQUES|CDATA|000006|INPUT|BYTE|X'F1'|F1|
19|BLOQUES|INST|000000||USE|INST|
20|BLOQUES|INST|000000||CLEAR|X|B410|
21|BLOQUES|INST|000002|INIC|LDA|#10|01000A|
22|BLOQUES|FINAL|000000||USE|FINAL|
23|BLOQUES|FINAL|000000|FIN|RSUB||4F0000|
24|BLOQUES|FINAL|000003|EXPRE|EQU|RETADR+BUFFEND-BUFFER|:ERROR:Sintaxis:variable de distinto bloque|
25|BLOQUES|BLOQUES|000013||USE||
26|BLOQUES|BLOQUES|000013||LDT|LENGTH|77200F|
27|BLOQUES|BLOQUES|000016||WORD|RETADR+BUFFEND-BUFFER+10|001026*R|
28|BLOQUES|BLOQUES|000019||WORD|MAXLEN+10|00100A|
29|BLOQUES|BLOQUES|00001C||END|INIC|
