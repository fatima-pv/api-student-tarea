# api-student-tarea

## Endpoints
- `GET /` → healthcheck (200 OK)
- `GET /students`
- `POST /students` (form-data o JSON con: firstname, lastname, gender, age)
- `GET /student/<id>`
- `PUT /student/<id>`
- `DELETE /student/<id>`

## Run local (opcional)
```bash
python db.py
python app.py
# http://localhost:3000
```

## Docker
```bash
docker build -t crud-sqlite-api:v1 .
docker run --rm -p 3000:3000 crud-sqlite-api:v1
```

## ECR (ejemplo)
```bash
ACCOUNT_ID=XXXXXXXXXXXX
REGION=us-east-1
ECR_REPO=crud-sqlite-api
IMAGE_TAG=v1
IMAGE_URI=$ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com/$ECR_REPO:$IMAGE_TAG

aws ecr create-repository --repository-name $ECR_REPO --region $REGION || true
aws ecr get-login-password --region $REGION | docker login --username AWS --password-stdin $ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com
docker tag crud-sqlite-api:v1 $IMAGE_URI
docker push $IMAGE_URI
```

## Pulumi (variables típicas)
```bash
export IMAGE_URI=$ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com/$ECR_REPO:$IMAGE_TAG
export LAB_ROLE_ARN=arn:aws:iam::$ACCOUNT_ID:role/LabRole
export APP_PORT=3000
pulumi up --yes
```
