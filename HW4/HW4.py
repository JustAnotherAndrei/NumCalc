import numpy as np
import os


def rezolva_gauss_seidel_final():
    for idx in range(1, 6):
        print(f"\n" + "=" * 40)
        print(f" PROCESARE SETUL {idx}")
        print("=" * 40)

        try:
            # Citire directă a valorilor (fără a presupune că prima linie e dimensiunea)
            d0 = np.loadtxt(f"d0_{idx}.txt").flatten()
            d1 = np.loadtxt(f"d1_{idx}.txt").flatten()
            d2 = np.loadtxt(f"d2_{idx}.txt").flatten()
            b = np.loadtxt(f"b_{idx}.txt").flatten()

            n = len(d0)
            p = n - len(d1)
            q = n - len(d2)

            print(f"Date detectate: n={n}, p={p}, q={q}")

            if np.any(np.abs(d0) < 1e-15):
                print("Eroare: Diagonala d0 are elemente nule.")
                continue

            # --- Metoda Gauss-Seidel ---
            x = np.zeros(n)
            eps = 1e-10
            max_iter = 5000

            for k in range(max_iter):
                x_old = x.copy()
                for i in range(n):
                    suma = 0
                    # Diagonalele p
                    if i - p >= 0: suma += d1[i - p] * x[i - p]
                    if i + p < n:  suma += d1[i] * x[i + p]
                    # Diagonalele q
                    if i - q >= 0: suma += d2[i - q] * x[i - q]
                    if i + q < n:  suma += d2[i] * x[i + q]

                    # Actualizare In-Place
                    x[i] = (b[i] - suma) / d0[i]

                # Verificare stabilitate (prevenire Overflow)
                if np.any(np.isnan(x)) or np.any(np.isinf(x)):
                    print(f"Sistemul {idx} este DIVERGENT (numere prea mari).")
                    break

                #    if np.max(np.abs(x - x_old)) > 10^300:
                    print(f"Divergenta atinsă în {k + 1} iterații.")
                    print(np.max(np.abs(x - x_old)))
                    break

                if np.max(np.abs(x - x_old)) > 10^10:
                    print(f"Div atinsă în {k + 1} iterații.")
                    break


                if np.max(np.abs(x - x_old)) < eps:
                    print(f"Convergență atinsă în {k + 1} iterații.")
                    break
            else:
                if not (np.any(np.isnan(x)) or np.any(np.isinf(x))):
                    print("Limita de iterații atinsă.")


            # --- Calcul Reziduu (y = Ax) ---
            y = np.zeros(n)
            for i in range(n):
                val_y = d0[i] * x[i]
                if i - p >= 0: val_y += d1[i - p] * x[i - p]
                if i + p < n:  val_y += d1[i] * x[i + p]
                if i - q >= 0: val_y += d2[i - q] * x[i - q]
                if i + q < n:  val_y += d2[i] * x[i + q]
                y[i] = val_y

            norma = np.max(np.abs(y - b))
            print(f"Norma finală ||Ax - b||_inf: {norma:.2e}")

        except Exception as e:
            print(f"Eroare la setul {idx}: {e}")


if __name__ == "__main__":
    rezolva_gauss_seidel_final()