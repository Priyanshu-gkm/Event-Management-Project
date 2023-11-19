<div align="center">
<h1 align="center">
<img src="https://raw.githubusercontent.com/PKief/vscode-material-icon-theme/ec559a9f6bfd399b82bb44393651661b08aaf7ba/icons/folder-markdown-open.svg" width="100" />
<br>EVENT MANAGEMENT BACKEND API - DJANGO REST</h1>
<h3>◦ ► Priyanshu Arora - GKM IT</h3>
<h3>◦ Developed with the software and tools below.</h3>

<p align="center">
<img src="https://img.shields.io/badge/Python-3776AB.svg?style=flat-square&logo=Python&logoColor=white" alt="Python" />
<img src="https://img.shields.io/badge/Django-092E20.svg?style=flat-square&logo=Django&logoColor=white" alt="Django" />
</p>
</div>

---

## 📖 Table of Contents

- [📖 Table of Contents](#-table-of-contents)
- [📍 Overview](#-overview)
- [📦 Features](#-features)
- [📂 repository Structure](#-repository-structure)
- [🚀 Getting Started](#-getting-started)
  - [🔧 Installation](#-installation)
  - [🤖 Running Event_Management_Project](#-running-Event_Management_Project)
- [🛣 Roadmap](#-roadmap)
- [🤝 Contributing](#-contributing)

---

## 📍 Overview

► **Created a comprehensive Event Management System using Django Rest Framework, tailored for businesses, event organizers, or venues to manage, promote, and host events. This project can cater to a wide range of event types, including conferences, concerts, workshops, and more.**

---

## 📦 Features

1. **User Authentication:** Implement user registration and login, with different roles such as event organizers, attendees, and administrators.
2. **Event Creation:** Event organizers can create events, providing details like event name, date, time, location, description, images, and ticket pricing.
3. **Ticketing System:** Implement a ticketing system that allows users to purchase event tickets. Provide options for different ticket types (e.g., VIP, General Admission).
4. **Event Management:** Organizers can manage their events, view ticket sales, check-in attendees, and monitor event analytics.
5. **Wishlisting** or adding events under watch for a user.
6. **Search and Filtering:** Users can search for events based on location, date, category, and keywords. Include advanced filtering options.
7. **User Profiles:** Users can create and customize profiles, track their attended events, and manage their ticket purchases.
8. **Notification management :** Email notifications to attendees , event organizers about various events.

---

## 📂 Repository Structure

```sh
└── Event_Management/
    ├── .env.sample
    ├── Event_Management/
    │   ├── asgi.py
    │   ├── settings.py
    │   ├── urls.py
    │   └── wsgi.py
    ├── accounts/
    │   ├── admin.py
    │   ├── apps.py
    │   ├── custom_permissions.py
    │   ├── managers.py
    │   ├── migrations/
    │   │   ├── 0001_initial.py
    │   ├── models.py
    │   ├── serializers.py
    │   ├── tests.py
    │   ├── urls.py
    │   └── views.py
    ├── api/
    │   ├── admin.py
    │   ├── apps.py
    │   ├── migrations/
    │   ├── models.py
    │   ├── tests.py
    │   ├── urls.py
    │   └── views.py
    ├── events_tickets/
    │   ├── admin.py
    │   ├── apps.py
    │   ├── custom_filters.py
    │   ├── custom_permissions.py
    │   ├── custom_validators.py
    │   ├── event_urls.py
    │   ├── migrations/
    │   │   ├── 0001_initial.py
    │   │   ├── 0002_ticket_archive.py
    │   │   ├── 0003_wishlist.py
    │   ├── model_factory.py
    │   ├── models.py
    │   ├── serializers.py
    │   ├── setup_data.py
    │   ├── tests.py
    │   ├── ticket_type_urls.py
    │   ├── ticket_urls.py
    │   ├── urls.py
    │   └── views.py
    ├── manage.py
    ├── notify/
    │   ├── apps.py
    │   ├── jobs.py
    │   └── migrations/
    └── requirements.txt

```

---

## 🚀 Getting Started

**_Dependencies_**

Please ensure you have the following dependencies installed on your system:

`- ℹ️ Python 3.11.5`

`- ℹ️ Django-Rest-Framework`

### 🔧 Installation

1. Clone the Event_Management repository:

```sh
git clone https://github.com/Priyanshu-gkm/Event-Management-Project.git
```

2. Change to the project directory:

```sh
cd Event_Management_Project
```

3. Install the dependencies:

```sh
pip install -r requirements.txt
```

### 🤖 Setup Environment Variables

```sh
touch .envrc
```

copy all variables from .env.sample and repopulate them according to your configuration

### 🤖 Running Event_Management_Project

```sh
python manage.py runserver
```

---

## 🤝 Contributing

Contributions are welcome! Here are several ways you can contribute:

- **[Submit Pull Requests](https://github.com/local/Event_Management/blob/main/CONTRIBUTING.md)**: Review open PRs, and submit your own PRs.
- **[Join the Discussions](https://github.com/local/Event_Management/discussions)**: Share your insights, provide feedback, or ask questions.
- **[Report Issues](https://github.com/local/Event_Management/issues)**: Submit bugs found or log feature requests for LOCAL.
