# LMNH Pipeline

This repository contains the all the code, documentation and resources required for the pipeline for Liverpool Natural History Museum. The pipeline serves to monitor the health of the plants over time in the botanical wing of the museum.


## Requirements

1. Clone this repository:
    ```sh
    git clone https://github.com/Zhi-704/C11-Kappa-Group-Project.git.
    ```

2. Navigate to the directory and install the required packages in the terminal:
    ```sh
    cd [PATH_TO_FOLDER]/C11-Kappa-Group-Project
    pip3 install -r local_requirements.txt
    ```

> [!NOTE]  
The `local_requirements.txt` file lists all necessary packages to run all folders locally. The other `requirements.txt` files are used for provisioning resources in AWS for Docker environments.

## Archictecture Diagram

The project architecture is based of the diagram below.

![Architecture Diagram](https://github.com/Zhi-704/C11-Kappa-Group-Project/raw/main/diagrams/Architecture_Diagram.png)


## Database Schema

To view the database schema for the plant data, please refer to this Entity-Relationship Diagram (ERD). 


<a id="erd-diagram"></a>
![ERD Diagram](https://github.com/Zhi-704/C11-Kappa-Group-Project/blob/main/diagrams/ERD_diagram.png)


## Secrets/Authentication
> [!IMPORTANT]  
> To be able to run these scripts the following details must be provided in an `.env` file inside their respective folders and should NOT be shared.

| KEY | Affected Folders | Description |
| -------- | --------| --------|
|ACCESS_KEY|`archiver`,`dashboard`| Used to access the AWS system.
|SECRET_ACCESS_KEY|`archiver`, `dashboard`| Used for authentication for the AWS system.
|BUCKET_NAME|`archiver`, `dashboard`| Name of storage bucket (e.g., Amazon S3) where long-term data is stored.
|AWS_ACCESS_KEY|`terraform`| Authentication key for AWS used by Terraform to manage cloud resources.
|AWS_SECRET_KEY|`terraform`| Secret key for AWS used by Terraform for secure authentication.
|DB_HOST|`archiver`, `dashboard`, `terraform`| Host address of the database server used by the applications and Terraform.
|DB_USER|`archiver`, `dashboard`, `terraform`| Username for authenticating and accessing the database.
|DB_SCHEMA|`archiver`, `dashboard`, `terraform`| Refers to the database schema or namespace within the database.
|DB_PASSWORD|`archiver`, `dashboard`, `terraform`| Used for authentication for the user accessing the RDS.
|DB_PORT|`archiver`, `dashboard`, `terraform`| Port number on which the database server listens for connections.
|DB_NAME|`archiver`, `dashboard`, `terraform`| Name of the database used by the applications and Terraform.

## Folders
- `pipeline`: ETL pipeline that moves data from the API to the RDS
- `archiver`: Moves old data from the RDS to the S3 bucket
- `dashboard`: Interface for the staff members managing the plants
- `terraform`: Provision and manage AWS resources and services
- `diagrams`: Relevant images to the project
- `.github`: Github files required for the repository

> [!IMPORTANT]  
> The project monitors only changes in the `reading` table ([see here](#erd-diagram)). All other data must be manually inserted during creation of the database or by informing the engineers.


