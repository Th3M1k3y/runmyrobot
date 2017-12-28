<pre>
<?php
//-- Auth token, do not share with anyone!
$authToken = "";

//-- Robot ID for the robot you want to modify
$robotID = 0;

//-- JSON for custom panels
$panels = '[]';

//-- Toggle between true/false
$json_output = array(
	"public" => "true",
	"anonymous_control" => "false",
	"profanity_filter" => "true",
	"global_chat" => "false",
	"show_exclusive" => "false",
	"mute_text-to-speech" => "false",
	"mic_enabled" => "true",
	"dev_mode" => "false",
	"custom_panels" => "true",
	"panels" => $panels
);

//-- Do iiiiit
$ch = curl_init();
curl_setopt($ch, CURLOPT_URL,"https://api.letsrobot.tv/api/v1/robots/" . $robotID);
curl_setopt($ch, CURLOPT_POST, 1);
curl_setopt($ch, CURLOPT_HTTPHEADER, array('Content-Type: application/json', 'Authorization: Bearer ' . $authToken));
curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode($json_output));
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
$server_output = curl_exec ($ch);
curl_close ($ch);

//-- Have a look at the output
echo $server_output;
?></pre>
