import React from 'react'
import ReactDOM from 'react-dom'

function Home() {
    return (
        <p><strong>Hello, React!</strong></p>
    )
}

ReactDOM.render(
  React.createElement(Home, window.props),
  window.reactMount,
)
