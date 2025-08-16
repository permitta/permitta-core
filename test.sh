#! /bin/bash

if [ $1 == 'opa' ]
then
  opa test opa/trino -v

elif [ $1 == 'bundle' ]
then
  mkdir tmp
  cd tmp
  wget wget localhost:8000/v1/opa/bundle/trino -O trino.tar.gz
  tar -zxvf trino.tar.gz
  ls
elif [ $1 == 'format' ]
then
  autoflake --in-place --remove-unused-variables -r permitta-core
fi