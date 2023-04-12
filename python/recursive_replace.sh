#!/bin/bash
# Recursively search all files with extension .sh in a given folder and for each file, replace all occurances of "bin" with "banana"

directory=$HOME"/Developments/Renaming/"
files=`find $directory -type f -name "*.txt"`
renaming_file='renaming.csv'
let num_of_lines=`awk '{++cnt} END {print cnt}' $renaming_file`-1
old_names=`awk -F ',' '{print $1}' $renaming_file | tail +2`
new_names=`awk -F ',' '{print $2}' $renaming_file | tail +2`

echo $num_of_lines
echo $old_names
echo $new_names

for file in $files
do
	echo $file
	old_name='david'
	new_name='norm'
	sed -i "s:\b$old_name\b:$new_name:g" $file
done
