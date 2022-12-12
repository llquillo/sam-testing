psql "postgresql://root@sam-app-rds-1dtwekerckbl.cgx1jv3igwx5.us-east-1.rds.amazonaws.com:5432/sample_rds?sslmode=require"

# sign up
aws cognito-idp sign-up \
    --client-id 29hd70ng2008r139ohdvn9taba \
    --username llquillo+3@spectrumone.co \
    --password Passw0rd! \
    --user-attributes Name="email",Value="" \
    --region us-east-1 \
    --profile default 

# confirm user
aws cognito-idp admin-confirm-sign-up \
    --user-pool-id us-east-1_y4EVS26NR \
    --username llquillo+3@spectrumone.co \
    --region  us-east-1 \
    --profile default 

# verify email
aws cognito-idp admin-update-user-attributes \
    --user-pool-id us-east-1_y4EVS26NR \
    --username llquillo+3@spectrumone.co \
    --user-attributes Name=email_verified,Value=true \
    --region us-east-1 \
    --profile default

# sam-testing
