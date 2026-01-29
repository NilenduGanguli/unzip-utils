#!/bin/bash
# Wait for SQL Server to be ready
echo "Waiting for SQL Server to be ready..."
for i in {1..50};
do
    /opt/mssql-tools18/bin/sqlcmd -C -S sql-server -U sa -P "$MSSQL_SA_PASSWORD" -Q "SELECT 1" > /dev/null 2>&1
    if [ $? -eq 0 ]
    then
        echo "SQL Server is ready."
        break
    else
        echo "Not ready yet..."
        sleep 1
    fi
done

# Run the initialization script
echo "Running initialization script..."
/opt/mssql-tools18/bin/sqlcmd -C -S sql-server -U sa -P "$MSSQL_SA_PASSWORD" -i /init.sql
