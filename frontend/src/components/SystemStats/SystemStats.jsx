import styled from "styled-components"
import ModuleContainer from "../ModuleContainer"
import { StatusCard, StatusCardSplit, StatusCardScrollable } from "../StatusCard"
import useWebSocket, { ReadyState } from 'react-use-websocket';
import { useState, useEffect } from 'react'

const StatusCardItem = styled.div`
    padding: 5px;

    width: calc(100% / 6);
    max-height: 6em;
    overflow: hidden;
`;
const LargeStatusCardItem = styled(StatusCardItem)`
    width: calc(100% / 4.5)
`

export default function SystemStats({ socketUrl }) {

    const { sendMessage, lastMessage, readyState } = useWebSocket(socketUrl);
    const [data, setData] = useState([])
    console.log(data)

    useEffect(() => {
        if (lastMessage !== null) {
            // console.log(lastMessage.data)
            let res = JSON.parse(lastMessage.data);
            // console.log(res)

            if (res["regular"] != null) {
                // set regular state
            } else if (res["ps"] != null) {
                // setStats(res["ps"])
                console.log("hej stat")
                setData([...res["ps"]])
            }
        }
    }, [lastMessage]);

    const diskUsage = 1.5;
    const diskAvailable = 8;
    const cpuTemperature = 75;
    const memoryUsage = 700;
    const cpuFrequency = 450;

    return (
        <ModuleContainer>
            <StatusCard>
                System Status
            </StatusCard>
            <StatusCardSplit>
                <LargeStatusCardItem>Disk: {diskUsage}/{diskAvailable}gb ({(diskUsage / diskAvailable) * 100}%)</LargeStatusCardItem>
                <LargeStatusCardItem>CPU Freq: {cpuFrequency}Mhz</LargeStatusCardItem>
                <LargeStatusCardItem>Memory Usage: {memoryUsage}mb</LargeStatusCardItem>
                <LargeStatusCardItem>CPU Temp: {cpuTemperature}</LargeStatusCardItem>
            </StatusCardSplit>
                <StatusCardSplit>
                    <StatusCardItem>User</StatusCardItem>
                    <StatusCardItem>Process Id</StatusCardItem>
                    <StatusCardItem>CPU Usage</StatusCardItem>
                    <StatusCardItem>RAM Usage</StatusCardItem>
                    <StatusCardItem>Command</StatusCardItem>
                </StatusCardSplit>
            <StatusCardScrollable>
                {data.map(process => {
                    return (
                        <StatusCardSplit>
                            <StatusCardItem>{process.user}</StatusCardItem>
                            <StatusCardItem>{process.processId}</StatusCardItem>
                            <StatusCardItem>{process.cpu}%</StatusCardItem>
                            <StatusCardItem>{process.memory}%</StatusCardItem>
                            <StatusCardItem>{process.command}</StatusCardItem>
                        </StatusCardSplit>
                    )
                })}
            </StatusCardScrollable>
        </ModuleContainer>
    )
}