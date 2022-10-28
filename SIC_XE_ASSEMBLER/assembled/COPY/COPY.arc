0 0x0 COPY START 1000  
1 0x0 FIRST STL RETDR  
2 0x3 CLOOP JSUB RDREC  
3 0x6  LDA LENGTH  
4 0x9  COMP #0  
5 0xc  LDA LENGTH  
6 0xf  USE CDATA !ERROR!,:Mnemonic:,Instruccion no existe 
7 0xf RETADR RESW 1  
8 0x12 LENGTH RESW 1  
9 0x15  USE CBLKS !ERROR!,:Mnemonic:,Instruccion no existe 
10 0x15 BUFFER RESB 4096  
11 0x1015 BUFFEND EQU * !ERROR!,:Mnemonic:,Instruccion no existe 
12 0x1015 MAXLEN EQU BUFFER !ERROR!,:Mnemonic:,Instruccion no existe 
13 0x1015  USE  !ERROR!,:Mnemonic:,Instruccion no existe 
14 0x1015 RDREC CLEAR X  
15 0x1017  +LDT #MAXLEN  
16 0x101b  USE CDATA !ERROR!,:Mnemonic:,Instruccion no existe 
17 0x101b INPUT BYTE X'F1'  
18 0x101c  USE  !ERROR!,:Mnemonic:,Instruccion no existe 
19 0x101c  LDT LENGTH  
20 0x101f  END FIRST  
