<?php
// Simulates both filters on a saved page: the content filter, plus the loader tag swap.
$filters=[]; $tagf=null;
function add_filter($h,$f,$p=10,$n=1){ global $filters,$tagf; if($h==="script_loader_tag") $tagf=$f; else $filters[]=$f; }
function add_action($h,$f,$p=10){}
function wp_json_encode($v){ return json_encode($v, JSON_UNESCAPED_SLASHES); }
function esc_url($u){ return htmlspecialchars($u, ENT_QUOTES); }
foreach (array_slice($argv,3) as $s) eval(file_get_contents(__DIR__."/$s.php"));
$html=file_get_contents($argv[1]);
foreach ($filters as $f) $html=$f($html);
$html=preg_replace_callback('/<script[^>]*id="trustindex-loader-js-js"[^>]*src="([^"]+)"[^>]*><\/script>/', function($m) use ($tagf){ return $tagf($m[0],'trustindex-loader-js',$m[1]); }, $html);
if (function_exists('eer_ti_lazy_images')) $html=eer_ti_lazy_images($html); // template_redirect output buffers
if (function_exists("eer_qup_delay")) $html=eer_qup_delay($html);
file_put_contents($argv[2],$html);
