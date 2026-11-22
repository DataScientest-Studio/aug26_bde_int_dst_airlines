from fastapi import APIRouter, Depends
from src.databases.databases import Database
from src.fapi.models.icon_model import IconModel
from src.databases.dependencies.get_database import get_db
from pypika import Query, Table, functions as fn

class Get_Icon_List:
    
    def __init__(self):
        self.router = APIRouter()
        self.router.add_api_route("/get_icon_list", self.get_icon_list, methods=["GET"])

    def get_icon_list(self, db: Database = Depends(get_db)):
        rows = self.get_icon_rows(db)

        icon_list = []

        for r in rows:
            icon = IconModel(
                icon_id = r["icon_id"], 
                icon = r["icon"],
            )
            icon_list.append(icon)
        

        return {
            "icon_list": icon_list
        }

    def get_icon_rows(self, db: Database):
        # SQL:
        # select * from icon
        
        icon = Table('icon')
        query = Query.from_(icon).select('*')
        sql_string = query.get_sql()

        result = db.execute_sql(sql_string)

        return result
