## /accounts/tribe POST

### Test 1
```
{
    "username":"chief1",
    "password":"password1",
    "password2":"password1",
    "tribename":"Tribe1"
}
```

Should result in creation of new user 'chief1', a new user profile linked to 'chief1' *with family admin status* and a new tribe called 'Tribe1'. Should return HTTP status 201 - PASS

### Test 2
```
{
    "username":"wpjpluihyszpffsmgrfyouhjgqainqqqlwlffbafdxvdrjbqzokkmuhuyrbotjhmktvgnpbestastfkeutvltyagpbyuapkeuwqgkczbzzzzqzsffaexaojgvjsmcimbjsiyscvrkrgzdtzizdblvpvlvcwqrjlg",
    "password":"password1",
    "password2":"password1",
    "tribename":"Tribe1"
}
```

Should result in 400 error with detailed error message ('Usernames cannot exceed 150 characters') - PASS

### Test 3
```
{
    "username":"",
    "password":"password1",
    "password2":"password1",
    "tribename":"Tribe1"
}
```

Should result in 400 error with detailed error message ('A username is required') - PASS

### Test 4
```
{
    "username":"chief2",
    "password":"password1",
    "password2":"password2",
    "tribename":"Tribe1"
}
```

Should result in 400 error with detailed error message ('Both password fields must contain the same value.') - PASS

### Test 5
```
{
    "username":"chief2",
    "password":"password1",
    "password2":"password1",
    "tribename":""
}
```

Should result in 400 error with detailed error message ('A tribename must be entered.') - PASS

### Test 6
```
{
    "username":"chief2",
    "password":"password1",
    "password2":"password1",
    "tribename":"jitdsuecqrxzfehnrdiywskzxuuzfifputzgjgggupvidkcofsxtxqluaifh"
}
```

Should result in 400 error with detailed error message ('Tribe names cannot exceed 50 characters.') - PASS

## /accounts/user/ POST

### Test 7
register_new_user/ POST
```
{
    "username":"family1",
    "password":"password1",
    "password2":"password1"
}
```

If logged in as *chief1* (a user with family_admin status), should result in creation of a new user 'family1', a new user profile linked to 'family1' *without family_admin status* and linked to the same tribe as chief1 - PASS

### Test 8

```
{
    "username":"family2",
    "password":"password1",
    "password2":"password1"
}
```

If logged in as *family1* (a user without family_admin status), should result in HTTP 403 Forbidden error - PASS

### Test 9
```
{
    "username":"wpjpluihyszpffsmgrfyouhjgqainqqqlwlffbafdxvdrjbqzokkmuhuyrbotjhmktvgnpbestastfkeutvltyagpbyuapkeuwqgkczbzzzzqzsffaexaojgvjsmcimbjsiyscvrkrgzdtzizdblvpvlvcwqrjlg",
    "password":"password1",
    "password2":"password1"
}
```

If logged in as *chief1* (a user with family_admin status), should result in 400 error with detailed error message ('Usernames cannot exceed 150 characters') - PASS

### Test 10
```
{
    "username":"",
    "password":"password1",
    "password2":"password1"
}
```

If logged in as *chief1* (a user with family_admin status), should result in 400 error with detailed error message ('A username is required') - PASS

### Test 11
```
{
    "username":"family1",
    "password":"password1",
    "password2":"password2"
}
```

Should result in 400 error with detailed error message ('Both password fields must contain the same value.') - PASS

## /accounts/user/<id:int> DELETE
### Test 12

Passing in the id of an existing user who is a member of the same tribe while logged in as the family admin user should make the user account inactive and delete the user profile, returning a HTTP 200 code with a message of 'The user account has been successfully deleted.' - PASS

### Test 13

Passing in the id of an existing user who is NOT a member of the same tribe while logged in as the family admin user of a different tribe should return a HTTP 403 error with an error message of 'You are not allowed to perform this action' - PASS

### Test 14

Passing in the id of an existing user who is a member of the same tribe while logged in as a member of the same tribe who is NOT the family admin user should return a HTTP 403 error with an error message of 'You are not allowed to perform this action' - PASS

### Test 15
Passing in the user's own id while logged in should make the user account inactive and delete the user profile, returning a HTTP 200 code with a message of 'The user account has been successfully deleted.' - PASS

### Test 16

Passing in the user's own id while logged in as a family admin user should make the user account inactive, delete the user profile, delete the tribe and all the user profiles associated with the tribe, and make all the user accounts associated with the tribe inactive. It should return a HTTP 200 code with a message of 'The user account has been successfully deleted.' - PASS

## /tribe GET
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
