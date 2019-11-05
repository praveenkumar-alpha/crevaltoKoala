[![Koala LMS logo](static/lms/img/banner-sm.png)](https://www.koala-lms.org)
  
# :koala: Koala, Learning Management system

## :school: What is Koala LMS?

**Koala LMS** is a **Learning Management System** (*LMS*) that aims to be simple, **made by users**, **for users**. It has been originally developed in the [LORIA Laboratory](http://www.loria.fr/fr/), Nancy, France.

Contrary to other LMS like Moodle for instance, **Koala LMS** wants to stay **simple**, **user focused** and without useless functionalities. Features and requirements come from interviews of people from the [Université de Lorraine](https://www.univ-lorraine.fr/), Nancy, France.

A demonstration instance is available at [demo.koala-lms.org](https://demo.koala-lms.org). It is populated with sample data and refreshed every ten minutes (ie: 2:20; 2:30, etc.). Login as “Erik Orsenna” to access relevant data with the following credentials: `erik-orsenna` and `koala-lms` as the password. Up to now, the demonstration server is populated with data in french, coming from Wikipedia.

**Koala-LMS** components are free software (free as in freedom). All of them are distributed under the [**GPLv3 Licence**](https://www.gnu.org/licenses/quick-guide-gplv3.en.html). We want free code to **remain free**! :blush:

## Preamble

### Requirements

In order to make it easy to install **Koala LMS** on your system, we decided to use Python. Python is a **common and massively used language** in scientific and research communities. At the very early hours of the project, we hoped contributions from those communities. Thus, targeting a programming language well known by our community seems to be a great idea.

As you may know, **Django** is a super easy, extensible framework. Thanks to this approach, **Koala LMS** is distributed as Django applications that you can plug and make your very own **Learning Management system**! This way, **Koala LMS** is expandable or minimizable. The whole **Learning Management System** is, in fact a full project with all the applications enabled. If you want to do your very own installation, you can! Easy, uh?

### Technical requirements

**Koala LMS** and the components run with [**Django 2.2**](https://docs.djangoproject.com/en/2.2/releases/2.2/) and [**version 3.7**](https://www.python.org/downloads/release/python-370/). Only **long term support Django releases** will be supported in the future.

## :ship: Start using Docker

You need to [install `docker`](https://docs.docker.com/install/) on your system. We host the [docker image in the Gitlab Registry](https://gitlab.com/koala-lms/lms/container_registry). Its `Dockerfile` is located at [`./docker/stable/Dockerfile`](docker/stable/Dockerfile). You can get the image (*<50MB to download*) using:
```bash
docker pull registry.gitlab.com/koala-lms/lms
```

#### Tweak Docker deployment

You can tweak the `koala-lms` deployment using some environment variables. None is required.
* `LANGUAGE_CODE`: the Django corresponding setting.
* `TIME_ZONE`: the Django corresponding setting.
* `FIXTURE`: the fixture to load (relative to the project directory, ie: `./fixtures/sample.json`). You will find additional fixtures in the `fixtures` directory.
* `DEMO`: if you wish to enable the demonstration server
* `DEMONSTRATION_LOGIN`: the user that exists in the *fixture* that will be logged in
* `DEBUG`: whether to use Django debug mode.

#### Start the container

To run `koala-lms`. You just have to run:
```bash
docker run --name koala-lms -e FIXTURE="./fixtures/sample-fr.json" -e DEBUG=1 -p 8080:8080 registry.gitlab.com/koala-lms/lms 
```
And the container will boot. The application is distributed under the URL [localhost:8080](http://localhost:8080).

## :snake: Start using a Python virtual environment

### Prepare your workspace

The really first step before contributing to Koala LMS is to prepare your workspace: it will contain your Python virtual environmnent, as long as the Django Project, **lms** and the applications you are working on: **django-learning**, **django-accounts**, etc. Before doing so, ensure you use Python 3.7 or greater, and that you can use the `virtualenv` Python module. If not, documentation [for Ubuntu](https://linuxize.com/post/how-to-create-python-virtual-environments-on-ubuntu-18-04/), or [for Fedora](https://developer.fedoraproject.org/start/sw/web-app/django.html).

1. Move where you want in your filesystem hierarchy and create a directory, for instance, `koala_lms`.
2. Move into this directory.
3. Create a Python virtual environment with: `python3 -m venv venv`.
4. Activate your Python virtual environment, using `source venv/bin/activate`.

### Download and use the latest version of Koala LMS

1. In your workspace, clone the Git repository: `git clone https://gitlab.com/koala-lms/lms.git`. A new directory called `lms` appears. It contains the Django project, this project.
2. Move into the `lms` project and install the **Koala LMS** dependencies: `pip3 install -r requirements.txt`
3. Before doing any migration, the [`SECRET_KEY`](https://docs.djangoproject.com/fr/2.2/ref/settings/#std:setting-SECRET_KEY) parameter must be set. You **MUST NOT** change the `lms/settings.py` file, as it contains settings for deployments of Koala LMS. Otherwise, for development purposes, you are encouraged to add a `lms/local_settings.py` file, where you can add the setting, like: `SECRET_KEY = "azertyuiop"`.
4. Call `migrate` to create the database: `./manage.py migrate`
5. You can optinaly load some fixtures, like the french ones: `./manage.py loaddata ./fixtures/sample-fr.json`

#### Load the demonstration user

If you intend to contribute to **Koala LMS**, it might be useful not to login manually each time you use the application. To avoid this, we provide, trough a [Django middleware](https://docs.djangoproject.com/en/2.2/topics/http/middleware/), a way to be automatically connected, when running a **demonstration server**.

In order to enable it, update the `lms/local_settings.py` file and add the following:
```python
DEMO = True  # To indicate the code is running as a demonstration
DEMONSTRATION_LOGIN = "erik-orsenna"  # A user that exists in the database and that will be logged-in automatically
```

#### Create a super-user

A super user is useful when you want to access [**Django’s admin backend**](https://docs.djangoproject.com/en/2.2/ref/contrib/admin/). To create it, call `./manage.py createsuperuser` and fill the form with a username and a password.

### Run the development server

The development server can be run using the command line `./manage.py runserver`. Then, by default, a web-server will be started, listening the port 8000 on localhost. You can access it through [https://127.0.0.1:8000](https://127.0.0.1:8000).

### Contribute to Koala LMS application

Now, you track stable applications. If you wish to contribute to the `learning` application for instance, you **MUST NOT** download it in the `lms` directory, but in your workspace. For more information on how applications work, please read [Applications](https://docs.djangoproject.com/en/2.2/ref/applications/) from the Django documentation.

1. Clone the Git repository: `git clone https://gitlab.com/koala-lms/django-learning.git`
2. Create a symbolic link in the `lms` directory (**Koala LMS** project) to the `learning` package: `cd lms && ln -s ../django-learning/learning learning`.
3. Now, run the project, you’re using the code from the `master` or `develop` branch.

**NOTE**: you might need to refresh the dependencies in the virtual environment, as new versions of applications may require extra dependencies.

## :open_hands: Contributing

Every kind of contribution is well welcomed! You can give us your feedback or report bugs. You can help us translate Koala-LMS components, write documentation, and more.

If you wish to contribute, please, follow the [contribution guidelines](CONTRIBUTING.md). It’s not that long, in a few minutes, you’ll understand how to help! :grinning:

## :book: Documentation

### :green_book: User documentation

We are not able to provide user documentation yet but we hope to have one really soon. If you wish to help us with this, please, read the [contribution guidelines](CONTRIBUTING.md).

### :ledger: Technical documentation

Technical documentation about **Koala LMS** is available in this [project wiki](https://gitlab.com/koala-lms/lms/wikis/home). As you have already understood, **Koala LMS** is a set of components and if you want to know more, please refer to each component documentation.

* the `learning` application is [`django-koalalms-learning`](https://pypi.org/project/django-koalalms-learning/) ([source code on Gitlab](https://gitlab.com/koala-lms/django-learning)).
* the `accounts` application is [`django-koalalms-accounts`](https://pypi.org/project/django-koalalms-accounts/) ([source code on Gitlab](https://gitlab.com/koala-lms/django-accounts)).
