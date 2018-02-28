now=$(date +"%Y%m%d_%H%M%S")
JOB_NAME="msc_thesis_$now"

TRAINER_PACKAGE_PATH="src"
MAIN_TRAINER_MODULE="src.trainer"
BUCKET="gs://msc-thesis-train-data"
PACKAGE_STAGING_PATH="$BUCKET/train/staging"
JOB_DIR="$BUCKET/train/$JOB_NAME"
INPUT_DIR="$BUCKET"
REGION="europe-west1"
SCALE_TIER="basic_gpu"

pipenv run gcloud ml-engine local train \
    --job-dir $JOB_DIR  \
    --package-path $TRAINER_PACKAGE_PATH \
    --module-name $MAIN_TRAINER_MODULE \
    -- \
    --train-data-root $INPUT_DIR \
    --train-data-records electronic_um.tfrecords metal_um.tfrecords classical_um.tfrecords