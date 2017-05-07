#!/usr/bin/env bash
old_uwsgi_proc="`ps aux | grep "[u]wsgi "`"
pid="`ps aux | awk '/[u]wsgi / {print $2}'`"
#echo $pid
if [ -n "$pid" ]
    then
    echo "proc old_uwsgi is finded successfully"
    for  x in  $pid
        do
        kill $x
        #echo $x
        done
    #ps aux
    sleep 1    #wait for proc to be killed
    pid="`ps aux | awk '/[u]wsgi / {print $2}'`"
    #echo $pid
    if [ -z "$pid" ]
        then
        echo "proc old_uwsgi is killed successfully"
        cd /home/www/wuji
        uwsgi -x wuji_uwsgi.xml
    else
        echo "proc old_uwsgi is killed failed"
    fi
    #ps aux
    pid="`ps aux | awk '/[u]wsgi / {print $2}'`"
    #echo $pid
    if [ -n "$pid" ]
        then
        echo "proc new_uwsgi is reload successfully"
    else
        echo "proc new_uwsgi is reload failed"
    fi
else
    echo "proc old_uwsgi is not find"
    echo "start new proc uwsgi "
    cd /home/www/wuji
    uwsgi -x wuji_uwsgi.xml
    pid="`ps aux | awk '/[u]wsgi / {print $2}'`"
    #echo $pid
    if [ -n "$pid" ]
        then
        echo "proc new_uwsgi is start successfully"
    else
        echo "proc new_uwsgi is start failed"
    fi
fi
sleep 1   #wait for proc uwsgi start
new_uwsgi_proc="`ps aux | grep "[u]wsgi "`"
echo "********old uwsgi proc**********"
echo "$old_uwsgi_proc"
echo "********new uwsgi proc**********"
echo "$new_uwsgi_proc"
