RUN_IN_BACKEND=docker-compose -p frank-proctor run --rm backend
GIT_HASH=`git rev-parse --short HEAD`
WEB_SERVER=35.188.222.19

.PHONY: lint
lint:
	$(RUN_IN_BACKEND) pylama .

.PHONY: build-backend
build-backend:
	$(eval IMAGE_TAG := gcr.io/frank-proctor/backend)	
	cd backend && docker build -t $(IMAGE_TAG):$(GIT_HASH) -t $(IMAGE_TAG):latest -f ./Dockerfile .
	docker push $(IMAGE_TAG):$(GIT_HASH)
	docker push $(IMAGE_TAG):latest

.PHONY: build-frontend
build-frontend:
	$(eval IMAGE_TAG := gcr.io/frank-proctor/frontend)	
	cd frontend && docker build -t $(IMAGE_TAG):$(GIT_HASH) -t $(IMAGE_TAG):latest -f ./Dockerfile .
	docker push $(IMAGE_TAG):$(GIT_HASH)
	docker push $(IMAGE_TAG):latest


.PHONY: deploy
deploy: build-backend build-frontend
	ssh oursky@$(WEB_SERVER) bash -i ./update.sh
