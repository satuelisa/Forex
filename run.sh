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
    python3 demo.py $workdir/data/$dataset.csv > daily.dat
    python3 heikenashi.py > ha.dat
    python3 avg.py
    python3 macd.py 
    python3 stochactisosc.py > so.dat
    python3 rsi.py > rsi.dat
    python3 zigzag.py daily.dat > zz.plot; gnuplot zz.plot 2> plot.log
    gnuplot demo.plot 2> plot.log
    #grep -v -e '^[[:space:]]*$' demo.dat > noblanks.dat
    python3 psar.py
    python3 folding.py; gnuplot fold.plot 2> plot.log
    python3 autocor.py $workdir/data/$dataset.csv
    echo 'Characterizing $dataset'
    python3 characterize.py
    sort -R char_2_3.dat | head -n 10 > sample.tex
    sed 's/\s\+/ \& /g;s/$/ \\\\/g' sample.tex > $workdir/sample_$label.tex
    echo 'Training $dataset' 
    python3 train.py > $workdir/perf_$label.tex
    python3 train.py RSI > $workdir/norsi_$label.tex
    python3 train.py RSI MACD > $workdir/nomacd_$label.tex
    mkdir -p $workdir/data/$label
    mv *.dat $workdir/data/$label
    mv *.eps $workdir/data/$label
done
