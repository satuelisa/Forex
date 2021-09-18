# make example decision trees in EPS for the manuscript

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


python3 dtvis.py $workdir/data/CNY/char_2_0.01.csv RSI SMA-3 > $workdir/dtscore.txt
inkscape -E $workdir/dt.eps dt.svg
# inkscape --export-dpi 300 -z dt.svg -e dt.png # these tend to be huge
