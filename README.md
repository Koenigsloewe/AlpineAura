# AlpineAura Website Project

## About AlpineAura

AlpineAura is a dynamic e-commerce platform dedicated to outdoor enthusiasts seeking high-quality gear for their next adventure. Built with Python using the Django framework and backed by a SQLite database, AlpineAura offers a streamlined shopping experience, featuring a wide range of outdoor products. Payment processing is seamlessly integrated through the Stripe API and PayPal, ensuring a secure and efficient checkout process for all users.

## Getting Started

To get AlpineAura up and running on your local machine for development and testing purposes, follow these steps:

### Prerequisites

Ensure you have Python installed on your system. This project also assumes you have `pip` and `virtualenv` installed. If not, install them using the following commands:

```bash
pip install virtualenv
```
### Installation

Clone the repository to your local machine:
```bash
git clone https://github.com/Koenigsloewe/AlpineAura.git
```
Install the required dependencies from requirements.txt:
```bash
pip install -r requirements.txt
```
### Before running the application, add your Stripe API and PayPal keys to AlpineAura/settings.py

## Running the Application

### Run the server:

```bash
python manage.py runserver
```
### Run stripe
```bash
stripe listen --forward-to localhost:8000/payment/webhook/
```
### superuser:

E-Mail: admin@admin.com

password: admin

### Run local smtp server

```bash
aiosmtpd -n -l localhost:1025
```

### Enjoy exploring AlpineAura and managing its outdoor products!