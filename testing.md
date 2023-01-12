# TribeHub API Manual Testing

## Methodology

A series of manual tests were devised for each endpoint. The test data set included a number of users grouped into families. Users with tribe administrative rights are called `chief1`, `chief2`, `chief3`, and each of these users is associated with a different tribe. Corresponding family members were created with numbers in the user names to signify which tribe they belong to, e.g. `family1a`, `family1b` are part of `chief1`'s tribe, `family2a`, `family2b` are part of `chief2`'s tribe, etc.

Please note that object id numbers used in the test may vary in the screenshots and in the current state of the database, because some of the tests involved permanent deletion of objects, with similar objects subsequently recreated to continue testing.

Tests were performed using the Django Rest Framework HTML interface running on a test server. Each endpoint has a heading below, with the corresponding tests and results.

**To add detail about performing the same tests on the deployed API via the React front-end**.

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

**Result: PASS**

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

**Result: PASS**

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
**Result: PASS**

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
**Result: PASS**

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

**Result: PASS**

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
    "tribename":"jitdsuecqrxzfehnrdiywskzxuuzfizgjgggupvidkcofsxtxqluaifh"
}
```

**Result: PASS**

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
**Result: PASS**

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

**Result: PASS**

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

**Result: PASS**

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

**Result: PASS**

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

**Result: PASS**

<p align="center">
    <img src="readme_media/testing/account11.png" width=800>
</p>

## `/accounts/user/<id:int>` DELETE
### Test 12

Passing in the id of an existing user who is a member of the same tribe to this endpoint while logged in as the family admin user (*chief1*) should make the user account inactive and delete the user profile, returning a HTTP 200 code with a message of 'The user account has been successfully deleted.'

**Result: PASS**

<p align="center">
    <img src="readme_media/testing/account12.png" width=800>
</p>

The user profile was seen to have been deleted and the user status set to inactive in the Django admin panel.

### Test 13

Passing in the id of an existing user who is NOT a member of the same tribe while logged in as the family admin user of a different tribe should return a HTTP 403 error with an error message of 'You are not allowed to perform this action'. A user id of 10 corresponding to user *family2c*  was used for this test, while logged in as *chief1* (has family admin status).

**Result: PASS**

<p align="center">
    <img src="readme_media/testing/account13.png" width=800>
</p>


### Test 14

Passing in the id of an existing user who is a member of the same tribe to this endpoint while logged in as a member of the same tribe who is NOT the family admin user should return a HTTP 403 error with an error message of 'You are not allowed to perform this action'. A user id of 10 corresponding to user *family2c*  was used for this test, while logged in as *family2d*.

**Result: PASS**

<p align="center">
    <img src="readme_media/testing/account14.png" width=800>
</p>

### Test 15
Passing in the user's own id while logged in should make the user account inactive and delete the user profile, returning a HTTP 200 code with a message of 'The user account has been successfully deleted.' A user id of 18 correspondeing to user *family3d* was used for this test, while also logged in as that user.

**Result: PASS**

<p align="center">
    <img src="readme_media/testing/account15.png" width=800>
</p>

### Test 16

Passing in the user's own id to this endpoint while logged in as a family admin user should make the user account inactive, delete the user profile, delete the tribe and all the user profiles associated with the tribe, and make all the user accounts associated with the tribe inactive. It should return a HTTP 200 code with a message of 'The user account has been successfully deleted.' 
This test was performed with a user id of 14 corresponding to user *chief3*, while also logged in as that user.

**Result: PASS**

<p align="center">
    <img src="readme_media/testing/account16.png" width=800>
</p>

The user profiles for *chief3*, *family3a*, *family3b*, *family3c* and *family3d* were seen to have been made inactive in the Django admin panel. The profiles for both users and the tribe to which they both belonged (*Tribe3*) were confirmed to have been deleted.

## `/tribe` GET
### Test 17

When not authenticated, the endpoint should return a 403 error.

**Result: PASS**

<p align="center">
    <img src="readme_media/testing/tribe1.png" width=800>
</p>

### Test 18

When authenticated as user *chief2*, a serialized JSON object and HTTP code 200 should be returned. The JSON object should contain the name of the tribe and an arrary of dictionaries containing the `user_id` and `display_name` values for other members of the tribe to which *chief2* belongs (*family2a*, *family2b*, *family2c*, *family2d*).

**Result: PASS**

<p align="center">
    <img src="readme_media/testing/tribe2.png" width=800>
</p>

### Test 19

When authenticated as user *family2b*, the same JSON object and HTTP code 200 should be returned as for test 18, since *family2b* is a member of the same tribe as *chief2*.

**Result: PASS**

<p align="center">
    <img src="readme_media/testing/tribe3.png" width=800>
</p>

### Test 20

When authenticated as user *chief1*, a serialized JSON object and HTTP code 200 should be returned. The JSON object should contain the name of the tribe and an arrary of dictionaries containing the `user_id` and `display_name` values for other members of the tribe to which *chief1* belongs (*chief1*, *family1a*, *family1b*, *family1c*, *family1d*).

**Result: PASS**

<p align="center">
    <img src="readme_media/testing/tribe4.png" width=800>
</p>

### Test 21

When authenticated as user *family1b*, the same JSON object and HTTP code 200 should be returned as for test 20, since *family1b* is a member of the same tribe as *chief1*.

**Result: PASS**

<p align="center">
    <img src="readme_media/testing/tribe5.png" width=800>
</p>

## `/profile/<id:int>` GET
### Test 22

When authenticated as user *chief2* (has family admin permission), a GET request with the user id 9 should return a JSON object containing `user`, `username`, `display_name`, `image`, `tribe` and `is_admin` values for user *family2b*, since *chief2* and *family2b* are in the same tribe.

**Result: PASS**

<p align="center">
    <img src="readme_media/testing/profile1.png" width=800>
</p>

### Test 23

When authenticated as user *chief2* (has family admin permission), a GET request with the user id 3 (corresponding to user *family1a*) should return an HTTP 403 forbidden error, since *chief2* and *family1a* are in different tribes.

**Result: PASS**

<p align="center">
    <img src="readme_media/testing/profile2.png" width=800>
</p>

### Test 24

When authenticated as user *family2a* (does not have family admin permission), a GET request with the user id 7 should return a JSON object containing `user`, `username`, `display_name`, `image`, `tribe` and `is_admin` values for user *chief2*, since *family2a* and *chief2* are in the same tribe.

**Result: PASS**

<p align="center">
    <img src="readme_media/testing/profile3.png" width=800>
</p>

### Test 25

When authenticated as user *family1a* (does not have family admin permission), a GET request with the user id 7 (corresponding to user *chief2*) should return an HTTP 403 forbidden error, since *chief2* and *family1a* are in different tribes.

**Result: PASS**

<p align="center">
    <img src="readme_media/testing/profile4.png" width=800>
</p>

### Test 26

When not authenticated, a GET request with the user id 9 (corresponding to user *family2b*) should return an HTTP 403 forbidden error.

**Result: PASS**

<p align="center">
    <img src="readme_media/testing/profile5.png" width=800>
</p>

## `/profile/<id:int>`
### Test 27
When authenticated as user *chief2* (has family admin permission), a request made with the following JSON should result in the `display_name` field for user *family2b* being changed in the database to *family2b_test_change* and the image url being saved as `test_change`. Changes to other fields should not be saved, as they are read-only.

Submitted JSON:
```
{
    "user": 10,
    "username": "family2b_test_change",
    "display_name": "family2b_test_change",
    "image": "test_change",
    "tribe": 99,
    "is_admin": true
}
```
**Result: PASS**

<p align="center">
    <img src="readme_media/testing/profile6.png" width=800>
</p>

### Test 28
When authenticated as user *family2c* (does not have family admin permission -  but should be  able to change own profile), a request made with the following JSON should result in the `display_name` field for user *family2c* being changed in the database to *family2c_test_change* and the image url being saved as `test_change`. Changes to other fields should not be saved, as they are read-only.

Submitted JSON:
```
{
    "user": 14,
    "username": "family2c_test_change",
    "display_name": "family2c_test_change",
    "image": "test_change",
    "tribe": 4,
    "is_admin": true
}
```

**Result: PASS**

<p align="center">
    <img src="readme_media/testing/profile7.png" width=800>
</p>

### Test 29
When authenticated as user *family2c* (does not have family admin permission, and should not be able to change the profile of someone else in their tribe), a request made with the following JSON (user id corresponding to user *family2b*) should result in an HTTP 403 forbidden error.

Submitted JSON:
```
{
    "user": 9,
    "username": "family2b_test_change_again",
    "display_name": "family2b_test_change_again",
    "image": "test_change_again",
    "tribe": 4,
    "is_admin": true
}
```

**Result: PASS**
<p align="center">
    <img src="readme_media/testing/profile8.png" width=800>
</p>

### Test 30
When authenticated as user *chief2* (has family admin permission, but should not be able to change the profile of someone in a different tribe), a request made with the following JSON (user id corresponding to user *family1d*) should result in an HTTP 403 forbidden error.

Submitted JSON:
```
{
    "user": 6,
    "username": "family1d_test_change_again",
    "display_name": "family1d_test_change_again",
    "image": "test_change_again",
    "tribe": 99,
    "is_admin": true
}
```

**Result: PASS**

<p align="center">
    <img src="readme_media/testing/profile9.png" width=800>
</p>

### Test 31
When authenticated as user *family2b* (does not have family admin permission, and should not be able to change the profile of someone in a different tribe), a request made with the following JSON (user id corresponding to user *family1d*) should result in an HTTP 403 forbidden error.

Submitted JSON:
```
{
    "user": 6,
    "username": "family1d_test_change_again",
    "display_name": "family1d_test_change_again",
    "image": "test_change_again",
    "tribe": 99,
    "is_admin": true
}
```

**Result: PASS**

<p align="center">
    <img src="readme_media/testing/profile10.png" width=800>
</p>

## `/events/` POST

### Test 31

When not authenticated, it should not be possible to access this endpoint via a POST request. This is confirmed by the API interface not offering a POST option for a non-authenticated user.

**Result: PASS**

<p align="center">
    <img src="readme_media/testing/event1.png" width=800>
</p>

### Test 32

When authenticated as user *chief1* (has family admin permission), a POST request with the following JSON (invitation sent to id corresponding to user *family1a*) should result in the creation of a new event, with the event linked to *chief1's* user id (2) and tribe id (1).

Submitted JSON:
```
{
    "to": ["3"],
    "start": "2023-01-15T10:00:00",
    "duration": "60.0",
    "recurrence_type": "WEK",
    "subject": "Violin lesson",
    "category": "MUS"
}
```

**Result: PASS**

<p align="center">
    <img src="readme_media/testing/event2.png" width=800>
</p>

### Test 33

When authenticated as user *family1a* (does not have family admin permission), a POST request with the following JSON (invitations sent to ids corresponding to users *chief1* and *family1b*) should result in the creation of a new event, with the event linked to *family1a's* user id (3),  and tribe id (1).

Submitted JSON:
```
{
    "to": ["2", "4"],
    "start": "2023-01-15T10:00:00",
    "duration": "30.0",
    "recurrence_type": "MON",
    "subject": "Chess club",
    "category": "EDU"
}
```

**Result: PASS**

<p align="center">
    <img src="readme_media/testing/event3.png" width=800>
</p>

### Test 34

When authenticated as user *chief1* (has family admin permission), a POST request with the following JSON (invitation sent to id corresponding to user *family2a*) should result in a HTTP 400 error with the message 'Users who are not part of this tribe cannot be invited.'

Submitted JSON:
```
{
    "to": ["8"],
    "start": "2023-01-15T10:00:00",
    "duration": "30.0",
    "recurrence_type": "NON",
    "subject": "Doctor's appointment",
    "category": "MED"
}
```

**Result: PASS**

<p align="center">
    <img src="readme_media/testing/event4.png" width=800>
</p>

### Test 35

When authenticated as user *chief1* (has family admin permission), a POST request with the following JSON containing invalid values for all fields (including `subject`, which cannot exceed 25 characters) should result in a HTTP 400 error with an informative error message for each field.

Submitted JSON:

```
{
    "to": ["sdfs"],
    "start": "2023-01-15ss10:00:00",
    "duration": "Hello",
    "recurrence_type": "XXX",
    "subject": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
    "category": "XXX"
}
```

**Result: PASS**

<p align="center">
    <img src="readme_media/testing/event5.png" width=800>
</p>

### Test 36

When authenticated as user *chief1* (user id 2), a request with the following JSON data should result in the creation of two new notification objects in the database, one for each invited user. These should be invitations to a new event.

Submitted JSON:

```
{
    "to": ["5", "4"],
    "start": "2023-01-15T10:00:00",
    "duration": "30.0",
    "recurrence_type": "MON",
    "subject": "Maths tutor",
    "category": "EDU"
}
```

**Result: PASS**

A new event was created using a POST request to this endpoint, and appropriate notifications were verified to have been created using the Django admin panel.

<p align="center">
    <img src="readme_media/testing/notifications1.png" width=800>
</p>

## `events/` GET

*Please note that the most useful combinations of search and filter parameters were tested, however every conceivable combination may not have been tested due to time constraints. Given sufficient time, further tests would be conducted to cover every combination.*

### Test 37

When authenticated as user *chief1*, all events only for the user's tribe from today and for the next two months should be returned. These should include programatically generated recurrences for repeat events (in this case, weekly recurrences for 'Violin lesson' and monthly recurrences for 'Chess club'). No events for other tribes should be returned.

**Result: PASS**

*Not every item in the list is pictured due to the number of items, but the beginning, middle and end are captured. This also applies to the other tests involving recurring events below.*

<p align="center">
    <img src="readme_media/testing/event6a.png" width=400>
    <img src="readme_media/testing/event6b.png" width=400>
    <img src="readme_media/testing/event6c.png" width=400>
</p>

### Test 38

When authenticated as user *family1c*, an identical set of events should be returned as for test 37, since *family1c* is a member of the same tribe as *chief1*.

**Result: PASS**

<p align="center">
    <img src="readme_media/testing/event7a.png" width=400>
    <img src="readme_media/testing/event7b.png" width=400>
    <img src="readme_media/testing/event7c.png" width=400>
</p>

### Test 39

When authenticated as user *family2c*, all events only for the user's tribe from today and for the next two months should be returned (including recurrences). In this case, this should be an event called 'Play rehearsals' with fortnightly recurrences. No events for other tribes should be returned.

**Result: PASS**

<p align="center">
    <img src="readme_media/testing/event8a.png" width=400>
    <img src="readme_media/testing/event8b.png" width=400>
</p>

### Test 40

Used URL: `events/?from_date=2023-12-15T00:00:00`

When authenticated as user *family1c*, all events for the tribe for two months from 15 December 2023 should be returned. For the test data set, these should only be programatically generated recurrences, since there are no actual events in the database after January 2023.

**Result: PASS**

<p align="center">
    <img src="readme_media/testing/event9a.png" width=400>
    <img src="readme_media/testing/event9b.png" width=400>
    <img src="readme_media/testing/event9c.png" width=400>
</p>

### Test 41

Used URL `events/?to_date=2023-03-15T00:00:00`

When authenticated as user *family1c*, all events for the tribe from today up to 15 March 2023 should be returned.

**Result: PASS**

<p align="center">
    <img src="readme_media/testing/event10a.png" width=400>
    <img src="readme_media/testing/event10b.png" width=400>
    <img src="readme_media/testing/event10c.png" width=400>
</p>

### Test 42

Used URL `events/?from_date=2023-03-15T00:00:00&to_date=2023-07-15T00:00:00`

When authenticated as user *family1c*, all events for the tribe from 15 March 2023 up to 15 July should be returned.

**Result: PASS**

<p align="center">
    <img src="readme_media/testing/event11a.png" width=400>
    <img src="readme_media/testing/event11b.png" width=400>
    <img src="readme_media/testing/event11c.png" width=400>
</p>

### Test 43

Used URL `events/?category=MUS`

When authenticated as user *family1c*, all events for the tribe with a category of `MUS` (for Music) for two months from today should be returned.

**Result: PASS**

<p align="center">
    <img src="readme_media/testing/event12a.png" width=400>
    <img src="readme_media/testing/event12b.png" width=400>
    <img src="readme_media/testing/event12c.png" width=400>
</p>

### Test 44

Used URL `events/?from_date=2023-03-15T00:00:00&to_date=2023-07-15T00:00:00&category=MUS`

When authenticated as user *family1c*, all events for the tribe with a category of 'MUS' (for Music) between 15 March 2023 and 15 July 2023 should be returned.

**Result: PASS**

<p align="center">
    <img src="readme_media/testing/event13a.png" width=400>
    <img src="readme_media/testing/event13b.png" width=400>
    <img src="readme_media/testing/event13c.png" width=400>
</p>

### Test 45

Used URL `events/?to=2`

When authenticated as user *family1c*, all events to which `chief1` (user id 2) is invited for two months from today should be returned.

**Result: PASS**

<p align="center">
    <img src="readme_media/testing/event14a.png" width=400>
    <img src="readme_media/testing/event14b.png" width=400>
</p>

### Test 46

Used URL `events/?from_date=2023-03-15T00:00:00&to_date=2023-07-15T00:00:00&to=2`

When authenticated as user *family1c*, all events to which `chief1` (user id 2) is invited between 15 March 2023 and 15 July 2023 should be returned.

**Result: PASS**

<p align="center">
    <img src="readme_media/testing/event15a.png" width=400>
    <img src="readme_media/testing/event15b.png" width=400>
</p>

### Test 47

Used URL `events/?search=Chess+club`

When authenticated as user *family1c*, all events with `Chess club` in the subject for the tribe for two months from today should be returned.

**Result: PASS**

<p align="center">
    <img src="readme_media/testing/event16a.png" width=400>
    <img src="readme_media/testing/event16b.png" width=400>
</p>

### Test 48

Used URL `events/?from_date=2023-03-15T00:00:00&to_date=2023-07-15T00:00:00&search=Chess+club`

When authenticated as user *family1c*, all events with `Chess club` in the subject for the tribe between 15 March 2023 and 15 July 2023 should be returned.

**Result: PASS**

<p align="center">
    <img src="readme_media/testing/event17a.png" width=400>
    <img src="readme_media/testing/event17b.png" width=400>
</p>

### Test 49

Used URL `events/?from_date=xxx&to_date=zzz`

When authenticated as user *family1c*, the above URL should result in a HTTP 400 error with a message of 'Enter a valid date/time' for both the `from_date` and `to_date` fields.

**Result: PASS**

<p align="center">
    <img src="readme_media/testing/event18.png" width=800>
</p>

### Test 50

Used URL `events/?category=xxx`

When authenticated as user *family1c*, the above URL should result in a HTTP 400 error with a message of 'Select a valid choice. xxx is not one of the available choices'.

**Result: PASS**

<p align="center">
    <img src="readme_media/testing/event19.png" width=800>
</p>

## `events/<id:int>/` GET

### Test 51

Used URL `events/54`

When not authenticated, the above URL should result in a HTTP 403 error.

**Result: PASS**

<p align="center">
    <img src="readme_media/testing/event20.png" width=800>
</p>

### Test 52

Used URL `events/53`

When authenticated as user *family1b*, the above URL should return the 'Violin lesson' event.

**Result: PASS**

<p align="center">
    <img src="readme_media/testing/event21.png" width=800>
</p>

### Test 53

Used URL `events/53`

When authenticated as user *chief2*, the above URL should result in a HTTP 404 error, as this user is not a member of the same tribe as the user who created the event.

**Result: PASS**

<p align="center">
    <img src="readme_media/testing/event22.png" width=800>
</p>

## `events/<id:int>/`

### Test 54

Used URL `events/53`

When authenticated as user *chief1*, the above URL with the following JSON data should result in corresponding changes to the event. Note a user has been added to the invitation, the date changed, the duration extended, the recurrence type changed from weekly to fortnightly, the subject amended and the category changed to education.

Submitted JSON:

```
{
    "to": ["3", "4", "5"],
    "start": "2023-01-20T10:00:00",
    "duration": "120.0",
    "recurrence_type": "TWK",
    "subject": "Violin lesson - change",
    "category": "EDU"
}
```

**Result: PASS**

<p align="center">
    <img src="readme_media/testing/event23.png" width=800>
</p>


### Test 54B

When authenticated as user *chief1*, a request with the following JSON data (the same as in test 54) should result in the creation of three new notification objects in the database. A notification that changes have been made to an existing event should be created for user ids 3 and 4 (*family1a* and *family1b*), as they were already invited. A notification of an invitation to an event should be created for user id 5 (*family1c*), as they were not previously invited.

Submitted JSON:

```
{
    "to": ["3", "4", "5"],
    "start": "2023-01-20T10:00:00",
    "duration": "120.0",
    "recurrence_type": "TWK",
    "subject": "Violin lesson - change",
    "category": "EDU"
}
```

**Result: PASS**

<p align="center">
    <img src="readme_media/testing/notifications2.png" width=800>
</p>

### Test 55

Used URL `events/53`

When authenticated as user *chief1*, the above URL with the following JSON data should result in a HTTP 400 error with a message of 'Users who are not part of this tribe cannot be invited'.

Submitted JSON:

{
    "to": ["3", "8"],
    "start": "2023-01-20T10:00:00",
    "duration": "120.0",
    "recurrence_type": "TWK",
    "subject": "Violin lesson - test change",
    "category": "EDU"
}

**Result: PASS**

<p align="center">
    <img src="readme_media/testing/event24.png" width=800>
</p>

### Test 56

Used URL `events/53`

When authenticated as user *family1a*, the above URL with the following JSON data should result in a HTTP 403 error, as although the user is a member of the tribe, they did not create this event and are not a tribe administrator.

Submitted JSON:

{
    "to": ["3", "4"],
    "start": "2023-01-20T10:00:00",
    "duration": "120.0",
    "recurrence_type": "TWK",
    "subject": "Violin lesson - test change",
    "category": "EDU"
}

**Result: PASS**

<p align="center">
    <img src="readme_media/testing/event25.png" width=800>
</p>

### Test 58

Used URL `events/54`

When authenticated as user *family1a*, the above URL with the following JSON data should result in corresponding changes to the event, as this user was the creator.

Submitted JSON:

```
{
    "to": ["4"],
    "start": "2023-02-15T10:00:00",
    "duration": "60.0",
    "recurrence_type": "WEK",
    "subject": "Chess club - test change",
    "category": "CLU"
}
```
**Result: PASS**

<p align="center">
    <img src="readme_media/testing/event26.png" width=800>
</p>

### Test 59

Used URL `events/54`

When authenticated as user *chief1*, the above URL with the following JSON data should result in corresponding changes to the event, because although this user did not create the event, they have tribe admin status.

Submitted JSON:

```
{
    "to": ["4", "2"],
    "start": "2023-01-15T10:00:00",
    "duration": "30.0",
    "recurrence_type": "TWK",
    "subject": "Chess club - more change",
    "category": "EDU"
}
```

**Result: PASS**

<p align="center">
    <img src="readme_media/testing/event27.png" width=800>
</p>

### Test 60

Used URL `events/54`

When authenticated as user *chief1*, the above URL with the following JSON data should result in a HTTP 400 error, with appropriate validation error messages for each field.

Submitted JSON:

```
{
    "to": ["aaa", "bbb"],
    "start": "2023-01-15T10:00:00BAD_DATE",
    "duration": "xxx",
    "recurrence_type": "XXX",
    "subject": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
    "category": "XXX"
}
```

**Result: PASS**

<p align="center">
    <img src="readme_media/testing/event28.png" width=800>
</p>

## `events/<id:int>/` DELETE

### Test 61

Used URL `events/54`

When authenticated as user *chief2* (has tribe admin permissions), this URL should result in a HTTP 404 error, as this user is not part of the same tribe as *family1a* who created the event.

**Result: PASS**

<p align="center">
    <img src="readme_media/testing/event29.png" width=800>
</p>

### Test 62

Used URL `events/54`

When authenticated as user *family1b* (does not have tribe admin permissions), this URL should result in a HTTP 403 error, as this user was not the creator of the event, although they are a member of the same tribe as the creator.

**Result: PASS**

<p align="center">
    <img src="readme_media/testing/event30.png" width=800>
</p>

### Test 67

Used URL `events/54`

When authenticated as user *family1a* (does not have tribe admin permissions),this URL should result in the deletion of the event, as this user was the creator.

**Result: PASS**

<p align="center">
    <img src="readme_media/testing/event31.png" width=800>
</p>

### Test 68

Used URL `events/56`

When authenticated as user *chief1* (has tribe admin permissions),this URL should result in the deletion of the event, as this user is the tribe admin, although did not create it (another event was created for this test with *family1a* as owner).

**Result: PASS**

<p align="center">
    <img src="readme_media/testing/event32.png" width=800>
</p>

## `events/response/<id:int>`

### Test 69

Used URL `events/response/53`

When unauthenticated, the above URL should result in a HTTP 403 error.

**Result: PASS**

<p align="center">
    <img src="readme_media/testing/event33.png" width=800>
</p>

### Test 70

Used URL `events/response/53`

When authenticated as user *family1a* (user id 3), a request with the following JSON should result in an HTTP 200 status with a success message and this user being added to the `accepted` field of the event. 

Submitted JSON:

```
{"event_response": "accept"}
```

**Result: PASS**

<p align="center">
    <img src="readme_media/testing/event34a.png" width=800>
    <img src="readme_media/testing/event34b.png" width=800>
</p>

### Test 71

Used URL `events/response/53`

When authenticated as user *family1a* (user id 3), a request with the following JSON should result in a HTTP 200 status with a success message and this user being removed from the `accepted` field of the event.

Submitted JSON:
```
{"event_response": "decline"}
```

**Result: PASS**

<p align="center">
    <img src="readme_media/testing/event35a.png" width=800>
    <img src="readme_media/testing/event35b.png" width=800>
</p>


### Test 72

Used URL `events/response/53`

When authenticated as user *family1a* (user id 3), a request with the following JSON should result in a HTTP 400 error, with an error message of 'Value must equal accept or decline'.

Submitted JSON:
```
{"event_response": "maybe"}
```

**Result: PASS**

<p align="center">
    <img src="readme_media/testing/event36.png" width=800>
</p>

### Test 73

Used URL `events/response/53`

When authenticated as user *family1a* (user id 3), a request with the following JSON should result in a HTTP 400 error, with an error message of 'An event response is required'.

Submitted JSON:
```
{"event_response": ""}
```

**Result: PASS**

<p align="center">
    <img src="readme_media/testing/event37.png" width=800>
</p>

### Test 74

Used URL `events/response/53`

When authenticated as user *family1c* (user id 5), a request with the following JSON should result in a HTTP 400 error, with an error message of 'Users who are not invited to this event cannot respond.'.

Submitted JSON:
```
{"event_response": "accept"}
```

**Result: PASS**

<p align="center">
    <img src="readme_media/testing/event38.png" width=800>
</p>

### Test 75

Used URL `events/response/53`

When authenticated as user *family2a* (user id 8), a request with the following JSON should result in a HTTP 400 error, with an error message of 'Users who are not invited to this event cannot respond.'.

Submitted JSON:
```
{"event_response": "accept"}
```

**Result: PASS**

<p align="center">
    <img src="readme_media/testing/event39.png" width=800>
</p>

## `notifications/` GET

### Test 76

When authenticated as user *family1a* (user id 3), all notifications for that user should be returned, and none for other users.

**Result: PASS**

<p align="center">
    <img src="readme_media/testing/notifications3.png" width=800>
</p>

### Test 77

When authenticated as user *family2c* (user id 10), all notifications for that user should be returned, and none for other users.

**Result: PASS**

<p align="center">
    <img src="readme_media/testing/notifications4.png" width=800>
</p>

## `notifications/<id:int>/` DELETE

### Test 78

Used URL `notifications/97`

When authenticated as user *family1b* (user id 4), the user should not be able to delete this notification, as it was sent to *family1a*. An HTTP 404 error should be returned, as this object should not be retrieved from the database for this user.

**Result: PASS**

<p align="center">
    <img src="readme_media/testing/notifications5.png" width=800>
</p>

### Test 79

Used URL `notifications/97`

When not authenticated, the user should not be able to access this end point.

**Result: PASS**

<p align="center">
    <img src="readme_media/testing/notifications6.png" width=800>
</p>

### Test 80

Used URL `notifications/97`

When authenticated as user *family1a* (user id 3), the notification should be successfully deleted with an HTTP 204 response code. Since the notification was sent to this user, they should have permission to delete it.

**Result: PASS**

<p align="center">
    <img src="readme_media/testing/notifications7.png" width=800>
</p>

## `contacts/` POST

### Test 81

When authenticated as user *chief1* (user id 2), a POST request to this URL with the following JSON should result in the creation of a new contact, linked to this user's tribe.

### Test 82

When authenticated as user *chief2* (user id 7), a POST request to this URL with the following JSON should result in the creation of a new contact, linked to this user's tribe.

### Test 83

When authenticated as user *family1a* (user id 3), a POST request to this URL with the following JSON should result in a HTTP 400 error, since this user does not have family admin permissions.

### Test 84

When authenticated as user *chief2* (user id 7), a POST request to this URL with the following JSON should result in a HTTP 404 error, since this object should not be returned from the database for this user, as it is linked to a different tribe than theirs.

### Test 85

When authenticated as user *chief2* (user id 7), a POST request to this URL with the following JSON should result in a HTTP 400 error with an appropriate error message for each field.

### Test 86

When not authenticated, a POST request to this URL with the following JSON should result in a HTTP 403 error.

## `contacts/` GET

### Test 87

When authenticated as user *chief1* (user id 2), a GET request to this URL should return all the contacts for this user's tribe, and none for other tribes.

### Test 88

When authenticated as user *family1b* (user id 4), a GET request to this URL should return all the contacts for this user's tribe (the same as for test 86), and none for other tribes.

### Test 89

When authenticated as user *chief2* (user id 7), a GET request to this URL should return all the contacts for this user's tribe, and none for other tribes.

### Test 90

When authenticated as user *family2c* (user id 10), a GET request to this URL should return all the contacts for this user's tribe (the same as for test 87), and none for other tribes.

### Test 91

When not authenticated, a GET request to this URL should return a HTTP 403 error.

### Test 92

Used URL `contacts/?search=xxx`

When authenticated as user *family1c*, this URL should return all contacts for this user's tribe where the search term xxx appears in any field.

### Test 93

Used URL `contacts/?search=xxx`

When authenticated as user *chief2*, this URL should return all contacts for this user's tribe where the search term xxx appears in any field.

## `contacts/<id:int>/` GET

### Test 94

Used URL `contacts/xx`

When authenticated as user *chief1* (user id 2), a GET request to this URL should return details of contact id xx.

### Test 95

Used URL `contacts/xx`

When authenticated as user *family1d* (user id 6), a GET request to this URL should return details of contact id xx.

### Test 96

Used URL `contacts/xx`

When authenticated as user *chief2* (user id 7), a GET request to this URL should return a HTTP 404 error, since this user is a member of a different tribe and no results should be returned from the database for them.

### Test 97

Used URL `contacts/xx`

When not authenticated, a GET request to this URL should return a HTTP 403 error.

## `contacts/<id:int>/` PUT

### Test 97

Used URL `contacts/xx`

When authenticated as user *chief1* (user id 2), a PUT request to this URL with the following JSON should result in the contact being updated with the relevant information for the `category`, `title`, `first_name`, `last_name`, `phone` and `email` fields, as this user has tribe admin status and the contact belongs to their tribe. The data in the id and tribe fields should not be changed.

### Test 98

Used URL `contacts/xx`

When authenticated as user *family1a* (user id 3), a PUT request to this URL with the following JSON should result in a HTTP 403 error, as this user does not have tribe admin status.

### Test 99

Used URL `contacts/xx`

When authenticated as user *chief2* (user id 7), a PUT request to this URL with the following JSON should result in a HTTP 404 error, as this user is a member of a different tribe and the object should not be returned from the database for them.

## `contacts/<id:int>/` DELETE

### Test 100

Used URL `contacts/xx`

When authenticated as user *family1a* (user id 3), a DELETE request to this URL should result in a HTTP 403 error, as this user does not have tribe admin status.

### Test 101

Used URL `contacts/xx`

When authenticated as user *chief2* (user id 7), a DELETE request to this URL should result in a HTTP 404 error, as this user is a member of a different tribe and this object should not be returned from the database for them.

### Test 102

Used URL `contacts/xx`

When authenticated as user *chief1* (user id 2), a DELETE request to this URL should result in the object being detailed and a HTTP 204 status message.