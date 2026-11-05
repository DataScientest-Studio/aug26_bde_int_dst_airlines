from src.databases.databases import Database

def get_db():
    with Database() as db:
        yield db