#!/bin/bash

echo about to Push

git push origin docker
echo Pushed
sleep 75

echo $(travis status)

while [ $(travis status)  == started ] || [ $(travis status)  == created ]
do
   echo $(travis status)
   sleep 10
done

if [ $(travis status) == failed ];
  then
     echo $(travis status)
     echo Failed
     exit
elif [ $(travis status) == passed ];
  then
     echo $(travis status)
     echo run Docker script
     ssh activity . /home/TolaActivity/docker.sh
else
     echo error
fi
