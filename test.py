import time
import re

t0 = time.time()
N = 4000

# tb = "AT"
# text = "AT0000A0GMD6"

tb = "C"
text = "CONWERT IMMO INVEST AG 2016 5,25"

for i in range(N):
    re.match("^" + tb + ".*", text)

print(time.time() - t0)
