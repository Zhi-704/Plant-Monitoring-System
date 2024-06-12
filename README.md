# LMNH Pipeline

This repository contains the all the code, documentation and resources required for the pipeline for Liverpool Natural History Museum. The pipeline serves to monitor the health of the plants over time in the botanical wing of the museum and alerts the gardeners when there is a problem.



## Requirements

1. Clone this repository:
    ```sh
    git clone https://github.com/danfh00/vodnik-plant-health-monitor.
    ```

2. Navigate to the directory and install the required packages in the terminal:
    ```sh
    cd [PATH_TO_FOLDER]/C11-Kappa-Group-Project
    pip3 install -r requirements.txt
    ```


## Archictecture Diagram

To view the archictecture diagram for the project, please refer to this diagram [here](https://github.com/Zhi-704/C11-Kappa-Group-Project/blob/main/diagrams/Architecture_Diagram.png).

## Database Schema

To view the database schema for the plant data, please refer to this Entity-Relationship Diagram (ERD) [here](https://github.com/Zhi-704/C11-Kappa-Group-Project/blob/main/diagrams/ERD_diagram.png).

**Secrets/Authentication**
> [!IMPORTANT]  
> To be able to run these scripts the following details must be provided in the `.env` file.

| KEY |Files Required|
| -------- | --------|
|DB_HOST|`load.py`,`main.py`|
|DB_USER|`load.py`,`main.py`|
|DB_SCHEMA|`load.py`,`main.py`|
|DB_PASSWORD|`load.py`,`main.py`|
|DB_PORT|`load.py`,`main.py`|
|DB_NAME|`load.py`,`main.py`|

## Folders
- `pipeline`: code for the ETL pipeline from the API to the database
- `archiver`: code that moves old data from database to an s3 bucket
- `diagrams`: relevant images to the project
- `.github`: github files required for the repository

> [!IMPORTANT]  
> The project monitors only changes in the `reading` table ([see here](https://github.com/Zhi-704/C11-Kappa-Group-Project/blob/main/diagrams/ERD_diagram.png)). All other data must be manually inserted during creation of the database.


