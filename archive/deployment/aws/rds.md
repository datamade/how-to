# AWS Relational Database Service (RDS)

This doc presents guides on working with AWS RDS, Amazon's Database-as-a-Service provider.

## Connecting with an EC2 instance

In order to connect to an RDS instance from an EC2 instance, you'll need to configure the security rules for the database to allow access from the instance. Broadly speaking, AWS allows you to do this by 1) creating the database and the EC2 instance in the same Virtual Private Cloud (VPC) and 2) creating an inbound rule for the database's security group that permits access to PostgreSQL from the EC2 instance's security group.

This process is useful when you have a database that is running in a VPC and that does not have access to the public Internet. Generally, we consider it a best practice to provision databases this way, so that they are protected from attacks over the Internet. For an example of a project that uses this configuration, see https://gitlab.com/ChicagoDataCooperative/court-terminal.

These instructions are loosely based on [AWS's official documentation](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_VPC.Scenarios.html#USER_VPC.Scenario1). They assume that you already have an RDS instance up and running in a private VPC (docs forthcoming).

### 1. Create the EC2 instance in the same VPC as the database

- Navigate to the page for your database in the RDS console.
- Under `Connectivity & security > Networking > VPC`, copy the ID of the VPC that the database runs in.
- Navigate to the EC2 console and begin to launch an EC2 instance [following our guide](https://github.com/datamade/deploy-a-site/blob/master/Launch-a-new-EC2-Instance.md)
    - During Step 3, the "Configure Instance Details" page, specify the following options:
        - For `Network`, select the VPC matching the ID that you copied above. This will launch your instance in the same VPC as your database.
        - For `Subnet`, Select any public subnet. This will allow the EC2 instance to access the public Internet.
    - During Step 6, the "Configure Security Group" page, create a new security group for this instance instead of using the `default`. Give it any HTTP/SSH access rules you need for your application.
    - Finish launching the instance as normal.

### 2. Use security groups to grant the EC2 instance access to the database

- In the EC2 console, click on the name of the security group that you created for your new EC2 instance, and copy the security group ID.
- In the RDS console, navigate to the security group for your database.
- In the detail view for your database's security group, select `Inbound > Edit > Add Rule` with the following attributes:
    - Type: `PostgreSQL`
    - Protocol: `TCP`
    - Port range: `5432`
    - Source: `Custom`, and paste in the value of the EC2 instance security group from above
- Shell into your server and test that you can access your database by [opening up an SSH tunnel](/postgres/Interacting-with-a-remote-database.md) to your RDS instance and attempting to `psql` into the database. (N.b., you can find the URL to your RDS instance on the database detail page in the RDS console.)
