<?php

@mkdir("data/preprocessed");

$hashtags=[];

function computeHashtags($fnameArr, $statsOut){
    global $hashtags;

    echo "Computing hashtags stats\n";
    $stat=[0=>[],1=>[]];
    foreach($fnameArr as $fname){
        echo "    Processing [$fname]\n";
        $fp=fopen($fname,"r");
        $lnum=0;

        while(!feof($fp)){
            $data=fgetcsv($fp,0,",","\"","\0");
            $lnum++;
            if($data===false)break;
            if(count($data)!==3){ // check for training data
                echo "Error in line [$lnum]\n";
                var_dump($data);die();
                continue;
            }

            if($lnum==1)continue; // skip header

            $id=$data[0];
            $text=$data[1];
            $label=intval($data[2]);

            // Space normalization
            $text=str_replace("\n"," ",$text);
            $text=str_replace("\r"," ",$text);
            $text=str_replace("\t"," ",$text);
            $text=str_replace("\xc2\xa0"," ",$text);
            $text=str_replace("\xf0\x9f"," ",$text);
            $text=str_replace("\xe2\x9e"," ",$text);
        // remove quotes: https://op.europa.eu/en/web/eu-vocabularies/formex/physical-specifications/character-encoding/quotation-marks
        $text=str_replace("\xe2\x80\x98"," ",$text); // "
        $text=str_replace("\xe2\x80\x99"," ",$text); // "
        $text=str_replace("\xe2\x80\x9a"," ",$text); // "
        $text=str_replace("\xe2\x80\x9b"," ",$text); // "
        $text=str_replace("\xe2\x80\x9c"," ",$text); // "
        $text=str_replace("\xe2\x80\x9d"," ",$text); // "
        $text=str_replace("\xe2\x80\x9e"," ",$text); // "
        $text=str_replace("\xe2\x80\x9f"," ",$text); // "
        $text=str_replace("\xe2\x80\xb9"," ",$text); // "
        $text=str_replace("\xe2\x80\xba"," ",$text); // "
        $text=str_replace("\""," ",$text); // "
        $text=str_replace("'"," ",$text); // "
        $text=str_replace("`"," ",$text); // "
            $text=mb_strtolower($text);

            $regex="/#([^-# .!?,:;]+)/";
            $r=preg_match_all($regex,$text,$matches);
            if($r!==false && $r>0){
                foreach($matches[0] as $tag){
                    if(!isset($stat[$label][$tag]))$stat[$label][$tag]=1;
                    else $stat[$label][$tag]++;
                }

            }

        }
        fclose($fp);
    }

    $all=array_merge(array_keys($stat[0]),array_keys($stat[1]));
    $fout=fopen($statsOut,"w");
    fwrite($fout,"Hashtag\tnum0\tnum1\n");
    foreach($all as $tag){
        fwrite($fout,"$tag\t");
        if(isset($stat[0][$tag]))fwrite($fout,$stat[0][$tag]."\t");
        else fwrite($fout,"0\t");
        if(isset($stat[1][$tag]))fwrite($fout,$stat[1][$tag]."\n");
        else fwrite($fout,"0\n");
    }
    fclose($fout);

    $hashtags=$stat;
}

function processFile($fname,$fnameOut,$gold,$statsOut){
    global $hashtags;
    echo "Processing [$fname] ";
    $fp=fopen($fname,"r");
    $fout=fopen($fnameOut,"w");
    fwrite($fout,"id\ttext\tlabel\tHashtags\tHashtagsRemain\tHashtagsSplit\tUsers\tURL\tRawSz\tPreSz\tDiffSz\n");

    $stats=[
        "raw" => [
            "size" => [],
            "total_size" => 0,
            "num" =>0,
        ],
        "pre" => [
            "size" => [],
            "total_size" => 0,
            "num" =>0,
        ],
    ];

    $lnum=0;

    while(!feof($fp)){
        $data=fgetcsv($fp,0,",","\"","\0");
        $lnum++;
        if($data===false)break;
        if($gold && count($data)!==3 || !$gold && count($data)!==2){
            echo "Error in line [$lnum]\n";
            var_dump($data);die();
            continue;
        }

        if($lnum==1)continue; // skip header

        $id=$data[0];
        $text=$data[1];
        $label=""; if($gold)$label=intval($data[2]);

        // Update raw stats
        $rawSz=mb_strlen($text);
        $stats['raw']['num']++;
        $stats['raw']['total_size']+=$rawSz;
        if(!isset($stats['raw']['size'][$rawSz]))$stats['raw']['size'][$rawSz]=1;
        else $stats['raw']['size'][$rawSz]++;


        // Space normalization
        $text=str_replace("\n"," ",$text);
        $text=str_replace("\r"," ",$text);
        $text=str_replace("\t"," ",$text);
        $text=str_replace("\xc2\xa0"," ",$text);
        $text=str_replace("\xf0\x9f"," ",$text);
        $text=str_replace("\xe2\x9e"," ",$text);
        // remove quotes: https://op.europa.eu/en/web/eu-vocabularies/formex/physical-specifications/character-encoding/quotation-marks
        $text=str_replace("\xe2\x80\x98"," ",$text); // "
        $text=str_replace("\xe2\x80\x99"," ",$text); // "
        $text=str_replace("\xe2\x80\x9a"," ",$text); // "
        $text=str_replace("\xe2\x80\x9b"," ",$text); // "
        $text=str_replace("\xe2\x80\x9c"," ",$text); // "
        $text=str_replace("\xe2\x80\x9d"," ",$text); // "
        $text=str_replace("\xe2\x80\x9e"," ",$text); // "
        $text=str_replace("\xe2\x80\x9f"," ",$text); // "
        $text=str_replace("\xe2\x80\xb9"," ",$text); // "
        $text=str_replace("\xe2\x80\xba"," ",$text); // "
        $text=str_replace("\""," ",$text); // "
        $text=str_replace("'"," ",$text); // "
        $text=str_replace("`"," ",$text); // "

        // Remove URL
        $regex = "@(https?://([-\w\.]+[-\w])+(:\d+)?(/([\w/_\.#-]*(\?\S+)?[^\.\s])?)?)@";
        $r=preg_match_all($regex,$text,$matches);
        $numUrl=0;
        if($r!==false && $r>0)$numUrl=count($matches[0]);
        $text=preg_replace($regex, ' ', $text);

        // Remove user mentions
        $regex="/@([^@ ]+)/";
        $r=preg_match_all($regex,$text,$matches);
        $numUsers=0;
        if($r!==false && $r>0)$numUsers=count($matches[0]);
        $text=preg_replace($regex, ' ', $text);

        // Remove hashtags
        $regex="/#([^-# .!?,:;]+)/";
        //$text=preg_replace($regex, ' ', $text);
        $numHashtags=0;
        $numHashtagsRemain=0;
        $numHashtagsSplit=0;
        $r=preg_match_all($regex,$text,$matches);
        if($r!==false && $r>0){
            $numHashtags=count($matches[0]);
            foreach($matches[0] as $tag){
                $tagl=mb_strtolower($tag);
                if(isset($hashtags[0][$tagl]) && isset($hashtags[1][$tagl])){
                    $text=str_replace($tag," ",$text);
                }else{
                    $numHashtagsRemain++;
                    $r1=preg_match_all("|[A-Z][^A-Z]*|",$tag,$matches1);
                    if($r1!==false && $r1>0){
                        $rep=""; $last="";
                        if(count($matches1[0])>1)$numHashtagsSplit++;
                        foreach($matches1[0] as $m){
                            if(strlen($rep)>0 && (strlen($last)>1 || strlen($m)>1))$rep.=" ";
                            $rep.=$m;
                            $last=$m;
                        }
                        $text=str_replace($tag,$rep,$text);
                        //echo "$tag => $rep\n";
                    }
                }
            }

        }


        // Remove non-characters
        $text=preg_replace("/[^a-zA-Z]/"," ",$text);

        // Replace multiple spaces with single space
        $text=preg_replace("/[ ]+/"," ",$text);
        $text=trim($text);

        // Lowercase
        $text=mb_strtolower($text);

        // Update pre-processed stats
        $preSz=mb_strlen($text);
        $stats['pre']['num']++;
        $stats['pre']['total_size']+=$preSz;
        if(!isset($stats['pre']['size'][$preSz]))$stats['pre']['size'][$preSz]=1;
        else $stats['pre']['size'][$preSz]++;

        $szDiff=$rawSz-$preSz;
        fwrite($fout,"$id\t$text\t$label\t$numHashtags\t$numHashtagsRemain\t$numHashtagsSplit\t$numUsers\t$numUrl\t$rawSz\t$preSz\t$szDiff\n");
    }

    fclose($fp);

    ksort($stats['raw']['size']);
    ksort($stats['pre']['size']);
    file_put_contents($statsOut,var_export($stats,true));

    echo "Lines=$lnum\n";

}

computeHashtags([
"data/raw/SubTask-A-train.csv",
//"data/raw/SubTask-A-train.csv",
//"data/raw/SubTask-A-train.csv",
], "data/hashtags.stat");

echo "\nPre-processing\n";
processFile("data/raw/SubTask-A-train.csv","data/preprocessed/A-train.pre",true,"data/A-train.stats");
processFile("data/raw/SubTask-B-train.csv","data/preprocessed/B-train.pre",true,"data/B-train.stats");
processFile("data/raw/SubTask-C-train.csv","data/preprocessed/C-train.pre",true,"data/C-train.stats");

processFile("data/raw/SubTask-A-(index,tweet)val.csv","data/preprocessed/A-eval.pre",false,"data/A-eval.stats");
processFile("data/raw/SubTask-B(index,tweet)val.csv","data/preprocessed/B-eval.pre",false,"data/B-eval.stats");
processFile("data/raw/SubTask-C(index,tweet)val.csv","data/preprocessed/C-eval.pre",false,"data/C-eval.stats");

processFile("data/raw/SubTask-A-(index,tweet)test.csv","data/preprocessed/A-test.pre",false,"data/A-test.stats");
processFile("data/raw/SubTask-B(index,tweet)test.csv","data/preprocessed/B-test.pre",false,"data/B-test.stats");
processFile("data/raw/SubTask-C(index,tweet)test.csv","data/preprocessed/C-test.pre",false,"data/C-test.stats");
