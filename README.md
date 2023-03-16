# TribeHub

## Project goals
This project provides a Django Rest Framework API for the [TribeHub React web app](https://github.com/andy-guttridge/tribehub_react). It has also been designed with a future native iOS app in mind.

TribeHub is intended to be a virtual equivalent to the typical wall planner a family might put up in a kitchen or other communal area. The primary goals of the web app are to:
1) Provide busy families with a single, central hub around which to plan and organise busy lives and schedules. This should include calendar/event scheduling functionality similar to a family wall planner, enabling events to be scheduled for one or multiple family members, and viewed by all the family.
2) Deliver a simple and intuitive user experience, suitable for adults and tech literate children aged 10+. 
3) Offer a minimal set of impactful features chosen in order to deliver a useful app within an achievable development timeframe, while laying a solid foundation for additional features in the future.

## Table of contents
- [TribeHub](#tribehub)
  * [Project goals](#project-goals)
  * [Table of contents](#table-of-contents)
  * [Planning](#planning)
    + [Data models](#data-models)
      - [**Profile**](#--profile--)
      - [**Tribe**](#--tribe--)
      - [**Event**](#--event--)
    + [**Notification**](#--notification--)
    + [**Contact**](#--contact--)
  * [API endpoints](#api-endpoints)
  * [Frameworks, libraries and dependencies](#frameworks--libraries-and-dependencies)
    + [django-cloudinary-storage](#django-cloudinary-storage)
    + [dj-allauth](#dj-allauth)
    + [dj-rest-auth](#dj-rest-auth)
    + [djangorestframework-simplejwt](#djangorestframework-simplejwt)
    + [dj-database-url](#dj-database-url)
    + [psychopg2](#psychopg2)
    + [python-dateutil](#python-dateutil)
    + [django-recurrence](#django-recurrence)
    + [django-filter](#django-filter)
    + [django-cors-headers](#django-cors-headers)
  * [Testing](#testing)
    + [Manual testing](#manual-testing)
    + [Python validation](#python-validation)
    + [Resolved bugs](#resolved-bugs)
      - [Bugs found while testing the API in isolation](#bugs-found-while-testing-the-api-in-isolation)
      - [Bugs found while testing the React front-end](#bugs-found-while-testing-the-react-front-end)
    + [Unresolved bugs](#unresolved-bugs)
  * [Deployment](#deployment)
  * [Credits](#credits)

<small><i><a href='http://ecotrust-canada.github.io/markdown-toc/'>Table of contents generated with markdown-toc</a></i></small>

## Planning
Planning started by creating epics and user stories for the frontend application, based on the project goals. The user stories were used to inform wireframes mapping out the intended functionality and 'flow' through the app. See the [repo for the frontend React app](https://github.com/andy-guttridge/tribehub_react) for more details.

The user stories requiring implementation to achieve a minimum viable product (MVP) were then mapped to API endpoints required to support the desired functionality.
The user stories themselves are recorded [on this Google sheet](https://docs.google.com/spreadsheets/d/11wcDHeqr85VaHXdJjATod_WECRY03IRUlGgT_L_ikIw/edit#gid=0), with the required API endpoints mapped to user stories on [this sheet](https://docs.google.com/spreadsheets/d/11wcDHeqr85VaHXdJjATod_WECRY03IRUlGgT_L_ikIw/edit#gid=311853659).

### Data models
Data model schema were planned in parallel with the API endpoints, using an entity relationship diagram.

Custom models implemented for Tribehub are:

#### **Profile**
Represents the user profile, using a one-to-one relationsip to the user model. A Profile instance is automatically created on user registration. The Profile model includes an `is_admin` boolean field, which is used to determine whether a given user has tribe admin privileges. Note that initial user registration creates a profile with tribe admin rights; this user can then create further accounts for their family members which are added as members of the tribe, and these do not have admin rights.

The Profile model has a many to one relationship with the Tribe model. This is used throught the API to associate users with their tribes.

Users can edit their own `display_name` and `image` fields.

#### **Tribe**
The Tribe model has only one field, which is the name of the tribe. This model is important however, as it is used throughout the API to associate individual users with the appropriate tribe - for example, members of the same tribe can invite each other to calendar events, see each others events in the tribe calendar and access the same key contacts list, but they cannot access these items for tribes to which they do not belong.

#### **Event**
The Event model represents a calendar event. It has many to one relationships with the User model (the `user` field) and the Tribe model (the `tribe` field), in order to record who created the event and which tribe they belong to. There are two fields with many to many relationships with the User model - `to` and `accepted` - which record who has been invited to the event and who has accepted the invitation.

The `recurrences` field is an instance of `RecurrenceField`, provided by the [django-recurrence](https://django-recurrence.readthedocs.io/en/latest/) utility. This enables the calculation of recurring events based on a single original datetime and a set of rules (e.g. weekly, monthly etc). This field is not exposed externally by the API - rather, the `recurrence_type`  field is exposed to allow incoming requests for recurrences using a simple string (`WEK` for weekly, `TWK` for fortnightly, `MON` for monthly, `YEA` for yearly or `NON` for none). The corresponding recurrences rule is then applied by the Event model when an instance is saved to the database.

Recurrences are not saved as new events the database. When a GET request to the `events/` endpoint is made by an authenticated user, the `recurrences` field is used to programatically generate any recurrences of events which fall within the requested time range. These are then added to the JSON response to the client without creating new objects in the database. 
These programatically generated recurrences are identifed in the JSON data with a value of `REC` for the `recurrence_type` field. Because the recurrences include the id of the original 'parent' event in the database, the client can always retrieve the original event from the API if required.

The `start` field records the start date and time of the event using an unlocalised ISO8601 format datetime string, and the `duration` field records the the length of the event, which is serialized in the format `[DD] [HH:[MM:]]ss[.uuuuuu]`.

`subject` is a character field to describe the subject of the event. `category` is a choices field to record the category of the event as a three character string, which must correspond to one of a list of valid choices.

Any member of a tribe can create a new event. They can only invite members of their own tribe. Users can only retrieve details of events for their own tribe. The user who created an event and the tribe admin can delete events.

### **Notification**
The Notification model represents user notifications. Currently these are implemented for invitations and changes to calendar events, however further notification types could be implemented in the future to compliment additional features.

Notifications are created programatically when a new event is created or details of an existing event changed - there is no API endpoint to directly create a new notification.
Notifications have a many to one relationship with the User model to record who the notification is for, and a one to many relationship to the Event model to record which event the notification relates to. The `event` field can have a value of `None` so that it could be utilised for non-event related functionality in the future.

Users can only access and delete their own notifications.

### **Contact**
The Contact model represents an instance of important contact information for a tribe (e.g. doctor, dentist etc). Contacts can only be created, edited or deleted by the tribe admin user. Users can retrieve details of contacts for their own tribe, and cannot access contacts for other tribes.

<p align="center">
    <img src="readme_media/pp5_db_schema.png" width=400>
</p>

<p align="center">
    Link to full-size diagram: 
</p>

<p align="center">
    <a href="readme_media/pp5_db_schema.png" target="_rel">Link to full size DB schema</a>
</p>

## API endpoints
| **URL** | **Notes** | **HTTP Method** | **CRUD operation** | **View type** | **POST/PUT data format** |
|---|---|---:|---|---:|---|
|  |  |  |  |  |  |
| **Custom user <br>account endpoints** |  |  |  |  |  |
| /accounts/tribe | Handles creation of a new user account with 'tribe' admin permissions, creates a new user profile and a new tribe attached to that user. | POST | Create | List | {<br>    "username":"string",<br>    "password":"string",<br>    "password2":"string",<br>    "tribename":"string"<br>} |
| /accounts/user | Only tribe admins have permission for this endpoint.<br>Handles creation of a new user account without tribe admin permissions, creates a new user profile and associates them with the same tribe as the tribe admin who creates the account. | POST | Create | List | {<br>    "username":"string",<br>    "password":"string",<br>    "password2":"string"<br>} |
| /accounts/user/ | Handles deletion of the specified user account and profile. If the action is performed by the tribe admin, the tribe and all the user accounts associated with it are also deleted. Action can only be performed by users on their own accounts, and by the tribe admin for user accounts which are part of their tribe. | DELETE | Delete | Detail | N/A |
| **Tribe endpoints** |  |  |  |  |  |
| /tribe | Lists all the members of the current authenticated user's tribe.<br>Can't be accessed by non-authenticated users.  | GET | Read | List | N/A |
| **Profile endpoints** |  |  |  |  |  |
| /profile/id | Retrieves profile details for the user id specified in the URL. Only members of the same tribe as the requested profile can access this data. | GET | Read | Detail | N/A |
| /profile/id | Updates existing user profiles. This action can only be performer by the user who owns the profile, or the admin of that user's tribe. | PUT | Update | Detail | {<br>    "display_name": "string",<br>    "image": "string",<br>    "is_admin": bool<br>}<br><br>Plus image data |
| **Notification endpoints** |  |  |  |  |  |
| /notifications | Lists all notifications for the authenticated user. | GET | Read | List | N/A |
| /notifications/id | Deletes the specified notification.<br>This action can only be performed by the owner of the notification. | DELETE | Delete | Detail | N/A |
| **Event endpoints** |  |  |  |  |  |
| /events | Returns all the scheduled events for the tribe to which the authenticated user belongs.<br>If no dates are specified, the next two months events are returned.<br><br>This endpoint programatically generates repeat occurrences where a repeat type has been <br>specified for an event, i.e. repeats are not stored in the database. Repeat occurrences <br>are indicated with a 'recurrence_type' value of 'REC'.<br><br>The following URL parameters are optionally available with this end point:<br><br>from_date=YYYY-MM-DDThh:mm:ss - accepts an ISO8601 format date and returns all events for the tribe from the specified date up until the specified to_date, or for the next two months if no to_date is specified.<br><br>to_date=YYYY-MM-DDThh:mm:ss - accepts an ISO8601 format date and returns all events for the tribe from today <br>or from the specified from_date.<br><br>category=string - accepts a valid category code and returns corresponding events <br><br>to=int - returns events to which the specified user is invited. Users who are not part of the<br>same tribe cannot access this data.<br><br>search=string - returns events where the search term is found in the subject field. | GET | Read | List | N/A |
| /events | Creates a new event for the tribe to which the user belongs.<br>Only users in the same tribe as the authenticated user can be invited.<br><br><br>Valid recurrence types are:<br>NON = None<br>WEK = Weekly<br>TWK = Two weekly<br>MON = Monthly<br>YEA = Yearly<br><br>Valid category strings are in events/event_values.py | POST | Create | List | {<br><br>    "to": [id, id...],<br>    "start": "YYYY-MM-DDThh:mm:ss",<br>    "duration": float,<br>    "recurrence_type": "String",<br>    "subject": "String",<br>    "category": "String"<br>} |
| /events/id | Returns details of a single event. Data is restricted to users who are members of the tribe with which the event associated. | GET | Read | List | N/A |
| /events/id | Updates details of an existing event. This action is restricted to the user who created the event and the tribe admin. | PUT | Update | Detail | {<br><br>    "to": [id, id...],<br>    "start": "YYYY-MM-DDThh:mm:ss",<br>    "duration": float,<br>    "recurrence_type": "String",<br>    "subject": "String",<br>    "category": "String"<br>} |
| /events/id | Deletes the specified event. This action is restricted to the user who created the event and the tribe admin. | DELETE | Delete | Detail | N/A |
| /events/response/id | Records the authenticated user as having accepted or declined an invitation to the specified event. Returns an error message if the user was not invited. | PUT | Update | Detail | {<br>    "event_response":"accept" OR "decline"<br>} |
| **Contact endpoints** |  |  |  |  |  |
| /contacts | Returns all the contacts for the authenticated user's tribe.<br> Accepts a URL search parameter and returns results where a match is found in the category, title, first_name, last_name, phone or email fields.| GET | Read | List | N/A |
| /contacts | Creates a new contact for the authenticated user's tribe. This action is restricted to tribe admins. | POST | Create | List | {<br>    "category": "String",<br>    "title": "String",<br>    "first_name": "String",<br>    "last_name": "String",<br>    "phone": "String",<br>    "email": "String"<br>} |
| /contacts/id | Updates details of an existing contact for the user's tribe.<br>This action is restricted to tribe admins. | PUT | Update | Detail | {<br>    "category": "String",<br>    "title": "String",<br>    "first_name": "String",<br>    "last_name": "String",<br>    "phone": "String",<br>    "email": "String"<br>} |
| /contacts/id | Delete the specified contact. This action is restricted to the admin of the tribe <br>to which the contact is associated. | DELETE | Delete | Detail | N/A |

Table generated using https://www.tablesgenerator.com/markdown_tables/load

<p align="center">
    Link to a larger version of this table with sample output data: 
</p>

<p align="center">
    <a href="endpoints.md" target="_rel">API endpoints table</a>
</p>

## Frameworks, libraries and dependencies
The TribeHub API is implemented in Python using [Django](https://www.djangoproject.com) and [Django Rest Framework](https://django-filter.readthedocs.io/en/stable/).

The following additional utilities, apps and modules were also used.

### django-cloudinary-storage
https://pypi.org/project/django-cloudinary-storage/

Enables cloudinary integration for storing user profile images in cloudinary.

### dj-allauth
https://django-allauth.readthedocs.io/en/latest/

Used for user authentication. While not currently utilised, this package enables registration and authentication using a range of social media accounts. This may be implemented in a future update.

### dj-rest-auth
https://dj-rest-auth.readthedocs.io/en/latest/introduction.html

Provides REST API endpoints for login and logout. The user registration endpoints provided by dj-rest-auth are not utilised by the Tribehub frontend, as custom functionality was required and implemented by the Tribehub API.

### djangorestframework-simplejwt
https://django-rest-framework-simplejwt.readthedocs.io/en/latest/

Provides JSON web token authentication.

### dj-database-url
https://pypi.org/project/dj-database-url/

Creates an environment variable to configure the connection to the database.

### psychopg2
https://pypi.org/project/psycopg2/

Database adapater to enable interaction between Python and the PostgreSQL database.

### python-dateutil
https://pypi.org/project/python-dateutil/

This module provides extensions to the standard Python datetime module. It is a pre-requisite for django-recurrence library.

### django-recurrence
https://django-recurrence.readthedocs.io/en/latest/

This utility enables functionality for working with recurring dates in Django. It provides a `ReccurenceField` field type for storing recurring datetimes in the database.
This is used by the TribeHub API to programatically generate recurrences when calendar events are requested by the client, without having to store them in the database.

### django-filter
https://django-filter.readthedocs.io/en/stable/

django-filter is used to implement ISO datetime filtering functionality for the `events` GET endpoint. The client is able to request dates within a range using the `from_date` and `to_date` URL parameters. The API performs an additional check after filtering to 'catch' any repeat events within the requested range, where the original event stored in the database occurred beforehand.

### django-cors-headers
This Django app adds Cross-Origin-Resource Sharing (CORS) headers to responses, to enable the API to respond to requests from origins other than its own host.
TribeHub is configured to allow requests from all origins, to facilitate future development of a native movile app using this API.

## Testing

### Manual testing

A series of manual tests were carried out for each end point using the Django Rest Framework HTML interface running on the local server and using the deployed database. Please see the separate [testing.md](/testing.md) document for details.

All the features of the deployed API were tested as part of testing/acceptance criteria for each of the React frontend user stories. These tests are documented in the [read-me](https://github.com/andy-guttridge/tribehub_react) for that project.

Testing on the frontend revealed a number of bugs which had not been detected while testing the API in isolation, and led to the implementation of several additional features for consumption by the React app. The bugs are detailed in the bugs section below, and the following additional features were added as a result of front-end testing:

- The `display_name` and `is_admin` fields from the Profile model were added to the serializer for the User model, as the React app requires easy access to these for (among other things) the welcome message in the header and to determine whether the user should be permitted access to certain features.
- Users' profile image URLs were added to the user data returned by the `tribe/` endpoint, to make it easier for the front-end to access profile images for an entire tribe.
- The profile image of the user who created a calendar event was added to the JSON generated by the `events` endpoints, to enable the React app to easily display an Avatar for the user who created a calendar event.
- Programatically generated event recurrences did not include details of users who had accepted invitations, meaning the React app could only display this data for the original event. The UserSerializer already utilised for the original events saved in the database was then also used to serialize the user data for the recurrences.
- An event field containing full details of the event to which a notification relates was added to the notifications serializer, otherwise the React app would have to request data for each event separately from the `events/<id:int>` endpoint.
- A `user` URL parameter was added to enable searching for events based on who created the event.
- A `company` field was added to the Contacts model.

### Python validation

Code errors and style issues were detected using the Pylance linter in VSCode, and immediately fixed throughout development.
All files containing custom Python code were then validated using the [Code Institute Python Linter](https://pep8ci.herokuapp.com/):

- `contacts/admin.py`: no errors found
- `contacts/models.py`: no errors found
- `contacts/serializers.py`: no errors found
- `contacts/urls.py`: no errors found
- `contacts/views.py`: no errors found

- `events/admin.py`: no errors found
- `events/event_values.py`: no errors found
- `events/filters.py`: no errors found
- `events/models.py`: no errors found
- `events/serializers.py`: no errors found
- `events/urls.py`: no errors found
- `events/utils.py`: no errors found
- `events/views.py`: no errors found

- `notifications/admin.py`: no errors found
- `notifications/models.py`: no errors found
- `notifications/notification_values.py`: no errors found
- `notifications/serializers.py`: no errors found
- `notifications/urls.py`: no errors found
- `notifications/views.py`:no errors found

- `profiles/admin.py`: no errors found
- `profiles/models.py`: no errors found
- `profiles/serializers.py`: no errors found
- `profiles/urls.py`: no errors found
- `profiles/views.py`: no errors found  

- `tribehub_drf/permissions.py`: no errors found
- `tribehub_drf/serializers.py`: no errors found
- `tribehub_drf/settings.py`: no errors found
- `tribehub_drf/urls.py`: no errors found  
- `tribehub_drf/views.py`: no errors found

- `tribes/admin.py`: no errors found
- `tribes/models.py`: no errors found
- `tribes/serializers.py`: no errors found
- `tribes/urls.py`: no errors found
- `tribes/views.py`: no errors found

### Resolved bugs

#### Bugs found while testing the API in isolation
- During testing, it became apparent that a user was unable to create a calendar event with no other members of the tribe invited (i.e. events only for themselves), because the `to` field on the `Event` model defaulted to not allowing null values. This was fixed by adding `null=True` and `blank=True` arguments to the field.
- Testing also revealed that the programatically generated event recurrences erroneously included the currently authenticated user as the 'owner' of the event, rather than the user who created them. This was fixed by changing two variables in `events/utils.py`.
- Testing demonstrated that using an id for a non-existent event object for the `events/response/id` endpoint resulted in an uncaught exception. Try...except blocks were added to  the EventResponse class in `events/views.py` to ensure any references to non-existent events are handled gracefully alongside permission related errors, and that appropriate HTTP status codes are returned for each class of error.

#### Bugs found while testing the React front-end
- When first implementing user sign-in from the React front-end, submission of the POST form data to `dj-rest-auth/login/` was causing an HTTP 405 'method not allowed' error. This was tracked down to a space in the string for the value of `JWT-REFRESH-TOKEN` in `settings.py`. In order to work out what exactly was causing the bug, the settings of the React app were temporarily changed to make requests to `localhost` instead of the deployed API, enabling the API to run in debug mode and to make live changes to the code and see their effect on the frontend without having to rebuild the deployed API. Once the bug was fixed, the changes were pushed to GitHub and the API redeployed.
- A bug was found causing incorrect profile image URLs to be served in the JSON data. This was fixed by overrdiding the `to_representation` method of the Profile and Tribe serializers so that the URL property of each CloudinaryField is used to generate the image URLs.
- Although programatically generated event recurrences appeared to be created correctly when testing via the Django Rest Framework admin interface, once they could be visualised on a calendar in the React frontend a number of issues with recurrences became apparent, including duplicated events on the same day and incorrect recurrence dates. These bugs were caused by incorrect use of the django-recurrence app used to generate the recurrences; the documentation for  django-recurrence is somewhat sparse, so some trial and error experimentation and inspection of the django-recurrence source code to identify relevant kwargs to try was required. The bugs were mostly fixed, with one exception (see below).
- During development of the frontend React application, it was found that requests for calendar events were causing an internal server error after a user was deleted. This was found to be because the user's profile had been deleted, but there were still references to it in some calendar events (e.g. if the user whose account was deleted was invited to an event and/or recorded as having accepted the invitation). This was addressed by performing 'clean-up' actions to remove references to deleted user accounts during the account deletion process.
- The behaviour of monthly recurrences when the original date is at the end of the month proved difficult to refine due to the varying number of days in a month. Initially, recurrences where the orginal event day is in the range `29 - 31` were generated using an offset from the end of the month. For example, monthly recurrences for an event with a date of 30 January 2023 would fall on the 30th of the month for months with 31 days, but the 29th of the month for months with 30 days. [Further research](https://stackoverflow.com/questions/35757778/rrule-for-repeating-monthly-on-the-31st-or-closest-day) eventually led to a better approach which ensures recurring monthly events at the end of the month are appropriately generated for all varying month lengths.
- Frontend testing exposed an issue with duration field data for programatically generated recurrences of calendar events being formatted incorrectly, causing errors in the React app. This was rectified by using a ModelSerializer to format the data for that specific field of the recurrences.
- A browser console error in the React app revealed that Cloudinary images were being served insecurely via http. After unnsuccessfully trying some changes to the Cloudinary configuration in `settings.py` and conducting some further research, it appeared that this might be a bug affecting some other part of the software stack, possibly the django-cloudinary-storage app. A fix was found on [Stack Overflow](https://stackoverflow.com/questions/48508750/how-to-force-https-in-a-django-project-using-cloudinary), requiring the `url_options` dictionary for every reference to an image instance to be individually set to `{'secure': True}`.
- Frontend testing demonstrated that the `company` field of the Contacts model was being omitted from search results. This was a simple fix, as the field had been added to the model later in development, and omitted from the `search_fields` parameter for the filter backends.  

### Unresolved bugs
- The `perform_create` method of the `ListCreate` generic view is overriden in `contacts/views.py`. Django does not seem to respond to custom permission classes in this circumstance, meaning that unauthorised users (i.e. authenticated users without tribe admin status) were able to create new contacts. Print statements at various points in the code were used to verify that the relevant custom permission classes were being invoked and returning the correct values, and it remains uncertain whether this issue is due to a bug in Django Rest Framework or in this project. 

    The issue was overcome by manually checking the status of the user within the `perform_create` method, but given more time it would be desirable to look into this further and revert to correct use of permission classes here if possible.

## Deployment
The TribeHub API is deployed to Heroku, using an ElephantSQL Postgres database.
To duplicate deployment to Heroku, follow these steps:

- Fork or clone this repository in GitHub.
- You will need a Cloudinary account to host user profile images.
- Login to Cloudinary.
- Select the 'dashboard' option.
- Copy the value of the 'API Environment variable' from the part starting `cloudinary://` to the end. You may need to select the eye icon to view the full environment variable. Paste this value somewhere for safe keeping as you will need it shortly (but destroy after deployment).
- Log in to Heroku.
- Select 'Create new app' from the 'New' menu at the top right.
- Enter a name for the app and select the appropriate region.
- Select 'Create app'.
- Select 'Settings' from the menu at the top.
- Login to ElephantSQL.
- Click 'Create new instance' on the dashboard.
- Name the 'plan' and select the 'Tiny Turtle (free)' plan.
- Select 'select region'.
- Choose the nearest data centre to your location.
- Click 'Review'.
- Go to the ElephantSQL dashboard and click on the 'database instance name' for this project.
- Copy the ElephantSQL database URL to your clipboard (this starts with `postgres://`).
- Return to the Heroku dashboard.
- Select the 'settings' tab.
- Locate the 'reveal config vars' link and select.
- Enter the following config var names and values:
    - `CLOUDINARY_URL`: *your cloudinary URL as obtained above*
    - `DATABASE_URL`: *your ElephantSQL postgres database URL as obtained above*
    - `SECRET_KEY`: *your secret key*
    - `ALLOWED_HOST`: *the url of your Heroku app (but without the `https://` prefix)*
- Select the 'Deploy' tab at the top.
- Select 'GitHub' from the deployment options and confirm you wish to deploy using GitHub. You may be asked to enter your GitHub password.
- Find the 'Connect to GitHub' section and use the search box to locate your repo.
- Select 'Connect' when found.
- Optionally choose the main branch under 'Automatic Deploys' and select 'Enable Automatic Deploys' if you wish your deployed API to be automatically redeployed every time you push changes to GitHub.
- Find the 'Manual Deploy' section, choose 'main' as the branch to deploy and select 'Deploy Branch'.
- Your API will shortly be deployed and you will be given a link to the deployed site when the process is complete.

## Credits
- The technique to limit the size of image uploads to cloudinary is adapted from this [Cloudinary](https://support.cloudinary.com/hc/en-us/community/posts/360009752479-How-to-resize-before-uploading-pictures-in-Django) support article
- A replacement for the deprecated `django.conf.urls.url()` was implemented as per this [StackOverflow article](https://stackoverflow.com/questions/70319606/importerror-cannot-import-name-url-from-django-conf-urls-after-upgrading-to)
- The approach to creating a string representation of a many to many field in the Django admin panel is adapted from https://stackoverflow.com/questions/18108521/many-to-many-in-list-display-django
- The technique to create a custom filter for date ranges using django-filters is adapted from this [StackOverflow article](https://stackoverflow.com/questions/37183943/django-how-to-filter-by-date-with-django-rest-framework)
- How to access URL arguments as kwargs in generic APIViews is from this [StackOverflow article](https://stackoverflow.com/questions/51042871/how-to-access-url-kwargs-in-generic-api-views-listcreateapiview-to-be-more-spec)
- How to filter on many-to-many fields is from this [StackOverflow article](https://stackoverflow.com/questions/4507893/django-filter-many-to-many-with-contains)
- The technique to use Python pattern matching as case statements is from this [StackOverflow article](https://stackoverflow.com/questions/11479816/what-is-the-python-equivalent-for-a-case-switch-statement)
- The technique to override the `save()` method of a model to programatically set the value of fields based on the value of other fields is adapted from this [StackOverflow article]:(https://stackoverflow.com/questions/22157437/model-field-based-on-other-fields)
- The approach to obtaining the current user context within a model serializer is from [Stackoverflow](https://stackoverflow.com/questions/30203652/how-to-get-request-user-in-django-rest-framework-serializer)
- The technique for using different serializers depending on the HTTP request type within the same generic class view is from [Stackoverflow](https://stackoverflow.com/questions/22616973/django-rest-framework-use-different-serializers-in-the-same-modelviewset)
- The fix for the Django Rest Framework bug that prevents user's cookies from being cleared on logout is from the Code Institute Django Rest Framework walkthrough project
- The technique for overriding the `to_representation` metehod of a serializer to make a change to the outgoing JSON data used in `profiles/serializers.py` is from [testdriven.io](https://testdriven.io/tips/ed79fa08-6834-4827-b00d-2609205129e0/)
- The code to correctly deal with monthly recurrences of events on days greater than 28th of the month is adapted from [this StackOverflow question](https://stackoverflow.com/questions/35757778/rrule-for-repeating-monthly-on-the-31st-or-closest-day)(although the question is for JavaScript the same rule can be applied in Python).
- The technqiue to sort a list by a dictionary key used to sort events data by start date is from [this StackOverflow question](https://stackoverflow.com/questions/72899/how-do-i-sort-a-list-of-dictionaries-by-a-value-of-the-dictionary)
- The code to force cloudinary to serve images using HTTPS used in serializers is from [this StackOverflow question](https://stackoverflow.com/questions/48508750/how-to-force-https-in-a-django-project-using-cloudinary)

In addition, the following documentation was extensively referenced throughout development:

- [Django documentation](https://www.djangoproject.com)
- [Django Rest Framework documentation](https://www.django-rest-framework.org)
- [django-filter documentation](https://django-filter.readthedocs.io/en/stable/)
- [django-recurrence documentation](https://django-recurrence.readthedocs.io/en/latest/)
- [Python datetime documentation](https://docs.python.org/3/library/datetime.html)
- [dateutil documentation](https://dateutil.readthedocs.io/en/stable/index.html)

