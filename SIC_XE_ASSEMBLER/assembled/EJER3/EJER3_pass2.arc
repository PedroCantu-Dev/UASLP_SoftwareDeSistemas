0 0x0 EJER3 START 0 ---- ----
1 0x0  RESW 10H ---- ----
2 0x30 NUM WORD 64 000040 000040
3 0x33  RESB 64 ---- ----
4 0x73 VALOR WORD 16H 000016 000016
5 0x76  HIO  0xF4 0xF4
6 0x77 INICIO CLEAR X 0xb410 0xb410
7 0x79  LDT NUMERO 0x776fff: simbolo no encontrado en la tabla de simbolos 0x776fff: simbolo no encontrado en la tabla de simbolos
8 0x7c  RESW 10 ---- ----
9 0x9a  BASE TABLA ---- ----
10 0x9a  +MUL #INICIO 0x21100077* 0x21100077*
11 0x9e  LDA @VALOR 0x22fd2 0x22fd2
12 0xa1  +STA #VALORES 0xd7fffff: simbolo no encontrado en la tabla de simbolos 0xd7fffff: simbolo no encontrado en la tabla de simbolos
13 0xa5  MULR X,A 0x9810 0x9810
14 0xa7 TEMP RESW 2 ---- ----
15 0xad CAD BYTE C'EJERC3' 454a45524333 454a45524333
16 0xb3 TABLA RESW 1004H ---- ----
17 0x30bf  LDCH NUM 0x536fff: Instruccion No es relativa ni a (CP) ni a (B) 0x536fff: Instruccion No es relativa ni a (CP) ni a (B)
18 0x30c2  +JGT 100H,X 0x37ffffff: Modo de direccionamiento no existe, constante fuera de rango 0x37ffffff: Modo de direccionamiento no existe, constante fuera de rango
19 0x30c6  COMP TEMP 0x2b6fff: Instruccion No es relativa ni a (CP) ni a (B) 0x2b6fff: Instruccion No es relativa ni a (CP) ni a (B)
20 0x30c9  RESB 1 ---- ----
21 0x30ca  BYTE X'321' 0321 0321
22 0x30cc  RSUB  0x4f0000 0x4f0000
23 0x30cf  END  ---- ----
