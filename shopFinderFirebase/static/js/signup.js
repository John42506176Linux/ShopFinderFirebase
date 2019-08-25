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


// [START gae_python37_auth_javascript]
'use strict'

$(document).ready(function() {
    // process the form
    $('form').submit(function(event) {
    	var formInitialData = new FormData();
		var username = $('input[name=username]').val();
		var email = $('input[name=email]').val();
		var password = $('input[name=password]').val();
		var userImage = $("#UserImage")[0].files[0];
		formInitialData.append('UserImage',userImage);
		formInitialData.append('email',email);
		formInitialData.append('password',password);
		formInitialData.append('username',username);
		var formData;
        // get the form data
        // there are many ways to get this data using jQuery (you can use the class or id also)

        // process the form
        $.ajax({
            type        : 'POST', // define the type of HTTP verb we want to use (POST for our form)
			processData: false,
  			contentType: false,
            url         : '/sign_up', // the url where we want to POST
            data        : formInitialData, // our data object
            dataType    : 'json', // what type of data do we expect back from the server
                        encode          : true
        })
            // using the done promise callback
            .done(function(data) {

                // log data to the console so we can see
                if(data.TAG_SUCCESS == 1)
				{
					formData = {
						'user_id':data.USER_ID
					};
					firebase.auth().signInWithCustomToken(data.CUSTOM_TOKEN)
						.then(function() {
						$.ajax({
						type        : 'POST', // define the type of HTTP verb we want to use (POST for our form)
						url         : '/add_user_session', // the url where we want to POST
						data        : formData, // our data object
						dataType    : 'json', // what type of data do we expect back from the server
						encode      : true,
						success		: function () {
							window.location.href="/";
						}
						});
						})
						.catch(function(error) {
						  // Handle Errors here.
						  var errorMessage = error.message;
						  console.log(errorMessage);
						});


					// process the form
				}
				else
				{
                	console.log("User not created successfully");
				}
                // here we will handle errors and validation messages
            });

        // stop the form from submitting the normal way and refreshing the page
        event.preventDefault();
    });

});