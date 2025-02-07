/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

$( document ).ready(function() {
    console.log( "ready!" );
    var prediction = $('#prediction').text();
    if(!!prediction){
        prediction = prediction.replace("tensor([","").replace("])","");
         $('#prediction').text(prediction);
        var bodyWidth = prediction.length*3.77;
        $('#prediction-container').css('width', bodyWidth+'px');
    }else{
        console.log("no prediction yet")
    }
});