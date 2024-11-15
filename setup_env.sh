#!/bin/bash

if [ -f .env ]; then
  export $(cat .env | xargs)
  echo "excport .env complete."
fi

