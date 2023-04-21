import ModuleContainer from "../ModuleContainer";
import useWebSocket from "react-use-websocket";
import { useState, useEffect } from "react";
import { StatusCard } from "../StatusCard";
import styled from "styled-components";

const Btn = styled.button`
  margin: 1em;
  color: black;
  border: 1px solid black;
  background-color: ${props => props.active ? "lightgreen" : "white"};
`

export default function Livestream({ socketUrl }) {
    const { sendMessage, lastMessage, readyState } = useWebSocket(socketUrl, { retryOnError: true });
    const [active, setActive] = useState(false);

    useEffect(() => {
        if (lastMessage !== null) {
            let res = JSON.parse(lastMessage.data);

            if (res["on"] != null) {
                setActive(res["on"])
            }
        }
    }, [lastMessage]);

    return (
        <ModuleContainer>
            <StatusCard>Control Panel</StatusCard>
            <StatusCard>
                <Btn onClick={() => { sendMessage("activate"); setActive(true) }} active={active}>Activate</Btn>
                <Btn onClick={() => { sendMessage("deactivate"); setActive(false) }} active={!active}>Deactivate</Btn>
            </StatusCard>
        </ModuleContainer>
    );
}
