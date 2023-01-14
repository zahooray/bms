#!/bin/bash

REQ_FILES=(
  "/code/config/requirements/base"
  "/code/config/requirements/dev"
  "/code/config/requirements/stage"
  "/code/config/requirements/prod"
)

for f in "${REQ_FILES[@]}"; do
  rm -f ${f}.txt && pip-compile --generate-hashes -o ${f}.txt ${f}.in || exit 1;
done
