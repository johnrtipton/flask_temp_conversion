# Temperature Conversion Checker

Temperature Conversion Checker will check the temperature conversions for accuracy.  Calculated temperatures are rounded to the nearest whole number and compared to the students answer.

## Usage

Enter the starting temperate in the **Input Temperature** field, enter the desired target unit in the **Target Unit** field, and enter the students answer in the **Student Response** field.  The application will show either correct, incorrect or invalid.

## Example Data

| **Input Temperature** | **Target Units** | **Student Response** | **Output** |
| --------------------- | ---------------- | -------------------- | ---------- |
| 84.2 Fahrenheit       | Rankine          | 543.5                | correct    |
| -45.14 Celsius        | Kelvin           | 227.51               | correct    |
| 317.33 Kelvin         | Fahrenheit       | 110.5                | incorrect  |
| 444.5 Rankine         | Celsius          | -30.9                | incorrect  |
| 6.5 Fahrenheit        | Rankine          | dog                  | incorrect  |
| dog                   | Celsius          | 45.32                | invalid    |

## REST

You can access the service using rest at the **/check_temp/** endpoint, see the curl example below.

**Example**

```bash
$ curl 'http://0.0.0.0:5000/check_temp/' --data 'starting_value=84.2+Fahrenheit&desired_unit=Rankine&student_answer=543.5'

{"answer": "correct"}
```

##Run locally

```bash
# Install and activate virtual environment
pip install virtualenv
python -m venv
. venv/bin/activate
pip install -r requirements.txt

# Run locally with debugging
python app.py

# Run locally with gunicorn
 gunicorn -w 4 -b 127.0.0.1:5000 wsgi:application
```

Then browse to http://127.0.0.1:5000/

## Run with Docker

```bash
# Build docker Image
docker build . -t fask_temp_check
# Start Docker image
docker run -d --rm -it -p 5000:5000 --name fask_temp_check_1 fask_temp_check
```

Then browse to http://127.0.0.1:5000/