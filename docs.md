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

---

### GET `/admin`

#### Description

This endpoint provides the admin dashboard.

#### Authentication

This endpoint is authenticated; you need to be logged in as an admin to access it.

#### Responses

- **200 OK**: Successfully renders the admin dashboard.
- **401 Unauthorized**: User is not authenticated or is not an admin.

---

## Python Method Documentation

### `render_admin_template`

#### Description

This function takes in various parameters required by the admin template and renders the template.

#### Parameters

- **services** (`List[Dict[str, Any]]`): A list of dictionaries containing service-related information.
- **username** (`str`): The username of the admin.
- **email** (`str`): The email address of the admin.
- **notifications** (`List[Dict[str, Any]]`): A list of dictionaries containing notification details.
- **notification_count** (`int`): The total number of notifications.
- **scoreboard_users** (`List[Dict[str, Any]]`): A list of dictionaries containing user scores.
- **the_7_day_score** (`List[Dict[str, Any]]`): A list of dictionaries containing the 7-day scoreboard.
- **job** (`Dict[str, Any]`): A dictionary containing the latest job details.

#### Returns

- **str**: The rendered HTML template for the admin dashboard.

---

### `admin_route`

#### Description

Admin route handler function. This function builds the service list, retrieves user information, notifications, and scoreboard data, then returns a rendered template with these data.

#### Parameters

- None.

#### Returns

- **str**: The rendered HTML template for the admin dashboard.

#### Side Effects

- May show a flash message for errors related to notifications or the latest job.

### POST `/admin/logout`

#### Description

This endpoint logs out the current user.

#### Authentication

This endpoint is authenticated; you need to be logged in to access it.

#### Responses

- **302 Redirect**: Redirects to the home route after successful logout.
- **401 Unauthorized**: User is not authenticated.

---

## Python Method Documentation

### `logout_route`

#### Description

Logout route handler function. Logs out the current user and redirects to the home route.

#### Parameters

- None.

#### Returns

- **Response**: A Flask Response object, redirecting the user to the home route.

#### Side Effects

- Logs out the current user.

---

### POST `/admin/add_customer`

#### Description

This endpoint adds a new customer.

#### Authentication

This endpoint is authenticated; you need to be logged in as an admin to access it.

#### Request Body

- **Form Data**: Requires a form body with details about the customer.

#### Responses

- **302 Redirect**: Redirects to the admin dashboard with a flash message about the operation's success or failure.
- **400 Bad Request**: Invalid or incomplete form data.
- **401 Unauthorized**: User is not authenticated.

---

## Python Method Documentation

### `add_customer_route`

#### Description

Add customer route handler function. This function adds a new customer based on form data and redirects to the admin route.

#### Parameters

- **Form Data**: Uses a Flask `request.form` object to capture the customer's details. Includes optional flags for sending a welcome email (`sendEmail`) and adding to a mailing list (`mailList`).

#### Returns

- **Response**: A Flask Response object, redirecting the user to the admin dashboard.

#### Side Effects

- May show a flash message for errors related to adding the customer or for successful addition.
- If the `sendEmail` flag is set, sends a welcome email to the new customer.
- If the `mailList` flag is set, adds the new customer to a mailing list.

---

### POST `/admin/delete_customer/<int:id>`

#### Description

This endpoint deletes a customer specified by the id.

#### Authentication

This endpoint is authenticated; you need to be logged in as an admin to access it.

#### URL Parameters

- **id** (`int`): The ID of the customer to be deleted.

#### Responses

- **200 OK**: JSON response with details about the operation's success.
- **400 Bad Request**: JSON response with details about the operation's failure.
- **401 Unauthorized**: User is not authenticated.

---

## Python Method Documentation

### `delete_customer_route`

#### Description

Delete customer route handler function. This function deletes a customer based on the given id.

#### Parameters

- **id** (`int`): The ID of the customer to be deleted.

#### Returns

- **Tuple[Any, int]**: A tuple containing a JSON-serializable response and the HTTP status code.

#### Side Effects

- May show a flash message for the successful deletion of the customer.

---

### POST `/admin/create_table`

#### Description

This endpoint creates a new table in the database.

#### Authentication

This endpoint is authenticated; you need to be logged in as an admin to access it.

#### Responses

- **200 OK**: Renders a template that will redirect to the admin dashboard, and includes details about the operation's success.
- **400 Bad Request**: JSON response with details about the operation's failure.
- **401 Unauthorized**: User is not authenticated.

---

## Python Method Documentation

### `create_table_route`

#### Description

Create table route handler function. This function creates a new table and returns a response.

#### Parameters

- None.

#### Returns

- **Any**: Either renders a template with a redirect to the admin dashboard, or returns a JSON-serializable response and the HTTP status code.

#### Side Effects

- Creates a new table in the database if the operation is successful.

---

### GET `/admin/all_customers`

#### Description

This endpoint retrieves all customers from the database.

#### Authentication

This endpoint is authenticated; you need to be logged in as an admin to access it.

#### Responses

- **200 OK**: Renders a template that displays the list of all customers.
- **400 Bad Request**: JSON response with an error message.
- **401 Unauthorized**: User is not authenticated.

---

## Python Method Documentation

### `customers`

#### Description

All customers route handler function. This function retrieves all customers and returns a response.

#### Parameters

- None.

#### Returns

- **Any**: Either renders a template that displays the list of all customers, or returns a JSON-serializable response and the HTTP status code.

#### Side Effects

- Retrieves all customers from the database.

---

### GET `/admin/custom_table`

#### Description

This endpoint retrieves a custom table of customers based on passed query parameters.

#### Authentication

This endpoint is authenticated; you need to be logged in as an admin to access it.

#### URL Parameters

- Query parameters to filter customers (optional).

#### Responses

- **200 OK**: Renders a template that displays the custom list of customers based on the query parameters.
- **400 Bad Request**: JSON response with an error message.
- **401 Unauthorized**: User is not authenticated.

---

## Python Method Documentation

### `single_table`

#### Description

Custom table route handler function. This function retrieves customers based on query parameters and returns a response.

#### Parameters

- **Query Parameters**: Optional query parameters to filter customers.

#### Returns

- **Any**: Either renders a template that displays the custom list of customers or returns a JSON-serializable response and the HTTP status code.

#### Side Effects

- Retrieves a custom list of customers based on query parameters from the database.

---

### POST `/admin/delete_table`

#### Description

This endpoint deletes a table in the database.

#### Authentication

This endpoint is authenticated; you need to be logged in as an admin to access it.

```
Authorization = headers.get('Authorization')
    if Authorization == "Basic superlfadmin:removemydata": # Consider using an environment variable here
```

#### Headers

- Headers may include information needed to authenticate or specify parameters for table deletion (optional).

#### Responses

- Redirects to the admin dashboard with a response indicating the success or failure of the operation.

---

## Python Method Documentation

### `delete_table_route`

#### Description

Delete table route handler function. This function deletes a table in the database.

#### Parameters

- **Headers**: Optional HTTP headers to specify parameters for table deletion or authentication.

#### Returns

- **str**: Renders a template that redirects to the admin dashboard, and includes a response indicating the success or failure of the operation.

#### Side Effects

- Deletes a table in the database.

---

### POST `/admin/upload_spreadsheets_single`

#### Description

This endpoint allows for a single spreadsheet upload and processes the uploaded file asynchronously.

#### Authentication

This endpoint is authenticated; you need to be logged in as an admin to access it.

#### Form Data

- `spreadsheetFile`: The spreadsheet file to be uploaded.

#### Responses

- Redirects to the admin dashboard with a message indicating that the spreadsheet is being processed.

---

## Python Method Documentation

### `upload_spreadsheets_single_route`

#### Description

Upload single spreadsheet route handler function. This function processes the uploaded spreadsheet file asynchronously.

#### Parameters

- **Form Data**: Contains the `spreadsheetFile` that needs to be uploaded and processed.

#### Returns

- **str**: Renders a template that redirects to the admin dashboard, and includes a message indicating that the spreadsheet is being processed.

#### Side Effects

- Initiates asynchronous processing of the uploaded spreadsheet.

---

### POST `/admin/add_job`

#### Description

This endpoint adds a new job to the job board.

#### Authentication

This endpoint is authenticated; you need to be logged in as an admin to access it.

#### Form Data

- `JobForm`: The form containing details about the job to be added.

#### Responses

- Redirects to the admin job board with a message indicating the success or failure of the operation.

---

## Python Method Documentation

### `add_job_route`

#### Description

Add job route handler function. This function adds a new job based on the submitted form data.

#### Parameters

- **Form Data**: Contains the `JobForm` with details about the job that needs to be added.

#### Returns

- **str**: Renders a template that redirects to the admin job board, and includes a message indicating the success or failure of the operation.

#### Side Effects

- Adds a new job to the job board based on the submitted form data.

---

### POST `/admin/edit_job`

#### Description

This endpoint edits an existing job on the job board.

#### Authentication

This endpoint is authenticated; you need to be logged in as an admin to access it.

#### Form Data

- `JobForm`: The form containing updated details about the job.
- `id`: The ID of the job to be edited.

#### Responses

- Redirects to the admin job board with a message indicating the success or failure of the operation.

---

## Python Method Documentation

### `edit_job_route`

#### Description

Edit job route handler function. This function edits an existing job based on the submitted form data and job ID.

#### Parameters

- **Form Data**: Contains the `JobForm` with updated details about the job that needs to be edited.
- **id**: The ID of the job to be edited.

#### Returns

- **str**: Renders a template that redirects to the admin job board, and includes a message indicating the success or failure of the operation.

#### Side Effects

- Edits an existing job on the job board based on the submitted form data and job ID.

---

### POST `/admin/delete_job`

#### Description

This endpoint deletes a job specified by its ID.

#### Authentication

This endpoint is authenticated; you need to be logged in as an admin to access it.

#### Form Data

- `id`: The ID of the job to be deleted.
- `email`: The email to which an exit email will be sent if specified.
- `exitEmail`: A boolean flag indicating whether or not to send an exit email.

#### Responses

- Redirects to the admin job board with a message indicating the success or failure of the operation.

---

## Python Method Documentation

### `delete_job_route`

#### Description

Delete job route handler function. This function deletes a job specified by its ID and optionally sends an exit email.

#### Parameters

- **id**: The ID of the job to be deleted.
- **email**: The email to which an exit email will be sent if specified.
- **exitEmail**: A boolean flag indicating whether or not to send an exit email.

#### Returns

- **str**: Renders a template that redirects to the admin job board, and includes a message indicating the success or failure of the operation.

#### Side Effects

- Deletes the specified job and optionally sends an exit email.

---

### GET `/admin/download_jobs`

#### Description

This endpoint allows for the downloading of job data in CSV format.

#### Authentication

This endpoint is authenticated; you need to be logged in as an admin or a salesman to access it.

#### Responses

- Returns a CSV file containing the list of jobs for the current user if the request is successful.
- Returns an error with a status code of `500 Internal Server Error` if there was an issue retrieving the jobs.

---

## Python Method Documentation

### `download_jobs_route`

#### Description

Download jobs route handler function. This function allows for the downloading of job data in CSV format.

#### Parameters

- **salesman**: The current user's ID, converted to a readable string format.
- **admin**: A boolean flag to indicate whether the current user is an admin.

#### Returns

- **Tuple[Any, int]**: Returns a CSV file in the HTTP response if the request is successful or an error message with a status code of `500 Internal Server Error` otherwise.

#### Side Effects

- Reads job data and generates a CSV file for download.

---

### POST `/admin/quoting_tool_route`

#### Description

This endpoint sends a quote email based on the details provided in the form body.

#### Authentication

This endpoint is authenticated and requires the user to be logged in to access it.

#### Request Body

- `jobTitle`: The title of the job.
- `jobDescription`: Description of the job.
- `quoteAmount`: Amount to be quoted.
- `customerName`: Name of the customer.
- `customerAddress`: Address of the customer.
- `customerEmail`: Email of the customer.
- `customerPhone`: Phone number of the customer.
- `yourEmail`: Your email address.
- `yourPhone`: Your phone number.
- `note`: Notes regarding the quote. Multiple notes can be provided.

#### Responses

- Returns a message indicating the success or failure of the email sending operation.

---

## Python Method Documentation

### `quoting_tool_route`

#### Description

Handles the quote form submission and sends the quote via email.

#### Parameters

- `form_data`: Dictionary containing the form fields for the quote.

#### Returns

- **str**: A string containing a message indicating the success or failure of the email sending operation.

#### Side Effects

- Sends an email containing the quote details.

#### Notes

- The method breaks down the form data to fill in the `QuoteForm` class attributes.
- Combines multiple note fields into one for the final quote.

---

### GET `/admin/get_quotes`

#### Description

This endpoint retrieves all quotes stored in the system.

#### Authentication

This endpoint is authenticated and requires the user to be logged in to access it.

#### Parameters

None

#### Responses

- Returns a list of quotes if successful.
- Returns an error message if the operation fails.

---

## Python Method Documentation

### `get_quote_list`

#### Description

Retrieves a list of all quotes stored in the system.

#### Parameters

None

#### Returns

- **str**: A string containing the rendered HTML template displaying the list of quotes or a redirect in case of an error.

#### Side Effects

- Formats the `notes` field of each quote for better readability.

#### Notes

- The method formats the notes for each quote, splitting them based on the `<>` separator and then joining them into an HTML paragraph format.
- Renders the list of quotes in a template and passes the `is_admin` flag to indicate admin access.

---

### POST `/admin/delete_quote/<int:id>`

#### Description

This endpoint deletes a specific quote identified by the given `id`.

#### Authentication

This endpoint is authenticated and requires the user to be logged in to access it.

#### Parameters

- **id**: Integer specifying the ID of the quote to be deleted.

#### Responses

- Returns a JSON response detailing the outcome of the operation if successful.
- Returns an error message and redirects to the admin dashboard if the operation fails.

---

## Python Method Documentation

### `delete_quote_route(id: int) -> str`

#### Description

Deletes a specific quote identified by the given `id`.

#### Parameters

- **id**: Integer specifying the ID of the quote to be deleted.

#### Returns

- **str**: A string containing either a JSON response detailing the outcome of the deletion operation or a rendered HTML template for redirection in case of failure.

#### Side Effects

None.

#### Notes

- The function calls the `delete_quote` function and checks the `HTTPStatus` to determine the outcome of the operation.

---

### POST `/admin/resend_quote/<int:id>`

#### Description

This endpoint resends an email for a specific quote identified by the given `id`.

#### Authentication

This endpoint is authenticated and requires the user to be logged in to access it.

#### Parameters

- **id**: Integer specifying the ID of the quote for which the email will be resent.

#### Responses

- Returns a message indicating the outcome of the operation and redirects to the admin dashboard.

---

## Python Method Documentation

### `resend_quote_route(id: int) -> str`

#### Description

Resends an email for a specific quote identified by the given `id`.

#### Parameters

- **id**: Integer specifying the ID of the quote for which the email will be resent.

#### Returns

- **str**: A string containing a rendered HTML template for redirection, along with a response message indicating the outcome of the operation.

#### Side Effects

None.

#### Notes

- The function calls the `resend_quote_email` function and uses its response and `HTTPStatus` to determine the outcome of the operation.

---

### GET `/admin/health`

#### Description

This endpoint provides a health check for the application.

#### Authentication

This endpoint is authenticated and requires the user to be logged in to access it.

#### Parameters

None.

#### Responses

- Returns a message indicating the health status of the application and redirects to the admin dashboard.

---

## Python Method Documentation

### `health() -> str`

#### Description

Checks the health status of the server and application.

#### Parameters

None.

#### Returns

- **str**: A string containing a rendered HTML template for redirection, along with a message indicating the health status of the application.

#### Side Effects

None.

#### Notes

- The function calls the `check_health` function to determine the health status of the application.
