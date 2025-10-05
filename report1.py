import math
import csv

# ======================================
# 행렬을 입력받는 함수
# matrix.a라는 배열에 저장된다.
# ======================================
def inputMatrix():
    print("n x n 크기의 정방행렬을 입력받습니다.")
    n = int(input("정방행렬의 차수를 입력하세요: "))
    if n <= 0:
        print("차수는 양의 정수여야 합니다.")
        return
    print(f"{n} x {n} 정방행렬을 입력하세요(각 원소를 공백으로 구분하여 한 행씩 입력해주세요.): ")
    matrix_a = []
    for i in range(n):
      row_input = input(f"{i+1}행: ").strip()
      row_values = [float(x) for x in row_input.split()]
      matrix_a.append(row_values)

    return matrix_a
# ======================================
# 행렬식을 이용한 역행렬 계산 기능
# ======================================

# 전치 행렬 구하기
def transposeMatrix(m):
    return [[m[j][i] for j in range(len(m))] for i in range(len(m[0]))]

# 소행렬 구하기
def getMatrixMinor(m, i, j):
    return [row[:j] + row[j+1:] for row in (m[:i] + m[i+1:])]

# 행렬식 계산
def getMatrixDeterminant(m):
    if len(m) == 1:
        return m[0][0]
    if len(m) == 2:
        return m[0][0]* m[1][1] - m[0][1] * m[1][0]

    determinant = 0
    for c in range(len(m)):
        determinant += ((-1) ** c) * m[0][c] * getMatrixDeterminant(getMatrixMinor(m, 0, c))
    return determinant

# 역행렬이 존재하는지 확인 det(A) = 0 일 때 역행렬은 존재하지 않는다.
def has_inverse(m):
    determinant = getMatrixDeterminant(m)
    if abs(determinant) < 1e-10: # 부동소수점 오차 고려 / 참고: abs()는 숫자의 절댓값을 구하는 내장 함수
        print("오류! 해당 행렬의 행렬식은 0입니다.")
        print("역행렬 계산은 불가능합니다!")
        return False
    return True

# 역행렬 계산
def getMatrixInverse(m):
    determinant = getMatrixDeterminant(m)

    if len(m) == 1:
        return [[1.0/m[0][0]]]

    if len(m) == 2:
        return [[m[1][1] / determinant, -1 * m[0][1] / determinant],
                [-1 * m[1][0] / determinant, m[0][0] / determinant]]

    cofactors = []
    for r in range(len(m)):
        cofactorRow = []
        for c in range(len(m)):
            minor = getMatrixMinor(m, r, c)
            cofactorRow.append(((-1) ** (r + c)) * getMatrixDeterminant(minor))
        cofactors.append(cofactorRow)
        
    adjugate = transposeMatrix(cofactors)

    for r in range(len(adjugate)):
        for c in range(len(adjugate)):
            adjugate[r][c] = adjugate[r][c] / determinant

    return adjugate

# ======================================
# 가우스-조던 소거법을 이용한 역행렬 계산 기능
# ======================================

# 가우스-조던 소거법
def gaussJordanElimination(A, eps=1e-12):
    n = len(A)
    if any(len(row) != n for row in A):
        raise ValueError("정방행렬이 아닙니다.")

    # 단위행렬 생성
    I = [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]
    # 원본 훼손 방지용 복사
    A = [row[:] for row in A]

    for i in range(n):
        # --- 부분 피벗팅: 현재 열 i에서 절댓값이 가장 큰 행 찾기
        pivot_row = -1
        max_value = 0.0
        for r in range(i, n):
            if abs(A[r][i]) > max_value:
                max_value = abs(A[r][i])
                pivot_row = r

        # --- 피벗을 찾을 수 없는 경우 (열 전체가 0)
        if pivot_row == -1:
            raise ValueError(f"역행렬이 존재하지 않습니다. (열 {i}의 모든 값이 0)")

        # --- 피벗이 너무 작거나 0에 가까운 경우
        if abs(A[pivot_row][i]) < eps:
            raise ValueError(f"역행렬이 존재하지 않습니다. (피벗이 0 또는 너무 작음, 열 {i})")

        # --- 피벗 행을 현재 행(i행)으로 스왑
        if pivot_row != i:
            A[i], A[pivot_row] = A[pivot_row], A[i]
            I[i], I[pivot_row] = I[pivot_row], I[i]

        # --- 피벗을 1로 만들기
        pivot = A[i][i]
        for c in range(n):
            A[i][c] /= pivot
            I[i][c] /= pivot

        # --- 같은 열의 다른 행을 0으로 만들기
        for r in range(n):
            if r == i:
                continue
            factor = A[r][i]
            if abs(factor) > 0.0:
                for c in range(n):
                    A[r][c] -= factor * A[i][c]
                    I[r][c] -= factor * I[i][c]

    # 결과적으로 A는 단위행렬, I는 A^-1
    return I

# ======================================
# 행렬식 이용한 역행렬과 가우스-조던 소거법으로 구한 역행렬의 값을 비교
# ======================================
def matrixCompare(a, b):
    for i in range(len(a)):
        for j in range(len(a)):
            if a[i][j] == b[i][j]:
                continue
            else: 
                print(f"두 행렬의 {i+1}행 {j+1}열이 같지 않습니다." )
    print("======================결과출력==========================")
    print("행렬식으로 구한 역행렬과 가우스-조던 소거법으로 구한 역행렬은 같습니다.")

# ======================================
# 유틸리티
# ======================================
# 행렬을 예쁘게 출력
def matrixout(mx):
    n = len(mx)
    if n == 0:
        print("[빈 행렬]")
        return

    # 각 원소를 문자열로 변환해 최대 폭 계산
    str_matrix = [[f"{val:.4g}" for val in row] for row in mx]  # 최대 4자리 유효숫자
    col_widths = [max(len(row[j]) for row in str_matrix) for j in range(n)]

    # 전체 폭 계산 (열 간 간격 + 테두리 여백)
    total_width = sum(col_widths) + 3 * n

    # 윗부분
    print("┌" + " " * total_width + "┐")

    # 각 행 출력
    for i in range(n):
        print(end = "    ")
        for j in range(n):
            cell = str_matrix[i][j].rjust(col_widths[j])
            print(cell, end="  ")
        print()
    # 아랫부분
    print("└" + " " * total_width + "┘")

# 반올림 함수
def roundMatrix(M, digits=1):
    return [[round(val, digits) for val in row] for row in M]


# ======================================
# 추가기능 - 행렬 결과를 csv 파일로 저장.
# ======================================
def save_matrix_csv(M, path):
    with open(path, "w", newline="") as f:
        w = csv.writer(f)
        for row in M:
            w.writerow(row)

def load_matrix_csv(path):
    with open(path, newline="") as f:
        r = csv.reader(f)
        A = [[float(x) for x in row] for row in r]
    # 정방 체크
    if any(len(row)!=len(A) for row in A):
        raise ValueError("CSV가 정방행렬이 아닙니다.")
    return A


# ======================================
# 결과출력
# ======================================
if __name__ == "__main__":
    try:
        a = inputMatrix()
        # 1) 행렬식(여인수) 방식
        if has_inverse(a):
            print("\n[여인수/행렬식 방식] 역행렬:")
            inverse = getMatrixInverse(a)
            inverse = roundMatrix(inverse, digits=1)
            matrixout(inverse)
        else:
            print("\n[여인수/행렬식 방식] 역행렬이 존재하지 않습니다.")

        # 2) 가우스-조던 방식
        try:
            gj_inverse = gaussJordanElimination(a)
            print("\n[가우스-조던 방식] 역행렬:")
            gj_inverse = roundMatrix(gj_inverse, digits=1)
            matrixout(gj_inverse)
        except ValueError as e:
            print("\n[가우스-조던 방식] 오류:", e)
        
        # 3) 여인수 전개와 가우스-조던 방식의 역행렬을 비교
        matrixCompare(inverse, gj_inverse)

        # 4) 결과 csv 파일로 저장
        print()
        savefile = int(input(">>> 파일을 저장하려면 1, 저장하지 않으려면 0을 눌러주세요.:  "))
        if savefile == 1:
            save_matrix_csv(inverse, "inverse_result.csv")
            save_matrix_csv(gj_inverse, "gj-inverse_result.csv")
            print(">>> csv 파일이 프로젝트 폴더에 저장되었습니다.")

    except Exception as e:
        print("\n[예기치 못한 오류]", e)
