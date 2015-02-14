
for file in `ls -1 | grep xlsx`;
do 
  mkdir "${file}_opened";
  cd "${file}_opened";
  unzip "../$file";
  change_to_YG.py xl/worksheets/sheet1.xml;
  zip "../${file}+yg_coloring.xlsx" -r *;
  cd ..;
done;
