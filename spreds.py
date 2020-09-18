from charm.toolbox.pairinggroup import PairingGroup,ZR,G1,G2,GT,pair,order

from charm.core.engine.util import objectToBytes, bytesToObject

Debug = False
class LHS :

	def __init__ (self,groupobj) :
		global group
		group = groupobj

	def KeyGen(self) :

		#Step 1
		alpha_h = group.random(ZR)

		g2 = group.random(G2)

		h2 = g2**(alpha_h)

		#Step 2
		xi = []
		sigma = []
		hp = []

		for i in range (0,2):
			xi_i = group.random(ZR)
			print(xi_i)
			sigma_i = group.random(ZR)
			hp_i = (g2**xi_i) * (h2**sigma_i)

			xi.append(xi_i)
			sigma.append(sigma_i)
			hp.append(hp_i)



		sk = {"xi" : xi , "sigma" : sigma , "h2" : h2}
		vk = {"h2" : h2 , "hp" : hp, "g2" : g2}

		return (sk,vk)

	def Sign (self,sk,M) :

		z = ((M[0] ** (sk["xi"][0])) * (M[1] ** (sk["xi"][1]) ))**(-1)

		u = ((M[0] ** (sk["sigma"][0])) * (M[1] ** (sk["sigma"][1]))) ** (-1)

		print("TEST : ", (M[0] ** sk["xi"][0]) * (M[1] ** sk["xi"][1]) * z)

		sig = {"z" : z, "u" : u}

		return sig

	def SignDerive(self,vk,coef_a,M1,sig1,coef_b,M2,sig2) :

		z = (sig1["z"] **coef_a) * (sig2["z"]**coef_b)

		u = (sig1["u"] **coef_a) * (sig2["u"] **coef_b)

		sig = {"z" : z, "u" : u}

		return sig


	def Verify(self,vk,M,sig) :

		res = pair(sig["z"],vk["g2"]) * pair(sig["u"],vk["h2"]) * pair(M[0],vk["hp"][0]) * pair(M[1],vk["hp"][1])
		#res = pair(M[0],vk["g2"]) * pair(M[0],vk["g2"]**(-1))

		a = group.random(ZR)

		print(res==res**a)
		print(res)


def main() :

	#=================MAIN===================#

	print("\n===================TEST===================\n")

	#Group Init
	group = PairingGroup('SS512')

	#Setup LHS
	lhs = LHS(group)

	#Setup
	sk,vk = lhs.KeyGen()

	#print("sk : ",sk)
	#print("vk : ",vk)

	M1 = []
	M1.append(group.random(G1))
	M1.append(group.random(G1))

	M2 = []
	M2.append(group.random(G1))
	M2.append(group.random(G1))

	sig1 = lhs.Sign(sk,M1)
	sig2 = lhs.Sign(sk,M2)

	lhs.Verify(vk,M1,sig1)
	lhs.Verify(vk,M2,sig2)


	coef_a = group.random()
	coef_b = group.random()

	sig3 = lhs.SignDerive(vk,coef_a,M1,sig1,coef_b,M2,sig2)

	M3 = []
	M3.append((M1[0]**coef_a) * (M2[0])**coef_b)
	M3.append((M1[1]**coef_a) * (M2[1])**coef_b)


	lhs.Verify(vk,M3,sig3)

if __name__ == "__main__" :
	Debug = True
	main()
