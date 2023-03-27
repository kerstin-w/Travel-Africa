# Testing

## Contents

- [Manual Testing](#manual-testing)
- [Automated Testing](#automated-testing)
- [User Stories Testing](#user-stories-testing)
- [Validator Testing](#validator-testing)
  - [HTML](#html)
  - [CSS](#css)
  - [JS](#js)
  - [Python](#python)
- [LightHouse](#lighthouse)
  - [Destop Results](#desktop-results)
  - [Mobile Results](#mobile-results)
- [Browser Compatibility](#browser-compatibility)
- [Responsivity](#responsivity)
- [Issues/ Bugs Found & Resolved](#issues-bugs)
- [Unresolved](#unresolved)

---

## <a name="automated-testing">Automated Testing</a>

Python **Automated Unit Testing** was implemented using the [Django Unit Testing](https://docs.djangoproject.com/en/3.2/topics/testing/overview/) framework.  
**Unit Tests** have been written to cover all **Forms**, **Models**, **Views**, **Admin**, **Context-Processors** and **Fields**.
I implemented unit testing only at the end of the project, because it was not a mandatory requirement. However, during testing I realized the importance of implementing unit testing from the start of a project in order to ensure the functionality of the code permanently during the development process.
A total of **171** **Unit Tests** have been written. All **171** tests run successfully without errors or warnings.   

<details>
    <summary>Coverage Automated Testing</summary>
    <img src="documentation/testing/automated-testing/coverage-1.png">
    <img src="documentation/testing/automated-testing/coverage-2.png">
</details>

<br>

## <a name="user-stories-testing">User Stories Testing</a>

All functionalities have been tested and they work as expected. You can find more about [Manual Testing](#manual-testing). 

### As a first-time visitor,
  - [#1](https://github.com/kerstin-w/Travel-Africa/issues/1) I want to know what this site is about immediately so that I can decide whether I will explore further.

    This was achieved with a nice hero banner, asking the user to explore the blog about Africa.

    <img src="documentation/testing/user-stories/hero1.png" width="500px" style="margin: 20px;">

  - [#2](https://github.com/kerstin-w/Travel-Africa/issues/2) I want to navigate pages so that I can understand what types of information I can find.

    This was achieved with a navbar which is fully responsive and functionality has been tested and works as expected.
    <img src="documentation/testing/user-stories/navbar.png" width="500px" style="margin: 20px;">

<br>

### As an unregistered User,
  - [#3](https://github.com/kerstin-w/Travel-Africa/issues/3) I can view a list of posts so that I can select one to read.

    In the navbar the user can select, wether to see a list of all post or post of a certain region. Afterwards a list of posts will be displayed and the user can select a post to read.

    <img src="documentation/testing/user-stories/post-list.png" width="500px" style="margin: 20px;">

  - [#4](https://github.com/kerstin-w/Travel-Africa/issues/4) I can select a category so that I can only view relevant posts.
    
    In the **navbar** the user can select, wether to see a list of all post or post of a certain region. Once a certain category was selected only posts of this category will be displayed. When creating a post, the auther has to select a region in order for the categorization to work. 

    This was achieved with a navbar which is fully responsive and functionality has been tested and works as expected.
    <img src="documentation/testing/user-stories/navbar.png" width="500px" style="margin: 20px;">
    <img src="documentation/testing/user-stories/regions.png" width="500px" style="margin: 20px;">

  - [#5](https://github.com/kerstin-w/Travel-Africa/issues/5) I can view a list of highlights posts so that I can select one to read.

    On the **Home Page** the user has the option to select 1 of 6 featured posts. The admin user can select featured posts either in the admin panel or on the post update page.

    <img src="documentation/testing/user-stories/featured.png" width="500px" style="margin: 20px;">
    <img src="documentation/testing/user-stories/featured-admin.png" width="500px" style="margin: 20px;">

  - [#6](https://github.com/kerstin-w/Travel-Africa/issues/6) I can create an account so that I can sign in and use of the sites full functionality.

    From the **navbar** the user can select **Register** to create a a user account. Afterwards the user is able to use all features, create posts, like post, user the bucket list and comment on posts.

    <img src="documentation/testing/user-stories/signup.png" width="500px" style="margin: 20px;">

  - [#13](https://github.com/kerstin-w/Travel-Africa/issues/13) I can search a post by a keyword so that I can try to find posts relative to the keyword.

    From the **navbar** the user can use the search function and enter a keyword. If the keywords was found in one of the post titles or countries those related posts will be displayed as search result.
    
    <img src="documentation/testing/user-stories/search.png" width="500px" style="margin: 20px;">

  - [#15](https://github.com/kerstin-w/Travel-Africa/issues/15) I can view comments so that I can read other users feedback.

    On a Post the comments are displayed for every user. 

    <img src="documentation/testing/user-stories/comment.png" width="500px" style="margin: 20px;">

<br>

### As an registered User,
  - [#7](https://github.com/kerstin-w/Travel-Africa/issues/7) I can view my own account so that I can manage my account easily.

    From the **navbar** the user can click on the small profile picture and the Profile Page will open. From the Profile Page the user has the option to **delete the account**, **edit the account** and reset the password. 

    <img src="documentation/testing/user-stories/profile.png" width="500px" style="margin: 20px;">

  - [#8](https://github.com/kerstin-w/Travel-Africa/issues/8) I can Edit/Update my account so that my profile is up to date.

    From the **Profile Page** the user can select the pen icon to edit or update their own profile or reset the password. 
    <img src="documentation/testing/user-stories/edit-profile.png" width="500px" style="margin: 20px;">

  - [#9](https://github.com/kerstin-w/Travel-Africa/issues/9) I can delete my account so that I can remove my footprint from the website if I am no longer active.

    From the **Profile Page** the user can select the bin icon to delete the profile. Afterwards a modal opens to confirm that the user is certain to delete the profile. Once the profile is delete all posts and comments of this user are deleted as well. 

    <img src="documentation/testing/user-stories/delete-profile.png" width="500px" style="margin: 20px;">

  - [#10](https://github.com/kerstin-w/Travel-Africa/issues/10) I can create a post so that I can share my experiences with other users.

    From the **navbar** the user can select the pen and paper icon and the profile create page will open. Before a post is published it needs to be approved be the admin first.

    <img src="documentation/testing/user-stories/create-post.png" width="500px" style="margin: 20px;">

  - [#11](https://github.com/kerstin-w/Travel-Africa/issues/11) I can edit my posts so that I can keep them current and amend mistake.

    On the **Post Page** the user can select the pen icon to edit the post. Afterwards the form will open to update the current post information. Once the post is updated it goes into the admins approval again.

    <img src="documentation/testing/user-stories/update-post-1.png" width="500px" style="margin: 20px;">
    <img src="documentation/testing/user-stories/update-post-2.png" width="500px" style="margin: 20px;">
    
  - [#12](https://github.com/kerstin-w/Travel-Africa/issues/12) I can delete my posts so that I can control the information that I share.

    On the **Post Page** the user can select the bin icon to delete the post. Afterwards a modal will open to confirm that the user is certain to delete the post.

    <img src="documentation/testing/user-stories/update-post-1.png" width="500px" style="margin: 20px;">
    <img src="documentation/testing/user-stories/delete-post.png" width="500px" style="margin: 20px;">

  - [#14](https://github.com/kerstin-w/Travel-Africa/issues/14) I can leave a comment on a post so that I can exchange with the author an be    involved in a conversation.

    On the **Post Page** the user can leave a comment to the related post. Before a comment is publish it will go into admin approval first.

    <img src="documentation/testing/user-stories/comment-section.png" width="500px" style="margin: 20px;">

  - [#16](https://github.com/kerstin-w/Travel-Africa/issues/16) I can like a post so that highlight useful content for other users.

    On the **Post Page** the user can on the heart button to like a post. Once post is liked the user can click the button again to unlike the post.

    <img src="documentation/testing/user-stories/like.png" width="300px" style="margin: 20px;"><img src="documentation/testing/user-stories/unlike.png" width="300px" style="margin: 20px;">

  - [#17](https://github.com/kerstin-w/Travel-Africa/issues/17) I can receive an email notification if another user commented on my post so that I can engage in a conversation with other users.

    Once user wrote a comment and the comment was approved by the admin, the user will receive a email notification.
    *Note: After I took the screenshot, I added the link to the related post to the comment confirmation mail.*

    <img src="documentation/testing/user-stories/comment-mail.png" width="500px" style="margin: 20px;">

  - [#18](https://github.com/kerstin-w/Travel-Africa/issues/18) I can can add a Post to my bucket list so that I can save destinations I want to travel to.

    On the **Post Page** the user can select the Bucket List button to add a post to the bucket list. From the **navbar** the user can click on the list icon to open their personal bucket list, where selected posts are stored. On the **Bucket List Page** the user can click on a certain post to revisit the post or select the bin icon to remove it. One a post is saved to the bucket list, on the Post Page the button is disabled. 

    <img src="documentation/testing/user-stories/bucketlist-1.png" width="300px" style="margin: 20px;">
    <img src="documentation/testing/user-stories/bucketlist-added.png" width="300px" style="margin: 20px;">
    <img src="documentation/testing/user-stories/bucketlist-disabled.png" width="300px" style="margin: 20px;">
    <img src="documentation/testing/user-stories/bucketlist-2.png" width="300px" style="margin: 20px;">

  - [#19](https://github.com/kerstin-w/Travel-Africa/issues/19) I can delete my comments so that I can control the information that I share.

    On the **Post Page** in the comment section the user can select the bin icon to delete a comment. This functionallity is available for the author of the post, and the commenter. After the user clicked on the bin icon a modal will open to confirm that the user is certain to delete the comment.

    <img src="documentation/testing/user-stories/delete-comment.png" width="300px" style="margin: 20px;">
    <img src="documentation/testing/user-stories/delete-comment-modal.png" width="300px" style="margin: 20px;">


  - [#26](https://github.com/kerstin-w/Travel-Africa/issues/26) I can rely on the app to log me out automatically so that strangers cannot access my profile in case I am on a public computer.
    
    A timeout for the user is setup in the settings, loggin the user out after 30mins or once the user closed the browser.
    <br>
        ```
        # Settings for Session Time Out
        SESSION_EXPIRE_SECONDS = 1800
        SESSION_TIMEOUT_REDIRECT = "/"
        SESSION_EXPIRE_AT_BROWSER_CLOSE = True
        ```
  - [#27](https://github.com/kerstin-w/Travel-Africa/issues/27) I can be routed to a error page in case a page is not found so that I understand the error and click on a link to get back to the homepage.

    A error page has been setup, in case user try to access a page without permission, the page does not exist or other errors occure.

    <img src="documentation/testing/user-stories/error-1.png" width="500px" style="margin: 20px;">
    <img src="documentation/testing/user-stories/error-2.png" width="500px" style="margin: 20px;">

  - [#31](https://github.com/kerstin-w/Travel-Africa/issues/31) I want to reset my password so that I can regain access to my account if I forget my password.
    
    On the **Login Page** the user can select *Forgot Password** to reset the password. Afterwards an **email** will be send to the user with a link to confirm. This link will redirect the user to the **change password page**. On the **change password page** the user can enter a new password. 

    <img src="documentation/testing/user-stories/forgot-password.png" width="300px" style="margin: 20px;">
    <img src="documentation/testing/user-stories/forgot-password-2.png" width="300px" style="margin: 20px;">
    <img src="documentation/testing/user-stories/forgot-password-3.png" width="300px" style="margin: 20px;">
    <img src="documentation/testing/user-stories/forgot-password-mail.png" width="300px" style="margin: 20px;">
    <img src="documentation/testing/user-stories/forgot-password-4.png" width="300px" style="margin: 20px;">

<br>

- As an Superuser,
  - [#28](https://github.com/kerstin-w/Travel-Africa/issues/28) I want to create a category when needed so that I can manage the site effectively.
  - [#29](https://github.com/kerstin-w/Travel-Africa/issues/29) I want to delete content when inappropriate so that I can maintain the site and ensure that only useful or relevant content remains
  - [#30](https://github.com/kerstin-w/Travel-Africa/issues/30) I want to block user accounts so that I can ensure only trusted users can access the site.

<br>

## <a name="validator-testing">Validator Testing</a>

### <a name="html">HTML</a>
All **HTML** code was validated using the [W3C Markup Validation Service](https://validator.w3.org/) regularly during the development process. **The HTML Source Code** was regularly viewed for each page using **Google Chrome** and passed through the [W3C Markup Validation Service](https://validator.w3.org/). Various minor errors were encountered and corrected during the final **HTML** validation check. 
A few errors occurred with summernote during the validation process. The `summernot-div` had attributes for `cols` and `rows` which resulted in an error during validation. I fixed that by copying the `widget_iframe.html` into my templates and styling the width with my custom CSS. Remaining issues with Summernote are the `<textarea>` element, which is set to `hidden=true` and CSS Parse Erros for blog posts that users created using Summernote. After consulting with Tutor Support about it, they advised me not to try and fix it since I did not develope the package myself and this could result in the package not functioning correctly. Besides Summernote, all HTML code now passes validation with no errors or warnings. 

### Errors during validation check

<details>
    <summary>Home Page</summary>
    <img src="documentation/validator/html/index-1.png">
    <img src="documentation/validator/html/index-2.png">
</details>
<details>
    <summary>Profile Page</summary>
    <img src="documentation/validator/html/profile.png">
</details>
<details>
    <summary>Bucket List Page</summary>
    <img src="documentation/validator/html/bucketlist-1.png">
    <img src="documentation/validator/html/bucketlist-2.png">
</details>
<details>
    <summary>Create Post Page</summary>
    <img src="documentation/validator/html/post-create-1.png">
    <img src="documentation/validator/html/post-create-2.png">
</details>
<details>
    <summary>Post Page</summary>
    <img src="documentation/validator/html/post-detail-1.png">
    <img src="documentation/validator/html/post-detail-2.png">
</details>

### Remaining Summernote Errors 
<details>
    <summary>Create Post Page</summary>
    <img src="documentation/validator/html/summernote-1.png">
</details>
<details>
    <summary>Post Page</summary>
    <img src="documentation/validator/html/summernote-2.png">
</details>

<br>

### <a name="css">CSS</a>
**Custom CSS Styling** from [style.css](static/css/style.css) was validated using the [W3C CSS Validation Service](https://jigsaw.w3.org/css-validator/).
Some *"Due to their dynamic nature, CSS variables are currently not statically checked"* warnings were generated.
These warnings are related to the global variables declared at the top of [style.css](static/css/style.css). 
The warnings are generated because the [W3C CSS Validation Service](https://jigsaw.w3.org/css-validator/) does not currently support CSS global variable declaration, and are not considered to be an issue. 
Some additional *"vendor extension"* warnings were also generated. These warnings are not considered to be an issue since the vendor extensions are to enable correct display of various elements in different browsers. 
*Imported style sheets are not checked in direct input and file upload modes* warnings were generated. Theses warnings are related to the Google Fonts and are not considered to be an issue, but just an information that imported style sheets cannot be validated. 
One error was generated using `clipath: circle()` without any values. I corrected this error and afterwards no errors were generated.

<details>
    <summary>Result</summary>
    <img src="documentation/validator/css/jigsaw-result.png">
</details>
<details>
    <summary>Warnings during validation check</summary>
    <img src="documentation/validator/css/jigsaw-warnings.png">
</details>
<details>
    <summary>Error during validation check</summary>
    <img src="documentation/validator/css/jigsaw-error.png">
</details>

<br>

### <a name="js">JavaScript</a>

The custom [script.js](static/js/script.js) was validated using the [JSHint](https://jshint.com/about/) static code analysis tool. 
A wanring *"One unused variable"* was generated for the `tooltipList` which I resolved by refactoring the code. Afterwards the test passed without errors or warnings.
Due to the lack of complexity of **JavaScript** code implemented on the project, **Automated Unit Testing** 
of the **JavaScript** code was considered unnecessary. All **JavaScript** functions and event handlers in the custom **JavaScript Code Libraries** have been thoroughly manually de-bugged and tested in the console.

<details>
    <summary>Result</summary>
    <img src="documentation/validator/js/jshint-result.png">
</details>
<details>
    <summary>Warning during validation check</summary>
    <img src="documentation/validator/js/jshint-warning.png">
</details>

<br>

### <a name="Python">Python</a>
All **Python Code** was thoroughly de-bugged and tested at the command line during the development process, and has been validated 
using [Flake8](https://flake8.pycqa.org/). [flake8-django](https://pypi.org/project/flake8-django/) was also installed to assist with validation.  
**Flake8** was configured by creating a `setup.cfg` file in the root of the project, which contains the following settings:
```
[flake8]
exclude = */migrations/*.py, *__init__.py, *_pychache_*, *settings.py*, .vscode, env.py
```
The settings exclude **django** migrations, `__init__.py`, `.vscode` and `_pychache_` files, as these are system generated files and do not need to be checked.  
*settings.py* (line too long) errors are ignored as it is not possible to shorten the affected lines of code without causing application errors.  
*env.py* (line too long) errors are ignored as it is not possible to shorten the affected lines of code without causing application errors.  

<details>
    <summary>Result</summary>
    <img src="documentation/validator/python/flake8.png">
</details>