#!/bin/bash
#===============================================================
export HEADER='\033[95m'
export OKBLUE='\033[94m'
export OKGREEN='\033[92m'
export WARNING='\033[93m'
export FAIL='\033[91m'
export ENDC='\033[0m'
export BOLD='\033[1m'
export UNDERLINE='\033[4m'
#===============================================================

V=$(date "+%Y%m%d_%H%M%S")
PROJECT="constant-money"
NAMESPACE=$1
BACKEND_IMAGE="$NAMESPACE-loan-backend-service"

if [ $1 = "staging" ]
then
    cp -a ./deployments/staging.py ./src/conf/settings/local.py
fi

if [ $1 = "production" ]
then
    cp -a ./deployments/production.py ./src/conf/settings/local.py
fi

# Do migration
python ./src/manage.py migrate --settings=conf.settings.local

buildNumber=$V
docker build \
    -t gcr.io/$PROJECT/$BACKEND_IMAGE:$buildNumber .
docker tag gcr.io/$PROJECT/$BACKEND_IMAGE:$buildNumber gcr.io/$PROJECT/$BACKEND_IMAGE:$buildNumber

gcloud auth activate-service-account --key-file ./deployments/deploy.cred.json
gcloud container clusters get-credentials service-cluster-1 --zone asia-southeast1-a --project constant-money
gcloud docker -- push gcr.io/$PROJECT/$BACKEND_IMAGE:$buildNumber

result=$(echo $?)
if [ $result != 0 ] ; then
    echo "$FAIL failed gcloud docker -- push gcr.io/$PROJECT/$BACKEND_IMAGE:buildNumber $V $ENDC";
    exit;
else
    echo "$OKGREEN gcloud docker -- push gcr.io/$PROJECT/$BACKEND_IMAGE:buildNumber $V $ENDC"
fi

kubectl --namespace=$NAMESPACE set image deployment/loan-backend-service loan-backend-service=gcr.io/$PROJECT/$BACKEND_IMAGE:$buildNumber

result=$(echo $?)
if [ $result != 0 ] ; then
    echo "$FAIL failed kubectl --namespace=$NAMESPACE set image deployment/loan-backend-service loan-backend-service=gcr.io/$PROJECT/$BACKEND_IMAGE:$buildNumber $ENDC";
    exit;
else
    echo "$OKGREEN DEPLOY SUCESSFULL gcr.io/$PROJECT/$BACKEND_IMAGE:$buildNumber $ENDC"
fi
