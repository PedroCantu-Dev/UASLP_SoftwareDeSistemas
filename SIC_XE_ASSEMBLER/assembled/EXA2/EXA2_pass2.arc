0 0x0 EXA2 START 0H ---- ----
1 0x0 BUSCA +LDB #DIRMAX 69101038* 69101038*
2 0x4  BASE DIRMAX ---- ----
3 0x4  SHIFT A,3 !ERROR!,:Mnemonic:,Instruccion no existe 
4 0x4  LDT #MAX 754003 754003
5 0x7  STT DIRM,X 87efff: simbolo no encontrado en la tabla de simbolos 87efff: simbolo no encontrado en la tabla de simbolos
6 0xa  LDCH CAD 532028 532028
7 0xd  STCH @DIRMAX 564000 564000
8 0x10  LDX #1 050001 050001
9 0x13 ETIQ SIO #1 !ERROR!,:Sintaxis:,sobra un operando 
10 0x13  LDS #ETIQUETA 6d6fff: simbolo no encontrado en la tabla de simbolos 6d6fff: simbolo no encontrado en la tabla de simbolos
11 0x16 CICLO LDCH CAD,X 53a01c 53a01c
12 0x19  +AND #1000H 41101000 41101000
13 0x1d  RMO A,T ac05 ac05
14 0x1f  LDCH @DIRMAX 524000 524000
15 0x22  COMPR T,A a050 a050
16 0x24  JGT MAYOR 372003 372003
17 0x27  J TABLA 3f6fff: simbolo no encontrado en la tabla de simbolos 3f6fff: simbolo no encontrado en la tabla de simbolos
18 0x2a MAYOR STCH MAX 574003 574003
19 0x2d AVANZA TIXR S b840 b840
20 0x2f  JLT CICLO 3b2fe4 3b2fe4
21 0x32  RSUB  4f0000 4f0000
22 0x35 CAD BYTE X'0F3224' 0F3224 0F3224
23 0x38  RESB 1000H ---- ----
24 0x1038 DIRMAX RESW 1 ---- ----
25 0x103b  RMO A !ERROR!,:Sintaxis:,Falta  o sobra un operando en la operacion 
26 0x103b MAX RESB 1 ---- ----
27 0x103c MAIN +JSUB BUSCA 4b100000* 4b100000*
28 0x1040  CLEAR A b400 b400
29 0x1042 MAYOR LDCH MAX 532ff6 !ERROR!,:Simbolo:,Simbolo duplicado 532ff6
30 0x1045  BYTE X'FF' FF FF
31 0x1046  END MAIN ---- ----
