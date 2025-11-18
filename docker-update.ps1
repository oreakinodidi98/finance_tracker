# Set your Docker Hub username
$DOCKER_USER = "oreakinodidi"
$VERSION = "v1.0"

# Login
docker login

# Build and push backend
docker build -t ${DOCKER_USER}/finance-tracker-backend:latest ./backend
docker push ${DOCKER_USER}/finance-tracker-backend:latest
#docker push ${DOCKER_USER}/finance-tracker-backend:${VERSION}

# Build and push frontend
docker build -t ${DOCKER_USER}/finance-tracker-frontend:latest ./frontend
docker push ${DOCKER_USER}/finance-tracker-frontend:latest
#docker push ${DOCKER_USER}/finance-tracker-frontend:${VERSION}

Write-Host "✅ Images pushed successfully!"