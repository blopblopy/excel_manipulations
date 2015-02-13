
for file in `ls -1 | grep xlsx`;
do 
  mkdir "${file}_opened";
  cd "${file}_opened";
  unzip "../$file";
  /Users/nadavwe/personal/python/excel_cond_format/change_to_YG.py xl/worksheets/sheet1.xml;
  zip "../${file}+yg_coloring.xlsx" -r *;
  cd ..;
done;
