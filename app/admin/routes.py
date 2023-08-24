from flask import (
    current_app, 
    render_template, 
    request, 
    redirect, 
    url_for, 
    send_from_directory, 
    jsonify, 
    flash,
    make_response
)
from flask_login import login_required, current_user
from werkzeug.wrappers import Response
from http import HTTPStatus
from app import executor
from . import bp
from .controllers import (
    insert_into_promo_list, 
    get_customers, 
    get_customers_based_on_params,
    add_customer, 
    create_table, 
    delete_table, 
    upload_spreadsheet_single,
    check_health, 
    delete_customer, 
    get_mail_list, 
    send_promo_email, 
    add_notification, 
    get_notifications, 
    delete_notification, 
    delete_mail_promo,
    get_jobs,
    add_job,
    get_the_latest_job,
    edit_job,
    delete_job,
    send_quote_email,
    get_quotes,
    delete_quote,
    resend_quote_email,
    build_service_list,
    get_sales_scoreboard,
    check_if_siib_key_works,
    logout
)
from .service import get_jobs_scheduler
from .models import (
    CustomerForm,
    JobForm,
    QuoteForm,
    PromoForm
)
from typing import Any, Tuple, Dict, List
import io, csv, locale


@bp.route('/static/<path:filename>')
@login_required
def admin_static(filename):
    """
    Static route handler function.
    This function serves static files from the static admin directory.
    """
    return send_from_directory('tpl/admin/assets', filename)

def handle_error(error: Exception) -> str:
    """
    Handle errors in a more detailed way.
    This function takes an exception as input and return an error message to the client.
    """
    # Handle the error as appropriate for your application.
    # This is just a placeholder.
    return str(error)

def render_admin_template(services: List[Dict[str, Any]], username: str, email: str, notifications: List[Dict[str, Any]], 
                          notification_count: int, scoreboard_users: List[Dict[str, Any]], the_7_day_score: List[Dict[str, Any]], job: Dict[str, Any]) -> str:
    """
    This function takes in various parameters required by the template and renders the template.
    """
    return render_template(
        'admin/views/admin.gary', 
        company_name=current_app.config['NAME'], 
        salesman_options=current_app.config['SALESMAN_OPTIONS'], 
        user=username, 
        email=email, 
        notifications=notifications, 
        notification_count=notification_count, 
        is_admin=current_user.admin, 
        services=services, 
        scoreboard=scoreboard_users, 
        the_7_day_score=the_7_day_score,
        job = job,
        technical_support=current_app.config['SUPPORT_EMAIL'], 
        config=current_app.config,
        pwa_config_is_enabled = current_app.config['PWA']
    )

@bp.route('/')
@login_required
def admin_route() -> str:
    """
    Admin route handler function.
    This function builds service list, retrieves user information, notifications, and scoreboard data, 
    then returns a rendered template with these data.
    """
    services = build_service_list(current_app.config['SERVICES'])           
    username = current_user.id[0].upper() + current_user.id[1:]
    email = f"{current_user.id}{current_app.config['EMAIL_HYPERLINK']}"

    notifications, status_code = get_notifications(current_user.id)

    if status_code != HTTPStatus.OK:
        flash(f"Error: {notifications}")
        notifications = []

    notification_count = len(notifications)
    
    scoreboard_users, the_7_day_score = get_sales_scoreboard(current_app.config['LEADER_BOARD_USERS'])
    
    job, status_code = get_the_latest_job()

    if status_code != HTTPStatus.OK:
        flash(f"Error: {job}")
        job = None

    if notification_count == 0:
        notifications = [{"title": "No Notifications", "notification": "You have no notifications at this time."}]

    if check_if_siib_key_works(current_app.config['SIB_API_KEY']) == False:
        notifications.append({"title": "SIIB Key Error", "notification": "SIIB key is not working. Please check."})
        notification_count += 1

    return render_admin_template(
        services=services, 
        username=username, 
        email=email, 
        notifications=notifications, 
        notification_count=notification_count, 
        scoreboard_users=scoreboard_users,
        the_7_day_score=the_7_day_score,
        job=job
    )

@bp.route('/docs', methods=['GET'])
@login_required
def docs_route() -> str:
    """
    Docs route handler function.
    This function renders the docs template.
    """
    return render_template('admin/views/docs.gary')


@bp.route('/add_customer', methods=['POST'])
@login_required
def add_customer_route() -> Response:
    """
    Add customer route handler function.
    This function adds a new customer based on form data and redirects to admin route.
    """
    form = CustomerForm(request.form)
    welcome = 'sendEmail' in request.form
    mailList = 'mailList' in request.form
    response, status_code = add_customer(form, welcome, mailList)
    if status_code != HTTPStatus.OK:
        flash(f"Error: {response}")
    else:
        flash(f"Customer {form.name.data} added successfully.")
    return redirect(url_for('admin.admin_route'))

@bp.route('/delete_customer/<int:id>', methods=['POST'])
@login_required
def delete_customer_route(id: int) -> Tuple[Any, int]:
    """
    Delete customer route handler function.
    This function deletes a customer based on the given id.
    """
    response, status_code = delete_customer(id)
    if status_code != HTTPStatus.OK:
        flash(f"Customer {id} deleted successfully.")
    return jsonify(response), status_code

@bp.route('/create_table', methods=['POST'])
@login_required
def create_table_route() -> Any:
    """
    Create table route handler function.
    This function creates a new table and returns a response.
    """
    response, status_code = create_table()
    if status_code == HTTPStatus.OK:
        return render_template('admin/views/redirect.gary', response=response, redirect="/admin")
    return jsonify(response), status_code

@bp.route('/all_customers', methods=['GET'])
@login_required
def customers() -> Any:
    """
    All customers route handler function.
    This function gets all customers and returns a response.
    """
    response, status_code = get_customers()
    if status_code == HTTPStatus.OK:
        return render_template('admin/views/customers.gary', customers=response)
    return jsonify(response), status_code

@bp.route('/custom_table', methods=['GET'])
@login_required
def single_table() -> Any:
    """
    Custom table route handler function.
    This function gets customers based on params and returns a response.
    """
    response = None
    if request.args:
        response, status_code = get_customers_based_on_params(request.args)
        if status_code == HTTPStatus.OK:
            return render_template('admin/views/single.gary', customers=response)
    return jsonify(response), status_code
 
@bp.route('/sms_promotion', methods=['GET'])
@login_required
def deploy_sms_promo() -> str:
    """
    SMS promotion route handler function.
    """
    # not implemented yet
    return render_template('admin/views/sms.gary')

@bp.route('/send_sms_promotion_main', methods=['POST'])
@login_required
def send_sms_promotion_main() -> str:
    """
    Send SMS promotion route handler function.
    """
    return render_template('admin/views/redirect.gary', response="Under construction.", redirect="/admin")

@bp.route('/email_promotion', methods=['GET'])
@login_required
def email_promo_main() -> Any:
    """
    Email promotion route handler function.
    """
    mailing_list, err_code = get_mail_list()
    if err_code != HTTPStatus.OK:
        return jsonify({'error': 'please initialize the database tables.'}), HTTPStatus.INTERNAL_SERVER_ERROR
    return render_template('admin/views/email.gary', salesman_options=current_app.config['SALESMAN_OPTIONS'], maillist=mailing_list)

@bp.route('/add_mail_promo_user', methods=['POST'])
@login_required
def add_mail_promo_user() -> str:
    """
    Add mail promo user route handler function.
    """
    promo = PromoForm(request.form)
    response, status_code = insert_into_promo_list(promo)
    if status_code != HTTPStatus.OK:
        flash(f"Customer {promo.customer.data} added successfully.")
    return render_template('admin/views/redirect.gary', response=response, redirect="/admin/email_promotion")

@bp.route('/send_email_promotion_main', methods=['POST'])
@login_required
def send_email_promotion_main() -> str:
    """
    Send email promotion route handler function.
    """
    executor.submit(send_promo_email, "Promo", request.form)
    #TODO: need to check errors.
    resp = {"promo": "Emails are being sent."}
    return render_template('admin/views/redirect.gary', response=resp, redirect="/admin")

@bp.route('/delete_mail_promo_user/<int:id>', methods=['POST'])
@login_required
def delete_mail_promo_user(id: int) -> Tuple[Any, int]:
    """
    Delete mail promo user route handler function.
    """
    response, status_code = delete_mail_promo(id)
    flash(f"Customer {id} deleted successfully.") if status_code == HTTPStatus.OK else None
    return jsonify(response), status_code

@bp.route('/add_notifications', methods=['GET'])
@login_required
def add_notifications() -> str:
    """
    Add notifications route handler function.
    """
    return render_template('admin/views/notifications.gary', salesman_options=current_app.config['SALESMAN_OPTIONS'])

@bp.route('/send_custom_notification', methods=['POST'])
@login_required
def send_custom_notification() -> str:
    """
    Send custom notification route handler function.
    """
    title = request.form['noteTitle']
    message = request.form['noteBody']
    user = request.form['salesman']
    addNote, err = add_notification(user, title, message)
    if err != HTTPStatus.OK:
        return jsonify({'error': addNote}), HTTPStatus.INTERNAL_SERVER_ERROR
    return render_template('admin/views/redirect.gary', response=addNote, redirect="/admin")

@bp.route('/delete_notification', methods=['POST'])
@login_required
def delete_notification_route() -> str:
    """
    Delete notification route handler function.
    """
    user = current_user.id
    response, status_code = delete_notification(user)
    return render_template('admin/views/redirect.gary', response=response, err_code=status_code, redirect="/admin")

@bp.route('/delete_table', methods=['POST'])
@login_required
def delete_table_route() -> str:
    """
    Delete table route handler function.
    """
    response, status_code = delete_table(request.headers)
    return render_template('admin/views/redirect.gary', response=response, err_code=status_code, redirect="/admin")

@bp.route('/upload_spreadsheets', methods=['GET'])
@login_required
def upload_spreadsheets_route() -> str:
    """
    Upload spreadsheets route handler function.
    """
    return render_template('admin/views/spreadsheets.gary')

@bp.route('/upload_spreadsheets_single', methods=['POST'])
@login_required
def upload_spreadsheets_single_route() -> str:
    """
    Upload single spreadsheet route handler function.
    """
    file = request.files['spreadsheetFile']
    executor.submit(upload_spreadsheet_single, file)
    return render_template('admin/views/redirect.gary', response="Processing spreadsheet.", redirect="/admin")

@bp.route('/job_board', methods=['GET'])
@login_required
def job_board_route() -> str:
    """
    Job board route handler function.
    """
    salesman = current_user.id[0].upper() + current_user.id[1:]
    is_admin = current_user.admin
    mode = 'admin' if is_admin else 'user'
    primary_jobs, status_code = get_jobs(salesman, is_admin)
    return render_template('admin/views/job.gary', salesman=salesman, salesman_options=current_app.config['SALESMAN_OPTIONS'], mode=mode, jobs=primary_jobs)

@bp.route('/add_job', methods=['POST'])
@login_required
def add_job_route() -> str:
    """
    Add job route handler function.
    """
    form = JobForm(request.form)
    msg, status_code = add_job(form)
    return render_template('admin/views/redirect.gary', response=msg, redirect="/admin/job_board")

@bp.route('/edit_job', methods=['POST'])
@login_required
def edit_job_route() -> str:
    """
    Edit job route handler function.
    """
    _id = request.form['id']
    form = JobForm(request.form)
    msg, status_code = edit_job(form, _id)
    return render_template('admin/views/redirect.gary', response=msg, redirect="/admin/job_board")

@bp.route('/delete_job', methods=['POST'])
@login_required
def delete_job_route() -> str:
    """
    Delete job route handler function.
    """
    customer_id = request.form['id']
    email = request.form['email']
    send_exit_email = 'exitEmail' in request.form
    msg, status_code = delete_job(customer_id, send_exit_email, email)
    return render_template('admin/views/redirect.gary', response=msg, redirect="/admin/job_board")

@bp.route('/send_job_updates', methods=['POST'])
@login_required
def send_job_updates_route() -> str:
    """
    Send job updates route handler function.
    """
    if not current_user.admin:
        return render_template('admin/views/redirect.gary', response="You must be an admin to send job updates.", redirect="/admin/job_board")
    get_jobs_scheduler()
    return render_template('admin/views/redirect.gary', response="Job updates are being sent.", redirect="/admin/job_board")

@bp.route('/download_jobs', methods=['GET'])
@login_required
def download_jobs_route() -> Tuple[Any, int]:
    """
    Download jobs route handler function.
    """
    salesman = current_user.id[0].upper() + current_user.id[1:]
    jobs, status_code = get_jobs(salesman, current_user.admin)
    if status_code != HTTPStatus.OK:
        return {"error": "Error getting jobs."}, HTTPStatus.INTERNAL_SERVER_ERROR

    si = io.StringIO()
    cw = csv.writer(si)
    cw.writerow(jobs[0].serialize().keys()) 
    for job in jobs:
        cw.writerow(job.serialize().values())
        
    output = make_response(si.getvalue())
    output.headers["Content-Disposition"] = "attachment; filename=jobs.csv"
    output.headers["Content-type"] = "text/csv"

    return output

@bp.route('/quoting_tool', methods=['GET'])
@login_required
def quoting_tool() -> str:
    """
    Render the quoting tool.
    """
    return render_template('admin/views/quote.gary')

@bp.route('/quoting_tool_route', methods=['POST'])
@login_required
def quoting_tool_route() -> str:
    """
    Handle the quote form submission and send the quote via email.
    """
    form_data = request.form
    form = QuoteForm()

    # Breakdown form and get data seperately
    form.job_title.data = form_data.get('jobTitle')
    form.job_description.data = form_data.get('jobDescription')
    form.quote_amount.data = form_data.get('quoteAmount')
    # TODO: Fix this
    # if form.quote_amount.data is not None:
    #     locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
    #     form.quote_amount.data = str(locale.currency(float(form.quote_amount.data), grouping=True))
    form.customer_name.data = form_data.get('customerName')
    form.customer_address.data = form_data.get('customerAddress')
    form.customer_email.data = form_data.get('customerEmail')
    form.customer_phone.data = form_data.get('customerPhone')
    form.your_email.data = form_data.get('yourEmail')
    form.your_phone.data = form_data.get('yourPhone')

    # Combine notes into one field
    noteBox = [form_data[key] for key in form_data if 'note' in key.lower()]
    form.notes.data = "<>".join(noteBox)

    msg, status_code = send_quote_email(form, noteBox)
    return render_template('admin/views/redirect.gary', response=msg, redirect="/admin")

@bp.route('/get_quotes', methods=['GET'])
@login_required
def get_quote_list() -> str:
    """
    Get the list of all quotes.
    """
    quote_list, status_code = get_quotes()
    for quote in quote_list:
        quote.notes = "".join(f'<p class="delv-list-item">* {note}</p>' for note in quote.notes.split("<>"))
    if status_code != HTTPStatus.OK:
        return render_template('admin/views/redirect.gary', response=quote_list, redirect="/admin")
    return render_template('admin/views/quotes.gary', quotes=quote_list, is_admin=current_user.admin)

@bp.route('/delete_quote/<int:id>', methods=['POST'])
@login_required
def delete_quote_route(id: int) -> str:
    """
    Delete a specific quote by id.
    """
    response, status_code = delete_quote(id)
    if status_code != HTTPStatus.OK:
        return render_template('admin/views/redirect.gary', response=response, redirect="/admin")
    return jsonify(response)

@bp.route('/resend_quote/<int:id>', methods=['POST'])
@login_required
def resend_quote_route(id: int) -> str:
    """
    Resend a specific quote by id.
    """
    response, status_code = resend_quote_email(id)
    return render_template('admin/views/redirect.gary', response=response, redirect="/admin")

@bp.route('/health', methods=['GET'])
@login_required
def health() -> str:
    """
    Check the health of the server.
    """
    get_health = check_health()
    return render_template('admin/views/redirect.gary', response=get_health, redirect="/admin")

@bp.route("/logout")
@login_required
def logout_route() -> Response:
    """
    Logout route handler function.
    Logs out the current user and redirects to home route.
    """
    logout()
    return redirect(url_for('user.home_route'))
