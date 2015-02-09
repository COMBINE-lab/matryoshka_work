#!/bin/bash

for (( chr=1; chr<=23; chr++ ))
do

directory='/home/laraib/Desktop/COMBINE lab work/armatus-master-final/data/IMR90/chr'$chr'/'
cd "$directory"
cat chr$chr.gamma.0.* > chr$chr.all.txt
cat chr$chr.all.txt | sort | uniq > chr$chr.uniq.txt

sort -k2,2n -k3,3nr chr$chr.uniq.txt > sort.txt
rm chr$chr.uniq.txt
mv sort.txt chr$chr.uniq.txt

input_file=$directory'chr'$chr.uniq.txt
output_file=$directory'chr'$chr.hier.txt
python ../../../../code/collapse_hier.py -i "$input_file" -o "$output_file"

sort -k4,4nr -k2,2n "$output_file" > sort.txt
rm "$output_file"
mv sort.txt "$output_file"

input_file=$directory'chr'$chr.hier.txt
output_file=$directory'chr'$chr.hier.rank.txt
python ../../../../code/build_hier.py -i "$input_file" -o "$output_file"

sort -k7,7n -k3,3n "$output_file" > sort.txt
rm "$output_file"
mv sort.txt "$output_file"

cp "$output_file" '/home/laraib/Desktop/COMBINE lab work/armatus-master-final/data/IMR90/hier/chr'$chr.hier.rank.txt

done

cd '/home/laraib/Desktop/COMBINE lab work/armatus-master-final/data/IMR90/hier/'
find . -name "*.hier.rank.txt" | xargs -n 1 tail -n +2 > fullhier.rank.txt
awk '{printf ("%s\t%s\t%s\t%s\n", $2, $3, $4, $7)}' fullhier.rank.txt > IMR90.hier.txt
mv fullhier.rank.txt IMR90.hier.rank.txt
