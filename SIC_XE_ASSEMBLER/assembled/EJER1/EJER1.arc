0 0x0 EJER1 START 0  
1 0x0  LDX #5  
2 0x3  HIO   
3 0x4  +LDB #TABLE2  
4 0x8  STA @COUNT  
5 0xb  CLEAR A  
6 0xd  BASE TABLE2  
7 0xd  ADDR X,A  
8 0xf LOOP ADD TABLE,X  
9 0x12  +STA TOTAL  
10 0x16  RSUB   
11 0x19 COUNT RESB 12H  
12 0x2b  SHIFTL X,2  
13 0x2d TABLE RESW 10  
14 0x4b TABLE2 BYTE C'TEST'  
15 0x4f  WORD 16  
16 0x52  END   
