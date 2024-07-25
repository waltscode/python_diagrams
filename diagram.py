from diagrams import Diagram, Cluster, Edge
from diagrams.aws.compute import ElasticBeanstalk, Lambda
from diagrams.aws.database import RDS
from diagrams.aws.network import ELB, InternetGateway
from diagrams.aws.security import SecretsManager
from diagrams.aws.storage import S3
from diagrams.aws.network import APIGateway  
from diagrams.aws.security import Detective  # adding this detective icon as stand-in for Auth0
with Diagram("Proposed AWS Elastic Beanstalk Environment", show=False):
    
    internet = InternetGateway("Internet Gateway")
    
    auth0 = Detective("Auth0 Login Functionality")  
    api_gateway = APIGateway("API Gateway (HTTP API)")
    
    with Cluster("Public Subnet"):
        alb = ELB("Application Load Balancer")
        web_app = ElasticBeanstalk("Web App Server")
    
    with Cluster("Private Subnet"):
        admin_console = ElasticBeanstalk("Admin Console App Server")
        api_server = ElasticBeanstalk("API Server - Express.js")
        rds = RDS("PostgreSQL Database")
        s3 = S3("S3 Buckets")
        
        with Cluster("AI Services"):
            lambda_transcription = Lambda("MP3 Transcription")
            lambda_summary = Lambda("Summary Transcript")
    
    secrets_manager = SecretsManager("AWS Secrets Manager")
    
    internet >> auth0 >> alb
    alb >> [web_app, api_gateway]
    api_gateway >> [api_server, admin_console]
    api_server >> [rds, s3]
    api_server >> lambda_transcription >> s3
    api_server >> lambda_summary >> s3
    
    secrets_manager >> Edge(style="dashed") >> [api_server, rds]
