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

    const { sendMessage, lastMessage, readyState } = useWebSocket(socketUrl, { retryOnError: true });
    const [data, setData] = useState([])

    useEffect(() => {
        if (lastMessage !== null) {
            let res = JSON.parse(lastMessage.data);

            if (res["regular"] != null) {
                // set regular state
            } else if (res["ps"] != null) {
                setData([...res["ps"]])
            }
        }
    }, [lastMessage]);

    return (
        <ModuleContainer>
            <StatusCard>
                System Status
            </StatusCard>
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
                        <StatusCardSplit key={process.processId}>
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