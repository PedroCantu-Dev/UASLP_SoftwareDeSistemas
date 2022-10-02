0 0x0 EJER3 START 0 
1 0x0 PTA RESW 100 !ERROR! :Simbolo: Simbolo duplicado 
2 0x12c  RESW 10H 
3 0x15c NUM WORD 64 !ERROR! :Simbolo: Simbolo duplicado 
4 0x15f  RESB 64 
5 0x19f VALOR WORD 16H !ERROR! :Simbolo: Simbolo duplicado 
6 0x1a2  HIO  
7 0x1a3 INICIO CLEAR X !ERROR! :Simbolo: Simbolo duplicado 
8 0x1a5  LDT NUMERO 
9 0x1a8  RESW 10 
10 0x1c6 PUTAA BASE TABLA 
11 0x1c6  +MUL #INICIO 
12 0x1ca  LDA @VALOR 
13 0x1cd  +STA #VALORES 
14 0x1d1  MULR X,A 
15 0x1d3 TEMP RESW 2 !ERROR! :Simbolo: Simbolo duplicado 
16 0x1d9 CAD BYTE C'EJERC3' !ERROR! :Simbolo: Simbolo duplicado 
17 0x1df TABLA RESW 1004H !ERROR! :Simbolo: Simbolo duplicado 
18 0x31eb  LDCH NUM 
19 0x31ee  +JGT 100H,X 
20 0x31f2  COMP TEMP 
21 0x31f5  RESB 1 
22 0x31f6  BYTE X'321' 
23 0x31f8  RSUB  
24 0x31fb  END  
