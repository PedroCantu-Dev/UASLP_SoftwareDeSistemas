0 0x0 EJER3 START 0  
1 0x0  RESW 10H  
2 0x30 NUM WORD 64  !ERROR!,:Simbolo:,Simbolo duplicado 
3 0x33  RESB 64  
4 0x73 VALOR WORD 16H  !ERROR!,:Simbolo:,Simbolo duplicado 
5 0x76  HIO   
6 0x77 INICIO CLEAR X  !ERROR!,:Simbolo:,Simbolo duplicado 
7 0x79  LDT NUMERO  
8 0x7c  RESW 10  
9 0x9a  BASE TABLA  
10 0x9a  +MUL #INICIO  
11 0x9e  LDA @VALOR  
12 0xa1  +STA #VALORES  
13 0xa5  MULR X,A  
14 0xa7 TEMP RESW 2  !ERROR!,:Simbolo:,Simbolo duplicado 
15 0xad CAD BYTE C'EJERC3'  !ERROR!,:Simbolo:,Simbolo duplicado 
16 0xb3 TABLA RESW 1004H  !ERROR!,:Simbolo:,Simbolo duplicado 
17 0x30bf  LDCH NUM  
18 0x30c2  +JGT 100H,X  
19 0x30c6  COMP TEMP  
20 0x30c9  RESB 1  
21 0x30ca  BYTE X'321'  
22 0x30cc  RSUB   
23 0x30cf  END   
