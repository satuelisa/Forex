workdir='/elisa/Dropbox/Research/Topics/Forex' # the data and manuscript location

if [ "$(uname)" == "Darwin" ]; then
    workdir='/Users'${workdir}
elif [ "$(expr substr $(uname -s) 1 5)" == "Linux" ]; then
    workdir='/home'${workdir}
else
    echo 'I have no plans to use this in Win10'
    exit

echo $workdir
python3 demo.py $workdir/eurusd_hour.csv > demo.dat
python3 heikenashi.py > ha.dat
python3 avg.py
python3 macd.py > macd.dat
python3 stochactisosc.py > so.dat
python3 rsi.py > rsi.dat
python3 zigzag.py; gnuplot zz.plot
gnuplot demo.plot
grep -v -e '^[[:space:]]*$' demo.dat > noblanks.dat
python3 psar.py
python3 folding.py; gnuplot fold.plot
python3 autocor.py $workdir/eurusd_hour.csv 
cp *.eps $workdir
# recompile the manuscript (not in the repo)
cd $workdir 
pdflatex --interaction=batchmode schaeffer
bibtex schaeffer
pdflatex --interaction=batchmode schaeffer
open schaeffer.pdf 
