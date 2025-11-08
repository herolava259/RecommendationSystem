from pydantic import BaseModel, Field
from uuid import UUID, uuid4
from datetime import datetime, date
from typing import List, Literal


class Product(BaseModel):
    product_id: UUID = Field(default_factory=uuid4)
    name: str = Field(default="")
    stock_quantity: int = Field(default=0)
    category_id: UUID = Field(default_factory=uuid4)
    publisher_id: UUID = Field(default_factory=uuid4)

class Category(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    name: str = Field(default="")
    slug: str = Field(default="")


class ProductAttribute(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    product_id: UUID = Field(default_factory=uuid4)
    attribute_name: str = Field(default="")
    attribute_value: str = Field(default="")

class MediaStuff(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    product_id: UUID = Field(default_factory=uuid4)
    url: str = Field(default="")
    type: str = Field(default="")


from enum import Enum

class OrderStatus(int, Enum):
    Pending = 1,
    Confirmed = 2,
    Canceled = 3,
    Shipping = 4,
    Finished = 5,
    Expired = 6


class Order(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    user_id: UUID = Field(default_factory=uuid4)
    order_date: date = Field(default=date.today())
    status: str = Field(default="")

class OrderItem(BaseModel):
    product_id: UUID = Field(default_factory=uuid4)
    order_id: UUID = Field(default_factory=uuid4)
    id: UUID = Field(default_factory=uuid4)
    quantity: int = Field(default=0)
    unit_price: int = Field(default=0)

class ShippingAddress(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    user_id: UUID = Field(default_factory=uuid4)
    address: str = Field(default="")
    city: str = Field(default="")
    province: str = Field(default="")
    full_name: str = Field(default="")
    street: str = Field(default="")
    zip_code: str = Field(default="")

class Transaction(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    order_id: UUID = Field(default_factory=uuid4)
    payment_date: date = Field(default_factory=date.today)
    method: str = Field(default="") # declare enum type later
    amount: int = Field(default=0)
    transaction_status: str = Field(default="")

#Specific Products

class Game(Product):
    genre: str = Field(default="")
    platform: str = Field(default="")
    age_rating: int = Field(default=3)
    release_date: date = Field(default_factory=date.today)


class Console(Product):
    model_number: int = Field(default=0)
    cpu_type: str = Field(default="")
    gpu_type: str = Field(default="")
    storage_size: str = Field(default="")



class Movie(Product):
    director: str = Field(default="")
    actors: List[str] = Field(default=list)
    runtime: int = Field(default=0)
    format: Literal["Blu-ray", "DVD", "Digital"] = Field(default="Digital")

# Coupons and Order Coupons

class Coupon(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    code: str = Field(default="")
    discount_type: str = Field(default="")
    discount_value: int = Field(default=0)
    expiry_date: date = Field(default_factory=date.today)
    min_order_amount: int = Field(default=0)

class OrderCouponRelationship(BaseModel):
    order_id: UUID = Field(default_factory=uuid4)
    coupon_id: UUID = Field(default_factory=uuid4)