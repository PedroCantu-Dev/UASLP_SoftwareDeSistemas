0 0x0 PARCIAL1 START 0H 
1 0x0  RESB 12 
2 0xc CICLO +JSUB ENTRADA !ERROR! :Simbolo: Simbolo duplicado 
3 0x10  BASE ARREG 
4 0x10  ADD 200,X 
5 0x13  TIO  
6 0x14 ARREG RESW 20 !ERROR! :Simbolo: Simbolo duplicado 
7 0x50 !ERROR! :Sintaxis: Falta  o sobra un operando en la operacion 
8 0x50 CICLO SUB @VALOR !ERROR! :Simbolo: Simbolo duplicado 
9 0x53 !ERROR! :Sintaxis: Operando invalido para BYTE 
10 0x53  WORD 100 
11 0x56  +RSUB  
12 0x5a  BYTE C'F3E0A' 
13 0x5f ENTRADA CLEAR A !ERROR! :Simbolo: Simbolo duplicado 
14 0x61 !ERROR! :Sintaxis: Direccionamiento indirecto e indexado a la vez ( solo el direccionamieto simple puede ser indexado) 
15 0x61  JSUB CICLO,X 
16 0x64 !ERROR! :Mnemonic: Instruccion no existe 
17 0x64  TIXR T 
18 0x66  BYTE X'1234567' 
19 0x6a  END ENTRADA 
20 0x31f2  COMP TEMP 
21 0x31f5  RESB 1 
22 0x31f6  BYTE X'321' 
23 0x31f8  RSUB  
24 0x31fb  END  
