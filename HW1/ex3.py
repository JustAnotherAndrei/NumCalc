import math
import time
import random


def my_tan_fraction(x, epsilon):
    # Tratăm periodicitatea: aducem x în (-pi/2, pi/2)
    x_reduced = x % math.pi
    if x_reduced > math.pi / 2:
        x_reduced -= math.pi

    # Verificăm asimptotele (multiplu de pi/2)
    if math.isclose(abs(x_reduced), math.pi / 2, rel_tol=1e-15):
        return float('inf')

    if x_reduced == 0:
        return 0.0

    mic = 1e-12

    # Parametrii inițiali conform algoritmului Lentz pentru tan(x)
    # b0 = 0
    f = mic  # deoarece f0 = b0 și dacă f0=0 atunci f0=mic
    C = f
    D = 0
    j = 1

    while True:
        # Definirea coeficienților aj și bj pentru tan(x)
        if j == 1:
            aj = x_reduced
            bj = 1.0
        else:
            aj = -(x_reduced ** 2)
            bj = 2.0 * j - 1.0

        # Recurența pentru D
        D = bj + aj * D
        if D == 0: D = mic

        # Recurența pentru C
        C = bj + aj / C
        if C == 0: C = mic

        D = 1.0 / D
        delta = C * D
        f = delta * f

        if abs(delta - 1.0) < epsilon:
            break
        j += 1
        if j > 2000: break  # Limită de siguranță

    return f


def my_tan_poly(x):
    # 1. Reducere la (-pi/2, pi/2)
    x = x % math.pi
    if x > math.pi / 2:
        x -= math.pi

    if math.isclose(abs(x), math.pi / 2, rel_tol=1e-15):
        return float('inf')

    # 2. Gestionare antisimetrie
    semn = 1
    if x < 0:
        semn = -1
        x = -x

    # 3. Reducere la [0, pi/4] conform indicației: tan(x) = 1 / tan(pi/2 - x)
    inv = False
    if x > math.pi / 4:
        x = (math.pi / 2) - x
        inv = True

    # Coeficienți
    c1 = 0.33333333333333333
    c2 = 0.133333333333333333
    c3 = 0.053968253968254
    c4 = 0.0218694885361552

    x2 = x * x
    # tan(x) ≈ x + (1/3)x^3 + (2/15)x^5 + (17/315)x^7 + (62/2835)x^9
    # Optimizat: x + x^3 * (c1 + x^2*(c2 + x^2*(c3 + x^2*c4)))
    res = x + (x ** 3) * (c1 + x2 * (c2 + x2 * (c3 + x2 * c4)))

    if inv:
        res = 1.0 / res if res != 0 else float('inf')

    return semn * res


# --- Demonstrație și Comparație ---
def main():
    try:
        eps_input = float(input("Introdu precizia epsilon (ex. 1e-10): "))
    except ValueError:
        eps_input = 1e-10

    test_vals = [random.uniform(-math.pi / 2 + 0.1, math.pi / 2 - 0.1) for _ in range(10000)]

    # Măsurare Fracții Continue
    t0 = time.time()
    err_f = sum(abs(math.tan(v) - my_tan_fraction(v, eps_input)) for v in test_vals)
    t1 = time.time() - t0

    # Măsurare Polinom
    t0 = time.time()
    err_p = sum(abs(math.tan(v) - my_tan_poly(v)) for v in test_vals)
    t2 = time.time() - t0

    print(f"\nRezultate pentru 10.000 de valori:")
    print(f"{'Metoda':<20} | {'Eroare Totală':<15} | {'Timp (s)':<10}")
    print("+" * 67)
    print(f"{'Fracții Continue':<20} | {err_f:<15.2e} | {t1:<10.4f}")
    print(f"{'Polinomială':<20} | {err_p:<15.2e} | {t2:<10.4f}")


if __name__ == "__main__":
    main()