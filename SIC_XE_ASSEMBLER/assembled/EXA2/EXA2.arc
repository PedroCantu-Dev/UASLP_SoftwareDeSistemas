0 0x0 EXA2 START 0H  
1 0x0 BUSCA +LDB #DIRMAX  
2 0x4  BASE DIRMAX  
3 0x4  SHIFT A,3 !ERROR!,:Mnemonic:,Instruccion no existe 
4 0x4  LDT #MAX  
5 0x7  STT DIRM,X  
6 0xa  LDCH CAD  
7 0xd  STCH @DIRMAX  
8 0x10  LDX #1  
9 0x13 ETIQ SIO #1 !ERROR!,:Sintaxis:,sobra un operando 
10 0x13  LDS #ETIQUETA  
11 0x16 CICLO LDCH CAD,X  
12 0x19  +AND #1000H  
13 0x1d  RMO A,T  
14 0x1f  LDCH @DIRMAX  
15 0x22  COMPR T,A  
16 0x24  JGT MAYOR  
17 0x27  J TABLA  
18 0x2a MAYOR STCH MAX  
19 0x2d AVANZA TIXR S  
20 0x2f  JLT CICLO  
21 0x32  RSUB   
22 0x35 CAD BYTE X'0F3224'  !ERROR!,:Simbolo:,Simbolo duplicado 
23 0x38  RESB 1000H  
24 0x1038 DIRMAX RESW 1  
25 0x103b  RMO A !ERROR!,:Sintaxis:,Falta  o sobra un operando en la operacion 
26 0x103b MAX RESB 1  
27 0x103c MAIN +JSUB BUSCA  
28 0x1040  CLEAR A  
29 0x1042 MAYOR LDCH MAX  !ERROR!,:Simbolo:,Simbolo duplicado 
30 0x1045  BYTE X'FF'  
31 0x1046  END MAIN  
