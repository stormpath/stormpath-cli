## Stormpath CLI

A command-line client for the Stormpath REST API (https://stormpath.com).

### Install:

    pip install stormpath-cli

### Usage:


#### Get an API Key

First things first, if you haven't already go and sign up for a Stormpath account [here](https://api.stormpath.com/register).
All requests to the Stormpath REST API must be authenticated with an API Key. To get an API key: 

  * Log in to the [Stormpath Admin Console](https://api.stormpath.com/login) using the email address and password you used to register with Stormpath.
  * In the top-right corner of the resulting page, visit Settings > My Account.
  * On the Account Details page, under Security Credentials, click Create API Key.

This will generate your API Key and download it to your computer as an apiKey.properties file. If you open the file in a text editor, you will see something similar to the following:

    apiKey.id = 144JVZINOF5EBNCMG9EXAMPLE
    apiKey.secret = lWxOiKqKPNwJmSldbiSkEbkNjgh2uRSNAb+AEXAMPLE


  * Save this file in a secure location, such as your home directory in a hidden .stormpath directory. For example:
  * Also change the file permissions to ensure only you can read this file. For example, on *nix operating systems:

    chmod go-rwx $HOME/.stormpath/apiKey.properties

It might be useful to fist familiarize yourself with the [Stormpath REST API](http://docs.stormpath.com/rest/product-guide/) and the naming used there in. 


#### Setting up the CLI

To setup the CLI tool run the following command (if the file `$HOME/.stormpath/apiKey.properties` exists it will be used automatically):

    stormpath setup

If you already had the `$HOME/.stormpath/apiKey.properties` file in place you should see the following output:

    Using API Key file /home/myuser/.stormpath/apiKey.properties for authentication.
    API Key written to /home/myuser/.stormpath/cli/apiKey.properties
    Stormpath CLI is set up and ready to go!

If you don't have the `apiKey.proerpties` file in place, to setup the CLI tool you will get prompted to enter
the API key and secret:

    Unable to discover an existing API Key file path or API Key environment variable.
    Please input your API Key ID and API Key Secret.
    (visit http://docs.stormpath.com/rest/quickstart/#get-an-api-key for more information)
    API Key ID:
    API Key Secret:
    API Key written to /home/myuser/.stormpath/cli/apiKey.properties


#### Override default settings

To override the default setting we just set up in the previous step there are several options available.
You can pass `-a` or `--apikey` flags to every command:

    stormpath command -a 144JVZINOF5EBNCMG9EXAMPLE:lWxOiKqKPNwJmSldbiSkEbkNjgh2uRSNAb+AEXAMPLE
    stormpath command --apikey 144JVZINOF5EBNCMG9EXAMPLE:lWxOiKqKPNwJmSldbiSkEbkNjgh2uRSNAb+AEXAMPLE

`WARNING` : don't use if there are other users on the machine, since the key and the secret will be visible to anyone using the `ps` command to list the running processes.

Point to a different `apiKey.properties` file like so:

    stormpath command --apikeyfile /home/myuser/apiKeyAlternate.properties

Using Environment variables:

    STORMPATH_APIKEY=144JVZINOF5EBNCMG9EXAMPLE:lWxOiKqKPNwJmSldbiSkEbkNjgh2uRSNAb+AEXAMPLE stormpath command
    STORMPATH_APIKEY_FILE=/home/myuser/apikey.properties stormpath command

If none of the described methods are found then the CLI tool will raise an error:

    Unable to discover an existing API Key file path or API Key environment variable.

#### Stormpath CLI actions

The stormpath cli tool uses the following format:

    stormpath [<action>] [<resource>] [options]

Supported actions are as follows:

  * list    -  List/search resources on Stormpath
  * create  -  Create a resource on Stormpath
  * update  -  Update a resource on Stormpath
  * delete  -  Remove a resource from Stormpath
  * set     -  Set context for user/group actions
  * context -  Show currently used context for user/group actions
  * setup   -  Set up credentials for accessing the Stormpath API

And supported resources are:

  * application  -   Application Resource
  * directory    -   Directory Resource
  * group        -   Group Resource
  * account      -   Account Resource
  * user         -   User Resource

If no action is specified the CLI defaults to a `list` actions. So the following 2 commands are the same:

    stormpath list applications
    stormpath applications

Which results in the following output:

    Using API Key file /home/myuser/.stormpath/cli/apiKey.properties for authentication.
    [
      {
        "defaultAccountStoreMapping": null, 
        "defaultGroupStoreMapping": null, 
        "description": null, 
        "href": "https://api.stormpath.com/v1/applications/4tlsArn68oWmwungvwo8PQ", 
        "name": "My Application", 
        "status": "ENABLED"
      }, 
      {
        "defaultAccountStoreMapping": null, 
        "defaultGroupStoreMapping": null, 
        "description": "Manages access to the Stormpath Console and API.", 
        "href": "https://api.stormpath.com/v1/applications/717TBJKdavce58Ox3iFuXA", 
        "name": "Stormpath", 
        "status": "ENABLED"
      }
    ]


Note how the cli tool supports using plural and singular forms (ie. `applications` and `application` do the same thing).

#### Creating an Application
    
To create an application issue the following command:

    stormpath create application -n "My Application" -d "My App created with CLI"

To automatically create a Directory for that application use `-R` or `--create-directory` flags:

    stormpath create application -n "My Application" -R
    stormpath create application -n "My Application" --create-directory

Test to see if the app and directory got created:

    stormpath list applications
    stormpath list directories

Depending on what resource you're referencing there are required and optional flags:

For applications, directories, groups: 
    
    -n, --name              required, the name of the resource
    -d, --description       optional, the description of the resource
    -R, --create-directory  optional, auto create directory
    
For accounts:

    -e, --email             required, the email property of the account
    -p, --password          required, the password property of the account
    -g, --given-name        required, the givenName property of the account
    -s, --surname           required, the surname property of the account
    -u, --username          optional, the username property
    -m, --middle-name       optional, the middleName property
    -f, --full-name         optional, the full name property
    
For Accounts and Groups:

    -A, --in-application
    -D, --in-directory      For All Resources
    -S, --status            optional, the status of the resource
    -j, --json              JSON representation of the resource

#### Update an Application

To update an application we use the `update` action and the `-n` or `--name` flags to specify the application name
we wish to update:

    stormpath update application -n "My Application"  -d "Updated description for this app"

Update commands require an identifier that identifies the resource:

For Applications, Directories, Groups:
    
    -n, --name  required, identifier name
    
For Accounts:
    
    -e, --email required, account email


#### Deleting a Resource

To delete a resource, a resource must be identified:

For Applications, Directories, Groups:
    
    -n, --name  required, identifier name
    
For Accounts:
    
    -e, --email required, account email

For example to delete an Application:

    stormpath delete -n "My Application"

Or and Account:

    stormpath delete -e "myuser@email.com"

You are going to be prompted to confirm the deletion. If you wish to avoid getting prompted use the `-F` flag.


#### Using raw JSON instead of flags:

If you wish you can use raw JSON to represent the Resource your trying to access:

    stormpath create application --json='{"name": "My App", "description": "My App created with CLI"}'


#### Creating Accounts/Groups


Since Accounts and Groups are tied to Applications and Directories when creating them we need to specify the flags
`-A` (that is `--in-applications`) or -D (that is `--in-directory`). For example:

    stormpath create account --username myuser --email myuser@email.com --password SomePassword12 --in-application "My Application"

    stormpath create group "My Group" --in-application "My Application"

Or we can use the JSON representation:
    
    stormpath create account --json '{"username": "myuser", "email": "myuser@email.com", "password": "SomePassword12"}' --in-application "My Application"

To avoid having to use the `--in-application` or `--in-directory` flags over and over you can set the context for all of the Accounts/Groups commands using the `set` command like so:

    stormpath set application -n "My Application"

Which will yield the following output:

    Current context is set to the application "My Application". Account / Groups actions are configured to target "My Application"

The same goes for directories:

    stormpath set directory --name "My Directory"

From here on out all the Account / Group actions are going to be targeted for the set application/directory.

To see the current context use the following command:

    stormpath context

Output:

    Using context from file /home/myuser/.stormpath/cli/context.properties.
    Current context set to the application 'My Application'.
    Account / Groups actions are configured to target 'My Application'.


# Copyright & Licensing

Copyright © 2012, 2013, 2014 Stormpath, Inc. and contributors.

This project is licensed under the [Apache 2.0 Open Source License](http://www.apache.org/licenses/LICENSE-2.0).

For additional information, please see the full [Project Documentation](https://www.stormpath.com/docs/python/product-guide).