
# ======================================
# 1. 관계 행렬 입력 기능 
# 사용자로부터 5 x 5 크기의 정방행렬을 행 단위로 입력받음
# 입력 데이터는 리스트(2차원 배열)로 저장.
# ======================================
def inputMatrix():
    print("5 x 5 정방행렬을 입력하세요(각 원소를 공백으로 구분하여 한 행씩 입력해주세요.): ")
    matrix_a = []
    for i in range(5):
      row_input = input(f"{i+1}행: ").strip()
      row_values = [int(x) for x in row_input.split()]
      matrix_a.append(row_values)

    return matrix_a

# ======================================
# 2. 동치 관계 판별 기능
# 반사, 대칭, 추이관계 각각 판별
# 관계의 성질 판별 결과에 따라 동치 관계 여부에 대한 메시지 출력
# ======================================
# 반사 관계 판단 함수
def is_reflexive(matrix):
    for i in range(len(matrix)):
        if matrix[i][i] != 1:
            return False
    return True

# 대칭 관계 판단 함수
def is_symmetric(matrix):
    for i in range(len(matrix)):
        for j in range(len(matrix)):
            # (i, j)와 (j, i)가 다르면 대칭이 아님
            if matrix[i][j] != matrix[j][i]:
                return False
    return True

# 관계행렬 부울곱 함수
def matrix_mult(A, B):
    size = len(A)
    result = [[0] * size for _ in range(size)]
    for i in range(size):
        for j in range(size):
            for k in range(size):
                result[i][j] |= A[i][k] & B[k][j]
    return result

# 추이 관계 판단 함수
def is_transitive(matrix):
    size = len(matrix)
    power = [row[:] for row in matrix]
    combined = [row[:] for row in matrix]

    for _ in range(1, size):
        power = matrix_mult(power, matrix)
        for i in range(size):
            for j in range(size):
                combined[i][j] |= power[i][j]
    return combined == matrix

# 동치 관계 여부 판별 함수
def is_equivalence_relation(matrix):
    return (
        is_reflexive(matrix) and
        is_symmetric(matrix) and
        is_transitive(matrix)
    )

# ======================================
# 3. 동치 관계일 경우 동치류의 출력 기능
# 집합의 원소에 대해 동치류를 판별하는 함수 구현
# 집합의 각 원소에 대해 동치류를 각각 출력
# ======================================
def print_equivalence_classes(matrix):
    # 동치 관계 확인
    if not is_equivalence_relation(matrix):
        print("이 관계는 동치 관계가 아닙니다.")
        return

    size = len(matrix)
    print("이 관계는 동치 관계입니다.")
    print("각 원소에 대한 동치류는 다음과 같습니다:")

    for i in range(size):
        eq_class = []
        for j in range(size):
            if matrix[i][j] == 1:     # i와 j가 관계 R에 있음
                eq_class.append(j + 1)  # 원소 번호는 1부터라 +1

        print(f"원소 {i+1}의 동치류: {eq_class}")

# ======================================
# 4. 폐포 구현 기능
# 입력받은 관계가 반사，대칭，추이 관계가 아닐 경우 각각의 폐포로 만드는 함수를 구현
# 각각의 관계에 한 폐포 변환 전，변환 후를 출력
# 각각의 폐포로 변환한 후 동치 관계를 다시 판별하고 동치류 출력하기
# ======================================
# 반사 폐포
def reflexive_closure(matrix):
    size = len(matrix)
    R = [row[:] for row in matrix]
    for i in range(size):
        R[i][i] = 1
    return R

# 대칭 폐포
def symmetric_closure(matrix):
    size = len(matrix)
    R = [row[:] for row in matrix]
    for i in range(size):
        for j in range(size):
            if R[i][j] == 1:
                R[j][i] = 1
    return R

# 추이 폐포(Warshall 알고리즘)
def transitive_closure(matrix):
    size = len(matrix)
    R = [row[:] for row in matrix]

    for k in range(size):
        for i in range(size):
            for j in range(size):
                if R[i][k] == 1 and R[k][j] == 1:
                    R[i][j] = 1
    return R


# ======================================
# main함수
# ======================================
# 행렬 출력 보조 함수
def print_matrix(matrix):
    for row in matrix:
        print(" ".join(str(int(x)) for x in row))

# 행렬을 파일에 출력하는 함수
def print_matrix_to_file(matrix, file):
    for row in matrix:
        print(" ".join(str(x) for x in row), file=file)

# 동치류를 파일에 출력하는 함수
def print_equivalence_classes_to_file(matrix, file):
    if not is_equivalence_relation(matrix):
        print("이 관계는 동치 관계가 아닙니다.", file=file)
        return

    size = len(matrix)
    print("이 관계는 동치 관계입니다.", file=file)
    print("각 원소에 대한 동치류는 다음과 같습니다:", file=file)

    for i in range(size):
        eq_class = []
        for j in range(size):
            if matrix[i][j] == 1:
                eq_class.append(j + 1)
        print(f"원소 {i+1}의 동치류: {eq_class}", file=file)


def main():
    # 1. 관계 행렬 입력
    matrix = inputMatrix()

    # 입력을 int로 강제 변환
    size = len(matrix)
    for i in range(size):
        for j in range(size):
            matrix[i][j] = int(matrix[i][j])

    # 파일 열기
    filename = "relation_report.txt"
    with open(filename, "w", encoding="utf-8") as f:

        print("=== 입력된 관계 행렬 ===", file=f)
        print_matrix_to_file(matrix, f)
        print(file=f)

        # 관계의 성질 판별
        r = is_reflexive(matrix)
        s = is_symmetric(matrix)
        t = is_transitive(matrix)

        print("=== 관계의 성질 판별 결과 ===", file=f)
        print(f"반사 관계인가? {'예' if r else '아니오'}", file=f)
        print(f"대칭 관계인가? {'예' if s else '아니오'}", file=f)
        print(f"추이 관계인가? {'예' if t else '아니오'}", file=f)

        if is_equivalence_relation(matrix):
            print("→ 이 관계는 동치 관계입니다.\n", file=f)
        else:
            print("→ 이 관계는 동치 관계가 아닙니다.\n", file=f)

        # 원래 관계의 동치류 출력
        print("=== 원래 관계에 대한 동치류 출력 ===", file=f)
        print_equivalence_classes_to_file(matrix, f)
        print(file=f)

        # 1) 반사 폐포
        print("=== 반사 폐포(reflexive closure) ===", file=f)
        if not r:
            print("[반사 폐포 변환 전]", file=f)
            print_matrix_to_file(matrix, f)

            r_closure = reflexive_closure(matrix)

            print("[반사 폐포 변환 후]", file=f)
            print_matrix_to_file(r_closure, f)
            print(file=f)

            print("반사 폐포 후 동치 관계 및 동치류 판별:", file=f)
            print_equivalence_classes_to_file(r_closure, f)
        else:
            print("이미 반사 관계이므로 반사 폐포는 원래 행렬과 동일합니다.", file=f)
            print("반사 폐포 후 동치 관계 및 동치류 판별:", file=f)
            print_equivalence_classes_to_file(matrix, f)
        print(file=f)

        # 2) 대칭 폐포
        print("=== 대칭 폐포(symmetric closure) ===", file=f)
        if not s:
            print("[대칭 폐포 변환 전]", file=f)
            print_matrix_to_file(matrix, f)

            s_closure = symmetric_closure(matrix)

            print("[대칭 폐포 변환 후]", file=f)
            print_matrix_to_file(s_closure, f)
            print(file=f)

            print("대칭 폐포 후 동치 관계 및 동치류 판별:", file=f)
            print_equivalence_classes_to_file(s_closure, f)
        else:
            print("이미 대칭 관계이므로 대칭 폐포는 원래 행렬과 동일합니다.", file=f)
            print("대칭 폐포 후 동치 관계 및 동치류 판별:", file=f)
            print_equivalence_classes_to_file(matrix, f)
        print(file=f)

        # 3) 추이 폐포
        print("=== 추이 폐포(transitive closure, Warshall 알고리즘) ===", file=f)
        if not t:
            print("[추이 폐포 변환 전]", file=f)
            print_matrix_to_file(matrix, f)

            t_closure = transitive_closure(matrix)

            print("[추이 폐포 변환 후]", file=f)
            print_matrix_to_file(t_closure, f)
            print(file=f)

            print("추이 폐포 후 동치 관계 및 동치류 판별:", file=f)
            print_equivalence_classes_to_file(t_closure, f)
        else:
            print("이미 추이 관계이므로 추이 폐포는 원래 행렬과 동일합니다.", file=f)
            print("추이 폐포 후 동치 관계 및 동치류 판별:", file=f)
            print_equivalence_classes_to_file(matrix, f)
        print(file=f)

    print(f'결과가 "{filename}" 파일로 저장되었습니다.')

if __name__ == "__main__":
    main()