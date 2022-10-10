0 0x0 EJERCFINAL START 0H ---- ----
1 0x0  SIO  0xF0 0xF0
2 0x1  +LDX @TABLA 0x6100008* 0x6100008*
3 0x5 VALOR WORD 140 00008C 00008C
4 0x8  BASE CAD ---- ----
5 0x8 TABLA RESW 20 ---- ----
6 0x44  +LDS VALOR,X 0x6f900005* 0x6f900005*
7 0x48  SHIFTL S,6 0xa445 0xa445
8 0x4a SIMBOLO LDD #VALOR !ERROR!,:Mnemonic:,Instruccion no existe 
9 0x4a  +LDA 1010H,X 0x3901010 0x3901010
10 0x4e CAD BYTE C'FINAL' 3046494e414c 3046494e414c
11 0x53  LDA #TABLA 0x12fb2 0x12fb2
12 0x56  SUBR S,X 0x9441 0x9441
13 0x58  RESW 2500H ---- ----
14 0x6f58 SALTO ADD VALOR,X 0x1befff: Instruccion No es relativa ni a (CP) ni a (B) 0x1befff: Instruccion No es relativa ni a (CP) ni a (B)
15 0x6f5b  STCH @TABLA 0x566fff: Instruccion No es relativa ni a (CP) ni a (B) 0x566fff: Instruccion No es relativa ni a (CP) ni a (B)
16 0x6f5e  JGT SALTO,X 0x37aff7 0x37aff7
17 0x6f61 AREA RESB 64 ---- ----
18 0x6fa1  STA SALTO 0xf2fb4 0xf2fb4
19 0x6fa4  +SUB 350 0x1f7fffff: Modo de direccionamiento no existe, constante fuera de rango 0x1f7fffff: Modo de direccionamiento no existe, constante fuera de rango
20 0x6fa8  J CADENA,X 0x3fefff: simbolo no encontrado en la tabla de simbolos 0x3fefff: simbolo no encontrado en la tabla de simbolos
21 0x6fab  +TIX TABLA,X 0x2f900008* 0x2f900008*
22 0x6faf  END INICIO ---- ----
