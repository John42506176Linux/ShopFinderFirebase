/**
 * Copyright 2018, Google LLC
 * Licensed under the Apache License, Version 2.0 (the `License`);
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *    http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an `AS IS` BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */


'use strict'

$(document).ready(function() {
	$('form').submit(function(event) {
		var email = $('input[name=email]').val();
		var password = $('input[name=password]').val();
		var formData = {
            'email'       : email,
            'password'    : password
        };

        // process the form
        $.ajax({
            type        : 'POST', // define the type of HTTP verb we want to use (POST for our form)
            url         : '/login', // the url where we want to POST
            data        : formData, // our data object
            dataType    : 'json', // what type of data do we expect back from the server
			encode      : true
        })
            // using the done promise callback
            .done(function(data) {

                // log data to the console so we can see
                if(data.TAG_SUCCESS == 1)
				{
					formData = {
						'user_id':data.USER_ID
					};
					firebase.auth().signInWithEmailAndPassword(email, password)
						.then(function() {
									$.ajax({
									type        : 'POST', // define the type of HTTP verb we want to use (POST for our form)
									url         : '/add_user_session', // the url where we want to POST
									data        : formData, // our data object
									dataType    : 'json', // what type of data do we expect back from the server
									encode      : true,
									success		: function(){
										window.location.href = "/";
									}
									});
						}

						)
						.catch(function (error) {
						// Handle Errors here.
						$("#error-box").css("display","block");
                		$("#error-message").html(error.message);
						console.log(error.message);
					});


					// process the form
				}
				else
				{
                	$("#error-box").css("display","block");
                	$("#error-message").html(data.bad_response);
                	console.log(data.bad_response);
				}
                // here we will handle errors and validation messages
            });


		event.preventDefault();
	});
});