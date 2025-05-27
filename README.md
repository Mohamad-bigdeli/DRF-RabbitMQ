### This project is a Django REST Framework API designed to process and analyze CSV files containing transaction data. The API accepts CSV uploads with the following format:

- Columns: `transaction_id`, `amount`, `timestamp`, `category`, `description`
- Example:
  ```
  transaction_id,amount,timestamp,category,description
  1,150.50,2023-01-01 12:30:00,food,restaurant dinner
  2,1200.00,2023-01-02 09:15:00,shopping,electronics purchase
  ```

## Architecture
- **Backend**: A Django REST API handles CSV file uploads and stores metadata in a PostgreSQL database.
- **Message Queue**: RabbitMQ manages asynchronous task queuing for file processing.
- **Worker**: A separate worker process consumes messages from the RabbitMQ queue, processes the CSV files, and stores results in a PostgreSQL JSONB field.
- **Database**: PostgreSQL stores uploaded file metadata and analysis results, leveraging JSONB for flexible result storage.
  
![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white)
![RabbitMQ](https://img.shields.io/badge/RabbitMQ-FF6600?style=for-the-badge&logo=rabbitmq&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)

## Processing Workflow
1. Users upload a CSV file via the API.
2. The file metadata is saved in the database, and a task is sent to the RabbitMQ `analyzer_queue`.
3. A worker process asynchronously consumes the task, reads the CSV file, and performs analysis using the `analyze_csv` function.
4. Results are stored in the `AnalysisResult` model using a JSONB field, and the file's status is updated (`processing`, `completed`, or `failed`).

## Asynchronous Processing
The processing is **asynchronous**. The worker uses a `threading.Thread` to consume messages from RabbitMQ, ensuring non-blocking operation. The `AnalyzerConsumer` class handles messages in a separate thread, and the `analyze_csv` function processes the CSV file independently of the main API thread.

## Setup
- **Docker**: The project uses Docker Compose to manage services (PostgreSQL, RabbitMQ, Django backend, and worker).
- **Dependencies**: Install requirements via `requirements.txt` and configure environment variables in `core/.env`.

1. **Clone the Repository**
  
   Clone the project repository to your local machine:

   ```bash
   git clone https://github.com/Mohamad-bigdeli/DRF-Shop.git

2. **Navigate to the Project Folder**

    Move into the project directory using the cd command:

    ```bash
    cd DRF-Shop
    

3. **Start Docker Compose** 

    Use Docker Compose to start the project services by running the command:

    ```bash
    docker-compose up --build 

4. **Create and Apply Migrations**

    After the services are up, create and apply the database migrations using the following commands:
    ```bash 
    docker-compose exec backend sh -c "python manage.py makemigrations"

    docker-compose exec backend sh -c "python manage.py migrate"

5. **Create a Superuser**

    Create a superuser to access the Django admin panel by running the command:

    ```bash
    docker-compose exec backend sh -c "python manage.py createsuperuser"

6. **Collect Static Files**

    Collect static files for the project using the command:

    ```bash
    docker-compose exec backend sh -c "python manage.py collectstatic --noinput"
    
7. **View the Project**

    Your project is now running on port 8000. Open your browser and navigate to:

   ```bash
    http://localhost:8000.

8. **Access the Admin Panel**

    To access the Django admin panel, go to the following URL and log in with your superuser credentials:

    ```bash
    http://localhost:8000/admin

**Additional Notes**

    If you make changes to the code and need to restart the services, use the docker-compose restart command.
    To stop the services, use the docker-compose down command.

<h3>By following these steps, your project will be fully set up and ready to use. 🎉</h3>
