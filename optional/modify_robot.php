<pre>
<?php
$ch = curl_init();

//-- Auth token, do not share with anyone!
$authToken = "";

//-- Robot ID
$robotID = 0;

//-- Toggle between true/false
$public = "true";
$anonymous_control = "false";
$profanity_filter = "true";
$global_chat = "false";
$show_exclusive = "false";
$mute_text_to_speech = "false";
$mic_enabled = "true";
$dev_mode = "true";
$custom_panels = "true";

//-- JSON for custom panels
$panels = '[]';

//-- Modify JSON so it can be used as a string inside JSON when posting
$panels = str_replace("\"", "\\\"", $panels);

//-- Build the JSON we need to post to the server
$post_output = '{"public": ' . $public . ', "anonymous_control": ' . $anonymous_control . ', "profanity_filter": ' . $profanity_filter . ', "global_chat": ' . $global_chat . ', "show_exclusive": ' . $show_exclusive . ', "mute_text-to-speech": ' . $mute_text_to_speech . ', "mic_enabled": ' . $mic_enabled . ', "dev_mode": ' . $dev_mode . ', "custom_panels": ' . $custom_panels . ', "panels": "' . $panels . '"}';

//-- Do iiiiit
curl_setopt($ch, CURLOPT_URL,"https://api.letsrobot.tv/api/v1/robots/" . $robotID);
curl_setopt($ch, CURLOPT_POST, 1);
curl_setopt($ch, CURLOPT_HTTPHEADER, array('Content-Type: application/json', 'Authorization: Bearer ' . $authToken));
curl_setopt($ch, CURLOPT_POSTFIELDS, $post_output);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);

$server_output = curl_exec ($ch);

//-- Have a look at the output
echo $server_output;

curl_close ($ch);
?>
</pre>
