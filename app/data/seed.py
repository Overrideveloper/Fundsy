from .database import db
from .repositories.admin import AdminRepository, AdminCreateReq
from common.config import ADMIN_NAME, ADMIN_PASSWORD, ADMIN_USERNAME

admin_repo = AdminRepository(db)

def seed_admin():
    try:       
        is_existing_admin = admin_repo.is_existing_admin()
        
        if not is_existing_admin:
            admin_repo.create(AdminCreateReq(name=ADMIN_NAME, username=ADMIN_USERNAME, password=ADMIN_PASSWORD))
            print("Admin created")
        else:
            pass
    except Exception as err:
        print(err)