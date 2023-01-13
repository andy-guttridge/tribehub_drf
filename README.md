# TribeHub

## Project goals

This project provides a Django Rest Framework backend for the TribeHub React web app. It has also been designed with a future native iOS app in mind.

TribeHub is designed to be a virtual equivalent to the typical wall planner a family might put up in a kitchen or other communal area. The primary goals of the web app are to:
1) Provide busy families with a single, central hub around which to plan and organise busy lives and schedules. This should include calendar/event scheduling functionality similar to a family wall planner, enabling events to be scheduled for one or multiple family members, and viewed by all the family.
2) Deliver a simple and intuitive user experience, suitable for adults and tech literate children aged 10+. 
3) Offer a minimal set of impactful features chosen in order to deliver a useful app within an achievable development timeframe, while laying a solid foundation for additional features in the future.

## Table of contents

## API endpoints
| **URL** | **Notes** | **HTTP Method** | **CRUD operation** | **View type** | **POST/PUT data format** |
|---|---|---:|---|---:|---|
|  |  |  |  |  |  |
| **Custom user <br>account endpoints** |  |  |  |  |  |
| /accounts/tribe | Handles creation of a new user account with 'tribe' admin permissions,<br>creates a new user profile and a new tribe attached to that user. | POST | Create | List | {<br>    "username":"string",<br>    "password":"string",<br>    "password2":"string",<br>    "tribename":"string"<br>} |
| /accounts/user | Only tribe admins have permission for this endpoint.<br>Handles creation of a new user account without tribe admin permissions,<br> creates a new user profile and associates them with the same tribe as the<br>tribe admin who creates the account. | POST | Create | List | {<br>    "username":"string",<br>    "password":"string",<br>    "password2":"string"<br>} |
| /accounts/user/ | Handles deletion of the specified user account and profile. If the action is performed <br>by the tribe admin, the tribe and all the user accounts associated with it are also<br>deleted. Action can only be performed by users on their own accounts, and by the tribe<br>admin for user accounts which are part of their tribe. | DELETE | Delete | Detail | N/A |
| **Tribe endpoints** |  |  |  |  |  |
| /tribe | Lists all the members of the current authenticated user's tribe.<br>Can't be accessed by non-authenticated users.  | GET | Read | List | N/A |
| **Profile endpoints** |  |  |  |  |  |
| /profile/id | Retrieves profile details for the user id specified in the URL. Only members of the same <br>tribe as the requested profile can access this data. | GET | Read | Detail | N/A |
| /profile/id | Updates existing user profiles. This action can only be performer by the user <br>who owns the profile, or the admin of that user's tribe. | PUT | Update | Detail | {<br>    "display_name": "string",<br>    "image": "string",<br>    "is_admin": bool<br>}<br><br>Plus image data |
| **Notification endpoints** |  |  |  |  |  |
| /notifications | Lists all notifications for the authenticated user. | GET | Read | List | N/A |
| /notifications/id | Deletes the specified notification.<br>This action can only be performed by the owner of the notification. | DELETE | Delete | Detail | N/A |
| **Event endpoints** |  |  |  |  |  |
| /events | Returns all the scheduled events for the tribe to which the authenticated user belongs.<br>If no dates are specified, the next two months events are returned.<br><br>This endpoint programatically generates repeat occurrences where a repeat type has been <br>specified for an event, i.e. repeats are not stored in the database. Repeat occurrences <br>are indicated with a 'recurrence_type' value of 'REC'.<br><br>The following URL parameters are optionally available with this end point:<br><br>from_date=YYYY-MM-DDThh:mm:ss - accepts an ISO8601 format date and returns all events for the tribe from the <br>specified date up until the specified to_date, or for the next two months if no to_date is <br>specified.<br><br>to_date=YYYY-MM-DDThh:mm:ss - accepts an ISO8601 format date and returns all events for the tribe from today <br>or from the specified from_date.<br><br>category=string - accepts a valid category code and returns corresponding events <br><br>to=int - returns events to which the specified user is invited. Users who are not part of the<br>same tribe cannot access this data.<br><br>search=string - returns events where the search term is found in the subject field. | GET | Read | List | N/A |
| /events | Creates a new event for the tribe to which the user belongs.<br>Only users in the same tribe as the authenticated user can be invited.<br><br><br>Valid recurrence types are:<br>NON = None<br>WEK = Weekly<br>TWK = Two weekly<br>MON = Monthly<br>YEA = Yearly<br><br>Valid category strings are in events/event_values.py | POST | Create | List | {<br><br>    "to": [id, id...],<br>    "start": "YYYY-MM-DDThh:mm:ss",<br>    "duration": float,<br>    "recurrence_type": "String",<br>    "subject": "String",<br>    "category": "String"<br>} |
| /events/id | Returns details of a single event. Data is restricted to users who are members of the tribe <br>with which the event associated. | GET | Read | List | N/A |
| /events/id | Updates details of an existing event. This action is restricted to the user who created the <br>event and the tribe admin. | PUT | Update | Detail | {<br><br>    "to": [id, id...],<br>    "start": "YYYY-MM-DDThh:mm:ss",<br>    "duration": float,<br>    "recurrence_type": "String",<br>    "subject": "String",<br>    "category": "String"<br>} |
| /events/id | Deletes the specified event. This action is restricted to the user who created the <br>event and the tribe admin. | DELETE | Delete | Detail | N/A |
| /events/response/id | Records the authenticated user as having accepted or declined an invitation to <br>the specified event. Returns an error message if the user was not invited. | PUT | Update | Detail | {<br>    "event_response":"accept" OR "decline"<br>} |
| **Contact endpoints** |  |  |  |  |  |
| /contacts | Returns all the contacts for the authenticated user's tribe. | GET | Read | List | N/A |
| /contacts | Creates a new contact for the authenticated user's tribe. This action is restricted to tribe admins. | POST | Create | List | {<br>    "category": "String",<br>    "title": "String",<br>    "first_name": "String",<br>    "last_name": "String",<br>    "phone": "String",<br>    "email": "String"<br>} |
| /contacts/id | Updates details of an existing contact for the user's tribe.<br>This action is restricted to tribe admins. | PUT | Update | Detail | {<br>    "category": "String",<br>    "title": "String",<br>    "first_name": "String",<br>    "last_name": "String",<br>    "phone": "String",<br>    "email": "String"<br>} |
| /contacts/id | Delete the specified contact. This action is restricted to the admin of the tribe <br>to which the contact is associated. | DELETE | Delete | Detail | N/A |

Table generated using https://www.tablesgenerator.com/markdown_tables/load


### Data models

### Endpoints

## Frameworks, libraries and dependencies
**Need to provide rationale for choices**

### Cloudinary Storage

### dj-all-auth

### dj-rest-auth

### djangorestframework-simplejwt

### dj-database-url

### psychopg2

### python-dateutil

This is a pre-requisite for django-recurrence

### django-recurrence

### django-filter

### django-cors-headers

## Testing

### Manual testing

### Automated testing

**TO BE COMPLETED**

### Python validation

### Resolved bugs

- During testing, it became apparent that a user could not create a calendar event with no other members of the tribe invited (i.e. events only for themselves), because the `to` field on the `Event` model defaulted to not allowing null values. This was fixed by adding `null=True` and `blank=True` arguments to the model.
- Testing also revealed that the programatically generated events returned as repeat occurences included the currently authenticated user rather than the user who created the event as the owner. This was fixed by changing two variables in `events/utils.py`.
- Testing demonstrated that sending using an id for a non-existent event object for the `events/response/<id>` endpoint resulted in an uncaught exception. Try...except blocks were added to  the EventResponse class in `events/views.py` to ensure any references to non-existent events are handled gracefully alongside permission related errors, and that appropriate HTTP status codes are returned for each class of error.

### Unresolved bugs

- The `perform_create` method of the `ListCreate` generic view is overriden in `contacts/views.py`. Django did not seem to respond correctly to custom permission classes when this method is overriden, meaning that unauthorised users (i.e. authenticated users without tribe admin status) were able create new contacts. It was verified that the relevant custom permission classes were being called and returning the correct values, and it remains uncertain whether this issue is due to a bug in Django Rest Framework or in this project. The issue was overcome by manually checking the status of the user, but given more time it would be good to look into this further and revert to correct use of permission classes if possible.

## Deployment

## Credits

### Code

- How to fully define a field within an array field from [Stack Overflow](https://stackoverflow.com/questions/41180829/arrayfield-missing-1-required-positional-argument)
- Technique to limit the size of image uploads to cloudinary adapted from this [Cloudinary](https://support.cloudinary.com/hc/en-us/community/posts/360009752479-How-to-resize-before-uploading-pictures-in-Django) support article
- Replacement for deprecated `django.conf.urls.url()` implemented as per this [StackOverflow article](https://stackoverflow.com/questions/70319606/importerror-cannot-import-name-url-from-django-conf-urls-after-upgrading-to)
- Approach to creating a string representation of a many to many field in the Django admin panel from https://stackoverflow.com/questions/18108521/many-to-many-in-list-display-django
- Technique to create a custom filter for date ranges using django-filters adapted from this [StackOverflow article](https://stackoverflow.com/questions/37183943/django-how-to-filter-by-date-with-django-rest-framework)
- How to access URL arguments as kwargs in generic APIViews from this [StackOverflow article](https://stackoverflow.com/questions/51042871/how-to-access-url-kwargs-in-generic-api-views-listcreateapiview-to-be-more-spec)
- How to filter on many-to-many fields is from this [StackOverflow article](https://stackoverflow.com/questions/4507893/django-filter-many-to-many-with-contains)
- Technique to use Python pattern matching as case statements from this [StackOverflow article](https://stackoverflow.com/questions/11479816/what-is-the-python-equivalent-for-a-case-switch-statement)
- Technique to override model `save()` method to programatically set the value of fields based on the value of other fields from this [StackOverflow article]:(https://stackoverflow.com/questions/11479816/what-is-the-python-equivalent-for-a-case-switch-statement)
- Approach to obtaining the current user context within a model serializer from [Stackoverflow](https://stackoverflow.com/questions/30203652/how-to-get-request-user-in-django-rest-framework-serializer)
- Technique to use different serializers depending on HTTP request type within the same generic class view from [Stackoverflow](https://stackoverflow.com/questions/22616973/django-rest-framework-use-different-serializers-in-the-same-modelviewset)

In addition, the following documentation was extensively referenced throughout development:

- Django documentation
- Django Rest Framework documentation
- django-filter documentation
- django-recurrence documentation
- Python datetime documentation

