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
