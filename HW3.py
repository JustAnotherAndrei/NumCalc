import numpy as np
from scipy.linalg import qr, solve_triangular, inv


def solve_qr_householder():
    # 6. Inițializare date (n, eps și random)
    n = 4  # Dimensiunea n a sistemului
    eps = 1e-10
    A_init = np.random.rand(n, n)
    s = np.random.rand(n)

    # 1. Calculăm vectorul b = A * s
    # b_i = suma(s_j * a_ij)
    b_init = np.zeros(n)
    for i in range(n):
        for j in range(n):
            b_init[i] += A_init[i, j] * s[j]# inmultire matrice-vector. daca obtinem un x prea diferit de s => alg are o eroare

    # --- CERINȚA 2: Descompunerea QR (Householder) ---
    A = A_init.copy()
    b = b_init.copy()
    U_vectors = []  # Pentru a stoca vectorii Householder
    beta_values = []

    # Algoritmul Householder pentru a aduce A la forma R (superior triunghiulară)
    # și a transforma simultan vectorul b (Q^T * b)
    for r in range(n - 1):
        # Calculăm sigma = suma(a_ir^2) pentru i de la r la n-1
        sigma = np.sum(A[r:, r] ** 2) # patratul normei coloanei curente (gen de la diagonala in jos)

        if sigma <= eps:
            break

        k = np.sqrt(sigma) # k - norma coloanei, dar ii schimbam semnul pentru a evita "anularea catastrofica" (scaderea a doua nr foarte apropiate care ar duce la pierderea preciziei)
        if A[r, r] > 0:
            k = -k

        beta = sigma - k * A[r, r] # scalar de normalizare ( 1/2 * ||u|| ^2) care ajuta sa aplicam reflexia fara sa calculam radicali inutili
        # Vectorul u_r
        u = np.zeros(n)
        u[r] = A[r, r] - k # Vectorul Householder. El defineste directia perpendiculara pe "oglinda" de relfexie
        u[r + 1:] = A[r + 1:, r]

        # Transformăm coloanele j = r+1...n-1 ale matricii A
        for j in range(r + 1, n):
            gamma = np.dot(u[r:], A[r:, j]) / beta # proiectia coloanei j pe vectorul u
            A[r:, j] -= gamma * u[r:] # aceasta linie scade proiectia, realizand reflexia coloanei. Practic, transformam coloana j fara sa atingem elementele deasupra randului curent r

        # tranformam vectorul b: b = (I - (u*u^T)/beta) * b
        gamma_b = np.dot(u[r:], b[r:]) / beta
        b[r:] -= gamma_b * u[r:]

        # Punem 0 sub diagonală și k pe diagonală (matricea R)
        A[r, r] = k
        A[r + 1:, r] = 0

        # Salvăm u și beta pentru calculul inversei mai târziu
        U_vectors.append(u)
        beta_values.append(beta)

    # Matricea R este acum stocată în A
    R = A

    # --- CERINȚA 3: Rezolvare sistem ---
    # a) Soluția x_QR din bibliotecă
    Q_bib, R_bib = qr(A_init)
    x_qr = inv(R_bib) @ Q_bib.T @ b_init

    # b) Soluția x_Householder (Substituție inversă: R * x = Q^T * b)
    # Q^T * b este deja stocat în variabila 'b' în urma transformărilor
    x_householder = solve_triangular(R, b) # deoarece R este superior triunghiulara, sistemul se rezolva de jos in sus

    # Afișare norma diferenței soluțiilor
    norm_diff_sol = np.linalg.norm(x_qr - x_householder, 2)
    print(f"||x_QR - x_Householder||: {norm_diff_sol:.12e}")

    # --- CERINȚA 4: Verificare erori ---
    # Calcul manual A_init * x pentru a respecta cerința de a nu folosi biblioteci în verificări
    def mat_vec_mult(Mat, vec):
        res = np.zeros(len(vec))
        for i in range(len(vec)):
            for j in range(len(vec)):
                res[i] += Mat[i, j] * vec[j]
        return res

    Ax_house = mat_vec_mult(A_init, x_householder)
    Ax_qr = mat_vec_mult(A_init, x_qr)

    err1 = np.linalg.norm(Ax_house - b_init, 2)
    err2 = np.linalg.norm(Ax_qr - b_init, 2)
    err3 = np.linalg.norm(x_householder - s, 2) / np.linalg.norm(s, 2) # impartim diferenta la norma lui s. aceasta ne spune procentual cat de mult am gresit.
                                                                                # Daca s e un vector cu valori uriase, o eroare de 0.001 e neglijabila; daca s are valori mici, aceeasi eroare e grava
    err4 = np.linalg.norm(x_qr - s, 2) / np.linalg.norm(s, 2)

    print(f"\nErori de precizie:")
    print(f"||A_init * x_Householder - b_init||: {err1:.12e}") # diferenta dintre metode
    print(f"||A_init * x_QR - b_init||: {err2:.12e}") # reziduul sistemului
    print(f"||x_Householder - s|| / ||s||: {err3:.12e}") # eroarea relativa fata de solutia dorita
    print(f"||x_QR - s|| / ||s||: {err4:.12e}")

    # --- CERINȚA 5: Inversa ---
    # Pentru a calcula inversa, rezolvăm Ax = e_j pentru fiecare coloană a matricii identitate
    A_inv_house = np.zeros((n, n))
    for j in range(n):
        # Vectorul unitar e_j
        e_j = np.zeros(n)
        e_j[j] = 1.0

        # Aplicăm transformările Householder (Q^T) asupra lui e_j (i.e. calculam inversa coloana cu coloana)
        for r in range(n - 1): # pt a gasi coloana j a inversei, trebuie sa rezolvam A*x=e_j. Dar noi am transformat deja A in R  prin Q^t.
                                # Deci trebuie sa aplicam aceleasi tranformari Q^t si vectorului unitar e_j inainte de a face substitutia inversa cu R
            u = U_vectors[r]
            beta = beta_values[r]
            gamma_e = np.dot(u[r:], e_j[r:]) / beta
            e_j[r:] -= gamma_e * u[r:]

        # Rezolvăm R * col_j = Q^T * e_j
        column_inv = solve_triangular(R, e_j)
        A_inv_house[:, j] = column_inv

    A_inv_bib = inv(A_init)
    norm_inv = np.linalg.norm(A_inv_house - A_inv_bib, 2)
    print(f"\nNorma diferenței inverselor: {norm_inv:.12e}")


solve_qr_householder()