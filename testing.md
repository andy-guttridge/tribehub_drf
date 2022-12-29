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