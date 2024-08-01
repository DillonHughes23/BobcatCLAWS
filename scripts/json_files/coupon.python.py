import requests
from datetime import datetime
from sqlalchemy import create_engine, Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Store(Base):
    __tablename__ = 'stores'

    id = Column(String, primary_key=True)
    name = Column(String)

class Coupon(Base):
    __tablename__ = 'coupons'

    id = Column(String, primary_key=True)
    store_id = Column(String)
    url = Column(String)
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    description = Column(String)
    product_name = Column(String)

def store_coupon_data(api_data, session):
    for coupon_data in api_data.get("Store", {}).get("Coupon", []):
        store = session.query(Store).filter_by(name=api_data["Store"]["Name"]).first()
        if not store:
            new_store = Store(id=str(len(session.query(Store).all()) + 1), name=api_data["Store"]["Name"])
            session.add(new_store)
            session.commit()
            store_id = new_store.id
        else:
            store_id = store.id

        new_coupon = Coupon(
            id=str(len(session.query(Coupon).all()) + 1),
            store_id=store_id,
            url=coupon_data.get("URL", ""),
            start_date=datetime.strptime(coupon_data.get("Start_Date", ""), "%Y-%m-%d"),
            end_date=datetime.strptime(coupon_data.get("End_Date", ""), "%Y-%m-%d"),
            description=coupon_data.get("Description", ""),
            product_name=coupon_data.get("Product_Name", None)
        )
        session.add(new_coupon)
        session.commit()
        
    api_url = "https://get-promo-codes.p.rapidapi.com/data/get-coupons/"
    headers = {'X-RapidAPI-Key': api_key}

    response = requests.get(api_url, params={"page": "1", "sort": "update_time_desc"}, headers=headers)

    if response.status_code == 200:
        api_data = response.json()
        store_coupon_data(api_data, session)
    else:
        print(f"API request failed with status code: {response.status_code}")

    session.close()

api_key = '490829acf0msh5ecade697e94d6cp1af5d2jsn'
get_promo_codes(api_key)