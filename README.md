[![Logo](https://patx.github.io/micropie/logo.png)](https://patx.github.io/micropie)

## **Introduction**

**MicroPie** is a lightweight Python web framework that makes building web applications simple and efficient. It includes features such as routing, session management, WSGI support, and Jinja2 template rendering.

### **Key Features**
*"Fast, efficient, and deliciously simple."*

- 🚀 **Easy Setup:** Minimal configuration required. Our setup is so simple, you’ll have time for dessert.
- 🔄 **Routing:** Maps URLs to functions automatically. So easy, even your grandma could do it (probably).
- 🔐 **Sessions:** Simple session management using cookies.
- 🎨 **Templates:** Jinja2 for dynamic HTML pages.
- ⚡ **Fast & Lightweight:** No unnecessary dependencies. Life’s too short for bloated frameworks.
- 🖥️ **WSGI support:** Deploy with WSGI servers like gunicorn making web development easy as... pie!

## **Installing MicroPie**
### **Normal Installation**
To install MicroPie [from the PyPI](https://pypi.org/project/MicroPie/) run the following command:
```bash
pip install micropie
```
This will install MicroPie along with `jinja2` as a dependency, enabling the built-in `render_template` method. This is the recommended way to install this framework.

### **Minimal Installation**
If you prefer an ultra-minimalistic setup, you can run MicroPie without installing Jinja. Simply download the standalone script:

[MicroPie.py](https://raw.githubusercontent.com/patx/micropie/refs/heads/main/MicroPie.py)

Place the script in your project directory, and you're good to go. Please note you will not be able to use the `render_template` method. It will raise an `ImportError`, unless you have Jinja installed via `pip install jinja2`.

## **Getting Started**

Create a basic MicroPie app in `app.py`:

```python
from MicroPie import Server

class MyApp(Server):
    def index(self, name="Guest"):
        return f"Hello, {name}!"

MyApp().run()
```

Run the server:

```bash
python app.py
```

Visit your app at [http://127.0.0.1:8080](http://127.0.0.1:8080).

## **Core Features**

### **1. Routing**
Define methods to handle URLs:
```python
class MyApp(Server):
    def hello(self):
        return "Hello, world!"
```

**Access:**
- Basic route: [http://127.0.0.1:8080/hello](http://127.0.0.1:8080/hello)

### **2. Handling GET Requests**

MicroPie allows passing data using query strings (`?key=value`) and URL path segments.

#### **Query Parameters**

You can pass query parameters via the URL, which will be automatically mapped to method arguments:

```python
class MyApp(Server):
    def greet(self, name="Guest"):
        return f"Hello, {name}!"
```

**Access:**
- Using query parameters: [http://127.0.0.1:8080/greet?name=Alice](http://127.0.0.1:8080/greet?name=Alice)
  - This will return: `Hello, Alice!`
- Using URL path segments: [http://127.0.0.1:8080/greet](http://127.0.0.1:8080/greet)
  - This will return: `Hello, Guest!`

#### **Path Parameters (Dynamic Routing)**

You can also pass parameters directly in the URL path instead of query strings:

```python
class MyApp(Server):
    def greet(self, name):
        return f"Hello, {name}!"
```

**Access:**
- Using path parameters: [http://127.0.0.1:8080/greet/Alice](http://127.0.0.1:8080/greet/Alice)
  - This will return: `Hello, Alice!`
- Another example: [http://127.0.0.1:8080/greet/John](http://127.0.0.1:8080/greet/John)
  - This will return: `Hello, John!`

#### **Using Both Query and Path Parameters Together**

```python
class MyApp(Server):
    def profile(self, user_id):
        age = self.query_params.get('age', ['Unknown'])[0]
        return f"User ID: {user_id}, Age: {age}"
```

**Access:**
- [http://127.0.0.1:8080/profile/123?age=25](http://127.0.0.1:8080/profile/123?age=25)
  - Returns: `User ID: 123, Age: 25`
- [http://127.0.0.1:8080/profile/456](http://127.0.0.1:8080/profile/456)
  - Returns: `User ID: 456, Age: Unknown`

#### **Other Considerations for GET requests**
In **MicroPie**, the `index` method serves as the default route handler, which behaves differently compared to other route methods such as `greet` or any custom-defined handlers.

##### Key Differences:

1. **Default Handling:**  
   - When the root URL (`/`) is accessed, the framework automatically maps the request to the `index` method.  
   - Other methods (e.g., `greet`) must be explicitly accessed via their route, such as `/greet`.

2. **URL Parameter Handling:**  
   - The `index` method does **not** receive URL path parameters in the same way as other route methods.  
   - Instead, it primarily relies on query parameters (e.g., `/index?name=John`).  
   - Other methods can accept parameters directly from the URL path (e.g., `/greet/John`).

##### Example Usage:

| URL                  | Method Called             | Notes                                  |
|--------------------- |--------------------------|----------------------------------------|
| `/`                  | `index()`                 | Default route, no path parameters.    |
| `/index?name=John`   | `index(name="John")`       | Query parameters work.                 |
| `/greet/John`        | `greet("John")`            | Path parameters are passed correctly.  |
| `/<dynamic_path>`    | **Not supported**          | Will result in a 404 error.            |

**Note:** Dynamic paths such as `/<dynamic_path>` will not work with the `index` method. Instead, they should be explicitly handled using dedicated route methods.

By understanding this distinction, you can structure your routes effectively when using MicroPie.

### **3. Handling POST Requests**

MicroPie supports handling form data submitted via HTTP POST requests. Form data is automatically mapped to method arguments.

#### **Handling Form Submission with Default Values**

```python
class MyApp(Server):
    def submit(self, username="Anonymous"):
        return f"Form submitted by: {username}"
```

#### **Accessing Raw POST Data**

```python
class MyApp(Server):
    def submit(self):
        username = self.body_params.get('username', ['Anonymous'])[0]
        return f"Submitted by: {username}"
```

#### **Handling Multiple POST Parameters**

```python
class MyApp(Server):
    def register(self):
        username = self.body_params.get('username', ['Guest'])[0]
        email = self.body_params.get('email', ['No Email'])[0]
        return f"Registered {username} with email {email}"
```

### 4. **WSGI Support**
MicroPie includes built-in WSGI support via the wsgi_app() method, allowing you to deploy your applications with WSGI-compatible servers like Gunicorn.

#### **Example**
Create a file named app.py:
```python
from MicroPie import Server

class MyApp(Server):
    def index(self):
        return "Hello, WSGI World!"

app = MyApp()
wsgi_application = app.wsgi_app
```

Run `app.py` with:
```bash
gunicorn app:wsgi_application
```

#### Why Use WSGI?
WSGI (Web Server Gateway Interface) is the standard Python interface between web servers and web applications. Deploying with a WSGI server like Gunicorn provides benefits such as:
- Better Performance: Multi-threaded and multi-process capabilities.
- Scalability: Easily handle multiple requests concurrently.
- Production Readiness: Designed for high-load environments.

### **5. Handling Sessions**
MicroPie has built in session handling:
```python
class MyApp(Server):

    def index(self):
        # Initialize or increment visit count in session
        if 'visits' not in self.session:
            self.session['visits'] = 1
        else:
            self.session['visits'] += 1

        return f"Welcome! You have visited this page {self.session['visits']} times."

MyApp().run()
```

### **6. Jinja2 Built In**
MicroPie has Jinja template engine built in. You can use it with the `render_template` method. You can also implement any other template engine you would like.

#### **`app.py`**
Save the following as `app.py`:
```python
class MyApp(Server):
    def index(self):
        # Pass data to the template for rendering
        return self.render_template("index.html", title="Welcome", message="Hello from MicroPie!")

MyApp().run(port=8080)
```

#### **HTML**
In order to use the `render_template` method you must put your HTML template files in a directory at the same level as `app.py` titled `templates`. Save the following as `templates/index.html`:
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ title }}</title>
</head>
<body>
    <h1>{{ message }}</h1>
    <p>This page is rendered using Jinja2 templates.</p>
</body>
</html>
```

### **7. Serving Static Files**
MicroPie can serve static files (such as CSS, JavaScript, and images) from a static directory using the built in `serve_static` method. To do this you must define a route you would like to serve your static files from. For example:
```python
class Root(Server):
    def static(self, filename):
        return self.serve_static(filename)
```

#### **Setup**
- Create a directory named `static` in the same location as your MicroPie application. For saftey the `serve_static` method will only work if `filename` is in the `static` directory.
- Place your static files (e.g., style.css, script.js, logo.png) inside the static directory.

#### **Accessing Static Files**
Static files can be accessed via the `/static/` URL path. For example, if you have a file named `style.css` in the `static` directory, you can access it using:
```
http://127.0.0.1:8080/static/style.css
```

### **8. Streaming Responses and WebSockets**

#### **Streaming Response Support**
MicroPie provides support for streaming responses, allowing you to send data to the client in chunks instead of all at once. This is particularly useful for scenarios where data is generated or processed over time, such as live feeds, large file downloads, or incremental data generation.

#### How It Works
Streaming is supported through the `wsgi_app` method, making it compatible with WSGI servers like **Gunicorn** or the built in `run` method. When a route handler returns a generator or an iterable (excluding strings), MicroPie automatically streams the response to the client.

With the following saved as `app.py`:
```python
import time
from MicroPie import Server

class Root(Server):

    def index(self):
        def generator():
            for i in range(1, 6):
                yield f"Chunk {i}\n"
                time.sleep(1)  # Simulate slow processing or data generation
        return generator()

app = Root()
wsgi_app = app.wsgi_app
```
Run your application with `gunicorn app:wsgi_app`. For best performance with streaming, consider tuning Gunicorn settings such as worker types (e.g., `--worker-class gevent`) to handle long-lived connections efficiently.

#### **WebSockets Integration**
MicroPie applications can seamlessly integrate **WebSockets** by running a separate WebSocket server using Python’s `websockets` library. This enables real-time, bidirectional communication between clients and the server, independent of the HTTP server being used. To get started with WebSockets in MicroPie, ensure you have the `websockets` package installed `pip install websockets`.

#### How It Works

- **The HTTP server (MicroPie)** handles regular web requests and serves the frontend.
- **A separate WebSocket server** runs concurrently to handle real-time communication.
- Clients connect to the WebSocket server via the frontend and exchange messages asynchronously.
- **Threading Considerations:** Since the WebSocket server runs in a separate thread, developers should handle shared resources carefully to avoid concurrency issues.
- **Port Management:** The WebSocket server must run on a different port than the HTTP server to avoid conflicts.
- **Client Compatibility:** Ensure that clients support WebSockets when implementing features relying on real-time communication.

**For a full example showing `websockets` and MicroPie check out the [chatroom example](https://github.com/patx/micropie/tree/main/examples/chatroom).**

## **API Reference**

### Class: Server

#### run(host='127.0.0.1', port=8080)
Starts the WSGI server with the specified host and port.

#### get_session(request_handler)
Retrieves or creates a session for the current request. Sessions are managed via cookies.

#### cleanup_sessions()
Removes expired sessions that have surpassed the timeout period.

#### redirect(location)
Returns a 302 redirect response to the specified URL.

#### render_template(name, **args)
Renders a Jinja2 template with provided context variables.

#### validate_request(method)
Validates incoming requests for both GET and POST methods based on query and body parameters.

#### wsgi_app(environ, start_response)
WSGI-compliant method for parsing requests and returning responses. Ideal for production deployment using WSGI servers.

#### serve_static(filename)
Serve static files from the `static` directory.

## **Examples**
Check out the [examples folder](https://github.com/patx/micropie/tree/main/examples) for more advanced usage, including template rendering, session usage, websockets, streaming and form handling.

## **Feature Comparison: MicroPie, Flask, CherryPy, and Bottle**

| Feature             | MicroPie  | Flask      | CherryPy  | Bottle     | Django            | FastAPI    |
|---------------------|-----------|------------|-----------|------------|-------------------|------------|
| **Ease of Use**     | Very Easy | Easy       | Easy      | Easy       | Moderate          | Moderate   |
| **Routing**         | Automatic | Manual     | Manual    | Manual     | Automatic         | Automatic  |
| **Template Engine** | Jinja2    | Jinja2     | None      | SimpleTpl  | Django Templating | Jinja2     |
| **Session Handling**| Built-in  | Extension  | Built-in  | Plugin     | Built-in          | Extension  |
| **Request Handling**| Simple    | Flexible   | Advanced  | Simple     | Advanced          | Advanced   |
| **Performance**     | High [^1] | High       | Moderate  | High       | Moderate          | Very High  |
| **WSGI Support**    | Yes       | Yes        | Yes       | Yes        | Yes               | No (ASGI)  |
| **Async Support**   | No        | No (Quart) | No        | No         | Limited           | Yes        |
| **Deployment**      | Simple    | Moderate   | Moderate  | Simple     | Complex           | Moderate   |


[^1]: *Note that while MicroPie is high-performing for lightweight applications, it may not scale well for complex, high-traffic web applications due to the lack of advanced features such as asynchronous request handling and database connection pooling, which are found in frameworks like Django and Flask. To achieve similiar performance with MicroPie use `gunicorn` with `gevent`.*

## **Suggestions or Feedback?**
We welcome suggestions, bug reports, and pull requests!
- File issues or feature requests [here](https://github.com/patx/micropie/issues).

