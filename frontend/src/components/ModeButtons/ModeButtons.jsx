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
`;

const ControlPanelButtons = styled.div`
    display: flex;
    width: 100%;
    justify-content: center;
    background-color: white;
    color: black;
`

export default function ModeButtons({ socketUrl }) {

    const [allowedfailsnum, setallowedfailsnum] = useState(3);
    const [historylengthnum, sethistorylengthnum] = useState(5);

    const [fails, setfails] = useState(0);
    const [historylen, sethistorylen] = useState(0);
    
    const [alertemail, setalertemail] = useState("");

    const { sendMessage, lastMessage, readyState } = useWebSocket(socketUrl, { retryOnError: true });
    const [active, setActive] = useState(false);

    useEffect(() => {
        if (lastMessage !== null) {
            let res = JSON.parse(lastMessage.data);

            if (res["on"] != null) {
                setActive(res["on"])
            }
            else if (res["controlpanel"] != null) {
                setallowedfailsnum(res["controlpanel"].allowedfails);
                sethistorylengthnum(res["controlpanel"].historylength);

                setfails(res["controlpanel"].currfails);
                sethistorylen(res["controlpanel"].currhistorylen);
            }
            else if (res["email"] != null) {
                setalertemail(res["email"]);
            }
        }
    }, [lastMessage]);

    return (
        <ModuleContainer>
            <StatusCard>Control Panel</StatusCard>
            <StatusCard>
                <ControlPanelButtons>
                    <p>Printer protection:</p>
                </ControlPanelButtons>
                <ControlPanelButtons>
                    <Btn onClick={() => { sendMessage("activate"); setActive(true) }} active={active}>Activated</Btn>
                    <Btn onClick={() => { sendMessage("deactivate"); setActive(false) }} active={!active}>Deactivated</Btn>
                </ControlPanelButtons>
                <ControlPanelButtons>
                    <p>{fails} failed of {historylen}</p>
                </ControlPanelButtons>
                <ControlPanelButtons>
                    <label htmlFor="email">
                        <p>Email for alerts:</p>
                        <input id="email" type="email" value={alertemail} onChange={(e) => {setalertemail(e.target.value) }}></input>
                        <button onClick={() => { let email = document.querySelector("#email"); sendMessage("email=" + email.value); }}>Update email</button>
                    </label>
                </ControlPanelButtons>
                <ControlPanelButtons>
                    <label htmlFor="allowedfails">
                        <p>Allowed fails</p>
                        <input id="allowedfails" type="number" value={allowedfailsnum}></input>
                    </label>
                    <label htmlFor="historylength">
                        <p>History length</p>
                        <input id="historylength" type="number" value={historylengthnum} onChange={(e) => { sendMessage("historylength=" + e.target.value); sethistorylengthnum(e.target.value) }}></input>
                    </label>
                </ControlPanelButtons>
            </StatusCard>
        </ModuleContainer>
    );
}
