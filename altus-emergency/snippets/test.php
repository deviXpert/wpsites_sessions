<?php
$filters=[];
function add_filter($h,$f,$p=10){ global $filters; $filters[]=$f; }
function esc_url($u){ return htmlspecialchars($u, ENT_QUOTES); }
foreach (array_slice($argv,3) ?: ['1-video','2-aibtn','3-slack'] as $s) eval(file_get_contents(__DIR__."/$s.php"));
$html=file_get_contents($argv[1]);
foreach ($filters as $f) $html=$f($html);
file_put_contents($argv[2],$html);
