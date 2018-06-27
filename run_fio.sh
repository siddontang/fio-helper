#!/bin/bash



mkdir -p ./log/com ./log/mixread ./log/var-bs

args="--output-format json \
    -filename=test \
    -filesize=16m \
    -thread \
    -runtime=60 \
    -numjobs=4 \
    -ioengine=libaio \
    -direct=1 \
    -name=\"FIO test\""

function run_fio {
    cmd="fio ${args} $1"
    echo $cmd
    eval $cmd

    ret=$?
    if [ $ret -ne 0 ]
    then
        exit $ret
    fi
}

for iodepth in 1 2 4 8 16 32
do
    echo "100% write 4k with different iodepth" ${iodepth}
    run_fio "-rw=write --output ./log/com/write-4k-iodepth${iodepth} -bs=4k -iodepth=${iodepth}"

    echo "100% read 4k with different iodepth" ${iodepth}
    run_fio "-rw=read --output ./log/com/read-4k-iodepth${iodepth} -bs=4k -iodepth=${iodepth}"

    echo "70% read 4k and 30% write 4k with different iodepth" ${iodepth}
    run_fio "-rw=readwrite --output ./log/com/read70-write-4k-iodepth${iodepth} -bs=4k -iodepth=${iodepth} -rwmixread=70"
done 

for mixread in 100 90 80 70 60 50
do
    mixwrite=$((100 - ${mixread}))
    echo ${mixread}% "read 4k and" ${mixwrite}% "write 4k with 32 iodepth"
    run_fio "-rw=readwrite --output ./log/mixread/read${mixread}-4k-iodepth32 -iodepth=32 -bs=4k -rwmixread=${mixread}"

    echo ${mixread}% "read 4k and" ${mixwrite}% "write 128k with 32 iodepth"
    run_fio "-rw=readwrite --output ./log/mixread/read${mixread}-4k-write-128k-iodepth32 -iodepth=32 -bs=4k,128k -rwmixread=${mixread}"
done

for iodepth in 1 2 4 8
do 
    for bs in 4k 8k 32k 64k
    do
        echo "write" ${bs} "with iodepth" ${iodepth}
        run_fio "-rw=write --output ./log/var-bs/write-${bs}-iodepth${iodepth} -bs=${bs} -iodepth=${iodepth}"

        echo "read" ${bs} "with iodepth" ${iodepth}
        run_fio "-rw=read --output ./log/var-bs/read-${bs}-iodepth${iodepth} -bs=${bs} -iodepth=${iodepth}"
    done
done 