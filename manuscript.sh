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
