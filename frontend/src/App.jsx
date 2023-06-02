import styled from 'styled-components'
import FailureOverview from './components/FailureOverview/FailureOverview'
import ModeButtons from './components/ModeButtons/ModeButtons'
import SystemStats from './components/SystemStats/SystemStats'
import Livestream from './components/Livestream/Livestream'
import { useState, useEffect } from 'react'
import ModuleContainer from './components/ModuleContainer'
import { StatusCard } from './components/StatusCard'

const AppLayout = styled.div`

  display: flex;
  flex-wrap: wrap;

  justify-content: center;
  align-items: center;
`

const Module = styled.div`
  margin: 5px;
  width: 100%;
`

const targetConversion = new Map([
  ['low_h', 0],
  ['low_s', 1],
  ['low_v', 2],
  ['high_h', 0],
  ['high_s', 1],
  ['high_v', 2],
])


function App() {
  // Filter settings
  const [lowHSV, setLowHSV] = useState([20, 130, 130])
  const [highHSV, setHighHSV] = useState([255, 255, 255])

  function handleChange(target, value) {
    if (target.includes("low_")) {
      let result = lowHSV
      result[targetConversion.get(target)] = parseInt(value)
      setLowHSV([...result])
    }
    else {
      let result = highHSV
      result[targetConversion.get(target)] = parseInt(value)
      setHighHSV([...result])
    }
  }

  // Socket stuff
  const [socketUrl, setSocketUrl] = useState("ws://" + window.location.href.split("/")[2] + "/ws");

  return (
    <>
      <AppLayout className="App">
        <Module>
          <ModuleContainer>
            <StatusCard>
              <p>
                Bachelor Thesis project Computer Science and Engineering
              </p>
            </StatusCard>
            <StatusCard>
              <p style={{padding: "1em", margin: 0}}>
                Utilizing Computer Vision and Machine Learning to detect and handle 3D printing failures autonomously with a limited dataset.
              </p>
            </StatusCard>
            <StatusCard>
              Written by Linus Thorsell and David Sohl
            </StatusCard>
            <StatusCard>
              Links: GitHub, Thesis Paper
            </StatusCard>
          </ModuleContainer>
        </Module>
        <Module>
          <ModeButtons socketUrl={socketUrl} />
        </Module>
        <Module>
          <FailureOverview socketUrl={socketUrl} />
        </Module>
        <Module>
          <Livestream socketUrl={socketUrl} />
        </Module>
        <Module>
          <SystemStats socketUrl={socketUrl} />
        </Module>
      </AppLayout >
    </>
  )
}

export default App
