#!/bin/bash
echo "Check whether it is the master"

cluster_id=$(cat /mnt/var/lib/info/job-flow.json | jq -r ".jobFlowId")

host_private_ip=$(hostname -i)
master_private_ip=$(aws emr list-instances \
                        --cluster-id $cluster_id \
                        --instance-group-types "MASTER" \
                        --query "Instances[0].PrivateIpAddress" \
                        --output text)

# Check whether it is the master. If it isn't -> exit
if [ $host_private_ip != $master_private_ip ]
then
    echo "exit 0"
    exit 0
fi

echo "Check whether the file with data exists"

aws s3 ls s3://YOUR_BUCKET/data/reviews_Electronics_5.json

# Check whether the file with data exists. If so -> exit
if [ $? = 0 ]
then
    echo "exit 0"
    exit 0
fi


wget http://snap.stanford.edu/data/amazon/productGraph/categoryFiles/reviews_Electronics_5.json.gz -P "/home/hadoop"
gzip -d /home/hadoop/reviews_Electronics_5.json.gz

echo "Check whether the bucket exists"

aws s3 ls "s3://aws-bigdata"

# Check whether the bucket exists. If it doesn't -> create the one
if [ $? = 255 ]
then
    echo "Doesn't exist"
    aws s3 mb s3://YOUR_BUCKET
fi

aws s3api put-object --bucket aws-bigdata --key data/
aws s3 cp /home/hadoop/reviews_Electronics_5.json s3://YOUR_BUCKET/data/reviews_Electronics_5.json

