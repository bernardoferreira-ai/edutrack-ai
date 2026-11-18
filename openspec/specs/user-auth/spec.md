# user-auth Specification

## Purpose

Define the client-side authentication requirements for user registration, login, and profile visualization in `pages/3_👤_Perfil.py` using EduTrack AI's existing Xano authentication endpoints (`auth/signup`, `auth/login`, `auth/me`).

## Requirements

### Requirement: User Registration Form
The system SHALL provide a registration form in `pages/3_👤_Perfil.py` collecting `name`, `email`, and `password`, submitting them to the `POST auth/signup` endpoint to persist the user in the `user` table.

#### Scenario: Successful registration
- **WHEN** user submits valid name, email, and password in the registration form
- **THEN** system calls `POST auth/signup`, stores the returned `authToken` in `st.session_state`, and displays a success notification

#### Scenario: Registration failure with existing email
- **WHEN** user submits an email that is already registered
- **THEN** system receives an error from `POST auth/signup` and displays a user-friendly error message

### Requirement: User Login Form
The system SHALL provide a login form in `pages/3_👤_Perfil.py` collecting `email` and `password`, submitting them to the `POST auth/login` endpoint.

#### Scenario: Successful login
- **WHEN** user provides valid credentials in the login form
- **THEN** system calls `POST auth/login`, saves the returned `authToken` in `st.session_state`, fetches profile details, and presents the authenticated profile view

#### Scenario: Invalid credentials
- **WHEN** user provides incorrect email or password
- **THEN** system receives an access-denied error from `POST auth/login` and displays an error message

### Requirement: Authenticated Profile Display
The system SHALL display the authenticated user's profile details (`name`, `email`, `role`, `created_at`) retrieved from the `GET auth/me` endpoint when an active `authToken` is present in `st.session_state`.

#### Scenario: Fetching and rendering profile details
- **WHEN** user has a valid `authToken` in session
- **THEN** system calls `GET auth/me` with header `Authorization: Bearer <authToken>` and renders the user's details

### Requirement: User Logout
The system SHALL allow an authenticated user to log out from `pages/3_👤_Perfil.py`, clearing the session state and returning to the login/signup view.

#### Scenario: User clicks logout
- **WHEN** authenticated user clicks the logout button
- **THEN** system removes the `authToken` and profile data from `st.session_state` and displays the login/signup interface

### Requirement: Profile Visual Design Enhancement
The system SHALL render visually enhanced presentation cards, typography, and layout styles for both authenticated user profile view and unauthenticated access views (login/signup) in `pages/3_👤_Perfil.py`, preserving all existing forms, options, inputs, buttons, and state behaviors.

#### Scenario: Rendering authenticated profile view
- **WHEN** an authenticated user opens `pages/3_👤_Perfil.py`
- **THEN** the system SHALL display the user details inside styled presentation cards with custom CSS, showing profile info, active status badge, PDF download section, and logout action

#### Scenario: Rendering unauthenticated login and signup view
- **WHEN** an unauthenticated visitor opens `pages/3_👤_Perfil.py`
- **THEN** the system SHALL display styled welcome and authentication card containers with tabs for login and registration, retaining the exact email, password, and name inputs

### Requirement: Authentication Form Box Visual Enhancement
The system SHALL display a centered, elevated, and styled form card for user login and registration in `pages/3_👤_Perfil.py`, preserving all existing form inputs, options, buttons, and authentication flows.

#### Scenario: Viewing login and registration box
- **WHEN** an unauthenticated visitor opens `pages/3_👤_Perfil.py`
- **THEN** the system SHALL render the authentication form box centered on the page with modern card borders, shadows, styled submission buttons, and refined input fields

### Requirement: Red Authentication Buttons Styling
The system SHALL style the "Entrar" (Login) and "Cadastrar" (Signup) submission buttons in `pages/3_👤_Perfil.py` with a vibrant red color scheme, preserving all submission logic and options.

#### Scenario: User views login and signup form buttons
- **WHEN** an unauthenticated visitor opens `pages/3_👤_Perfil.py`
- **THEN** the system SHALL render the "Entrar" and "Cadastrar" buttons with red gradient backgrounds and styled shadows

