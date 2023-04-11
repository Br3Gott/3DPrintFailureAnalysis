import { useState } from 'react'
import styled from 'styled-components'
import FailureOverview from './FailureOverview'

const AppLayout = styled.div`
  height: 100vh;
  width: 100vw;

  display: grid;
  grid-template-columns: 1fr 1fr 1fr;
`

const Module = styled.div`
  border: 1px solid orange;

  padding: 10px;
`

function App() {
  return (
    <AppLayout className="App">
      <Module>
        <FailureOverview />
      </Module>
      <Module>
        <img src="https://via.placeholder.com/600x400?text=Overview of system stats" />
      </Module>
      <Module>
        <img src="https://via.placeholder.com/600x400?text=Live stream" />
      </Module>

      <Module>
        <img src="https://via.placeholder.com/600x400?text=Controls" />
      </Module>
      <Module>
        <img src="https://via.placeholder.com/600x400?text=Placeholder of a placeholder" />
      </Module>
      <Module>
        <img src="https://via.placeholder.com/600x400?text=Last filtered image" />
      </Module>
    </AppLayout >
  )
}

export default App
