# API Automation Framework (Python+Pytest)

Python API automation framework that does its job in a simple but effective way. It is designed to work with HTTP APIs but can be adapted to work with other protocols.

Libraries used:

- Pytest - Test Runner
- Requests - HTTP client
- Python-dotenv - Environment management with .env files
- Flake8 - Linting
- Black - Formatting

## Setup

Before you begin, make sure you have Python installed on your machine.

### Preparing your Environment

Before starting with the setup, ensure you have a local copy of the repository. Follow these steps to clone the repository and set up your environment:

1. Navigate to the project directory on your terminal. This is where the `requirements.txt` file is located.

    ```bash
    cd testing
    ```

2. Install the necessary dependencies by running the following command in the root folder:

    ```bash
    pip install -r requirements.txt
    ```

### Setting up your local environment

The `.env` file is used to store environment variables that are important for running your tests. By default, this file is not tracked by Git to prevent sensitive data like usernames and passwords from being shared publicly.

- Start by copying the `example.env` file provided in the project directory:

    ```bash
    cp example.env .env
    ```

- Open the `.env` file in your preferred text editor and update the following properties with your local environment values:

    ```yaml
    BASE_URL=api_base_url
    ```

    Make sure to replace `api_base_url` with the actual values you wish to use for testing. The `BASE_URL` should point to the base URL of the API you are testing. 

**Note:** It is crucial to **never** commit these values or your personal environment variables to version control in a real project, as it can expose sensitive information.
    
### VS Code Extensions

Five VS Code extensions are recommended for this project:

- Python (ms-python.python): Python language support
- Pylance (ms-python.vscode-pylance): Python language server
- Flake8 (ms-python.flake8): Linter
- Black (ms-python.black-formatter): Code formatter
- TODO Highlight (jgclark.vscode-todo-highlight): Bug management

They will be recommended to the user on the setup since they are set as recommendations in the extension.json file.

### Running the tests

```bash
# Runs all tests
pytest
```
```bash
# Runs smoke tests
pytest -m smoke
```


### Flake8

You can use flake8 with the help of the VS Code extension and with the following script.

```bash
flake8
```

### Black

Black is configured to run with flake8 and to format the code on each save. 
In case you want to run it separately use the following scripts:

- Check for issues:
    
    ```bash
    black --check .
    ```
    
- Resolve issues:
    
    ```bash
    black .
    ```
    
## Getting started

The idea behind this framework is to encapsulate endpoints on Service Models, for maintainability and reusability. You can think of Service Models as an analogy of Page Object Models for UI Automation.

## Service Models

In this framework, Service Models are used to encapsulate the API endpoints you are testing. This abstraction allows for better maintainability and reusability of your test code. The concept here is somewhat similar to the Page Object Model used in UI Automation, where each service model represents a specific set of functionality provided by your API.

### Understanding `ServiceBase`

The `ServiceBase` class is the foundation of all Service Models. It provides common functionality needed for making API requests and processing responses. When you create a new Service Model, it should extend `ServiceBase` to inherit these capabilities. This approach ensures consistency and reduces boilerplate code in your service models.

Here's what `ServiceBase` offers:

- **API Client Management**: It initializes and holds an instance of the `ApiClient`, ensuring that all service models use the same API client setup.
- **Base URL Configuration**: It dynamically sets the base URL for API requests using the `BASEURL` from your `.env` file. This allows for flexibility across different environments (e.g., development, staging, production).
- **Authentication**: The `authenticate` method simplifies the process of authenticating with the API. Once called, it stores the authentication token in the request headers, so subsequent API calls are authenticated. Note that as explained below in the [Authentication](#authentication) section, this is specific to this API, and must be adapted to your use case.
- **HTTP Methods**: `ServiceBase` provides methods for common HTTP requests (GET, POST, PUT, PATCH, DELETE, HEAD, OPTIONS). These methods handle the request execution and timing, then format the response into a standardized `Response` object, making it easier to work with.

### Extending `ServiceBase`

When you create a Service Model, you extend `ServiceBase` and define methods specific to the service you're testing. For example, a `BookingService` might have methods like `getBooking` or `createBooking`. Each method uses the HTTP methods provided by `ServiceBase` to interact with the API.

Here's a simple example of a service model:

```python
from typing import List

from src.base.service_base import ServiceBase
from src.models.responses.base.response import Response
from src.models.responses.booking.booking_response import (
    BookingIdResponse
)


class BookingService(ServiceBase):
    def __init__(self):
        super().__init__("/booking")

    def get_booking_ids(
        self, params: dict = None, config: dict = None
    ) -> Response[List[BookingIdResponse]]:
        config = config or self.default_config
        if params:
            config["params"] = params
        return self.get(self.url, config=config, response_model=List[BookingIdResponse])
```

By extending ServiceBase, BookingService gains all the functionalities of making HTTP requests, handling authentication, and standardizing responses, allowing you to focus on the logic specific to the Booking service.

### Other Models

In addition to **Service Models**, you should declare **Request** and **Response** models as needed. For example, here is the BookingModel that will be used to deserialize the response from the endpoint above.

```python
from pydantic import BaseModel
from typing import Optional


class BookingDates(BaseModel):
    checkin: Optional[str] = None
    checkout: Optional[str] = None


class BookingModel(BaseModel):
    id: Optional[int] = None
    firstname: Optional[str] = None
    lastname: Optional[str] = None
    totalprice: Optional[int] = None
    depositpaid: Optional[bool] = None
    bookingdates: Optional[BookingDates] = None
    additionalneeds: Optional[str] = None
```

## Tests

Next, you can create a simple test like this. 

```python
import pytest
from src.models.services.booking_service import BookingService

@pytest.fixture
def booking_service():
    return BookingService()

def test_get_booking_successfully(booking_service):
    booking_id = 123456
    response = booking_service.get_booking(booking_id)
    assert response.status == 200
```

And you can easily assert against the response body properties.

```python
def test_get_booking_successfully(booking_service, created_booking):
    booking_id = created_booking.data.bookingid
    response = booking_service.get_booking(booking_id)
    assert response.status == 200
    assert response.data.firstname == created_booking.data.booking.firstname
    assert response.data.lastname == created_booking.data.booking.lastname
    assert response.data.totalprice == created_booking.data.booking.totalprice
    assert response.data.depositpaid is True
    assert (
        response.data.bookingdates.checkin
        == created_booking.data.booking.bookingdates.checkin
    )
    assert (
        response.data.bookingdates.checkout
        == created_booking.data.booking.bookingdates.checkout
    )
    assert response.data.additionalneeds == created_booking.data.booking.additionalneeds
```

In the example above, I am using a call to the add_booking endpoint to create the booking needed for the get_booking test, and then using the newly created booking to assert against it.

## Performance

Request duration is measured and saved to the response_time property of the response object. Therefore, you can add assertions to check the response time of each request.

```python
def test_get_booking_successfully_response_time(booking_service):
    booking_id = 123456
    response = booking_service.get_booking(booking_id)
    assert response.response_time < 1000
```

This makes adding simple but powerful performance checks to your API automation suite easy.

## Authentication

The authentication process depends on the method required by the API, but in most cases, it involves sending tokens in the request headers.

In this repository, the API uses an `/auth` endpoint to obtain a token, which is then sent in the request headers as a cookie. To streamline this process, I've added an `authenticate()` method in the `ServiceBase` class, making it easy to authenticate with the API.

Additionally, the token is cached so that subsequent calls to `authenticate()` from any service do not result in unnecessary requests to the server.

Here's the implementation of the `authenticate()` method:

```python
    def authenticate(
        self,
        auth_method: AuthMethod = AuthMethod.USERNAME_PASSWORD,
        credentials: Dict[str, Any] = None,
    ) -> None:
        """
        Uses the specified authentication method to generate the auth headers.

        Args:
            auth_method (AuthMethod): The authentication method to use.
            credentials (Dict[str, Any]): A dictionary of credentials.
                For BEARER: expects {"token": str}.
                For BASE64: expects {"encoded": str}.
                For COOKIE: expects {"cookie": str}.
                For USERNAME_PASSWORD: expects {"username": str, "password": str}.
        """
        if not credentials:
            credentials = {
                "username": os.getenv("USERNAME"),
                "password": os.getenv("PASSWORD"),
            }

        auth_config = Authenticator.authenticate(auth_method, credentials)

        if auth_method != AuthMethod.USERNAME_PASSWORD:
            self.default_config = auth_config
            return

        username = credentials.get("username")
        password = credentials.get("password")
        cached_token = SessionManager.get_cached_token(username, password)
        if cached_token:
            self.store.headers["Cookie"] = f"token={cached_token}"
            self.headers.update(self.store.headers)
            return

        credentials_req = CredentialsModel(username=username, password=password)
        response = self.post(f"{self.base_url}/auth", json=credentials_req.__dict__)

        raw_data = response.json()
        auth_response = AuthResponse.model_validate(raw_data)
        SessionManager.store_token(username, password, auth_response.token)
        self.store.headers["Cookie"] = f"token={auth_response.token}"
        self.headers.update(self.store.headers)
```

Then you can use it on the services that require authentication, like in the before hook below.

```python
import pytest
from src.models.services.booking_service import BookingService

@pytest.fixture
def booking_service():
    service = BookingService()
    service.authenticate()
    return service

def test_delete_booking_successfully(booking_service):
    booking_id = 123456
    response = booking_service.delete_booking(booking_id)
    assert response.status == 204
```

## Contribution Guidelines

I welcome contributions from everyone and value your input and ideas. Here's how you can contribute:

1. **Fork the Repository**: Begin by forking the repository to your GitHub account. This creates your own copy of the project where you can make your changes.

2. **Clone the Forked Repo**: Clone the forked repository to your local machine to start working on the changes.

    ```bash
    git clone https://github.com/YOUR_USERNAME/YOUR_FORKED_REPO.git
    ```

3. **Create a New Branch**: Create a new branch on your local repository for each set of changes you want to make. This keeps your modifications organized and separate from the main project.

    ```bash
    git checkout -b your-new-branch-name
    ```

4. **Make Your Changes**: Implement your changes, fix a bug, add a new feature, or update documentation as needed in your new branch.

5. **Commit Your Changes**: Commit your changes with a clear and descriptive commit message. This message should explain what you've done and why.

    ```bash
    git commit -m "Add a concise but descriptive commit message"
    ```

6. **Push Changes to Your Fork**: Push your changes to your fork on GitHub.

    ```bash
    git push origin your-new-branch-name
    ```

7. **Submit a Pull Request**: Go to your fork on GitHub and click the 'New pull request' button. Select the original repository as the base and your branch as the compare. Fill in the pull request with a title and description that explains your changes.

8. **Wait for Review**: Wait for the review of your changes. Be ready to make additional changes based on the feedback.

9. **Merge**: Once your changes have been approved, they will be merged into the main project.

Please ensure that your code adheres to the project's standards and has passed all tests. 


## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE.txt) file for details.
