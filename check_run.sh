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
        cd $path; python3 checkin.py
fi
