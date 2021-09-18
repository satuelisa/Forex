# USAGE: bash run.sh > log.txt

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
echo 'DT scores' > dt.txt
starttime=$(date +%s.%N)
for dataset in `ls -1 $workdir/data/*.csv`;
do
    label=`python3 clean.py $dataset`
    echo $label
    # additional indicators that are not presently 
    python3 psar.py $dataset # this one plots within the python script
    python3 folding.py $dataset; gnuplot fold.plot 2> plot.log
    python3 autocor.py $dataset # this one also plots within the python script
    # the indicators used as features
    python3 heikenashi.py $dataset > ha.csv; gnuplot ha.plot 2> plot.log
    python3 avg.py $dataset; gnuplot avg.plot 2> plot.log
    python3 macd.py $dataset; gnuplot macd.plot 2> plot.log
    python3 stochacticosc.py $dataset > so.csv; gnuplot so.plot 2> plot.log
    python3 rsi.py $dataset > rsi.csv; gnuplot rsi.plot 2> plot.log
    python3 zigzag.py $dataset > zz.plot; gnuplot zz.plot 2> plot.log
    #grep -v -e '^[[:space:]]*$' demo.csv > noblanks.csv
    echo Characterizing $label
    python3 characterize.py $dataset
    mkdir -p $workdir/data/$label
    cp *.csv $workdir/data/$label
#    sort -R char_2_3.csv | head -n 10 > sample.tex
#    sed 's/\s\+/ \& /g;s/$/ \\\\/g' sample.tex > $workdir/sample_$label.tex
    echo Training $label with all the features
    python3 train.py $label > perf_$label.tex
    echo Training $label without RSI
    python3 train.py $label RSI > norsi_$label.tex
    echo Training $label without RSI and MACD    
    python3 train.py $label RSI MACD > nomacd_$label.tex
    echo Training $label with only RSI and SMA
    python3 train.py $label EMA ZZS HA MACD SO > rsisma_$label.tex
    echo Training $label with only RSI and EMA
    python3 train.py $label ZZS HA MACD SO SMA > rsiema_$label.tex 
    echo Training $label with only SMA
    python3 train.py $label EMA ZZS HA MACD SO RSI > sma_$label.tex dt
done
endtime=$(date +%s.%N)
duration=$((end-start))
echo The process took $duration seconds

# build the LaTeX tables of the results

cat perf_*.tex | sort | grep total > bottom1.tex
cat perf_*.tex | sort | grep -v total > top1.tex
cat header.tex top1.tex sep.tex bottom1.tex footer.tex > $workdir/perf.tex

cat norsi_*.tex | sort | grep total > bottom2.tex
cat norsi_*.tex | sort | grep -v total > top2.tex
cat header.tex top2.tex sep.tex bottom2.tex footer.tex > $workdir/norsi.tex

cat nomacd_*.tex | sort | grep total > bottom3.tex
cat nomacd_*.tex | sort | grep -v total > top3.tex
cat header.tex top3.tex sep.tex bottom3.tex footer.tex > $workdir/nomacd.tex

cat rsisma_*.tex | sort | grep total > bottom4.tex
cat rsisma_*.tex | sort | grep -v total > top4.tex
cat header.tex top4.tex sep.tex bottom4.tex footer.tex > $workdir/rsisma.tex

cat rsiema_*.tex | sort | grep total > bottom5.tex
cat rsiema_*.tex | sort | grep -v total > top5.tex
cat header.tex top5.tex sep.tex bottom5.tex footer.tex > $workdir/rsiema.tex

cat sma_*.tex | sort | grep total > bottom6.tex
cat sma_*.tex | sort | grep -v total > top6.tex
cat header.tex top6.tex sep.tex bottom6.tex footer.tex > $workdir/sma.tex

# draw the bar chart of the usage frequency

python3 comp.py > comp.csv
Rscript comp.R
cp comp.png $workdir

# make example decision trees in EPS for the manuscript

python3 dtvis.py $workdir/AUDUSD/char_2_0.3.csv > $workdir/scorefull.txt
mv vis.svg full.svg
python3 dtvis.py $workdir/AUDUSD/char_2_0.3.csv RSI SMA-3 > $workdir/scoremini.txt
mv vis.svg mini.svg

for vis in `ls -1 *.svg`;
do
    label=`basename $vis .svg`
    inkscape -E $basename.eps $vis
    # inkscape --export-dpi 300 -z $vis -e $label.png # these tend to be huge
cp *.eps $workdir
