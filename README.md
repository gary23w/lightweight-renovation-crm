# Lightweight-Construction-CRM-API

<hr />

![LICENSE](https://img.shields.io/github/license/Ileriayo/markdown-badges?style=for-the-badge)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](http://makeapullrequest.com)
[![CircleCI](https://circleci.com/gh/google/pybadges.svg?style=svg)](https://circleci.com/gh/google/pybadges)
![versions](https://img.shields.io/pypi/pyversions/pybadges.svg)
![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)
![LeetCode](https://img.shields.io/badge/LeetCode-000000?style=for-the-badge&logo=LeetCode&logoColor=#d16c06)
![GitHub](https://img.shields.io/badge/github-%23121011.svg?style=for-the-badge&logo=github&logoColor=white)

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
<li>-> *python prototype.</li>
</ul>

**reach me on Discord: @gary23w**

## Building and Running the API

### Prerequisites

- SendInBlue API Key
- Docker
- Docker Compose

### Configuring app/config.json

Modify the values to align with your conventions.

### Instructions

# Build

1. Obtain an API key from [Brevo](https://www.brevo.com/).
2. Clone this repository to your local machine.
3. Navigate to the project's root directory.
4. Open app/config.json and add your configurations.
5. Assuming Docker and Docker Compose are installed correctly, run the build script (`build.sh`) found in the root directory of this project. This script builds the Docker images and starts the Docker containers.
6. Access the REST API at `http://localhost:8080/`.
7. Once inside the UI, init the database tables.

---

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
