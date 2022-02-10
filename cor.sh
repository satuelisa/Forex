# USAGE: bash cor.sh 

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
    label=`python3 clean.py $dataset`
    echo $label
    python3 heikenashi.py $dataset > cor.$label.ha.csv
    python3 avg.py $dataset stdout > cor.$label.avg.csv
    python3 macd.py $dataset stdout > cor.$label.macd.csv
    python3 stochacticosc.py $dataset > cor.$label.so.csv
    python3 rsi.py $dataset stdout > cor.$label.rsi.csv
    python3 zigzag.py $dataset stdout >  cor.$label.zz.csv
done
python3 combine.py 
Rscript cor.R

