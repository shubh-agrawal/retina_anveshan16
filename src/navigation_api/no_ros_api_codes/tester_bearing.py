import math
from espeak import espeak 
def bearing_calculator(A,B): # A=(lat,lng) , B=(lat,lng) two orderes tuple
	"gives bearing angle when looking from A towards B"
	
	X=(math.cos(B[0]))*(math.sin(B[1]-A[1]))
	Y=(math.cos(A[0]))*(math.sin(B[0]))-(math.sin(A[0]))*(math.cos(B[0]))*(math.cos(B[1]-A[1]))
	
	beta=math.atan2(Y,X)*180/math.pi
	print beta

bearing_calculator((39.099912, -94.581213),(38.627089, -90.200203))