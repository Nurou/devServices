# DevServices Agency

You can access the application locally at http://localhost:5000, or remotely at https://dev-services.herokuapp.com/

The application offers two, very different, sets of functionalities:

1. **Client**
2. **Admin**

This has been achieved by implementing role-based authentication - certain pages are only viewable to accounts associated with a certain role, CLIENT or ADMIN in this instance.

Both of which are described in detail below.

# Client 

## Registration

You can register by navigating to the **Register** page by - the link for which is found in the header menu in the top right-hand corner.

Enter the required information into the form fields. The form uses error messages to prompt you in case any of the inputs do not meet the required input-validation requirements. Fix these as necessary. A successful registration will result in you being automatically directed to the login page. You have now registered a client account, and have a set of credentials required to log in.

## Client Login



Logging in grants access the application's services. Use the credentials that you received upon registration. You may also use a test account to log in without registration. The credentials for this account are the following:

| USERNAME | PASSWORD | ROLE |
| -------- | -------- | ---- |
| client   | password | N/A  |

This account provides access to all of the application's functionality.


## Account Management

Once you've logged in you'll be directed to your account page. Here you can update your profile information and navigate to other areas of the application, namely your orders. You also have the option of deleting your account. Since this is the homepage for a client, clicking on the logo in the top left-hand corner will also redirect you to this page.

## Orders

The client functionality is primary related to making and managing orders.

The orders section of the application can be navigated to through from your account's profile page (described in the section above). 

### Viewing Orders

On the orders page, you are able to view all of the orders that you've made, each with a hyperlink to the individual order for further inspection. 

Clicking on any given order in the order listing will take you to a page specific to that order where you are displayed all the details pertaining to said order, including its status (complete/in progress).

### Making Orders

You can navigate to the page for making a new order by clicking on the 'make new order' button on the orders page, or by clicking the header navigation link titled 'New Order', both of which direct you to the same page.

On the 'New Order' page is a form in which you are able to add the details for your order, such as a description of its requirements and the type of service required. Clicking on the 'order' button located below the form will confirm your submission, and the order is now in accessible to the agency staff.

You will then be redirected back to the orders page where you can continue inspecting and modifying any ongoing orders.

### Order Progress

Once the agency is done with your order, you will be able to see that under the 'status' column on the information table for an order.

### Updating Orders

Orders can be updated for as long as they're in progress. 

### Cancelling Orders

Orders can be cancelled by clicking on the 'cancel' button located beneath the order information table, to the right of the 'update' button. Your browser window will prompt you for confirmation before the order is completely removed from the system. This action cannot be undone! 

---

# Admin 

## Admin Login

To login as admin, you need to the credentials to an account with admin authority. Clicking on 'Admin' in the header menu in the top right-hand corner will direct you to a page that has a set of admin credentials listed that you may use to login.

A successful login will direct you to the admin dashboard and you are now able to navigate to the admin-only pages.

## Clients

The 'Clients' page is navigable through the header navigation menu. This page has a list of all of the agency's clients with some of the details relating to them, including the number of orders made by each.

## Orders

This page is navigable through the top header navigation menu. Here is a list of all the orders made by all of the agency's clients, each with a link to view the order in more detail. 

### Updating Orders

An admin has the right to mark orders as complete. This is done by clicking on the 'View Order' button on the orders page, followed by clicking the 'Mark Done' button. This update will also be reflected on the client's side.

### Assigning Developers

Under the order details table, a list of developer's that are available to be assigned to the given order is presented. Only the developer's with the requested service in their skill repertoire can be assigned to a given order. Also, a developer can only work on a maximum of 3 orders at any given time.

## Developers

The 'Developers' page, also navigable through the header navigation menu, is for viewing and managing the agency's developers. Details about them, including the order's that they've been assigned to are on display here. The page also has a 'Add Developer' link, which takes you to a page for adding a new developer to the agency.

### Adding Developers

Similar to orders, new developers are added by filling a form with their details. The skills attached to each developer determine the types of projects that they are then available to work on.


## Services

The 'Services' page contains the services currently offered by the agency - these are the services that clients can choose from when making orders. New services can be added by clicking 'Add Service'. 

---

## Log out

To **Logout**, click the logout link located in the top right-hand corner. The link is only shown to you if you're logged in.
