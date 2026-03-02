<!-- Prerequisites -->

Before running the project, ensure:

1.Python 3.9 or above installed

2.ClickHouse server installed and running

3.Database business_ops created

4.Required tables created and populated with data

<!-- Setup Instructions -->

Step 1: Clone the Repository

git clone <repository_url>
cd business_ops_api

Step 2: Create Virtual Environment

Windows
python -m venv venv
venv\Scripts\activate
Linux / WSL / Mac
python3 -m venv venv
source venv/bin/activate

Step 3: Install Dependencies

pip install -r requirements.txt

<!-- Database Verification -->

Open ClickHouse client:

clickhouse-client

Verify database exists:

SHOW DATABASES;

Ensure business_ops is present.

Then:

USE business_ops;
SHOW TABLES;

<!-- Running the API Server -->

Start the FastAPI server:

uvicorn main:app --reload

<!-- Expected Output: -->

Uvicorn running on http://127.0.0.1:8000

<!-- Access Swagger Documentation -->

Open browser:

http://127.0.0.1:8000/docs

Swagger UI will open automatically.