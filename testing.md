**register_new_tribe/ POST**
```
{
    "username":"chief1",
    "password":"password1",
    "password2":"password1",
    "tribename":"Tribe1"
}
```

Should result in creation of new user 'chief1', a new user profile linked to 'chief1' and a new tribe called 'Tribe1'. Should return HTTP status 201 - PASS

```
{
    "username":"wpjpluihyszpffsmgrfyouhjgqainqqqlwlffbafdxvdrjbqzokkmuhuyrbotjhmktvgnpbestastfkeutvltyagpbyuapkeuwqgkczbzzzzqzsffaexaojgvjsmcimbjsiyscvrkrgzdtzizdblvpvlvcwqrjlg",
    "password":"password1",
    "password2":"password1",
    "tribename":"Tribe1"
}
```

Should result in 400 error with detailed error message ('Usernames cannot exceed 150 characters') - PASS

```
{
    "username":"",
    "password":"password1",
    "password2":"password1",
    "tribename":"Tribe1"
}
```

```
{
    "username":"chief2",
    "password":"password1",
    "password2":"password2",
    "tribename":"Tribe1"
}
```

Should result in 400 error with detailed error message ('Both password fields must contain the same value.') - PASS

```
{
    "username":"chief2",
    "password":"password1",
    "password2":"password1",
    "tribename":""
}
```

Should result in 400 error with detailed error message ('A tribename must be entered.') - PASS

```
{
    "username":"chief2",
    "password":"password1",
    "password2":"password1",
    "tribename":"jitdsuecqrxzfehnrdiywskzxuuzfifputzgjgggupvidkcofsxtxqluaifh"
}
```

Should result in 400 error with detailed error message ('Tribe names cannot exceed 50 characters.') - PASS