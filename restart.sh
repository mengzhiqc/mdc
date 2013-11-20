ps aux|grep 'python code.py'|awk '{print $2}' |while read line
do
    kill -9 $line
done

