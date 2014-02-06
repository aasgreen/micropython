#Bash script to plot all the data files in the directory

#Create plot dir
mkdir plt
mkdir plt/bar
mkdir plt/freq

dfiles=$(ls *.dat)
#Add error checking for database. IE: create the database if it isn't in the directory
#now, loop through, and call the python program
i=0
for data in $dfiles
do
    echo $data
    echo "Please enter a description of this data (-m opens editor)"
    read temp
    if [ "$temp" =  "-m" ]; then
        desfile=$(date +%s)
        vim $desfile
        temp="$(cat $desfile)"
        rm $desfile
    fi
    echo "$data| $temp" >> description.txt
     
    #python plt.py $data 'Frequency' 'Vrms/rtHz'
    #mv *freq.eps plt/freq/
  #  mv *.eps plt/bar/
#   DATABASE OPTIONS
    echo "Please enter keywords seperated by commas"
    read key
    date="$(echo $data | grep -o '^[0-9]\{8\}-[0-9]\{4\}')"
    echo $date
    sqlite3 ../data.db "insert into databll (name, time, description,keywords) values ('$data','$date','$temp','$key');"
done
