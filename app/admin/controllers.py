from flask import request, jsonify, flash
from flask_login import logout_user
from sqlalchemy import inspect, or_, text
from sqlalchemy.exc import SQLAlchemyError
from openpyxl import load_workbook
from pytz import utc
from app import db
from app.admin.email.engine import send_email
from app.models.customer import Customer
from app.models.mailing import Mailing
from app.models.notifications import Notifications
from app.models.job import Jobs
from app.models.quote import Quote
import pandas as pd
import os
import requests
from io import BytesIO

#TODO: more error handling.

def log_important_stuff(message):
    print(message)

def create_table():
    table_names = ['customers', 'mailing', 'notifications', 'jobs', 'quotes']
    existing_tables = inspect(db.engine).get_table_names()
    table_existence = {table: table in existing_tables for table in table_names}
    try:
        db.create_all()
        return {'message': 'Tables created or already exist', 'tables': table_existence}, 200
    except SQLAlchemyError as e:
        return {'message': 'An error occurred', 'error': str(e)}, 500

def get_the_score(scoreboard_users):
    the_score = []
    try:
        for user in scoreboard_users:
            score = len(Customer.query.filter_by(salesman=user['username']).all())
            obj = {"username": user['username'], "score": score, "call_sign": user['call_sign']}
            the_score.append(obj)
        the_score = sorted(the_score, key=lambda k: k['score'], reverse=True)
    except SQLAlchemyError as e:
        flash("The tables do not exist. Please create them first.")
    return the_score

def delete_table(headers):
    # this was used in development mode. saved time from having to delete the tables manually.
    Authorization = headers.get('Authorization')
    modular = False
    if Authorization == "Basic superbigadminwithbigadminideas:imnotthatbright":
        try:
            db.drop_all()
            modular = True
            return {'message': 'Table deleted'}, 200
        except SQLAlchemyError as e:
               return {'message': 'An error occurred', 'error': str(e)}, 500
    else:
        return {'message': 'An error occurred', 'error': 'Invalid credentials'}, 500

def check_service_status(url):
    try:
        response = requests.get(url)
        return response.status_code == 200
    except requests.RequestException:
        return False

def build_service_list(service_list):
    services_ = ""
    for service in service_list:
        for service_name, url in service.items():
            status = "ONLINE" if check_service_status(url) else "OFFLINE"
            badge = "success" if status == "ONLINE" else "danger"
            services_ += f'<li><span class="badge badge-{badge}">{status}</span> : <a href="{url}">{service_name.capitalize()}</a></li>'
    return services_

def insert_into_promo_list(form):
    try:
        if 'mailing' not in inspect(db.engine).get_table_names():
            return {'message': 'An error occurred', 'error': 'The table is not initialized. Please click the "Initialize" button on the main page.'}, 500
        new_customer = Mailing(customer=form.customer.data, email=form.email.data)
        db.session.add(new_customer)
        db.session.commit()
        return {'message': 'Customer added'}, 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return {'message': 'An error occurred', 'error': str(e)}, 500

def add_customer(form, welcome_email=False, mailList=False):
    if 'customers' not in inspect(db.engine).get_table_names():
        return {'message': 'An error occurred', 'error': 'The table is not initialized. Please click the "Initialize" button on the main page.'}, 500
    try:
        if mailList:
            mail_promo_customer = Mailing(customer=form.name.data, email=form.email.data)
            db.session.add(mail_promo_customer)
        new_customer = Customer(contract_number=form.contract_number.data, salesman=form.salesman.data, 
                                name=form.name.data, address=form.address.data, city=form.city.data, 
                                phone=form.phone.data, description=form.description.data, date=form.date.data, email=form.email.data)
        db.session.add(new_customer)
        db.session.commit()
        conf = None
        if welcome_email:
            conf = send_email(new_customer.email, "welcome", new_customer.salesman)
        return {'message': 'Customer added', 'status': str(conf)}, 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return {'message': 'An error occurred', 'error': str(e)}, 500

def delete_customer(id):
    try:
        rows_deleted = Customer.query.filter_by(id=id).delete()
        if rows_deleted == 0:
            return {'message': 'No customer found with this id'}, 404

        db.session.commit()
        return {'message': 'deleted'}, 200

    except SQLAlchemyError as e:
        db.session.rollback()
        return {'message': 'An error occurred', 'error': str(e)}, 500

def get_customers():
    try:
        if 'customers' not in inspect(db.engine).get_table_names():
            return {'message': 'An error occurred', 'error': 'The table is not initialized. Please click the "Initialize" button on the main page.'}, 500

        customers = Customer.query.all()
        return customers, 200
    except SQLAlchemyError as e:
        return {'message': 'An error occurred', 'error': str(e)}, 500
       
def get_customers_based_on_params(params):
    try:
        if 'customers' not in inspect(db.engine).get_table_names():
            return {'message': 'An error occurred', 'error': 'The table is not initialized. Please click the "Initialize" button on the main page.'}, 500

        query = Customer.query
        for key, value in params.items():
            if value.strip():
                if key == 'description':
                    query = query.filter(Customer.description.like(f'%{value}%'))
                else:
                    query = query.filter_by(**{key: value})
        
        customers = query.all()
        return customers, 200
    except SQLAlchemyError as e:
        return {'message': 'An error occurred', 'error': str(e)}, 500

def get_mail_list():
    try:
        if 'mailing' not in inspect(db.engine).get_table_names():
            return {'message': 'An error occurred', 'error': 'The table is not initialized. Please click the "Initialize" button on the main page.'}, 500

        customers = Mailing.query.all()
        return customers, 200
    except SQLAlchemyError as e:
        return {'message': 'An error occurred', 'error': str(e)}, 500

def send_promo_email(salesman, data):
    try:
        if 'mailing' not in inspect(db.engine).get_table_names():
            return {'message': 'An error occurred', 'error': 'The table is not initialized. Please click the "Initialize" button on the main page.'}, 500
        customers = Mailing.query.all()
        for customer in customers:
            conf = send_email(customer.email, "mailing", salesman, data['emailBody'], data['emailSubject'])
        #return {'message': 'Promo emails sent', 'status': str(conf)}, 200
    except SQLAlchemyError as e:
        # return {'message': 'An error occurred', 'error': str(e)}, 500
        pass

def delete_mail_promo(id):
    try:
        rows_deleted = Mailing.query.filter_by(id=id).delete()
        if rows_deleted == 0:
            return {'message': 'No customer found with this id'}, 404

        db.session.commit()
        return {'message': 'deleted'}, 200

    except SQLAlchemyError as e:
        db.session.rollback()
        return {'message': 'An error occurred', 'error': str(e)}, 500

def add_notification(user, title, message):
    try:
        if 'notifications' not in inspect(db.engine).get_table_names():
            return {'message': 'An error occurred', 'error': 'The table is not initialized. Please click the "Initialize" button on the main page.'}, 500
        new_notification = Notifications(user=user, title=title, notification=message)
        db.session.add(new_notification)
        db.session.commit()
        return {'message': 'Notification added'}, 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return {'message': 'An error occurred', 'error': str(e)}, 500

def get_notifications(user_):
    try:
        if 'notifications' not in inspect(db.engine).get_table_names():
            return {'message': 'An error occurred', 'error': 'The table is not initialized. Please click the "Initialize" button on the main page.'}, 500
        query = Notifications.query
        notifications = query.filter_by(user=user_).all()
        return notifications, 200
    except SQLAlchemyError as e:
        return {'message': 'An error occurred', 'error': str(e)}, 500

def delete_notification(user):
    try:
        rows_deleted = Notifications.query.filter_by(user=user).delete()
        if rows_deleted == 0:
            return {'message': 'No notifications found for this user'}, 404

        db.session.commit()
        return {'message': 'deleted'}, 200

    except SQLAlchemyError as e:
        db.session.rollback() 
        return {'message': 'An error occurred', 'error': str(e)}, 500

def add_job(data):
    try:
        contract_number = data.contract_number.data
        salesman = data.salesman.data
        customer = data.customer.data
        address = data.address.data
        city = data.city.data
        phone = data.phone.data
        description = data.description.data
        date = data.date.data
        email = data.email.data
        selling_price = data.selling_price.data
        cost = data.cost.data
        installer = data.installer.data
        status = data.status.data
        notes = data.notes.data

        new_job = Jobs(
            contract_number=contract_number,
            salesman=salesman,
            customer=customer,
            address=address,
            city=city,
            phone=phone,
            description=description,
            date=date,
            email=email,
            selling_price=selling_price,
            cost=cost,
            installer=installer,
            status=status,
            notes=notes
        )
        db.session.add(new_job)
        db.session.commit()
        return {'message': 'Job added'}, 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return {'message': 'An error occurred', 'error': str(e)}, 500

def filter_job_salesman(data):
    try:
        jobs = Jobs.query.filter_by(salesman=data.salesman).all()
        return jobs, 200
    except SQLAlchemyError as e:
        return {'message': 'An error occurred', 'error': str(e)}, 500

def get_jobs(salesman, admin):
    try:
        if 'jobs' not in inspect(db.engine).get_table_names():
            return {'message': 'An error occurred', 'error': 'The table is not initialized. Please click the "Initialize" button on the main page.'}, 500
        if admin:
            jobs = Jobs.query.all()
            return jobs, 200
        jobs = Jobs.query.filter_by(salesman=salesman).all()
        return jobs, 200
    except SQLAlchemyError as e:
        return {'message': 'An error occurred', 'error': str(e)}, 500

def edit_job(data, id_):
    try:
        job = Jobs.query.get(id_)
        job.phone = data.phone.data
        job.description = data.description.data
        job.date = data.date.data
        job.email = data.email.data
        job.selling_price = data.selling_price.data
        job.cost = data.cost.data
        job.installer = data.installer.data
        job.status = data.status.data
        job.notes = data.notes.data
        db.session.commit()
        return {'message': 'Job edited'}, 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return {'message': 'An error occurred', 'error': str(e)}, 500

def delete_job(id, send_exit_email, email=None):
    conf = None
    if send_exit_email and email:
        conf = send_email(email, 'exit')
    job = Jobs.query.get(id)
    customer_ = Customer(
        contract_number=job.contract_number,
        salesman=job.salesman,
        name=job.customer,
        address=job.address,
        city=job.city,
        phone=job.phone,
        description=job.description,
        date=job.date,
        email=job.email
    )
    db.session.add(customer_)
    try:
        rows_deleted = Jobs.query.filter_by(id=id).delete()
        if rows_deleted == 0:
            return {'message': 'No job found with this id'}, 404

        db.session.commit()
        return {'message': 'deleted', 'email': str(conf)}, 200

    except SQLAlchemyError as e:
        db.session.rollback()
        return {'message': 'An error occurred', 'error': str(e), 'email': str(conf)}, 500

def send_quote_email(data, notes):
    quote = Quote(
        job_title=data.job_title.data,
        job_description=data.job_description.data,
        quote_amount=data.quote_amount.data,
        customer_name=data.customer_name.data,
        customer_address=data.customer_address.data,
        customer_email=data.customer_email.data,
        customer_phone=data.customer_phone.data,
        your_email=data.your_email.data,
        your_phone=data.your_phone.data,
        notes=data.notes.data
    )
    db.session.add(quote)
    db.session.commit()
    conf = send_email(quote.customer_email, 'quote', data=quote, notes=notes)
    if conf.__class__.__name__ == 'ApiException':
        return {'message': 'Quote sent', 'email': str(conf)}, 200
    return {'status': str(conf)}, 404

def get_quotes():
    try:
        if 'quotes' not in inspect(db.engine).get_table_names():
            return {'message': 'An error occurred', 'error': 'The table is not initialized. Please click the "Initialize" button on the main page.'}, 500

        quotes = Quote.query.all()
        return quotes, 200
    except SQLAlchemyError as e:
        return {'message': 'An error occurred', 'error': str(e)}, 500

def delete_quote(id):
    try:
        rows_deleted = Quote.query.filter_by(id=id).delete()
        if rows_deleted == 0:
            return {'message': 'No quote found with this id'}, 404

        db.session.commit()
        return {'message': 'deleted'}, 200

    except SQLAlchemyError as e:
        db.session.rollback()
        return {'message': 'An error occurred', 'error': str(e)}, 500

def resend_quote_email(id):
    try:
        quote = Quote.query.get(id)
        notes = quote.notes.split('<>')
        conf = send_email(quote.customer_email, 'quote', data=quote, notes=notes)
        return {'message': 'Quote sent', 'email': str(conf)}, 200
    except SQLAlchemyError as e:
        return {'message': 'An error occurred', 'error': str(e)}, 500
    

def upload_spreadsheet_single(file):
    # This method uploads a single xls/xlsx file from the spreadsheet.gary page
    try:
        if file and (file.filename.endswith(".xls") or file.filename.endswith(".xlsx")):
            file.seek(0)
            stream = BytesIO(file.read())

            salesman = file.filename.split('.')[0]
            # read the file
            wb = load_workbook(stream, read_only=True)
            for sheet_name in wb.sheetnames:
                sheet = wb[sheet_name]
                df = pd.DataFrame(sheet.values)
                header_row = df.iloc[0]
                
                # Iterate over the rows in DataFrame and add each as a new Customer
                for index, row in df.iterrows():
                    try:
                        if (row == header_row).all():
                            continue  
                        if row.isnull().all():
                            continue 

                        contract_number = str(row.iloc[0])[:64] if len(row) > 0 else None
                        name = str(row.iloc[1])[:64] if len(row) > 1 else None
                        address = str(row.iloc[2])[:120] if len(row) > 2 else None
                        city = str(row.iloc[3])[:64] if len(row) > 3 else None
                        phone = str(row.iloc[4])[:20] if len(row) > 4 else None
                        description = str(row.iloc[5])[:120] if len(row) > 5 else None
                        date = str(row.iloc[6])[:30] if len(row) > 6 else None
                        email = str(row.iloc[7])[:64] if len(row) > 7 and row.iloc[7] else 'NONE'

                        customer = Customer(
                            contract_number=contract_number,    
                            salesman=salesman,                       
                            name=name,               
                            address=address,           
                            city=city,               
                            phone=phone,              
                            description=description,       
                            date=date,                
                            email=email
                        )

                        db.session.add(customer)
                    except Exception as e:
                        print(e)
                        pass

            db.session.commit()
            print("A new sheet was added to the database")
    except Exception as e:
        print("An error occurred while processing the file: ", e)

def upload_spreadsheets_dump():
    # This method dumps all xls/xlsx files in the app/spreadsheets folder
    directory = 'app/spreadsheets'
    for filename in os.listdir(directory):
        if file and (file.filename.endswith(".xls") or file.filename.endswith(".xlsx")):
            # File is an in-memory file object, need to convert it to an in-memory bytes stream object.
            file.seek(0)
            stream = BytesIO(file.read())

            salesman = file.filename.split('.')[0]
            # read the file
            wb = load_workbook(stream, read_only=True)
            for sheet_name in wb.sheetnames:
                sheet = wb[sheet_name]
                df = pd.DataFrame(sheet.values)
                header_row = df.iloc[0]
                
                # Iterate over the rows in DataFrame and add each as a new Customer
                for index, row in df.iterrows():
                    try:
                        if (row == header_row).all():
                            continue  # Skip this row and move to the next one
                        if row.isnull().all():
                            continue  # Skip this row and move to the next one

                        contract_number = str(row.iloc[0])[:64] if len(row) > 0 else None
                        name = str(row.iloc[1])[:64] if len(row) > 1 else None
                        address = str(row.iloc[2])[:120] if len(row) > 2 else None
                        city = str(row.iloc[3])[:64] if len(row) > 3 else None
                        phone = str(row.iloc[4])[:20] if len(row) > 4 else None
                        description = str(row.iloc[5])[:120] if len(row) > 5 else None
                        date = str(row.iloc[6])[:30] if len(row) > 6 else None
                        email = str(row.iloc[7])[:64] if len(row) > 7 and row.iloc[7] else 'NONE'

                        customer = Customer(
                            contract_number=contract_number,    
                            salesman=salesman,                       
                            name=name,               
                            address=address,           
                            city=city,               
                            phone=phone,              
                            description=description,       
                            date=date,                
                            email=email
                        )

                        db.session.add(customer)
                    except Exception as e:
                        print(e)
                        pass
            db.session.commit()
        os.remove(file_path)

def check_health():
    db_status = 'connected'
    code = "NONE"
    try:
        with db.engine.connect() as connection:
            connection.execute(text('SELECT 1'))
    except Exception as e:
        db_status = 'disconnected'
        code = "DB ERROR CODE: " + str(e)
    return {
        'status': 'online',
        'database': db_status,
        'code': code
    }

def logout():
    logout_user()
