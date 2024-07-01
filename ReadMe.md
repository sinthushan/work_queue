# Work Queue

This is a backend application that helps companies assign work to their employees. Individuals can create tickets and assign these tickets to a team. The application would then assign the ticket to the next available team member. Team members will have a queue of tickets which they are able to update which will in turn update their availability.

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
- [License](#license)
- [Questions](#questions)

## Installation

1. Clone the repo and CD into the folder you cloned it into. 
```bash
$ CD work_queue
```

2. Create a virtual enviroment
```bash
$ python -m venv env
```

3. install the dependencies in the requirements.txt file
```bash
$ pip install -r requirements.txt
```

4. make migrations by running:
```bash
$ python manage.py makemigrations
```
followed by:
```bash
$ python manage.py migrate
```

5. Create a superuser
```bash
$ python manage.py createsuperuser --username <username of your liking>  --email <email address of your liking
```
You will be prompted to make a password, feel free to make any password you like. If you choose to use a simple password you may get a warning but just type Y and enter to continue with your chosen password

6. runserver locally
```bash
$ python manage.py runserver
```

## Usage

## License

The project is licensed under: MIT License. To see the license permissions for commercial and non-commercial use, check the link https://opensource.org/licenses/MIT

## Questions

For any questions about the application, please contact me via [email](mailto:sinthushan@gmail.com)