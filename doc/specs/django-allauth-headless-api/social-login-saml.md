Social login and SAML integration
=================================

This document describes the extensions beyond basic account management and
basic login and logout to allow sign-up and login with different identity
Providers (IdP).

1. [Login via SAML-based identity provider](#login-via-saml-based-identity-provider)
    1. [Begin flow](#begin-flow)
    1. [IdP login form](#idp-login-form)
    1. [Confirm e-mail](#confirm-e-mail)

Login via SAML-based identity provider
--------------------------------------

### Begin flow

* URL: `/accounts/saml/mocksaml/login/?process=login`
* The SAML provider has already been chosen before starting the process.
* Clicking the button redirects the client to the IdP login page.

![Start SAML login page](img/saml-login-start-page.png)

### IdP login form

![SAML IdP login page](img/saml-login-idp-page.png)

### Confirm e-mail

* URLs: `/accounts/confirm-email/` and `/accounts/confirm-email/.../`
* After the first login, the e-mail address must be verified.
* This is the exact same flow as when signing up for a local account (see below).

![Confirmation sent page](img/confirmation-sent-page.png)
![Confirm e-mail page](img/confirm-email-page.png)

TODO: API Calls