workdir='/Dropbox/Research/Topics/Forex' # manuscript location

if [ "$(uname)" == "Darwin" ]; then
    # workdir='/Users/elisa'${workdir}
    workdir='/Volume/dropbox'${workdir}
elif [ "$(expr substr $(uname -s) 1 5)" == "Linux" ]; then
    workdir='/home/elisa'${workdir}
else
    echo 'I have no plans to use this in Win10'
    exit
fi

echo $workdir
echo 'Preprocessing'
for dataset in `ls -1 $workdir/data/*.csv`;
do
    echo $dataset
    label=`basename $dataset .csv`
    echo $label
    python3 heikenashi.py $dataset > ha.csv; gnuplot ha.plot
    python3 avg.py $dataset; gnuplot avg.plot
    python3 macd.py $dataset; gnuplot macd.plot
    python3 stochacticosc.py $dataset > so.csv; gnuplot so.plot
    python3 rsi.py $dataset > rsi.csv; gnuplot rsi.plot
    python3 zigzag.py $dataset > zz.plot; gnuplot zz.plot 2> plot.log
    #grep -v -e '^[[:space:]]*$' demo.csv > noblanks.csv
    python3 psar.py $dataset # this one plots within the python script
    python3 folding.py $dataset; gnuplot fold.plot 2> plot.log
    python3 autocor.py $dataset # this one also plots within the python script
    echo 'Characterizing $dataset' 
    python3 characterize.py $dataset
    sort -R char_2_3.csv | head -n 10 > sample.tex
    sed 's/\s\+/ \& /g;s/$/ \\\\/g' sample.tex > $workdir/sample_$label.tex
    echo 'Training $dataset' 
    python3 train.py > $workdir/perf_$label.tex
    python3 train.py RSI > $workdir/norsi_$label.tex
    python3 train.py RSI MACD > $workdir/nomacd_$label.tex
    mkdir -p $workdir/data/$label
    mv *.csv $workdir/data/$label
    mv *.eps $workdir/data/$label
done
