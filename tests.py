from flask import url_for
from flask_testing import TestCase
import application
import datetime


class TestBase(TestCase):
    def create_app(self):
        application.app.config.update(
            SQLALCHEMY_DATABASE_URI='sqlite:///test.db',
            SECRET_KEY='TEST_SECRET_KEY',
            DEBUG=True,
            WTF_CSRF_ENABLED=False
        )
        return application.app

    def setUp(self):
        application.db.create_all()
        sampleemp = application.Employees(name='John', dept='IT', rate=9, hours=40)
        sampleshift = application.Shifts(date=datetime.datetime(2021, 11, 15), no_emps=1, type='eve', hours=9)
        samplerota = application.Rota(emp_no=1, shift_no=1)
        application.db.session.add(sampleshift)
        application.db.session.add(sampleemp)
        application.db.session.add(samplerota)
        application.db.session.commit()

    def tearDown(self):
        application.db.session.remove()
        application.db.drop_all()


class TestViews(TestBase):
    def test_rotas_get(self):
        response = self.client.get(url_for('homepage'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'1', response.data)

    def test_emps_get(self):
        response = self.client.get(url_for('employees'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'John', response.data)

    def test_shifts_get(self):
        response = self.client.get(url_for('shifts'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'1', response.data)

    def test_edit_emp(self):
        response = self.client.post(
            url_for('editemployee', emp_no=1),
            data=dict(name="Chris", dept='Consultants', rate=10, hours=30),
            follow_redirects=True
        )
        self.assertIn(b'Chris', response.data)

    def test_view_emp(self):
        response = self.client.get(url_for('editemployee', emp_no=1))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Name', response.data)

    def test_add_emp(self):
        response = self.client.post(
            url_for('addemp'),
            data=dict(name='James', dept='Consultants', rate=8, hours=40),
            follow_redirects=True
        )
        self.assertIn(b'James', response.data)

    def test_del_emp(self):
        response = self.client.get(url_for('delemp', emp_no=1), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Employee Editing', response.data)

    def test_add_shift(self):
        response = self.client.post(
            url_for('addshift'),
            data=dict(date='2021-11-16', no_emps=1, type='morn', hours=3),
            follow_redirects=True
        )
        self.assertIn(b'2021-11-16', response.data)

    def test_edit_shift(self):
       response= self.client.post(
           url_for('editshift', shift_no=1),
           data=dict(date='2021-12-20', no_emps=3, type='eve', hours=3),
           follow_redirects=True
       )
       self.assertIn(b'2021-12-20', response.data)

    def test_view_shift(self):
        response=self.client.get(url_for('editshift', shift_no=1))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Date', response.data)

    def test_del_shift(self):
        response = self.client.get(url_for('delshift', shift_no=1), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Shift Editing', response.data)

    def test_create_rota(self):
        response=self.client.post(
            url_for('createrota'),
            data=dict(emp_id=1, shift_id=1),
            follow_redirects=True
        )
        self.assertIn(b'1', response.data)

    def test_view_addemp(self):
        response = self.client.get(url_for('addemp'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Name', response.data)

    def test_view_addshift(self):
        response = self.client.get(url_for('addshift'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Date', response.data)

    def test_view_createrota(self):
        response = self.client.get(url_for('createrota'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Select Employee', response.data)
