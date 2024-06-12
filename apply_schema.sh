# Checks if .env file exists
if [ -f .env ]; then
    # If it exists, loads environment variables from it
    source .env
else
    # if it doesn't exist, prints a message and exits with an error
    echo ".env file not found!"
    exit 1
fi

# Runs the sqlcmd command to execute the schema.sql script
sqlcmd -S $DB_HOST -U $DB_USER -P $DB_PASSWORD -d $DB_NAME -i schema.sql