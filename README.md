psql "postgresql://root@sam-app-rds-kacte84cjwsw.cgx1jv3igwx5.us-east-1.rds.amazonaws.com:5432/sample_rds?sslmode=require"

# sign up
aws cognito-idp sign-up \
    --client-id 32kam8v6epjun7jbvf9uo1afqn \
    --username llquillo+1@spectrumone.co \
    --password Passw0rd! \
    --user-attributes Name="email",Value="" \
    --region us-east-1 \
    --profile default 

# confirm user
aws cognito-idp admin-confirm-sign-up \
    --user-pool-id us-east-1_F4MBEZQbD \
    --username llquillo+1@spectrumone.co \
    --region  us-east-1 \
    --profile default 

# verify email
aws cognito-idp admin-update-user-attributes \
    --user-pool-id us-east-1_F4MBEZQbD \
    --username llquillo+1@spectrumone.co \
    --user-attributes Name=email_verified,Value=true \
    --region us-east-1 \
    --profile default

# sam-testing
