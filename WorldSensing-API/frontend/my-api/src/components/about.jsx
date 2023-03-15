import React from 'react'
import '../styles/about.css'
// import { Route } from 'react-router-dom'

function Api() {
    return (
        <div>
            <div className="about">
                <table>
                    <tr>
                        <td><h2> About </h2></td>
                        <td><a className="docs" href = 'https://fastapi.tiangolo.com/'>fastApi Docs</a></td>
                    </tr>
                </table>
            </div>
             
            <p>
            FastAPI is a modern, fast (hence the name) web framework for building APIs with Python. It's built on top of Starlette for the web parts and Pydantic for the data parts, which means that it provides a very efficient and easy-to-use interface for defining API routes and models, with great performance and type checking. It's commonly used to build web services and back-end applications, but it can also be used to create microservices or full-stack applications.
            </p>
            <p>
            React, on the other hand, is a JavaScript library for building user interfaces. It's commonly used for creating complex and interactive web applications, especially single-page applications (SPAs). React allows developers to create reusable UI components, handle state and props, and efficiently update the UI when data changes.
            </p>
            <p>
            FastAPI and React can be used together to create full-stack web applications. FastAPI is used to create the API endpoints that serve data to the React front-end, while React is used to create the user interface and handle user interactions. This approach allows for a more efficient and scalable way of building web applications, since each part of the application can be developed and maintained independently.
            </p>
            <p>
            To connect the FastAPI back-end with the React front-end, you can use a technique called API calls. This involves using JavaScript functions to fetch data from the API endpoints defined in FastAPI and update the React components with the retrieved data. This way, you can create a seamless user experience where the front-end and back-end work together to provide dynamic and real-time updates.
            </p>
        </div>
    );
}

export default Api;