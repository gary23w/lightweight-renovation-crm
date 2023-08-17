# LF Builders REST API

<hr />

[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](http://makeapullrequest.com)
[![CircleCI](https://circleci.com/gh/google/pybadges.svg?style=svg)](https://circleci.com/gh/google/pybadges)
![versions](https://img.shields.io/pypi/pyversions/pybadges.svg)

<hr />

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)

Built this during my lunch break a couple of weeks ago. It turned out to be extremely useful, so I thought I would share it!

Ideal lightweight Construction CRM -> Powered by [BREVO](https://www.brevo.com/en)

This is a REST API(with flask templates) designed to streamline and manage construction workloads. This lightweight, mobile-friendly tool is a contractor's best friend, capable of managing customer interactions and database implementation with ease.

**_has a user interface_**.

Built to provide real-time updates, it sends out notification emails, quote emails, and exit emails, keeping you in touch with your workflow at all times. The 'Board' feature allows you to keep track of ongoing jobs, while the 'Service Tool' sends daily job updates to admins. For those handling extensive customer lists, the 'View Customer List' action provides a seamless interface, enabling easy iteration over thousands of past clients. Mailing list? Quickly send out thousands of promotional emails. Filter down customers with the table filter tool and share short links with other users. More tools to come, stay posted!

Key Features:

- Utilizes Brevo (formerly known as SendInBlue) to manage all email interactions.
- The user-friendly interface is developed with Bootstrap and JavaScript (jQuery, DataTables, Moment, FileSaver, xlsx, Popper) to enhance user interaction.
- The endpoints are documented and commented for easy understanding.
- Updates to improve efficiency and functionality.

Would love to collaborate on this with another person.

<ul>
<li>-> possible go or rust version in the near future.</li>
<li>-> ** python prototype.</li>
</ul>

**reach me on Discord: @gary23w**

## Building and Running the API

### Prerequisites

- SendInBlue API Key
- Docker
- Docker Compose

### Configuring app/config.json

Modify the values to align with your conventions.

```
{
  "version": "v1.0.0",
  "name": "Professional Services Inc.",
  "short_name": "Professional Services Inc.",
  "start_url": "/",
  "display": "standalone",
  "background_image_login": "https://probackgrounds.img/login-background.png",
  "logo": "https://prologos.img/logo.png",
  "login_design": {
    "button_background": "#2b8d93",
    "button_background_hover": "#27c0c8",
    "button_text": "LOGIN",
    "card_color_background": "rgba(132, 208, 212, 0.9)",
    "card_border_color": "#27c0c8"
  },
  "website": "https://professional_services_inc.com",
  "office_phone": "1-800-776-4521",
  "enable_pwa": true,
  "support_email": "support@professional_services_inc.com",
  "info_email": "info@professional_services_inc.com",
  "email_hyperlink": "@professional_services_inc.com",
  "users": [
    {
      "username": "g.hawkins",
      "password": "SecuredPassword123!",
      "call_sign": "GH",
      "email": "g.hawkins@professional_services_inc.com",
      "phone": "1-800-776-4521",
      "admin": true
    },
    {
      "username": "d.richards",
      "password": "SecureCloudsRun@123",
      "call_sign": "DR",
      "email": "d.richards@professional_services_inc.com",
      "phone": "1-800-776-4521",
      "admin": true
    },
    {
      "username": "s.mitchell",
      "password": "SecurePassword!234",
      "call_sign": "SM",
      "email": "s.mitchell@professional_services_inc.com",
      "phone": "1-800-776-4521",
      "admin": false
    },
    {
      "username": "installer",
      "password": "CrazyChickenDances@123",
      "call_sign": "Installer",
      "email": "installer@professional_services_inc.com",
      "phone": "1-800-776-4521",
      "admin": false
    }
  ],
  "sib_api_key": "SEND IN BLUE API KEY",
  "services": [
    { "blog": "https://blog.professional_services_inc.com" },
    { "website": "https://www.professional_services_inc.com" }
  ]
}
```

### Instructions

1. Obtain an API key from [Brevo](https://www.brevo.com/).
2. Clone this repository to your local machine.
3. Navigate to the project's root directory.
4. Open app/config.json and add your configurations.
5. Assuming Docker and Docker Compose are installed correctly, run the build script (`build.sh`) found in the root directory of this project. This script builds the Docker images and starts the Docker containers.
6. Access the REST API at `http://localhost:8080/`.
7. Once inside the UI, init the database tables.
   ![image](https://github.com/gary23w/lfbuilders-rest-api/assets/61893883/e1f4f562-cb7f-4126-9b01-0e2eca952df4)

If all else fails, simply execute `docker-compose up -d`.

## API Endpoints

For more details, refer to docs.md.

## Database

The application uses PostgreSQL for its database. Database name, user, and password are specified in the docker-compose file.

## Security Considerations

- Ensure the PostgreSQL port is not exposed to the public; keep it internal to the Docker network.
- Alter the database user, password, and other sensitive information before deploying to a production environment.
- Avoid sharing sensitive information like passwords and secret keys in code or version control systems.

## Logging

The application logs are accessible via Docker. Docker commands can be used to view the logs.

```
docker logs <container_id>
```

## Contributions

Contributions to the LF Builders REST API are always welcome. Please adhere to the coding conventions within the codebase and add appropriate tests where necessary.

## License

This project is licensed under the terms of the MIT license. For details, see the `LICENSE` file.
