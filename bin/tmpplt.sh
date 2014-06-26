filename=$1
pwd
out="$filename.py"
cp /Users/aag2/Documents/Micro/Python/scripts/plt.template ./$out
python $out $filename

mv $out ./
mv $filename.eps ./

