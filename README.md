
# Django CLI Application for Property Rewriting

## Table of Contents
1. [Overview](#overview)
2. [Key Features](#key-features)
3. [Technologies Used](#technologies-used)
4. [Development Setup](#development-setup)
5. [Project Structure](#project-structure)
6. [Author](#author)

## Overview
This project involves building a Django CLI application that leverages an Ollama model to rewrite property titles and descriptions, generate summaries, and create ratings and reviews. The rewritten content and generated metadata are stored in a PostgreSQL database using Django ORM. The application ensures high code coverage and adheres to best practices.

---

## Key Features
- **Rewriting Property Information**: Utilizes an Ollama model in this case I have used Gemini to rewrite property titles and descriptions.
- **Summary Generation**: Summarizes property data and stores it in a separate table.
- **Ratings and Reviews**: Generates ratings and reviews using the model and saves them in  another table in the database.
- **Database Integration**: Employs PostgreSQL for data storage and Django ORM for seamless interactions.
- **CLI Interface**: Implements Django CLI commands for executing tasks.

---

## Technologies Used
- **Django**
- **PostgreSQL**
- **Ollama Model** `gemini-2.0-flash-exp` model For text generation and LLM functionalities.
- **Python**
- **Django ORM**

---

## Development Setup

### Prerequisites
Ensure the following are installed on your system:
- Python 3.6 or higher
- PostgreSQL
- Django framework
- Ollama CLI (refer to [Ollama Documentation](https://ollama.com/))

---

### Steps: 1. Clone the repository:
```bash
git clone https://github.com/Rubayet09/Internship_Assignmemt10_LLM
cd Project
```
### Steps: 2. Build and compose Docker
 ```bash 
docker compose build

docker-compose up
 ```
Scraper will run and you can see the  `properties` table with all the property-hotel information of 3 random cities.
```
docker-compose exec db psql -U myuser -d tripcom_db

SELECT * FROM properties;
```
### Steps: 3. Run migrations:
 ```bash 
docker-compose exec web python manage.py makemigrations property_rewriter

docker-compose exec web python manage.py migrate property_rewriter
 ```
 
### Steps: 4. Run the model to rewrite the prompt:
 ```bash 
docker-compose exec web python manage.py rewrite_properties
 ```
 The model will rewrite the prompt and create new tables with summary and review. You can access the table from here:
 ```bash 
docker-compose exec db psql -U myuser -d tripcom_db

SELECT * FROM property_rewriter_propertyreview;

SELECT * FROM property_rewriter_propertysummary;
 ```
### Steps: 5. Installation for test:
 ```bash

docker-compose exec web pip install pytest pytest-django pytest-cov coverage

```
### Steps: 6. Run the Test:
 ```bash

docker-compose exec web pytest -v --cov=property_rewriter --cov-report=html
```
It will show, Total coverage: 100.00%
```
Name                                                          Stmts   Miss  Cover   Missing
-------------------------------------------------------------------------------------------
property_rewriter/management/commands/rewrite_properties.py      12      0   100%
property_rewriter/models.py                                      23      0   100%
property_rewriter/services/gemini_service.py                     48      0   100%
property_rewriter/services/property_service.py                   20      0   100%
-------------------------------------------------------------------------------------------
TOTAL                                                           103      0   100%
```

## Project Structure

```

Project/
├── django_cli/
│   ├── django_cli/
│   │   ├── __init__.py
│   │   ├── asgi.py
│   │   ├── settings.py
│   │   ├── urls.py
│   │   ├── wsgi.py
│   ├── property_rewriter/
│   │   ├── management/
│   │   │   ├── commands/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── rewrite_properties.py
│   │   │   └── __init__.py
│   │   ├── migrations/
│   │   │   ├── __init__.py
│   │   ├── services/
│   │   │   ├── gemini_service.py
│   │   │   └── property_service.py
│   │   ├── __init__.py
│   │   ├── tests.py
│   │   ├── views.py
│   │   ├── models.py
│   │   ├── admin.py
│   │   ├── apps.py
├── hotel_images/
│   └── .gitkeep
├── src/
│   ├── projectscrape/
│   │   ├── database.py
│   │   ├── main.py
├── tests/
│   ├── __init__.py
├── .env
├── .gitignore
├── docker-compose.test.yml
├── docker-compose.yml
├── Dockerfile
├── hotels_data.json  # This is an empty file
├── LICENSE
├── pyproject.toml
├── README.md
├── requirements.txt
├── setup.py

```

## Author
Rubayet Shareen
SWE Intern, W3 Engineers
Dhaka, Bangladesh
