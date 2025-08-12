"""Quy trình làm bài tập CRUD User với FastAPI và MongoDB
            Chuẩn bị môi trường
Tạo môi trường Python ảo, cài thư viện cần thiết:
fastapi, uvicorn, pymongo, pydantic.
            Lên kế hoạch code
a) Kết nối MongoDB
Dùng PyMongo MongoClient để kết nối tới MongoDB.
Chọn database và collection lưu user.
b) Tạo ứng dụng FastAPI
Khởi tạo app FastAPI để viết các API.
c) Định nghĩa dữ liệu user
Dùng Pydantic BaseModel để định nghĩa cấu trúc dữ liệu user (ví dụ: name, email, age).
Điều này giúp tự động kiểm tra dữ liệu khi client gửi lên.
d) Viết hàm định dạng dữ liệu
MongoDB trả dữ liệu có trường _id kiểu ObjectId không thể gửi thẳng về JSON.
Viết hàm chuyển ObjectId sang chuỗi để trả về client.
e) Viết API CRUD
POST /nguoi_dung: Thêm user mới (nhận dữ liệu, validate, lưu MongoDB).
GET /nguoi_dung: Lấy danh sách user (truy vấn tất cả, format, trả về JSON).
PUT /nguoi_dung/{id}: Cập nhật user theo ID (tìm, cập nhật, kiểm tra lỗi).
DELETE /nguoi_dung/{id}: Xóa user theo ID (tìm, xóa, kiểm tra lỗi)."""
# Import thư viện
from pymongo import MongoClient  # 1.kết nối với mongoDB,trả về nếu lỗi
from fastapi import FastAPI,HTTPException  # 2.tạo ứng dụng fastapi 
from pydantic import BaseModel #3.định nghĩa kiểu dữ liệu
from bson import ObjectId # 4.để tạo và xử lí id 1 cách hợp lệ trong mongoDB(định dạng)
"""bson > định dạng dữ liệu nhị phân mà MongoDB dùng (giống JSON nhưng mạnh hơn).
   ObjectId > kiểu dữ liệu đặc biệt cho khóa _id.
   from bson import ObjectId > để bạn tạo và xử lý _id đúng kiểu khi làm việc với MongoDB bằng Python."""

# 1. Kết nối MongoDB
ket_noi_mongo = MongoClient("mongodb://localhost:27017")   # Tạo kết nối tới MongoDB (localhost, cổng 27017)
db = ket_noi_mongo["user_db"]           # Chọn database "user_db"
users_collection = db["users"]           # Chọn collection (bảng)"users"     collection tương tự như dict là từ điển trong python

# 2. Tạo ứng dụng FastAPI
app = FastAPI()

# 3.định nghĩa (để kiểm tra & ép kiểu)
class user(BaseModel):
    """(BaseModel)cho phép:
Xác định cấu trúc dữ liệu (có những trường nào, kiểu gì).
Tự động validate (báo lỗi nếu thiếu hoặc sai kiểu).
Tự động ép kiểu (nếu có thể).
Tích hợp sẵn với FastAPI để hiển thị tài liệu API trên /docs."""
    name: str
    email: str
    age: int

# 4. định dạng 
def dinh_dang_user(user_goc) -> dict:
    return {
        "id": str(user_goc["_id"]),  # ép id thành chuỗi có dấu _ là khóa chính của mongoDB quy ước dấu _ sẽ là khóa chính và kh trùng lặp dữ liệu
        "ten": user_goc["name"],
        "email": user_goc["email"],
        "tuoi": user_goc["age"]
    }

# 5. API chào mừng !!!!! đăng kí đường dẫn API đến sever
@app.get("/")
def trang_chu():
    return {"thong_diep": "Chào mừng đến API Quản Lý Người Dùng với MongoDB"}
# 6. API thêm người dùng
@app.post("/user")   
#=>>>>>>>>>>>>>>>>>>>>>>sự khác biệt giữa () trong hàm 6&7 là 
#Get () rỗng vì kh cần dữ lịu đầu vào 
#Post (du...:... cần dưx liệu vì nhận dữ liệu từ ng dùng gửi lên)
def them_user(du_lieu:user):
    moi = du_lieu.dict()  # Ép BaseModel -> dict 
    """Vì dữ liệu từ client > FastAPI ép kiểu thành BaseModel (để kiểm tra).
       Muốn lưu vào MongoDB > chuyển BaseModel thành dict vì MongoDB không hiểu object Python."""
    ket_qua = users_collection.insert_one(moi)
    return {"_id": str(ket_qua.inserted_id), **moi} # **moi là chèn dô từ cái moi cũ lên moi mới
#ép về str vì MongoDB tạo ID kiểu ObjectId > phải chuyển thành chuỗi str
#  > mới gửi được qua API cho client

# 7. API lấy danh sách người dùng
@app.get("/user")
def lay_danh_sach():
    tat_ca = users_collection.find()  #find lấy tất cả tài liệu trong doc của collection
    return [dinh_dang_user(nd) for nd in tat_ca]    #[ biểu_thức for i in range hài lúc học ]

"""ket_qua = []
for nd in tat_ca:
    nd_dinh_dang = {
        "id": str(nd["_id"]),
        "ten": nd["name"],
        "email": nd["email"],
        "tuoi": nd["age"]
    }
    ket_qua.append(nd_dinh_dang)
return ket_qua    =>>> này là return kiểu còn gà !!!!!!!nhớ học cái nâng cao ở trên
"""
# 8. API cập nhật người dùng
@app.put("/user/{id_user}")
def cap_nhat_user(id_user: str, du_lieu: user):
    ket_qua = users_collection.update_one( #diều kiện lọc dữ liệu
        {"_id": ObjectId(id_user)},
        #Lấy ID từ client (chuỗi)	Chuyển chuỗi > ObjectId để truy vấn MongoDB
        #Lấy document trả về client	Chuyển ObjectId > chuỗi để JSON hoá và gửi đi
        {"$set": du_lieu.dict()} # $set  thay đổi hoặc thêm trường mới vào document
    ) 
    if ket_qua.matched_count == 0: #matched_count là số document tìm thấy
        raise HTTPException(status_code=404, detail="Không tìm thấy người dùng")
    else:
        return {"thong_diep": "Cập nhật thành công"}
#raise dùng để ném ra một lỗi (exception)
"""HTTPException trong Fastapi dùng để báo cho client rằng API đã gặp lỗi HTTP (ví dụ: 404 Not Found
detail là nội dung mô tả lỗi(phải dùng them này sau khi dungfHTTPException vì nếu kh dùng thì chỉ 
clent biết 404 thoi chứ kh biết là sai cái gì)"""
# 9. API xóa người dùng
@app.delete("/user/{id_user}")
def xoa_user(id_user: str):
    ket_qua = users_collection.delete_one({"_id": ObjectId(id_user)})
    if ket_qua.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Không tìm thấy người dùng")
    else:
        return {"thong_diep": "Xóa thành công"}
#Lưu > dict()   Tìm > ObjectId()  Trả > str()