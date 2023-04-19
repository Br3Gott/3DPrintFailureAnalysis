import ModuleContainer from "../ModuleContainer";
import useWebSocket from "react-use-websocket";
import { useState, useEffect } from "react";
import { StatusCard } from "../StatusCard";

export default function Livestream({ socketUrl }) {
  const { sendMessage, lastMessage, readyState } = useWebSocket(socketUrl);
  const [data, setData] = useState(null);

  useEffect(() => {
    sendMessage("I want image :)");
  }, []);

  useEffect(() => {
    if (lastMessage !== null) {
      try {
        JSON.parse(lastMessage.data);
      } catch (e) {
        // it is not json, therefore its image bytes
        setData(lastMessage.data);
      }
    }
  }, [lastMessage]);

  return (
    <ModuleContainer>
      <StatusCard>Filter Preview</StatusCard>
      <StatusCard>
        {data ? (
          <img
            id="latestImage"
            style={{
              width: "calc(100% - 1em)",
              height: "fit-content",
              paddingTop: "0.5em",
              paddingBottom: "0.5em",
              transform: "rotate(180deg)"
            }}
            src={URL.createObjectURL(data)}
          />
        ) : (
          <p>Loading stream...</p>
        )}
      </StatusCard>
    </ModuleContainer>
  );
}
