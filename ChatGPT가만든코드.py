# 1. 선언 및 중복 허용 여부 확인
print("=== 1. 선언 및 중복 데이터 처리 ===")
# 중복된 값(2)을 넣어 선언해 봅니다.
sample_list = [1, 2, 2, 3]
sample_tuple = (1, 2, 2, 3)
sample_set = {1, 2, 2, 3}  # 중복 허용 안 됨
sample_dict = {"a": 1, "b": 2, "b": 3}  # 중복된 키는 마지막 값으로 덮어써짐

print(f"List:   {sample_list} (중복 허용)")
print(f"Tuple:  {sample_tuple} (중복 허용)")
print(f"Set:    {sample_set} (중복 자동 제거)")
print(f"Dict:   {sample_dict} (동일한 Key는 덮어써짐)\n")


# 2. 순서(Indexing) 접근 가능 여부
print("=== 2. 인덱싱(Indexing) 접근 ===")
print(f"List[0]:  {sample_list[0]}")
print(f"Tuple[0]: {sample_tuple[0]}")
print(f"Dict['a']: {sample_dict['a']} (Key로 접근)")

# Set은 순서가 없으므로 인덱싱을 지원하지 않습니다.
try:
    print(sample_set[0])
except TypeError as e:
    print(f"Set[0] 접근 실패: {e} (Set은 인덱싱을 지원하지 않습니다.)\n")


# 3. 수정 가능 여부 (Mutability)
print("=== 3. 수정 가능 여부 (Mutability) ===")

# List는 수정 가능 (Mutable)
sample_list[0] = 99
print(f"List 수정 완료: {sample_list}")

# Dict는 수정 가능 (Mutable)
sample_dict["a"] = 99
print(f"Dict 수정 완료: {sample_dict}")

# Set은 요소 추가/삭제 가능 (Mutable)
sample_set.add(4)
sample_set.discard(1)
print(f"Set 수정(추가/삭제) 완료: {sample_set}")

# Tuple은 수정 불가능 (Immutable)
try:
    sample_tuple[0] = 99
except TypeError as e:
    print(f"Tuple 수정 실패: {e} (Tuple은 생성 후 수정할 수 없습니다.)\n")


# 4. 멤버십 테스트 (원소 포함 여부 검사 속도)
# Set과 Dict(Key 검사)는 해시 테이블을 사용하여 탐색 속도가 O(1)로 매우 빠릅니다.
# 반면 List와 Tuple은 순차 검색을 하므로 O(n)의 시간이 걸립니다.
print("=== 4. 데이터 탐색 속도 비교 방식 ===")
print(f"List 내 2 존재 여부: {2 in sample_list}")
print(f"Set 내 2 존재 여부: {2 in sample_set}")
print(f"Dict 내 'b' Key 존재 여부: {'b' in sample_dict}")