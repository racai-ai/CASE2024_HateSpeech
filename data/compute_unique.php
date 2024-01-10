<?php

$sent=[];

$n=0;
$first=true;
foreach(explode("\n",file_get_contents("preprocessed/A-train.pre")) as $line){

    if($first){$first=false;continue;}

    $data=explode("\t",$line);
    if(count($data)<3)continue;

    $n++;
    $s=$data[1];
    $sent[$s]=true;
}

echo "Total = $n\nUnique = ".count($sent)."\n";

