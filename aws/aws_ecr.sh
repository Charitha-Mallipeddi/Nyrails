docker build -t rfc/core -f ./compose/production/django/Dockerfile --platform linux/arm64 .

docker buildx build --platform linux/amd64 --build-arg GIT_COMMIT=$(git log -1 --format=%h) -t rfc/core -f ./compose/production/django/Dockerfile .
docker buildx build --platform linux/amd64 -t rfc/core -f ./compose/production/django/Dockerfile --no-cache --progress=plain .

docker tag rfc/core:latest 205251327187.dkr.ecr.us-east-2.amazonaws.com/rfc/core:latest
aws ecr get-login-password --region us-east-2 | docker login --username AWS --password-stdin 205251327187.dkr.ecr.us-east-2.amazonaws.com
docker push 205251327187.dkr.ecr.us-east-2.amazonaws.com/rfc/core:latest
# aws iam create-role --role-name dev-core-apprunner-role --assume-role-policy-document file://$PWD/aws/trust-policy.json
# aws iam create-policy --policy-name dev-core-apprunner-ecr-policy --policy-document file://$PWD/aws/apprunner-ecr-policy.json
# aws iam attach-role-policy --role-name dev-core-apprunner-role --policy-arn arn:aws:iam::205251327187:policy/dev-core-apprunner-ecr-policy

# aws apprunner create-service --cli-input-yaml file://$PWD/aws/apprunner-core-service.yml

docker run --env-file .envs/.production/.django -p 8080:8000  rfc/core

aws dynamodb delete-table --table-name scan-event --endpoint-url http://localhost:8000
aws dynamodb create-table --cli-input-json file://aws/dynamodb-table-definition.json --endpoint-url http://localhost:8000
aws dynamodb create-table --cli-input-json file://aws/dynamodb-etix-table-definition.json --endpoint-url http://localhost:8000
