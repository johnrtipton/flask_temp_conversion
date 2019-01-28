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



# Resources

Terraform Buildout

http://fedulov.website/2018/02/18/terraform-deploying-containers-on-aws-fargate/

https://github.com/mattghali/terraform-fargate/commits/master



Terraform update when code pushed

https://github.com/alex/ecs-terraform

- Checkout newer version:

  https://github.com/silinternational/ecs-deploy



Scaling

https://aws.amazon.com/blogs/compute/automatic-scaling-with-amazon-ecs/



# Issues

- When running terraform apply, the ecr repository may already exist, to get around this you can import the existing resource.

  ```bash
  terraform import aws_ecr_repository.myapp myapp
  ```

  

  To create the ecr when it does not exist.

- ```bash
  terraform apply --target aws_ecr_repository.myapp 
  ```

  **But, I think I will not let terraform manage it and create it manually**

- Terraform sees that the task definition has changed and wants to set it back during terraform apply.  I guess this wouldn't technically be a problem, as the original task definition is set to latest, and each image is pushed with both the release and latest as tags.

  Solved this by adding:

  ```terraform
  data "aws_ecs_task_definition" "myapp" {
    task_definition = "${aws_ecs_task_definition.myapp.family}"
  }
  
    task_definition = "${replace(aws_ecs_task_definition.myapp.arn, "/:\\d*$/", "")}:${max("${aws_ecs_task_definition.myapp.revision}", "${data.aws_ecs_task_definition.myapp.revision}")}"
  
  ```

  

