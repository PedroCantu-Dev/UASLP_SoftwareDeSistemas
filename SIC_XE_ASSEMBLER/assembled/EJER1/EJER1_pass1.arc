0|EJER1|EJER1|000000|EJER1|START|0|
1|EJER1|EJER1|000000||LDX|#5|
2|EJER1|EJER1|000003||HIO||
3|EJER1|EJER1|000004||+LDB|#TABLE2|
4|EJER1|EJER1|000008||STA|@COUNT|
5|EJER1|EJER1|00000B||CLEAR|A|
6|EJER1|EJER1|00000D||BASE|TABLE2|
7|EJER1|EJER1|00000D||ADDR|X,A|
8|EJER1|EJER1|00000F|LOOP|ADD|TABLE,X|
9|EJER1|EJER1|000012||+STA|TOTAL|
10|EJER1|EJER1|000016||RSUB||
11|EJER1|EJER1|000019|COUNT|RESB|12H|
12|EJER1|EJER1|00002B||SHIFTL|X,2|
13|EJER1|EJER1|00002D|TABLE|RESW|10|
14|EJER1|EJER1|00004B|TABLE2|BYTE|C'TEST'|
15|EJER1|EJER1|00004F||WORD|16|
16|EJER1|EJER1|000052||END||
