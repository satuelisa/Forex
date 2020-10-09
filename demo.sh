workdir='/Users/elisa/Dropbox/Research/Topics/Forex' # set this to where you want the EPS files to go
python3 demo.py $workdir/eurusd.csv > demo.dat
python3 heikenashi.py > ha.dat
python3 avg.py
python3 macd.py > macd.dat
python3 stochactisosc.py > so.dat
python3 rsi.py > rsi.dat
gnuplot demo.plot
python3 psar.py
python3 folding.py; gnuplot fold.plot
cp *.eps $workdir
# recompile the manuscript (not in the repo)
cd $workdir 
pdflatex --interaction=batchmode schaeffer
bibtex --interaction=batchmode schaeffer
pdflatex --interaction=batchmode schaeffer
open schaeffer.pdf # open the PDF in OS X
