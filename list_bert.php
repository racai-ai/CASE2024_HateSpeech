<?php

$models=[];

foreach(glob("data/bert-*") as $dir){

    foreach(glob("$dir/A-*") as $fold){

        $fpath="$fold/test.json";
        if(is_file($fpath)){
            $data=json_decode(file_get_contents($fpath),true);
            $f1=$data['weighted avg']['f1-score'];
            //var_dump($data);die();
            $models[$fold]=$f1;
        }
    }
}

arsort($models);
var_dump($models);

