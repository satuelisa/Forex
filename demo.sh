workdir='/Dropbox/Research/Topics/Forex' # the data and manuscript location

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
python3 demo.py $workdir/EURUSD.csv > daily.dat
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
python3 autocor.py $workdir/EURUSD.csv
echo 'Characterizing'
python3 characterize.py
sort -R char_2_3.dat | head -n 10 > sample.tex
sed 's/\s\+/ \& /g;s/$/ \\\\/g' sample.tex > $workdir/sample.tex
echo 'Training' 
python3 train.py > $workdir/perf.tex
python3 train.py RSI > $workdir/norsi.tex
python3 train.py RSI MACD > $workdir/nomacd.tex
cp *.eps $workdir
# recompile the manuscript (not in the repo)
cd $workdir 
pdflatex --interaction=batchmode schaeffer
bibtex schaeffer
pdflatex --interaction=batchmode schaeffer
if [ "$(uname)" == "Darwin" ]; then
    open schaeffer.pdf 
elif [ "$(expr substr $(uname -s) 1 5)" == "Linux" ]; then
    evince schaeffer.pdf &
else
    echo 'I have no plans to use this in Win10'
    exit
fi



