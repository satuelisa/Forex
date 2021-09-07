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
echo Target directory is $workdir
for dataset in `ls -1 $workdir/data/*.csv`;
do
    echo $dataset
    label=`basename $dataset .csv`
    echo $label
    python3 heikenashi.py $dataset > ha.csv; gnuplot ha.plot 2> plot.log
    python3 avg.py $dataset; gnuplot avg.plot 2> plot.log
    python3 macd.py $dataset; gnuplot macd.plot 2> plot.log
    python3 stochacticosc.py $dataset > so.csv; gnuplot so.plot 2> plot.log
    python3 rsi.py $dataset > rsi.csv; gnuplot rsi.plot 2> plot.log
    python3 zigzag.py $dataset > zz.plot; gnuplot zz.plot 2> plot.log
    #grep -v -e '^[[:space:]]*$' demo.csv > noblanks.csv
    python3 psar.py $dataset # this one plots within the python script
    python3 folding.py $dataset; gnuplot fold.plot 2> plot.log
    python3 autocor.py $dataset # this one also plots within the python script
    echo Characterizing $label
    python3 characterize.py $dataset
    sort -R char_2_3.csv | head -n 10 > sample.tex
    sed 's/\s\+/ \& /g;s/$/ \\\\/g' sample.tex > $workdir/sample_$label.tex
    echo Training $label
    python3 train.py $label > perf_$label.tex
    python3 train.py $label RSI > norsi_$label.tex
    python3 train.py $label RSI MACD > nomacd_$label.tex
    mkdir -p $workdir/data/$label
    mv *.csv $workdir/data/$label
    mv *.eps $workdir/data/$label
done
cat perf_*.tex | sort > perf.tex
cat norsi_*.tex | sort > norsi.tex
cat nomacd_*.tex | sort > nomacd.tex
cat header.tex perf.tex footer.tex > $workdir/perf.tex
cat header.tex norsi.tex footer.tex > $workdir/norsi.tex
cat header.tex nomacd.tex footer.tex > $workdir/nomacd.tex
