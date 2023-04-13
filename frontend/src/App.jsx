import styled from 'styled-components'
import FailureOverview from './components/FailureOverview/FailureOverview'
import FilterSettings from './components/FilterSettings/FilterSettings'
import SystemStats from './components/SystemStats/SystemStats'
import Controls from './components/Controls/Controls'
import Livestream from './components/Livestream/Livestream'
import FilteredImage from './components/FilteredImage/FilteredImage'
import { useState, useEffect } from 'react'
import useWebSocket, { ReadyState } from 'react-use-websocket';
import ModuleContainer from './components/ModuleContainer'
import { StatusCard } from './components/StatusCard'

const AppLayout = styled.div`
  height: 100vh;
  width: 100vw;

  display: flex;
  flex-wrap: wrap;

  justify-content: center;
  align-items: center;
`

const Module = styled.div`
  padding: 15px;
  width: 100%
  height: 100%;
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

  const [socketUrl, setSocketUrl] = useState('ws://10.8.160.199:8080/ws');

  return (
    <>
      <Module>
        <ModuleContainer>
          <StatusCard>
            Bachelor Thesis project Computer Science and Engineering
          </StatusCard>
          <StatusCard>
            Utilizing Computer Vision and Machine Learning to detect and handle 3D printing failures autonomously with a limited dataset.
          </StatusCard>
          <StatusCard>
            Written by Linus Thorsell and David Sohl
          </StatusCard>
          <StatusCard>
            Links: GitHub, Thesis Paper
          </StatusCard>
        </ModuleContainer>
      </Module>

      <AppLayout className="App">
        <Module>
          <FailureOverview socketUrl={socketUrl} />
        </Module>
        <Module>
          <SystemStats socketUrl={socketUrl} />
        </Module>
        <Module>
          <Livestream />
        </Module>

        <Module>
          <Controls />
        </Module>
        <Module>
          <FilterSettings lowHSV={lowHSV} highHSV={highHSV} handleChange={handleChange} />
        </Module>
        <Module>
          <FilteredImage low_hsv={lowHSV} high_hsv={highHSV} />
        </Module>
      </AppLayout >
    </>
  )
}

export default App
