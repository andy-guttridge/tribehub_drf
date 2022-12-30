## `/accounts/tribe` POST

### Test 1
When unauthenticated, a POST request to this endpoint with the following data should result in creation of new user 'chief1', a new user profile linked to 'chief1' *with family admin status* and a new tribe called 'Tribe1'. Should return HTTP status 201.

Submitted JSON:
```
{
    "username":"chief1",
    "password":"password1",
    "password2":"password1",
    "tribename":"Tribe1"
}
```

Result: PASS

<p align="center">
    <img src="readme_media/testing/account1.png" width=800>
</p>


### Test 2
When unauthenticated, a POST request to this endpoint with the following data should result in an HTTP 400 error with detailed error message ('Usernames cannot exceed 150 characters').

Submitted JSON:
```
{
    "username":"wpjpluihyszpffsmgrfyouhjgqainqqqlwlffbafdxvdrjbqzokkmuhuyrbotjhmktvgnpbestastfkeutvltyagpbyuapkeuwqgkczbzzzzqzsffaexaojgvjsmcimbjsiyscvrkrgzdtzizdblvpvlvcwqrjlg",
    "password":"password1",
    "password2":"password1",
    "tribename":"Tribe1"
}
```

Result: PASS

<p align="center">
    <img src="readme_media/testing/account2.png" width=800>
</p>

### Test 3
When unauthenticated, a POST request to this endpoint with the following data should result in 400 error with detailed error message ('A username is required').

Submitted JSON:
```
{
    "username":"",
    "password":"password1",
    "password2":"password1",
    "tribename":"Tribe1"
}
```
Result: PASS

<p align="center">
    <img src="readme_media/testing/account3.png" width=800>
</p>

### Test 4
When unauthenticated, a POST request to this endpoint with the following data should result in 400 error with detailed error message ('Both password fields must contain the same value.') 

Submitted JSON:
```
{
    "username":"chief2",
    "password":"password1",
    "password2":"password2",
    "tribename":"Tribe1"
}
```
Result: PASS

<p align="center">
    <img src="readme_media/testing/account4.png" width=800>
</p>

### Test 5
When unauthenticated, a POST request to this endpoint with the following data should result in 400 error with detailed error message ('A tribename must be entered.')

Submitted JSON:
```
{
    "username":"chief2",
    "password":"password1",
    "password2":"password1",
    "tribename":""
}
```

Result:PASS

<p align="center">
    <img src="readme_media/testing/account5.png" width=800>
</p>



### Test 6
When unauthenticated, a POST request to this endpoint with the following data should result in 400 error with detailed error message ('Tribe names cannot exceed 50 characters.')

Submitted JSON:
```
{
    "username":"chief2",
    "password":"password1",
    "password2":"password1",
    "tribename":"jitdsuecqrxzfehnrdiywskzxuuzfifputzgjgggupvidkcofsxtxqluaifh"
}
```

Result:PASS

<p align="center">
    <img src="readme_media/testing/account6.png" width=800>
</p>

## `/accounts/user/` POST

### Test 7
When logged in as *chief1* (a user with family_admin status), submitted the following data via this endpoint should result in creation of a new user 'family1a', a new user profile linked to 'family1a' *without family_admin status* and linked to the same tribe as chief1.

Submitted JSON:
```
{
    "username":"family1a",
    "password":"password1",
    "password2":"password1"
}
```
Result:PASS

<p align="center">
    <img src="readme_media/testing/account7.png" width=800>
</p>

### Test 8
When logged in as *family1a* (a user without family_admin status), attempting to use this endpoint should result in an HTTP 403 Forbidden error.

Submitted JSON:
```
{
    "username":"family1b",
    "password":"password1",
    "password2":"password1"
}
```

Result:PASS

<p align="center">
    <img src="readme_media/testing/account8.png" width=800>
</p>

### Test 9
When logged in as *chief1* (a user with family_admin status), submitting the following data via this endpoint should result in 400 error with detailed error message ('Usernames cannot exceed 150 characters')
```
{
    "username":"wpjpluihyszpffsmgrfyouhjgqainqqqlwlffbafdxvdrjbqzokkmuhuyrbotjhmktvgnpbestastfkeutvltyagpbyuapkeuwqgkczbzzzzqzsffaexaojgvjsmcimbjsiyscvrkrgzdtzizdblvpvlvcwqrjlg",
    "password":"password1",
    "password2":"password1"
}
```

Result: PASS

<p align="center">
    <img src="readme_media/testing/account9.png" width=800>
</p>

### Test 10
When logged in as *chief1* (a user with family_admin status), submitting the following data via this endpoint should result in 400 error with detailed error message ('A username is required').
```
{
    "username":"",
    "password":"password1",
    "password2":"password1"
}
```

Result: PASS

<p align="center">
    <img src="readme_media/testing/account10.png" width=800>
</p>

### Test 11
When logged in as *chief1* (a user with family_admin status), submitting the following data via this endpoint should result in 400 error with detailed error message ('Both password fields must contain the same value.')
```
{
    "username":"family1",
    "password":"password1",
    "password2":"password2"
}
```

Result: PASS

<p align="center">
    <img src="readme_media/testing/account11.png" width=800>
</p>

## `/accounts/user/<id:int>` DELETE
### Test 12

Passing in the id of an existing user who is a member of the same tribe to this endpoint while logged in as the family admin user (*chief1*) should make the user account inactive and delete the user profile, returning a HTTP 200 code with a message of 'The user account has been successfully deleted.'

Result: PASS

<p align="center">
    <img src="readme_media/testing/account12.png" width=800>
</p>

The user profile was seen to have been deleted and the user status set to inactive in the Django admin panel.


### Test 13

Passing in the id of an existing user who is NOT a member of the same tribe while logged in as the family admin user of a different tribe should return a HTTP 403 error with an error message of 'You are not allowed to perform this action'. A user id of 13 corresponding to user *family2c*  was used for this test, while logged in as *chief1* (has family admin status).

Result: PASS

<p align="center">
    <img src="readme_media/testing/account13.png" width=800>
</p>


### Test 14

Passing in the id of an existing user who is a member of the same tribe to this endpoint while logged in as a member of the same tribe who is NOT the family admin user should return a HTTP 403 error with an error message of 'You are not allowed to perform this action'. A user id of 13 corresponding to user *family2c*  was used for this test, while logged in as *family2d*.

Result: PASS

<p align="center">
    <img src="readme_media/testing/account14.png" width=800>
</p>

### Test 15
Passing in the user's own id while logged in should make the user account inactive and delete the user profile, returning a HTTP 200 code with a message of 'The user account has been successfully deleted.' A user id of 14 correspondeing to user *family2d* was used for this test, while also logged in as that user.

Result: PASS

<p align="center">
    <img src="readme_media/testing/account15.png" width=800>
</p>

### Test 16

Passing in the user's own id to this endpoint while logged in as a family admin user should make the user account inactive, delete the user profile, delete the tribe and all the user profiles associated with the tribe, and make all the user accounts associated with the tribe inactive. It should return a HTTP 200 code with a message of 'The user account has been successfully deleted.' 
This test was performed with a user id of 25 corresponding to user *chief1*, while also logged in as that user.

Result: PASS

<p align="center">
    <img src="readme_media/testing/account16.png" width=800>
</p>

The user profiles for both *chief1* and *family1a* were seen to have been made inactive in the Django admin panel. The profiles for both users and the tribe to which they both belonged (*Tribe1*)
were confirmed to have been deleted.

## `/tribe` GET
### Test 17

When not authenticated, the endpoint should return a 403 error - PASS

<p align="center">
    <img src="readme_media/testing/tribe1.png" width=800>
</p>

### Test 18

When authenticated as user *chief2*, a serialized JSON object and HTTP code 200 should be returned. The JSON object should contain the name of the tribe and an arrary of dictionaries containing the `user_id` and `display_name` values for other members of the tribe to which *chief2* belongs (*chief1*, *family2b*, *family2c*, *family2d*, *family2f*) - PASS

<p align="center">
    <img src="readme_media/testing/tribe2.png" width=800>
</p>

### Test 19

When authenticated as user *family2b*, the same JSON object and HTTP code 200 should be returned as for test 18, since *family2b* is a member of the same tribe as *chief2* - PASS

<p align="center">
    <img src="readme_media/testing/tribe3.png" width=800>
</p>

### Test 20

When authenticated as user *chief3*, a serialized JSON object and HTTP code 200 should be returned. The JSON object should contain the name of the tribe and an arrary of dictionaries containing the `user_id` and `display_name` values for other members of the tribe to which *chief3* belongs (*chief3*, *family3a*, *family3b*) - PASS

<p align="center">
    <img src="readme_media/testing/tribe4.png" width=800>
</p>

### Test 21

When authenticated as user *family3b*, the same JSON object and HTTP code 200 should be returned as for test 20, since *family3b* is a member of the same tribe as *chief3b* - PASS

<p align="center">
    <img src="readme_media/testing/tribe5.png" width=800>
</p>

## `/profile/<id:int>` GET
### Test 22

When authenticated as user *chief2* (has family admin permission), a GET request with the user id 12 should return a JSON object containing `user`, `username`, `display_name`, `image`, `tribe` and `is_admin` values for user *family2b*, since *chief2* and *family2b* are in the same tribe - PASS

<p align="center">
    <img src="readme_media/testing/profile1.png" width=800>
</p>

### Test 23

When authenticated as user *chief2* (has family admin permission), a GET request with the user id 18 (corresponding to user *family3a*) should return an HTTP 403 forbidden error, since *chief2* and *family3a* are in different tribes- PASS

<p align="center">
    <img src="readme_media/testing/profile2.png" width=800>
</p>

### Test 24

When authenticated as user *family3a* (does not have family admin permission), a GET request with the user id 16 should return a JSON object containing `user`, `username`, `display_name`, `image`, `tribe` and `is_admin` values for user *chief3*, since *family3a* and *chief3* are in the same tribe - PASS

<p align="center">
    <img src="readme_media/testing/profile3.png" width=800>
</p>

### Test 25

When authenticated as user *family3a* (does not have family admin permission), a GET request with the user id 10 (corresponding to user *chief2*) should return an HTTP 403 forbidden error, since *chief2* and *family3a* are in different tribes - PASS

<p align="center">
    <img src="readme_media/testing/profile4.png" width=800>
</p>

### Test 26

When not authenticated, a GET request with the user id 12 (corresponding to user *family2b*) should return an HTTP 403 forbidden error - PASS

<p align="center">
    <img src="readme_media/testing/profile5.png" width=800>
</p>

## `/profile/<id:int>` PUT
### Test 27
When authenticated as user *chief2* (has family admin permission), a PUT request made with the following JSON should result in the `display_name` field for user *family2b* being changed in the database to *family2b_test_change* and the image url being saved as `test_change`. Changes to other fields should not be saved, as they are read-only.

Submitted JSON:
```
{
    "user": 10,
    "username": "family2b_test_change",
    "display_name": "family2b_test_change",
    "image": "test_change",
    "tribe": 7,
    "is_admin": true
}
```
Result: PASS
<p align="center">
    <img src="readme_media/testing/profile6.png" width=800>
</p>

### Test 28
When authenticated as user *family2c* (does not have family admin permission -  but should be  able to change own profile), a PUT request made with the following JSON should result in the `display_name` field for user *family2c* being changed in the database to *family2c_test_change* and the image url being saved as `test_change`. Changes to other fields should not be saved, as they are read-only.

Submitted JSON:
```
{
    "user": 14,
    "username": "family2c_test_change",
    "display_name": "family2c_test_change",
    "image": "test_change",
    "tribe": 7,
    "is_admin": true
}
```

Result: PASS
<p align="center">
    <img src="readme_media/testing/profile7.png" width=800>
</p>

### Test 29
When authenticated as user *family2c* (does not have family admin permission, and should not be able to change the profile of someone else in their tribe), a PUT request made with the following JSON (user id corresponding to user *family2b*) should result in an HTTP 403 forbidden error.

Submitted JSON:
```
{
    "user": 10,
    "username": "family2b_test_change_again",
    "display_name": "family2b_test_change_again",
    "image": "test_change_again",
    "tribe": 7,
    "is_admin": true
}
```

Result: PASS
<p align="center">
    <img src="readme_media/testing/profile8.png" width=800>
</p>

### Test 30
When authenticated as user *chief2* (has family admin permission, but should not be able to change the profile of someone in a different tribe), a PUT request made with the following JSON (user id corresponding to user *family3b*) should result in an HTTP 403 forbidden error.

Submitted JSON:
```
{
    "user": 19,
    "username": "family3b_test_change_again",
    "display_name": "family3b_test_change_again",
    "image": "test_change_again",
    "tribe": 99,
    "is_admin": true
}
```

Result: PASS
<p align="center">
    <img src="readme_media/testing/profile9.png" width=800>
</p>

### Test 31
When authenticated as user *family2b* (does not have family admin permission, and should not be able to change the profile of someone in a different tribe), a PUT request made with the following JSON (user id corresponding to user *family3b*) should result in an HTTP 403 forbidden error.

Submitted JSON:
```
{
    "user": 19,
    "username": "family3b_test_change_again",
    "display_name": "family3b_test_change_again",
    "image": "test_change_again",
    "tribe": 99,
    "is_admin": true
}
```

Result: PASS
<p align="center">
    <img src="readme_media/testing/profile10.png" width=800>
</p>