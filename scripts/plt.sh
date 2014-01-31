#Bash script to plot all the data files in the directory

#Create plot dir
mkdir plt
mkdir plt/bar
mkdir plt/freq

dfiles=$(ls *.dat)

#now, loop through, and call the python program
i=0
for data in $dfiles
do
    echo $data
    echo "Please enter a description of this data"
    read temp
    if [ "$i" -eq "0" ]; then
        des="$temp"
        i=1
        echo first line
    else
        des="$des|$temp"
    fi
    echo $data, $temp >> description.txt
    python plt.py $data 'Frequency' 'Vrms/rtHz'
    mv *freq.eps plt/freq/
    mv *.eps plt/bar/
echo $des
done
