## Planning

I set out with modest expectations for this project with the awareness that the application would be limited in its functionality. The goal was to produce a prototype that covers as much ground as possible with regard to learning and practicing database-related concepts. This was achieved for the most part.

## Implementation

The features that have been implemented are listed in the [user stories](https://github.com/Nurou/devServices/blob/master/documentation/user-stories.md) documentation. The ones checked with a ticket have been implemented, and those without have not been.

### Areas of Expansion/Improvement

Below are some ways in which the application could be enhanced further:

- Separate login functionality for the agency's developers so that they are able to manage the projects that they've been assigned to
- Enabling clients to choose the developers to work on a given project themselves
- Adding a chat box that connects the clients with the agency staff
- Email clients/staff on changes to an order
- The cost of developers and their experience level are not factored into anything as it stands. The orders could have some sort of projected cost calculation based on these and other variables.
- Various usability and aesthetic improvements, such as adding icons/images for services

## Issues Encountered

These were the main ones:

- Continual modification of the database schema leads to a lot of time-consuming refactoring
- Reflecting structural changes to the local database onto the remote database - there must/should be a smoother way of doing
- WTForms and Bootstrap integration was good for the most part, but there were difficulty in implementing certain use cases, such as having a multi-select checkbox list.
- Issues with Heroku and database configuration took up a significant chunk of the time allocated for the project, which took away from feature implementation.

## What I learned

- Planning the database structure in as much detail as possible before implementation is essential for smooth progress in feature implementation
- Python, Flask, and SQLAlchemy make implementing simple CRUD applications a breeze
- ORMs really do make life easier
