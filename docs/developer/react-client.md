---
title: React Client
reviewers: Dr Simon Chapman, Dr Marcus Baw
audience: developers
---

## Developer documentation

The demonstration React client for the dGC API is built in React and styled with Semantic UI React. It is intended as a good starting point for understanding the dGC API backend and serves as a prototype client from which you can build your own client, if that is what you require.

It's important to understand the three parts of the dGC platform that are in play here:

1. **React client application** - this comprises the left sidebar with the input boxes and UI tools for inputting data such as heights, weights, age, sex, and gestation at birth. The React client imports the React chart component from NPM, so the chart component is a dependency of the client. When data are entered into the forms and submitted, the React client sends a HTTP request to the:

1. **dGC API server** - which processes the data and returns a JSON response containing calculated centile data, corrected gestational ages, etc. This response is received by the React client which passes it direct into the React chart component without any JSON transformation being required.

1. **React chart component** - this is the right hand side two thirds section of the screen in the demo client, containing the chart vector image. The component can be embedded in any web page and it natively 'understands' the JSON response from the API call. Passing an array of JSON API responses to the React chart component will result in all those measurements being plotted for you.

### Set Up for local development using Docker

1. Enter into your Code Projects directory
```console
cd YourCodeProjects
```

1. Clone the React Client repo
```console
git clone https://github.com/rcpch/digital-growth-charts-react-client.git
```

1. Build the Docker image
```console
s/docker-rebuild
```

1. Start the Docker container
```console
s/docker-start
```

1. Open the React Client in your browser
```console
open http://localhost:3000
```

If you make changes to the dependencies you will need to rebuild the Docker image using `s/docker-rebuild` and restart the Docker container using `s/docker-start`.



### Style

We recommend the use of the Prettier Javascript linter.
