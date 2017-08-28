#!/bin/python2

from decimal import *

def readModulo(filename):
    modFile = open(filename, "r")
    modStr = modFile.read()
    return int(modStr, 16)

def readCipher(filename):
    cipStr = open(filename, "rb").read()
    cip = 0
    for byte in range(0, len(cipStr)):
        cip = (cip << 8) + ord(cipStr[byte])
    return cip

def chinese_remainder(n, a):
    sum = 0
    prod = reduce(lambda a, b: a*b, n)

    for n_i, a_i in zip(n, a):
        p = prod / n_i
        sum += a_i * mul_inv(p, n_i) * p
    return sum % prod

def mul_inv(a, b):
    b0 = b
    x0, x1 = 0, 1
    if b == 1: return 1
    while a > 1:
        q = a / b
        a, b = b, a%b
        x0, x1 = x1 - q * x0, x0
    if x1 < 0: x1 += b0
    return x1

print("Reading moduli...")
moduli = [1001191535967882284769094654562963158339094991366537360172618359025855097846977704928598237040115495676223744383629803332394884046043603063054821999994629411352862317941517957323746992871914047324555019615398720677218748535278252779545622933662625193622517947605928420931496443792865516592262228294965047903627, 405864605704280029572517043538873770190562953923346989456102827133294619540434679181357855400199671537151039095796094162418263148474324455458511633891792967156338297585653540910958574924436510557629146762715107527852413979916669819333765187674010542434580990241759130158992365304284892615408513239024879592309, 1204664380009414697639782865058772653140636684336678901863196025928054706723976869222235722439176825580211657044153004521482757717615318907205106770256270292154250168657084197056536811063984234635803887040926920542363612936352393496049379544437329226857538524494283148837536712608224655107228808472106636903723]
print("Reading ciphertexts...")
ciphers = [261345950255088824199206969589297492768083568554363001807292202086148198540785875067889853750126065910869378059825972054500409296763768604135988881188967875126819737816598484392562403375391722914907856816865871091726511596620751615512183772327351299941365151995536802718357319233050365556244882929796558270337, 147535246350781145803699087910221608128508531245679654307942476916759248311896958780799558399204686458919290159543753966699893006016413718139713809296129796521671806205375133127498854375392596658549807278970596547851946732056260825231169253750741639904613590541946015782167836188510987545893121474698400398826, 633230627388596886579908367739501184580838393691617645602928172655297372145912724695988151441728614868603479196153916968285656992175356066846340327304330216410957123875304589208458268694616526607064173015876523386638026821701609498528415875970074497028482884675279736968611005756588082906398954547838170886958]

print("Calculating plaintext^e by using the chinese remainder theorem...")
plainPowE = chinese_remainder(moduli, ciphers)

print("Calculating plaintext...")
e = 3
getcontext().prec = 4000
plain = plainPowE**(Decimal(1)/Decimal(e))

# Round to int
plain = plain.quantize(Decimal(1), rounding=ROUND_HALF_EVEN)
plain = int(plain)

# Convert to ASCII-encoded chars
plainStr = ""
while (plain > 0):
    plainStr = chr(plain & 0xFF) + plainStr
    plain = plain >> 8

print("Decrypted plaintext:")
print(plainStr)
