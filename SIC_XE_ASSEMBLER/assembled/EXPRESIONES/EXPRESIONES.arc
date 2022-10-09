0 0x0 EXPRESIONES START 0H  
1 0x0 TABLA RESW 3  
2 0x9 NUM EQU 19 !ERROR!,:Mnemonic:,Instruccion no existe 
3 0x9 ETIQ CLEAR X  
4 0xb TAM EQU * !ERROR!,:Mnemonic:,Instruccion no existe 
5 0xb  TIX NUM  
6 0xe  LDA #(ETIQ-TABLA+3) !ERROR!, :Sintaxis:, El operando no coincide con algun token valido 
7 0xe SALTO JLT ETIQ  
8 0x11  LDT COUNT+4 !ERROR!, :Sintaxis:, El operando no coincide con algun token valido 
9 0x11 COUNT WORD ETIQ-(TAM-TABLA) !ERROR!,:Sintaxis:,Operando invalido para BASE 
10 0x11  WORD 2*(SALTO-TAM)  
11 0x14  END SALTO  
