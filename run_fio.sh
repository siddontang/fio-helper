#!/bin/bash

m_bs=(4k 16k 32k 64k)
m_jobs=(read write readwrite randread randwrite randrw)
m_iodepths=(4 8 16)

NUMJOBS=${NUMJOBS=1}

echo concurrency ${NUMJOBS}

mkdir -p ./log

for job in ${m_jobs[@]}
do 
    for bs in ${m_bs[@]}
    do 
        echo psync ${job} ${bs} cache
        fio fio.fio --section ${job} --output-format json --output ./log/psync-${job}-bs${bs}-thread${NUMJOBS}-cache -ioengine=psync -bs=${bs} -numjobs=${NUMJOBS}
        echo psync ${job} ${bs} direct 
        fio fio.fio --section ${job} --output-format json --output ./log/psync-${job}-bs${bs}-thread${NUMJOBS}-direct -ioengine=psync -bs=${bs} -numjobs=${NUMJOBS} -direct=1
        echo psync ${job} ${bs} sync
        fio fio.fio --section ${job} --output-format json --output ./log/psync-${job}-bs${bs}-thread${NUMJOBS}-sync -ioengine=psync -bs=${bs} -numjobs=${NUMJOBS} -fdatasync=1
        for iodepth in ${m_iodepths[@]} 
        do 
            echo libaio ${job} ${bs} iodepth${iodepth}
            fio fio.fio --section ${job} --output-format json --output ./log/libaio-${job}-bs${bs}-thread${NUMJOBS}-iodepth${iodepth} -ioengine=libaio -bs=${bs} -numjobs=${NUMJOBS} -direct=1 -iodepth=${iodepth}
        done 
    done 
done 


