
clef=dict()
etat=dict()

def lire_clef():
  for i in range(0,16):
    clef[i]=int(input('clef['+str(i)+'] ? '))%256

def initialiser_etat():
  for i in range(0,256):
    etat[i]=i

def melanger_etat():
  i=0
  j=0
  for i in range(0,256):
    j=(j+etat[i]+clef[i%16])%256
    t=etat[i]
    etat[i]=etat[j]
    etat[j]=t

def octet_suivant():
  global i
  global j
  i=(i+1)%256
  j=(j+etat[i])%256
  t=etat[i]
  etat[i]=etat[j]
  etat[j]=t
  t=(etat[i]+etat[j])%256
  return etat[t]

lire_clef()

initialiser_etat()

melanger_etat()

i=0
j=0

n=int(input('Nombre octets ? '))

for k in range(0,n):
  print(octet_suivant())

