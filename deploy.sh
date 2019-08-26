#!/bin/bash

for i in "$@"
do
case $i in
    --token=*)
	OKC_TOKEN="${i#*=}"
	shift
	;;
	--project=*)
	OKC_PROJECT="${i#*=}"
	shift
	;;
	--release_tag=*)
	RELEASE_TAG="${i#*=}"
	shift
	;;
	--node=*)
	NODES[NODE_INDEX]="${i#*=}"
	NODE_INDEX=$((NODE_INDEX + 1))
	shift
	;;
	-h|--help)
	echo "Usage:"
	echo "run_lwce.ch [--ip=<value>] [--host=<value>] [--net=<overlay_network_name>] [[--node=<hostname:ip>] [--node=<hostname:ip>] ...]"
	printf "\n"
	echo "Options:"
	echo "1. ip: REQUIRED; The IP address to be assigned to the container."
	echo "2. net: REQUIRED; The name of the attachable overlay network to which the container should attach on startup. You should already have created an attachable overlay network on your swarm manager."
	echo "3. node: OPTIONAL; HOSTNAME:IP of other nodes on the same docker swarm network. The /etc/hosts inside the current container is appended with this info."
	exit 0
	shift
	;;
esac
done
if [ -z "$RELEASE_TAG" ]
then
	echo "Please specify the git repository tag/branch that should be deployed in production."
# elif [ -z "$NET" ]
# then
# 	echo "Please specify the name of the attachable docker overlay network that the container should connect to on startup."
# 	exit 1
# fi
# if [ $NODE_INDEX -eq 0 ]
# then
# 	echo "Please note that no additional nodes have been specified. Therefore the /etc/hosts file in the container won't be modified. This could potentially create some troubles when trying to communicate over the overlay network."
# 	sleep 5
fi
GIT_REPO=$(git remote get-url origin)
GIT_BRANCH=$(git branch | grep \* | cut -d ' ' -f2)
oc login https://openshift-dev.cern.ch --token=${OKC_TOKEN}
oc project ${OKC_PROJECT}
oc status
oc create -f $(pwd)/openshift/templates/rucio-opint-backend.json
oc new-app $(pwd)/openshift/templates/rucio-opint-backend.json \
    -p SOURCE_REPOSITORY=$GIT_REPO
    -p SOURCE_REPOSITORY_REF=$RELEASE_TAG
