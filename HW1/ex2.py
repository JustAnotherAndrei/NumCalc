def demonstreaza_neasociativitatea():    # ---------------------------------------------------------
    # i. Pregătire: Determinarea preciziei mașină u
    # ---------------------------------------------------------
    u = 1.0
    while (1.0 + (u / 10.0)) != 1.0:
        u /= 10.0

    print(f"Precizia mașină determinată: u = {u}")
    print("-" * 50)

    # ---------------------------------------------------------
    # ii. Neasociativitatea ADUNĂRII (+c)
    # Cerința: x = 1.0, y = u/10, z = u/10
    # ---------------------------------------------------------
    x = 1.0
    y = u / 10.0
    z = u / 10.0

    # (x + y) + z
    # Deoarece 1.0 + u/10 = 1.0 (eroare de subflow relativ), rezultatul e 1.0
    suma_stanga = (x + y) + z

    # x + (y + z)
    # y + z se calculează întâi (u/10 + u/10 = 2u/10), apoi se adună la 1.0
    suma_dreapta = x + (y + z)

    print("NEASOCIATIVITATEA ADUNĂRII:")
    print(f" (x +c y) +c z = ({x} + {y}) + {z} = {suma_stanga}")
    print(f" x +c (y +c z) = {x} + ({y} + {z}) = {suma_dreapta}")
    print(f" Sunt diferite? {suma_stanga != suma_dreapta}")
    print("-" * 50)

    # ---------------------------------------------------------
    # iii. Neasociativitatea ÎNMULȚIRII (*c)
    # Folosim overflow pentru a forța neasociativitatea
    # ---------------------------------------------------------
    # x și y sunt numere mari care înmulțite depășesc 1.8e308 (Infinity)
    # z este un număr mic care ar trebui să "echilibreze" produsul
    a = 1e300
    b = 1e300
    c = 1e-300

    # (a * b) * c  -> (inf) * 1e-300 = inf
    prod_stanga = (a * b) * c

    # a * (b * c)  -> 1e300 * (1.0) = 1e300
    prod_dreapta = a * (b * c)

    print("NEASOCIATIVITATEA ÎNMULȚIRII:")
    print(f" (a *c b) *c c = ({a} * {b}) * {c} = {prod_stanga}")
    print(f" a *c (b *c c) = {a} * ({b} * {c}) = {prod_dreapta}")
    print(f" Sunt diferite? {prod_stanga != prod_dreapta}")


if __name__ == "__main__":
    demonstreaza_neasociativitatea()