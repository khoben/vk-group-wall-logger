#!/bin/bash

CURL='/usr/bin/curl'
RVMHTTP="http://0.0.0.0:5000/callback/xE4sA"

$CURL -H "Content-Type: application/json" -X POST -d '{"type":"wall_post_new","object":{"id":309,"from_id":-105873414,"owner_id":-105873414,"date":1473637173,"post_type":"post","text":"","copy_history":[{"id":986,"owner_id":140643708,"from_id":140643708,"date":1473578267,"post_type":"post","text":"&#9996; [id12280585|Павел Городецкий]  [id22594346|Антон Егоров]","attachments":[{"type":"photo","photo":{"id":431952382,"album_id":-7,"owner_id":140643708,"photo_75":"https:\/\/pp.vk.me\/c622029\/v622029708\/4905c\/FAKYcvHGlGY.jpg","photo_130":"https:\/\/pp.vk.me\/c622029\/v622029708\/4905d\/5bUr10wh_LI.jpg","photo_604":"https:\/\/pp.vk.me\/c622029\/v622029708\/4905e\/m1gziG8SPAY.jpg","photo_807":"https:\/\/pp.vk.me\/c622029\/v622029708\/4905f\/6by7GP-ouM0.jpg","photo_1280":"https:\/\/pp.vk.me\/c622029\/v622029708\/49060\/pXNqkaApBpQ.jpg","photo_2560":"https:\/\/pp.vk.me\/c622029\/v622029708\/49061\/ydCYwtCKiUI.jpg","width":2304,"height":1728,"text":"","date":1473578253,"access_key":"74df2b29197d00a3a1"}}],"post_source":{"type":"api","platform":"android"}}],"can_edit":1,"created_by":23168985,"can_delete":1,"comments":{"count":0}},"group_id":105873414}' $RVMHTTP