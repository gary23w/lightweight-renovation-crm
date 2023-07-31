from abc import ABC, abstractmethod
from flask import current_app
from sib_api_v3_sdk import SendSmtpEmail, TransactionalEmailsApi
from sib_api_v3_sdk.rest import ApiException
from sib_api_v3_sdk import Configuration, ApiClient
import datetime


class EmailBuilder(ABC):

    @abstractmethod
    def build_content(self, **kwargs):
        pass

class UpdateAdminEmailBuilder(EmailBuilder):

    def build_content(self, data):
        html_content = open('app/admin/email/tpls/update.gary.email').read()
        job_payload = ""
        for job in data:
            job_payload += f"""
            <div class="customer-info">
                <hr style="border: 1px solid #ccc; margin-bottom: 20px;">
                <h3 class="delv-h3">Job ID: {job.id}</h3>
                <p class="delv-head">Customer: {job.customer}</p>
                <p class="delv-comp">Salesman: {job.salesman}</p>
                <p class="delv-comp">Address: {job.address}, {job.city}</p>
                <p class="delv-comp">Phone: {job.phone}</p>
                <p class="delv-desc">Job Description: {job.description}</p>
                <p class="delv-comp">Status: {job.status}</p>
                <p class="delv-list-item">Notes: {job.notes}</p>
                <hr style="border: 1px solid #ccc; margin-bottom: 20px;">
            </div>
            """
        html_content = html_content.replace("{{ job_updates }}", job_payload)

        return html_content


class WelcomeEmailBuilder(EmailBuilder):

    def build_content(self, salesman):
        html_content = open('app/admin/email/tpls/welcome.gary.email').read()
        html_content = html_content.replace("{{ salesman }}", salesman)
        html_content = html_content.replace("{{ phone }}", current_app.config['PHONE_LIST'][salesman.lower()])
        return html_content


class ExitEmailBuilder(EmailBuilder):

    def build_content(self):
        html_content = open('app/admin/email/tpls/exit.gary.email').read()
        return html_content


class QuoteEmailBuilder(EmailBuilder):

    def build_content(self, data, notes):
        expiry_date = datetime.datetime.now() + datetime.timedelta(days=30)
        expiry_date = expiry_date.strftime("%Y-%m-%d")
        current_date = datetime.datetime.now().strftime("%Y-%m-%d")
        noteBox = []
        html_content = open('app/admin/email/tpls/quote.gary.email').read()
        html_content = html_content.replace("{{ job_title }}", data.job_title)
        html_content = html_content.replace("{{ job_description }}", data.job_description)
        html_content = html_content.replace("{{ quote_amount }}", str(data.quote_amount))
        html_content = html_content.replace("{{ quote_date }}", current_date)
        html_content = html_content.replace("{{ quote_expiry }}", expiry_date)
        html_content = html_content.replace("{{ client_email }}", data.customer_email)
        html_content = html_content.replace("{{ your_phone }}", str(data.your_phone))
        if notes is not None:
            html_content = html_content.replace("{{ sendNotes }}", "<p class=\"delv-speach\">Here are the details about your job:</p>")
            for note in notes:
                noteBox.append("<li>" + note + "</li>")
            html_content = html_content.replace("{{ notes }}", "".join(noteBox))
        return html_content


class MailingEmailBuilder(EmailBuilder):

    def build_content(self, content_):
        return content_

def email_builder_factory(type_):
    if type_ == 'welcome':
        return WelcomeEmailBuilder()
    elif type_ == 'exit':
        return ExitEmailBuilder()
    elif type_ == 'quote':
        return QuoteEmailBuilder()
    elif type_ == 'mailing':
        return MailingEmailBuilder()
    elif type_ == 'update':
        return UpdateAdminEmailBuilder()
    else:
        raise ValueError("Invalid email type")


class EmailSender:
    def __init__(self, email_builder):
        self.email_builder = email_builder

    def send_email(self, to, type_, salesman="admin", content_=None, subject_=None, notes=None, data=None):
        logo = current_app.config['LOGO']
        configuration = Configuration()
        configuration.api_key['api-key'] = current_app.config['SIB_API_KEY']
        company_website = current_app.config['WEBSITE']
        email_hyperlink = current_app.config['EMAIL_HYPERLINK']
        sales_email = salesman + email_hyperlink
        info_email = current_app.config['INFO_EMAIL']
        company_name = current_app.config['NAME']
        company_short_name = current_app.config['SHORT_NAME']
        office_phone = current_app.config['SUPPORT_PHONE']
        api_instance = TransactionalEmailsApi(ApiClient(configuration))
        date_now = datetime.datetime.now().strftime("%Y-%m-%d")

        if type_ == 'welcome':
            html_content = self.email_builder.build_content(salesman=salesman)
            subject = "Welcome to " + company_name + "."
        elif type_ == 'exit':
            html_content = self.email_builder.build_content()
            subject = "Thank you for choosing " + company_name
        elif type_ == 'mailing':
            html_content = self.email_builder.build_content(content_=content_)
            subject = subject_
        elif type_ == 'quote':
            html_content = self.email_builder.build_content(data=data, notes=notes)
            subject = company_short_name + " QUOTE " + date_now
            sales_email = info_email
        elif type_ == 'update':
            html_content = self.email_builder.build_content(data=data)
            subject = "LFBUILDERS-DAILY-UPDATE-" + date_now
            sales_email = info_email
        else:
            raise Exception("Invalid email type")
        
        html_content = html_content.replace("{{ logo_main }}", logo)
        html_content = html_content.replace("{{ company_name }}", company_name)
        html_content = html_content.replace("{{ office_phone }}", office_phone)
        html_content = html_content.replace("{{ company_website }}", company_website)
        html_content = html_content.replace("{{ info_email }}", info_email)

        sender = {"name": salesman,"email": sales_email}

        send_smtp_email = SendSmtpEmail(to=[{"email": to}], html_content=html_content, sender=sender, subject=subject)
        
        try:
            api_response = api_instance.send_transac_email(send_smtp_email)
            return api_response
        except ApiException as e:
            return e

#TODO: expand this design pattern across the entire app. this is a hack to get it working for now.
def send_email(to, type_, salesman="admin", content_=None, subject_=None, notes=None, data=None):
    builder = email_builder_factory(type_)
    email_sender = EmailSender(builder)
    email_sender.send_email(to, type_, salesman, content_, subject_, notes, data)
