people = [
    {"name":"Khang", "age":20, "email":"asdasf@gmail.com"},
    {"name":"Kh", "age":2, "email":"sf@gmail.com"},
    {"name":"ang", "age":0, "email":"f@gmail.com"}
]
print("danh sách ban đàu:")
for p in people:
    print(p)
new =     {"name":"g", "age":2000, "email":"a@gmail.com"}
people.append(new)
print("thêm 1 ng: ")
for p in people:
    print(p)
print("\n tuoi ng thu hai:",people[1]["age"])
people[0]["email"]="aaaaaa@gmail.com"
print("\n đã sửa ng đàu tiên:")
for p in people:
    print(p)
people.pop(2)
print("xóa ng cúi ")
for p in people:
    print(p)