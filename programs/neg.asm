	INP R2

	SW  R2, 0x81

	LI 	R3, 0xff
	SUB R3, R2

	SW  R3, 0x80

end:
    JMP end