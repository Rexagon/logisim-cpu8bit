	LI 	R2, 0x04 	# number of iterations (4)

	LI  R0, 0x00 	# n-2 number
	LI 	R1, 0x01 	# n-1 number

	JNE R2, loop

loop:
	LI	R3, 0x01
	SUB R2, R3

	JEQ R2, end

	LI	R3, 0x00	# reset temp
	ADD R3, R0		# F(n) = F(n-2)
	ADD R3, R1		# 	   + F(n-1)

	MOV R0, R1		# F(n-2) -> F(n-1)
	MOV R1, R3		# F(n-1) -> F(n)

	SW	R3, 0x1b

	JNE R2, loop

end:
	JMP end