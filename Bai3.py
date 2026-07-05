from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel

app = FastAPI()

products_db = [
    {"id": 101, "name": "Bàn phím cơ", "stock": 5, "price": 1200000.0},
    {"id": 102, "name": "Chuột Gaming", "stock": 2, "price": 600000.0}
]
orders_db = []


class OrderCreate(BaseModel):
    product_id: int
    quantity: int

@app.post("/orders", status_code=status.HTTP_201_CREATED)
def create_order(order_data: OrderCreate):
    if order_data.quantity <= 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Số lượng mua phải lớn hơn 0")

    target_product = None
    for p in products_db:
        if p["id"] == order_data.product_id:
            target_product = p
            break

    if target_product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sản phẩm không tồn tại trên hệ thống")

    if order_data.quantity > target_product["stock"]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Sản phẩm không đủ số lượng trong kho")

    target_product["stock"] -= order_data.quantity

    total_price = order_data.quantity * target_product["price"]
    new_order = {
        "order_id": len(orders_db) + 1,
        "product_id": order_data.product_id,
        "product_name": target_product["name"],
        "quantity": order_data.quantity,
        "total_price": total_price
    }

    orders_db.append(new_order)
    return {"message": "Tạo đơn hàng thành công", "order": new_order}