## register_new_tribe/ POST

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

## register_new_user/ POST

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

## register_new_user/<id:int> DELETE
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



