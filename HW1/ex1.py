m = 0
u = 1.0

# cautam cel mai mic m pentru care 1 + 10^-m != 1
while (1.0 + (u / 10.0)) != 1.0:
    u /= 10.0
    m += 1

print(f"Valoarea m găsită: {m}")
print(f"Precizia mașină u (10^-{m}): {u}")
print(f"Verificare 1.0 + u: {1.0 + u}")
print(f"Verificare 1.0 + u/10: {1.0 + (u/10.0)}")