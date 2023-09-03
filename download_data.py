import os
import requests
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DATABASE_URL = "sqlite:///products.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    brand = Column(String)
    category = Column(String)
    merchant = Column(String)
    ram = Column(String)
    rom = Column(String)
    front_camera = Column(String)
    image_url = Column(String)


if not os.path.exists("products.db"):
    Base.metadata.create_all(bind=engine)


def download_and_save_data():
    url = "https://API_EXAMPLE.com/products"

    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()["offers"]

        db = SessionLocal()

        for item in data:
            product = Product(
                name=item["name"],
                brand=item["brand"],
                category=item["category"],
                merchant=item["merchant"],
                ram=item["attributes"][0]["value"] if len(item["attributes"]) > 0 else None,
                rom=item["attributes"][1]["value"] if len(item["attributes"]) > 1 else None,
                front_camera=item["attributes"][2]["value"] if len(item["attributes"]) > 2 else None,
                image_url=item["image"]["url"],
            )
            db.add(product)

        db.commit()
        db.close()
        print("Данные успешно загружены и сохранены в базе данных.")
    else:
        print("Не удалось получить данные с сервера.")


if __name__ == "__main__":
    download_and_save_data()
