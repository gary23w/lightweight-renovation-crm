## Endpoint Documentation

# LOGIN

### GET /

This is the primary endpoint of the application which serves the login page.

**Request parameters**: None.

**Response**: Login page.

**Errors**: None.

---

### POST /

This endpoint handles the login requests. Upon successful login, the user is redirected to the admin dashboard.

**Request parameters**:

- `u`: Username of the user.
- `p`: Password of the user.

**Response**: Redirects to `/admin` upon successful login, serves the login page with error message upon unsuccessful login.

**Errors**:

- 400: Bad Request - In case of invalid username or password.

---

After a successful login, the user will need to save the `cookies.gary` file to maintain their session. This cookie is used for authentication for the subsequent requests.

**_EXAMPLE_**

```
curl -c cookies.gary -d "u=username&p=password" http://localhost:5000/
```

### GET /admin

This endpoint provides the admin dashboard. This endpoint is authenticated, meaning you need to be logged in as an admin to access it.

### POST /admin/logout

This endpoint logs out the current user. This endpoint is authenticated.

### POST /admin/add_customer

This endpoint adds a new customer. This endpoint is authenticated and requires a form body with details about the customer. It will flash a message about the operation's success or failure and redirect to the admin dashboard.

### POST /admin/delete_customer/<int:id>

This endpoint deletes a customer specified by the id. This endpoint is authenticated and will return a JSON response with details about the operation's success or failure.

### POST /admin/create_table

This endpoint creates a new table in the database. This endpoint is authenticated and returns a JSON response with details about the operation's success or failure.

### GET /admin/all_customers

This endpoint retrieves all customers. This endpoint is authenticated and returns a JSON response with the list of customers or an error message.

### GET /admin/custom_table

This endpoint retrieves a custom table of customers based on passed parameters. This endpoint is authenticated and returns a JSON response with the custom list of customers or an error message.

### POST /admin/delete_table

This endpoint deletes a table in the database. This endpoint is authenticated and returns a response indicating the success or failure of the operation.

### POST /admin/upload_spreadsheets_single

This endpoint allows for a single spreadsheet upload. This endpoint is authenticated and will process the uploaded spreadsheet file asynchronously.

### POST /admin/add_job

This endpoint adds a new job. This endpoint is authenticated and requires a form body with details about the job. It will return a message about the operation's success or failure.

### POST /admin/edit_job

This endpoint edits an existing job. This endpoint is authenticated and requires a form body with details about the updated job. It will return a message about the operation's success or failure.

### POST /admin/delete_job

This endpoint deletes a job specified by the id. This endpoint is authenticated and requires a form body. It will return a message about the operation's success or failure.

### GET /admin/download_jobs

This endpoint allows for the downloading of jobs data in CSV format. This endpoint is authenticated and will return a CSV file.

### POST /admin/quoting_tool_route

This endpoint sends a quote email. This endpoint is authenticated and requires a form body with details about the quote. It will return a message about the operation's success or failure.

### GET /admin/get_quotes

This endpoint retrieves all quotes. This endpoint is authenticated and returns a list of quotes or an error message.

### POST /admin/delete_quote/<int:id>

This endpoint deletes a quote specified by the id. This endpoint is authenticated and will return a JSON response with details about the operation's success or failure.

### POST /admin/resend_quote/<int:id>

This endpoint resends a quote email for a quote specified by the id. This endpoint is authenticated and will return a message about the operation's success or failure.

### GET /admin/health

This endpoint provides a health check for the application. This endpoint is authenticated and will return a response indicating the application's health status.
