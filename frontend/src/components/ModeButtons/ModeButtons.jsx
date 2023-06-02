import ModuleContainer from "../ModuleContainer";
import useWebSocket from "react-use-websocket";
import { useState, useEffect } from "react";
import { StatusCard } from "../StatusCard";
import styled from "styled-components";

const Btn = styled.button`
  color: black;
  border: 1px solid black;
  background-color: ${props => props.active ? "lightgreen" : "white"};
`;

const Ebtn = styled.button`
    height: fit-content;
    width: fit-content;

    padding: 0.25em;
    background-color: white;
    color: #252525;
    border: thin solid gray;

    p {
        height: fit-content;
        padding: 0;
        margin: 0;
    }
`

const Input = styled.input`
    padding: 0.25em;
    background-color: white;
    color: black;
    border: thin solid gray;
`

const ControlPanelButtons = styled.div`
    display: flex;
    width: 100%;
    justify-content: space-evenly;
    align-items: center;
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
                        Email for alerts:
                    </label>
                    <Input id="email" type="email" value={alertemail} onChange={(e) => { setalertemail(e.target.value) }}></Input>
                    <Ebtn onClick={() => { let email = document.querySelector("#email"); sendMessage("email=" + email.value); }}><p>Update email</p></Ebtn>
                </ControlPanelButtons>
                <ControlPanelButtons style={{paddingBottom: "1.3em"}}>
                    <label htmlFor="allowedfails">
                        <p>Allowed fails</p>
                        <Input id="allowedfails" type="number" value={allowedfailsnum} onChange={(e) => { sendMessage("allowedfails=" + e.target.value); setallowedfailsnum(e.target.value) }}></Input>
                    </label>
                    <label htmlFor="historylength">
                        <p>History length</p>
                        <Input id="historylength" type="number" value={historylengthnum} onChange={(e) => { sendMessage("historylength=" + e.target.value); sethistorylengthnum(e.target.value) }}></Input>
                    </label>
                </ControlPanelButtons>
            </StatusCard>
        </ModuleContainer>
    );
}
