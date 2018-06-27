com_args=""
var_bs_args=""
mix_read_args=""
for arg in "$@" 
do
    com_args+=" -i ${arg}/com"
    var_bs_args+=" -i ${arg}/var-bs"
    mix_read_args+=" -i ${arg}/mixread"
done

function generate {
    cmd="python $@"
    echo $cmd
    eval $cmd

    ret=$?
    if [ $ret -ne 0 ]
    then
        exit $ret
    fi
}

generate parse_latency.py ${com_args}
generate parse_bw.py ${com_args}
generate parse_var_bs.py ${var_bs_args}
generate parse_rwmixread_bw.py ${mix_read_args}
