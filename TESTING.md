# Testing

## Contents

- [Functional Testing](#functional-testing)
- [User Stories Testing](#user-stories-testing)
- [Validator Testing](#validator-testing)
  - [HTML](#html)
  - [CSS](#css)
  - [JS](#js)
  - [Python](#python)
- [WAVE](#wave)
- [LightHouse](#lighthouse)
  - [Destop Results](#desktop-results)
  - [Mobile Results](#mobile-results)
- [Browser Compatibility](#browser-compatibility)
- [Responsivity](#responsivity)
- [Issues/ Bugs Found & Resolved](#issues-bugs)
- [Unresolved](#unresolved)

---

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