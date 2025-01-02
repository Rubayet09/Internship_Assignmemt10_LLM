
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
- **Ollama Model: `gemini-2.0-flash-exp` model** For text generation and LLM functionalities.
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



django_cli_property_rewriter/
├── django_cli/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
├── property_rewriter/
│   ├── management/
│   │   ├── commands/
│   │   │   ├── rewrite_property_info.py
│   │   │   ├── generate_property_summary.py
│   │   │   └── generate_property_reviews.py
│   ├── migrations/
│   ├── models.py
│   ├── services/
│   │   ├── ollama_service.py
│   │   └── __init__.py
│   ├── tests.py
│   └── views.py
├── manage.py
├── requirements.txt
├── README.md
├── setup.py
└── .env



## Author
Rubayet Shareen
SWE Intern, W3 Engineers
Dhaka, Bangladesh
