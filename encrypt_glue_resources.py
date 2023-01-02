import boto3

# Create a client for the Glue service
glue = boto3.client('glue')

key_id = input('KMS key Id : ')

# Get a list of all Glue databases
databases = glue.get_databases()['DatabaseList']

# Iterate over the list of databases and encrypt each one
for database in databases:
    database_name = database['Name']
    update_database_response = glue.update_database(
        Name=database_name,
        DatabaseInput={
            'Name': database_name,
            'Parameters': {
                'encryption_type': 'SSE-KMS',
                'kms_key_id': f'{key_id}'
            }
        }
    )

    # Get a list of all Glue tables
    tables = glue.get_tables(DatabaseName=database)['TableList']
    
    # Iterate over the list of tables and encrypt each one
    for table in tables:
        table_name = table['Name']
        table_input = glue.get_table(DatabaseName=database, Name=table_name)
        update_table_response = glue.update_table(
            DatabaseName=database,
            TableInput={
                'Name': table_name,
                'StorageDescriptor': {
                    'Columns': table_input['Table']['StorageDescriptor']['Columns'],
                    'Location': table_input['Table']['StorageDescriptor']['Location'],
                    'InputFormat': table_input['Table']['StorageDescriptor']['InputFormat'],
                    'OutputFormat': table_input['Table']['StorageDescriptor']['OutputFormat'],
                    'SerdeInfo': table_input['Table']['StorageDescriptor']['SerdeInfo'],
                    'Parameters': {
                        'encryption_type': 'SSE-KMS',
                        'kms_key_id': f'{key_id}'
                    }
                }
            }
        )
