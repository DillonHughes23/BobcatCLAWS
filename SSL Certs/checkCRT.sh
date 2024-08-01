#!/bin/bash

KEY_FILE="server.key"
KEY_MD5=$(openssl rsa -noout -modulus -in "$KEY_FILE" | openssl md5)

for CRT_FILE in *.crt; do
  CRT_MD5=$(openssl x509 -noout -modulus -in "$CRT_FILE" | openssl md5)
  echo -n "Checking $CRT_FILE: "
  if [ "$KEY_MD5" == "$CRT_MD5" ]; then
    echo "Match"
  else
    echo "Does not match"
  fi
done

