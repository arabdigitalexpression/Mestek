# Space Reservation System

<a name="readme-top"></a>

<br />
<div align="center">
    <img src="/app/static/images/adef.png" alt="Logo" width="80" height="80">
  <p align="center">
    <a href="https://github.com/arabdigitalexpression/Mestek/issues">Report Bug</a>
    ·
    <a href="https://github.com/arabdigitalexpression/Mestek/issues">Request Feature</a>
  </p>
</div>

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>

<!-- ABOUT THE PROJECT -->

## About The Project

The story of this project begins in Arab Digital Expression Foundation when we needed to make our friends from non-profit organizations and civil associations life easier with mangaging there own spaces and renting thier tools. We needed to find a online solution for spaces and tools reservations.

We've quickly evaluated a couple of existing solutions, but they were either too big and complicated and/or too expensive. As We assumed that other people would have the same challenge We had, We decided to spend our after-hours time making an open-source tailored platform for the need and it is for free use.

What our platform can do:

-  It allows people to reserve, de-reserve spaces and tools in your organization.
- It allows people to pay online by virtual wallet for their own reservations.
- Platform can deployed online or on a dedicated internal server inside your organization.
- Administrators has a visually statistics for reservations.

Of course, no platform will serve all organizations needs since your needs may be different. So I'll be adding more soon. You may also suggest changes by forking this repo and creating a pull request or opening an issue. Thanks in advance to all the people who will contribute to expanding this platform!

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Built With

[![Flask][flask]][flask-url]
[![MariaDB][mariadb]][mariadb-url]
[![Bootstrap][bootstrap.com]][bootstrap-url]
[![JQuery][jquery.com]][jquery-url]

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- GETTING STARTED -->

## Getting Started

The next steps are for running Space Reservation System on a local or remote server.

So please take steps forward in order for doing it in the right way.

### Prerequisites

You should:

- Know how to deal with Linux environment.
- Programmed with python before and flask.
- Used database management system before _ex: (MySQL)_

### Installation

1. #### Installing Database service

   In this project, we used MySQL in our development process but you can use other database management systems that SQLAlchemy supporting it.

   You can install your database service depending on your operating system. In this process, I used ubuntu Linux OS.

   ```sh
   $ sudo apt update
   ```

   ```sh
   $ sudo apt install mysql-server libmysqlclient21
   ```

   ```sh
   $ sudo systemctl start mysql.service
   ```

   ```sh
   $ mysql_secure_installation
   ```

   after installation use, this commands to create a new database for this application

   ```sh
   mysql -u root -p
   ```

   ```sh
   mysql> CREATE DATABASE 'database_name' CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   ```

   ```sh
   mysql> CREATE USER 'username'@'host' IDENTIFIED BY 'password';
   ```

   ```sh
   mysql> GRANT PRIVILEGE ON 'database_name'.* TO 'username'@'host';
   ```

   ```sh
   mysql> FLUSH PRIVILEGES;
   ```

2. Clone the repo
   ```sh
   git clone https://github.com/arabdigitalexpression/Mestek.git
   ```
3. Install dependencies

   ```sh
   $ sudo apt-get install python3 python3-dev python3-pip
   ```

   ```sh
   $ sudo pip3 install virtualenv
   ```

   ```sh
   $ cd Mestek
   ```

   ```sh
   $ virtualenv -p python3 myenv
   ```

   ```sh
   $ source venv/bin/activate
   ```

   ```sh
   $ pip3 install -r requirements.txt
   ```

   - Create environment variables (see <a href="/.env-example">example .env file</a>):
   ```sh
   $ vi .env
   ```

   ```sh
   $ flask db upgrade
   ```

   ```sh
   $ flask run
   ```

   <p align="right">(<a href="#readme-top">back to top</a>)</p>

## Usage

After the installation process, you can run the application on your browser and start creating new space and tools.

And when you are finished anyone is ready to reserve and space or tool that they want.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

See the [open issues](https://github.com/arabdigitalexpression/Mestek/issues) for a full list of proposed features (and known issues).

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Contributing

Contributions are what makes the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## License

Distributed under the GNU General Public License v3.0
License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Contact

Arab Digital Expression Foundation - [Visit website](https://www.adef.xyz)

Project Link: [https://github.com/arabdigitalexpression/Mestek](https://github.com/arabdigitalexpression/Mestek)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

[product-screenshot]: screenshot.png
[mariadb]: https://img.shields.io/badge/MariaDB-c0765a?style=for-the-badge&logo=mariadb&logoColor=white
[mariadb-url]: https://mariadb.org/
[flask]: https://img.shields.io/badge/Flask-ffff00?style=for-the-badge&logo=FLASK&logoColor=black
[flask-url]: https://flask.palletsprojects.com/en/2.2.x/
[bootstrap.com]: https://img.shields.io/badge/Bootstrap-563D7C?style=for-the-badge&logo=bootstrap&logoColor=white
[bootstrap-url]: https://getbootstrap.com
[jquery.com]: https://img.shields.io/badge/jQuery-0769AD?style=for-the-badge&logo=jquery&logoColor=white
[jquery-url]: https://jquery.com
