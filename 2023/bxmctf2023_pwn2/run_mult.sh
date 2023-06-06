#!/bin/bash
echo "Bash version ${BASH_VERSION}..."
for i in {0..10000..1}
do
  echo "Welcome $i times"
  ./main_moded1 >> m2a.out
done


