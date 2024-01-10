<?php

eval("\$dataTrain=".file_get_contents("A-train.stats").";");
eval("\$dataTest=".file_get_contents("A-test.stats").";");
eval("\$dataVal=".file_get_contents("A-eval.stats").";");


echo ",Train,Valid,Test\n";

for($i=0;$i<1000;$i++){
    $r="";
    $r.=",";
    if(isset($dataTrain['raw']['size'][$i]))$r.=$dataTrain['raw']['size'][$i];
    $r.=",";
    if(isset($dataVal['raw']['size'][$i]))$r.=$dataVal['raw']['size'][$i];
    $r.=",";
    if(isset($dataTest['raw']['size'][$i]))$r.=$dataTest['raw']['size'][$i];

    if(strlen($r)>3)echo "$i$r\n";
}

//foreach($data['raw']['size'] as $sz=>$n){
//    echo "$sz,$n\n";
    /*if($sz<72)$lt+=$n;
    else{
        if($first){echo "<72,$lt\n";$first=false;}

        if($sz>=312)
            $gt+=$n;
        else
            echo "$sz,$n\n";
    }*/
//}

//echo ">311,$gt\n";
