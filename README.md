# TribeHub

## Project goals

This project provides a Django Rest Framework backend for the TribeHub React web app. It has also been designed with a future native iOS app in mind.

TribeHub is designed to be a virtual equivalent to the typical wall planner a family might put up in a kitchen or other communal area. The primary goals of the web app are to:
1) Provide busy families with a single, central hub around which to plan and organise busy lives and schedules. This should include calendar/event scheduling functionality similar to a family wall planner, enabling events to be scheduled for one or multiple family members, and viewed by all the family.
2) Deliver a simple and intuitive user experience, suitable for adults and tech literate children aged 10+. 
3) Offer a minimal set of impactful features chosen in order to deliver a useful app within an achievable development timeframe, while laying a solid foundation for additional features in the future.

## Table of contents

## CRUD functionality

## Planning

### Data models

### API endpoints

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

## Testing

### Manual testing

### Automated testing

### Python validation

### Resolved bugs

### Unresolved bugs

## Deployment

## Credits

### Code

- How to fully define a field within an array field from [Stack Overflow](https://stackoverflow.com/questions/41180829/arrayfield-missing-1-required-positional-argument)
- Technique to limit the size of image uploads to cloudinary adapted from this [Cloudinary](https://support.cloudinary.com/hc/en-us/community/posts/360009752479-How-to-resize-before-uploading-pictures-in-Django) support article
- Replacement for deprecated `django.conf.urls.url()` implemented as per this [StackOverflow article](https://stackoverflow.com/questions/70319606/importerror-cannot-import-name-url-from-django-conf-urls-after-upgrading-to)
- Approach to creating a string representation of a many to many field in the Django admin panel from https://stackoverflow.com/questions/18108521/many-to-many-in-list-display-django

