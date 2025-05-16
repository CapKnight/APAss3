import os
from app import create_app, db
from app.models import BasicInfo, Appearance, OtherInfo, UrlInfo

def init_sample_data():
    app = create_app()
    with app.app_context():
        if BasicInfo.query.count() == 0:
            basic = BasicInfo(
                page_id=1,
                name="Test Character",
                ID="TEST001",
                ALIGN="Good",
                SEX="Male",
                ALIVE="Living",
                YEAR="2023"
            )
            db.session.add(basic)
            
            appearance = Appearance(
                page_id=1,
                EYE="Blue",
                HAIR="Brown"
            )
            db.session.add(appearance)
            
            other = OtherInfo(
                page_id=1,
                GSM="Heterosexual",
                APPEARANCES="10",
                FIRST_APPEARANCE="Issue #1"
            )
            db.session.add(other)
            
            url = UrlInfo(
                page_id=1,
                urlslug="/character/test"
            )
            db.session.add(url)
            
            db.session.commit()
            print("Sample data initialized")
        else:
            print("Data already exists")

if __name__ == '__main__':
    init_sample_data()