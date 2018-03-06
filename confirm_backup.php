<?php
function send_confirmation_email($address, $results)
{
    // send email
    mail($address,"Backups Complete",$results);
}


if ($_POST['password'] == "password")
{
    send_confirmation_email($_POST['email'],$_POST['result']);
}
?>