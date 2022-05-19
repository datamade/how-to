import React from 'react'
import { createRoot } from 'react-dom/client'

function Home() {
    return (
        <p><strong>Hello, React!</strong></p>
    )
}

const container = document.getElementById('App')
const root = createRoot(container)
root.render(<Home />)
