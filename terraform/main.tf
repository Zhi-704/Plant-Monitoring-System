provider "aws" {
    region = var.AWS_REGION
    access_key = var.ACCESS_KEY
    secret_key = var.SECRET_ACCESS_KEY
}

# terraform import aws_lambda_function.c11-kappa-archiver-lambda c11-kappa-archiver-lambda
resource "aws_lambda_function" "c11-kappa-archiver-lambda" {
    function_name                  = "c11-kappa-archiver-lambda"
    image_uri                      = "129033205317.dkr.ecr.eu-west-2.amazonaws.com/c11-kappa-archiver:latest"
    package_type                   = "Image"
    role                           = "arn:aws:iam::129033205317:role/service-role/c11-kappa-archiver-lambda-role-41hfhx92"
    timeout                        = 120

    environment {
        variables = {
            "ACCESS_KEY"        = var.ACCESS_KEY
            "BUCKET_NAME"       = var.BUCKET_NAME
            "DB_HOST"           = var.DB_HOST
            "DB_NAME"           = var.DB_NAME
            "DB_PASSWORD"       = var.DB_PASSWORD
            "DB_PORT"           = var.DB_PORT
            "DB_SCHEMA"         = var.DB_SCHEMA
            "DB_USER"           = var.DB_USER
            "SECRET_ACCESS_KEY" = var.SECRET_ACCESS_KEY
        }
    }

    logging_config {
        log_format = "Text"
        log_group  = "/aws/lambda/c11-kappa-archiver-lambda"
    }

    tracing_config {
        mode = "PassThrough"
    }
}

# terraform import aws_lambda_function.c11-kappa-pipeline c11-kappa-pipeline
resource "aws_lambda_function" "c11-kappa-pipeline" {
    function_name                  = "c11-kappa-pipeline"
    image_uri                      = "129033205317.dkr.ecr.eu-west-2.amazonaws.com/c11-kappa-group-pipeline:latest"
    package_type                   = "Image"
    role                           = "arn:aws:iam::129033205317:role/service-role/c11-kappa-pipeline-role-fcj1rlek"
    timeout                        = 50

    environment {
        variables = {
            "DB_HOST"     = var.DB_HOST
            "DB_NAME"     = var.DB_NAME
            "DB_PASSWORD" = var.DB_PASSWORD
            "DB_PORT"     = var.DB_PORT
            "DB_USER"     = var.DB_USER
        }
    }

    logging_config {
        log_format = "Text"
        log_group  = "/aws/lambda/c11-kappa-pipeline"
    }

    tracing_config {
        mode = "PassThrough"
    }
}

# terraform import aws_s3_bucket.c11-kappa-group-s3-bucket c11-kappa-group-s3-bucket
resource "aws_s3_bucket" "c11-kappa-group-s3-bucket" {
    bucket                      = "c11-kappa-group-s3-bucket"
    force_destroy               = true
    object_lock_enabled         = false
}

# terraform import aws_s3_bucket_ownership_controls.c11-kappa-group-s3-bucket-ownership c11-kappa-group-s3-bucket
resource "aws_s3_bucket_ownership_controls" "c11-kappa-group-s3-bucket-ownership" {
    bucket = "c11-kappa-group-s3-bucket"

    rule {
        object_ownership = "ObjectWriter"
    }
}

# terraform import aws_s3_bucket_acl.c11-kappa-group-s3-bucket-acl c11-kappa-group-s3-bucket
resource "aws_s3_bucket_acl" "c11-kappa-group-s3-bucket-acl" {
    bucket = "c11-kappa-group-s3-bucket"

    access_control_policy {
        grant {
            permission = "FULL_CONTROL"

            grantee {
                id   = "c3c9c6dec6716abc6b40931d6645cb2bca0ce3be2559f1a49e02d41b6f8cda90"
                type = "CanonicalUser"
            }
        }
        owner {
            id = "c3c9c6dec6716abc6b40931d6645cb2bca0ce3be2559f1a49e02d41b6f8cda90"
        }
    }
}

# terraform import aws_s3_bucket_server_side_encryption_configuration.c11-kappa-group-s3-bucket-encryption c11-kappa-group-s3-bucket
resource "aws_s3_bucket_server_side_encryption_configuration" "c11-kappa-group-s3-bucket-encryption" {
    bucket = "c11-kappa-group-s3-bucket"

    rule {
        apply_server_side_encryption_by_default {
            sse_algorithm = "AES256"
        }
    }
}

# terraform import aws_s3_bucket_versioning.c11-kappa-group-s3-bucket-versioning c11-kappa-group-s3-bucket
resource "aws_s3_bucket_versioning" "c11-kappa-group-s3-bucket-versioning" {
    bucket = "c11-kappa-group-s3-bucket"

    versioning_configuration {
        status = "Disabled"
    }
}

# terraform import aws_scheduler_schedule.c11-kappa-pipeline-every-min default/c11-kappa-pipeline-every-min
resource "aws_scheduler_schedule" "c11-kappa-pipeline-every-min" {
    description                  = "Runs the pipeline lambda function every minute"
    name                         = "c11-kappa-pipeline-every-min"
    schedule_expression          = "cron(* * * * ? *)"
    schedule_expression_timezone = "Europe/London"

    flexible_time_window {
        mode                      = "OFF"
    }

    target {
        arn      = "arn:aws:lambda:eu-west-2:129033205317:function:c11-kappa-pipeline"
        role_arn = "arn:aws:iam::129033205317:role/service-role/Amazon_EventBridge_Scheduler_LAMBDA_2a5802cc60"

        retry_policy {
            maximum_event_age_in_seconds = 60
            maximum_retry_attempts       = 60
        }
    }
}

# terraform import aws_scheduler_schedule.c11-kappa-archiver-daily default/c11-kappa-archiver-daily
resource "aws_scheduler_schedule" "c11-kappa-archiver-daily" {
    description                  = "Runs the archiver lambda function every day"
    name                         = "c11-kappa-archiver-daily"
    schedule_expression          = "cron(0 0 * * ? *)"
    schedule_expression_timezone = "Europe/London"

    flexible_time_window {
        mode                      = "OFF"
    }

    target {
        arn      = "arn:aws:lambda:eu-west-2:129033205317:function:c11-kappa-archiver-lambda"
        role_arn = "arn:aws:iam::129033205317:role/service-role/Amazon_EventBridge_Scheduler_LAMBDA_f313f5cf9d"
    }
}

# terraform import aws_ecs_task_definition.c11-kappa-dashboard arn:aws:ecs:eu-west-2:129033205317:task-definition/c11-kappa-dashboard:2
resource "aws_ecs_task_definition" "c11-kappa-dashboard" {
    container_definitions    = jsonencode(
        [
            {
                cpu             = 0
                environment     = [
                    {
                        name  = "ACCESS_KEY"
                        value = var.ACCESS_KEY
                    },
                    {
                        name  = "BUCKET_NAME"
                        value = var.BUCKET_NAME
                    },
                    {
                        name  = "DB_HOST"
                        value = var.DB_HOST
                    },
                    {
                        name  = "DB_NAME"
                        value = var.DB_NAME
                    },
                    {
                        name  = "DB_PASSWORD"
                        value = var.DB_PASSWORD
                    },
                    {
                        name  = "DB_PORT"
                        value = var.DB_PORT
                    },
                    {
                        name  = "DB_SCHEMA"
                        value = var.DB_SCHEMA
                    },
                    {
                        name  = "DB_USER"
                        value = var.DB_USER
                    },
                    {
                        name  = "SECRET_ACCESS_KEY"
                        value = var.SECRET_ACCESS_KEY
                    },
                ]
                essential        = true
                image            = "129033205317.dkr.ecr.eu-west-2.amazonaws.com/c11-kappa-dashboard"
                logConfiguration = {
                    logDriver     = "awslogs"
                    options       = {
                        awslogs-create-group  = "true"
                        awslogs-group         = "/ecs/c11-kappa-dashboard"
                        awslogs-region        = "eu-west-2"
                        awslogs-stream-prefix = "ecs"
                    }
                }
                name             = "c11-kappa-dashboard"
                portMappings     = [
                    {
                        appProtocol   = "http"
                        containerPort = 80
                        hostPort      = 80
                        name          = "c11-kappa-dashboard-80-tcp"
                        protocol      = "tcp"
                    },
                ]
            },
        ]
    )
    cpu                      = "1024"
    execution_role_arn       = "arn:aws:iam::129033205317:role/ecsTaskExecutionRole"
    family                   = "c11-kappa-dashboard"
    memory                   = "3072"
    network_mode             = "awsvpc"
    requires_compatibilities = [
        "FARGATE",
    ]
    track_latest             = true

    runtime_platform {
        cpu_architecture        = "X86_64"
        operating_system_family = "LINUX"
    }
}

# terraform import aws_ecs_task_definition.c11-kappa-archiver-td arn:aws:ecs:eu-west-2:129033205317:task-definition/c11-kappa-archiver-td:1
resource "aws_ecs_task_definition" "c11-kappa-archiver-td" {
    container_definitions    = jsonencode(
        [
            {
                cpu              = 0
                environment      = [
                    {
                        name  = "ACCESS_KEY"
                        value = var.ACCESS_KEY
                    },
                    {
                        name  = "DB_HOST"
                        value = var.DB_HOST
                    },
                    {
                        name  = "DB_NAME"
                        value = var.DB_NAME
                    },
                    {
                        name  = "DB_PASSWORD"
                        value = var.DB_PASSWORD
                    },
                    {
                        name  = "DB_PORT"
                        value = var.DB_PORT
                    },
                    {
                        name  = "DB_SCHEMA"
                        value = var.DB_SCHEMA
                    },
                    {
                        name  = "DB_USER"
                        value = var.DB_USER
                    },
                    {
                        name  = "SECRET_ACCESS_KEY"
                        value = var.SECRET_ACCESS_KEY
                    },
                ]
                essential        = true
                image            = "129033205317.dkr.ecr.eu-west-2.amazonaws.com/c11-kappa-archiver:latest"
                logConfiguration = {
                    logDriver     = "awslogs"
                    options       = {
                        awslogs-create-group  = "true"
                        awslogs-group         = "/ecs/c11-kappa-archiver-td"
                        awslogs-region        = "eu-west-2"
                        awslogs-stream-prefix = "ecs"
                    }
                }
                name             = "c11-kappa-archive"
                portMappings     = [
                    {
                        appProtocol   = "http"
                        containerPort = 80
                        hostPort      = 80
                        name          = "c11-kappa-archive-80-tcp"
                        protocol      = "tcp"
                    },
                ]
            },
        ]
    )
    cpu                      = "1024"
    execution_role_arn       = "arn:aws:iam::129033205317:role/ecsTaskExecutionRole"
    family                   = "c11-kappa-archiver-td"
    memory                   = "3072"
    network_mode             = "awsvpc"
    requires_compatibilities = [
        "FARGATE",
    ]
    track_latest             = true

    runtime_platform {
        cpu_architecture        = "X86_64"
        operating_system_family = "LINUX"
    }
}

# terraform import aws_ecs_service.c11-kappa-dashboard-service c11-ecs-cluster/c11-kappa-dashboard-service
resource "aws_ecs_service" "c11-kappa-dashboard-service" {
    cluster                            = "arn:aws:ecs:eu-west-2:129033205317:cluster/c11-ecs-cluster"
    deployment_maximum_percent         = 200
    deployment_minimum_healthy_percent = 100
    desired_count                      = 1
    enable_ecs_managed_tags            = true
    enable_execute_command             = false
    iam_role                           = "/aws-service-role/ecs.amazonaws.com/AWSServiceRoleForECS"
    launch_type                        = "FARGATE"
    name                               = "c11-kappa-dashboard-service"
    task_definition                    = "c11-kappa-dashboard"

    deployment_circuit_breaker {
        enable   = true
        rollback = true
    }

    network_configuration {
        assign_public_ip = true
        security_groups  = [
            "sg-000efe4b9fbb01850",
        ]
        subnets          = [
            "subnet-07de213eeae1f6307",
            "subnet-08781450402b81aa2",
            "subnet-0e6c6a8f959dae31a",
        ]
    }
}