import unittest
from app import create_app, db
from app.models import BasicInfo, Appearance, OtherInfo, UrlInfo
from app.blueprints.character import character_bp

class TestDCCharacters(unittest.TestCase):
    def setUp(self):
        """设置测试环境，创建测试应用和数据库"""
        self.app = create_app()
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # 使用内存数据库
        self.app.config['TESTING'] = True
        # 移除重复注册，因为 create_app() 已注册蓝图
        # self.app.register_blueprint(character_bp, url_prefix='/')
        self.client = self.app.test_client()

        # 创建表
        with self.app.app_context():
            db.create_all()
            # 插入测试数据
            self._insert_test_data()

    def tearDown(self):
        """清理测试环境"""
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def _insert_test_data(self):
        """插入测试数据到数据库"""
        with self.app.app_context():
            basic1 = BasicInfo(page_id=1, name="Superman", ALIGN="Good", SEX="Male", ALIVE="Living", YEAR="1938")
            basic2 = BasicInfo(page_id=2, name="Batman", ALIGN="Good", SEX="Male", ALIVE="Living", YEAR="1939")
            db.session.add_all([basic1, basic2])
            db.session.flush()

            appearance1 = Appearance(page_id=1, EYE="Blue", HAIR="Black")
            appearance2 = Appearance(page_id=2, EYE="Blue", HAIR="Black")
            db.session.add_all([appearance1, appearance2])

            other1 = OtherInfo(page_id=1, GSM="No", APPEARANCES="1000", FIRST_APPEARANCE="Action Comics #1")
            other2 = OtherInfo(page_id=2, GSM="No", APPEARANCES="2000", FIRST_APPEARANCE="Detective Comics #27")
            db.session.add_all([other1, other2])

            url1 = UrlInfo(page_id=1, urlslug="/superman")
            url2 = UrlInfo(page_id=2, urlslug="/batman")
            db.session.add_all([url1, url2])
            db.session.commit()

    def test_index_route(self):
        """测试 index 路由和筛选功能"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Superman', response.data)
        self.assertIn(b'Batman', response.data)

        # 测试筛选
        response = self.client.get('/?search_name=Superman')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Superman', response.data)
        self.assertNotIn(b'Batman', response.data)

    def test_character_detail_route(self):
        """测试 character_detail 路由"""
        response = self.client.get('/character/1')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Superman', response.data)
        self.assertIn(b'1938', response.data)

        # 测试 404
        response = self.client.get('/character/999')
        self.assertEqual(response.status_code, 404)

    def test_compare_route(self):
        """测试 compare 路由"""
        # 无选择角色
        response = self.client.get('/compare')
        self.assertEqual(response.status_code, 400)
        self.assertIn(b'No characters selected', response.data)

        # 选择角色
        with self.client.session_transaction() as sess:
            sess['selected_ids'] = [1]
        response = self.client.get('/compare')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Superman', response.data)

    def test_clear_filters_route(self):
        """测试 clear_filters 路由"""
        # 应用筛选
        response = self.client.get('/?search_name=Superman')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Superman', response.data)
        self.assertNotIn(b'Batman', response.data)

        # 清除筛选，跟随重定向
        response = self.client.get('/clear_filters', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Superman', response.data)
        self.assertIn(b'Batman', response.data)

    def test_analysis_route(self):
        """测试 analysis 路由"""
        response = self.client.get('/analysis')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Good', response.data)  # 阵营比例
        self.assertIn(b'Male', response.data)  # 性别分布

    def test_database_records(self):
        """测试数据库记录和关系"""
        with self.app.app_context():
            basics = BasicInfo.query.all()
            self.assertEqual(len(basics), 2)
            self.assertEqual(basics[0].name, "Superman")
            self.assertEqual(basics[0].appearance.EYE, "Blue")
            self.assertEqual(basics[0].other_info.APPEARANCES, "1000")
            self.assertEqual(basics[0].url_info.urlslug, "/superman")

if __name__ == '__main__':
    unittest.main()