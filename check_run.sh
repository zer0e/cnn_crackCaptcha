#!/bin/sh
proc_name="recognize_api.py"
path=$(cd `dirname $0`; pwd)
proc_num(){
        num=`ps -ef | grep $proc_name | grep -v grep | wc -l`
        return $num
}
proc_num
number=$?
if [ $number -eq 0 ]
then
        cd $path; python3 recognize_api.py
else
        id=`ps -ef | grep $proc_name | grep -v grep | awk '{print $2}'`
        `kill -s 9 $id`
        cd $path; python3 recognize_api.py
fi

