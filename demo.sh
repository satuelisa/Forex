workdir='/elisa/Dropbox/Research/Topics/Forex' # the data and manuscript location

if [ "$(uname)" == "Darwin" ]; then
    workdir='/Users'${workdir}
elif [ "$(expr substr $(uname -s) 1 5)" == "Linux" ]; then
    workdir='/home'${workdir}
else
    echo 'I have no plans to use this in Win10'
    exit
fi

echo $workdir
python3 demo.py $workdir/eurusd_hour.csv > daily.dat
python3 demo.py $workdir/eurusd_hour.csv 4 > fourhour.dat
python3 heikenashi.py > ha.dat
python3 avg.py
python3 macd.py > macd.dat
python3 stochactisosc.py > so.dat
python3 rsi.py > rsi.dat
python3 zigzag.py daily.dat > zzd.plot; gnuplot zzd.plot
python3 zigzag.py fourhour.dat > zz4.plot; gnuplot zz4.plot
gnuplot demo.plot
#grep -v -e '^[[:space:]]*$' demo.dat > noblanks.dat
python3 psar.py
python3 folding.py; gnuplot fold.plot
python3 autocor.py $workdir/eurusd_hour.csv
python3 characterize.py > char.dat
python3 train.py > $workdir/perf.tex
cp *.eps $workdir
# recompile the manuscript (not in the repo)
cd $workdir 
pdflatex --interaction=batchmode schaeffer
bibtex schaeffer
pdflatex --interaction=batchmode schaeffer
if [ "$(uname)" == "Darwin" ]; then
    open schaeffer.pdf 
elif [ "$(expr substr $(uname -s) 1 5)" == "Linux" ]; then
    evince schaeffer.pdf 
else
    echo 'I have no plans to use this in Win10'
    exit
fi



