import boto3

# Set the SSL certificate identifier
ssl_certificate_identifier = input('SSL Certificate Identifier : ')

# Create an RDS client
rds_client = boto3.client('rds')

# Get a list of all DB clusters in the account
response = rds_client.describe_db_clusters()

# Iterate through the list of DB clusters and modify each one to enforce SSL
for db_cluster in response['DBClusters']:
    db_cluster_identifier = db_cluster['DBClusterIdentifier']
    rds_client.modify_db_cluster(DBClusterIdentifier=db_cluster_identifier,
                                 CertificateAuthorityArn=ssl_certificate_identifier,
                                 EnableIAMDatabaseAuthentication=True)
