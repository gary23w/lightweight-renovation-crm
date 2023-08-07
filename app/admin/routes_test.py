from unittest.mock import patch
from flask import url_for
from werkzeug.datastructures import ImmutableMultiDict
from flask_testing import TestCase
from app import create_app, db
from http import HTTPStatus
from werkzeug.datastructures import FileStorage
from io import BytesIO

class GaryTest(TestCase):
    def create_app(self):
        app = create_app('config_for_testing')
        return app

    def setUp(self):
        db.create_all() # yahtzee

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    @patch('app.bp.login_required')
    def test_admin_static(self, mock_login_required):
        mock_login_required.return_value = True
        response = self.client.get(url_for('admin_static', filename='test.png'))
        self.assert200(response)

    @patch('app.bp.login_required')
    def test_admin_route(self, mock_login_required):
        mock_login_required.return_value = True
        response = self.client.get(url_for('admin_route'))
        self.assert200(response)

    @patch('app.bp.login_required')
    def test_logout_route(self, mock_login_required):
        mock_login_required.return_value = True
        response = self.client.get(url_for('logout_route'))
        self.assertRedirects(response, url_for('user.home_route'))

    @patch('app.bp.login_required')
    def test_docs_route(self, mock_login_required):
        mock_login_required.return_value = True
        response = self.client.get(url_for('docs_route'))
        self.assert200(response)

    @patch('app.bp.login_required')
    def test_add_customer_route(self, mock_login_required):
        mock_login_required.return_value = True
        form = ImmutableMultiDict({
            # FILL OUT FORM DATA
        })
        response = self.client.post(url_for('add_customer_route'), data=form)
        self.assertRedirects(response, url_for('admin.admin_route'))

        @patch('app.bp.login_required')
    def test_delete_customer_route(self, mock_login_required):
        mock_login_required.return_value = True
        response = self.client.post(url_for('delete_customer_route', id=1))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    @patch('app.bp.login_required')
    def test_create_table_route(self, mock_login_required):
        mock_login_required.return_value = True
        response = self.client.post(url_for('create_table_route'))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    @patch('app.bp.login_required')
    def test_customers(self, mock_login_required):
        mock_login_required.return_value = True
        response = self.client.get(url_for('customers'))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    @patch('app.bp.login_required')
    def test_single_table(self, mock_login_required):
        mock_login_required.return_value = True
        response = self.client.get(url_for('single_table'))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    @patch('app.bp.login_required')
    def test_deploy_sms_promo(self, mock_login_required):
        mock_login_required.return_value = True
        response = self.client.get(url_for('deploy_sms_promo'))
        self.assert200(response)

    @patch('app.bp.login_required')
    def test_send_sms_promotion_main(self, mock_login_required):
        mock_login_required.return_value = True
        response = self.client.post(url_for('send_sms_promotion_main'))
        self.assert200(response)

    @patch('app.bp.login_required')
    def test_email_promo_main(self, mock_login_required):
        mock_login_required.return_value = True
        response = self.client.get(url_for('email_promo_main'))
        self.assert200(response)

    @patch('app.bp.login_required')
    def test_add_mail_promo_user(self, mock_login_required):
        mock_login_required.return_value = True
        form = ImmutableMultiDict({
            # FILL OUT FORM DATA
        })
        response = self.client.post(url_for('add_mail_promo_user'), data=form)
        self.assert200(response)

    @patch('app.bp.login_required')
    def test_send_email_promotion_main(self, mock_login_required):
        mock_login_required.return_value = True
        response = self.client.post(url_for('send_email_promotion_main'), data={"promo": "Promo"})
        self.assert200(response)

    @patch('app.bp.login_required')
    def test_delete_mail_promo_user(self, mock_login_required):
        mock_login_required.return_value = True
        response = self.client.post(url_for('delete_mail_promo_user', id=1))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    @patch('app.bp.login_required')
    def test_add_notifications(self, mock_login_required):
        mock_login_required.return_value = True
        response = self.client.get(url_for('add_notifications'))
        self.assert200(response)

    @patch('app.bp.login_required')
    def test_send_custom_notification(self, mock_login_required):
        mock_login_required.return_value = True
        form = ImmutableMultiDict({
            "noteTitle": "Test Notification",
            "noteBody": "This is a test notification.",
            "salesman": "yaaaarrrr",
        })
        response = self.client.post(url_for('send_custom_notification'), data=form)
        self.assert200(response)

        @patch('app.bp.login_required')
    def test_delete_notification_route(self, mock_login_required):
        mock_login_required.return_value = True
        response = self.client.post(url_for('delete_notification_route'))
        self.assert200(response)

    @patch('app.bp.login_required')
    def test_delete_table_route(self, mock_login_required):
        mock_login_required.return_value = True
        response = self.client.post(url_for('delete_table_route'))
        self.assert200(response)

    @patch('app.bp.login_required')
    def test_upload_spreadsheets_route(self, mock_login_required):
        mock_login_required.return_value = True
        response = self.client.get(url_for('upload_spreadsheets_route'))
        self.assert200(response)

    @patch('app.bp.login_required')
    def test_upload_spreadsheets_single_route(self, mock_login_required):
        mock_login_required.return_value = True
        data = {
            'spreadsheetFile': (BytesIO(b'my file contents'), 'test_file.xlsx')
        }
        response = self.client.post(url_for('upload_spreadsheets_single_route'), data=data, content_type='multipart/form-data')
        self.assert200(response)

    @patch('app.bp.login_required')
    def test_job_board_route(self, mock_login_required):
        mock_login_required.return_value = True
        response = self.client.get(url_for('job_board_route'))
        self.assert200(response)

    @patch('app.bp.login_required')
    def test_add_job_route(self, mock_login_required):
        mock_login_required.return_value = True
        form = ImmutableMultiDict({
            # FILL OUT FORM DATA
        })
        response = self.client.post(url_for('add_job_route'), data=form)
        self.assert200(response)

    @patch('app.bp.login_required')
    def test_edit_job_route(self, mock_login_required):
        mock_login_required.return_value = True
        form = ImmutableMultiDict({
            # FILL OUT FORM DATA
        })
        response = self.client.post(url_for('edit_job_route'), data=form)
        self.assert200(response)

    @patch('app.bp.login_required')
    def test_delete_job_route(self, mock_login_required):
        mock_login_required.return_value = True
        form = ImmutableMultiDict({
            "id": "1",
            "email": "test@email.com"
        })
        response = self.client.post(url_for('delete_job_route'), data=form)
        self.assert200(response)

    @patch('app.bp.login_required')
    def test_download_jobs_route(self, mock_login_required):
        mock_login_required.return_value = True
        response = self.client.get(url_for('download_jobs_route'))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    @patch('app.bp.login_required')
    def test_quoting_tool(self, mock_login_required):
        mock_login_required.return_value = True
        response = self.client.get(url_for('quoting_tool'))
        self.assert200(response)

        @patch('app.bp.login_required')
    def test_quoting_tool_route(self, mock_login_required):
        mock_login_required.return_value = True
        form_data = {
            # FILL OUT FORM DATA
        }
        response = self.client.post(url_for('quoting_tool_route'), data=form_data)
        self.assert200(response)

    @patch('app.bp.login_required')
    def test_get_quote_list(self, mock_login_required):
        mock_login_required.return_value = True
        response = self.client.get(url_for('get_quote_list'))
        self.assert200(response)

    @patch('app.bp.login_required')
    def test_delete_quote_route(self, mock_login_required):
        mock_login_required.return_value = True
        id = 1 # Adjust the id based on your test data
        response = self.client.post(url_for('delete_quote_route', id=id))
        self.assert200(response)

    @patch('app.bp.login_required')
    def test_resend_quote_route(self, mock_login_required):
        mock_login_required.return_value = True
        id = 1 # Adjust the id based on your test data
        response = self.client.post(url_for('resend_quote_route', id=id))
        self.assert200(response)

    @patch('app.bp.login_required')
    def test_health(self, mock_login_required):
        mock_login_required.return_value = True
        response = self.client.get(url_for('health'))
        self.assert200(response)

    

    